"""Prerequisites hook for DocsForge — injects folded prerequisites admonition."""
from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import yaml


def _read_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def on_page_markdown(markdown, page, config, files):
    src_uri = getattr(page, "src_uri", "")
    if not src_uri or src_uri.endswith("/index.md") or src_uri == "index.md":
        return markdown

    fm = _read_frontmatter(markdown)
    prerequisites = fm.get("prerequisites")
    
    if not prerequisites:
        return markdown

    # Build prerequisites markdown
    lines = ["??? note \"Prerequisites\"", ""]
    
    for prereq in prerequisites:
        if isinstance(prereq, dict):
            prereq_id = prereq.get("id", prereq.get("concept", ""))
        else:
            prereq_id = prereq
        
        if not prereq_id:
            continue
        
        # Try to get title from SQLite
        title = prereq_id.replace("-", " ").title()
        cfg_path = Path(config.config_file_path).resolve().parent
        db_path = cfg_path / "concepts.db"
        if db_path.exists():
            try:
                conn = sqlite3.connect(db_path)
                row = conn.execute("SELECT name FROM concepts WHERE id = ?", (prereq_id,)).fetchone()
                if row:
                    title = row[0]
                conn.close()
            except Exception:
                pass
        
        lines.append(f"- [{title}]({prereq_id}.md)")
    
    lines.append("")
    prereq_md = "\n".join(lines)

    # Find first heading and insert after it
    heading_match = re.search(r"^(# .+)$", markdown, re.MULTILINE)
    if heading_match:
        insert_pos = heading_match.end()
        return markdown[:insert_pos] + "\n\n" + prereq_md + markdown[insert_pos:]

    return markdown
