#!/bin/bash

#----------Significance testing WITHIN models (compares change from baseline per model)
pval_1=$(sbatch scripts/shell/get_pvals.sh game nllb unbalanced inter | awk '{print $4}')
pval_2=$(sbatch scripts/shell/get_pvals.sh game bart unbalanced inter | awk '{print $4}')
pval_3=$(sbatch scripts/shell/get_pvals.sh bible nllb '' inter | awk '{print $4}')
pval_4=$(sbatch scripts/shell/get_pvals.sh bible bart '' inter | awk '{print $4}')
pval_5=$(sbatch scripts/shell/get_pvals.sh game nllb balanced inter | awk '{print $4}')
pval_6=$(sbatch scripts/shell/get_pvals.sh game bart balanced inter | awk '{print $4}')

inter_pvals="$pval_1:$pval_2:$pval_3:$pval_4:$pval_5:$pval_6"
sbatch --dependency=afterok:"$inter_pvals" scripts/shell/get_holm.sh inter

#----------Significance testing ACROSS models (compares change between models per config) 
pval_7=$(sbatch scripts/shell/get_pvals.sh game bart unbalanced cross | awk '{print $4}')
pval_8=$(sbatch scripts/shell/get_pvals.sh bible bart '' cross | awk '{print $4}')
pval_9=$(sbatch scripts/shell/get_pvals.sh game bart balanced cross | awk '{print $4}')
# OBS! since comparison between models is the same regardless of model input, bart was arbitrarily selected

cross_pvals="$pval_7:$pval_8:$pval_9"
sbatch --dependency=afterok:"$cross_pvals" scripts/shell/get_holm.sh cross
sbatch --dependency=afterok:"$cross_pvals" scripts/shell/get_holm.sh inter