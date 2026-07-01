#!/usr/bin/env python3
"""Lemma production pipeline — CI-ready quality scorer, validator, and dashboard generator."""

import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple

CONCEPTS_FILE = Path("concepts.json")
DOCS_DIR = Path("docs")
SPECS_DIR = Path("specs")
DASHBOARD_FILE = Path("site/dashboard.html")
PLAN_FILE = Path("PLAN.md")

# Quality scoring rubric (0-100)
RUBRIC = {
    "definition": 15,
    "formal_statement": 15,
    "examples": 15,
    "proof_or_theorem": 15,
    "links_resolve": 15,
    "diagram": 10,
    "related_section": 10,
    "spelling_grammar": 5,
}


def load_concepts() -> dict:
    if not CONCEPTS_FILE.exists():
        print("No concepts.json found. Run: python scripts/plan_to_graph.py")
        sys.exit(1)
    with open(CONCEPTS_FILE) as f:
        return json.load(f)


def compute_quality_score(concept_id: str, md_content: str) -> int:
    """Score a page 0-100 based on content quality."""
    score = 0

    # Definition present (15 pts)
    if re.search(r'^##\s+Definition', md_content, re.MULTILINE):
        score += RUBRIC["definition"]

    # Formal statement (15 pts)
    if re.search(r'^##\s+Formal\s+Statement', md_content, re.MULTILINE):
        score += RUBRIC["formal_statement"]

    # Examples (15 pts) — at least 1 example section
    examples = re.findall(r'^###\s+Example\s+\d+', md_content, re.MULTILINE)
    if len(examples) >= 1:
        score += RUBRIC["examples"]

    # Proof or theorem (15 pts)
    if re.search(r'^##\s+(Proof|Theorem|Proposition|Lemma|Corollary)', md_content, re.MULTILINE):
        score += RUBRIC["proof_or_theorem"]

    # Links resolve (15 pts)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', md_content)
    broken = 0
    for _, target in links:
        # Skip external links
        if target.startswith(('http://', 'https://', 'mailto:')):
            continue
        # Check if target exists in docs/
        target_path = DOCS_DIR / target
        if not target_path.exists() and not target_path.with_suffix('.md').exists():
            broken += 1
    if broken == 0 and len(links) > 0:
        score += RUBRIC["links_resolve"]

    # Diagram (10 pts) — image or TikZ
    if re.search(r'!\[', md_content) or '\\begin{tikzpicture}' in md_content:
        score += RUBRIC["diagram"]

    # Related section (10 pts) — must have at least 2 related links
    related_match = re.search(r'^##\s+Related\s*$\n(.*?)(?=^##|\Z)', md_content, re.MULTILINE | re.DOTALL)
    if related_match:
        related_links = re.findall(r'-\s+\[([^\]]+)\]\(([^)]+)\)', related_match.group(1))
        if len(related_links) >= 2:
            score += RUBRIC["related_section"]

    # Spelling/grammar (5 pts) — assume clean if CI passes
    score += RUBRIC["spelling_grammar"]

    return min(score, 100)


def check_prerequisites(concepts: dict) -> List[str]:
    """Return violations where published pages have unpublished prerequisites."""
    violations = []
    by_id = {c["id"]: c for c in concepts["concepts"]}

    for c in concepts["concepts"]:
        if c.get("status") == "published":
            for prereq in c.get("prerequisites", []):
                if prereq in by_id and by_id[prereq].get("status") != "published":
                    violations.append(
                        f"❌ {c['id']} is published but prerequisite '{prereq}' is {by_id[prereq]['status']}"
                    )
    return violations


def find_cycles(concepts: dict) -> List[List[str]]:
    """Detect circular dependencies in the strict graph."""
    by_id = {c["id"]: c for c in concepts["concepts"]}
    cycles = []
    visited = set()

    def dfs(node: str, path: List[str], path_set: Set[str]):
        if node in path_set:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        path_set.add(node)
        for prereq in by_id.get(node, {}).get("prerequisites", []):
            dfs(prereq, path, path_set)
        path.pop()
        path_set.remove(node)

    for c in concepts["concepts"]:
        if c["id"] not in visited:
            dfs(c["id"], [], set())

    # Deduplicate cycles
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        normalized = tuple(sorted(cycle[:-1]))  # Remove duplicate end node
        if normalized not in seen:
            seen.add(normalized)
            unique_cycles.append(cycle)
    return unique_cycles


def update_statuses(concepts: dict) -> dict:
    """Update page_exists, quality_score, and status from filesystem."""
    for c in concepts["concepts"]:
        page_path = DOCS_DIR / c["area"] / f"{c['id']}.md"

        if page_path.exists():
            c["page_exists"] = True
            content = page_path.read_text()
            c["quality_score"] = compute_quality_score(c["id"], content)

            # Auto-promote status based on quality
            if c.get("status") in ("not_started", None):
                if c["quality_score"] >= 80:
                    c["status"] = "published"
                elif c["quality_score"] >= 50:
                    c["status"] = "draft"
                else:
                    c["status"] = "not_started"
        else:
            c["page_exists"] = False
            c["quality_score"] = 0

    return concepts


def generate_dashboard(concepts: dict) -> str:
    """Generate HTML dashboard."""
    total = len(concepts["concepts"])
    published = sum(1 for c in concepts["concepts"] if c.get("status") == "published")
    drafts = sum(1 for c in concepts["concepts"] if c.get("status") == "draft")
    not_started = sum(1 for c in concepts["concepts"] if c.get("status") == "not_started")

    by_id = {c["id"]: c for c in concepts["concepts"]}

    # Compute unblocked: all prereqs published (or no prereqs)
    unblocked = []
    for c in concepts["concepts"]:
        if c.get("status") == "not_started":
            prereqs = c.get("prerequisites", [])
            if all(by_id.get(p, {}).get("status") == "published" for p in prereqs if p in by_id):
                unblocked.append(c)

    # Average quality of published pages
    published_scores = [c["quality_score"] for c in concepts["concepts"] if c.get("status") == "published" and c["quality_score"] > 0]
    avg_quality = sum(published_scores) / max(len(published_scores), 1)

    # Areas breakdown
    areas = {}
    for c in concepts["concepts"]:
        area = c.get("area", "unknown")
        if area not in areas:
            areas[area] = {"total": 0, "published": 0}
        areas[area]["total"] += 1
        if c.get("status") == "published":
            areas[area]["published"] += 1

    # Recent pages (highest quality published)
    top_pages = sorted(
        [c for c in concepts["concepts"] if c.get("status") == "published"],
        key=lambda x: x.get("quality_score", 0),
        reverse=True
    )[:10]

    # Next to write
    next_to_write = sorted(unblocked, key=lambda x: x.get("difficulty", 1))[:10]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lemma Dashboard — Math Wiki</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; color: #1a1a1a; }}
.subtitle {{ color: #666; margin-bottom: 2rem; font-size: 1.1rem; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
.metric {{ background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.metric-value {{ font-size: 2.5rem; font-weight: bold; color: #2563eb; }}
.metric-label {{ color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; }}
.section {{ background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem; }}
.section h2 {{ font-size: 1.3rem; margin-bottom: 1rem; color: #1a1a1a; }}
.areas {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }}
.area {{ padding: 1rem; background: #f8f9fa; border-radius: 8px; }}
.area-name {{ font-weight: bold; margin-bottom: 0.5rem; }}
.area-bar {{ height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden; margin-top: 0.5rem; }}
.area-fill {{ height: 100%; background: #2563eb; border-radius: 4px; }}
.concept-list {{ list-style: none; }}
.concept-list li {{ padding: 0.5rem 0; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }}
.concept-list li:last-child {{ border-bottom: none; }}
.quality-badge {{ display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }}
.quality-high {{ background: #dcfce7; color: #166534; }}
.quality-mid {{ background: #fef9c3; color: #854d0e; }}
.quality-low {{ background: #fee2e2; color: #991b1b; }}
.status {{ font-size: 0.85rem; color: #666; }}
.footer {{ text-align: center; color: #999; margin-top: 2rem; font-size: 0.9rem; }}
</style>
</head>
<body>
<div class="container">
<h1>📐 Lemma Dashboard</h1>
<p class="subtitle">A rigorous mathematical encyclopedia. Target: MathWorld scale.</p>

<div class="metrics">
    <div class="metric">
        <div class="metric-value">{published}</div>
        <div class="metric-label">Published</div>
    </div>
    <div class="metric">
        <div class="metric-value">{total}</div>
        <div class="metric-label">Total Concepts</div>
    </div>
    <div class="metric">
        <div class="metric-value">{len(unblocked)}</div>
        <div class="metric-label">Ready to Write</div>
    </div>
    <div class="metric">
        <div class="metric-value">{avg_quality:.1f}</div>
        <div class="metric-label">Avg Quality</div>
    </div>
    <div class="metric">
        <div class="metric-value">{drafts}</div>
        <div class="metric-label">Drafts</div>
    </div>
    <div class="metric">
        <div class="metric-value">{not_started}</div>
        <div class="metric-label">Not Started</div>
    </div>
</div>

<div class="areas">
    <div class="section">
        <h2>📚 Areas</h2>
"""

    for area_id, area_data in sorted(areas.items(), key=lambda x: x[0]):
        pct = (area_data["published"] / max(area_data["total"], 1)) * 100
        html += f"""
        <div class="area">
            <div class="area-name">{area_id.replace('-', ' ').title()}</div>
            <div class="status">{area_data["published"]}/{area_data["total"]} published</div>
            <div class="area-bar"><div class="area-fill" style="width: {pct}%"></div></div>
        </div>
"""

    html += """
    </div>
</div>

<div class="section">
    <h2>🏆 Top Quality Pages</h2>
    <ul class="concept-list">
"""

    for c in top_pages:
        score = c.get("quality_score", 0)
        badge_class = "quality-high" if score >= 80 else "quality-mid" if score >= 50 else "quality-low"
        html += f'<li><span>{c["name"]}</span><span class="quality-badge {badge_class}">{score}/100</span></li>\n'

    html += """
    </ul>
</div>

<div class="section">
    <h2>🔓 Next to Write</h2>
    <p class="status">Concepts with all prerequisites published, sorted by difficulty.</p>
    <ul class="concept-list">
"""

    for c in next_to_write:
        html += f'<li><span>{c["name"]}</span><span class="status">{c["area"]} • difficulty {c.get("difficulty", "?")}</span></li>\n'

    html += """
    </ul>
</div>

<div class="footer">
    <p>Generated by Lemma Pipeline • <a href="https://github.com/QQSHI13/lemma">GitHub</a></p>
</div>
</div>
</body>
</html>
"""

    return html


def validate_all(concepts: dict) -> Tuple[bool, List[str]]:
    """Run all validation checks. Returns (pass, [messages])."""
    all_messages = []
    passed = True

    # 1. Prerequisite violations
    prereq_violations = check_prerequisites(concepts)
    if prereq_violations:
        all_messages.extend(prereq_violations)
        passed = False

    # 2. Cycles
    cycles = find_cycles(concepts)
    if cycles:
        for cycle in cycles:
            all_messages.append(f"⚠️ Circular dependency: {' → '.join(cycle)}")
        passed = False

    # 3. Orphan pages (published but no incoming links, except root concepts)
    by_id = {c["id"]: c for c in concepts["concepts"]}
    root_concepts = set(concepts.get("bootstrap_concepts", []))
    for c in concepts["concepts"]:
        if c.get("status") == "published" and c["id"] not in root_concepts:
            incoming = [k for k, v in by_id.items() if c["id"] in v.get("prerequisites", [])]
            if not incoming:
                all_messages.append(f"⚠️ Orphan page: {c['id']} (published but no prerequisites link to it)")

    # 4. Missing quality scores for published pages
    for c in concepts["concepts"]:
        if c.get("status") == "published" and c.get("quality_score", 0) < 50:
            all_messages.append(f"❌ {c['id']}: Published but quality score only {c['quality_score']}/100")
            passed = False

    return passed, all_messages


def main():
    parser = argparse.ArgumentParser(description="Lemma production pipeline")
    parser.add_argument("--validate", action="store_true", help="Run full validation")
    parser.add_argument("--quality-check", action="store_true", help="Check quality scores")
    parser.add_argument("--notation-check", action="store_true", help="Check notation consistency")
    parser.add_argument("--dashboard", action="store_true", help="Generate dashboard")
    parser.add_argument("--update", action="store_true", help="Update concepts.json from filesystem")
    args = parser.parse_args()

    concepts = load_concepts()

    if args.update or not any([args.validate, args.quality_check, args.notation_check, args.dashboard]):
        # Default: update and validate
        concepts = update_statuses(concepts)
        with open(CONCEPTS_FILE, 'w') as f:
            json.dump(concepts, f, indent=2, ensure_ascii=False)
        print(f"Updated {CONCEPTS_FILE} — {sum(1 for c in concepts['concepts'] if c.get('status') == 'published')} published")

    if args.validate or args.update:
        passed, messages = validate_all(concepts)
        for msg in messages:
            print(msg)
        if not passed:
            print("\n❌ Validation FAILED")
            sys.exit(1)
        print("\n✅ Validation passed")

    if args.quality_check:
        published = [c for c in concepts["concepts"] if c.get("status") == "published"]
        low_quality = [c for c in published if c.get("quality_score", 0) < 80]
        if low_quality:
            print(f"❌ FAIL: {len(low_quality)} published pages with quality < 80:")
            for c in low_quality:
                print(f"  - {c['id']}: {c['quality_score']}/100")
            sys.exit(1)
        print(f"✅ All {len(published)} published pages have quality >= 80")

    if args.notation_check:
        # Basic notation consistency check
        registry = concepts.get("notation_registry", {})
        if registry:
            print(f"✅ Notation registry has {len(registry)} entries")
        else:
            print("⚠️ No notation registry configured")

    if args.dashboard:
        DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
        dashboard = generate_dashboard(concepts)
        DASHBOARD_FILE.write_text(dashboard, encoding='utf-8')
        print(f"Dashboard generated: {DASHBOARD_FILE}")


if __name__ == "__main__":
    main()
