"""CLEAR-framework prompt templates for 3 quality levels × 3 task types.

CLEAR (Lo 2023): Concise, Logical, Explicit, Adaptive, Reflective.
- L1 basic: 0-1 CLEAR criteria (vague directive).
- L2 intermediate: 2-3 criteria (concise + explicit).
- L3 advanced: 4-5 criteria (full CLEAR with self-check + role).

Task types are framings of the SAME HumanEval problem, not different corpora.
"""

from __future__ import annotations

LEVELS = ("basic", "intermediate", "advanced")
TASK_TYPES = ("algorithm_explanation", "complexity_analysis", "problem_solving")

_TEMPLATES: dict[tuple[str, str], str] = {
    ("algorithm_explanation", "basic"): "Explain this:\n\n{signature}",
    ("algorithm_explanation", "intermediate"):
        "You are teaching CS. Concisely explain the algorithm for this function. "
        "List the steps in order.\n\n{signature}",
    ("algorithm_explanation", "advanced"):
        "As a CS tutor for an IT undergraduate, provide a structured explanation of the algorithm "
        "behind the function below. Follow these steps: "
        "(1) restate the problem in plain English; "
        "(2) outline the high-level approach; "
        "(3) walk through the key invariants or data flow; "
        "(4) state when this approach is preferred over alternatives. "
        "Use concise prose, adapt vocabulary to an undergraduate audience, and end with a one-sentence "
        "self-check: 'Does this explanation help someone solve a similar problem themselves?'\n\n{signature}",

    ("complexity_analysis", "basic"): "What is the complexity of this?\n\n{signature}",
    ("complexity_analysis", "intermediate"):
        "Analyze the time and space complexity of this function. State the Big-O at the end.\n\n{signature}",
    ("complexity_analysis", "advanced"):
        "As a CS tutor, conduct a complexity analysis for the function below. Follow these steps: "
        "(1) identify loops and recursions; "
        "(2) count operations symbolically; "
        "(3) derive worst-case time T(n) and auxiliary space S(n); "
        "(4) comment on whether this is asymptotically optimal for the problem; "
        "(5) end with a self-check: 'Can a student replicate this analysis on a similar problem?'\n\n{signature}",

    ("problem_solving", "basic"): "Solve:\n\n{signature}",
    ("problem_solving", "intermediate"):
        "Write a Python implementation for the function below. Return only the function body "
        "(no explanation).\n\n{signature}",
    ("problem_solving", "advanced"):
        "You are a senior Python engineer mentoring an IT undergraduate. Write a clean, idiomatic "
        "Python implementation for the function below. Requirements: "
        "(1) include a one-line docstring summary; "
        "(2) use Pythonic constructs where appropriate; "
        "(3) avoid external libraries; "
        "(4) aim for the best complexity you can justify; "
        "(5) end with a brief comment verifying edge cases you considered.\n\n{signature}",
}


def build(task_type: str, level: str, signature: str) -> str:
    key = (task_type, level)
    if key not in _TEMPLATES:
        raise KeyError(f"unknown (task_type, level): {key}")
    return _TEMPLATES[key].format(signature=signature.strip())


def all_prompts(signature: str) -> list[dict]:
    out = []
    for tt in TASK_TYPES:
        for lvl in LEVELS:
            out.append({"task_type": tt, "prompt_level": lvl, "text": build(tt, lvl, signature)})
    return out
