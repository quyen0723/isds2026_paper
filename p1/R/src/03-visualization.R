# Visualisation. Writes PNGs to output_dir.

make_figures <- function(results, output_dir) {
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
  }
  out <- file.path(output_dir, "rm_anova_summary.txt")
  utils::capture.output(print(results), file = out)
  message(sprintf("wrote %s", out))
  invisible(out)
}
