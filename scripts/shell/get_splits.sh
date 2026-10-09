task="${1}"
domain="${2}"
lang="${3}"

data_path='data/_test-n-finetune_/'
json_path="${data_path}_finetuning/"

par_corpus_split() {
    local json_path="${json_path}/${1}/"
    mkdir -p "$json_path"
    python scripts/python/split_par_corpus.py \
        -p "$data_path" \
        -o "$json_path" \
        -d "${domain}_deu/" \
        -e "${domain}_eng/" \
        -n "$domain" \
        -s 0.8 0.1 0.1 \
        --data_size "${1}" \
        --min_len 4 
}

txt_corpus_split() {
    local json_path="${json_path}/${1}/"
    mkdir -p "$json_path"
    python scripts/python/split_txt_corpus.py \
        -i "$data_path" \
        -o "$json_path" \
        -d "$domain" \
        -l "$lang" \
        -s 0.8 0.1 0.1 \
        --min_len 5 
}

if [[ "$task" == "llm" ]]; then
    txt_corpus_split "ppl"
elif [[ "$task" == "nmt" ]]; then
    for i in $(seq 3 3 15); do
        par_corpus_split "${i}k"
    done
    par_corpus_split "max"
fi