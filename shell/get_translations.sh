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
domain="${3}"
balance="${4}"

# this script is very repetetive and cluttered, have fun reading it :^)

# part 1: translate with increasing tuning sizes
if [[ "$config" == "tuned" ]]; then
    if [[ "$domain" == "archaic" ]]; then
        model_domain='pseudo'
    elif [[ "$domain" == "pseudo" ]]; then
        model_domain='archaic'
    fi
    for i in $(seq 0 3 15); do
        if (( i > 0 )); then
            inp_path="data/_test-n-finetune_/${domain}_eng/"
            out_path="results/translations/${config}/${i}k/${domain}"
            model_path="models/${config}/${i}k/${model_domain}/"

            if [[ "$model" == "nllb" ]]; then
                src='eng_Latn'
                tgt='deu_Latn'
            elif [[ "$model" == "bart" ]]; then
                src='en_XX'
                tgt='de_DE'
            fi

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
        fi
    done

# part 1: translate with maximum tuning size
    inp_path="data/_test-n-finetune_/${domain}_eng/"
    out_path="results/translations/${config}/max/${domain}"
    model_path="models/${config}/max/${model_domain}/"

    if [[ "$model" == "nllb" ]]; then
        src='eng_Latn'
        tgt='deu_Latn'
    elif [[ "$model" == "bart" ]]; then
        src='en_XX'
        tgt='de_DE'
    fi

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

# part 3: translate baselines
elif [[ "$config" == "base" ]]; then
    inp_path="data/_test-n-finetune_/${domain}_eng/"
    out_path="results/translations/${config}/${domain}"
    model_path="models/${config}/${model}/"

    if [[ "$model" == "nllb" ]]; then
        src='eng_Latn'
        tgt='deu_Latn'
    elif [[ "$model" == "bart" ]]; then
        src='en_XX'
        tgt='de_DE'
    fi

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
fi