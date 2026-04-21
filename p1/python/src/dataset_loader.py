"""HumanEval loader + deterministic sampling for pilot.

HumanEval (Chen et al. 2021, MIT License). 164 Python function-completion tasks.
We sample a deterministic subset by seed and expose normalised fields the pilot
pipeline consumes.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Iterable


def load_humaneval(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"HumanEval file not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def sample(tasks: list[dict], n: int, seed: int = 20260421) -> list[dict]:
    if n > len(tasks):
        raise ValueError(f"n={n} exceeds corpus size {len(tasks)}")
    rng = random.Random(seed)
    idxs = rng.sample(range(len(tasks)), n)
    return [tasks[i] for i in sorted(idxs)]


def normalise(task: dict) -> dict:
    return {
        "task_id": task["task_id"],
        "entry_point": task["entry_point"],
        "prompt_code": task["prompt"],
        "canonical_solution": task["canonical_solution"],
        "tests": task["test"],
    }


def iter_normalised(tasks: Iterable[dict]) -> list[dict]:
    return [normalise(t) for t in tasks]
