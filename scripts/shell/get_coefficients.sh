#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 12:00:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

r_path=/proj/uppmax2025-2-505/mame0175/thesis_PROJ/R/lib
mkdir -p "$r_path"
export R_LIBS_USER="$r_path"

metric="${1}"
inp_path="stat_analysis/data.csv"
out_path="results/evaluations/lmm_coefficients/${metric^^}.txt"
mkdir -p "$out_path"

Rscript scripts/Rscript/lmm_coefficients.r \
    "$inp_path" \
    "$out_path" \
    "$metric"