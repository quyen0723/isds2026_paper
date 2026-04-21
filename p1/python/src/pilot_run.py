"""Appendix-B pilot runner — multi-platform variant.

Pipeline: HumanEval sample → CLEAR prompts (3 task_types × 3 levels)
         → generator(s) → AIOQ-R LLM-as-judge → JSONL + CSV.

Pass ``platforms`` as a list of ``{"label": str, "ask": callable}``
entries; a single-element default runs the GPT-4o-mini relay exactly
like the previous single-platform pilot.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from .dataset_loader import iter_normalised, load_humaneval, sample
from .judge import DIMS, score
from .llm_client import ask as ask_gpt4o
from .llm_client import log_call
from .prompt_builder import all_prompts

AskFn = Callable[[str], dict[str, Any]]
_DEFAULT_PLATFORMS: list[dict[str, Any]] = [{"label": "gpt-4o-mini", "ask": ask_gpt4o}]


def run(humaneval_path: str, out_dir: str, n_problems: int = 10,
        platforms: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    platforms = platforms or _DEFAULT_PLATFORMS
    tasks = iter_normalised(sample(load_humaneval(humaneval_path), n_problems))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    call_log = out / "calls.jsonl"
    results: list[dict[str, Any]] = []
    started = datetime.utcnow().isoformat() + "Z"

    for plat in platforms:
        label = plat["label"]
        ask_fn: AskFn = plat["ask"]
        for task in tasks:
            for p in all_prompts(task["prompt_code"]):
                gen = ask_fn(p["text"])
                log_call(call_log, {"phase": "generate", "platform": label,
                                    "task_id": task["task_id"], **p, **gen})
                jd = score(p["text"], gen["text"])
                log_call(call_log, {"phase": "judge", "platform": label,
                                    "task_id": task["task_id"], **p, **jd})
                results.append({
                    "participant_id": task["task_id"],
                    "task_type": p["task_type"],
                    "prompt_level": p["prompt_level"],
                    "platform": label,
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
        "n_platforms": df["platform"].nunique(),
        "n_task_types": df["task_type"].nunique(),
        "n_levels": df["prompt_level"].nunique(),
        "n_sessions": int(len(df)),
        "mean_composite_by_level": df.groupby(
            "prompt_level", observed=True)["composite_aioq_r"].mean().to_dict(),
        "mean_composite_by_platform": df.groupby(
            "platform", observed=True)["composite_aioq_r"].mean().to_dict(),
        "cache_hit_rate_gen": float(df["gen_cached"].mean()),
        "cache_hit_rate_judge": float(df["judge_cached"].mean()),
    }
    (out / "pilot_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
