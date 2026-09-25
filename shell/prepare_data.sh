task="${1}"
domain_A="${2}"
lang="${3}"

if [[ "$task" == "nmt" ]]; then
    if [[ "$domain_A" == "game" ]]; then
        domain_B='pseudo'
        domain_A_path=data/"$domain_A"_data/preprocessed_tk_al_cl_ed_FINAL/*
    elif [[ "$domain_A" == "bible" ]]; then
        domain_B='archaic'
        domain_A_path=data/"$domain_A"_data/final/*
    fi

    en_path="data/_test-n-finetune_/${domain_B}_eng/"
    de_path="data/_test-n-finetune_/${domain_B}_deu/"

    rm -f \
        "$en_path"*.txt \
        "$de_path"*.txt

    for i in $domain_A_path; do # DON'T make string of $domain_A_path, else the wildcard fails!!!
        file=$(basename "$i")
        if [[ "$file" == *EN.txt ]]; then 
            cat "$i" >> "${en_path}${domain_A}_EN.txt"
            printf '\n' >> "${en_path}${domain_A}_EN.txt"
        elif [[ "$file" == *DE.txt ]]; then
            cat "$i" >> "${de_path}${domain_A}_DE.txt"
            printf '\n' >> "${de_path}${domain_A}_DE.txt"
        fi
    done
elif [[ "$task" == "llm" ]]; then
    inp_path="data/${domain_A}_data/tokenized/"
    out_path="data/_test-n-finetune_/${domain_A}_${lang}/"
    mkdir -p "$inp_path" "$out_path"
    python python/concatenate.py \
        -i "$inp_path" \
        -o "$out_path" \
        -l "$lang" \
        -d "$domain_A"
fi