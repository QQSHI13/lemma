"""Prerequisites hook for DocsForge — injects folded prerequisites admonition.

Reads frontmatter prerequisites and renders them as a foldable "Prerequisites"
box at the top of each content page. Skips index pages.
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


def _get_page_title(config, page_file: str) -> str:
    """Get title from frontmatter or filename."""
    docs_dir = Path(config.config_file_path).resolve().parent / "docs"
    file_path = docs_dir / page_file
    if not file_path.exists():
        return page_file.replace("-", " ").title()
    
    fm = _read_frontmatter(file_path.read_text())
    return fm.get("title", page_file.replace("-", " ").title())


def _build_prerequisites_md(config, prerequisites: list) -> str:
    """Build prerequisites admonition from frontmatter list."""
    if not prerequisites:
        return ""
    
    lines = ["??? note \"Prerequisites\"", ""]
    
    for prereq_id in prerequisites:
        if isinstance(prereq_id, dict):
            # Complex prerequisite with description
            prereq_id = prereq_id.get("id", prereq_id.get("concept", ""))
        
        if not prereq_id:
            continue
            
        title = _get_page_title(config, f"{prereq_id}.md")
        lines.append(f"- [{title}]({prereq_id}.md)")
    
    lines.append("")
    return "\n".join(lines)


def on_page_markdown(markdown, page, config, files):
    """Inject prerequisites admonition after the heading."""
    src_uri = getattr(page, "src_uri", "")
    if not src_uri or src_uri.endswith("/index.md") or src_uri == "index.md":
        return markdown

    fm = _read_frontmatter(markdown)
    prerequisites = fm.get("prerequisites")
    
    if not prerequisites:
        return markdown

    prereq_md = _build_prerequisites_md(config, prerequisites)
    if not prereq_md:
        return markdown

    # Find first heading and insert after it
    heading_match = re.search(r"^(# .+)$", markdown, re.MULTILINE)
    if heading_match:
        insert_pos = heading_match.end()
        return markdown[:insert_pos] + "\n\n" + prereq_md + markdown[insert_pos:]

    return markdown
