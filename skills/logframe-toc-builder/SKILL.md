---
name: logframe-toc-builder
description: Builds a logical framework (logframe) matrix and/or Theory of Change narrative for an NGO or development program from its stated goal and planned activities. Produces impact, outcome, and output levels with indicators, means of verification, and assumptions/risks, plus an optional causal narrative highlighting load-bearing assumptions. Use when a user asks to build a logframe, create a theory of change, design a logical framework, map activities to outcomes and indicators, or needs this for a grant proposal or M&E plan.
version: 0.1.0
license: CC-BY-SA-4.0
evidence_strength: established-standard
evidence_sources:
  - "NORAD. The Logical Framework Approach (LFA): Handbook for Objectives-Oriented Planning, 4th ed., 1999 -- the logframe format required by most bilateral and multilateral donors."
  - "USAID. ADS Chapter 201: Program Cycle Operational Policy -- results frameworks and logframe requirements for USAID-funded programs."
  - "Vogel, I. (2012). Review of the Use of 'Theory of Change' in International Development. UK Department for International Development (DFID)."
  - "Mayne, J. (2015). Useful Theory of Change models. Canadian Journal of Program Evaluation, 30(2), 119-142."
---

# Logframe / Theory of Change Builder

## Purpose

Produce a defensible logframe matrix and/or Theory of Change (ToC) narrative from a program's goal and activities. Treat the output as a draft for an M&E specialist to review before it goes into a proposal or donor report — not a final document. Say so explicitly in the output.

## Required input

Collect, or extract from what the user already provided:

- Program goal (the overarching, long-term change the program is working toward)
- Planned activities
- Target group / beneficiaries
- Available resources/inputs (optional)
- Known constraints or context (optional)
- Preferred output: logframe matrix, ToC narrative, or both (default: both)

If the goal or activities are too vague to build a coherent chain, ask one clarifying question before proceeding. Do not invent activities or outcomes the user didn't describe.

## Process

1. Write a single, clear impact/goal-level statement from what the user provided — the long-term change the program ultimately contributes to.
2. Identify outcome-level statement(s): the medium-term changes in behavior, systems, or conditions that result from the outputs. Keep this to as few outcomes as the program logic actually supports — don't multiply outcomes to look comprehensive.
3. Identify output-level statement(s): the direct products or services the activities deliver.
4. Map each stated activity to the output(s) it produces. If an activity doesn't clearly connect to any output, flag it rather than forcing a connection.
5. For each level (Impact, Outcome, Output), draft:
   - **Indicator(s)** — measurable, and as close to SMART (specific, measurable, achievable, relevant, time-bound) as the input allows.
   - **Means of verification** — a plausible, realistic data source (program records, a specific survey, admin data). Do not invent an oddly specific data source that likely wouldn't exist for this program.
   - **Assumptions/risks** — the condition that must hold for the causal link from this level to the next to work. Mark which assumptions are load-bearing (if false, the chain breaks) versus minor.
6. If a ToC narrative is requested, write it as a connected if-then chain: "If [activities], and [key assumption holds], then [outputs]. If [outputs], and [assumption], then [outcomes]. This contributes to [impact]."
7. Flag any link in the chain that reads as a stretch rather than smoothing over it — a weak causal link is more useful to surface than to hide.

## Output format

Default to both:

1. A logframe table with columns: Level | Statement | Indicator(s) | Means of Verification | Assumptions/Risks.
2. A short ToC narrative paragraph beneath it.
3. A separate short list of load-bearing assumptions pulled out from the table — the ones worth the user double-checking first.

Follow with a "Known limitations" note covering:
- This is a draft for review by someone in an M&E role, and every indicator should be checked against real data availability before being finalized in a proposal or report.
- The logframe format simplifies causality into a linear chain, which critics of rigid results-based management argue can obscure complex, non-linear program dynamics (see `docs/EXCLUSIONS.md`). Treat the assumptions/risks column as the place that complexity should surface, and revisit it as the program evolves rather than treating the logframe as fixed once written.

## Optional chaining with other skills

If the user has also mapped this program's SDGs (e.g. with the `sdg-alignment-mapper` skill in this library), the outcome-level indicators drafted here are often the same measures that get cross-referenced against SDG target indicators. Mention this as a natural next step, but do not require that skill's output to run this one — this skill must work standalone.
