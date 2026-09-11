#!/bin/bash

# Sentence-balanced
sbatch shell/train.sh nmt nllb archaic 
sbatch shell/train.sh nmt nllb pseudo 
sbatch shell/train.sh nmt bart archaic 
sbatch shell/train.sh nmt bart pseudo 
sbatch shell/train.sh llm qwen archaic eng 
sbatch shell/train.sh llm qwen prose eng 
sbatch shell/train.sh llm qwen archaic deu 
sbatch shell/train.sh llm qwen prose deu 

# Token-balanced
sbatch shell/train.sh nmt nllb archaic balanced
sbatch shell/train.sh nmt bart archaic balanced
sbatch shell/train.sh llm qwen archaic eng balanced
sbatch shell/train.sh llm qwen archaic deu balanced