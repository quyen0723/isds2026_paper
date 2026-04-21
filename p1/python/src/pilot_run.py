"""Appendix-B pilot runner.

Pipeline: HumanEval sample → CLEAR prompts (3 task_types × 3 levels)
         → GPT-4o-mini (relay) → AIOQ-R LLM-as-judge → JSONL + CSV.

This is a computational FEASIBILITY pilot. It exercises the whole pipeline end
to end; it is not a substitute for the IRB-gated human-participant experiment
described in Section 4 of the manuscript.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from .dataset_loader import iter_normalised, load_humaneval, sample
from .judge import DIMS, score
from .llm_client import ask, log_call
from .prompt_builder import all_prompts


def run(humaneval_path: str, out_dir: str, n_problems: int = 10) -> dict[str, Any]:
    tasks = iter_normalised(sample(load_humaneval(humaneval_path), n_problems))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    call_log = out / "calls.jsonl"
    results: list[dict[str, Any]] = []

    started = datetime.utcnow().isoformat() + "Z"
    for task in tasks:
        for p in all_prompts(task["prompt_code"]):
            gen = ask(p["text"])
            log_call(call_log, {"phase": "generate", "task_id": task["task_id"], **p, **gen})
            jd = score(p["text"], gen["text"])
            log_call(call_log, {"phase": "judge", "task_id": task["task_id"], **p, **jd})
            results.append({
                "participant_id": task["task_id"],
                "task_type": p["task_type"],
                "prompt_level": p["prompt_level"],
                "platform": "gpt-4o-mini",
                **{d: jd[d] for d in DIMS},
                "composite_aioq_r": jd["composite_aioq_r"],
                "gen_wall_ms": gen.get("wall_ms"),
                "gen_cached": gen.get("cached", False),
                "judge_wall_ms": jd.get("judge_wall_ms"),
                "judge_cached": jd.get("judge_cached", False),
            })

    df = pd.DataFrame(results)
    df.to_csv(out / "pilot_aioq_r_scores.csv", index=False)
    with (out / "pilot_raw.jsonl").open("w", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary = {
        "started_utc": started,
        "ended_utc": datetime.utcnow().isoformat() + "Z",
        "n_problems": n_problems,
        "n_task_types": df["task_type"].nunique(),
        "n_levels": df["prompt_level"].nunique(),
        "n_sessions": int(len(df)),
        "mean_composite_by_level": df.groupby("prompt_level", observed=True)["composite_aioq_r"].mean().to_dict(),
        "cache_hit_rate_gen": float(df["gen_cached"].mean()),
        "cache_hit_rate_judge": float(df["judge_cached"].mean()),
    }
    (out / "pilot_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
