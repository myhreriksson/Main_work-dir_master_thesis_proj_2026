#!/bin/bash

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

# Retrieves all (except GAME) data & performs sentence tokenization
bash scripts/shell/process_data.sh bible 
bash scripts/shell/process_data.sh prose 

# Prepares data for NMT task
bash scripts/shell/prepare_data.sh nmt game
bash scripts/shell/prepare_data.sh nmt bible

# prepares data for PPL task
bash scripts/shell/prepare_data.sh llm prose eng
bash scripts/shell/prepare_data.sh llm prose deu

# makes training splits for NMT task
bash scripts/shell/get_splits.sh nmt game 
bash scripts/shell/get_splits.sh nmt bible 

# makes training splits for PPL task
bash scripts/shell/get_splits.sh llm bible eng 
bash scripts/shell/get_splits.sh llm prose eng 
bash scripts/shell/get_splits.sh llm bible deu 
bash scripts/shell/get_splits.sh llm prose deu 

#------------------------------------------#
# make token-balanced vers of split data for NMT task
bash scripts/shell/get_balanced_sents.sh train eng 
bash scripts/shell/get_balanced_sents.sh test eng
bash scripts/shell/get_balanced_sents.sh dev eng
bash scripts/shell/get_balanced_sents.sh train deu
bash scripts/shell/get_balanced_sents.sh test deu
bash scripts/shell/get_balanced_sents.sh dev deu