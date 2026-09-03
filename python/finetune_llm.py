from transformers import (AutoTokenizer, 
                          AutoModelForCausalLM)
from trl import (SFTConfig, 
                 SFTTrainer)
from peft import (LoraConfig, # apply Low-Rank Adaptation (LoRA)
                  get_peft_model, 
                  TaskType)
from datasets import load_dataset
import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model')
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-d', '--domain')
parser.add_argument('-l', '--lang')
parser.add_argument('--seed', type=int, default=100)
arg = parser.parse_args()

file_path = os.path.join(arg.input, f'{arg.lang}_{arg.domain}')
# part 1: load data
data_files = {
    'train':f'{file_path}_train.json',
    'test':f'{file_path}_test.json',
    'dev':f'{file_path}_dev.json'
}
dataset = load_dataset('json', data_files=data_files)

# part 2: tokenize data
tokenizer = AutoTokenizer.from_pretrained(arg.model)
tokenizer.pad_token = tokenizer.eos_token

# part 3: finetune model
model = AutoModelForCausalLM.from_pretrained(arg.model)
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8, # rank: controls adapter capacity
    lora_alpha=16, # scaling factor
    lora_dropout=0.1, # regularization
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', # query, key, value, output
                    'up_proj', 'gate_proj', 'down_proj'], # up/down vectors, gate
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 3.1: define training arguments
training_args = SFTConfig(
    max_length=512,
    output_dir=arg.output,
    num_train_epochs=5,
    per_device_train_batch_size=4, 
    per_device_eval_batch_size=4, 
    learning_rate=5e-5, 
    weight_decay=0.01,
    eval_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='eval_loss',
    greater_is_better=False,
    save_total_limit=1,
    seed=arg.seed
)

# 3.2: load trainer
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['dev'],
    processing_class=tokenizer
)

# 3.3: run inference and save best model
trainer.train()
model.save_pretrained(arg.output)
tokenizer.save_pretrained(arg.output)

# for later plotting of training/validation loss decrease
with open(os.path.join(arg.output, 'training_log.json'), 'w') as f:
    json.dump(trainer.state.log_history, f)