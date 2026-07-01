---
name: sdg-alignment-mapper
description: Maps an NGO or development program's activities, target group, and intended outcomes to relevant UN Sustainable Development Goals (SDGs), targets, and global indicators. Works for any country by default; loads a national-context reference file (e.g., Malaysia/MySDG) when the specified country has one, adding localized indicator status and sub-national detail. Use when a user asks to map a project to the SDGs, show SDG alignment, identify which SDG targets a program contributes to, or needs an SDG crosswalk table for a grant proposal, M&E framework, or donor report.
version: 0.1.0
license: CC-BY-SA-4.0
---

# SDG Alignment Mapper

## Purpose

Produce a defensible mapping table showing which UN SDG goals, targets, and indicators a program's activities and outcomes contribute to. Treat the output as a starting point for an M&E specialist or grant writer to review — not a final classification. Always say so explicitly in the output.

This skill is country-agnostic by default: it maps against the UN Global Indicator Framework regardless of where the program operates. A national-context layer is optional and only activates when a matching reference file exists in `references/`.

## Required input

Collect, or extract from what the user already provided:

- Program/project description
- Key activities
- Target group / beneficiaries
- Intended outcomes or results
- Country of implementation (optional — if omitted, map against global indicators only)

If activities or outcomes are too vague to map with confidence, ask one clarifying question before mapping. Do not guess at a program's scope.

## Process

1. Identify candidate SDG goals (1–17) based on the activities and outcomes described.
2. For each candidate goal, identify the specific numbered target(s) (e.g., 4.4, 8.6) the activity plausibly contributes to. Only include a target when there's a clear, explainable causal link between the activity/outcome and the target — do not force a mapping onto every goal just to show breadth.
3. Identify the official global indicator(s) tied to each target (e.g., indicator 4.4.1), using the UN Global Indicator Framework.
4. Check whether a national-context reference file exists for the specified country in `references/`:
   - If yes, load it. Add the corresponding national indicator (if one exists), an availability status, and any sub-national (state/district) indicator the reference notes.
   - If no reference file exists for the country, state this plainly in the output: "No localized indicator layer available for [country] in this library yet — mapping shown against global indicators only." Do not fabricate a national indicator.
5. Write a one-sentence justification for each row, connecting the specific activity or outcome to the target.
6. Mark any weak or speculative mapping as "weak link" rather than presenting it with the same confidence as a strong match. Do not omit it silently — flagging is more useful than hiding uncertainty.

## Output format

A table with these columns: SDG Goal | Target | Global Indicator | National Indicator (if applicable) | Status | Justification.

Follow the table with a short "Known limitations" note covering:
- This mapping has not been reviewed by an M&E specialist and should be checked before use in a funding proposal or formal report.
- When a national context file was used, note that its indicator coverage may be incomplete (point to the specific gaps documented in that reference file, not a generic disclaimer).

## National context files

Available in `references/`:

- `malaysia.md` — Malaysia/MySDG framework notes: DOSM indicator availability categories, how Malaysia's contextualised national targets differ from the UN's universal targets, and the state/district reporting layer. This is a **seed reference**, not a complete indicator-by-indicator crosswalk. When this file is used, tell the user it needs to be expanded with verified data from the latest DOSM "Sustainable Development Goals (SDG) Indicators, Malaysia" report before being relied on for formal MySDG or donor reporting.

To add another country: create `references/<country>.md` following the same structure (indicator availability categories, national-vs-global target differences, any sub-national layer), then add it to this list.
