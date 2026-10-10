#!/bin/bash

# Get PPL baselines
sbatch scripts/shell/get_ppl.sh base '' eng '' game
sbatch scripts/shell/get_ppl.sh base '' deu '' game

sbatch scripts/shell/get_ppl.sh base '' eng '' flores
sbatch scripts/shell/get_ppl.sh base '' deu '' flores

# Get PPL fine-tuned
sbatch scripts/shell/get_ppl.sh tuned bible eng '' game
sbatch scripts/shell/get_ppl.sh tuned prose eng '' game
sbatch scripts/shell/get_ppl.sh tuned bible deu '' game
sbatch scripts/shell/get_ppl.sh tuned prose deu '' game

# Get PPL fine-tuned on balanced bible
sbatch scripts/shell/get_ppl.sh tuned bible eng balanced_ game
sbatch scripts/shell/get_ppl.sh tuned bible deu balanced_ game