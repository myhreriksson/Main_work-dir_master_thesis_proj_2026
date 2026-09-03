#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 03:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

style="${1}"
model="${2}"

# NOTE: debugging this has stolen years from my life; God is dead, and slurm killed him

data_path='data/_test-n-finetune_/'
src_path="${data_path}${style}_eng/"
ref_path="${data_path}${style}_deu/"
base_path="results/translations/base/${style}/"
out_path="results/evaluations/bootstraps/${style}/${model}/"
mkdir -p "$out_path"

# part 1: bootstrap with increasing tuning sizes
for i in $(seq 0 3 15); do
    if (( i > 0 )); then
        tuned_path="results/translations/tuned/${i}k/${style}/"
        out_file="${out_path}paired_bs-${i}k.txt"
        for base_file in "${base_path}/"*"_${model}_EN-DE.txt"; do
            file=$(basename "$base_file")
            tuned_file="${tuned_path}${file}"
            src="${src_path}${file%%_*}_EN.txt"
            ref="${ref_path}${file%%_*}_DE.txt"
        {
            sacrebleu $ref \
                -i "$base_file" "$tuned_file" \
                -m bleu ter \
                --paired-bs \
                --paired-bs-n 5000
        } > "${out_path}${file%%_*}bleu_${i}k.json"
        {
            comet-compare \
                -s $src \
                -t "$base_file" "$tuned_file" \
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
tuned_path="results/translations/tuned/max/${style}/"
out_file="${out_path}paired_bs-max.txt"

for base_file in "${base_path}/"*"_${model}_EN-DE.txt"; do
    file=$(basename "$base_file")
    tuned_file="${tuned_path}${file}"
    src="${src_path}${file%%_*}_EN.txt"
    ref="${ref_path}${file%%_*}_DE.txt"
    {
        sacrebleu $ref \
        -i "$base_file" "$tuned_file" \
        -m bleu ter \
        --paired-bs \
        --paired-bs-n 5000 
    } > "${out_path}${file%%_*}bleu_max.json"
    {
    comet-compare \
        -s $src \
        -t "$base_file" "$tuned_file" \
        -r $ref 
    } > "${out_path}${file%%_*}comet_max.txt"
    
    python python/write_results.py \
        "${out_path}${file%%_*}bleu_max.json" \
        "${out_path}${file%%_*}comet_max.txt" \
        "$out_file" \
        bootstrap

    rm "${out_path}${file%%_*}bleu_max.json" "${out_path}${file%%_*}comet_max.txt"
done