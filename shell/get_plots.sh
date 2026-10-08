config="${1}"
domain="${2}"
path="models/tuned/"
output="results/plots/"

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis_venv

if [[ "$config" == "nmt" ]]; then
    mkdir -p "$output"
    python python/plot_scores.py \
        -p "$path" \
        -d "$domain" \
        -o "$output"
elif [[ "$config" == "llm" ]]; then
    python python/plot_loss.py \
        -p "$path" \
        -o "$output"
fi