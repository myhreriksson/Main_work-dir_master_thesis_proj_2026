library(lme4)

args <- commandArgs(trailingOnly = TRUE)
inp_path <- args[1]
out_path <- args[2]
out_file <- args[3]
metric <- args[4]

csv_data <- read.csv(inp_path)
csv_data_model <- lmer(
    as.formula(paste(metric, "~ train_data_size * model_design * train_domain + (1 | sentence)")), # nolint
                       data = csv_data)

capture.output(
  print(csv_data_model),
  file = file.path(out_path, out_file)
)