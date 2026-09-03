#!/bin/bash

# bible data:
en_bible_1=https://www.gutenberg.org/cache/epub/10/pg10.txt # King James Version
# prose data:
en_prose_1=https://www.gutenberg.org/ebooks/395.txt.utf-8 # holy war by bunyan
en_prose_2=https://www.gutenberg.org/ebooks/17181.txt.utf-8 # rosalynde by lodge
en_prose_3=https://www.gutenberg.org/ebooks/70854.txt.utf-8 # arcadia by sidney

# bible data:
de_bible_1=http://www.ntslibrary.com/Bible%20-%20German%20Luther%20Translation.pdf # Martin Luthers Bibel
# prose data:
de_prose_1=https://www.gutenberg.org/ebooks/55171.txt.utf-8 # simplicius by grimmelshausen
de_prose_2=https://www.gutenberg.org/ebooks/22355.txt.utf-8 # schelmuffsky by reuter
de_prose_3=https://textgridlab.org/1.0/aggregator/text/textgrid:xdgw.0 # asiatische benise by kliphausen

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

domain="${1}"
lang="${2}"
author="${3}"
extension="${4}"
n="${5}"

path="data/${domain}_data/"
source="${lang}_${domain}_${n}"
source="${!source}"

mkdir -p \
    "${path}/raw/" \
    "${path}/tokenized/"

python python/retrieve_data.py \
    -s "$source" \
    -p "${path}/raw/" \
    -n "${domain}_${author}_raw" \
    -e ".${extension}"

# above is data retrieval, whereas below is preprocessing of aforementioned data
# there's alot of jumping inbetween shellscripts at this stage, which probably could have been avoided, but idc anymore :')

if [[ "$domain" == "bible" ]]; then
    python python/tokenize_bible.py \
        -i "${path}/raw" \
        -o "${path}/tokenized" \
        -n "bible_${author}" \
        -e ".${extension}"
elif [[ "$domain" == "prose" ]]; then
    python python/tokenize_prose.py \
        -i "${path}/raw" \
        -o "${path}/tokenized" \
        -n "${domain}_${author}" \
        -l "$lang"
fi