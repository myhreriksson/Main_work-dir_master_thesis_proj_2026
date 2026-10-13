library(lme4)

# define args
args <- commandArgs(trailingOnly = TRUE)
inp_path <- args[1]
out_path <- args[2]
out_file <- args[3]
metric <- args[4]

csv_data <- read.csv(inp_path) # load csv data
predictors <- "~ train_data_size * model_design * train_domain + (1 | sentence)"
formula <- as.formula(paste(metric, predictors))

# define LMM
model <- lmer(
  formula = formula,
  data = csv_data,
  REML = FALSE
)

capture.output(
  print(summary(model)),
  file = file.path(out_path, out_file)
)

# anova(null_model, semi_model, full_model)