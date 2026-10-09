#!/bin/bash

#----------Sentence-balanced BASELINES
base_1=$(bash scripts/shell/test.sh game nllb base '') # get baselines on game-data (NLLB-200)
base_2=$(bash scripts/shell/test.sh game bart base '') # get baselines on game-data (mBART-50)

base_3=$(bash scripts/shell/test.sh bible nllb base '') # get baselines on bible-data (NLLB-200)
base_4=$(bash scripts/shell/test.sh bible bart base '') # get baselines on bible-data (mBART-50)

base_5=$(bash scripts/shell/test.sh flores nllb base '') # get benchmark on flores_200 (NLLB-200)
base_6=$(bash scripts/shell/test.sh flores bart base '') # get benchmark on flores_200 (mBART-50)

post_baseline="$base_1:$base_2:$base_3:$base_4:$base_5:$base_6" # collective conditional

#----------Sentence-balanced (aka unbalanced) FINETUNED
tuned_1U=$(bash scripts/shell/test.sh bible nllb tuned unbalanced "$post_baseline") # tuned on game, tested on bible (NLLB-200)
tuned_2U=$(bash scripts/shell/test.sh bible bart tuned unbalanced "$post_baseline") # tuned on game, tested on bible (mBART-50)

tuned_3U=$(bash scripts/shell/test.sh game nllb tuned unbalanced "$post_baseline") # tuned on unb_bible, tested on game (NLLB-200)
tuned_4U=$(bash scripts/shell/test.sh game bart tuned unbalanced "$post_baseline") # tuned on unb_bible, tested on game (mBART-50)

post_finetuned_U="$tuned_1U:$tuned_2U:$tuned_3U:$tuned_4U" # collective conditional unbalanced

#----------Token-balanced FINETUNED
tuned_1B=$(bash scripts/shell/test.sh game nllb tuned balanced "$post_baseline") # tuned on bal_bible, tested on game (NLLB-200)
tuned_2B=$(bash scripts/shell/test.sh game bart tuned balanced "$post_baseline") # tuned on bal_bible, tested on game (mBART-50)

post_finetuned_B="$tuned_1B:$tuned_2B" # collective conditional balanced

#----------Significance testing WITHIN models (compares change from baseline per model)
sbatch --dependency=afterok:$post_finetuned_U scripts/shell/get_pvals.sh game nllb unbalanced config 
sbatch --dependency=afterok:$post_finetuned_U scripts/shell/get_pvals.sh game bart unbalanced config 
sbatch --dependency=afterok:$post_finetuned_U scripts/shell/get_pvals.sh bible nllb '' config 
sbatch --dependency=afterok:$post_finetuned_U scripts/shell/get_pvals.sh bible bart '' config
sbatch --dependency=afterok:$post_finetuned_B scripts/shell/get_pvals.sh game nllb balanced config 
sbatch --dependency=afterok:$post_finetuned_B scripts/shell/get_pvals.sh game bart balanced config 

#----------Significance testing ACROSS models (compares change between models per config) 
sbatch --dependency=afterok:$post_finetuned_U scripts/shell/get_pvals.sh game bart unbalanced model 
sbatch --dependency=afterok:$post_finetuned_U scripts/shell/get_pvals.sh bible bart '' model 
sbatch --dependency=afterok:$post_finetuned_B scripts/shell/get_pvals.sh game bart balanced model 
# OBS! since comparison between models is the same regardless of model input, bart was arbitrarily selected