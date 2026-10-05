model="${1}"
out_path="results/evaluations/base/flores_200/"
mkdir -p "$out_path"
{
    sacrebleu "data/flores_data/flores_deu/flores_DE.txt" \
        -i "results/translations/base/flores_200/flores_Translation_${model}_EN-DE.txt" \
        -m bleu ter \
        -l en-de
} > "${out_path}/flores_sacrebleu_${model}.json"