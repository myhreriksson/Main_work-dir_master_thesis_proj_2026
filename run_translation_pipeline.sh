#!/bin/bash

#----------Sentence-balanced BASELINES
base_1=$(bash scripts/shell/test.sh game nllb base '') # get baselines on game-data (NLLB-200)
base_2=$(bash scripts/shell/test.sh game bart base '') # get baselines on game-data (mBART-50)

base_3=$(bash scripts/shell/test.sh bible nllb base '') # get baselines on bible-data (NLLB-200)
base_4=$(bash scripts/shell/test.sh bible bart base '') # get baselines on bible-data (mBART-50)

base_5=$(bash scripts/shell/test.sh flores nllb base '') # get baseline-comparison on flores_200 (NLLB-200)
base_6=$(bash scripts/shell/test.sh flores bart base '') # get baseline-comparison on flores_200 (mBART-50)

post_baseline="$base_1:$base_2:$base_3:$base_4:$base_5:$base_6" # collective conditional

#----------Sentence-balanced (aka unbalanced) FINETUNED
bash scripts/shell/test.sh bible nllb tuned unbalanced "$post_baseline" # tuned on game, tested on bible (NLLB-200)
bash scripts/shell/test.sh bible bart tuned unbalanced "$post_baseline" # tuned on game, tested on bible (mBART-50)

bash scripts/shell/test.sh game nllb tuned unbalanced "$post_baseline" # tuned on unb_bible, tested on game (NLLB-200)
bash scripts/shell/test.sh game bart tuned unbalanced "$post_baseline" # tuned on unb_bible, tested on game (mBART-50)

#----------Token-balanced FINETUNED
bash scripts/shell/test.sh game nllb tuned balanced "$post_baseline" # tuned on bal_bible, tested on game (NLLB-200)
bash scripts/shell/test.sh game bart tuned balanced "$post_baseline" # tuned on bal_bible, tested on game (mBART-50)