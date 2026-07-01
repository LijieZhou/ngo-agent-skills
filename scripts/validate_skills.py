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
  - every file under a skill's references/ is actually mentioned in its
    SKILL.md (catches orphaned reference files)
  - every references/*.md path mentioned in a SKILL.md body actually exists
    on disk (catches broken links, e.g. after a rename)

Run locally:
    python3 scripts/validate_skills.py

Exits non-zero and prints every failure if any check fails.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []


def fail(msg):
    errors.append(msg)


def parse_frontmatter(text, rel_path):
    if not text.startswith("---\n"):
        fail(f"{rel_path}: missing YAML frontmatter (file must start with '---')")
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{rel_path}: frontmatter opened with '---' but never closed")
        return {}
    block = text[4:end]
    data = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"{rel_path}: malformed frontmatter line: {line!r}")
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


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
        fm = parse_frontmatter(body, rel_skill_md)

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

    print(f"OK — {skill_count} skill(s) passed structural validation.")


if __name__ == "__main__":
    main()
