#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 03:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

model="${1}"
config="${2}"
style="${3}"

# this script is very repetetive and cluttered, have fun reading it :^)

# part 1: translate with increasing tuning sizes
if [[ "$config" == "tuned" ]]; then
    if [[ "$style" == "archaic" ]]; then
        style='pseudo'
    elif [[ "$style" == "pseudo" ]]; then
        style='archaic'
    fi
    for i in $(seq 0 3 15); do
        if (( i > 0 )); then
            inp_path="data/_test-n-finetune_/${style}_eng/"
            out_path="results/translations/${config}/${i}k/${style}"
            model_path="models/${config}/${i}k/${model}/"

            if [[ "$model" == "nllb" ]]; then
                src='eng_Latn'
                tgt='deu_Latn'
            elif [[ "$model" == "bart" ]]; then
                src='en_XX'
                tgt='de_DE'
            fi
            model_path="${model_path}${style}"

            mkdir -p "$out_path"
            python python/translate.py \
                -m "$model_path" \
                -n "$model" \
                -i "$inp_path" \
                -o "$out_path" \
                -b 4 \
                --src_lang "$src" \
                --tgt_lang "$tgt" \
                --batch_size 256
        fi
    done

# part 1: translate with maximum tuning size
    inp_path="data/_test-n-finetune_/${style}_eng/"
    out_path="results/translations/${config}/max/${style}"
    model_path="models/${config}/max/${model}/"

    if [[ "$model" == "nllb" ]]; then
        src='eng_Latn'
        tgt='deu_Latn'
    elif [[ "$model" == "bart" ]]; then
        src='en_XX'
        tgt='de_DE'
    fi
    model_path="${model_path}${style}"

    mkdir -p "$out_path"
    python python/translate.py \
        -m "$model_path" \
        -n "$model" \
        -i "$inp_path" \
        -o "$out_path" \
        -b 4 \
        --src_lang "$src" \
        --tgt_lang "$tgt" \
        --batch_size 256

# part 3: translate baselines
elif [[ "$config" == "base" ]]; then
    inp_path="data/_test-n-finetune_/${style}_eng/"
    out_path="results/translations/${config}/${style}"
    model_path="models/${config}/${model}/"

    if [[ "$model" == "nllb" ]]; then
        src='eng_Latn'
        tgt='deu_Latn'
    elif [[ "$model" == "bart" ]]; then
        src='en_XX'
        tgt='de_DE'
    fi

    mkdir -p "$out_path"
    python python/translate.py \
        -m "$model_path" \
        -n "$model" \
        -i "$inp_path" \
        -o "$out_path" \
        -b 4 \
        --src_lang "$src" \
        --tgt_lang "$tgt" \
        --batch_size 256
fi