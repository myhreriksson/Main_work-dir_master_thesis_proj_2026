#!/bin/bash

style="${1}"
model="${2}"
config="${3}"
balance="${4}"
dependency="${5}"

# translate baselines
if [[ -n "$dependency" ]]; then # checks whether dependency is not empty
    job_1=$(sbatch --dependency=afterok:"$dependency" \
        shell/get_translations.sh "$model" "$config" "$style" "$balance" | awk '{print $4}')
else
    job_1=$(sbatch \
        shell/get_translations.sh "$model" "$config" "$style" "$balance" | awk '{print $4}')
fi

# evaluate baselines
job_2=$(sbatch --dependency=afterok:"$job_1" \
    shell/evaluate.sh "$style" "$config" "$model" "$balance" | awk '{print $4}')

echo "$job_2"