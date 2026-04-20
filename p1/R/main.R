# Entry point for p1 R analysis.
# Paper: Prompt Quality x GenAI Response.

source("src/00-utils.R")
source("src/01-data-prep.R")
source("src/02-analysis.R")
source("src/03-visualization.R")

# Pipeline: load -> prep -> RM-ANOVA -> plot.
main <- function() {
  data <- load_data("../data/processed/aioq_r_scores.csv")
  cleaned <- prep(data)
  results <- run_rm_anova(cleaned)
  make_figures(results, "output/")
  invisible(results)
}

if (sys.nframe() == 0) main()
