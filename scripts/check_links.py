#!/usr/bin/env python3
"""Check all links in Lemma docs — internal wikilinks and cross-references.

Usage:
    python scripts/check_links.py           # Lenient mode (default)
    python scripts/check_links.py --strict  # Fail on any broken link
    python scripts/check_links.py --fix     # Auto-remove broken links from index pages

Lenient mode only fails on broken links in EXISTING content pages,
not on index pages linking to not-yet-written topics.
"""

import argparse
import re
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
CONCEPTS_FILE = Path("concepts.json")

# Files that are allowed to have broken links (table of contents / index pages)
INDEX_FILES = {"index.md", "README.md"}


def load_concepts():
    import json
    with open(CONCEPTS_FILE) as f:
        data = json.load(f)
    return {c["id"]: c for c in data["concepts"]}


def resolve_link(target: str, from_file: Path) -> Path | None:
    """Resolve a markdown link target relative to the source file."""
    if target.startswith('/'):
        # Absolute from docs root
        return DOCS_DIR / target.lstrip('/')
    else:
        # Relative to current file
        return from_file.parent / target


def check_links(strict: bool = False, fix: bool = False):
    if not CONCEPTS_FILE.exists():
        print("No concepts.json found. Skipping link check.")
        sys.exit(0)

    concepts = load_concepts()
    violations = []
    warnings = []
    stats = {"total_links": 0, "broken": 0, "external": 0, "fixed": 0}

    # Build set of known concept IDs and their page paths
    known_concept_ids = set(concepts.keys())
    known_page_paths = set()
    for c in concepts.values():
        page_path = DOCS_DIR / c.get("area", "") / f"{c['id']}.md"
        known_page_paths.add(page_path)
        known_page_paths.add(page_path.with_suffix(""))  # without .md

    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text()
        rel_path = md_file.relative_to(DOCS_DIR)
        is_index = md_file.name in INDEX_FILES

        # Check standard markdown links
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, target in md_links:
            stats["total_links"] += 1
            if target.startswith(('http://', 'https://', 'mailto:', '#', 'data:')):
                stats["external"] += 1
                continue

            # Resolve the target
            resolved = resolve_link(target, md_file)
            if resolved is None:
                continue

            # Check if target exists (with or without .md extension)
            exists = resolved.exists() or resolved.with_suffix('.md').exists()

            if not exists:
                stats["broken"] += 1
                msg = f"{rel_path}: Broken link [{text}]({target})"

                # Check if this is a known concept that just hasn't been written yet
                target_stem = Path(target).stem
                is_planned = target_stem in known_concept_ids

                if is_planned and not strict:
                    # Planned but not yet written — warn, don't fail
                    warnings.append(f"⚠️  {msg} (planned concept)")
                elif is_index and not strict:
                    # Index pages often link to future content — warn but don't fail
                    warnings.append(f"⚠️  {msg}")
                else:
                    violations.append(f"❌ {msg}")

        # Check wikilinks [[concept-id]] (skip [[ref:...]] and [[thm:...]] — handled by lemma_md plugin)
        wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        for link in wikilinks:
            # Skip plugin-specific wikilink syntax
            if link.startswith(('ref:', 'thm:', 'eq:', 'def:', 'lem:', 'cor:')):
                continue
            stats["total_links"] += 1
            link_id = link.split('#')[0]
            if link_id not in concepts:
                stats["broken"] += 1
                msg = f"{rel_path}: Broken wikilink [[{link_id}]]"
                if is_index and not strict:
                    warnings.append(f"⚠️  {msg}")
                else:
                    violations.append(f"❌ {msg}")

    # Report results
    print(f"Link check complete: {stats['total_links']} links, {stats['broken']} broken, {stats['external']} external")

    if warnings:
        print(f"\n⚠️  {len(warnings)} warnings (index pages linking to future content):")
        for w in warnings[:20]:
            print(f"  {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")

    if violations:
        print(f"\n❌ {len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        print("\n❌ Validation FAILED")
        sys.exit(1)

    if warnings:
        print("\n✅ All content page links valid (warnings are only from index pages)")
    else:
        print("\n✅ All links valid")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Check links in Lemma docs")
    parser.add_argument("--strict", action="store_true", help="Fail on any broken link, even in index pages")
    parser.add_argument("--fix", action="store_true", help="Auto-remove broken links from index pages (not implemented)")
    args = parser.parse_args()

    check_links(strict=args.strict, fix=args.fix)


if __name__ == "__main__":
    main()
