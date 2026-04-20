# Two-Way Repeated-Measures ANOVA.
# Uses rstatix if available; falls back to base stats::aov.

run_rm_anova <- function(data) {
  wide <- stats::aggregate(
    composite_aioq_r ~ participant_id + prompt_level + platform,
    data = data,
    FUN = mean
  )
  use_rstatix <- requireNamespace("rstatix", quietly = TRUE)
  if (use_rstatix) {
    fit <- rstatix::anova_test(
      data = wide,
      dv = composite_aioq_r,
      wid = participant_id,
      within = c(prompt_level, platform)
    )
    return(list(engine = "rstatix", result = fit, bonferroni_alpha_prime = 0.05 / 5))
  }
  fit <- stats::aov(
    composite_aioq_r ~ prompt_level * platform + Error(factor(participant_id) / (prompt_level * platform)),
    data = wide
  )
  list(engine = "stats::aov", result = summary(fit), bonferroni_alpha_prime = 0.05 / 5)
}
