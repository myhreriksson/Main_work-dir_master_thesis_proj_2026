#!/bin/bash

translate_1=$(sbatch shell/get_flores_test.sh bart | awk '{print $4}')
translate_2=$(sbatch shell/get_flores_test.sh nllb | awk '{print $4}')
sbatch --dependency=afterok:$translate_1 shell/get_flores_evals.sh bart
sbatch --dependency=afterok:$translate_2 shell/get_flores_evals.sh nllb