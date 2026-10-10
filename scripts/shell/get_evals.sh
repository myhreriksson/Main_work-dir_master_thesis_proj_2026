#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 2:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

domain="${1}"
config="${2}"
model="${3}"
balance="${4}"

evaluate() {
    local config="${1}"
    local sents="${2}"
    if [[ "$balance" && "$domain" == "game" ]]; then
        domain_balance="${domain}/${balance}"
    else
        domain_balance="${domain}"
    fi
    local src="data/_test-n-finetune_/${domain}_eng/${domain}_EN.txt"
    local tgt="results/translations/${config}/${domain_balance}/${domain}_Translation_${model}_EN-DE.txt"
    local ref="data/_test-n-finetune_/${domain}_deu/${domain}_DE.txt"
    local out_path="results/evaluations/${config}/${domain_balance}"
    mkdir -p "$out_path"

    # corpus-level
    if [[ ! "$sents" ]]; then
        { sacrebleu "$tgt" \
            -i "$ref" \
            -m bleu ter \
            -l en-de
        } > "${out_path}/${domain}_sacrebleu_${model}.json"

        { comet-score \
            -s "$src" \
            -t "$tgt" \
            -r "$ref" \
            --quiet \
            --only_system
        } > "${out_path}/${domain}_comet_${model}.txt"

        python scripts/python/write_results.py \
            "${out_path}/${domain}_sacrebleu_${model}.json" \
            "${out_path}/${domain}_comet_${model}.txt" \
            "${out_path}/${domain}_Evaluation_${model}.txt" \
            score

        rm \
            "${out_path}/${domain}_comet_${model}.txt" \
            "${out_path}/${domain}_sacrebleu_${model}.json"
    fi

    # sentence-level
    if [[ "$sents" ]]; then
        { sacrebleu "$tgt" \
            -i "$ref" \
            -m bleu \
            -l en-de \
            --sentence-level 
        } > "${out_path}/${domain}_bleu_per_sent_${model}.txt"

        { sacrebleu "$tgt" \
            -i "$ref" \
            -m ter \
            -l en-de \
            --sentence-level 
        } > "${out_path}/${domain}_ter_per_sent_${model}.txt"

        { comet-score \
            -s "$src" \
            -t "$tgt" \
            -r "$ref" \
            --quiet
        } > "${out_path}/${domain}_comet_per_sent_${model}.txt"
    fi
}

if [[ "$config" == "base" ]]; then
    evaluate "base"
elif [[ "$config" == "tuned" ]]; then
    for i in $(seq 3 3 15); do
        evaluate "tuned/${i}k"
        evaluate "tuned/${i}k" 'sents'
    done
    evaluate 'tuned/max'
    evaluate 'tuned/max' 'sents'
fi