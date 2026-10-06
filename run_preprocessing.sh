#!/bin/bash

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

# Retrieves all (except GAME) data & performs sentence tokenization
bash shell/process_data.sh bible 
bash shell/process_data.sh prose 

# Prepares data for NMT task
bash shell/prepare_data.sh nmt game
bash shell/prepare_data.sh nmt bible

# prepares data for PPL task
bash shell/prepare_data.sh llm prose eng
bash shell/prepare_data.sh llm prose deu

# makes training splits for NMT task
bash shell/get_splits.sh nmt game 
bash shell/get_splits.sh nmt bible 

# makes training splits for PPL task
bash shell/get_splits.sh llm bible eng 
bash shell/get_splits.sh llm prose eng 
bash shell/get_splits.sh llm bible deu 
bash shell/get_splits.sh llm prose deu 

#------------------------------------------#
# make token-balanced vers of split data for NMT task
bash shell/get_balanced.sh train eng 
bash shell/get_balanced.sh test eng
bash shell/get_balanced.sh dev eng
bash shell/get_balanced.sh train deu
bash shell/get_balanced.sh test deu
bash shell/get_balanced.sh dev deu