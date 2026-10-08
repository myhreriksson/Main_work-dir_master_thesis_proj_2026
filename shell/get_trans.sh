#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 03:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

model="${1}"
config="${2}"
domain="${3}"
balance="${4}"

if [[ "$model" == "nllb" ]]; then
    src='eng_Latn'
    tgt='deu_Latn'
elif [[ "$model" == "bart" ]]; then
    src='en_XX'
    tgt='de_DE'
fi

translate() {
    local size_config="${1}"
    local inp_path="data/_test-n-finetune_/${domain}_eng/"
    local out_path="results/translations/${size_config}/${domain}/"
    local model_path="models/${size_config}/${model}/"
    mkdir -p "$out_path"

    python python/translate.py \
        -m "$model_path" \
        -c "$config" \
        -n "$model" \
        -i "$inp_path" \
        -o "$out_path" \
        -d "$domain" \
        -b 4 \
        --src_lang "$src" \
        --tgt_lang "$tgt" \
        --batch_size 256 \
        --balance "$balance"
}

if [[ "$config" == "base" ]]; then
    translate "base"
elif [[ "$config" == "tuned" ]]; then
    for i in $(seq 3 3 15); do
        translate "tuned/${i}k"
    done
    translate "tuned/max"
fi