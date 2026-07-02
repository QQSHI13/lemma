"""Prerequisites hook for DocsForge — injects folded prerequisites admonition.

Reads frontmatter prerequisites and renders them as a foldable "Prerequisites"
box at the top of each content page.
"""
from __future__ import annotations

import json
from pathlib import Path

_CONCEPTS_CACHE: dict[str, dict] = {}

def _load_concepts(config):
    """Load concepts.json once and cache."""
    global _CONCEPTS_CACHE
    if _CONCEPTS_CACHE:
        return _CONCEPTS_CACHE

    cfg_path = Path(config.config_file_path).resolve().parent
    concepts_file = cfg_path / "concepts.json"

    if not concepts_file.exists():
        return {}

    with open(concepts_file) as f:
        data = json.load(f)

    _CONCEPTS_CACHE = {c["id"]: c for c in data.get("concepts", [])}
    return _CONCEPTS_CACHE


def _rel_path(from_uri: str, to_area: str, to_id: str) -> str:
    """Compute relative markdown path from current page to target page."""
    from_dir = "/".join(from_uri.split("/")[:-1])  # e.g., 'foundations'
    if from_dir == to_area:
        return f"{to_id}.md"
    elif from_dir == "":
        return f"{to_area}/{to_id}.md"
    else:
        return f"../{to_area}/{to_id}.md"


def on_page_markdown(markdown, *, page, config, files):
    """Inject folded prerequisites admonition at top of content pages."""
    try:
        src_uri = getattr(page.file, "src_uri", "")

        # Skip index pages and root index
        if src_uri.endswith("/index.md") or src_uri == "index.md":
            return markdown

        # Frontmatter is already parsed into page.meta by docsforge
        meta = getattr(page, "meta", {}) or {}
        prerequisites = meta.get("prerequisites") or []

        # Handle single string or list
        if isinstance(prerequisites, str):
            prerequisites = [prerequisites] if prerequisites else []

        # Filter out empty/null entries
        prerequisites = [p for p in prerequisites if p]
        if not prerequisites:
            return markdown

        concepts = _load_concepts(config)

        # Build prerequisite links
        lines = ["??? note \"Prerequisites\""]
        lines.append("")
        lines.append("    Before reading this page, you should be familiar with:")
        lines.append("")

        for prereq_id in prerequisites:
            concept = concepts.get(prereq_id, {})
            name = concept.get("name", prereq_id.replace("-", " ").title())
            area = concept.get("area", "")
            path = _rel_path(src_uri, area, prereq_id) if area else f"{prereq_id}.md"
            lines.append(f"    - [{name}]({path})")

        lines.append("")

        admonition = "\n".join(lines)
        return admonition + "\n" + markdown

    except Exception as e:
        print(f"[prerequisites] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return markdown
