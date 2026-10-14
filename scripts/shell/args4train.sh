#!/bin/bash

load="${1}"
task="${2}"
model="${3}"
domain="${4}"
lang="${5}"
balance="${6}"

sbatch scripts/shell/train.sh "$load" "$task" "$model" "$domain" "$lang" "$balance" 3k
sbatch scripts/shell/train.sh "$load" "$task" "$model" "$domain" "$lang" "$balance" 6k
sbatch scripts/shell/train.sh "$load" "$task" "$model" "$domain" "$lang" "$balance" 9k
sbatch scripts/shell/train.sh "$load" "$task" "$model" "$domain" "$lang" "$balance" 12k
sbatch scripts/shell/train.sh "$load" "$task" "$model" "$domain" "$lang" "$balance" 15k
sbatch scripts/shell/train.sh "$load" "$task" "$model" "$domain" "$lang" "$balance" max