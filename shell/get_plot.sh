domain="${1}"
metric="${2}"
path="models/tuned/"
output="results/plots/"

mkdir -p "$output"
python python/plot_scores.py \
    -p "$path" \
    -s "$domain" \
    -o "$output" \
    --metric "$metric" \