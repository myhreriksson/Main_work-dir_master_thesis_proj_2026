task="${1}"
domain="${2}"
lang="${3}"

if [[ "$task" == "nmt" ]]; then
    if [[ "$domain" == "game" ]]; then
        style='pseudo'
        domain_path=data/"$domain"_data/preprocessed_tk_al_cl_ed_FINAL/*
    elif [[ "$domain" == "bible" ]]; then
        style='archaic'
        domain_path=data/"$domain"_data/final/*
    fi

    en_path="data/_test-n-finetune_/${style}_eng/"
    de_path="data/_test-n-finetune_/${style}_deu/"

    rm -f \
        "$en_path"*.txt \
        "$de_path"*.txt

    for i in $domain_path; do # DON'T make string of it $domain_path, else the wildcard fails!!!
        file=$(basename "$i")
        if [[ "$file" == *EN.txt ]]; then 
            cat "$i" >> "${en_path}${domain}_EN.txt"
            printf '\n' >> "${en_path}${domain}_EN.txt"
        elif [[ "$file" == *DE.txt ]]; then
            cat "$i" >> "${de_path}${domain}_DE.txt"
            printf '\n' >> "${de_path}${domain}_DE.txt"
        fi
    done
elif [[ "$task" == "llm" ]]; then
    inp_path="data/${domain}_data/tokenized/"
    out_path="data/_test-n-finetune_/${domain}_${lang}/"
    mkdir -p "$inp_path" "$out_path"
    python python/concatenate.py \
        -i "$inp_path" \
        -o "$out_path" \
        -l "$lang" \
        -d "$domain"
fi