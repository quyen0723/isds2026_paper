# Abstract (p1 — ISDS 2026).

## Title.
The Impact of Prompt Quality on Generative AI Response Quality: A Controlled Experiment with IT Students.

## Authors.
- Ngoc_My_Quyen_Nguyen (FPT University, Ho Chi Minh City, Vietnam).
- Khuong_Ho_Van (HCMUT, Vietnam).
- Thanh_Phong_Lam (Banking University of Ho Chi Minh City, Vietnam).

## Contracts.
- N := 30–40. design := within_subjects × Latin_Square (4 × 4).
- IV := prompt_quality ∈ { basic, intermediate, advanced } (CLEAR-grounded).
- DV := AIOQ_R_composite ∈ [5, 25], 5 dims (accuracy, completeness, relevance, clarity, learning_value).
- moderator := platform ∈ { GPT_4o, Claude_Sonnet }, temperature = 0.7.
- covariate := self_reported_AI_literacy (ANCOVA robustness).

## Abstract (Paper-Ready, ~250 words).

The rapid adoption of generative artificial intelligence (GenAI) tools such as ChatGPT and Claude among university students has raised a critical pedagogical question: does the quality of user-written prompts significantly influence the quality of AI-generated responses? Despite growing evidence that prompt engineering matters, most existing studies examine only a single AI platform, rely on uncontrolled observations, and are situated exclusively in Western educational contexts. This paper presents the design of a controlled within-subjects experiment to quantify the impact of prompt quality on GenAI response efficacy across two competing platforms — ChatGPT (GPT-4o) and Claude Sonnet — in the context of IT students performing academic learning tasks at a Vietnamese university. We operationalize prompt quality into three levels (basic, intermediate, advanced) guided by the CLEAR framework and measure response quality using a proposed five-dimensional AI Output Quality Rubric (AIOQ-R) covering accuracy, completeness, relevance, clarity, and learning value. The experimental design employs a Two-Way Repeated-Measures ANOVA with Latin Square counterbalancing (N = 30–40), complemented by semi-structured interviews analyzed through thematic analysis. We hypothesize that higher prompt quality produces significantly better AI responses (partial η² ≥ 0.06) and that platform-specific differences emerge across task types. This study contributes the first cross-platform controlled experimental design in a Southeast Asian educational setting, a validated assessment rubric, and practical prompt-writing guidelines for IT students.

## Keywords.
prompt engineering, generative AI, response quality, AIOQ-R rubric, higher education, CLEAR framework.

## Preconditions (PRE).
- P1: IRB approval obtained before Phase 2.
- P2: API temperature fixed 0.7 both platforms.
- P3: raters blind to prompt_level.

## Postconditions (POST).
- Q1: composite score + 5 dimensions per session recorded.
- Q2: CVI ≥ 0.80 ∧ κ ≥ 0.70 rubric validation achieved.
- Q3: Joint Display links quant ↔ qualitative.

## Invariants (INV).
- I1: design = expected results; no empirical data claimed in ISDS submission.
- I2: ∀ claim ∈ background: citation ≥ 1.

## Mathematical Spec.
- partial_η² ≥ 0.06 ⇒ medium effect expected.
- N_min := 28 (G*Power, α = 0.05, 1-β = 0.80, f = 0.25).
- α' := 0.01 (Bonferroni-corrected across 5 dims).
