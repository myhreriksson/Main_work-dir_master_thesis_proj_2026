#!/bin/bash

# Retrieves all data (except GAME data) & performs sentence tokenization
bash shell/process_data.sh bible 
bash shell/process_data.sh prose 

# Prepares data for NMT task
bash shell/prepare_data.sh nmt game
bash shell/prepare_data.sh nmt bible

# prepares data for PPL task
bash shell/prepare_data.sh llm prose eng
bash shell/prepare_data.sh llm prose deu

#------------------------------------------#
# Sentence-balanced run
# makes training splits for NMT task
bash shell/get_splits.sh nmt pseudo _
bash shell/get_splits.sh nmt archaic _

# makes training splits for PPL task
bash shell/get_splits.sh llm bible eng _
bash shell/get_splits.sh llm prose eng _
bash shell/get_splits.sh llm bible deu _
bash shell/get_splits.sh llm prose deu _

#------------------------------------------#
# Token-balanced run
# makes token-balanced versions of prepared data
bash shell/balance_token_count.sh eng 
bash shell/balance_token_count.sh deu 

# makes token-balanced training splits
bash shell/get_splits.sh nmt archaic balanced
bash shell/get_splits.sh llm bible eng balanced
bash shell/get_splits.sh llm bible deu balanced