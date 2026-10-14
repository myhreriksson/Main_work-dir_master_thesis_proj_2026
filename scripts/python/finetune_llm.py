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
parser.add_argument('--load')
parser.add_argument('--seed', type=int, default=100)
parser.add_argument('--database')
parser.add_argument('--load', default=False)
arg = parser.parse_args()

# class used for pruning
class PruningCallback(TrainerCallback):
    '''
    if, during HPO fine-tuning, an epoch displays really bad performance,
    terminate fine-tuning trial and proceed to next parameter configuration.
    '''
    def __init__(self, trial):
        self.trial = trial

    def on_evaluate(self, args, state, control, metrics, **kwargs):
        if 'eval_loss' in metrics: # use evaluation loss as pruning metric
            self.trial.report(metrics['eval_loss'], state.epoch)
            if self.trial.should_prune():
                raise optuna.TrialPruned()

def objective(trial):
    '''
    main HPO function. the following 9 vars refer to training hyper-params,
    which are tested in varying combinations during optimization.
    '''
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
        target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', # lora recommended to use all modules
                        'up_proj', 'down_proj', 'gate_proj']
    )
    model = get_peft_model(model, lora_config) # DON'T move to device

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

if arg.domain.startswith('balanced_'):
    domain = arg.domain.split('_')[1]
    prefix = f'{arg.domain.split("_")[0]}_{arg.lang}'
else:
    domain = arg.domain
    prefix = arg.lang
file_path = os.path.join(arg.input, f'{prefix}_{domain}')

# load data
data_files = {
    'train':f'{file_path}_train.json',
    'test':f'{file_path}_test.json',
    'dev':f'{file_path}_dev.json'
}
dataset = load_dataset('json', data_files=data_files)

tokenizer = AutoTokenizer.from_pretrained(arg.model) # load tokenizer
tokenizer.pad_token = tokenizer.eos_token

# sql database storing hyper-parameter combinations. load best one for final fine-tuning
storage = RDBStorage(f'sqlite:///{arg.database}/optimized_llm_hparams.db')
if arg.load == 'load':
    study = optuna.load_study(
        study_name='optimizing_hyperparams',
        storage=storage,
        pruner=optuna.pruners.MedianPruner(
            n_startup_trials=5,
            n_warmup_steps=1
        )
    )
elif arg.load == 'fresh':
    try:
        optuna.delete_study( # functions as overwriting the study every time code is run
            study_name='optimizing_hyperparams',
            storage=storage
        )
    except KeyError: # ignores if not existing
        pass
    study = optuna.create_study(
        study_name='optimizing_hyperparams',
        direction='minimize',
        storage=storage,
        load_if_exists=False,
        pruner=optuna.pruners.MedianPruner(
            n_startup_trials=5,
            n_warmup_steps=1
        )
    )
    study.optimize(objective, n_trials=20) # try setting to higher if more resource available
best_hparams = study.best_params

# finetune model
model = AutoModelForCausalLM.from_pretrained(arg.model) # load model
# define lora configurations (with best-performing hparams)
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=best_hparams['r'], 
    lora_alpha=best_hparams['alpha'], 
    lora_dropout=best_hparams['dropout'],
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 
                    'up_proj', 'gate_proj', 'down_proj'], 
)
model = get_peft_model(model, lora_config).to('cuda') # load model unto GPU with lora config
model.print_trainable_parameters()

# define training args (with best-performing hparams)
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

# load trainer
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['dev'],
    processing_class=tokenizer
)

# run inference and save best model
if __name__=='__main__':
    trainer.train()
    model.save_pretrained(arg.output)
    tokenizer.save_pretrained(arg.output)

# save best epoch
    with open(os.path.join(arg.output, 'training_log.json'), 'w') as f:
        json.dump(trainer.state.log_history, f)