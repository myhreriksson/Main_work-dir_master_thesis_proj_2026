#!/bin/bash
#SBATCH -A uppmax2026-1-95
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 00:10:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

model="${1}"

inp_path='data/flores_data/flores_eng/'
out_path='results/translations/base/flores/'
model_path="models/base/${model}/"

mkdir -p "$out_path"

if [[ "$model" == "nllb" ]]; then
    src='eng_Latn'
    tgt='deu_Latn'
elif [[ "$model" == "bart" ]]; then
    src='en_XX'
    tgt='de_DE'
fi

python python/translate.py \
    -m "$model_path" \
    -c 'base' \
    -n "$model" \
    -i "$inp_path" \
    -o "$out_path" \
    -b 4 \
    --src_lang "$src" \
    --tgt_lang "$tgt" \
    --batch_size 256
