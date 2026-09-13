#!/bin/bash

# fine-tune NMT
bash shell/arg_for_train.sh nmt nllb archaic 
bash shell/arg_for_train.sh nmt nllb pseudo 
bash shell/arg_for_train.sh nmt bart archaic 
bash shell/arg_for_train.sh nmt bart pseudo 
bash shell/arg_for_train.sh nmt nllb archaic balanced # use token-balanced
bash shell/arg_for_train.sh nmt bart archaic balanced # use token-balanced

# fine-tune LLM
bash shell/arg_for_train.sh llm qwen archaic eng 
bash shell/arg_for_train.sh llm qwen prose eng 
bash shell/arg_for_train.sh llm qwen archaic deu 
bash shell/arg_for_train.sh llm qwen prose deu 
bash shell/arg_for_train.sh llm qwen archaic eng balanced # use token-balanced
bash shell/arg_for_train.sh llm qwen archaic deu balanced # use token-balanced