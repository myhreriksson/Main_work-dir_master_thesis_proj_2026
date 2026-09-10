import argparse
from comet import (download_model, load_from_checkpoint)
from datasets import load_dataset
import evaluate
import json
import numpy as np
import optuna
from optuna.storages import RDBStorage
import os
from peft import (LoraConfig, get_peft_model, TaskType)
from transformers import (AutoTokenizer, 
                          AutoModelForSeq2SeqLM, 
                          DataCollatorForSeq2Seq, 
                          Seq2SeqTrainingArguments, 
                          Seq2SeqTrainer,
                          TrainerCallback)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--style')
parser.add_argument('-p', '--path')
parser.add_argument('-m', '--model')
parser.add_argument('-o', '--output')
parser.add_argument('--tgt_lang')
parser.add_argument('--src_lang')
parser.add_argument('--seed', type=int, default=100)
arg = parser.parse_args()

#-------------------------------------------------------------------------------#
# part 0: load evaluation metrics
bleu = evaluate.load('sacrebleu')
ter = evaluate.load('ter')
comet_model = load_from_checkpoint(download_model('Unbabel/wmt22-comet-da')).to('cuda:1')

#-------------------------------------------------------------------------------#
# part 1: define functions
class PruningCallback(TrainerCallback):
    def __init__(self, trial):
        self.trial = trial
        
    def on_evaluate(self, args, state, control, metrics, **kwargs):
        if 'eval_bleu' in metrics:
            self.trial.report(metrics['eval_bleu'], state.epoch)
            if self.trial.should_prune():
                raise optuna.TrialPruned()

def preprocess(examples):
    inputs = examples['en']
    targets = examples['de']
    model_inputs = tokenizer(
        inputs,
        text_target=targets, 
        max_length=512, 
        truncation=True
    )
    return model_inputs

def postprocess(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]
    return preds, labels

def decode(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    preds = np.where(preds != -100, preds, tokenizer.pad_token_id)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id) 
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    decoded_preds, decoded_labels = postprocess(decoded_preds, decoded_labels)
    return decoded_preds, decoded_labels

def get_sacrebleu(preds, labels):
    bleu_score = bleu.compute(
        predictions=preds, 
        references=labels
    )
    ter_score = ter.compute(
        predictions=preds,
        references=labels
    )
    result = {
        'ter': ter_score['score'],
        'bleu': bleu_score['score'],
    }
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result['gen_len'] = np.mean(prediction_lens)
    result = {key: f'{val:.4f}' for key, val in result.items()}
    return result

def get_comet(preds, labels):
    comet_data = [
        {'src': src, 'mt':mt, 'ref':ref}
        for src, mt, ref in zip(dataset['dev']['en'], preds, labels)
    ]
    result = comet_model.predict(
        data=comet_data,
        batch_size=8
    ).system_score
    return result

def combine_metrics(sacrebleu, comet):
    result = {
        'ter': sacrebleu['ter'],
        'bleu': sacrebleu['bleu'],
        'comet': comet
    }
    return result

def compute_metrics(eval_preds):
    preds, labels = decode(eval_preds)
    sacrebleu = get_sacrebleu(preds, labels)
    comet = get_comet(preds, labels)
    return combine_metrics(sacrebleu, comet)

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

    model = AutoModelForSeq2SeqLM.from_pretrained(arg.model)
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)
    lora_config = LoraConfig(
        task_type=TaskType.SEQ_2_SEQ_LM,
        r=r,
        lora_alpha=alpha,
        lora_dropout=dropout,
        target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 
                        'up_proj', 'down_proj', 'gate_proj'], 
    )
    model = get_peft_model(model, lora_config).to('cuda:0')

    training_args = Seq2SeqTrainingArguments(
        output_dir=arg.output,
        generation_max_length=512,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        warmup_ratio=warmup_ratio,
        lr_scheduler_type=scheduler,
        num_train_epochs=num_train_epochs,
        eval_strategy='epoch',
        save_strategy='no',
        metric_for_best_model='bleu',
        greater_is_better=True,
        predict_with_generate=True,
        seed=arg.seed
    )
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized['train'],
        eval_dataset=tokenized['dev'],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=get_sacrebleu,
        callbacks=[PruningCallback(trial)]
    )
    trainer.train()
    metrics = trainer.evaluate()
    return float(metrics['eval_bleu'])

#-------------------------------------------------------------------------------#
# part 2: load data
file_path = os.path.join(arg.path, arg.style)
data_files = {
    'train':f'{file_path}_train.json',
    'test':f'{file_path}_test.json',
    'dev':f'{file_path}_dev.json'
}
dataset = load_dataset('json', data_files=data_files)

#-------------------------------------------------------------------------------#
# part 3: tokenize data
tokenizer = AutoTokenizer.from_pretrained(arg.model)
tokenizer.src_lang = arg.src_lang
tokenizer.tgt_lang = arg.tgt_lang
tokenized = dataset.map(preprocess, batched=True)

#-------------------------------------------------------------------------------#
# part 4: parameter optimization
storage = RDBStorage("sqlite:///optimized_nmt_hparams.db")
study = optuna.create_study(
    study_name="optimizing_hyperparams",
    direction="maximize",
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
model = AutoModelForSeq2SeqLM.from_pretrained(arg.model)
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)
lora_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,
    r=best_hparams['r'],
    lora_alpha=best_hparams['alpha'],
    lora_dropout=best_hparams['dropout'],
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 
                    'up_proj', 'down_proj', 'gate_proj'], 
)
model = get_peft_model(model, lora_config).to('cuda:0')
model.print_trainable_parameters()

# 5.1: define training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir=arg.output,
    generation_max_length=512,
    num_train_epochs=best_hparams['num_train_epochs'],
    per_device_train_batch_size=best_hparams['batch_size'],
    per_device_eval_batch_size=best_hparams['batch_size'],
    learning_rate=best_hparams['learning_rate'], 
    weight_decay=best_hparams['weight_decay'],
    warmup_ratio=best_hparams['warmup_ratio'],
    lr_scheduler_type=best_hparams['scheduler'],
    eval_strategy='epoch',
    save_strategy='epoch',
    metric_for_best_model='bleu',
    load_best_model_at_end=True,
    greater_is_better=True,
    predict_with_generate=True,
    save_total_limit=1,
    run_name='optimizing_hyperparams',
    seed=arg.seed,
)

# 5.2: load trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized['train'],
    eval_dataset=tokenized['dev'],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# 5.3: run inference and save best model
trainer.train()
model.save_pretrained(arg.output)
tokenizer.save_pretrained(arg.output)

#-------------------------------------------------------------------------------#
# part 6: save best epoch
with open(os.path.join(arg.output, 'training_log.json'), 'w') as f:
    json.dump(trainer.state.log_history, f)