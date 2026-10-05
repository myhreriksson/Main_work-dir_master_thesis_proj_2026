#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 00:45:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

model="${1}"
source="data/flores_data/flores_eng/flores_EN.txt"
target="results/translations/base/flores/flores_Translation_${model}_EN-DE.txt"
reference="data/flores_data/flores_deu/flores_DE.txt"
out_path="results/evaluations/base/flores/"
mkdir -p "$out_path"
{
    sacrebleu "data/flores_data/flores_deu/flores_DE.txt" \
        -i "$target" \
        -m bleu ter \
        -l en-de
} > "${out_path}/flores_sacrebleu_${model}.json"
{
    comet-score \
        -s "$source" \
        -t "$target" \
        -r "$reference" \
        --quiet \
        --only_system
} > "${out_path}/flores_comet_${model}.txt"

python python/write_results.py \
    "${out_path}/flores_sacrebleu_${model}.json" \
    "${out_path}/flores_comet_${model}.txt" \
    "${out_path}/flores_Evaluation_${model}.txt" \
    score

rm "${out_path}/flores_comet_${model}.txt" "${out_path}/flores_sacrebleu_${model}.json"