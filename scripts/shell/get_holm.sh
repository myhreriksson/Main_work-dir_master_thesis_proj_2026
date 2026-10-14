#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 00:05:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

family="${1}"

inp_path="results/significance/"
out_path="${inp_path}holm/"
mkdir -p "$out_path"

python scripts/python/holm_correction.py \
    -f "$family" \
    -i "$inp_path" \
    -o "$out_path"