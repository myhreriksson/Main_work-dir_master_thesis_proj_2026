#!/bin/bash

# Copies sents and metadata from game translations by models trained on balanced bible data
bash scripts/shell/get_copies.sh game bart bleu balanced
bash scripts/shell/get_copies.sh game bart comet balanced
bash scripts/shell/get_copies.sh game bart ter balanced
bash scripts/shell/get_copies.sh game nllb bleu balanced
bash scripts/shell/get_copies.sh game nllb comet balanced
bash scripts/shell/get_copies.sh game nllb ter balanced

# Copies sents and metadata from game translations by models trained on unbalanced bible data
bash scripts/shell/get_copies.sh game bart bleu unbalanced
bash scripts/shell/get_copies.sh game bart comet unbalanced
bash scripts/shell/get_copies.sh game bart ter unbalanced
bash scripts/shell/get_copies.sh game nllb bleu unbalanced
bash scripts/shell/get_copies.sh game nllb comet unbalanced
bash scripts/shell/get_copies.sh game nllb ter unbalanced

# Copies sents and metadata from bible translations by models trained on game data
bash scripts/shell/get_copies.sh bible bart bleu 
bash scripts/shell/get_copies.sh bible bart comet 
bash scripts/shell/get_copies.sh bible bart ter
bash scripts/shell/get_copies.sh bible nllb bleu 
bash scripts/shell/get_copies.sh bible nllb comet 
bash scripts/shell/get_copies.sh bible nllb ter

# Uses copies to create uniform CSV contianing all results
python scripts/python/make_csv_data.py
rm -r files/

# Compute coefficients for all metrics
sbatch scripts/shell/get_coefficients.sh bleu
sbatch scripts/shell/get_coefficients.sh comet
sbatch scripts/shell/get_coefficients.sh ter

# # Select good and bad performing sentence pairs for each metric (for qualitative analysis)
# python scripts/python/sent_selector.py bleu
# python scripts/python/sent_selector.py comet
# python scripts/python/sent_selector.py ter