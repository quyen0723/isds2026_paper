"""p1 analysis package.

Public modules consumed by ``python/main.py``:
  data_prep       — load_raw, clean (synthetic fallback for the design paper).
  analysis        — summarize (RM-ANOVA, Mauchly).
  visualization   — make_figures (matplotlib + CUD palette).
  dataset_loader  — HumanEval sampling (Appendix-B pilot).
  prompt_builder  — CLEAR 3-level × 3-task_type prompt templates.
  llm_client      — GPT-4o-mini relay HTTP client.
  judge           — LLM-as-judge AIOQ-R scorer.
  pilot_run       — Appendix-B pilot orchestrator.
"""
