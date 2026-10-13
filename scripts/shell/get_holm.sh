family="${1}"

path="results/significance/"

python scripts/python/holm_correction.py \
    -f "$family" \
    -p "$path"