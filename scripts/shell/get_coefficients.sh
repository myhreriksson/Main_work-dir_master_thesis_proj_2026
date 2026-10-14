#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 00:20:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

metric="${1}"
inp_path="results/coefficients/lmm_data.csv"
out_path="results/coefficients/"
out_file="output_${metric^^}.txt"
mkdir -p "$out_path"

Rscript scripts/Rscript/lmm_coefficients.r \
    "$inp_path" \
    "$out_path" \
    "$out_file" \
    "$metric"