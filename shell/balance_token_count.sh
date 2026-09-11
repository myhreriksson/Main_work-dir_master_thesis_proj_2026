lang="${1}"

path='data/_test-n-finetune_/'
c_path="${path}archaic_${lang}/"
r_path="${path}pseudo_${lang}/"
output="${c_path}balanced/"
mkdir -p "$output"

python python/token_count_filter.py \
    -c "$c_path" \
    -r "$r_path" \
    -o "$output" \
    -l "$lang" 