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
import torch
from transformers import (AutoTokenizer, 
                          AutoModelForSeq2SeqLM, 
                          DataCollatorForSeq2Seq, 
                          Seq2SeqTrainingArguments, 
                          Seq2SeqTrainer)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--style')
parser.add_argument('-p', '--path')
parser.add_argument('-m', '--model')
parser.add_argument('-o', '--output')
parser.add_argument('--tgt_lang')
parser.add_argument('--src_lang')
parser.add_argument('--seed', type=int, default=100)
arg = parser.parse_args()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

#-------------------------------------------------------------------------------#
# part 0: load evaluation metrics
bleu = evaluate.load('sacrebleu')
ter = evaluate.load('ter')
comet_model = load_from_checkpoint(download_model('Unbabel/wmt22-comet-da'))

#-------------------------------------------------------------------------------#
# part 1: define functions
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

def postprocess(translations, references):
    translations = [translation.strip() for translation in translations]
    references = [[reference.strip()] for reference in references]
    return translations, references

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    preds = np.where(preds != -100, preds, tokenizer.pad_token_id)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id) 
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    decoded_preds, decoded_labels = postprocess(decoded_preds, decoded_labels)
    bleu_score = bleu.compute(
        predictions=decoded_preds, 
        references=decoded_labels
    )
    ter_score = ter.compute(
        predictions=decoded_preds,
        references=decoded_labels
    )
    comet_data = [
        {'src': src, 'mt':mt, 'ref':ref}
        for src, mt, ref in zip(dataset['dev']['en'], decoded_preds, decoded_labels)
    ]
    comet_score = comet_model.predict(
        data=comet_data,
        batch_size=8,
        gpus=1
    ).system_score
    result = {
        'ter': ter_score['score'],
        'bleu': bleu_score['score'],
        'comet': comet_score
    }
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result['gen_len'] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

def optuna_metric(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    preds = np.where(preds != -100, preds, tokenizer.pad_token_id)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id) 
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    decoded_preds, decoded_labels = postprocess(decoded_preds, decoded_labels)
    bleu_score = bleu.compute(
        predictions=decoded_preds, 
        references=decoded_labels
    )
    result = {'bleu': bleu_score['score']}
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result['gen_len'] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

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
    return

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
storage = RDBStorage("sqlite:///optimized_hyper_params.db") # make sql database
study = optuna.create_study(
    study_name="optimizing_nmt_params",
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
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', # query, key, value, output
                    'up_proj', 'down_proj', 'gate_proj'], # up/down vectors, gate
)
model = get_peft_model(model, lora_config).to(device)
model.print_trainable_parameters()

# 5.1: define training arguments
training_args = Seq2SeqTrainingArguments(
    generation_max_length=512,
    output_dir=arg.output,
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
    metric_for_best_model='bleu',
    greater_is_better=True,
    save_total_limit=1,
    predict_with_generate=True,
    run_name='optimizing_nmt_params',
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