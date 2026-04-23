"""Complexity-analysis prompts at the three CLEAR levels.

L3 embeds both a Gherkin acceptance contract and a formal specification
(PRE/INV/POST/ERR) for the derivation quality, not just the final Big-O.
"""

from __future__ import annotations

from .prompts_rcifeni import l1, l2, l3

ROLE = "Computer-scientist. Complexity-analysis specialist."

GHERKIN = (
    "Feature: Derive worst-case time and space complexity with reasoning.\n\n"
    "  Scenario: Reasoning transfer\n"
    "    Given a student who has seen recurrences but not the master theorem\n"
    "    When the student reads the analysis\n"
    "    Then the student can reproduce the derivation on a similar problem\n"
    "     And can point to the operation count that drives the bound\n\n"
    "  Scenario: Reported bounds are explicit\n"
    "    Given the produced analysis\n"
    "    When inspected for the final line\n"
    "    Then T(n) and S(n) are both stated as Big-O expressions\n"
    "     And each is accompanied by a justification earlier in the analysis"
)

FORMAL_SPEC = (
    "PRE:\n"
    "  - P1: Input is a Python function signature + docstring.\n"
    "  - P2: n denotes the primary input size.\n\n"
    "INV:\n"
    "  - I1: All new symbols (besides n) are introduced before first use.\n"
    "  - I2: If a bound is ambiguous, a tighter AND a looser bound are named.\n"
    "  - I3: Unsupported claims ∉ output.\n\n"
    "POST:\n"
    "  - Q1: 5 numbered paragraphs answer instruction steps 1-5.\n"
    "  - Q2: Final line has shape 'T(n) = O(...)  S(n) = O(...)'.\n"
    "  - Q3: Step 4 contains an explicit optimality verdict with reasoning.\n\n"
    "ERR:\n"
    "  - E1: Missing T(n) or S(n) on the final line ⇒ append.\n"
    "  - E2: Guessed bound without derivation ⇒ add symbolic counting step.\n"
    "  - E3: Self-check sentence missing in step 5 ⇒ add one sentence."
)


def build(level: str, sig: str) -> str:
    if level == "basic":
        return l1(f"What is the complexity of this?\n\n{sig}")
    if level == "intermediate":
        return l2(
            ROLE,
            "1. Count loops and recursive calls.\n"
            "2. State time and space complexity as Big-O.",
            sig,
        )
    return l3(
        role=ROLE,
        context=(
            "Why: an IT undergraduate must derive, not recall, Big-O.\n"
            "Where: algorithms course, week on asymptotic analysis.\n"
            "Who: reader has seen recurrences but not the master theorem.\n"
            "How: the analysis will be graded for reasoning, not just the answer."
        ),
        steps=(
            "1. Identify loops and recursions.\n"
            "2. Count operations symbolically.\n"
            "3. Derive worst-case time T(n) and auxiliary space S(n).\n"
            "4. Decide whether the bound is asymptotically optimal.\n"
            "5. Close with a one-sentence transfer self-check."
        ),
        fmt=(
            "Five numbered paragraphs answering steps 1-5.\n"
            "Final line: T(n) = O(...)  S(n) = O(...)."
        ),
        notices=(
            "- Use n for the primary input size; introduce new symbols explicitly.\n"
            "- Do not guess; if a bound is unclear, state the tighter + looser options."
        ),
        okr=(
            "O: Reader can reproduce the derivation on a similar problem.\n"
            "KR1: T(n) and S(n) stated in the final line.\n"
            "KR2: Optimality claim justified in step 4.\n"
            "KR3: Self-check sentence present in step 5."
        ),
        sig=sig,
        gherkin=GHERKIN,
        formal_spec=FORMAL_SPEC,
    )
