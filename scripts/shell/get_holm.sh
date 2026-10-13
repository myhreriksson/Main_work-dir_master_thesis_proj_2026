family="${1}"

inp_path="results/significance/"
out_path="${inp_path}holm/"
mkdir -p "$out_path"

python scripts/python/holm_correction.py \
    -f "$family" \
    -i "$inp_path" \
    -o "$out_path"