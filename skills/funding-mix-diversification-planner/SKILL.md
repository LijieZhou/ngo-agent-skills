---
name: funding-mix-diversification-planner
description: Analyzes an NGO's current funding mix and recommends how to diversify it — including toward earned income — using the "Ten Nonprofit Funding Models" framework (Foster, Kim & Christiansen, Bridgespan/Stanford Social Innovation Review, 2009). Classifies the organization's closest-fit funding model archetype(s) by funding source, decision-maker type, and motivation, flags single-source dependency risk, and suggests realistic next funding sources to pursue. Use when a user asks to diversify funding, reduce grant or donor dependency, plan a funding strategy, assess funding concentration risk, or build a funding-mix section for a business plan, sustainability plan, or board strategy discussion.
version: 0.1.0
license: CC-BY-SA-4.0
evidence_strength: established-standard
evidence_sources:
  - "Foster, W., Kim, P., & Christiansen, B. (2009). Ten Nonprofit Funding Models. Stanford Social Innovation Review, Spring 2009. (Research: Bridgespan Group analysis of 144 nonprofits reaching $50M+ annual revenue since 1970.)"
  - "Bridgespan Group (2011). Finding Your Funding Model: A Practical Approach."
topics:
  - funding-strategy
official: true
last_reviewed: 2026-07-02
---

# Funding-Mix Diversification Planner

## Purpose

Give an organization a structured read on its current funding concentration and a realistic path to diversify — including where earned income fits alongside grants and donations. Built on Bridgespan's research-derived "Ten Nonprofit Funding Models," which found that nonprofits that scaled sustainably did so by matching their programs to funding markets with compatible decision-makers and motivations, rather than by chasing every available source. Treat the output as a strategy discussion starter, not a fundraising plan ready to execute.

## Required input

Collect, or extract from what the user already provided:

- Organization's mission and who it serves
- Current funding sources and, if known, the rough share each contributes (e.g., "70% one foundation, 20% government grant, 10% small individual donations")
- Any earned-income ideas already identified (optional — e.g., from the `earned-income-model-screener` skill in this library)
- Appetite or constraints: is the organization open to government funding, corporate partnerships, individual giving, membership fees, and so on, or are any of these off-limits for legal, political, or capacity reasons?

If current funding shares are unknown, ask the user for a rough percentage breakdown rather than proceeding on a guess — concentration risk is the central thing this skill assesses, and it can't be assessed without at least an approximate mix.

## Process

1. Identify which of the ten funding model archetypes the organization's current primary funding source(s) most resemble, based on the source of funds, the type of decision-maker, and their motivation. The ten archetypes (Foster, Kim & Christiansen, 2009) are: Heartfelt Connector, Beneficiary Builder, Member Motivator, Big Bettor, Public Provider, Policy Innovator, Beneficiary Broker, Resource Recycler, Market Maker, and Local Nationalizer. Briefly name which archetype(s) fit and which do not, rather than forcing every organization into exactly one box — some legitimately blend two.
2. Flag concentration risk explicitly: if any single source is estimated at 50% or more of total funding, name it as a dependency risk regardless of how stable that source currently feels.
3. Assess fit between the program model and 2-3 realistic additional funding archetypes the organization could plausibly pursue next, given its beneficiaries, decision-maker access, and capacity — not an exhaustive list of all ten. For each, state: which archetype it is, why the program is a plausible match, and one concrete first step.
4. If earned-income ideas have already been screened (e.g., Star or Heart ideas from `earned-income-model-screener`), map them explicitly onto the archetype they'd represent (often Member Motivator, Resource Recycler, or Market Maker) so the earned-income work is shown as one lever within the broader funding-mix strategy, not a separate initiative.
5. Do not recommend pursuing a funding archetype that conflicts with a stated constraint (e.g., recommending government funding to an organization that stated political constraints rule it out). If a strong-fitting archetype is off-limits, say so and move to the next-best fit rather than silently dropping the constraint.
6. Close with a target funding mix framed as a direction, not a fixed percentage promise — e.g., "reduce single-foundation share from ~70% toward 40-50% over 2-3 years by adding X and Y" — and name the biggest assumption that target depends on.

## Output format

1. A short paragraph naming the current archetype(s) and the concentration-risk flag if applicable.
2. A table with columns: Candidate Funding Archetype | Why It Fits | First Step | Constraint Check.
3. A closing paragraph with the directional target mix and its biggest assumption.
4. A "Known limitations" note covering: this framework was derived from large (mostly US-based, $50M+ revenue) nonprofits, so its archetypes may fit a small or early-stage organization loosely rather than precisely — use it to structure the conversation, not as a checklist to satisfy exactly. Funding-source percentages given by the user are estimates unless drawn from actual financial records, and should be confirmed against real figures before being used in a funder-facing document.

## Optional chaining with other skills

Pairs naturally with `earned-income-model-screener` — screen ideas there first, then bring the Star/Heart results into this skill to see how they fit the wider funding-mix picture. Neither skill requires the other to run standalone.
