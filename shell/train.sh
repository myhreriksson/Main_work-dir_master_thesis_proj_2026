#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 3:30:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

task="${1}"
model="${2}"
domain="${3}"
lang="${4}"

data_path='data/_test-n-finetune_/'
model_path="models/base/${model}"

if [[ "$task" == "nmt" ]]; then
    json_path="${data_path}_finetuning/"
    # part 1: finetune with increasing tuning sizes
    for i in $(seq 0 3 15); do
        if (( i > 0 )); then
            if [[ "$model" == "nllb" ]]; then
                tgt='eng_Latn'
                src='deu_Latn'
                res_path="models/tuned/${i}k/${model}/${domain}/"
            elif [[ "$model" == "bart" ]]; then
                tgt='en_XX'
                src='de_DE'
                res_path="models/tuned/${i}k/${model}/${domain}/"
            fi

            mkdir -p "$res_path"
            python python/finetune_nmt.py \
                -p "${json_path}${i}k" \
                -o "$res_path" \
                -s "$domain" \
                -m "$model_path" \
                --seed 21 \
                --tgt_lang "$tgt" \
                --src_lang "$src"
        fi
    done

    # part 2: finetune with maximum tuning size
    if [[ "$model" == "nllb" ]]; then
        tgt='eng_Latn'
        src='deu_Latn'
        res_path="models/tuned/max/${model}/${domain}/"
    elif [[ "$model" == "bart" ]]; then
        tgt='en_XX'
        src='de_DE'
        res_path="models/tuned/max/${model}/${domain}/"
    fi

    mkdir -p "$res_path"
    python python/finetune_nmt.py \
        -p "${json_path}max" \
        -o "$res_path" \
        -s "$domain" \
        -m "$model_path" \
        --seed 21 \
        --tgt_lang "$tgt" \
        --src_lang "$src"

elif [[ "$task" == "llm" ]]; then
    json_path="${data_path}_finetuning/ppl/"
    python python/finetune_llm.py \
        -m "$model_path" \
        -i "$json_path" \
        -o "models/tuned/max/${model}/${domain}/trained_on_${lang}" \
        -d "$domain" \
        -l "$lang" \
        --seed 21 
fi