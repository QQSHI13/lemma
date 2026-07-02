#!/usr/bin/env python3
"""Auto-generate docsforge nav from concepts.json + docs/ structure.

Run before `docsforge build` to update nav in docsforge.yml.
"""

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
CONFIG_FILE = ROOT / "docsforge.yml"
CONCEPTS_FILE = ROOT / "concepts.json"


def read_frontmatter(path: Path) -> dict:
    """Read YAML frontmatter from a markdown file."""
    content = path.read_text()
    if not content.startswith("---"):
        return {}
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def generate_nav() -> list:
    """Generate nav structure from file system + concepts.json."""
    # Load concepts.json
    with open(CONCEPTS_FILE) as f:
        data = json.load(f)

    areas = {a["id"]: a for a in data.get("areas", [])}
    area_order = {a["id"]: a.get("order", 99) for a in data.get("areas", [])}

    # Build concept ID → concept map for titles
    concepts = {c["id"]: c for c in data.get("concepts", [])}

    # Group pages by area
    area_pages: dict[str, list[tuple[str, str]]] = {}  # area -> [(title, path), ...]

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        rel = md_file.relative_to(DOCS_DIR)
        rel_str = str(rel).replace("\\", "/")

        # Skip root index (handled separately)
        if rel_str == "index.md":
            continue

        fm = read_frontmatter(md_file)
        title = fm.get("title")
        area = fm.get("area")

        # Infer area from path if not in frontmatter
        if not area:
            parts = rel_str.split("/")
            if len(parts) >= 2:
                area = parts[0]

        # Skip files in unknown areas (not in concepts.json)
        if area not in areas:
            continue

        if not title:
            # Fall back to concept name
            stem = md_file.stem
            title = concepts.get(stem, {}).get("name", stem.replace("-", " ").title())

        if area not in area_pages:
            area_pages[area] = []

        area_pages[area].append((title, rel_str))

    # Sort areas by order from concepts.json
    sorted_areas = sorted(area_pages.keys(), key=lambda a: area_order.get(a, 99))

    # Build nav with proper {Title: path} entries
    nav = []
    nav.append({"Home": "index.md"})

    for area_id in sorted_areas:
        pages = area_pages[area_id]
        area_name = areas.get(area_id, {}).get("name", area_id.replace("-", " ").title())

        # Sort pages: index first, then alphabetically by title
        def sort_key(item):
            title, path = item
            is_index = path.endswith("/index.md") or path == f"{area_id}/index.md"
            return (0 if is_index else 1, title.lower())

        pages.sort(key=sort_key)

        # Build section: area name -> list of {Title: path} dicts
        section_pages = []
        for title, path in pages:
            # For index pages, use the area name as title (or keep as-is)
            if path.endswith("/index.md"):
                section_pages.append(path)  # Just the path, docsforge shows directory name
            else:
                section_pages.append({title: path})

        section = {area_name: section_pages}
        nav.append(section)

    return nav


def update_config():
    """Update docsforge.yml with auto-generated nav."""
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)

    config["nav"] = generate_nav()

    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, sort_keys=False, allow_unicode=True)

    print("Nav updated in docsforge.yml")


if __name__ == "__main__":
    update_config()
