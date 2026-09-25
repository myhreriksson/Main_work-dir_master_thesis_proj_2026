#!/bin/bash

# Sentence-balanced
base_1=$(bash shell/test.sh pseudo nllb base '') # get baselines on game-data (nllb-200)
base_2=$(bash shell/test.sh pseudo bart base '') # get baselines on game-data (mBart-50)
base_3=$(bash shell/test.sh archaic nllb base '') # get baselines on bible-data (nllb-200)
base_4=$(bash shell/test.sh archaic bart base '') # get baselines on bible-data (mBart-50)

post_baseline="$base_1:$base_2:$base_3:$base_4"

# Sentence-balanced
tuned_1=$(bash shell/test.sh pseudo nllb tuned '' "$post_baseline") # finetuned on bible-data, tested on game-data (nllb-200)
tuned_2=$(bash shell/test.sh pseudo bart tuned '' "$post_baseline") # finetuned on bible-data, tested on game-data (mBart-50)
tuned_3=$(bash shell/test.sh archaic nllb tuned '' "$post_baseline") # finetuned on game-data, tested on bible-data (nllb-200)
tuned_4=$(bash shell/test.sh archaic bart tuned '' "$post_baseline") # finetuned on game-data, tested on bible-data (mBart-50)

# Token-balanced
tuned_1_b=$(bash shell/test.sh pseudo nllb tuned balanced "$post_baseline") # finetuned on bible-data, tested on game-data (nllb-200)
tuned_2_b=$(bash shell/test.sh pseudo bart tuned balanced "$post_baseline") # finetuned on bible-data, tested on game-data (mBart-50)

post_finetuned="$tuned_1:$tuned_2:$tuned_3:$tuned_4"
post_finetuned_b="$tuned_1_b:$tuned_2_b"

sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo nllb '' config
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo bart '' config
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic nllb '' config
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic bart '' config

sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo nllb '' model
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo bart '' model
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic nllb '' model
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic bart '' model

sbatch --dependency=afterok:$post_finetuned_b shell/get_significance.sh pseudo nllb balanced config
sbatch --dependency=afterok:$post_finetuned_b shell/get_significance.sh pseudo bart balanced config

sbatch --dependency=afterok:$post_finetuned_b shell/get_significance.sh pseudo nllb balanced model
sbatch --dependency=afterok:$post_finetuned_b shell/get_significance.sh pseudo bart balanced model