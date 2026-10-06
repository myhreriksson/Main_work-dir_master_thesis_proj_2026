#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 01:30:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

domain="${1}"
config="${2}"
model="${3}"
balance="${4}"

evaluate() {
    local config="${1}"
    local source="data/_test-n-finetune_/${domain}_eng/${domain}_EN.txt"
    local target="results/translations/${config}/${domain}/${domain}_Translation_${model}_EN-DE.txt"
    local reference="data/${domain}_data/${domain}_deu/${domain}_DE.txt"
    local out_path="results/evaluations/${config}/${domain}/${balance}"
    mkdir -p "$out_path"

    { sacrebleu "$source" \
        -i "$target" \
        -m bleu ter \
        -l en-de
    } > "${out_path}/${domain}_sacrebleu_${model}.json"

    { comet-score \
        -s "$source" \
        -t "$target" \
        -r "$reference" \
        --quiet \
        --only_system
    } > "${out_path}/${domain}_comet_${model}.txt"

    python python/write_results.py \
        "${out_path}/${domain}_sacrebleu_${model}.json" \
        "${out_path}/${domain}_comet_${model}.txt" \
        "${out_path}/${domain}_Evaluation_${model}.txt" \
        score

    rm \
        "${out_path}/${domain}_comet_${model}.txt" \
        "${out_path}/${domain}_sacrebleu_${model}.json"
}

if [[ "$config" == "base" ]]; then
    evaluate "base"
elif [[ "$config" == "tuned" ]]; then
    for i in $(seq 3 3 15); do
        evaluate "tuned/${i}k"
    done
    evaluate "tuned/max"
fi