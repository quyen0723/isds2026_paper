# Pilot Prompts — CLEAR Levels × RCIFENI-O

Nine templates (3 CLEAR-grounded levels × 3 pedagogical framings), each
an RCIFENI-O prompt per
`.fong/instructions/instructions-rcifeni-o-prompt-engineering.md`
(and `…-gherkin-prompt-engineer.md` for the code-producing L3 in
problem-solving).

Placeholder `{signature}` is the HumanEval `prompt` field (function
signature + docstring). Source of truth: `p1/python/src/prompts_*.py`.

**CLEAR → RCIFENI-O completeness mapping.**

| CLEAR level | Criteria satisfied | RCIFENI-O sections included |
|---|---|---|
| L1 basic | 0–1 | Input only (no structure) |
| L2 intermediate | 2–3 | Role + Instructions + Input |
| L3 advanced | 4–5 | Role + Context + Instructions + Format + Notices + OKR + Input (+ Gherkin for code) |

RCIFENI-O legend: **R**ole, **C**ontext, **I**nstructions, **F**ormat,
**E**xample (optional), **N**otices, **I**nput, **O**KR.

---

## Task 1 — Algorithm Explanation

### L1 basic
```
Explain this:

{signature}
```

### L2 intermediate
```
# 1. Role:
CS tutor. Undergraduate IT audience.

# 3. Instructions:
1. Read the signature + docstring.
2. Explain the algorithm concisely.
3. List the steps in order.

<<< INPUT:
{signature}
```

### L3 advanced (full RCIFENI-O)
```
# 1. Role:
CS tutor. Undergraduate IT audience.

# 2. Context (5W1H):
Why: an IT undergraduate is learning this algorithm.
Where: a 100-level data-structures course.
Who: reader knows Python but not advanced CS theory.
How: the explanation will be read once, without the code open.

# 3. Instructions:
1. Restate the problem in plain English.
2. Outline the high-level approach.
3. Walk through the key invariants or data flow.
4. State when this approach is preferred over alternatives.
5. Close with a one-sentence self-check.

# 4. Format:
Prose. Four short paragraphs matching steps 1-4, then one italic
self-check sentence.

# 6. Notices/Cautions:
- Avoid code blocks; use plain English.
- Keep vocabulary at undergraduate level.
- No more than 220 words total.

# 7. OKRs (O+KRs):
O: Explanation lets a student solve a similar problem unaided.
KR1: Each of steps 1-4 is answered in one paragraph.
KR2: A final self-check sentence is present.

<<< INPUT:
{signature}
```

---

## Task 2 — Complexity Analysis

### L1 basic
```
What is the complexity of this?

{signature}
```

### L2 intermediate
```
# 1. Role:
Computer-scientist. Complexity-analysis specialist.

# 3. Instructions:
1. Count loops and recursive calls.
2. State time and space complexity as Big-O.

<<< INPUT:
{signature}
```

### L3 advanced (full RCIFENI-O)
```
# 1. Role:
Computer-scientist. Complexity-analysis specialist.

# 2. Context (5W1H):
Why: an IT undergraduate must derive, not recall, Big-O.
Where: algorithms course, week on asymptotic analysis.
Who: reader has seen recurrences but not the master theorem.
How: the analysis will be graded for reasoning, not just the answer.

# 3. Instructions:
1. Identify loops and recursions.
2. Count operations symbolically.
3. Derive worst-case time T(n) and auxiliary space S(n).
4. Decide whether the bound is asymptotically optimal.
5. Close with a one-sentence transfer self-check.

# 4. Format:
Five numbered paragraphs answering steps 1-5.
Final line: T(n) = O(...)  S(n) = O(...).

# 6. Notices/Cautions:
- Use n for the primary input size; introduce new symbols explicitly.
- Do not guess; if a bound is unclear, state the tighter + looser options.

# 7. OKRs (O+KRs):
O: Reader can reproduce the derivation on a similar problem.
KR1: T(n) and S(n) stated in the final line.
KR2: Optimality claim justified in step 4.
KR3: Self-check sentence present in step 5.

<<< INPUT:
{signature}
```

---

## Task 3 — Problem Solving (RCIFENI-O + Gherkin for L3)

### L1 basic
```
Solve:

{signature}
```

### L2 intermediate
```
# 1. Role:
Senior Python engineer. Mentoring an IT undergraduate.

# 3. Instructions:
1. Read the function signature + docstring.
2. Write an implementation.
3. Return only the function body. No prose.

<<< INPUT:
{signature}
```

### L3 advanced (full RCIFENI-O + Gherkin)
```
# 1. Role:
Senior Python engineer. Mentoring an IT undergraduate.

# 2. Context (5W1H):
Why: demonstrate idiomatic Python for a learner.
Where: introductory Python course; no external packages allowed.
Who: reader knows stdlib only; will run the code in CPython 3.11+.
How: code will be read, then executed against hidden tests.

# 3. Instructions:
1. Read the Gherkin scenarios below as the acceptance contract.
2. Implement the function so both scenarios pass.
3. Prefer Pythonic constructs; use only the standard library.
4. Target the best complexity you can justify in a comment.
5. Finish with a comment listing the edge cases you handled.

# 4. Format:
A single Python code block.
First line: one-line docstring summary.
Last lines: # Complexity: ... and # Edge cases: ...

# 6. Notices/Cautions:
- Do not import third-party packages.
- Do not rewrite the signature or the docstring.
- Keep the body self-contained and deterministic.

# 7. OKRs (O+KRs):
O: A correct, idiomatic implementation that satisfies both scenarios.
KR1: Both Gherkin scenarios pass on the documented inputs.
KR2: Complexity comment names both time and space.
KR3: Edge-cases comment names at least two handled cases.

<<< INPUT:
{signature}

# 7.1 Behaviour (Gherkin):
Feature: Implement the function described in the signature.

  Scenario: Typical input
    Given the function is called with arguments that match the docstring
    When the implementation runs
    Then it returns the value specified by the docstring
     And no exception is raised

  Scenario: Edge input
    Given arguments at the documented boundaries (empty, negative, None)
    When the implementation runs
    Then it returns the boundary result the docstring implies
     And it does not silently coerce types
```

---

## AIOQ-R Judge Prompt

```
You are an academic rater for AI output quality in a CS learning context.
Score the RESPONSE on five dimensions (integer 1-5 each, where
1=poor, 5=excellent):

- accuracy: technical correctness of the content.
- completeness: coverage of what the task asks for.
- relevance: alignment with the learner's level and the task intent.
- clarity: logical structure, readable formatting.
- learning_value: stimulates Bloom higher-order thinking; explains
  *why*, not just *what*.

TASK (the user prompt that was sent to the assistant):
<<<TASK
{task_text}
TASK

RESPONSE (the assistant's reply being rated):
<<<RESPONSE
{response_text}
RESPONSE

Return ONE JSON object on a single line and nothing else. Do not use
code fences. Keys MUST be exactly: accuracy, completeness, relevance,
clarity, learning_value, rationale. Keep rationale short (<=200 chars)
and DO NOT include code or backslashes in it.
```

Composite score = sum of five dimensions, range 5–25 (the paper's
AIOQ-R composite scale).
