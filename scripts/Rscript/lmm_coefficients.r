library(lme4)

# define args
args <- commandArgs(trailingOnly = TRUE)
inp_path <- args[1]
out_path <- args[2]
out_file <- args[3]
metric <- args[4]

csv_data <- read.csv(inp_path) # load csv data

# all fixed terms and their effects
full_preds <- "~ train_data_size * model_design * train_domain + (1 | sentence)"

# exclude one fixed term
design_domain_preds <- "~ model_design * train_domain + (1 | sentence)"
design_size_preds <- "~ model_design * train_data_size + (1 | sentence)"
size_domain_preds <- "~ train_domain * train_data_size + (1 | sentence)"

# define small function for less clutter
get_model <- function(preds) {
  lmer(
    formula = as.formula(paste(metric, preds)),
    data = csv_data,
    REML = FALSE
  )
}

# make models investigating impact on performance by removing one fixed term
full <- get_model(full_preds) # all fixed term
semi_design_domain <- get_model(design_domain_preds)
semi_design_size <- get_model(design_size_preds)
semi_size_domain <- get_model(size_domain_preds)

size_impact <- anova(full, semi_design_domain) # impact of tuning data size
domain_impact <- anova(full, semi_design_size) # impact of fine-tuning domain
design_impact <- anova(full, semi_size_domain) # impact of model design

# store everything in a .txt
capture.output({
  cat("Fine-Tuning Data Size Impact:\n")
  print(size_impact)
  cat("\nFine-Tuning Domain Impact:\n")
  print(domain_impact)
  cat("\nModel Design Impact:\n")
  print(design_impact)
}, file = file.path(out_path, out_file))