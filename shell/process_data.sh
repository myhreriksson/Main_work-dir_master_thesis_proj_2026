domain="${1}"

tok_path="data/${domain}_data/tokenized"
fin_path="data/${domain}_data/final"

if [[ "$domain" == "bible" ]]; then
    mkdir -p "$fin_path" "$tok_path"
    bash shell/get_data.sh "$domain" de ML pdf 1
    bash shell/get_data.sh "$domain" en KJ txt 1

    # postprocessing step
    sed -i '1d' "${tok_path}/${domain}_KJ_tokenized.txt" # deletes first non-verse line of KJV
    sed -i '23145s/.\{94\}$//' "${tok_path}/${domain}_KJ_tokenized.txt" # removes non-verse text from a verse-line
    sed -i '31102s/.\{18236\}$//' "${tok_path}/${domain}_KJ_tokenized.txt" # removes non-verse text from a verse-line
    sed -i '23145s/.\{19\}$//' "${tok_path}/${domain}_ML_tokenized.txt" # removes non-verse text from a verse-line
    sed -i '29561s/.\{66\}$//' "${tok_path}/${domain}_KJ_tokenized.txt" # remove trailing book information (Thessalonius)
    sed -i '29562d' "${tok_path}/${domain}_ML_tokenized.txt" # deletes Thessalonius line (non-verse)

    sed -E 's/^[0-9]+:[0-9]+[[:space:]]//' "${tok_path}/${domain}_KJ_tokenized.txt" > "${fin_path}/KJV_EN.txt"
    sed -E 's/^[0-9]+:[0-9]+[[:space:]]//' "${tok_path}/${domain}_ML_tokenized.txt" > "${fin_path}/MLB_DE.txt"

    echo "Successfully created parallel ${domain} corpora."

elif [[ "$domain" == "prose" ]]; then
    mkdir -p "$tok_path"
    bash shell/get_data.sh "$domain" de Grimmelshausen txt 1
    bash shell/get_data.sh "$domain" de Reuter txt 2
    bash shell/get_data.sh "$domain" de Kliphausen txt 3
    bash shell/get_data.sh "$domain" en Bunyan txt 1
    bash shell/get_data.sh "$domain" en Lodge txt 2
    bash shell/get_data.sh "$domain" en Sidney txt 3
fi