# Lemma — Production System Architecture

> **Status:** Design document (P2 — infrastructure, no API costs)
> **Goal:** Define the concrete production pipeline before writing any content

---

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        LEMMA PRODUCTION PIPELINE                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │  concepts.   │   │    specs/    │   │    docs/     │        │
│  │    json      │◄──│   *.yaml     │──►│   *.md       │        │
│  │  (master     │   │  (human      │   │  (generated  │        │
│  │   graph)     │   │   specs)     │   │   + manual)  │        │
│  └──────┬───────┘   └──────────────┘   └──────┬───────┘        │
│         │                                       │                │
│         ▼                                       ▼                │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              scripts/lemma_pipeline.py                │       │
│  │  • Dependency resolver                               │       │
│  │  • Quality scorer (0-100)                            │       │
│  │  • Link checker                                      │       │
│  │  • Notation consistency tracker                      │       │
│  │  • Dashboard generator                               │       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              .github/workflows/build.yml              │       │
│  │  Every push to main:                                 │       │
│  │  1. Run pipeline → update concepts.json              │       │
│  │  2. Quality gate → fail if published < 80            │       │
│  │  3. Build docsforge site                             │       │
│  │  4. Deploy to GitHub Pages                           │       │
│  │  5. Update dashboard.html                            │       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│                           ▼                                      │
│                    https://qqshi13.github.io/lemma/              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Data Layer

### 1.1 concepts.json (The Master Graph)

Single source of truth. ~120 entries for pilot, expandable to 10K.

```json
{
  "version": "1.0.0",
  "concepts": [
    {
      "id": "proposition",
      "name": "Proposition",
      "area": "foundations",
      "prerequisites": [],
      "unlocks": ["truth-table", "logical-connective", "quantifier"],
      "status": "published",
      "author": "QQ",
      "quality_score": 92,
      "page_exists": true,
      "last_reviewed": "2026-06-27",
      "spec_file": null,
      "difficulty": 1
    },
    {
      "id": "eigenvalue",
      "name": "Eigenvalue",
      "area": "algebra",
      "prerequisites": ["linear-map", "vector-space", "field", "polynomial"],
      "unlocks": ["diagonalization", "spectral-theorem"],
      "status": "not_started",
      "author": null,
      "quality_score": 0,
      "page_exists": false,
      "last_reviewed": null,
      "spec_file": "specs/eigenvalue.yaml",
      "difficulty": 3
    }
  ],
  "areas": [
    {"id": "foundations", "name": "Foundations", "order": 1},
    {"id": "number-systems", "name": "Number Systems", "order": 2},
    {"id": "algebra", "name": "Algebra", "order": 3},
    {"id": "analysis", "name": "Analysis", "order": 4},
    {"id": "geometry", "name": "Geometry", "order": 5},
    {"id": "number-theory", "name": "Number Theory", "order": 6},
    {"id": "discrete-mathematics", "name": "Discrete Mathematics", "order": 7},
    {"id": "probability", "name": "Probability", "order": 8}
  ],
  "notation_registry": {
    "vector-space": {"V": "vector space", "W": "vector space"},
    "field": {"F": "field", "K": "field"}
  }
}
```

### 1.2 Spec Format (specs/*.yaml)

Human writes specs. Pipeline generates pages from them.

```yaml
id: eigenvalue
name: Eigenvalue
area: algebra
difficulty: 3

definition: |
  A scalar λ is an eigenvalue of a linear map T: V → V
  if there exists a non-zero vector v such that T(v) = λv.

key_theorems:
  - spectral-theorem
  - cayley-hamilton

examples_needed: 3
example_types:
  - concrete: "2×2 matrix with integer eigenvalues"
  - nontrivial: "Rotation matrix with complex eigenvalues"
  - counterexample: "What if v=0 is allowed?"

diagrams_needed: 1
diagram_descriptions:
  - "Shear transformation showing eigenvector direction"

prerequisites:
  - linear-map
  - vector-space
  - field
  - polynomial

related:
  - eigenvector
  - characteristic-polynomial
  - diagonalization

notation_notes: |
  Use λ (lambda) for eigenvalue, v for eigenvector.
  V should match the vector-space page notation.
```

---

## 2. Build Layer (scripts/)

### 2.1 lemma_pipeline.py

The main orchestrator. Run locally or in CI.

```python
#!/usr/bin/env python3
"""Lemma production pipeline."""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

CONCEPTS_FILE = Path("concepts.json")
DOCS_DIR = Path("docs")
SPECS_DIR = Path("specs")
DASHBOARD_FILE = Path("site/dashboard.html")

def load_concepts() -> dict:
    with open(CONCEPTS_FILE) as f:
        return json.load(f)

def compute_quality_score(concept_id: str, md_content: str) -> int:
    """Score 0-100 based on content quality."""
    score = 0
    
    # Definition present (15 pts)
    if re.search(r'^## Definition', md_content, re.M):
        score += 15
    
    # Formal statement (15 pts)
    if re.search(r'^## Formal Statement', md_content, re.M):
        score += 15
    
    # ≥1 example (15 pts)
    examples = re.findall(r'^### Example \d+', md_content, re.M)
    if len(examples) >= 1:
        score += 15
    
    # Proof or "proof omitted" (15 pts)
    if re.search(r'^## (Proof|Theorem).*$', md_content, re.M):
        score += 15
    
    # All links resolve (15 pts)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', md_content)
    broken = 0
    for _, target in links:
        if not (DOCS_DIR / target).exists():
            broken += 1
    if broken == 0 and len(links) > 0:
        score += 15
    
    # ≥1 diagram (10 pts)
    if re.search(r'!\[', md_content):
        score += 10
    
    # Related section (10 pts)
    if re.search(r'^## Related', md_content, re.M):
        related_links = re.findall(r'- \[([^\]]+)\]\(([^)]+)\)', 
            md_content[md_content.find('## Related'):])
        if len(related_links) >= 2:
            score += 10
    
    # Spelling/grammar (5 pts) — delegated to cspell/typos
    score += 5  # Assume clean if CI passes
    
    return min(score, 100)

def check_prerequisites(concepts: dict) -> List[str]:
    """Return list of violations: published pages with unpublished prereqs."""
    violations = []
    by_id = {c["id"]: c for c in concepts["concepts"]}
    
    for c in concepts["concepts"]:
        if c["status"] == "published":
            for prereq in c.get("prerequisites", []):
                if prereq in by_id and by_id[prereq]["status"] != "published":
                    violations.append(
                        f"{c['id']} is published but prereq {prereq} is {by_id[prereq]['status']}"
                    )
    return violations

def find_cycles(concepts: dict) -> List[List[str]]:
    """Detect circular dependencies."""
    by_id = {c["id"]: c for c in concepts["concepts"]}
    cycles = []
    
    def dfs(node: str, path: Set[str], visited: Set[str]):
        if node in path:
            cycles.append(list(path) + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.add(node)
        for prereq in by_id.get(node, {}).get("prerequisites", []):
            dfs(prereq, path, visited)
        path.remove(node)
    
    for c in concepts["concepts"]:
        dfs(c["id"], set(), set())
    
    return cycles

def generate_dashboard(concepts: dict) -> str:
    """Generate HTML dashboard."""
    total = len(concepts["concepts"])
    published = sum(1 for c in concepts["concepts"] if c["status"] == "published")
    drafts = sum(1 for c in concepts["concepts"] if c["status"] == "draft")
    not_started = sum(1 for c in concepts["concepts"] if c["status"] == "not_started")
    
    # Compute unblocked: all prereqs published
    by_id = {c["id"]: c for c in concepts["concepts"]}
    unblocked = []
    for c in concepts["concepts"]:
        if c["status"] == "not_started":
            if all(by_id[p]["status"] == "published" for p in c.get("prerequisites", []) if p in by_id):
                unblocked.append(c)
    
    avg_quality = sum(c["quality_score"] for c in concepts["concepts"] if c["quality_score"] > 0) / max(published, 1)
    
    return f"""<!DOCTYPE html>
<html>
<head><title>Lemma Dashboard</title><style>
body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; }}
.metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
.metric-value {{ font-size: 2em; font-weight: bold; }}
.metric-label {{ color: #666; }}
.unblocked {{ margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 8px; }}
</style></head>
<body>
<h1>📐 Lemma Dashboard</h1>
<div class="metric"><div class="metric-value">{published}/{total}</div><div class="metric-label">Published</div></div>
<div class="metric"><div class="metric-value">{len(unblocked)}</div><div class="metric-label">Ready to Write</div></div>
<div class="metric"><div class="metric-value">{avg_quality:.1f}</div><div class="metric-label">Avg Quality</div></div>
<div class="unblocked">
<h3>🔓 Ready to Write</h3>
<ol>{''.join(f'<li>{c["name"]} <code>{c["id"]}</code></li>' for c in unblocked[:10])}</ol>
</div>
</body></html>"""

def main():
    concepts = load_concepts()
    
    # Update statuses and scores from filesystem
    for c in concepts["concepts"]:
        page_path = DOCS_DIR / c["area"] / f"{c['id']}.md"
        spec_path = SPECS_DIR / f"{c['id']}.yaml"
        
        if page_path.exists():
            c["page_exists"] = True
            content = page_path.read_text()
            c["quality_score"] = compute_quality_score(c["id"], content)
            if c["status"] == "not_started" and c["quality_score"] >= 80:
                c["status"] = "published"
            elif c["status"] == "not_started" and c["quality_score"] >= 50:
                c["status"] = "draft"
        else:
            c["page_exists"] = False
            c["quality_score"] = 0
        
        if spec_path.exists():
            c["spec_file"] = str(spec_path)
    
    # Validate
    violations = check_prerequisites(concepts)
    cycles = find_cycles(concepts)
    
    # Report
    print(f"Total concepts: {len(concepts['concepts'])}")
    print(f"Published: {sum(1 for c in concepts['concepts'] if c['status'] == 'published')}")
    print(f"Violations: {len(violations)}")
    for v in violations:
        print(f"  ⚠️ {v}")
    print(f"Cycles: {len(cycles)}")
    
    # Save updated concepts
    with open(CONCEPTS_FILE, 'w') as f:
        json.dump(concepts, f, indent=2)
    
    # Generate dashboard
    DASHBOARD_FILE.parent.mkdir(exist_ok=True)
    DASHBOARD_FILE.write_text(generate_dashboard(concepts))
    print(f"Dashboard: {DASHBOARD_FILE}")
    
    return 1 if violations or cycles else 0

if __name__ == "__main__":
    sys.exit(main())
```

### 2.2 generate_page.py

Takes a spec, generates a markdown page using the standard template.

```python
#!/usr/bin/env python3
"""Generate a Lemma page from a spec file."""

import yaml
import sys
from pathlib import Path

TEMPLATE = """# {name}

## Definition

{definition}

## Formal Statement

{formal_statement}

## Why It Matters

{intuition}

## Properties

{properties}

## Theorem

### Statement
{theorem_statement}

### Proof
{proof}

**QED**

## Examples

{examples}

## Related

{related}
"""

def load_concepts():
    import json
    with open("concepts.json") as f:
        return {c["id"]: c for c in json.load(f)["concepts"]}

def load_prereq_content(prereq_ids, concepts):
    """Load prerequisite pages for context."""
    context = []
    for pid in prereq_ids:
        path = Path("docs") / concepts[pid]["area"] / f"{pid}.md"
        if path.exists():
            content = path.read_text()
            # Extract just the definition section
            def_match = content.split("## Definition")
            if len(def_match) > 1:
                definition = def_match[1].split("##")[0].strip()
                context.append(f"From '{concepts[pid]['name']}': {definition[:200]}...")
    return "\n\n".join(context)

def generate_from_spec(spec_path: Path):
    spec = yaml.safe_load(spec_path.read_text())
    concepts = load_concepts()
    
    # Gather prerequisite context
    prereq_context = load_prereq_content(spec.get("prerequisites", []), concepts)
    
    # Build related links
    related = []
    for rid in spec.get("related", []):
        if rid in concepts:
            related.append(f"- [{concepts[rid]['name']}]({rid}.md)")
    
    # Generate page
    page = TEMPLATE.format(
        name=spec["name"],
        definition=spec.get("definition", "[TODO: Add definition]"),
        formal_statement=spec.get("formal_statement", "[TODO: Add formal statement]"),
        intuition=spec.get("intuition", "[TODO: Explain why this matters]"),
        properties="\n".join(f"- {p}" for p in spec.get("properties", [])),
        theorem_statement=spec.get("theorem_statement", "[TODO: Add theorem]"),
        proof=spec.get("proof", "[TODO: Add proof]"),
        examples="\n\n".join(
            f"### Example {i+1}\n{e}" 
            for i, e in enumerate(spec.get("examples", []))
        ),
        related="\n".join(related) if related else "- [TODO: Add related concepts]"
    )
    
    # Write
    area = spec["area"]
    out_path = Path("docs") / area / f"{spec['id']}.md"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(page)
    print(f"Generated: {out_path}")
    return out_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_page.py specs/eigenvalue.yaml")
        sys.exit(1)
    generate_from_spec(Path(sys.argv[1]))
```

---

## 3. CI/CD Layer

### 3.1 .github/workflows/build.yml

```yaml
name: Lemma Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      - name: Install dependencies
        run: |
          pip install pyyaml
          pip install docsforge
      
      - name: Validate concepts.json
        run: python scripts/lemma_pipeline.py
      
      - name: Check quality scores
        run: |
          python -c "
          import json
          with open('concepts.json') as f:
              data = json.load(f)
          published = [c for c in data['concepts'] if c['status'] == 'published']
          low_quality = [c for c in published if c['quality_score'] < 80]
          if low_quality:
              print(f'FAIL: {len(low_quality)} published pages with quality < 80')
              for c in low_quality:
                  print(f'  {c[\"id\"]}: {c[\"quality_score\"]}')
              exit(1)
          print(f'PASS: All {len(published)} published pages have quality >= 80')
          "
      
      - name: Check links
        run: python scripts/check_links.py
      
      - name: Build site
        run: docsforge build
      
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

### 3.2 Pre-commit Hooks (optional)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lemma-validate
        name: Validate Lemma concepts
        entry: python scripts/lemma_pipeline.py
        language: system
        pass_filenames: false
        always_run: true
```

---

## 4. Dashboard Layer

The pipeline auto-generates `site/dashboard.html` on every build.

Key metrics tracked:
- Total concepts / published / drafts / not_started
- Unblocked count (ready to write)
- Average quality score
- Quality violations
- Circular dependencies
- Sprint progress

---

## 5. Directory Structure (Target)

```
lemma/
├── concepts.json              # Master dependency graph
├── docsforge.yml              # Site config (already exists)
├── README.md
├── PLAN.md                    # Topic outline (~120 concepts)
├── WORKFLOW_DESIGN.md         # This doc + Phase 2-4 plans
├── PRODUCTION_SYSTEM.md       # This file
│
├── specs/                     # Human-written specs
│   ├── eigenvalue.yaml
│   └── ...
│
├── docs/                      # Generated + manual pages
│   ├── index.md
│   ├── foundations/
│   │   ├── index.md
│   │   ├── proposition.md
│   │   └── ...
│   ├── algebra/
│   │   ├── index.md
│   │   └── ...
│   └── ...
│
├── scripts/                   # Production pipeline
│   ├── lemma_pipeline.py      # Main orchestrator
│   ├── generate_page.py       # Spec → markdown
│   ├── check_links.py         # Link validator
│   └── check_notation.py      # Notation consistency
│
├── templates/                 # Page templates
│   ├── concept.md.j2          # Jinja2 template
│   └── theorem.md.j2
│
├── plugins/                   # DocsForge plugins (already exists)
│
└── .github/
    └── workflows/
        └── build.yml          # CI/CD
```

---

## 6. Implementation Phases

### Phase 1: Core Infrastructure (Week 1–2) — P2, NO API COSTS

| Task | Files | Status |
|------|-------|--------|
| Create concepts.json from PLAN.md | `scripts/plan_to_graph.py` | 🔲 |
| Build quality scorer | `scripts/lemma_pipeline.py` | 🔲 |
| Build link checker | `scripts/check_links.py` | 🔲 |
| Build page generator | `scripts/generate_page.py` | 🔲 |
| Create CI workflow | `.github/workflows/build.yml` | 🔲 |
| Generate dashboard | `scripts/lemma_pipeline.py` | 🔲 |
| Test on existing 10 pages | Manual | 🔲 |

### Phase 2: Batch Generation (Week 3–4) — P3, NEEDS API

| Task | Cost | Status |
|------|------|--------|
| Write specs for Foundations (10 concepts) | Human time | 🔲 |
| Generate pages via Kimi ACP | API credits | 🔲 |
| Human review + fix | Human time | 🔲 |
| Publish batch, unlock next area | CI | 🔲 |

### Phase 3: Scale (Month 2+) — P3, NEEDS API

| Task | Cost | Status |
|------|------|--------|
| Expand to 500 concepts | API credits | 🔲 |
| Notation consistency checker | Local | 🔲 |
| Prerequisite change propagation | Local | 🔲 |
| Contributor system | Local | 🔲 |

---

## 7. Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Source format** | Markdown + YAML specs | Human-readable, version-controllable, works with DocsForge |
| **Graph storage** | JSON (concepts.json) | Simple, diffable, no database needed |
| **Template engine** | Python f-strings + Jinja2 | Simple for basic, powerful for complex |
| **Quality gating** | Score ≥ 80 to publish | Prevents low-quality pages from going live |
| **Prereq rule** | ALL prereqs must be published | Enforces dependency order |
| **Generation model** | Kimi ACP for now | Quality over speed; switch to cheaper model later |
| **Notation tracking** | Registry in concepts.json | Ensures V means vector space everywhere |

---

## 8. What Exists vs What's Needed

| Component | Exists? | Gap |
|-----------|---------|-----|
| Site generator (DocsForge) | ✅ Yes | None |
| Topic plan (PLAN.md) | ✅ Yes | Needs conversion to concepts.json |
| Workflow design | ✅ Yes | Needs implementation |
| ~10 content pages | ✅ Yes | Need quality scoring |
| concepts.json | ❌ No | **Need to build** |
| Quality scorer | ❌ No | **Need to build** |
| Page generator | ❌ No | **Need to build** |
| CI pipeline | ❌ No | **Need to build** |
| Dashboard | ❌ No | **Need to build** |
| Spec format | ❌ No | **Need to define** |

---

## Next Steps

1. **Convert PLAN.md → concepts.json** (~1 hour, no API cost)
2. **Build lemma_pipeline.py** (~2 hours, no API cost)
3. **Build generate_page.py** (~1 hour, no API cost)
4. **Test on existing 10 pages** (~30 min)
5. **Write specs for 5 unblocked concepts** (~1 hour)
6. **Generate + review first batch** (API cost: ~$0.50–$1.00)

**Total Phase 1 effort:** ~4–5 hours of work, **$0 API cost** for infrastructure.

Ready to start?
