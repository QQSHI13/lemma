"""Auto-nav hook for DocsForge — generates nav from concepts.json + docs/ structure.

Replaces manual nav editing in docsforge.yml. Place in hooks list before build.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


def _read_frontmatter(content: str) -> dict:
    """Read YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def on_config(config):
    """Generate nav from concepts.json and docs/ file structure."""
    # Resolve paths relative to config file
    cfg_path = Path(config.config_file_path).resolve().parent
    docs_dir = cfg_path / "docs"
    concepts_file = cfg_path / "concepts.json"

    if not concepts_file.exists():
        print("[auto_nav] concepts.json not found, skipping nav generation")
        return config

    # Load concepts.json
    with open(concepts_file) as f:
        data = json.load(f)

    areas = {a["id"]: a for a in data.get("areas", [])}
    area_order = {a["id"]: a.get("order", 99) for a in data.get("areas", [])}
    concepts = {c["id"]: c for c in data.get("concepts", [])}

    # Group pages by area
    area_pages: dict[str, list[tuple[str, str]]] = {}

    for md_file in sorted(docs_dir.rglob("*.md")):
        rel = md_file.relative_to(docs_dir)
        rel_str = str(rel).replace("\\", "/")

        if rel_str == "index.md":
            continue

        fm = _read_frontmatter(md_file.read_text())
        title = fm.get("title")
        area = fm.get("area")

        if not area:
            parts = rel_str.split("/")
            if len(parts) >= 2:
                area = parts[0]

        if area not in areas:
            continue  # Skip unknown areas

        if not title:
            stem = md_file.stem
            title = concepts.get(stem, {}).get("name", stem.replace("-", " ").title())

        area_pages.setdefault(area, []).append((title, rel_str))

    # Sort areas by order
    sorted_areas = sorted(area_pages.keys(), key=lambda a: area_order.get(a, 99))

    # Build nav
    nav = [{"Home": "index.md"}]

    for area_id in sorted_areas:
        pages = area_pages[area_id]
        area_name = areas.get(area_id, {}).get("name", area_id.replace("-", " ").title())

        # Sort: index first, then alphabetically
        def sort_key(item):
            title, path = item
            is_index = path.endswith("/index.md")
            return (0 if is_index else 1, title.lower())

        pages.sort(key=sort_key)

        section_pages = []
        for title, path in pages:
            if path.endswith("/index.md"):
                section_pages.append(path)
            else:
                section_pages.append({title: path})

        nav.append({area_name: section_pages})

    config["nav"] = nav
    print(f"[auto_nav] Generated nav with {len(nav)} sections")
    return config
