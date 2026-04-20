"""Entry point for p1 Python analysis.

Paper: Prompt Quality x GenAI Response.
Use-cases: data wrangling, API-driven prompt execution, pre-processing for R.
"""

from src.data_prep import load_raw, clean
from src.analysis import summarize
from src.visualization import make_figures


def main() -> None:
    raw = load_raw("../data/raw/sessions.jsonl")
    df = clean(raw)
    summary = summarize(df)
    df.to_csv("../data/processed/aioq_r_scores.csv", index=False)
    make_figures(summary, "output/")


if __name__ == "__main__":
    main()
