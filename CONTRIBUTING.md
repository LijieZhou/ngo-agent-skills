# Contributing

Thanks for considering a contribution to NGO Agent Skills. The bar is intentionally high: every skill should be evidence-grounded, honestly labelled, and useful beyond a single program or funder.

## Inclusion criteria

A skill should:

1. solve a recurring NGO program design, MEL (monitoring, evaluation & learning), or donor-reporting problem;
2. be useful beyond one program, one country, or one funder;
3. cite named evidence sources in its `evidence_sources` frontmatter — an institutional standard, peer-reviewed research, or documented sector guidance;
4. label its evidence tier honestly via `evidence_strength` (see `docs/EVIDENCE.md` for the four tiers) — don't claim `established-standard` for something that's really just our own design choice;
5. preserve program staff and M&E specialist judgement rather than pretending the skill can decide everything — every skill's output should say plainly that it's a draft for review, not a final answer;
6. never fabricate a data source, indicator, or citation it can't back up — if information isn't available, the skill should say so explicitly rather than inventing something plausible-sounding;
7. include clear required-input guidance and a defined output format;
8. avoid frameworks recorded in `docs/EXCLUSIONS.md`, or explain why an exception is justified.

See [`docs/EVIDENCE.md`](docs/EVIDENCE.md) for the evidence canon and tier definitions, and [`docs/EXCLUSIONS.md`](docs/EXCLUSIONS.md) for what's deliberately left out and why.

## Skill structure

Skills live at:

```
skills/<skill-name>/SKILL.md
```

Flat, one level deep only — do not nest a domain folder underneath `skills/`. Cowork's plugin loader only auto-discovers skills at exactly this depth; a nested folder breaks the Claude plugin install even though other Agent Skills tools tolerate it. See `scripts/validate_skills.py` for the automated check.

Every `SKILL.md` must include, in its YAML frontmatter:

- `name` — must match the parent folder name exactly, lowercase kebab-case
- `description` — third-person, specific enough to trigger correctly
- `version`, `license`
- `evidence_strength` — one of the four tiers in `docs/EVIDENCE.md`
- `evidence_sources` — a non-empty list, even for `original-framework` skills (state explicitly that there's no external evidence base)

## Validation before a pull request

Run:

```bash
python3 scripts/validate_skills.py
npx -y skills@latest add . --list
```

The first checks plugin/skill structure, frontmatter completeness, and evidence sourcing. The second confirms the vercel `skills` CLI can actually discover every skill — not just that the static checks pass. Both also run automatically in CI on every push/PR.

## Pull request guidance

In your PR, briefly explain:

- what skill changed and why it's useful;
- what evidence tier it claims and what source backs that claim;
- what validation commands you ran.

Small, well-evidenced additions are better than broad ones that dilute the library. The goal isn't the most skills — it's skills worth trusting.
