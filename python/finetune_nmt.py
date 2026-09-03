from transformers import (AutoTokenizer, 
                          AutoModelForSeq2SeqLM, 
                          DataCollatorForSeq2Seq, 
                          Seq2SeqTrainingArguments, 
                          Seq2SeqTrainer)
from peft import (LoraConfig, # apply Low-Rank Adaptation (LoRA)
                  get_peft_model, 
                  TaskType)
from datasets import load_dataset
import torch
import evaluate
import numpy as np
import argparse
import os
import json

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

# part 1: load data
file_path = os.path.join(arg.path, arg.style)
data_files = {
    'train':f'{file_path}_train.json',
    'test':f'{file_path}_test.json',
    'dev':f'{file_path}_dev.json'
}
dataset = load_dataset('json', data_files=data_files)

# part 2: tokenize data
tokenizer = AutoTokenizer.from_pretrained(arg.model)
tokenizer.src_lang = arg.src_lang
tokenizer.tgt_lang = arg.tgt_lang

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

tokenized = dataset.map(preprocess, batched=True)

# part 3: finetune model
model = AutoModelForSeq2SeqLM.from_pretrained(arg.model)
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)
lora_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,
    r=8, # rank: controls adapter capacity
    lora_alpha=16, # scaling factor
    lora_dropout=0.1, # regularization
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', # query, key, value, output
                    'up_proj', 'gate_proj', 'down_proj'], # up/down vectors, gate
)
model = get_peft_model(model, lora_config).to(device)
model.print_trainable_parameters()

# 3.1: load evaluation metric models
bleu = evaluate.load('sacrebleu')
ter = evaluate.load('ter')

# original hf code use 'pred' & 'label' variables, but i renamed them to better understand what's going on
def postprocess(translations, references):
    translations = [translation.strip() for translation in translations]
    references = [[reference.strip()] for reference in references]
    return translations, references

# here i used the original hf variable names; cuz now i get it :^)
def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]

    # fixes overflow error: out of range integral conversion attempted
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
    result = {
        'ter': ter_score['score'],
        'bleu': bleu_score['score'],
    }

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result['gen_len'] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

# 3.2: define training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir=arg.output,
    num_train_epochs=5, # increased from 3 to 5
    per_device_train_batch_size=4, # decreased from 8 to 4
    per_device_eval_batch_size=4, # decreased from 8 to 4
    learning_rate=5e-5, # started at 5e-5; decreased to 1e-5; increased to 1e-4; decreased to 5e-5 again
    weight_decay=0.01,
    eval_strategy='epoch',
    save_strategy='epoch', # save the best epoch, based on 'metric_for_best_model'
    load_best_model_at_end=True,
    metric_for_best_model='bleu',
    greater_is_better=True,
    save_total_limit=1,
    predict_with_generate=True,
    generation_max_length=512,
    seed=arg.seed,
)

# 3.3: load trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized['train'],
    eval_dataset=tokenized['dev'],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# 3.4: run inference and save best model
trainer.train()
model.save_pretrained(arg.output)
tokenizer.save_pretrained(arg.output)

# for later plotting of training/validation loss decrease
with open(os.path.join(arg.output, 'training_log.json'), 'w') as f:
    json.dump(trainer.state.log_history, f)