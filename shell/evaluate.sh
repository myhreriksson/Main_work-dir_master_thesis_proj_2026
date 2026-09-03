#!/bin/bash
#SBATCH -A uppmax2025-2-505
#SBATCH -M pelle
#SBATCH -p gpu
#SBATCH -t 01:30:00
#SBATCH --gres=gpu:1

source /proj/uppmax2025-2-505/mame0175/thesis_PROJ/miniconda3/etc/profile.d/conda.sh
conda activate thesis-venv

style="${1}"
config="${2}"
model="${3}"

path="data/_test-n-finetune_/${style}_deu/"

# I realize in hindsight that I defenitely could have written this using more intuitive variables instead of this f*cking mess...
# but since I'm a novice at shellscripting, I'm just gonna say idc and call it a day :)

# part 1: evaluate increasing tuning sizes
if [[ "$config" == "tuned" ]]; then
    for i in $(seq 0 3 15); do
        if (( i > 0 )); then
            mkdir -p "results/evaluations/${config}/${i}k/${style}"
            for filename in "$path"*; do
                file=$(basename "$filename")
                {
                    sacrebleu "${path}${file}" \
                        -i "results/translations/${config}/${i}k/${style}/${file%%_*}_Translation_${model}_EN-DE.txt" \
                        -m bleu ter \
                        -l en-de
                } > "results/evaluations/${config}/${i}k/${style}/${file%%_*}_sacrebleu_${model}.json"
                {
                    comet-score \
                        -s "data/_test-n-finetune_/${style}_eng/${file%%_*}_EN.txt" \
                        -t "results/translations/${config}/${i}k/${style}/${file%%_*}_Translation_${model}_EN-DE.txt" \
                        -r "data/_test-n-finetune_/${style}_deu/${file%%_*}_DE.txt" \
                        --quiet \
                        --only_system
                } > "results/evaluations/${config}/${i}k/${style}/${file%%_*}_comet_${model}.txt"

                python python/write_results.py \
                    "results/evaluations/${config}/${i}k/${style}/${file%%_*}_sacrebleu_${model}.json" \
                    "results/evaluations/${config}/${i}k/${style}/${file%%_*}_comet_${model}.txt" \
                    "results/evaluations/${config}/${i}k/${style}/${file%%_*}_Evaluation_${model}.txt" \
                    score

                rm "results/evaluations/${config}/${i}k/${style}/${file%%_*}_comet_${model}.txt" "results/evaluations/${config}/${i}k/${style}/${file%%_*}_sacrebleu_${model}.json"
            done
            echo "Evaluation for size '${i}' is completed!"
        fi
    done

# part 2: evaluate with maximum tuning size
    mkdir -p "results/evaluations/${config}/max/${style}"
    for filename in "$path"*; do
        file=$(basename "$filename")
        {
            sacrebleu "${path}${file}" \
                -i "results/translations/${config}/max/${style}/${file%%_*}_Translation_${model}_EN-DE.txt" \
                -m bleu ter \
                -l en-de
        } > "results/evaluations/${config}/max/${style}/${file%%_*}_sacrebleu_${model}.json"
        {
            comet-score \
                -s "data/_test-n-finetune_/${style}_eng/${file%%_*}_EN.txt" \
                -t "results/translations/${config}/max/${style}/${file%%_*}_Translation_${model}_EN-DE.txt" \
                -r "data/_test-n-finetune_/${style}_deu/${file%%_*}_DE.txt" \
                --quiet \
                --only_system
        } > "results/evaluations/${config}/max/${style}/${file%%_*}_comet_${model}.txt"

        python python/write_results.py \
            "results/evaluations/${config}/max/${style}/${file%%_*}_sacrebleu_${model}.json" \
            "results/evaluations/${config}/max/${style}/${file%%_*}_comet_${model}.txt" \
            "results/evaluations/${config}/max/${style}/${file%%_*}_Evaluation_${model}.txt" \
            score

        rm "results/evaluations/${config}/max/${style}/${file%%_*}_comet_${model}.txt" "results/evaluations/${config}/max/${style}/${file%%_*}_sacrebleu_${model}.json"
    done
    echo "Evaluation for size 'max' is completed!"

# part 3: evaluate baselines
elif [[ "$config" == "base" ]]; then
    mkdir -p "results/evaluations/${config}/${style}"
    for filename in "$path"*; do
        file=$(basename "$filename")
        {
            sacrebleu "${path}${file}" \
                -i "results/translations/${config}/${style}/${file%%_*}_Translation_${model}_EN-DE.txt" \
                -m bleu ter \
                -l en-de
        } > "results/evaluations/${config}/${style}/${file%%_*}_sacrebleu_${model}.json"
        {
            comet-score \
                -s "data/_test-n-finetune_/${style}_eng/${file%%_*}_EN.txt" \
                -t "results/translations/${config}/${style}/${file%%_*}_Translation_${model}_EN-DE.txt" \
                -r "data/_test-n-finetune_/${style}_deu/${file%%_*}_DE.txt" \
                --quiet \
                --only_system
        } > "results/evaluations/${config}/${style}/${file%%_*}_comet_${model}.txt"

        python python/write_results.py \
            "results/evaluations/${config}/${style}/${file%%_*}_sacrebleu_${model}.json" \
            "results/evaluations/${config}/${style}/${file%%_*}_comet_${model}.txt" \
            "results/evaluations/${config}/${style}/${file%%_*}_Evaluation_${model}.txt" \
            score

        rm "results/evaluations/${config}/${style}/${file%%_*}_comet_${model}.txt" "results/evaluations/${config}/${style}/${file%%_*}_sacrebleu_${model}.json"
    done
    echo "Base evaluation is completed!"
fi