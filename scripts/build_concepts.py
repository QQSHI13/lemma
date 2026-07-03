#!/usr/bin/env python3
"""Build script to generate concepts.json from frontmatter.

Scans all markdown files in docs/, reads their frontmatter, and generates
a concepts.json that is a pure derived artifact. Do NOT edit concepts.json manually.
"""
from __future__ import annotations

import json
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


def _get_area_order() -> list:
    """Read area order from docsforge.yml."""
    docsforge_path = Path(__file__).parent.parent / "docsforge.yml"
    if not docsforge_path.exists():
        return []
    
    content = docsforge_path.read_text()
    # Find extra.lemma.areas
    match = re.search(r'extra:\s*\n\s*lemma:\s*\n.*?areas:\s*\n((?:\s+-\s+\w+\s*\n)+)', content, re.DOTALL)
    if match:
        areas = re.findall(r'-\s+(\w+)', match.group(1))
        return areas
    return []


def build_concepts():
    docs_dir = Path(__file__).parent.parent / "docs"
    concepts = []
    seen_areas = set()
    
    for md_file in docs_dir.rglob("*.md"):
        rel = md_file.relative_to(docs_dir)
        rel_str = str(rel).replace("\\", "/")
        
        if rel_str == "index.md":
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
        
        if area:
            seen_areas.add(area)
        
        concept = {
            "id": concept_id,
            "name": fm.get("title", concept_id.replace("-", " ").title()),
            "area": area or "uncategorized",
            "prerequisites": fm.get("prerequisites", []),
            "unlocks": [],  # Will be computed later
            "related": fm.get("related", []),
            "status": fm.get("status", "draft"),
            "author": fm.get("author"),
            "quality_score": fm.get("quality_score", 0),
            "page_exists": True,
            "last_reviewed": fm.get("last_reviewed"),
            "difficulty": fm.get("difficulty", 1)
        }
        concepts.append(concept)
    
    # Compute unlocks (reverse of prerequisites)
    concept_map = {c["id"]: c for c in concepts}
    for concept in concepts:
        prereqs = concept.get("prerequisites", [])
        for prereq in prereqs:
            if isinstance(prereq, dict):
                prereq_id = prereq.get("id", prereq.get("concept", ""))
            else:
                prereq_id = prereq
            if prereq_id and prereq_id in concept_map:
                concept_map[prereq_id].setdefault("unlocks", []).append(concept["id"])
    
    # Build areas list
    area_order = _get_area_order()
    areas = []
    for i, area_id in enumerate(area_order):
        if area_id in seen_areas:
            areas.append({
                "id": area_id,
                "name": area_id.replace("-", " ").title(),
                "order": i + 1
            })
            seen_areas.discard(area_id)
    
    # Add remaining areas not in config
    for area_id in sorted(seen_areas):
        areas.append({
            "id": area_id,
            "name": area_id.replace("-", " ").title(),
            "order": len(areas) + 1
        })
    
    # Find bootstrap concepts (no prerequisites)
    bootstrap = [c["id"] for c in concepts if not c.get("prerequisites")]
    
    output = {
        "version": "1.0.0",
        "bootstrap_concepts": bootstrap,
        "concepts": concepts,
        "areas": areas,
        "notation_registry": {}
    }
    
    output_path = Path(__file__).parent.parent / "concepts.json"
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"[build_concepts] Generated {len(concepts)} concepts, {len(areas)} areas")


if __name__ == "__main__":
    build_concepts()
