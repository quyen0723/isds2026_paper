"""LLM-as-judge scoring on the five AIOQ-R dimensions.

Returns integer Likert scores 1-5 per dimension plus composite (5-25).
Judge model is the same GPT-4o-mini relay — cheap, public, reproducible.
This is a FEASIBILITY pilot rater, not a substitute for the human rater
calibration specified in the main study (CVI / Cohen's kappa).
"""

from __future__ import annotations

import json
import re
from typing import Any

from .llm_client import ask

DIMS = ("accuracy", "completeness", "relevance", "clarity", "learning_value")

_JUDGE_TEMPLATE = """You are an academic rater for AI output quality in a CS learning context.
Score the RESPONSE on five dimensions (integer 1-5 each, where 1=poor, 5=excellent):

- accuracy: technical correctness of the content.
- completeness: coverage of what the task asks for.
- relevance: alignment with the learner's level and the task intent.
- clarity: logical structure, readable formatting.
- learning_value: stimulates Bloom higher-order thinking; explains *why*, not just *what*.

TASK (the user prompt that was sent to the assistant):
<<<TASK
{task_text}
TASK

RESPONSE (the assistant's reply being rated):
<<<RESPONSE
{response_text}
RESPONSE

Return ONE JSON object on a single line and nothing else. Do not use code fences.
Keys MUST be exactly: accuracy, completeness, relevance, clarity, learning_value, rationale.
Keep rationale short (<=200 chars) and DO NOT include code or backslashes in it.
"""

_FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", flags=re.DOTALL | re.IGNORECASE)
_BAD_ESC = re.compile(r"\\(?![\"\\/bfnrtu])")


def _extract_json(text: str) -> dict[str, Any]:
    fence = _FENCE.search(text)
    candidate = fence.group(1) if fence else text
    m = re.search(r"\{.*\}", candidate, flags=re.DOTALL)
    if not m:
        raise ValueError(f"no JSON in judge reply: {text[:200]!r}")
    raw = m.group(0)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            return json.loads(_BAD_ESC.sub(r"\\\\", raw))
        except json.JSONDecodeError:
            return _field_by_field(raw)


def _field_by_field(raw: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for d in DIMS:
        m = re.search(rf'"{d}"\s*:\s*(\d+)', raw)
        if not m:
            raise ValueError(f"missing dim {d}: {raw[:200]!r}")
        out[d] = int(m.group(1))
    m = re.search(r'"rationale"\s*:\s*"(.*?)"\s*[,}]', raw, flags=re.DOTALL)
    out["rationale"] = m.group(1)[:500] if m else ""
    return out


def score(task_text: str, response_text: str, retries: int = 2) -> dict[str, Any]:
    prompt = _JUDGE_TEMPLATE.format(task_text=task_text, response_text=response_text)
    last_err: Exception | None = None
    for _ in range(retries + 1):
        reply = ask(prompt)
        try:
            obj = _extract_json(reply["text"])
            dims = {d: max(1, min(5, int(obj[d]))) for d in DIMS}
            return {
                **dims,
                "composite_aioq_r": sum(dims.values()),
                "rationale": str(obj.get("rationale", ""))[:500],
                "judge_wall_ms": reply.get("wall_ms"),
                "judge_cached": reply.get("cached", False),
            }
        except (ValueError, KeyError, TypeError) as e:
            last_err = e
    raise RuntimeError(f"judge parse failed after {retries + 1} attempts: {last_err}")
