#!/bin/bash

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
bash shell/get_splits.sh nmt pseudo 
bash shell/get_splits.sh nmt archaic 

# makes training splits for PPL task
bash shell/get_splits.sh llm bible eng 
bash shell/get_splits.sh llm prose eng 
bash shell/get_splits.sh llm bible deu 
bash shell/get_splits.sh llm prose deu 

#------------------------------------------#
# make token-balanced vers of split data for NMT task
bash shell/balance_token_count.sh train eng 
bash shell/balance_token_count.sh test eng
bash shell/balance_token_count.sh dev eng
bash shell/balance_token_count.sh train deu
bash shell/balance_token_count.sh test deu
bash shell/balance_token_count.sh dev deu