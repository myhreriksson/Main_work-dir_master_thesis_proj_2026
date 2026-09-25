#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 03:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

domain="${1}"
model_A="${2}"
balance="${3}"
comparison="${4}"

# NOTE: debugging this has stolen years from my life; God is dead, and slurm killed him

if [[ "$comparison" == "config" ]]; then
    secondary_path="results/translations/base/${domain}/"
    out_path="results/evaluations/bootstraps/${domain}/${balance}/comps_within_${model_A}/"
    model_B="$model_A"
fi

data_path='data/_test-n-finetune_/'
src_path="${data_path}${domain}_eng/"
ref_path="${data_path}${domain}_deu/"
mkdir -p "$out_path"

# part 1: bootstrap with increasing tuning sizes
for i in $(seq 0 3 15); do
    if (( i > 0 )); then
        if [[ "$comparison" == "model" ]]; then
            secondary_path="results/translations/tuned/${i}k/${domain}/${balance}/"
            out_path="results/evaluations/bootstraps/${domain}/${balance}/comps_across_models/"
            if [[ "$model_A" == "nllb" ]]; then
                model_B='bart'
            elif [[ "$model_A" == "bart" ]]; then
                model_B='nllb'
            fi
        fi
        main_path="results/translations/tuned/${i}k/${domain}/${balance}/"
        out_file="${out_path}paired_bs-${i}k.txt"
        for secondary_file in "${secondary_path}/"*"_${model_B}_EN-DE.txt"; do
            file=$(basename "$secondary_file")
            main_file="${main_path}${file%%_*}_Translation_${model_A}_EN-DE.txt"
            src="${src_path}${file%%_*}_EN.txt"
            ref="${ref_path}${file%%_*}_DE.txt"
        {
            sacrebleu $ref \
                -i "$secondary_file" "$main_file" \
                -m bleu ter \
                --paired-bs \
                --paired-bs-n 5000
        } > "${out_path}${file%%_*}bleu_${i}k.json"
        {
            comet-compare \
                -s $src \
                -t "$secondary_file" "$main_file" \
                -r $ref 
        } > "${out_path}${file%%_*}comet_${i}k.txt"
        
        python python/write_results.py \
            "${out_path}${file%%_*}bleu_${i}k.json" \
            "${out_path}${file%%_*}comet_${i}k.txt" \
            "$out_file" \
            bootstrap
        
        rm "${out_path}${file%%_*}bleu_${i}k.json" "${out_path}${file%%_*}comet_${i}k.txt"
        done
    fi
done

# part 1: bootstrap with maximum tuning size
if [[ "$comparison" == "model" ]]; then
    secondary_path="results/translations/tuned/max/${domain}/${balance}/"
    out_path="results/evaluations/bootstraps/${domain}/${balance}/comps_across_models/"
fi
main_path="results/translations/tuned/max/${domain}/${balance}/"
out_file="${out_path}paired_bs-max.txt"
for secondary_file in "${secondary_path}/"*"_${model_B}_EN-DE.txt"; do
    file=$(basename "$secondary_file")
    main_file="${main_path}${file%%_*}_Translation_${model_A}_EN-DE.txt"
    src="${src_path}${file%%_*}_EN.txt"
    ref="${ref_path}${file%%_*}_DE.txt"
    {
        sacrebleu $ref \
        -i "$secondary_file" "$main_file" \
        -m bleu ter \
        --paired-bs \
        --paired-bs-n 5000 
    } > "${out_path}${file%%_*}bleu_max.json"
    {
    comet-compare \
        -s $src \
        -t "$secondary_file" "$main_file" \
        -r $ref 
    } > "${out_path}${file%%_*}comet_max.txt"
    
    python python/write_results.py \
        "${out_path}${file%%_*}bleu_max.json" \
        "${out_path}${file%%_*}comet_max.txt" \
        "$out_file" \
        bootstrap

    rm "${out_path}${file%%_*}bleu_max.json" "${out_path}${file%%_*}comet_max.txt"
done