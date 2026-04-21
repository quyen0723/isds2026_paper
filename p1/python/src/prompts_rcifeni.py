"""RCIFENI-O assembly helpers shared across task-type prompt modules.

Three level assemblers map CLEAR criteria count to prompt completeness:
  _l1 — 0-1 criteria:   bare input only.
  _l2 — 2-3 criteria:   Role + Instructions + Input.
  _l3 — 4-5 criteria:   full RCIFENI-O (+ optional Gherkin).

Ref: ``.fong/instructions/instructions-rcifeni-o-prompt-engineering.md``.
"""

from __future__ import annotations


def l1(body: str) -> str:
    return body.strip()


def l2(role: str, steps: str, sig: str) -> str:
    return (
        "# 1. Role:\n"
        f"{role}\n\n"
        "# 3. Instructions:\n"
        f"{steps}\n\n"
        "<<< INPUT:\n"
        f"{sig.strip()}\n"
    )


def l3(role: str, context: str, steps: str, fmt: str,
       notices: str, okr: str, sig: str, gherkin: str = "") -> str:
    out = [
        "# 1. Role:", role, "",
        "# 2. Context (5W1H):", context, "",
        "# 3. Instructions:", steps, "",
        "# 4. Format:", fmt, "",
        "# 6. Notices/Cautions:", notices, "",
        "# 7. OKRs (O+KRs):", okr, "",
        "<<< INPUT:", sig.strip(),
    ]
    if gherkin:
        out += ["", "# 7.1 Behaviour (Gherkin):", gherkin.strip()]
    return "\n".join(out) + "\n"
