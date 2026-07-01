#!/usr/bin/env python3
"""
Generate registry.json from every skills/<name>/SKILL.md's frontmatter.

registry.json is the single source of truth the companion website
(ngo-agent-skills-site) builds from — it never reads SKILL.md files
directly. Regenerate and commit this file whenever a skill is added or its
frontmatter changes. CI (see .github/workflows/validate.yml) fails the
build if registry.json is out of date, the same way the reference skill
library we looked at treats an un-regenerated registry as a build error.

Run locally:
    python3 scripts/generate_registry.py

Exits non-zero if any skill fails to parse (run validate_skills.py first —
this script assumes the frontmatter is already valid).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _frontmatter import parse_frontmatter, as_bool  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REGISTRY_JSON = ROOT / "registry.json"


def build_registry():
    skills = []
    errors = []

    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            continue

        rel_path = skill_md.relative_to(ROOT).as_posix()
        body = skill_md.read_text()
        fm = parse_frontmatter(
            body, on_error=lambda msg, p=rel_path: errors.append(f"{p}: {msg}")
        )

        skills.append(
            {
                "name": fm.get("name", entry.name),
                "description": fm.get("description", ""),
                "version": fm.get("version", ""),
                "license": fm.get("license", ""),
                "evidence_strength": fm.get("evidence_strength", ""),
                "evidence_sources": fm.get("evidence_sources", []),
                "topics": fm.get("topics", []),
                "official": as_bool(fm.get("official")),
                "last_reviewed": fm.get("last_reviewed", ""),
                "path": rel_path,
            }
        )

    if errors:
        for e in errors:
            print(f"ERROR  {e}")
        print(
            "\nregistry.json was not written because frontmatter failed to parse. "
            "Run scripts/validate_skills.py for the full picture."
        )
        sys.exit(1)

    # Deliberately no "generated_at" timestamp here: this file is committed
    # to git, and a volatile timestamp would make every regeneration look
    # like a change even when no skill content actually changed, defeating
    # the CI "is registry.json up to date" check in validate.yml.
    return {
        "skill_count": len(skills),
        "skills": skills,
    }


def main():
    registry = build_registry()
    REGISTRY_JSON.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"Wrote {REGISTRY_JSON.relative_to(ROOT)} — {registry['skill_count']} skill(s).")


if __name__ == "__main__":
    main()
