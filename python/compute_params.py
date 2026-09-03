from transformers import (AutoModelForSeq2SeqLM,
                          AutoModelForCausalLM)
import sys

if sys.argv[1] == 'qwen':
    AutoModel = AutoModelForCausalLM
else:
    AutoModel = AutoModelForSeq2SeqLM

model = AutoModel.from_pretrained(
    f'models/base/{sys.argv[1]}'
)

print(f'{sum(p.numel() for p in model.parameters()):,}')