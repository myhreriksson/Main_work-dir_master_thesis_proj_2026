#!/bin/bash

# fine-tune NMT
bash shell/arg_for_train.sh nmt nllb game 
bash shell/arg_for_train.sh nmt bart game 
bash shell/arg_for_train.sh nmt nllb bible # uses unbalanced bible
bash shell/arg_for_train.sh nmt bart bible # uses unbalanced bible
bash shell/arg_for_train.sh nmt nllb bible "" balanced_ # uses balanced bible 
bash shell/arg_for_train.sh nmt bart bible "" balanced_ # uses balanced bible 

# fine-tune LLM
sbatch shell/train.sh llm qwen prose eng 
sbatch shell/train.sh llm qwen prose deu 
sbatch shell/train.sh llm qwen bible eng # uses unbalanced bible
sbatch shell/train.sh llm qwen bible deu # uses unbalanced bible
sbatch shell/train.sh llm qwen bible eng balanced_ # uses balanced bible 
sbatch shell/train.sh llm qwen bible deu balanced_ # uses balanced bible 