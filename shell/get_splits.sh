task="${1}"
domain="${2}"

data_path='data/_test-n-finetune_/'
json_path="${data_path}_finetuning/"

if [[ "$task" == "llm" ]]; then
    lang="${3}"
    if [[ "$domain" == "bible" ]]; then
        domain='archaic'
    else
        domain="${2}"
    fi
    mkdir -p "${json_path}ppl/"
    python python/split_txt_corpus.py \
        -i "$data_path" \
        -o "${json_path}ppl/" \
        -d "$domain" \
        -l "$lang" \
        -s 0.8 0.1 0.1 \
        --min_len 5

elif [[ "$task" == "nmt" ]]; then
    for i in $(seq 0 3 15); do
        if (( i > 0 )); then 
            mkdir -p "${json_path}${i}k/" 
            python python/split_par_corpus.py \
                -p "$data_path" \
                -o "${json_path}${i}k/" \
                -d "${domain}_deu/" \
                -e "${domain}_eng/" \
                -n "$domain" \
                -s 0.8 0.1 0.1 \
                --data_size "$i" \
                --min_len 4
        fi
    done
    mkdir -p "${json_path}max/" 
    python python/split_par_corpus.py \
        -p "$data_path" \
        -o "${json_path}max/" \
        -d "${domain}_deu/" \
        -e "${domain}_eng/" \
        -n "$domain" \
        -s 0.8 0.1 0.1 \
        --data_size 'max' \
        --min_len 4
fi