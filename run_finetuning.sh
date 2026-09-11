#!/bin/bash

# fine-tune NMT
sbatch shell/train.sh nmt nllb archaic 
sbatch shell/train.sh nmt nllb pseudo 
sbatch shell/train.sh nmt bart archaic 
sbatch shell/train.sh nmt bart pseudo 
sbatch shell/train.sh nmt nllb archaic balanced # use token-balanced
sbatch shell/train.sh nmt bart archaic balanced # use token-balanced

# fine-tune LLM
sbatch shell/train.sh llm qwen archaic eng 
sbatch shell/train.sh llm qwen prose eng 
sbatch shell/train.sh llm qwen archaic deu 
sbatch shell/train.sh llm qwen prose deu 
sbatch shell/train.sh llm qwen archaic eng balanced # use token-balanced
sbatch shell/train.sh llm qwen archaic deu balanced # use token-balanced