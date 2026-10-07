#!/bin/bash

# Get PPL baselines
sbatch shell/get_ppl.sh base '' eng '' game
sbatch shell/get_ppl.sh base '' deu '' game

sbatch shell/get_ppl.sh base '' eng '' flores
sbatch shell/get_ppl.sh base '' deu '' flores

# Get PPL fine-tuned
sbatch shell/get_ppl.sh tuned bible eng '' game
sbatch shell/get_ppl.sh tuned prose eng '' game
sbatch shell/get_ppl.sh tuned bible deu '' game
sbatch shell/get_ppl.sh tuned prose deu '' game

# Get PPL fine-tuned on balanced bible
sbatch shell/get_ppl.sh tuned bible eng balanced_ game
sbatch shell/get_ppl.sh tuned bible deu balanced_ game

