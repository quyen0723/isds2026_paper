"""Raw OpenCode CLI client — no pre-prompt wrapper.

Motivation: the RCIFENI-O enforcement inside
``.fong/tools/zai-rcifeni-o-relay.sh`` and the ``mcp__mcp-zai`` MCP
tool both wrap the user's prompt inside an additional pre-prompt
template. That wrapping confounds the paper's independent variable,
because an L1 ``Solve: ...`` prompt arriving at the model after the
wrapper has injected Role/Context/Instructions is effectively an L2-
or L3-shaped prompt. This client bypasses every wrapper: whatever
string you pass becomes the model's first user message, verbatim.

The underlying provider is OpenCode.ai (CLI at ``$HOME/.opencode/bin/
opencode``); the paper labels the platform as ``OpenCode CLI /
GLM-5.1`` — implementation in practice, model in theory.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from typing import Any

CLI = "/home/fong/.opencode/bin/opencode"
CLI_MODEL_ARG = "ollama-cloud/glm-5.1"  # user's default working route
PUBLIC_MODEL_LABEL = "glm-5.1"          # platform label reported in paper
COOLDOWN_S = 1.5
TIMEOUT_S = 180
_LAST = [0.0]
_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _throttle() -> None:
    wait = COOLDOWN_S - (time.time() - _LAST[0])
    if wait > 0:
        time.sleep(wait)
    _LAST[0] = time.time()


def _extract_json_events(stdout: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = _ANSI.sub("", line).strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def _extract_text(events: list[dict[str, Any]], fallback: str) -> str:
    chunks: list[str] = []
    for ev in events:
        if ev.get("type") != "text":
            continue
        part = ev.get("part") or {}
        if isinstance(part, dict) and isinstance(part.get("text"), str):
            chunks.append(part["text"])
        elif isinstance(ev.get("text"), str):
            chunks.append(ev["text"])
    return "".join(chunks).strip() or fallback


def ask(prompt: str) -> dict[str, Any]:
    _throttle()
    start = time.time()
    cmd = [CLI, "run", "-m", CLI_MODEL_ARG, "--format", "json", prompt]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        wall = int((time.time() - start) * 1000)
        return {"text": "[timeout] inference exceeded wall-time budget",
                "model": PUBLIC_MODEL_LABEL, "wall_ms": wall,
                "cached": False, "returncode": -1, "error": "timeout"}
    wall = int((time.time() - start) * 1000)
    events = _extract_json_events(proc.stdout)
    err = next((e for e in events if e.get("type") == "error"), None)
    if err:
        msg = err.get("error", {}).get("data", {}).get("message", str(err))
        return {"text": f"[error] {msg}", "model": PUBLIC_MODEL_LABEL,
                "wall_ms": wall, "cached": False,
                "returncode": proc.returncode, "error": msg}
    stripped = _ANSI.sub("", proc.stdout)
    text = _extract_text(events, stripped.strip() or proc.stderr)
    return {"text": text, "model": PUBLIC_MODEL_LABEL, "wall_ms": wall,
            "cached": False, "returncode": proc.returncode}
