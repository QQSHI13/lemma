"""Build concepts database from frontmatter."""
from __future__ import annotations

import re
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


def on_config(config):
    cfg_path = Path(config.config_file_path).resolve().parent
    docs_dir = cfg_path / "docs"
    db_path = cfg_path / "concepts.db"

    import sqlite3
    import json
    
    db_path.unlink(missing_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
        CREATE TABLE concepts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            area TEXT NOT NULL,
            file_path TEXT NOT NULL,
            prerequisites TEXT,
            related TEXT,
            status TEXT DEFAULT 'draft',
            author TEXT,
            quality_score INTEGER DEFAULT 0,
            difficulty INTEGER DEFAULT 1,
            last_reviewed TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE prerequisites (
            concept_id TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
            prerequisite_id TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
            PRIMARY KEY (concept_id, prerequisite_id)
        )
    """)

    conn.execute("""
        CREATE TABLE unlocks (
            concept_id TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
            unlocks_id TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
            PRIMARY KEY (concept_id, unlocks_id)
        )
    """)

    conn.execute("CREATE INDEX idx_concepts_area ON concepts(area)")
    conn.execute("CREATE INDEX idx_concepts_status ON concepts(status)")
    conn.execute("CREATE INDEX idx_prerequisites_concept ON prerequisites(concept_id)")
    conn.execute("CREATE INDEX idx_prerequisites_prereq ON prerequisites(prerequisite_id)")

    concepts = []

    # Pass 1: Collect all concepts
    for md_file in sorted(docs_dir.rglob("*.md")):
        rel = md_file.relative_to(docs_dir)
        rel_str = str(rel).replace("\\", "/")

        if rel_str == "index.md" or rel_str.endswith("/index.md"):
            continue

        content = md_file.read_text()
        fm = _read_frontmatter(content)

        if not fm:
            continue

        concept_id = md_file.stem
        area = fm.get("area")

        if not area:
            parts = rel_str.split("/")
            if len(parts) >= 2:
                area = parts[0]

        prereqs = fm.get("prerequisites") or []
        related = fm.get("related") or []

        conn.execute("""
            INSERT INTO concepts (id, name, area, file_path, prerequisites, related, status, author, quality_score, difficulty, last_reviewed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            concept_id,
            fm.get("title", concept_id.replace("-", " ").title()),
            area or "uncategorized",
            rel_str,
            json.dumps(prereqs),
            json.dumps(related),
            fm.get("status", "draft"),
            fm.get("author"),
            fm.get("quality_score", 0),
            fm.get("difficulty", 1),
            fm.get("last_reviewed")
        ))

        concepts.append({"id": concept_id, "prerequisites": prereqs})

    # Pass 2: Insert prerequisites (all concepts now exist)
    concept_ids = {c["id"] for c in concepts}
    for concept in concepts:
        for prereq in concept.get("prerequisites", []):
            if isinstance(prereq, dict):
                prereq_id = prereq.get("id", prereq.get("concept", ""))
            else:
                prereq_id = prereq
            if prereq_id and prereq_id in concept_ids:
                conn.execute("INSERT INTO prerequisites (concept_id, prerequisite_id) VALUES (?, ?)", (concept["id"], prereq_id))

    # Pass 3: Compute unlocks
    for concept in concepts:
        for prereq in concept.get("prerequisites", []):
            if isinstance(prereq, dict):
                prereq_id = prereq.get("id", prereq.get("concept", ""))
            else:
                prereq_id = prereq
            if prereq_id and prereq_id in concept_ids:
                conn.execute("INSERT INTO unlocks (concept_id, unlocks_id) VALUES (?, ?)", (prereq_id, concept["id"]))

    conn.commit()
    conn.close()

    print(f"[build_concepts] Generated {db_path} with {len(concepts)} concepts")
    return config
