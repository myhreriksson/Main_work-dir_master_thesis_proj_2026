#!/bin/bash

# Sentence-balanced
base_1=$(bash shell/test.sh pseudo nllb base _) # get baselines on game-data (nllb-200)
base_2=$(bash shell/test.sh pseudo bart base _) # get baselines on game-data (mBart-50)
base_3=$(bash shell/test.sh archaic nllb base _) # get baselines on bible-data (nllb-200)
base_4=$(bash shell/test.sh archaic bart base _) # get baselines on bible-data (mBart-50)

# Token-balanced
base_1_b=$(bash shell/test.sh archaic nllb base balanced) # get baselines on bible-data (nllb-200)
base_2_b=$(bash shell/test.sh archaic bart base balanced) # get baselines on bible-data (mBart-50)

post_baseline="$base_1:$base_2:$base_3:$base_4"
post_baseline_b="$base_1_b:$base_2_b"

# Sentence-balanced
tuned_1=$(bash shell/test.sh pseudo nllb tuned _ "$post_baseline") # finetuned on game-data, tested on bible-data (nllb-200)
tuned_2=$(bash shell/test.sh pseudo bart tuned _ "$post_baseline") # finetuned on game-data, tested on bible-data (mBart-50)
tuned_3=$(bash shell/test.sh archaic nllb tuned _ "$post_baseline") # finetuned on bible-data, tested on game-data (nllb-200)
tuned_4=$(bash shell/test.sh archaic bart tuned _ "$post_baseline") # finetuned on bible-data, tested on game-data (mBart-50)

# Token-balanced
tuned_1_b=$(bash shell/test.sh archaic nllb tuned balanced "$post_baseline_b") # finetuned on bible-data, tested on game-data (nllb-200)
tuned_2_b=$(bash shell/test.sh archaic bart tuned balanced "$post_baseline_b") # finetuned on bible-data, tested on game-data (mBart-50)

post_finetuned="$tuned_1:$tuned_2:$tuned_3:$tuned_4"
post_finetuned_b="$tuned_1:$tuned_2"

sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo nllb _
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo bart _
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic nllb _
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic bart _

sbatch --dependency=afterok:$post_finetuned_b shell/get_significance.sh archaic nllb balanced
sbatch --dependency=afterok:$post_finetuned_b shell/get_significance.sh archaic bart balanced