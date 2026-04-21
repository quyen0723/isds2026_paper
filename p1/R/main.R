# Entry point for p1 R analysis.
# Paper: Prompt Quality x GenAI Response.
# Sub-commands:
#   Rscript main.R            -> design analysis (synthetic / future real data).
#   Rscript main.R pilot      -> Appendix-B pilot analysis on pilot_aioq_r_scores.csv.

source("src/00-utils.R")
source("src/01-data-prep.R")
source("src/02-analysis.R")
source("src/03-visualization.R")
source("src/04-pilot-analysis.R")
source("src/05-pilot-figures.R")

main_design <- function() {
  data <- load_data("../data/processed/aioq_r_scores.csv")
  cleaned <- prep(data)
  results <- run_rm_anova(cleaned)
  make_figures(results, "output/")
  invisible(results)
}

main_pilot <- function() {
  result <- run_pilot(
    input_csv = "../data/processed/pilot_aioq_r_scores.csv",
    output_dir = "output/",
    tex_out = "../latex/pilot-macros.tex"
  )
  plot_all(result, "output/")
  invisible(result)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) > 0 && args[1] == "pilot") main_pilot() else main_design()
}
