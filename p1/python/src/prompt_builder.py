"""Dispatcher over the three task-type prompt builders.

Each builder lives in its own module and returns an RCIFENI-O-structured
prompt for the requested CLEAR level (basic / intermediate / advanced).
``{signature}`` is expected to be the HumanEval ``prompt`` field
(function signature + docstring).
"""

from __future__ import annotations

from .prompts_algo import build as _build_algo
from .prompts_cx import build as _build_cx
from .prompts_ps import build as _build_ps

LEVELS = ("basic", "intermediate", "advanced")
TASK_TYPES = ("algorithm_explanation", "complexity_analysis", "problem_solving")

_BUILDERS = {
    "algorithm_explanation": _build_algo,
    "complexity_analysis": _build_cx,
    "problem_solving": _build_ps,
}


def build(task_type: str, level: str, signature: str) -> str:
    if task_type not in _BUILDERS:
        raise KeyError(f"unknown task_type: {task_type}")
    if level not in LEVELS:
        raise KeyError(f"unknown level: {level}")
    return _BUILDERS[task_type](level, signature)


def all_prompts(signature: str) -> list[dict]:
    return [
        {"task_type": tt, "prompt_level": lvl, "text": build(tt, lvl, signature)}
        for tt in TASK_TYPES
        for lvl in LEVELS
    ]
