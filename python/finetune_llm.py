import argparse
from datasets import load_dataset
import json
import optuna
from optuna.storages import RDBStorage
import os
from peft import (LoraConfig, get_peft_model, TaskType)
from transformers import (AutoTokenizer, 
                          AutoModelForCausalLM,
                          TrainerCallback)
from trl import (SFTConfig, SFTTrainer)

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model')
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-d', '--domain')
parser.add_argument('-l', '--lang')
parser.add_argument('--seed', type=int, default=100)
parser.add_argument('--database')
arg = parser.parse_args()

#-------------------------------------------------------------------------------#
# part 1: define functions
class PruningCallback(TrainerCallback):
    def __init__(self, trial):
        self.trial = trial

    def on_evaluate(self, args, state, control, metrics, **kwargs):
        if 'eval_loss' in metrics:
            self.trial.report(metrics['eval_loss'], state.epoch)
            if self.trial.should_prune():
                raise optuna.TrialPruned()

def objective(trial):
    r = trial.suggest_categorical('r', [4, 8, 16, 32])
    alpha = trial.suggest_categorical('alpha', [8, 16, 32, 64])
    dropout = trial.suggest_float('dropout', 0.0, 0.3)
    learning_rate = trial.suggest_float('learning_rate', 1e-6, 1e-4, log=True)
    weight_decay = trial.suggest_float('weight_decay', 1e-5, 0.1, log=True)
    warmup_ratio = trial.suggest_float('warmup_ratio', 0.0, 0.2)
    scheduler = trial.suggest_categorical('scheduler', ['linear', 'cosine'])
    num_train_epochs = trial.suggest_int('num_train_epochs', 2, 10)
    batch_size = trial.suggest_categorical('batch_size', [2, 4, 8])

    model = AutoModelForCausalLM.from_pretrained(arg.model)
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=r,
        lora_alpha=alpha,
        lora_dropout=dropout,
        target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj',
                        'up_proj', 'down_proj', 'gate_proj']
    )
    model = get_peft_model(model, lora_config) # don't move to device for parallel data training

    training_args = SFTConfig(
        output_dir=arg.output,
        max_length=512,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        warmup_ratio=warmup_ratio,
        lr_scheduler_type=scheduler,
        eval_strategy='epoch',
        save_strategy='no',
        metric_for_best_model='eval_loss',
        greater_is_better=False,
        seed=arg.seed
    )
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],
        eval_dataset=dataset['dev'],
        processing_class=tokenizer,
        callbacks=[PruningCallback(trial)]
    )
    trainer.train()
    metrics = trainer.evaluate()
    return metrics['eval_loss']

#-------------------------------------------------------------------------------#
# part 2: load data
file_path = os.path.join(arg.input, f'{arg.domain}_{arg.lang}')
data_files = {
    'train':f'{file_path}_train.json',
    'test':f'{file_path}_test.json',
    'dev':f'{file_path}_dev.json'
}
dataset = load_dataset('json', data_files=data_files)

#-------------------------------------------------------------------------------#
# part 3: tokenize data
tokenizer = AutoTokenizer.from_pretrained(arg.model)
tokenizer.pad_token = tokenizer.eos_token

#-------------------------------------------------------------------------------#
# part 4: parameter optimization
storage = RDBStorage(f'sqlite:///{arg.database}/optimized_llm_hparams.db')
study = optuna.create_study(
    study_name='optimizing_hyperparams',
    direction='minimize',
    storage=storage,
    load_if_exists=True,
    pruner=optuna.pruners.MedianPruner(
        n_startup_trials=5,
        n_warmup_steps=1
    )
)
study.optimize(objective, n_trials=20) # might set to 50 if runs smoothly
best_hparams = study.best_params

#-------------------------------------------------------------------------------#
# part 5: finetune model
model = AutoModelForCausalLM.from_pretrained(arg.model)
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=best_hparams['r'], 
    lora_alpha=best_hparams['alpha'], 
    lora_dropout=best_hparams['dropout'],
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 
                    'up_proj', 'gate_proj', 'down_proj'], 
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 5.1: define training arguments
training_args = SFTConfig(
    output_dir=arg.output,
    max_length=512,
    num_train_epochs=best_hparams['num_train_epochs'],
    per_device_train_batch_size=best_hparams['batch_size'], 
    per_device_eval_batch_size=best_hparams['batch_size'], 
    learning_rate=best_hparams['learning_rate'], 
    weight_decay=best_hparams['weight_decay'],
    warmup_ratio=best_hparams['warmup_ratio'],
    lr_scheduler_type=best_hparams['scheduler'],
    eval_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='eval_loss',
    greater_is_better=False,
    save_total_limit=1,
    run_name='optimizing_hyperparams',
    seed=arg.seed
)

# 5.2: load trainer
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['dev'],
    processing_class=tokenizer
)

# 5.3: run inference and save best model
trainer.train()
model.save_pretrained(arg.output)
tokenizer.save_pretrained(arg.output)

#-------------------------------------------------------------------------------#
# part 6: save best epoch
with open(os.path.join(arg.output, 'training_log.json'), 'w') as f:
    json.dump(trainer.state.log_history, f)