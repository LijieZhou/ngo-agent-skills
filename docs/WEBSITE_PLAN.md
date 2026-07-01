# NGO Agent Skills — Website Plan

Modeled on [skills.sh](https://www.skills.sh) (Vercel's Agent Skills Directory), adapted for the NGO/MEL context and for where this project actually is: two skills, one repo, one maintainer.

Reference: skills.sh's real navigation is Topics / Official / Audits / Docs, backed by a leaderboard of installs across many indexed repos, a per-skill security-audit aggregation (Gen Agent Trust Hub, Socket, Snyk), and an "Official" list of the companies that publish skills for their own products. We're keeping the four section names because they're good ones, but changing what each one means and how it's populated, since our risk profile and scale are different.

## Phased scope

**Phase 1 (build now): single-repo showcase.** The site reads only `ngo-agent-skills`' own generated `registry.json`. No crawler, no database, no external submissions. This is what the rest of this plan details.

**Phase 2 (later): multi-org NGO skills directory.** Once other NGOs or institutions have their own compatible skill repos, the site grows into an actual directory — indexing multiple repos, with a submission process and moderation. Phase 1's data schema is designed so this is an additive change, not a rewrite. See "Designing for Phase 2" at the end.

Do not start Phase 2 work until Phase 1 is live and there's an actual second repo wanting to be listed — building crawler/moderation infrastructure for a directory of one is wasted effort.

---

## Architecture (Phase 1)

**Data source:** a new `scripts/generate_registry.py` (mirrors the pattern in the education-agent-skills reference repo) reads every `skills/<name>/SKILL.md`'s frontmatter and emits a single `registry.json` at the repo root. This becomes the one source of truth the site builds from — no separate content to maintain.

**Site generator:** Next.js with static export (`next build`, static HTML/JSON output, no server, no database). Reasons over a simpler static-HTML generator:
- It's the same framework skills.sh itself uses, so the mental model (and possibly some layout conventions) transfers if you ever want to compare notes or reuse patterns.
- Static export today can become a real server-rendered Next.js app later (API routes, a database) without switching frameworks — relevant because you want to grow into Phase 2, which will eventually need a real backend for crawling and moderation. Starting on a static-HTML-only generator would mean a rewrite when that day comes; starting on Next.js static export does not.
- Deploy target: GitHub Pages (free, ties naturally to the existing repo) or Vercel (also free for this scale, and consistent with the ecosystem this project plugs into). Either works with static export; recommend GitHub Pages for Phase 1 to keep everything under one GitHub account with no third-party account setup required.

**Repo placement:** a separate repo, e.g. `ngo-agent-skills-site`, not a folder inside `ngo-agent-skills` itself. The skill library's whole design principle is "no dependencies, no build step" (that's what makes it agent-agnostic and installable via `npx skills` or as a Claude plugin with zero setup). A Next.js site has a real build step and a `node_modules` tree — mixing that into the skill repo would contradict its own stated design goal. Keep them separate; the site repo just points at the skill repo's `registry.json` (via a GitHub raw URL or a git submodule) as its data source.

**CI:** a GitHub Action in `ngo-agent-skills` (the skill repo) already runs `validate_skills.py` on every push. Add a step there that also regenerates `registry.json` and commits it if changed — same pattern already used for `registry.json`/bundle regeneration in the reference repo. The site repo's own Action then rebuilds and redeploys whenever `registry.json` changes upstream.

---

## Frontmatter additions needed

Three fields aren't in the schema yet and the site needs them. Add these to both existing `SKILL.md` files, and extend `scripts/validate_skills.py` to enforce them (same pattern used for `evidence_strength`/`evidence_sources`):

| Field | Type | Purpose |
|---|---|---|
| `topics` | array | Powers the Topics page. e.g. `["sdg-alignment"]` for the mapper, `["me-program-design"]` for the logframe builder. A skill can have more than one topic. |
| `official` | boolean | Powers the Official page. Every skill in this repo is `true` for now (you're the sole maintainer) — but adding the field now means Phase 2 doesn't require retrofitting it onto every skill later. |
| `last_reviewed` | date (`YYYY-MM-DD`) | Powers the Audit page. When the evidence sourcing was last checked against current reality (e.g., against the latest DOSM report). |

## Page-by-page plan

### Home
Hero + the actual `npx skills add` install command for this repo, agent logos for Claude/Codex/Hermes Agent (not all 70+, matching your stated scope), and a plain list of current skills grouped by topic. Skip a skills.sh-style "leaderboard by install count" — you have no install telemetry, and faking a ranking with 2 skills would be misleading. If you want *a* popularity signal later, GitHub stars/forks on the repo are a defensible rough proxy; don't build fake analytics before there's real usage.

### Topics (`/topics`, `/topics/[topic]`)
Generated directly from the `topics` frontmatter field. Right now: **SDG Alignment** (1 skill), **M&E / Program Design** (1 skill). This page is basically free — it's the same grouping already in the README's "Current skills" table, just rendered as a browsable page instead of a static markdown table.

### Official (`/official`)
For skills.sh, "Official" distinguishes skills published by the actual company that makes the product (Anthropic, Microsoft, Stripe) from community submissions. For Phase 1, with one maintainer, this page is honestly a placeholder: it shows that all current skills are maintained by the core NGO Agent Skills team, with the `official` field ready to distinguish this from outside contributions once `CONTRIBUTING.md` starts accepting them. Don't oversell this page's importance yet — say plainly on the page that "official" here currently just means "maintained by this project," not "endorsed by an external NGO accreditation body." That distinction matters more once Phase 2 involves other orgs.

### Audit (`/audits`)
This is where the plan meaningfully diverges from skills.sh, per your call on Audit meaning. Instead of aggregating Socket/Snyk-style malicious-code scans (not the right fit — these are markdown instructions, not executable packages), this page surfaces **evidence and content accuracy status**, built directly from fields you already enforce:

- Evidence tier (`established-standard` / `evidence-based` / `emerging-practice` / `original-framework`)
- Source count and a link to the citations in `docs/EVIDENCE.md`
- `last_reviewed` date, with a staleness flag — e.g., if a skill cites an annually-updated report (like DOSM's SDG Indicators report) and `last_reviewed` is more than ~12-18 months old, flag it for re-verification rather than silently trusting a stale citation
- A direct link to any caveats already documented in the skill's own "Known limitations" section (both current skills already have these) and to `docs/EXCLUSIONS.md` where relevant

This is a genuinely more useful audit for your users than a security scan would be, since the real risk in this library is "the guidance is stale or the citation no longer reflects current government data," not "the file contains malware." Worth stating that framing explicitly on the page itself, so users understand what's being checked and what isn't (e.g., this page does *not* check for prompt-injection risk or unsafe shell commands in a skill — call that out as future scope if any skill ever ships a script, which neither current skill does).

### Docs (`/docs`)
Reuses content you've already written rather than duplicating it — the docs site should link to/render from the actual repo files so there's one source of truth:
- **Overview** — what this library is, the agent-agnostic philosophy (from `README.md`'s intro)
- **Install** — per-agent instructions, already written in `README.md`'s Install section
- **Contributing** — renders `CONTRIBUTING.md` directly
- **Evidence Policy** — renders `docs/EVIDENCE.md` and `docs/EXCLUSIONS.md`
- **FAQ** — new content worth writing once you have a few real user questions; don't invent FAQ entries speculatively

---

## Designing for Phase 2 (multi-org directory) — not building yet

So Phase 1 doesn't need a rewrite later:

- Keep `registry.json`'s schema generic enough that a second repo's `registry.json` could be merged in without a schema change — i.e., don't bake "this is the only repo" assumptions into field names.
- When Phase 2 starts, add a top-level directory listing (which repos are indexed) as its own small file, plus a GitHub Action that periodically fetches each listed repo's `registry.json` and merges them — this is the actual "crawler," and it's much simpler than a real web crawler because you're only ever fetching one well-known file path per registered repo, not scraping arbitrary pages.
- "Official" becomes a real governance question at that point: who verifies a submitting org is actually the NGO/institution it claims to be. Recommend a manual PR-based submission/review process (a human looks at each new repo before it's listed) rather than automated trust — this is a low-volume, high-stakes decision, exactly where automation is the wrong tool.
- "Audit" for externally-submitted skills should require the same `evidence_strength`/`evidence_sources`/`last_reviewed` schema so the audit page can render everyone uniformly; repos that don't comply get flagged rather than silently excluded, so gaps are visible rather than hidden.
- This is a meaningfully bigger project than Phase 1 — expect it to need a real database once more than a handful of repos are indexed, since merging and deduplicating JSON files by hand stops scaling fast. Don't build that infrastructure speculatively; build it when a second real repo actually wants to be listed.

---

## Concrete next steps for Phase 1

1. Add `topics`, `official`, `last_reviewed` frontmatter fields to both existing `SKILL.md` files; extend `scripts/validate_skills.py` to enforce them.
2. Write `scripts/generate_registry.py` → commit `registry.json`; add a CI step to regenerate and commit it on skill changes.
3. Scaffold a new `ngo-agent-skills-site` repo: Next.js, static export, five pages (Home, Topics, Official, Audit, Docs) reading from `registry.json`.
4. Deploy via GitHub Pages.
5. Wire a GitHub Action so the site rebuilds whenever `registry.json` changes upstream.
