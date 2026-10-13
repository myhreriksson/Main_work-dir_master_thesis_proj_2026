#----------Significance testing WITHIN models (compares change from baseline per model)
sbatch scripts/shell/get_pvals.sh game nllb unbalanced inter
sbatch scripts/shell/get_pvals.sh game bart unbalanced inter 
sbatch scripts/shell/get_pvals.sh bible nllb '' inter
sbatch scripts/shell/get_pvals.sh bible bart '' inter
sbatch scripts/shell/get_pvals.sh game nllb balanced inter 
sbatch scripts/shell/get_pvals.sh game bart balanced inter
bash scripts/shell/get_holm.sh inter

#----------Significance testing ACROSS models (compares change between models per config) 
sbatch scripts/shell/get_pvals.sh game bart unbalanced cross
sbatch scripts/shell/get_pvals.sh bible bart '' cross
sbatch scripts/shell/get_pvals.sh game bart balanced cross 
# OBS! since comparison between models is the same regardless of model input, bart was arbitrarily selected
bash scripts/shell/get_holm.sh cross
bash scripts/shell/get_holm.sh inter