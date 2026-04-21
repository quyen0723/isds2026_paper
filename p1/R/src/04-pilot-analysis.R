# Appendix-B pilot analysis. Small-N within-problem: Friedman primary,
# RM-ANOVA secondary, Kendall W effect size. Reads pilot CSV directly.

CUD <- list(
  Black = "#000000", Orange = "#E69F00", SkyBlue = "#56B4E9",
  BluishGreen = "#009E73", Yellow = "#F0E442", Blue = "#0072B2",
  Vermilion = "#D55E00", ReddishPurple = "#CC79A7"
)

load_pilot <- function(path) {
  if (!file.exists(path)) stop(sprintf("pilot CSV not found: %s", path))
  df <- utils::read.csv(path, stringsAsFactors = FALSE)
  df$prompt_level <- factor(df$prompt_level,
                            levels = c("basic", "intermediate", "advanced"),
                            ordered = TRUE)
  df$task_type <- factor(df$task_type)
  df$participant_id <- as.character(df$participant_id)
  df
}

friedman_by_problem <- function(df) {
  wide <- stats::aggregate(
    composite_aioq_r ~ participant_id + prompt_level,
    data = df, FUN = mean
  )
  mat <- stats::reshape(
    wide, idvar = "participant_id", timevar = "prompt_level",
    direction = "wide"
  )
  scores <- as.matrix(mat[, -1])
  fr <- stats::friedman.test(scores)
  k <- ncol(scores); n <- nrow(scores)
  kendall_w <- as.numeric(fr$statistic) / (n * (k - 1))
  list(
    n_problems = n, k_levels = k,
    chi_sq = as.numeric(fr$statistic),
    df = as.numeric(fr$parameter),
    p_value = as.numeric(fr$p.value),
    kendall_W = round(kendall_w, 4)
  )
}

descriptives <- function(df) {
  agg <- stats::aggregate(
    composite_aioq_r ~ prompt_level + task_type,
    data = df,
    FUN = function(x) c(mean = mean(x), sd = stats::sd(x), n = length(x))
  )
  cbind(agg[, 1:2], as.data.frame(agg$composite_aioq_r))
}

emit_tex_macros <- function(fr, desc, df, tex_path) {
  cell <- function(lvl, task) {
    row <- desc[desc$prompt_level == lvl & desc$task_type == task, ]
    if (nrow(row) == 1 && !is.na(row$sd)) sprintf("%.2f$\\pm$%.2f", row$mean, row$sd)
    else if (nrow(row) == 1) sprintf("%.2f", row$mean)
    else "n/a"
  }
  n_sessions <- nrow(df)
  lines <- c(
    sprintf("\\newcommand{\\PilotN}{%d}", fr$n_problems),
    sprintf("\\newcommand{\\PilotSessions}{%d}", n_sessions),
    sprintf("\\newcommand{\\PilotFriedmanChi}{%.3f}", fr$chi_sq),
    sprintf("\\newcommand{\\PilotFriedmanDF}{%d}", as.integer(fr$df)),
    sprintf("\\newcommand{\\PilotFriedmanP}{%.4f}", fr$p_value),
    sprintf("\\newcommand{\\PilotKendallW}{%.4f}", fr$kendall_W),
    sprintf("\\newcommand{\\PilotAlgoBasic}{%s}", cell("basic", "algorithm_explanation")),
    sprintf("\\newcommand{\\PilotAlgoInt}{%s}",   cell("intermediate", "algorithm_explanation")),
    sprintf("\\newcommand{\\PilotAlgoAdv}{%s}",   cell("advanced", "algorithm_explanation")),
    sprintf("\\newcommand{\\PilotCxBasic}{%s}",   cell("basic", "complexity_analysis")),
    sprintf("\\newcommand{\\PilotCxInt}{%s}",     cell("intermediate", "complexity_analysis")),
    sprintf("\\newcommand{\\PilotCxAdv}{%s}",     cell("advanced", "complexity_analysis")),
    sprintf("\\newcommand{\\PilotPsBasic}{%s}",   cell("basic", "problem_solving")),
    sprintf("\\newcommand{\\PilotPsInt}{%s}",     cell("intermediate", "problem_solving")),
    sprintf("\\newcommand{\\PilotPsAdv}{%s}",     cell("advanced", "problem_solving"))
  )
  writeLines(lines, tex_path)
  invisible(tex_path)
}

run_pilot <- function(input_csv, output_dir, tex_out = NULL) {
  df <- load_pilot(input_csv)
  fr <- friedman_by_problem(df)
  desc <- descriptives(df)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  utils::write.csv(desc, file.path(output_dir, "pilot_descriptives.csv"), row.names = FALSE)
  saveRDS(fr, file.path(output_dir, "pilot_friedman.rds"))
  if (!is.null(tex_out)) emit_tex_macros(fr, desc, df, tex_out)
  cat(sprintf(
    "[pilot] N_problems=%d, k=%d, chi2(%d)=%.3f, p=%.4f, Kendall W=%.4f\n",
    fr$n_problems, fr$k_levels, fr$df, fr$chi_sq, fr$p_value, fr$kendall_W
  ))
  list(friedman = fr, descriptives = desc, cud = CUD)
}
