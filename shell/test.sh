#!/bin/bash

style="${1}"
model="${2}"
config="${3}"
dependency="${4}"

# translate baselines
if [[ -n "$dependency" ]]; then # checks whether dependency is not empty
    job_1=$(sbatch --dependency=afterok:"$dependency" \
        shell/get_translations.sh "$model" "$config" "$style" | awk '{print $4}')
else
    job_1=$(sbatch \
        shell/get_translations.sh "$model" "$config" "$style" | awk '{print $4}')
fi

# evaluate baselines
job_2=$(sbatch --dependency=afterok:"$job_1" \
    shell/evaluate.sh "$style" "$config" "$model" | awk '{print $4}')

echo "$job_2"