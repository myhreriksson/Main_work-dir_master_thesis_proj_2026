#!/bin/bash

bash scripts/shell/get_copies.sh game bart sacrebleu balance
bash scripts/shell/get_copies.sh game bart comet balance
bash scripts/shell/get_copies.sh game nllb sacrebleu balance
bash scripts/shell/get_copies.sh game nllb comet balance

bash scripts/shell/get_copies.sh game bart sacrebleu unbalanced
bash scripts/shell/get_copies.sh game bart comet unbalanced
bash scripts/shell/get_copies.sh game nllb sacrebleu unbalanced
bash scripts/shell/get_copies.sh game nllb comet unbalanced

bash scripts/shell/get_copies.sh bible bart sacrebleu unbalanced
bash scripts/shell/get_copies.sh bible bart comet unbalanced
bash scripts/shell/get_copies.sh bible nllb sacrebleu unbalanced
bash scripts/shell/get_copies.sh bible nllb comet unbalanced

python scripts/python/make_csv_data.py
sbatch scripts/shell/get_coefficients.sh