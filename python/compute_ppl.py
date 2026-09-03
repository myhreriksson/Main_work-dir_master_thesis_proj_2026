from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
import argparse
import torch
import os

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model')
parser.add_argument('-o', '--output')
parser.add_argument('-l', '--lang')
arg = parser.parse_args()

# part 1: load model & tokenizer
device = 'cuda' if torch.cuda.is_available() else 'cpu' # device to GPU if possible

tokenizer = AutoTokenizer.from_pretrained(arg.model)
model = AutoModelForCausalLM.from_pretrained(arg.model, 
                                             device_map=device, 
                                             attn_implementation='sdpa',
                                             dtype=torch.float16)

# part 2: load data
if arg.lang == 'eng':
    LANG = 'EN'
elif arg.lang == 'deu':
    LANG = 'DE'
test_file = os.path.join(f'data/_test-n-finetune_/pseudo_{arg.lang}/game_{LANG}.txt')

with open(test_file, 'r', encoding='utf-8') as f:
    txt = f.read()

encodings = tokenizer(txt, return_tensors='pt')

# part 3: compute perplexity
stride = 512
seq_len = encodings.input_ids.size(1)
max_len = stride * 8

nll_sum = 0.0
n_tokens = 0
prev_end_loc = 0
for start_loc in tqdm(range(0, seq_len, stride)):
    end_loc = min(start_loc + max_len, seq_len)
    tgt_len = end_loc - prev_end_loc
    inp_ids = encodings.input_ids[:, start_loc:end_loc].to(device)
    tgt_ids = inp_ids.clone()
    tgt_ids[:, :-tgt_len] = -100

    with torch.no_grad():
        output = model(inp_ids, labels=tgt_ids)
        neg_log_likelihood = output.loss

    num_valid_tokens = (tgt_ids != -100).sum().item()
    batch_size = tgt_ids.size(0)
    num_loss_tokens = num_valid_tokens - batch_size
    nll_sum += neg_log_likelihood * num_loss_tokens
    n_tokens += num_loss_tokens

    prev_end_loc = end_loc
    if end_loc == seq_len:
        break

avg_nll = nll_sum / n_tokens
ppl = torch.exp(avg_nll)
with open(os.path.join(arg.output, f'ppl_{LANG}.txt'), 'w', encoding='utf-8') as f:
    f.write(f'PPL: {ppl.item():.4f}')