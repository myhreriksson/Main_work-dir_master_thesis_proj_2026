library(lme4)

path = 

csv_data = read.csv(file.choose( ))
csv_data.model = lmer(bleu ~ data_size * model * domain + (1|sentence))