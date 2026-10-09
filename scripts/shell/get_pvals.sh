#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 03:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

domain="${1}"
model_A="${2}"
balance="${3}"
comparison="${4}"

out_path="results/evaluations/significance/${domain}/${balance}/"
data_path='data/_test-n-finetune_/'
tgt_path='results/translations/'
src_path="${data_path}${domain}_eng/"
ref_path="${data_path}${domain}_deu/"

compare() {
    local model_B="${1}"
    local config_A="${2}"
    local config_B="${3}"
    local comp_type="${4}"
    local size="${config_B#*/}"
    local out_dir="${out_path}/${comp_type}"
    mkdir -p "$out_dir"
    local out_file="${out_dir}/paired_bs-${size}.txt"
    if [[ "$config_A" == "base" ]]; then
        local tgt_A="${tgt_path}/${config_A}/${domain}/${domain}_Translation_${model_A}_EN-DE.txt"
        local tgt_B="${tgt_path}/${config_B}/${domain}/${domain}_Translation_${model_B}_EN-DE.txt"
    else
        local tgt_A="${tgt_path}/${config_A}/${domain}/${balance}/${domain}_Translation_${model_A}_EN-DE.txt"
        local tgt_B="${tgt_path}/${config_B}/${domain}/${balance}/${domain}_Translation_${model_B}_EN-DE.txt"
    fi
    local src="${src_path}/${domain}_EN.txt"
    local ref="${ref_path}/${domain}_DE.txt"

    { sacrebleu $ref \
        -i "$tgt_A" "$tgt_B" \
        -m bleu ter \
        --paired-bs \
        --paired-bs-n 5000
    } > "${out_dir}/${domain}_bleu_${size}.json"

    { comet-compare \
        -s $src \
        -t "$tgt_A" "$tgt_B" \
        -r $ref 
    } > "${out_dir}/${domain}_comet_${size}.txt"
        
    python scripts/python/write_results.py \
        "${out_dir}/${domain}_bleu_${size}.json" \
        "${out_dir}/${domain}_comet_${size}.txt" \
        "$out_file" \
        bootstrap
    rm \
        "${out_dir}/${domain}_bleu_${size}.json" \
        "${out_dir}/${domain}_comet_${size}.txt"
}

# significance testing within same model, comparing all configs with baseline
if [[ "$comparison" == "config" ]]; then
    model_B="$model_A" 
    for i in $(seq 3 3 15); do
        compare \
            "$model_B" \
            "base" \
            "tuned/${i}k" \
            "comps_within_${model_B}" 
    done
    compare \
        "$model_B" \
        "base" \
        "tuned/max" \
        "comps_within_${model_B}" 
elif [[ "$comparison" == "model" ]]; then
    model_B='nllb'
    for i in $(seq 3 3 15); do
        compare \
            "$model_B" \
            "tuned/${i}k" \
            "tuned/${i}k" \
            "comps_across_models"
    done
    compare \
        "$model_B" \
        "tuned/max" \
        "tuned/max" \
        "comps_across_models"
    compare \
        "$model_B" \
        "base" \
        "base" \
        "comps_across_models"
fi