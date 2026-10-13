domains=("game" "bible" "balanced_bible")
path="models/tuned/"
output="results/plots/"
mkdir -p "$output"

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

for domain in "${domains[@]}"; do
    python scripts/python/plot_scores.py \
        -p "$path" \
        -d "$domain" \
        -o "$output"
done
python scripts/python/plot_loss.py \
    -p "$path" \
    -o "$output"