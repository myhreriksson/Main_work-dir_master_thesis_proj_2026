model="${1}"
style="${2}"
metric="${3}"
path="models/tuned/"
output="results/plots/"

mkdir -p "$output"
python python/plot_loss.py \
    -p "$path" \
    -m "$model" \
    -s "$style" \
    -o "$output" \
    --metric "$metric" \