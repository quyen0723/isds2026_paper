"""Algorithm-explanation prompts at the three CLEAR levels."""

from __future__ import annotations

from .prompts_rcifeni import l1, l2, l3

ROLE = "CS tutor. Undergraduate IT audience."


def build(level: str, sig: str) -> str:
    if level == "basic":
        return l1(f"Explain this:\n\n{sig}")
    if level == "intermediate":
        return l2(
            ROLE,
            "1. Read the signature + docstring.\n"
            "2. Explain the algorithm concisely.\n"
            "3. List the steps in order.",
            sig,
        )
    return l3(
        role=ROLE,
        context=(
            "Why: an IT undergraduate is learning this algorithm.\n"
            "Where: a 100-level data-structures course.\n"
            "Who: reader knows Python but not advanced CS theory.\n"
            "How: the explanation will be read once, without the code open."
        ),
        steps=(
            "1. Restate the problem in plain English.\n"
            "2. Outline the high-level approach.\n"
            "3. Walk through the key invariants or data flow.\n"
            "4. State when this approach is preferred over alternatives.\n"
            "5. Close with a one-sentence self-check."
        ),
        fmt=(
            "Prose. Four short paragraphs matching steps 1-4, "
            "then one italic self-check sentence."
        ),
        notices=(
            "- Avoid code blocks; use plain English.\n"
            "- Keep vocabulary at undergraduate level.\n"
            "- No more than 220 words total."
        ),
        okr=(
            "O: Explanation lets a student solve a similar problem unaided.\n"
            "KR1: Each of steps 1-4 is answered in one paragraph.\n"
            "KR2: A final self-check sentence is present."
        ),
        sig=sig,
    )
