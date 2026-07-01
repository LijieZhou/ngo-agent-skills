"""
Shared minimal YAML-subset frontmatter parser for this library's SKILL.md
files. Used by both scripts/validate_skills.py and scripts/generate_registry.py
so there is exactly one place that understands the frontmatter format.

Supports scalar 'key: value' lines and block sequences ('key:' followed by
indented '- item' lines). Deliberately does not take on a PyYAML dependency —
the skill library's whole design principle is "no dependencies, no build
step," and this is simple enough to not need one.
"""
import re

_LIST_ITEM_RE = re.compile(r"^\s+-\s+(.*)$")


def parse_frontmatter(text, on_error=None):
    """Parse the YAML-subset frontmatter block at the top of `text`.

    `on_error(msg)` is called for each malformed line encountered; if not
    provided, malformed lines are silently skipped. Returns a dict of the
    parsed fields (possibly incomplete if errors occurred).
    """
    if on_error is None:
        on_error = lambda msg: None  # noqa: E731

    if not text.startswith("---\n"):
        on_error("missing YAML frontmatter (file must start with '---')")
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        on_error("frontmatter opened with '---' but never closed")
        return {}

    block = text[4:end]
    data = {}
    current_list_key = None
    for raw_line in block.splitlines():
        if not raw_line.strip():
            continue

        list_item = _LIST_ITEM_RE.match(raw_line)
        if list_item:
            if current_list_key is None:
                on_error(f"list item with no preceding key: {raw_line!r}")
                continue
            item = list_item.group(1).strip().strip('"').strip("'")
            data[current_list_key].append(item)
            continue

        if ":" not in raw_line:
            on_error(f"malformed frontmatter line: {raw_line!r}")
            continue

        key, _, value = raw_line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            # Key introduces a block sequence on following indented lines.
            current_list_key = key
            data[key] = []
        else:
            current_list_key = None
            data[key] = value.strip('"').strip("'")
    return data


def as_bool(value):
    """Coerce a parsed scalar string to a bool, or None if not a valid bool."""
    if isinstance(value, bool):
        return value
    if value in ("true", "True"):
        return True
    if value in ("false", "False"):
        return False
    return None
