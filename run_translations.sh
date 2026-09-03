#!/bin/bash

base_1=$(bash shell/test.sh pseudo nllb base) # get baselines on game-data (nllb-200)
base_2=$(bash shell/test.sh pseudo bart base) # get baselines on game-data (mBart-50)
base_3=$(bash shell/test.sh archaic nllb base) # get baselines on bible-data (nllb-200)
base_4=$(bash shell/test.sh archaic bart base) # get baselines on bible-data (mBart-50)

post_baseline="$base_1:$base_2:$base_3:$base_4"

tuned_1=$(bash shell/test.sh pseudo nllb tuned "$post_baseline") # finetuned on game-data, tested on bible-data (nllb-200)
tuned_2=$(bash shell/test.sh pseudo bart tuned "$post_baseline") # finetuned on game-data, tested on bible-data (mBart-50)
tuned_3=$(bash shell/test.sh archaic nllb tuned "$post_baseline") # finetuned on bible-data, tested on game-data (nllb-200)
tuned_4=$(bash shell/test.sh archaic bart tuned "$post_baseline") # finetuned on bible-data, tested on game-data (mBart-50)

post_finetuned="$tuned_1:$tuned_2:$tuned_3:$tuned_4"

sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo nllb
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh pseudo bart
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic nllb
sbatch --dependency=afterok:$post_finetuned shell/get_significance.sh archaic bart