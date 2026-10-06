limit="${1}"
domain="${2}"
config="${3}"
line="${4}"
size="${5}"
balance="${6}"
path="data/_test-n-finetune_/${domain}"

python python/select_for_analysis.py \
    -p $path \
    -c "$config" \
    -s "$size" \
    -d "$domain" \
    -l "$line" \
    --limit "$limit" \
    --balance "$balance"