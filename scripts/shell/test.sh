#!/bin/bash

domain="${1}"
model="${2}"
config="${3}"
balance="${4}"
dependency="${5}"

# translate baselines
if [[ -n "$dependency" ]]; then # checks whether dependency is not empty
    job_1=$(sbatch --dependency=afterok:"$dependency" \
        scripts/shell/get_trans.sh "$model" "$config" "$domain" "$balance" | awk '{print $4}')
else
    job_1=$(sbatch \
        scripts/shell/get_trans.sh "$model" "$config" "$domain" "$balance" | awk '{print $4}')
fi

# evaluate baselines
job_2=$(sbatch --dependency=afterok:"$job_1" \
    scripts/shell/get_evals.sh "$domain" "$config" "$model" "$balance" | awk '{print $4}')

echo "$job_2"