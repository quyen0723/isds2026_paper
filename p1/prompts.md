# Pilot Prompts — CLEAR Levels × Task Framings

Nine prompt templates (3 CLEAR-grounded levels × 3 pedagogical framings).
Source of truth: `p1/python/src/prompt_builder.py` (identical text).
Placeholder `{signature}` is replaced by the HumanEval problem's
function signature + docstring.

CLEAR criteria (Lo, 2023): **C**oncise, **L**ogical, **E**xplicit,
**A**daptive, **R**eflective.

| Level | CLEAR criteria satisfied |
|---|---|
| L1 basic | 0–1 |
| L2 intermediate | 2–3 |
| L3 advanced (full) | 4–5 |

---

## Task 1 — Algorithm Explanation

### L1 basic
```
Explain this:

{signature}
```

### L2 intermediate
```
You are teaching CS. Concisely explain the algorithm for this function.
List the steps in order.

{signature}
```

### L3 advanced
```
As a CS tutor for an IT undergraduate, provide a structured explanation
of the algorithm behind the function below. Follow these steps:
(1) restate the problem in plain English;
(2) outline the high-level approach;
(3) walk through the key invariants or data flow;
(4) state when this approach is preferred over alternatives.
Use concise prose, adapt vocabulary to an undergraduate audience, and
end with a one-sentence self-check:
'Does this explanation help someone solve a similar problem themselves?'

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
Analyze the time and space complexity of this function.
State the Big-O at the end.

{signature}
```

### L3 advanced
```
As a CS tutor, conduct a complexity analysis for the function below.
Follow these steps:
(1) identify loops and recursions;
(2) count operations symbolically;
(3) derive worst-case time T(n) and auxiliary space S(n);
(4) comment on whether this is asymptotically optimal for the problem;
(5) end with a self-check: 'Can a student replicate this analysis on a
    similar problem?'

{signature}
```

---

## Task 3 — Problem Solving

### L1 basic
```
Solve:

{signature}
```

### L2 intermediate
```
Write a Python implementation for the function below.
Return only the function body (no explanation).

{signature}
```

### L3 advanced
```
You are a senior Python engineer mentoring an IT undergraduate.
Write a clean, idiomatic Python implementation for the function below.
Requirements:
(1) include a one-line docstring summary;
(2) use Pythonic constructs where appropriate;
(3) avoid external libraries;
(4) aim for the best complexity you can justify;
(5) end with a brief comment verifying edge cases you considered.

{signature}
```

---

## AIOQ-R Judge Prompt

Same GPT-4o-mini scores the 5 AIOQ-R dimensions on a 1–5 Likert scale:

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
