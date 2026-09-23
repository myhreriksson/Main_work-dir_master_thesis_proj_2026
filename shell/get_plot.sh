domain="${1}"
path="models/tuned/"
output="results/plots/"

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

mkdir -p "$output"
python python/plot_scores.py \
    -p "$path" \
    -s "$domain" \
    -o "$output" 