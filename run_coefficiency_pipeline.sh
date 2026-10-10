#!/bin/bash

# Copies sents and metadata from game translations by models trained on balanced bible data
bash scripts/shell/get_copies.sh game bart sacrebleu balance
bash scripts/shell/get_copies.sh game bart comet balance
bash scripts/shell/get_copies.sh game nllb sacrebleu balance
bash scripts/shell/get_copies.sh game nllb comet balance

# Copies sents and metadata from game translations by models trained on unbalanced bible data
bash scripts/shell/get_copies.sh game bart sacrebleu unbalanced
bash scripts/shell/get_copies.sh game bart comet unbalanced
bash scripts/shell/get_copies.sh game nllb sacrebleu unbalanced
bash scripts/shell/get_copies.sh game nllb comet unbalanced

# Copies sents and metadata from bible translations by models trained on game data
bash scripts/shell/get_copies.sh bible bart sacrebleu unbalanced
bash scripts/shell/get_copies.sh bible bart comet unbalanced
bash scripts/shell/get_copies.sh bible nllb sacrebleu unbalanced
bash scripts/shell/get_copies.sh bible nllb comet unbalanced

# Uses copies to create uniform CSV contianing all results
python scripts/python/make_csv_data.py
rm -r stat_analysis/files # remove unnecessary copies once CSV is made

# Compute coefficients for all metrics
sbatch scripts/shell/get_coefficients.sh bleu
sbatch scripts/shell/get_coefficients.sh comet
sbatch scripts/shell/get_coefficients.sh ter

# Select good and bad performing sentence pairs for each metric (for qualitative analysis)
python scripts/python/sent_selector.py bleu
python scripts/python/sent_selector.py comet
python scripts/python/sent_selector.py ter