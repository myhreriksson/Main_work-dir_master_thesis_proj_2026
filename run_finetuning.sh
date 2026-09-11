#!/bin/bash

# Sentence-balanced
sbatch shell/train.sh nmt nllb archaic _
sbatch shell/train.sh nmt nllb pseudo _
sbatch shell/train.sh nmt bart archaic _
sbatch shell/train.sh nmt bart pseudo _
sbatch shell/train.sh llm qwen archaic eng _
sbatch shell/train.sh llm qwen prose eng _
sbatch shell/train.sh llm qwen archaic deu _
sbatch shell/train.sh llm qwen prose deu _

# Token-balanced
sbatch shell/train.sh nmt nllb archaic balanced
sbatch shell/train.sh nmt nllb pseudo balanced
sbatch shell/train.sh nmt bart archaic balanced
sbatch shell/train.sh nmt bart pseudo balanced
sbatch shell/train.sh llm qwen archaic eng balanced
sbatch shell/train.sh llm qwen prose eng balanced
sbatch shell/train.sh llm qwen archaic deu balanced
sbatch shell/train.sh llm qwen prose deu balanced