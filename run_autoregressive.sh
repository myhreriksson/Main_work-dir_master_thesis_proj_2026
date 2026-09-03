#!/bin/bash

# sbatch shell/get_perplexity.sh base _ eng
# sbatch shell/get_perplexity.sh base _ deu

sbatch shell/get_perplexity.sh tuned bible eng
sbatch shell/get_perplexity.sh tuned prose eng
sbatch shell/get_perplexity.sh tuned bible deu
sbatch shell/get_perplexity.sh tuned prose deu