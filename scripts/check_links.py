#!/usr/bin/env python3
"""Check all links in Lemma docs — internal wikilinks and cross-references."""

import re
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
CONCEPTS_FILE = Path("concepts.json")


def load_concepts():
    import json
    with open(CONCEPTS_FILE) as f:
        data = json.load(f)
    return {c["id"]: c for c in data["concepts"]}


def check_links():
    if not CONCEPTS_FILE.exists():
        print("No concepts.json found. Skipping link check.")
        sys.exit(0)

    concepts = load_concepts()
    violations = []
    stats = {"total_links": 0, "broken": 0, "external": 0, "missing_pages": []}

    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text()
        rel_path = md_file.relative_to(DOCS_DIR)

        # Check standard markdown links
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, target in md_links:
            stats["total_links"] += 1
            if target.startswith(('http://', 'https://', 'mailto:', '#')):
                stats["external"] += 1
                continue

            # Resolve relative to docs dir
            target_path = DOCS_DIR / target
            if not target_path.exists() and not target_path.with_suffix('.md').exists():
                stats["broken"] += 1
                stats["missing_pages"].append(target)
                violations.append(f"❌ {rel_path}: Broken link [{text}]({target})")

        # Check wikilinks [[concept-id]]
        wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        for link in wikilinks:
            stats["total_links"] += 1
            link_id = link.split('#')[0]
            if link_id not in concepts:
                stats["broken"] += 1
                violations.append(f"❌ {rel_path}: Broken wikilink [[{link_id}]]")

    print(f"Link check complete: {stats['total_links']} links, {stats['broken']} broken, {stats['external']} external")

    for v in violations:
        print(v)

    if violations:
        print(f"\n❌ {len(violations)} link violations found")
        sys.exit(1)
    else:
        print("\n✅ All links valid")


if __name__ == "__main__":
    check_links()
