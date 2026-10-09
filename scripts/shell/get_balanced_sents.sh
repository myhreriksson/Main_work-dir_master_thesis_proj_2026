split="${1}"

path='data/_test-n-finetune_/_finetuning/'
cand="bible_${split}"
ref="game_${split}"

tok_count() {
    local lang="${1}"
    python scripts/python/create_balanced_ver.py \
        -p "${dir}/" \
        -c "$cand" \
        -r "$ref" \
        -o "$output" \
        -s "$split" \
        -d "$domain" \
        -l "$lang"
}

for dir in "$path"*/; do
    if [[ "$dir" != */ppl/ ]]; then
        domain='game'
        output="${dir}/"
        mkdir -p "$output"
        tok_count ''
    else
        domain='prose'
        output="${dir}/"
        lang="${2}"
        mkdir -p "$output"
        tok_count "$lang"
    fi
done