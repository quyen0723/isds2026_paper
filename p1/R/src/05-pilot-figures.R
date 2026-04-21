# CUD-palette figures for the Appendix-B pilot. Base R (no ggplot dep).

plot_pilot_bars <- function(result, output_dir) {
  desc <- result$descriptives
  levels_order <- c("basic", "intermediate", "advanced")
  tasks <- levels(factor(desc$task_type))
  cud <- result$cud
  fills <- c(cud$SkyBlue, cud$Orange, cud$BluishGreen)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  png(file.path(output_dir, "pilot_aioq_by_level_task.png"),
      width = 1700, height = 1050, res = 200)
  old_par <- graphics::par(mar = c(5, 4.5, 4.5, 1), family = "sans",
                           xpd = TRUE)
  on.exit(graphics::par(old_par), add = TRUE)
  mat <- matrix(NA_real_, nrow = length(levels_order), ncol = length(tasks))
  sds <- matrix(NA_real_, nrow = length(levels_order), ncol = length(tasks))
  rownames(mat) <- levels_order; colnames(mat) <- tasks
  rownames(sds) <- levels_order; colnames(sds) <- tasks
  for (i in seq_along(levels_order)) for (j in seq_along(tasks)) {
    row <- desc[desc$prompt_level == levels_order[i] & desc$task_type == tasks[j], ]
    if (nrow(row) == 1) { mat[i, j] <- row$mean; sds[i, j] <- row$sd }
  }
  bp <- graphics::barplot(mat, beside = TRUE, col = fills,
                          ylim = c(0, 25),
                          ylab = "Composite AIOQ-R (5-25)",
                          xlab = "Task type", las = 1)
  graphics::arrows(bp, mat - sds, bp, mat + sds,
                   angle = 90, code = 3, length = 0.04, col = cud$Black)
  graphics::abline(h = c(5, 25), lty = 3, col = cud$Black)
  # Legend above the plot area (xpd=TRUE) so it never overlaps bars.
  graphics::legend(
    x = mean(range(bp)), y = 28.5,
    legend = levels_order, fill = fills,
    horiz = TRUE, bty = "n", cex = 0.95, xjust = 0.5
  )
  dev.off()
}

plot_pilot_heatmap <- function(result, output_dir) {
  desc <- result$descriptives
  cud <- result$cud
  wide <- reshape(desc[, c("prompt_level", "task_type", "mean")],
                  idvar = "prompt_level", timevar = "task_type",
                  direction = "wide")
  mat <- as.matrix(wide[, -1])
  rownames(mat) <- as.character(wide$prompt_level)
  colnames(mat) <- sub("^mean\\.", "", colnames(mat))
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  png(file.path(output_dir, "pilot_aioq_heatmap.png"),
      width = 1800, height = 1200, res = 200)
  old_par <- graphics::par(mar = c(9, 11, 1.5, 2), family = "sans",
                           mgp = c(3, 0.6, 0))
  on.exit(graphics::par(old_par), add = TRUE)
  pal <- grDevices::colorRampPalette(
    c(cud$Blue, cud$SkyBlue, cud$Yellow, cud$Orange, cud$Vermilion)
  )(64)
  rng <- range(mat, na.rm = TRUE)
  pad <- max(0.5, 0.1 * diff(rng))
  zlim <- c(floor((rng[1] - pad) * 10) / 10, ceiling((rng[2] + pad) * 10) / 10)
  image(x = seq_len(ncol(mat)), y = seq_len(nrow(mat)), z = t(mat),
        col = pal, axes = FALSE, xlab = "", ylab = "", zlim = zlim)
  graphics::axis(1, at = seq_len(ncol(mat)), labels = colnames(mat),
                 las = 2, cex.axis = 1.0, tick = FALSE)
  graphics::axis(2, at = seq_len(nrow(mat)), labels = rownames(mat),
                 las = 1, cex.axis = 1.0, tick = FALSE)
  for (i in seq_len(nrow(mat))) for (j in seq_len(ncol(mat))) {
    txt <- sprintf("%.1f", mat[i, j])
    graphics::text(j, i, txt, cex = 1.1, col = cud$Black, font = 2)
  }
  dev.off()
}

plot_all <- function(result, output_dir) {
  plot_pilot_bars(result, output_dir)
  plot_pilot_heatmap(result, output_dir)
}
