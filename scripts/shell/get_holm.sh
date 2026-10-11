family="${1}"

path="results/significance/${domain_balance}/"

python scripts/python/holm_correction.py \
    -f "$family" \
    -p "$path"
