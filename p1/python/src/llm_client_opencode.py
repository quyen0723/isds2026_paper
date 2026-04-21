"""Subprocess client that relays a structured prompt via
``.fong/tools/zai-rcifeni-o-relay.sh``. Backend is OpenCode CLI bound
to GLM 5.1 (see memory ``lessons-opencode-relay-backend.md``).

The script enforces a strict RCIFENI-O six-field interface, so this
module splits the prompt-builder blob back into sections before
calling the shell. A cooldown (``COOLDOWN_S``, default 2 s)
serialises calls well inside any provider rate-limit window.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from typing import Any

RELAY = "/home/fong/Projects/Quyen-isds2026_paper/.fong/tools/zai-rcifeni-o-relay.sh"
COOLDOWN_S = 2.0
TIMEOUT_S = 180
_LAST_CALL = [0.0]

_SECTION = re.compile(
    r"^#\s*(?P<num>\d+(?:\.\d+)?)\.?\s*(?P<name>[^:\n]+):\s*\n(?P<body>.*?)(?=^#\s*\d+\.?|<<<\s*INPUT|$)",
    flags=re.DOTALL | re.MULTILINE,
)


def _split(blob: str) -> dict[str, str]:
    out = {m.group("name").strip().lower(): m.group("body").strip()
           for m in _SECTION.finditer(blob)}
    if "<<< INPUT:" in blob:
        tail = blob.split("<<< INPUT:", 1)[1].strip()
        out["input"] = re.split(r"^#\s*\d+\.\d+", tail, maxsplit=1,
                                flags=re.MULTILINE)[0].strip()
    return out


def _throttle() -> None:
    wait = COOLDOWN_S - (time.time() - _LAST_CALL[0])
    if wait > 0:
        time.sleep(wait)
    _LAST_CALL[0] = time.time()


def ask(prompt_blob: str) -> dict[str, Any]:
    _throttle()
    p = _split(prompt_blob)
    role = p.get("role") or "domain expert"
    context = p.get("context (5w1h)") or p.get("context") or "see input"
    steps = p.get("instructions") or "answer the input"
    fmt = p.get("format") or "plain text, concise"
    notices = p.get("cautions") or p.get("notices/cautions") or "be accurate"
    okr = p.get("okrs (o+krs)") or p.get("okrs") or "O: correct response."
    sig = p.get("input") or prompt_blob
    with open("/tmp/opencode_input.txt", "w", encoding="utf-8") as fh:
        fh.write(sig)
    cmd = [RELAY,
           "-r", role, "-c", context, "-i", steps, "-f", fmt,
           "-n", notices, "-o", okr, "-F", "/tmp/opencode_input.txt"]
    start = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
    wall = int((time.time() - start) * 1000)
    out = proc.stdout.strip()
    m = re.search(r"\{.*?\"response\"\s*:\s*\"(.*?)\"\s*\}", out, flags=re.DOTALL)
    if m:
        text = m.group(1).encode("utf-8").decode("unicode_escape", errors="replace")
    else:
        jm = re.search(r"\{.*\}", out, flags=re.DOTALL)
        try:
            text = json.loads(jm.group(0)).get("response", out) if jm else out
        except json.JSONDecodeError:
            text = out or proc.stderr
    rate_limited = "rate_limit" in (proc.stdout + proc.stderr).lower()
    return {"text": text, "model": "opencode/glm-5.1", "wall_ms": wall,
            "cached": False, "rate_limited": rate_limited,
            "returncode": proc.returncode}
