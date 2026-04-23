"""Algorithm-explanation prompts at the three CLEAR levels.

L3 embeds both a Gherkin acceptance contract and a formal specification
(PRE/INV/POST/ERR) so that the reader's acceptance criterion is
behaviourally explicit, not prose-only.
"""

from __future__ import annotations

from .prompts_rcifeni import l1, l2, l3

ROLE = "CS tutor. Undergraduate IT audience."

GHERKIN = (
    "Feature: Produce a pedagogically-sound algorithm explanation.\n\n"
    "  Scenario: Cold-read comprehension\n"
    "    Given a learner who has read only the function signature and docstring\n"
    "    When the learner reads the explanation once, without the source code\n"
    "    Then the learner can restate the problem, the high-level approach,\n"
    "         and at least one key invariant in their own words\n\n"
    "  Scenario: Scope compliance\n"
    "    Given the produced explanation text\n"
    "    When reviewed against the 4 required steps\n"
    "    Then all 4 steps are addressed\n"
    "     And a single-sentence italic self-check closes the response"
)

FORMAL_SPEC = (
    "PRE:\n"
    "  - P1: Input is a Python function signature + docstring.\n"
    "  - P2: Reader level := undergraduate (IT major).\n\n"
    "INV:\n"
    "  - I1: Output language := plain English prose.\n"
    "  - I2: Code blocks ∉ output.\n"
    "  - I3: Word count ≤ 220.\n"
    "  - I4: Vocabulary ⊆ undergraduate CS lexicon.\n\n"
    "POST:\n"
    "  - Q1: 4 numbered paragraphs exist (one per instruction step 1-4).\n"
    "  - Q2: Exactly 1 italic self-check sentence closes the response.\n\n"
    "ERR:\n"
    "  - E1: Code block detected ⇒ rewrite as prose.\n"
    "  - E2: Self-check missing ⇒ append one sentence.\n"
    "  - E3: Word count > 220 ⇒ compress steps 1-4."
)


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
            "KR2: A final italic self-check sentence is present."
        ),
        sig=sig,
        gherkin=GHERKIN,
        formal_spec=FORMAL_SPEC,
    )
