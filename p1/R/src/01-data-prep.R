# Preparation: coerce types, drop incomplete rows.

prep <- function(data) {
  required <- c("participant_id", "prompt_level", "platform", "task_type", "composite_aioq_r")
  missing <- setdiff(required, names(data))
  if (length(missing) > 0L) {
    stop(sprintf("missing required columns: %s", paste(missing, collapse = ", ")))
  }
  data <- data[stats::complete.cases(data[, required]), , drop = FALSE]
  data$prompt_level <- factor(data$prompt_level, levels = c("basic", "intermediate", "advanced"), ordered = TRUE)
  data$platform <- factor(data$platform)
  data$task_type <- factor(data$task_type)
  data$participant_id <- as.integer(data$participant_id)
  data
}
