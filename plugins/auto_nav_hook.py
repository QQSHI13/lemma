"""Auto-nav hook for DocsForge — generates nav from docs/ frontmatter.

Reads frontmatter from all markdown files to build navigation.
Areas defined in docsforge.yml or auto-detected from file paths.
"""
from __future__ import annotations

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
    """Generate nav from docs/ file structure and frontmatter."""
    cfg_path = Path(config.config_file_path).resolve().parent
    docs_dir = cfg_path / "docs"

    # Load area order from docsforge.yml if present, or auto-detect
    area_order = {}
    extra = config.get("extra", {})
    lemma_extra = extra.get("lemma", {})
    areas_config = lemma_extra.get("areas", [])
    
    if areas_config:
        for i, area in enumerate(areas_config):
            area_order[area] = i

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

        if not area:
            continue

        if not title:
            title = md_file.stem.replace("-", " ").title()

        area_pages.setdefault(area, []).append((title, rel_str))

    # Sort areas: configured order first, then alphabetically
    def area_sort_key(a):
        return (area_order.get(a, 999), a.lower())

    sorted_areas = sorted(area_pages.keys(), key=area_sort_key)

    # Build nav
    nav = [{"Home": "index.md"}]

    for area_id in sorted_areas:
        pages = area_pages[area_id]
        area_name = area_id.replace("-", " ").title()

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
