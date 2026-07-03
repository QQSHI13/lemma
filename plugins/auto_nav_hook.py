"""Auto-nav hook for DocsForge — generates nav from SQLite."""
from __future__ import annotations

import sqlite3
from pathlib import Path


def on_config(config):
    cfg_path = Path(config.config_file_path).resolve().parent
    db_path = cfg_path / "concepts.db"
    
    if not db_path.exists():
        print(f"[auto_nav] Warning: {db_path} not found, skipping nav generation")
        return config
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Load area order from config
    extra = config.get("extra", {})
    lemma_extra = extra.get("lemma", {})
    area_order = lemma_extra.get("areas", [])
    
    # Group pages by area
    area_pages = {}
    for row in conn.execute("SELECT id, name, area, file_path FROM concepts ORDER BY name"):
        area = row["area"]
        if area not in area_pages:
            area_pages[area] = []
        area_pages[area].append({
            "title": row["name"],
            "path": row["file_path"]
        })
    
    conn.close()
    
    # Sort areas
    def area_sort_key(a):
        return (area_order.index(a) if a in area_order else 999, a.lower())
    
    sorted_areas = sorted(area_pages.keys(), key=area_sort_key)
    
    # Build nav
    nav = [{"Home": "index.md"}]
    
    for area_id in sorted_areas:
        pages = area_pages[area_id]
        area_name = area_id.replace("-", " ").title()
        
        # Sort: index first, then alphabetically
        def sort_key(p):
            is_index = p["path"].endswith("/index.md")
            return (0 if is_index else 1, p["title"].lower())
        
        pages.sort(key=sort_key)
        
        section_pages = []
        for p in pages:
            section_pages.append({p["title"]: p["path"]})
        
        nav.append({area_name: section_pages})
    
    config["nav"] = nav
    print(f"[auto_nav] Generated nav with {len(nav)} sections")
    return config
