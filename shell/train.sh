#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 8:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

task="${1}"
model="${2}"
domain="${3}"
lang="${4}"
balance="${5}"
size="${6}"

if [[ "$balance" == "balanced" ]]; then
    domain="balanced_${3}"
else
    domain="${3}"
fi

data_path='data/_test-n-finetune_/'
model_path="models/base/${model}"

# for NMT tasks:
if [[ "$task" == "nmt" ]]; then
    json_path="${data_path}_finetuning/"
    if [[ "$model" == "nllb" ]]; then
        src='eng_Latn'
        tgt='deu_Latn'
        res_path="models/tuned/${size}/${model}/${domain}/"
    elif [[ "$model" == "bart" ]]; then
        src='en_XX'
        tgt='de_DE'
        res_path="models/tuned/${size}/${model}/${domain}/"
    fi
    mkdir -p "$res_path"
    mkdir -p "databases/${size}/${model}/${domain}"
    python python/finetune_nmt.py \
        -p "${json_path}${size}" \
        -o "$res_path" \
        -s "$domain" \
        -m "$model_path" \
        --seed 21 \
        --tgt_lang "$tgt" \
        --src_lang "$src" \
        --database "databases/${size}/${model}/${domain}"

# for LLM tasks:
elif [[ "$task" == "llm" ]]; then
    json_path="${data_path}_finetuning/ppl/"
    mkdir -p "databases/llm_${lang}/${model}/${domain}"
    python python/finetune_llm.py \
        -m "$model_path" \
        -i "$json_path" \
        -o "models/tuned/max/${model}/${domain}/trained_on_${lang}" \
        -d "$domain" \
        -l "$lang" \
        --seed 21 \
        --database "databases/llm_${lang}/${model}/${domain}"
fi