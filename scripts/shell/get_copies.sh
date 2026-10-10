#!/bin/bash

domain="${1}"
model="${2}"
metric="${3}"
balance="${4}"

copy() {
    if [[ "$domain" == "game" ]]; then
        model_domain="bible"
    elif [[ "$domain" == "bible" ]]; then
        model_domain="game"
    fi
    local size="${1}"
    local tgt_dir="files/"
    local trans_path="results/translations/tuned/${size}/${domain}/${balance}"
    local evals_path="results/evaluations/tuned/${size}/${domain}/${balance}"
    local trans_file="${domain}_Translation_${model}_EN-DE.txt"
    local evals_file="${domain}_${metric}_per_sent_${model}.txt"
    mkdir -p "$tgt_dir"
    cp "${trans_path}/${trans_file}" "${tgt_dir}/translation-${balance}_${model_domain}-${model}-${size}.txt"
    cp "${evals_path}/${evals_file}" "${tgt_dir}/sent_evals-${balance}_${model_domain}-${model}-${size}-${metric}.txt"
}

for i in $(seq 3 3 15); do
    copy "${i}k"
done
copy "max"