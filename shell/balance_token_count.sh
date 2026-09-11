split="${1}"

path='data/_test-n-finetune_/_finetuning/'
cand="archaic_${split}"
ref="pseudo_${split}"

for dir in "$path"*/; do
    if [[ "$dir" != */ppl/ ]]; then
        domain='pseudo'
        output="${dir}/"
        mkdir -p "$output"
        python python/token_count_filter.py \
            -p "${dir}/" \
            -c "$cand" \
            -r "$ref" \
            -o "$output" \
            -s "$split" \
            -d "$domain"
    else
        domain='prose'
        output="${dir}/"
        lang="${2}"
        mkdir -p "$output"
        python python/token_count_filter.py \
            -p "${dir}/" \
            -c "$cand" \
            -r "$ref" \
            -o "$output" \
            -s "$split" \
            -d "$domain" \
            -l "$lang"
    fi
done