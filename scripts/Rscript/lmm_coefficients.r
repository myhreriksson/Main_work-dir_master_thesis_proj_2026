library(lme4)

args <- commandArgs(trailingOnly = TRUE)
inp_path <- args[1]
out_path <- args[2]
metric <- args[3]

csv_data <- read.csv(inp_path)
csv_data_model <- lmer(metric ~ data_size * model * domain + (1 | sentence), # nolint
                       data = csv_data)

capture.output(
  print(csv_data_model),
  file = out_path
)