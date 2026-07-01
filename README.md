# NGO Agent Skills

An open, agent-agnostic library of skills for NGO program design, monitoring & evaluation (M&E), and SDG/donor reporting.

Each skill is a self-contained folder under `skills/` containing a `SKILL.md` (instructions + YAML frontmatter) and, where needed, a `references/` folder with supporting detail. This is the [Agent Skills](https://agentskills.io) format — no dependencies, no build step.

Distribution uses two paths that don't conflict:

- **Claude (Cowork / Claude Code):** a `.claude-plugin/plugin.json` manifest is included so the library installs directly as a native Claude plugin. Cowork's plugin loader auto-discovers skills at exactly `skills/<skill-name>/SKILL.md` — one level deep, no domain subfolder — so this repo keeps that flat layout at the root.
- **Claude, Codex, Hermes Agent (and any other Agent Skills-compatible tool):** the [`vercel-labs/skills`](https://github.com/vercel-labs/skills) CLI (`npx skills`) reads the same flat layout with no changes needed, and copies/symlinks each skill into the right directory per agent. This is the primary cross-agent install path — we don't hand-build per-agent adapter files.

If this library grows to many skills across several domains later, group by domain using metadata inside each `SKILL.md` (or an explicit `skills` path list in `plugin.json`) rather than nested folders — nested folders break Cowork's auto-discovery even though the vercel CLI tolerates them.

## Status

**Early / single-skill stage.** We are deliberately starting small: prove one skill works well on Claude first, then confirm it installs cleanly on Codex and Hermes Agent via `npx skills`, before adding more skills. Scope is intentionally limited to these three agents for now — not the full 70+ the vercel CLI supports.

## Current skills

| Domain | Skill | Status |
|---|---|---|
| SDG Alignment | [`sdg-alignment-mapper`](skills/sdg-alignment-mapper/SKILL.md) | Testing on Claude |

The mapper is country-agnostic by default (maps to the UN Global Indicator Framework) and supports optional national-context overlays — Malaysia/MySDG is the first one, in `skills/sdg-alignment-mapper/references/malaysia.md`.

## Roadmap

1. ✅ Scaffold repo + first skill (`sdg-alignment-mapper`)
2. ✅ Confirm `npx skills add` discovers the skill and installs it correctly, scoped to Claude Code, Codex, and Hermes Agent
3. ✅ Test the skill end-to-end inside Claude (Cowork)
4. ✅ Test the skill end-to-end inside Codex
5. 🔲 Test the skill end-to-end inside Hermes Agent
6. ✅ Add structural CI validation (`scripts/validate_skills.py` + GitHub Actions)
7. 🔲 Publish to GitHub
8. 🔲 Add more skills once the pattern is validated across all three

## Install

**Claude — Cowork:** Customize → (+) Add Plugin → paste this repo's URL once it's pushed to GitHub.

**Claude — Claude Code CLI:**
```
claude plugin install <repo-url>
```

**Claude, Codex, or Hermes Agent — via `npx skills`:**
```
npx skills add <repo-url> --skill sdg-alignment-mapper -a claude-code -a codex -a hermes-agent
```
Add `-g` to install globally instead of per-project, or drop `--skill` / `-a` flags to be prompted interactively.

**Manual (any agent):** copy `skills/<skill-name>/` into your agent's skills directory.

## Testing

`scripts/validate_skills.py` is a dependency-free structural check that runs on every push/PR via `.github/workflows/validate.yml`. It catches format regressions before they reach an install — including the nested-folder bug that once broke Cowork's plugin discovery.

Specifically it checks:

- `.claude-plugin/plugin.json` exists, is valid JSON, and has a lowercase kebab-case `name`
- every skill lives at exactly `skills/<skill-name>/SKILL.md` — one level deep, never nested under a domain folder
- every `SKILL.md` has valid frontmatter with required `name` and `description` fields, and the frontmatter `name` matches its folder name
- every file under a skill's `references/` is actually mentioned in its `SKILL.md` (no orphaned reference files)
- every `references/*.md` path mentioned in a `SKILL.md` body actually exists on disk (no broken links after a rename)

The CI workflow also runs `npx skills add . --list` as a smoke test, confirming the vercel CLI can actually discover every skill — not just that the static checks pass.

Run it locally before committing:
```
python3 scripts/validate_skills.py
```

This covers structural/format correctness only — it does not check whether a skill's output is actually good (e.g., whether an SDG mapping is accurate). That would require a behavioral eval harness, which is a possible future addition once there are more skills to justify the setup cost.

## Adding a new national context

To extend `sdg-alignment-mapper` to another country, add `skills/sdg-alignment-mapper/references/<country>.md` following the same structure as the Malaysia file (indicator availability categories, national vs. global target differences, any sub-national reporting layer), then list it in the skill's SKILL.md.

## License

CC BY-SA 4.0 — open, forkable, share-alike.
