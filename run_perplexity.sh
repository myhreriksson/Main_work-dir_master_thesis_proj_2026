#!/bin/bash

# Get PPL baselines
sbatch shell/get_perplexity.sh base '' eng '' game
sbatch shell/get_perplexity.sh base '' deu '' game

sbatch shell/get_perplexity.sh base '' eng '' flores
sbatch shell/get_perplexity.sh base '' deu '' flores

# Get PPL fine-tuned
sbatch shell/get_perplexity.sh tuned bible eng '' game
sbatch shell/get_perplexity.sh tuned prose eng '' game
sbatch shell/get_perplexity.sh tuned bible deu '' game
sbatch shell/get_perplexity.sh tuned prose deu '' game

# Get PPL fine-tuned on balanced bible
sbatch shell/get_perplexity.sh tuned bible eng balanced_ game
sbatch shell/get_perplexity.sh tuned bible deu balanced_ game

