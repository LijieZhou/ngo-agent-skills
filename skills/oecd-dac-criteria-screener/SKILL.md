---
name: oecd-dac-criteria-screener
description: Screens an NGO or development program's design against the six OECD-DAC evaluation criteria (Relevance, Coherence, Effectiveness, Efficiency, Impact, Sustainability) — the structure nearly every donor evaluation terms of reference is built on. Rates each applicable criterion qualitatively (Strong / Partial / Weak / Insufficient information), names the evidence gap behind any weak rating, and flags which criteria can't yet be meaningfully assessed given the program's stage. Use when a user asks to pre-check a program against OECD-DAC criteria, prepare for a donor evaluation, self-assess relevance/coherence/effectiveness/efficiency/impact/sustainability, or wants an honest read on evaluation-readiness before a proposal or report goes out.
version: 0.1.0
license: CC-BY-SA-4.0
evidence_strength: established-standard
evidence_sources:
  - "OECD/DAC Network on Development Evaluation (2019). Better Criteria for Better Evaluation: Revised Evaluation Criteria Definitions and Principles for Use."
  - "OECD (2021). Applying Evaluation Criteria Thoughtfully. OECD Publishing."
topics:
  - program-evaluation
  - oecd-dac-criteria
official: true
last_reviewed: 2026-07-03
---

# OECD-DAC Evaluation Criteria Screener

## Purpose

Give program staff an honest, pre-emptive read on how a program design would hold up against the six OECD-DAC evaluation criteria — Relevance, Coherence, Effectiveness, Efficiency, Impact, Sustainability — before an actual donor evaluation does it for them. This is not a certified evaluation and cannot substitute for one: a real OECD-DAC evaluation draws on independently collected evidence (surveys, interviews, financial audits, field visits) that this skill does not have access to. Treat the output as a draft self-screen for the program team and M&E specialist to react to, not an evaluation score to hand to a donor.

## Required input

Collect, or extract from what the user already provided:

- Program goal, activities, and target group/beneficiaries (reuse `logframe-toc-builder` output if it exists)
- Program stage: design/proposal, mid-implementation, or completed/ex-post. This matters — Effectiveness, Impact, and Sustainability can only be rated on plausibility for a design-stage program, not on actual achievement
- Any existing M&E data, monitoring reports, or results already observed (optional — absence of this is itself informative, not a blocker)
- Known coordination or overlap with other actors' interventions in the same sector/geography (needed for Coherence)
- Known budget, timeline, or resourcing constraints (needed for Efficiency)
- Whether the user wants all six criteria screened, or only a subset relevant to this evaluation's actual purpose (per OECD's own 2021 guidance, not every evaluation needs equal-depth treatment of all six)

If the program description is too thin to say anything evidence-based about a given criterion, do not invent a rating — mark that criterion as "Insufficient information" and say what's missing.

## Process

1. Establish program stage first — it determines which criteria can be assessed on actual results versus plausibility only. Say this explicitly before rating anything.
2. For each criterion the user wants screened (default: all six, unless the program's stage or stated evaluation purpose makes one clearly inapplicable — see OECD (2021) on adapting criteria rather than mechanically applying all six every time):
   - **Relevance** — do the program's objectives and design respond to the stated needs, policies, and priorities of its beneficiaries and context, and would they still hold if circumstances shifted?
   - **Coherence** — internal coherence (does this program's logic hang together and align with the same organization's other work?) and external coherence (does it complement or duplicate other actors' interventions in the same space?).
   - **Effectiveness** — is the program achieving, or plausibly positioned to achieve, its stated objectives and results, including whether results are likely to differ across subgroups of beneficiaries?
   - **Efficiency** — are resources (funding, time, staff) being used, or planned to be used, in an economical and timely way relative to what's delivered?
   - **Impact** — what higher-level effects, intended or unintended, positive or negative, has the program generated or is it plausibly positioned to generate?
   - **Sustainability** — are the program's net benefits likely to continue after the funding period or external support ends?
3. Rate each assessed criterion qualitatively as Strong / Partial / Weak / Insufficient information — never a numeric score; OECD deliberately does not mandate one, and a manufactured number would overstate precision this skill doesn't have.
4. For every rating below Strong, name the specific evidence gap or design weakness driving it, not a generic caveat.
5. Note real interdependencies only when actually visible in what the user provided (e.g., a Coherence gap already named in step 2 that would plausibly also weaken Effectiveness) — don't manufacture connections that aren't there.
6. Close by naming the 1-3 gaps that would most weaken this program if it faced a real donor evaluation today, ordered by how load-bearing each is.

## Output format

1. A table: Criterion | Assessed? (Yes / Not yet — stage) | Rating | Why | Evidence Gap.
2. A short paragraph on any criteria left unassessed and why (stage-inappropriate or insufficient input).
3. A prioritized list of the top gaps to close before a real evaluation.
4. A "Known limitations" note covering: this is a self-screen using program-reported information, not an independent evaluation — actual OECD-DAC evaluations require evidence this skill cannot collect (field data, beneficiary interviews, financial audits). Ratings are directional and qualitative, not certified scores, and should not be presented to a donor as evaluation results. For a design-stage program, Effectiveness/Impact/Sustainability ratings reflect plausibility only, not demonstrated achievement.

## Optional chaining with other skills

If the program's logframe or Theory of Change has already been built (e.g. with `logframe-toc-builder`), its outcome/impact statements and indicators are useful direct input for the Effectiveness and Impact ratings here. If the program has been mapped to the SDGs (e.g. with `sdg-alignment-mapper`), that mapping can inform the Relevance rating. Neither skill is required — this skill works standalone from a plain program description.
