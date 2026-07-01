#!/usr/bin/env python3
"""Convert PLAN.md topic outline to concepts.json dependency graph."""

import re
import json
import sys
from pathlib import Path

PLAN_FILE = Path("PLAN.md")
CONCEPTS_FILE = Path("concepts.json")


def parse_plan():
    """Parse PLAN.md and extract concept hierarchy with dependencies."""
    content = PLAN_FILE.read_text()
    concepts = []
    areas = {}
    current_area = None
    area_order = 0

    # Extract area sections
    for line in content.split('\n'):
        # Area headers like "## algebra/" or "├── algebra/"
        area_match = re.match(r'(?:##\s+|├──\s+|│\s+├──\s+)(\w[\w-]*)/', line)
        if area_match:
            current_area = area_match.group(1)
            area_order += 1
            areas[current_area] = {"order": area_order, "concepts": []}
            continue

        # Concept files like "├── proposition.md # What is a proposition"
        concept_match = re.match(r'(?:├──\s+|│\s+├──\s+|\s+├──\s+)([\w-]+)\.md\s*#\s*(.+)?', line)
        if concept_match and current_area:
            concept_id = concept_match.group(1)
            description = concept_match.group(2) or ""
            areas[current_area]["concepts"].append({
                "id": concept_id,
                "name": concept_id.replace('-', ' ').title(),
                "description": description.strip() if description else "",
            })

    # Build concepts list with basic dependencies
    # Foundations have no prerequisites; everything else depends on foundations
    foundation_ids = set()
    if "foundations" in areas:
        for c in areas["foundations"]["concepts"]:
            foundation_ids.add(c["id"])

    for area_id, area_data in areas.items():
        for c in area_data["concepts"]:
            prereqs = []
            if area_id != "foundations" and foundation_ids:
                # Basic dependency: all non-foundations need some foundations
                # This is a simplified version — manual refinement needed
                prereqs = ["set", "function"] if "set" in foundation_ids and "function" in foundation_ids else []

            concepts.append({
                "id": c["id"],
                "name": c["name"],
                "area": area_id,
                "prerequisites": prereqs,
                "unlocks": [],
                "related": [],
                "status": "not_started",
                "author": None,
                "quality_score": 0,
                "page_exists": False,
                "last_reviewed": None,
                "difficulty": 1,
            })

    # Build areas list
    areas_list = [{"id": k, "name": k.replace('-', ' ').title(), "order": v["order"]} for k, v in sorted(areas.items(), key=lambda x: x[1]["order"])]

    return {
        "version": "1.0.0",
        "bootstrap_concepts": ["proposition", "set"],
        "concepts": concepts,
        "areas": areas_list,
        "notation_registry": {}
    }


def main():
    if not PLAN_FILE.exists():
        print(f"{PLAN_FILE} not found")
        sys.exit(1)

    data = parse_plan()

    with open(CONCEPTS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Generated {CONCEPTS_FILE} with {len(data['concepts'])} concepts across {len(data['areas'])} areas")
    print("Next: Review and refine prerequisites, then run: python scripts/lemma_pipeline.py --update")


if __name__ == "__main__":
    main()
