#!/bin/bash

# Get PPL baselines
sbatch shell/get_perplexity.sh base '' eng ''
sbatch shell/get_perplexity.sh base '' deu ''

# Get PPL fine-tuned
sbatch shell/get_perplexity.sh tuned bible eng ''
sbatch shell/get_perplexity.sh tuned prose eng '' 
sbatch shell/get_perplexity.sh tuned bible deu ''
sbatch shell/get_perplexity.sh tuned prose deu ''

# Get PPL fine-tuned on balanced bible
sbatch shell/get_perplexity.sh tuned bible eng balanced_
sbatch shell/get_perplexity.sh tuned bible deu balanced_