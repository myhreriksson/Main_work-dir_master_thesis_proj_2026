#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 03:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

config="${1}"
domain="${2}"
lang="${3}"
balance="${4}"

model_path="models/${config}/"

# fine-tuned
if [[ "$config" == "tuned" ]]; then
    if [[ "$domain" == "bible" ]]; then
        model_domain="${balance}archaic"
    elif [[ "$domain" == "prose" ]]; then
        model_domain="$domain"
    fi
    output_path="results/evaluations/perplexity/${config}/${domain}/"
    mkdir -p "$output_path"
    model="${model_path}max/qwen/${model_domain}/trained_on_${lang}/"

# baselines
elif [[ "$config" == "base" ]]; then
    output_path="results/evaluations/perplexity/${config}/"
    mkdir -p "$output_path"
    model="${model_path}qwen/"
fi

python python/compute_ppl.py \
    -m "$model" \
    -o "$output_path" \
    -l "$lang" 