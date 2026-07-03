# NGO Agent Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-1.0-blue)](https://agentskills.io) [![Skills](https://img.shields.io/badge/skills-5-blue)](https://github.com/LijieZhou/ngo-agent-skills) [![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/) [![Last Commit](https://img.shields.io/github/last-commit/LijieZhou/ngo-agent-skills)](https://github.com/LijieZhou/ngo-agent-skills/commits/main)

An open-source library of evidence-based skills for NGO program design, monitoring & evaluation (M&E), and SDG/donor reporting — works in Claude (Cowork, Claude Code) and OpenAI Codex, and follows the open [Agent Skills](https://agentskills.io) standard so it can run anywhere that supports it.

---

## Get Started

Works with Claude and Codex, and any tool that supports the Agent Skills standard.

### Claude

**Cowork (easiest)** — go to **Customize → (+) Add Plugin** and paste:

```
https://github.com/LijieZhou/ngo-agent-skills
```

**Claude Code CLI** — add this repo as a marketplace, then install only the skills you want:

```
claude plugin marketplace add https://github.com/LijieZhou/ngo-agent-skills.git
claude plugin install sdg-alignment-mapper@ngo-agent-skills
claude plugin install logframe-toc-builder@ngo-agent-skills
claude plugin install earned-income-model-screener@ngo-agent-skills
claude plugin install funding-mix-diversification-planner@ngo-agent-skills
claude plugin install oecd-dac-criteria-screener@ngo-agent-skills
```

Each skill is a separate installable plugin, so you can pick just the ones you need — see [Current Skills](#current-skills) below.

### OpenAI Codex

```
npx skills add LijieZhou/ngo-agent-skills -a codex
```

Installs into `.agents/skills/`. Restart Codex after installing.

### Any Agent Skills-compatible tool

Copy the skill folder you need from `skills/` into your agent's skills directory. Each skill is a folder containing `SKILL.md` with name/description frontmatter — no dependencies, no build step.

### Manual (no setup)

1. Open a skill file in the repository (under `skills/`)
2. Copy the prompt block
3. Paste it into any AI and fill in the fields for your program or context

---

## Feedback & Contributions

Found a gap, a stale citation, or want to add a skill? Open a Pull Request or Issue on GitHub — see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the inclusion bar.

---

**I work at an NGO — [start here](#try-it-now).** No setup required. Use the plugin, a local skill install, or manual copy-paste and start using it for your program.

**I'm a developer or AI builder — [start here](#architecture).** YAML schemas, evidence-sourcing fields, and validation scripts live under `scripts/`.

---

## Who This Is For

This library is designed to grow — today it covers SDG alignment, logframe/Theory of Change design, and earned-income/funding-strategy screening, but the aim is to keep expanding into whatever else program officers and project managers need most.

- **Program officers and project managers** who want evidence-grounded support across the program lifecycle — design, SDG alignment, M&E, donor reporting — without hours of manual research
- **M&E (monitoring, evaluation & learning) staff** building reporting frameworks or indicator crosswalks
- **Grant writers** translating program activities into the format a funder requires
- **Training and capacity-building teams** running AI-assisted NGO programs
- **Developers and AI builders** who need a structured, evidence-sourced NGO/development knowledge layer

---

## Why This Exists

AI is arriving in the NGO and development sector fast. Whether it improves program design or just scales confident-sounding, unsourced advice depends on what it's built on.

Most AI tools aimed at NGOs are built on plausible output, not on named evidence or the institutional standards the sector already runs on. This library exists to build something different: skills grounded in frameworks practitioners already trust — the UN SDG Global Indicator Framework, national statistics offices' own indicator data, the logframe format donors require, and the research literature on Theory of Change — and honest about what's still a draft for a person to check, not a finished answer.

---

## Try It Now

**Example:** *"Map this program to the SDGs — we teach basic literacy to out-of-school children in rural Sabah, Malaysia."*

Claude runs the `sdg-alignment-mapper` skill and returns a table of SDG goals, targets, and global indicators the program plausibly contributes to, flags any weak links honestly instead of hiding them, and — because a country was named — adds Malaysia/MySDG-specific indicator status wherever a national reference exists.

**Without the plugin (manual):** open `skills/sdg-alignment-mapper/SKILL.md`, copy the prompt block, and paste it into any AI along with your program description.

---

## What Makes This Different

**Evidence is the filter.** Every skill cites named sourcing — an institutional standard, peer-reviewed research, or documented sector practice. See [`docs/EXCLUSIONS.md`](docs/EXCLUSIONS.md) for frameworks deliberately left out and why.

**Evidence strength is rated transparently.**

| Tier | What it means |
|---|---|
| **Established standard** | A recognized institutional standard the sector already defers to — OECD-DAC criteria, Sphere Standards, UN/DOSM official frameworks, donor-mandated formats like the logframe |
| **Evidence-based** | Peer-reviewed evaluation research showing the approach works |
| **Emerging practice** | Documented sector guidance, used by practitioners, not yet strongly validated |
| **Original framework** | Our own design choice, explicitly labelled as such rather than dressed up as more authoritative than it is |

See [`docs/EVIDENCE.md`](docs/EVIDENCE.md) for the full bibliography behind every skill.

**Every skill says what it doesn't know.** No skill fabricates a data source, indicator, or citation — if information isn't available (e.g., no national indicator layer exists yet for a given country), it says so plainly instead of inventing something plausible-sounding.

**Built for evidence tracking, not just prompts.** Every `SKILL.md` carries a machine-readable header with evidence sourcing, topic tags, and a last-reviewed date — this is a skill library engineered for accountability, not a prompt collection with metadata bolted on.

---

## Current Skills

| Skill | Topic | Evidence tier |
|---|---|---|
| [`sdg-alignment-mapper`](skills/sdg-alignment-mapper/SKILL.md) | SDG Alignment | Established standard |
| [`logframe-toc-builder`](skills/logframe-toc-builder/SKILL.md) | M&E / Program Design | Established standard |
| [`earned-income-model-screener`](skills/earned-income-model-screener/SKILL.md) | Earned Income & Social Enterprise | Established standard |
| [`funding-mix-diversification-planner`](skills/funding-mix-diversification-planner/SKILL.md) | Funding Strategy | Established standard |
| [`oecd-dac-criteria-screener`](skills/oecd-dac-criteria-screener/SKILL.md) | Program Evaluation | Established standard |

`sdg-alignment-mapper` is country-agnostic by default (maps to the UN Global Indicator Framework) and adds optional national-context overlays — Malaysia/MySDG is the first one, in `skills/sdg-alignment-mapper/references/malaysia.md`.

`logframe-toc-builder` builds a logframe matrix and/or Theory of Change narrative — impact/outcome/output levels with indicators, means of verification, and load-bearing assumptions — from a program's goal and activities. Its outcome-level indicators pair naturally with `sdg-alignment-mapper`'s output, though neither skill depends on the other.

`earned-income-model-screener` classifies and scores earned-income/social-enterprise ideas using Kim Alter's Social Enterprise Typology and the Matrix Map (mission impact vs. financial profitability), producing a Star/Heart/Money Tree/Stop Sign recommendation per idea.

`funding-mix-diversification-planner` assesses an organization's current funding concentration and recommends diversification moves using Bridgespan's "Ten Nonprofit Funding Models." It pairs naturally with `earned-income-model-screener` — screened ideas map onto candidate funding archetypes — though neither skill depends on the other.

`oecd-dac-criteria-screener` screens a program's design against the six OECD-DAC evaluation criteria — Relevance, Coherence, Effectiveness, Efficiency, Impact, Sustainability — rating each honestly and naming the evidence gap behind any weak rating, so program staff can see where a design would struggle in a real donor evaluation before it happens. It pairs naturally with `logframe-toc-builder` and `sdg-alignment-mapper`, though it works standalone from a plain program description.

A companion browsable site (Topics / Official / Audits / Docs) is at [`ngo-agent-skills-site`](https://github.com/LijieZhou/ngo-agent-skills-site).

---

## Architecture

### For developers: the YAML schema

Every skill opens with a machine-readable YAML header: `name`, `description`, `version`, `license`, `evidence_strength`, `evidence_sources`, `topics`, `official`, and `last_reviewed`. See any file under `skills/` for the full format.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for inclusion criteria. The bar is intentionally high: every skill must be grounded in named evidence, honestly rated, and practically useful.

### Workflow for adding or revising a skill

After creating or editing a `SKILL.md`, run these before committing:

```bash
python3 scripts/validate_skills.py
python3 scripts/generate_registry.py
npx -y skills@latest add . --list
```

Commit `registry.json` if it changed — CI fails the build if it's out of date.

---

## Credit

Built by [Lijie Zhou](https://www.zhoueesleyfoundation.com/), co-founder of the [Zhou & Eesley Family Foundation](https://www.zhoueesleyfoundation.com/), part of Project Aspirasai 2026 (Malaysia, MySDG).

## Licence

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Open. Forkable. Share alike.
