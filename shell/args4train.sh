#!/bin/bash

task="${1}"
model="${2}"
domain="${3}"
lang="${4}"
balance="${5}"

sbatch shell/train.sh "$task" "$model" "$domain" "$lang" "$balance" 3k
sbatch shell/train.sh "$task" "$model" "$domain" "$lang" "$balance" 6k
sbatch shell/train.sh "$task" "$model" "$domain" "$lang" "$balance" 9k
sbatch shell/train.sh "$task" "$model" "$domain" "$lang" "$balance" 12k
sbatch shell/train.sh "$task" "$model" "$domain" "$lang" "$balance" 15k
sbatch shell/train.sh "$task" "$model" "$domain" "$lang" "$balance" max