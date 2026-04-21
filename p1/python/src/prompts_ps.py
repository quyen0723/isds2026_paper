"""Problem-solving prompts at the three CLEAR levels.

L3 embeds a Gherkin Given/When/Then block per
``.fong/instructions/instructions-rcifeni-o-gherkin-prompt-engineer.md``
— code/app-dev flows get behavioural acceptance contracts instead of
prose-only instructions.
"""

from __future__ import annotations

from .prompts_rcifeni import l1, l2, l3

ROLE = "Senior Python engineer. Mentoring an IT undergraduate."

GHERKIN = (
    "Feature: Implement the function described in the signature.\n\n"
    "  Scenario: Typical input\n"
    "    Given the function is called with arguments that match the docstring\n"
    "    When the implementation runs\n"
    "    Then it returns the value specified by the docstring\n"
    "     And no exception is raised\n\n"
    "  Scenario: Edge input\n"
    "    Given arguments at the documented boundaries (empty, negative, None)\n"
    "    When the implementation runs\n"
    "    Then it returns the boundary result the docstring implies\n"
    "     And it does not silently coerce types"
)


def build(level: str, sig: str) -> str:
    if level == "basic":
        return l1(f"Solve:\n\n{sig}")
    if level == "intermediate":
        return l2(
            ROLE,
            "1. Read the function signature + docstring.\n"
            "2. Write an implementation.\n"
            "3. Return only the function body. No prose.",
            sig,
        )
    return l3(
        role=ROLE,
        context=(
            "Why: demonstrate idiomatic Python for a learner.\n"
            "Where: introductory Python course; no external packages allowed.\n"
            "Who: reader knows stdlib only; will run the code in CPython 3.11+.\n"
            "How: code will be read, then executed against hidden tests."
        ),
        steps=(
            "1. Read the Gherkin scenarios below as the acceptance contract.\n"
            "2. Implement the function so both scenarios pass.\n"
            "3. Prefer Pythonic constructs; use only the standard library.\n"
            "4. Target the best complexity you can justify in a comment.\n"
            "5. Finish with a comment listing the edge cases you handled."
        ),
        fmt=(
            "A single Python code block.\n"
            "First line: one-line docstring summary.\n"
            "Last lines: # Complexity: ... and # Edge cases: ..."
        ),
        notices=(
            "- Do not import third-party packages.\n"
            "- Do not rewrite the signature or the docstring.\n"
            "- Keep the body self-contained and deterministic."
        ),
        okr=(
            "O: A correct, idiomatic implementation that satisfies both scenarios.\n"
            "KR1: Both Gherkin scenarios pass on the documented inputs.\n"
            "KR2: Complexity comment names both time and space.\n"
            "KR3: Edge-cases comment names at least two handled cases."
        ),
        sig=sig,
        gherkin=GHERKIN,
    )
