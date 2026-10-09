#!/bin/bash

# fine-tune NMT
bash scripts/shell/args4train.sh nmt nllb game 
bash scripts/shell/args4train.sh nmt bart game 
bash scripts/shell/args4train.sh nmt nllb bible # uses unbalanced bible
bash scripts/shell/args4train.sh nmt bart bible # uses unbalanced bible
bash scripts/shell/args4train.sh nmt nllb bible "" balanced_ # uses balanced bible 
bash scripts/shell/args4train.sh nmt bart bible "" balanced_ # uses balanced bible 

# fine-tune LLM
sbatch scripts/shell/train.sh llm qwen prose eng 
sbatch scripts/shell/train.sh llm qwen prose deu 
sbatch scripts/shell/train.sh llm qwen bible eng # uses unbalanced bible
sbatch scripts/shell/train.sh llm qwen bible deu # uses unbalanced bible
sbatch scripts/shell/train.sh llm qwen bible eng balanced_ # uses balanced bible 
sbatch scripts/shell/train.sh llm qwen bible deu balanced_ # uses balanced bible 