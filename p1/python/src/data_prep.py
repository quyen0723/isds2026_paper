"""Data ingestion and cleaning for p1.

Protocol paper: no empirical data exists at submission time. ``load_raw``
therefore either reads a real JSONL session log if present, or synthesises a
deterministic N=30 exemplar so the pipeline is executable end-to-end.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _synthesise_sessions(n_participants: int = 30, seed: int = 20260421) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    levels = ["basic", "intermediate", "advanced"]
    platforms = ["gpt-4o-2024-08-06", "claude-sonnet-4-5-20250929"]
    tasks = ["algorithm_explanation", "debugging", "complexity_analysis"]
    means = {"basic": 12.5, "intermediate": 18.0, "advanced": 21.5}
    rows = []
    for pid in range(1, n_participants + 1):
        for lvl in levels:
            for plat in platforms:
                for task in tasks:
                    mu = means[lvl] + (0.8 if plat.startswith("claude") else 0.0)
                    score = float(np.clip(rng.normal(mu, 1.3), 5.0, 25.0))
                    rows.append(
                        {
                            "participant_id": pid,
                            "prompt_level": lvl,
                            "platform": plat,
                            "task_type": task,
                            "composite_aioq_r": round(score, 2),
                        }
                    )
    return pd.DataFrame(rows)


def load_raw(path: str | Path) -> pd.DataFrame:
    p = Path(path)
    if p.exists() and p.is_file() and p.stat().st_size > 0:
        with p.open("r", encoding="utf-8") as fh:
            records: list[dict[str, Any]] = [json.loads(line) for line in fh if line.strip()]
        return pd.DataFrame.from_records(records)
    return _synthesise_sessions()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    required = {"participant_id", "prompt_level", "platform", "task_type", "composite_aioq_r"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    out = df.dropna(subset=sorted(required)).copy()
    out["prompt_level"] = pd.Categorical(out["prompt_level"], categories=["basic", "intermediate", "advanced"], ordered=True)
    out["platform"] = out["platform"].astype("category")
    out["task_type"] = out["task_type"].astype("category")
    return out.reset_index(drop=True)
