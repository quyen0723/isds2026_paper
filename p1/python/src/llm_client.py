"""Thin HTTP client for the GPT-4o-mini relay at http://127.0.0.1:2812/api/ask.

Retries + timeout + JSONL logging. Cache is server-side (30-day file cache),
so identical prompts replay without re-billing.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import urllib.request
import urllib.error

DEFAULT_URL = "http://127.0.0.1:2812/api/ask"
DEFAULT_TIMEOUT = 60
DEFAULT_RETRIES = 3


def ask(prompt: str, url: str = DEFAULT_URL, timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES) -> dict[str, Any]:
    body = json.dumps({"prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            start = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            payload.setdefault("wall_ms", int((time.time() - start) * 1000))
            payload["attempt"] = attempt
            return payload
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = e
            time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(f"relay failed after {retries} attempts: {last_err}")


def log_call(log_path: str | Path, record: dict[str, Any]) -> None:
    p = Path(log_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
