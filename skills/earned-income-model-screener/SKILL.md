---
name: earned-income-model-screener
description: Screens and classifies earned-income and social-enterprise ideas for an NGO, cooperative, or social enterprise using Kim Alter's Social Enterprise Typology and the Matrix Map (mission impact vs. financial profitability). Produces a per-idea classification (Embedded/Integrated/External/Complex), a Matrix Map placement (Star/Heart/Money Tree/Stop Sign), and a viability recommendation. Use when a user asks to evaluate an earned-income idea, screen a social-enterprise concept, decide whether a revenue idea fits the mission, prioritize between multiple potential income-generating activities, or needs this for a business plan, grant proposal, or board discussion.
version: 0.1.0
license: CC-BY-SA-4.0
evidence_strength: established-standard
evidence_sources:
  - "Alter, K. (2007). Social Enterprise Typology (updated Nov 27, 2007). Virtue Ventures LLC. https://www.4lenses.org/setypology"
  - "Bell, J., Masaoka, J., & Zimmerman, S. (2010). Nonprofit Sustainability: Making Strategic Decisions for Financial Viability. Jossey-Bass. (Matrix Map framework)"
  - "Zimmerman, S., & Bell, J. (2014). The Sustainability Mindset: Using the Matrix Map to Make Strategic Decisions. Jossey-Bass."
topics:
  - earned-income
official: true
last_reviewed: 2026-07-02
---

# Earned-Income & Social-Enterprise Model Screener

## Purpose

Help an NGO, cooperative, or social enterprise decide whether a candidate earned-income idea is worth pursuing further — before time is spent building a full financial model. Combines two established frameworks: Alter's Social Enterprise Typology, which classifies how tightly a revenue activity is tied to the mission, and the Matrix Map, which plots each idea by mission impact and financial profitability to surface a strategic recommendation. Treat the output as a structured starting point for leadership or board discussion, not a final investment decision.

## Required input

Collect, or extract from what the user already provided:

- Organization's mission/purpose (one or two sentences)
- One or more candidate earned-income ideas (paid services, products, membership fees, asset rental, consulting, training, etc.)
- For each idea, whatever is known about: who would pay, how closely programs and the idea would share staff/assets/beneficiaries, and any early sense of cost versus revenue
- Existing programs/activities, if the user wants to compare a new idea against the current portfolio (optional)

If a candidate idea is described in one line with no detail on delivery or customer, ask one clarifying question (e.g., "who exactly would pay for this, and would they be the same people you currently serve?") before classifying it — the typology depends on that relationship.

## Process

1. For each candidate idea, determine its relationship to the mission and programs using Alter's typology:
   - **Embedded** — the enterprise activity and the social program are the same activity; beneficiaries are producers or customers (e.g., a vocational-training program that sells what trainees make).
   - **Integrated** — the enterprise overlaps with programs and shares costs, assets, or staff, but is not identical to the program (e.g., a clinic that also treats paying patients alongside subsidized ones).
   - **External** — the enterprise is a separate, largely unrelated income-generating activity that funds the mission but doesn't itself deliver the mission (e.g., a thrift shop run to fund an unrelated youth programme).
   - **Complex** — genuinely combines two or more of the above; don't force a single label onto an idea that legitimately spans categories.
2. For each idea, estimate two independent scores (High / Medium / Low), each with one sentence of reasoning:
   - **Mission impact** — how directly the activity itself advances the organization's mission (not just the money it generates).
   - **Financial profitability** — how likely the activity is to cover its own costs and generate a surplus, based on what's known about pricing, demand, and cost.
3. Plot each idea on the Matrix Map using the two scores and assign the resulting quadrant:
   - **Star** (high impact, high profitability) — invest and grow.
   - **Heart** (high impact, low profitability) — worth subsidizing deliberately if funding allows, but name the subsidy required rather than treating it as self-sustaining.
   - **Money Tree** (low impact, high profitability) — a legitimate revenue source, but be explicit that its value is financial, not mission-advancing — do not oversell it in an impact report.
   - **Stop Sign** (low impact, low profitability) — flag for discontinuation or major redesign; don't recommend pursuing it without naming what would need to change first.
4. Do not let a compelling founder story inflate a Stop Sign into a Heart. If the profitability or impact estimate rests on optimistic assumptions rather than evidence, say so explicitly rather than smoothing the score to be agreeable.
5. When multiple ideas are screened together, rank them and recommend which one or two to pursue first — prioritizing Stars, then a deliberate Heart choice only if mission urgency clearly justifies the subsidy — not by number of ideas proposed or founder enthusiasm.

## Output format

A table with columns: Idea | Typology (Embedded/Integrated/External/Complex) | Mission Impact | Profitability | Matrix Quadrant | Recommendation.

Follow the table with:

- A short paragraph naming which idea(s) to pursue first and why.
- A "Known limitations" note covering: this screening uses estimates, not verified costs or market data — before committing resources, pricing/costing/break-even and cash-flow work (a natural next step, typically built in a spreadsheet) should confirm the profitability estimate used here. Mission-impact scoring is a qualitative judgment call and should be sense-checked with staff or beneficiaries close to the programme, not decided by one person alone.

## Optional chaining with other skills

If the user has also built a logframe or Theory of Change for the organization's core programs (e.g. with the `logframe-toc-builder` skill in this library), use its outcome statements to sharpen the mission-impact reasoning for `Embedded` and `Integrated` ideas — an activity that advances a stated outcome should score higher than one that merely resembles programme work. This skill also pairs naturally with `funding-mix-diversification-planner`: a Star or Heart idea identified here becomes a candidate earned-income line in that skill's funding-mix analysis. Neither skill requires the other to run standalone.
