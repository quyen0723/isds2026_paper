"""Complexity-analysis prompts at the three CLEAR levels."""

from __future__ import annotations

from .prompts_rcifeni import l1, l2, l3

ROLE = "Computer-scientist. Complexity-analysis specialist."


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
    )
