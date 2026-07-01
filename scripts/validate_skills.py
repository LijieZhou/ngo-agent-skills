#!/usr/bin/env python3
"""
Structural validator for the NGO Agent Skills library.

Checks (no external dependencies — stdlib only):
  - .claude-plugin/plugin.json exists, is valid JSON, and has a lowercase
    kebab-case "name"
  - skills/ contains only one level of skill folders (skills/<name>/SKILL.md) —
    a nested domain folder here breaks Cowork's plugin auto-discovery even
    though other tools tolerate it
  - every skill folder name is lowercase kebab-case
  - every SKILL.md has YAML frontmatter with required "name" and
    "description" fields, and frontmatter "name" matches the folder name
  - every SKILL.md has an "evidence_strength" field set to one of the four
    allowed tiers, AND a non-empty "evidence_sources" list — every skill
    must say where its approach comes from and how strong that backing is,
    not just claim to be evidence-based in prose
  - every SKILL.md has a non-empty "topics" list (kebab-case entries), an
    "official" boolean, and a "last_reviewed" date in YYYY-MM-DD format —
    these three power the website's Topics/Official/Audit pages, generated
    from scripts/generate_registry.py
  - every file under a skill's references/ is actually mentioned in its
    SKILL.md (catches orphaned reference files)
  - every references/*.md path mentioned in a SKILL.md body actually exists
    on disk (catches broken links, e.g. after a rename)

Note on evidence enforcement: this deliberately goes further than a similar
check in a reference skill library we looked at, whose validator confirmed
an `evidence_strength` field existed but never checked it was one of the
allowed values, and never checked `evidence_sources` was non-empty — two
skills in that library ended up with off-schema values (e.g. "low-moderate")
that slipped through because nothing enforced the enum. Presence-only
checks catch "you forgot the field," not "you filled it in badly."

Run locally:
    python3 scripts/validate_skills.py

Exits non-zero and prints every failure if any check fails.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _frontmatter import parse_frontmatter, as_bool  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# MEL (Monitoring, Evaluation & Learning) evidence tiers — see docs/EVIDENCE.md
ALLOWED_EVIDENCE_TIERS = {
    "established-standard",   # e.g. OECD-DAC criteria, Sphere, UN/DOSM official frameworks
    "evidence-based",         # peer-reviewed evaluation research showing the approach works
    "emerging-practice",      # documented sector guidance, not yet strongly validated
    "original-framework",     # our own design, explicitly labelled as such
}

errors = []


def fail(msg):
    errors.append(msg)


def check_plugin_json():
    if not PLUGIN_JSON.is_file():
        fail(f"Missing {PLUGIN_JSON.relative_to(ROOT)}")
        return
    try:
        plugin = json.loads(PLUGIN_JSON.read_text())
    except json.JSONDecodeError as e:
        fail(f"{PLUGIN_JSON.relative_to(ROOT)}: invalid JSON ({e})")
        return
    name = plugin.get("name", "")
    if not name:
        fail(f"{PLUGIN_JSON.relative_to(ROOT)}: missing required 'name' field")
    elif not KEBAB_RE.match(name):
        fail(f"{PLUGIN_JSON.relative_to(ROOT)}: name '{name}' is not lowercase kebab-case")


def check_evidence(fm, rel_skill_md):
    tier = fm.get("evidence_strength", "")
    if not tier:
        fail(f"{rel_skill_md}: missing required 'evidence_strength' field")
    elif tier not in ALLOWED_EVIDENCE_TIERS:
        fail(
            f"{rel_skill_md}: evidence_strength '{tier}' is not one of "
            f"{sorted(ALLOWED_EVIDENCE_TIERS)}"
        )

    sources = fm.get("evidence_sources")
    if sources is None:
        fail(f"{rel_skill_md}: missing required 'evidence_sources' list")
    elif not isinstance(sources, list) or len(sources) == 0:
        fail(
            f"{rel_skill_md}: 'evidence_sources' must be a non-empty list — "
            f"even an original-framework skill must say so explicitly "
            f"(e.g. 'Original framework — no external evidence base; see docs/EXCLUSIONS.md')"
        )


def check_site_fields(fm, rel_skill_md):
    """topics / official / last_reviewed — required for the website (Topics,
    Official, and Audit pages) built from scripts/generate_registry.py."""
    topics = fm.get("topics")
    if topics is None or not isinstance(topics, list) or len(topics) == 0:
        fail(f"{rel_skill_md}: missing required non-empty 'topics' list")
    else:
        for topic in topics:
            if not KEBAB_RE.match(topic):
                fail(f"{rel_skill_md}: topic '{topic}' is not lowercase kebab-case")

    official = fm.get("official")
    if official is None:
        fail(f"{rel_skill_md}: missing required 'official' field")
    elif as_bool(official) is None:
        fail(f"{rel_skill_md}: 'official' must be true or false, got {official!r}")

    last_reviewed = fm.get("last_reviewed", "")
    if not last_reviewed:
        fail(f"{rel_skill_md}: missing required 'last_reviewed' date (YYYY-MM-DD)")
    elif not DATE_RE.match(last_reviewed):
        fail(f"{rel_skill_md}: 'last_reviewed' must be YYYY-MM-DD, got {last_reviewed!r}")


def check_skills():
    if not SKILLS_DIR.is_dir():
        fail("Missing skills/ directory")
        return 0

    count = 0
    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        count += 1
        skill_name = entry.name
        skill_md = entry / "SKILL.md"
        rel_skill_md = skill_md.relative_to(ROOT)

        if not KEBAB_RE.match(skill_name):
            fail(f"skills/{skill_name}: folder name is not lowercase kebab-case")

        # Catch accidental re-introduction of a nested domain folder — this is
        # the exact bug that broke Cowork's plugin auto-discovery previously.
        nested = [
            p.name for p in entry.iterdir()
            if p.is_dir() and p.name != "references" and (p / "SKILL.md").is_file()
        ]
        if nested:
            fail(
                f"skills/{skill_name}: contains nested SKILL.md one level too deep "
                f"({nested}) — Cowork only discovers skills/<name>/SKILL.md, not "
                f"skills/<domain>/<name>/SKILL.md"
            )

        if not skill_md.is_file():
            fail(f"skills/{skill_name}: missing SKILL.md")
            continue

        body = skill_md.read_text()
        fm = parse_frontmatter(body, on_error=lambda msg: fail(f"{rel_skill_md}: {msg}"))

        if "name" not in fm:
            fail(f"{rel_skill_md}: frontmatter missing required 'name' field")
        elif fm["name"] != skill_name:
            fail(
                f"{rel_skill_md}: frontmatter name '{fm['name']}' does not match "
                f"folder name '{skill_name}'"
            )

        if not fm.get("description", "").strip():
            fail(f"{rel_skill_md}: frontmatter missing required 'description' field")
        elif len(fm["description"]) < 20:
            fail(f"{rel_skill_md}: description is too short to support skill discovery")

        check_evidence(fm, rel_skill_md)
        check_site_fields(fm, rel_skill_md)

        # Every file under references/ should be mentioned in SKILL.md.
        refs_dir = entry / "references"
        if refs_dir.is_dir():
            for ref_file in sorted(refs_dir.rglob("*")):
                if ref_file.is_file() and ref_file.name not in body:
                    fail(
                        f"{ref_file.relative_to(ROOT)}: exists but is never mentioned "
                        f"in {skill_md.name} (orphaned reference file)"
                    )

        # Every references/*.md path mentioned in the body should exist on disk.
        for match in re.finditer(r"references/([A-Za-z0-9_\-./]+\.md)", body):
            ref_path = entry / "references" / match.group(1)
            if not ref_path.is_file():
                fail(f"{rel_skill_md}: references missing file 'references/{match.group(1)}'")

    return count


def main():
    check_plugin_json()
    skill_count = check_skills()

    if errors:
        print(f"FAILED — {len(errors)} issue(s):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"OK — {skill_count} skill(s) passed structural validation, including evidence sourcing.")


if __name__ == "__main__":
    main()
