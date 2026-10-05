#!/bin/bash

sbatch shell/get_flores_test.sh bart
sbatch shell/get_flores_test.sh nllb
sbatch shell/get_flores_evals.sh bart
sbatch shell/get_flores_evals.sh nllb