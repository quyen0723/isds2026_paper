"""Entry point for p1 Python analysis.

Paper: Prompt Quality x GenAI Response.
Two sub-commands:
  python main.py pilot   — run the Appendix-B computational feasibility pilot.
  python main.py analyze — run the protocol-style summary on whatever sessions
                           JSONL is present in ../data/raw/.
"""

from __future__ import annotations

import sys
from pathlib import Path

from src.analysis import summarize
from src.data_prep import clean, load_raw
from src.pilot_run import run as run_pilot
from src.visualization import make_figures


HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "data" / "raw"
PROCESSED = HERE.parent / "data" / "processed"


def _analyze() -> None:
    raw = load_raw(str(RAW / "sessions.jsonl"))
    df = clean(raw)
    summary = summarize(df)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "aioq_r_scores.csv", index=False)
    make_figures(summary, str(HERE / "output"))


def _pilot(n: int) -> None:
    summary = run_pilot(
        humaneval_path=str(RAW / "HumanEval.jsonl"),
        out_dir=str(PROCESSED),
        n_problems=n,
    )
    print("pilot done:", summary)


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "analyze"
    if cmd == "pilot":
        n = int(argv[2]) if len(argv) > 2 else 10
        _pilot(n)
    elif cmd == "analyze":
        _analyze()
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
