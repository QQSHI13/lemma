#!/usr/bin/env python3
"""Check all links and frontmatter in Lemma docs.

Usage:
    python scripts/check_links.py           # Lenient mode (default)
    python scripts/check_links.py --strict  # Fail on any broken link

Lenient mode only fails on broken links in EXISTING content pages,
not on index pages linking to not-yet-written topics.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

DOCS_DIR = Path("docs")
CONCEPTS_FILE = Path("concepts.json")

# Files that are allowed to have broken links (table of contents / index pages)
INDEX_FILES = {"index.md", "README.md"}

# Required frontmatter fields
REQUIRED_FIELDS = {"title", "area", "difficulty", "tags"}

# Valid areas from concepts.json (populated at runtime)
VALID_AREAS = set()


def load_concepts():
    import json
    with open(CONCEPTS_FILE) as f:
        data = json.load(f)
    return {c["id"]: c for c in data["concepts"]}


def extract_frontmatter(content: str) -> tuple[dict | None, str]:
    """Extract YAML frontmatter from markdown content.
    
    Returns (frontmatter_dict, body) or (None, content) if no frontmatter.
    """
    if not content.startswith("---\n"):
        return None, content
    
    end = content.find("\n---\n", 4)
    if end == -1:
        return None, content
    
    fm_text = content[4:end]
    body = content[end + 5:]
    
    if yaml is None:
        # Fallback: basic parsing for title, area, difficulty, tags, prerequisites, related
        fm = {}
        current_key = None
        current_list = None
        
        for line in fm_text.strip().split("\n"):
            # List item
            if line.strip().startswith("- "):
                if current_key:
                    value = line.strip()[2:].strip()
                    if current_key not in fm:
                        fm[current_key] = []
                    fm[current_key].append(value)
                continue
            
            # Key-value pair
            match = re.match(r"^(\w+):\s*(.*)$", line)
            if match:
                key, value = match.group(1), match.group(2).strip()
                current_key = key
                
                if value == "":
                    fm[key] = []  # Will be populated by list items
                elif value.isdigit():
                    fm[key] = int(value)
                else:
                    fm[key] = value.strip("\"'")
        
        return fm, body
    else:
        try:
            fm = yaml.safe_load(fm_text)
            return fm if isinstance(fm, dict) else None, body
        except Exception:
            return None, body


def validate_frontmatter(md_file: Path, content: str, concepts: dict) -> list[str]:
    """Validate YAML frontmatter. Returns list of violation messages."""
    violations = []
    rel_path = md_file.relative_to(DOCS_DIR)
    
    fm, body = extract_frontmatter(content)
    
    if fm is None:
        violations.append(f"❌ {rel_path}: Missing or malformed YAML frontmatter")
        return violations
    
    # Check required fields
    missing = REQUIRED_FIELDS - set(fm.keys())
    if missing:
        violations.append(f"❌ {rel_path}: Missing required frontmatter fields: {', '.join(sorted(missing))}")
    
    # Check title is string and non-empty
    title = fm.get("title")
    if title is not None:
        if not isinstance(title, str) or not title.strip():
            violations.append(f"❌ {rel_path}: 'title' must be a non-empty string")
    
    # Check area is string and matches directory
    area = fm.get("area")
    if area is not None:
        if not isinstance(area, str):
            violations.append(f"❌ {rel_path}: 'area' must be a string")
        else:
            # Check area matches directory (skip root index.md)
            expected_area = md_file.parent.name
            if area != expected_area and expected_area != 'docs':
                violations.append(f"❌ {rel_path}: 'area' is '{area}' but file is in '{expected_area}/'")
            
            # Check area is known (skip special areas like 'home')
            if VALID_AREAS and area not in VALID_AREAS and area != 'home':
                violations.append(f"⚠️  {rel_path}: 'area' '{area}' not found in concepts.json")
    
    # Check difficulty is int
    difficulty = fm.get("difficulty")
    if difficulty is not None:
        if not isinstance(difficulty, int) or isinstance(difficulty, bool):
            violations.append(f"❌ {rel_path}: 'difficulty' must be an integer")
        elif difficulty < 1 or difficulty > 5:
            violations.append(f"⚠️  {rel_path}: 'difficulty' {difficulty} is outside typical range 1-5")
    
    # Check tags is list
    tags = fm.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            violations.append(f"❌ {rel_path}: 'tags' must be a list")
        elif len(tags) == 0:
            violations.append(f"⚠️  {rel_path}: 'tags' is empty")
    
    # Check prerequisites is list of strings
    prereqs = fm.get("prerequisites")
    if prereqs is not None:
        if not isinstance(prereqs, list):
            violations.append(f"❌ {rel_path}: 'prerequisites' must be a list")
        else:
            for p in prereqs:
                if not isinstance(p, str):
                    violations.append(f"❌ {rel_path}: prerequisite '{p}' must be a string")
                elif p not in concepts:
                    violations.append(f"⚠️  {rel_path}: prerequisite '{p}' not found in concepts.json")
    
    # Check related is list of strings
    related = fm.get("related")
    if related is not None:
        if not isinstance(related, list):
            violations.append(f"❌ {rel_path}: 'related' must be a list")
        else:
            for r in related:
                if not isinstance(r, str):
                    violations.append(f"❌ {rel_path}: related item '{r}' must be a string")
                elif r not in concepts:
                    violations.append(f"⚠️  {rel_path}: related item '{r}' not found in concepts.json")
    
    # Check for unknown fields
    known_fields = {"title", "area", "difficulty", "tags", "prerequisites", "related", "status", "quality_score"}
    unknown = set(fm.keys()) - known_fields
    if unknown:
        violations.append(f"⚠️  {rel_path}: Unknown frontmatter fields: {', '.join(sorted(unknown))}")
    
    return violations


def resolve_link(target: str, from_file: Path) -> Path | None:
    """Resolve a markdown link target relative to the source file."""
    if target.startswith('/'):
        return DOCS_DIR / target.lstrip('/')
    else:
        return from_file.parent / target


def check_all(strict: bool = False):
    if not CONCEPTS_FILE.exists():
        print("No concepts.json found. Skipping check.")
        sys.exit(0)

    concepts = load_concepts()
    
    # Build valid areas set
    global VALID_AREAS
    VALID_AREAS = {c.get("area", "") for c in concepts.values()}
    
    # Build set of known concept IDs and their page paths
    known_concept_ids = set(concepts.keys())

    link_violations = []
    link_warnings = []
    fm_violations = []
    fm_warnings = []
    
    stats = {"total_links": 0, "broken": 0, "external": 0, "pages_checked": 0}

    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text()
        rel_path = md_file.relative_to(DOCS_DIR)
        is_index = md_file.name in INDEX_FILES
        stats["pages_checked"] += 1

        # Validate frontmatter
        fm_issues = validate_frontmatter(md_file, content, concepts)
        for issue in fm_issues:
            if issue.startswith("❌"):
                fm_violations.append(issue)
            else:
                fm_warnings.append(issue)

        # Skip link checks for index pages in lenient mode (they link to future content)
        if is_index and not strict:
            continue

        # Check standard markdown links
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, target in md_links:
            stats["total_links"] += 1
            if target.startswith(('http://', 'https://', 'mailto:', '#', 'data:')):
                stats["external"] += 1
                continue

            resolved = resolve_link(target, md_file)
            if resolved is None:
                continue

            exists = resolved.exists() or resolved.with_suffix('.md').exists()

            if not exists:
                stats["broken"] += 1
                msg = f"{rel_path}: Broken link [{text}]({target})"
                target_stem = Path(target).stem
                is_planned = target_stem in known_concept_ids

                if is_planned and not strict:
                    link_warnings.append(f"⚠️  {msg} (planned concept)")
                else:
                    link_violations.append(f"❌ {msg}")

        # Check wikilinks (skip plugin-specific syntax)
        wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        for link in wikilinks:
            if link.startswith(('ref:', 'thm:', 'eq:', 'def:', 'lem:', 'cor:')):
                continue
            stats["total_links"] += 1
            link_id = link.split('#')[0]
            if link_id not in concepts:
                stats["broken"] += 1
                link_violations.append(f"❌ {rel_path}: Broken wikilink [[{link_id}]]")

    # Report results
    print(f"Checked {stats['pages_checked']} pages, {stats['total_links']} links ({stats['broken']} broken, {stats['external']} external)")

    if fm_warnings:
        print(f"\n⚠️  {len(fm_warnings)} frontmatter warnings:")
        for w in fm_warnings:
            print(f"  {w}")

    if link_warnings:
        print(f"\n⚠️  {len(link_warnings)} link warnings:")
        for w in link_warnings[:20]:
            print(f"  {w}")
        if len(link_warnings) > 20:
            print(f"  ... and {len(link_warnings) - 20} more")

    if fm_violations:
        print(f"\n❌ {len(fm_violations)} frontmatter violations:")
        for v in fm_violations:
            print(f"  {v}")

    if link_violations:
        print(f"\n❌ {len(link_violations)} link violations:")
        for v in link_violations:
            print(f"  {v}")

    all_violations = fm_violations + link_violations
    if all_violations:
        print(f"\n❌ Validation FAILED ({len(all_violations)} total violations)")
        sys.exit(1)

    if fm_warnings or link_warnings:
        print("\n✅ Validation passed with warnings")
    else:
        print("\n✅ All checks passed")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Check links and frontmatter in Lemma docs")
    parser.add_argument("--strict", action="store_true", help="Fail on any broken link, even in index pages")
    args = parser.parse_args()

    check_all(strict=args.strict)


if __name__ == "__main__":
    main()
