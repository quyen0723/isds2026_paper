# Utilities for p1 R pipeline. Loaded first by main.R.

suppressPackageStartupMessages({
  ok <- requireNamespace("dplyr", quietly = TRUE) &&
        requireNamespace("tidyr", quietly = TRUE) &&
        requireNamespace("rstatix", quietly = TRUE)
  if (!ok) {
    message("INFO: rstatix/dplyr/tidyr not installed; synthetic-data path still runs base-R only.")
  }
})

load_data <- function(path) {
  if (file.exists(path) && file.info(path)$size > 0) {
    return(utils::read.csv(path, stringsAsFactors = FALSE))
  }
  message(sprintf("INFO: %s not found; generating N=30 synthetic exemplar.", path))
  set.seed(20260421L)
  participants <- 1:30
  levels <- c("basic", "intermediate", "advanced")
  platforms <- c("gpt-4o-2024-08-06", "claude-sonnet-4-5-20250929")
  tasks <- c("algorithm_explanation", "debugging", "complexity_analysis")
  grid <- expand.grid(
    participant_id = participants,
    prompt_level = levels,
    platform = platforms,
    task_type = tasks,
    KEEP.OUT.ATTRS = FALSE,
    stringsAsFactors = FALSE
  )
  mu <- c(basic = 12.5, intermediate = 18.0, advanced = 21.5)
  bump <- ifelse(grid$platform == "claude-sonnet-4-5-20250929", 0.8, 0.0)
  grid$composite_aioq_r <- pmin(pmax(rnorm(nrow(grid), mu[grid$prompt_level] + bump, 1.3), 5), 25)
  grid$composite_aioq_r <- round(grid$composite_aioq_r, 2)
  grid
}
