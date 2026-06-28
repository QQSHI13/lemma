# Lemma — Production Workflow Design

## Scale Reality Check

| Wiki | Pages | Contributors | Age |
|------|-------|--------------|-----|
| Wikipedia (Math) | ~40,000 | Millions | 24 years |
| Wolfram MathWorld | ~13,000 | ~20 core | 20+ years |
| nLab | ~15,000 | ~50 active | 15+ years |
| ProofWiki | ~20,000 | ~30 active | 15+ years |
| **Lemma (target)** | **5,000–10,000** | **Starts with 1** | **Year 1** |

At MathWorld scale, writing every page by hand is impossible. The workflow must be **AI-assisted, human-curated**.

---

## The Core Problem

Math is a **dependency graph**. Page 5,000 assumes Pages 1–4,999. You can't write "eigenvalue" without "linear map", "vector space", "field", "number", etc.

So the workflow is about **managing the dependency graph** while **producing content at scale**.

---

## Phase 1: Infrastructure (Month 1–2)

### 1.1 Dependency Graph (The Master Map)

```
concepts.json
├── "id": "eigenvalue"
├── "name": "Eigenvalue"
├── "area": "algebra"
├── "prerequisites": ["linear-map", "vector-space", "field", "polynomial"]
├── "unlocks": ["diagonalization", "spectral-theorem", "principal-component-analysis"]
├── "status": "not_started" | "draft" | "review" | "published"
├── "author": null
├── "quality_score": 0.0
└── "page_exists": false
```

- **Source of truth**: `concepts.json` (~10,000 entries for full coverage)
- **Status rules**: A concept can only be written when ALL prerequisites are `published`
- **Unblocked count**: Dashboard shows "127 concepts ready to write"

### 1.2 Page Quality Score

Every page gets a 0–100 score based on:

| Component | Points | Auto-check? |
|-----------|--------|-------------|
| Definition present | 15 | Yes (regex) |
| Formal statement | 15 | Yes (regex) |
| ≥1 example | 15 | Yes (regex) |
| Proof or "proof omitted" | 15 | Yes (regex) |
| All links resolve | 15 | Yes (link check) |
| ≥1 diagram or visual | 10 | Yes (image count) |
| Related section populated | 10 | Yes (regex) |
| Spelling/grammar clean | 5 | Yes (linter) |
| **Total** | **100** | **Mostly** |

Pages with score < 50 are "drafts" (not in nav). Pages with score ≥ 80 are "published".

### 1.3 Build Pipeline

```
Every push to main:
  1. Parse all .md files
  2. Update concept statuses in concepts.json
  3. Check all [[ref:...]] links resolve
  4. Check prerequisite links resolve
  5. Compute quality scores
  6. Generate navigation from published pages only
  7. Build docsforge site
  8. Deploy to GitHub Pages
  9. Update dashboard with: % done, avg quality, top contributors
```

---

## Phase 2: Content Generation (Month 2–12)

### 2.1 The Generation Pipeline

**The key insight**: You don't write pages. You write **page specifications**, then the pipeline generates them.

```
Workflow:

1. PICK: Select an unblocked concept (all prerequisites published)
2. SPEC: Write a spec file:

specs/eigenvalue.yaml:
  id: eigenvalue
  definition: |
    A scalar λ is an eigenvalue of a linear map T: V → V
    if there exists a non-zero vector v such that T(v) = λv.
  key_theorems:
    - spectral-theorem
    - cayley-hamilton
  examples_needed: 3
  diagrams_needed: 1
  difficulty: 2  # 1=easy, 5=research

3. GENERATE: AI pipeline creates the page from the spec
   - Uses prerequisite pages for context
   - Ensures notation consistency
   - Follows the page template exactly

4. HUMAN_REVIEW: You edit and approve
   - Fix any errors
   - Add intuition that AI missed
   - Ensure proofs are correct

5. PUBLISH: Quality score ≥ 80, merge to main
```

### 2.2 AI Generation Prompts

The generator prompt needs to know:
- What the concept is
- How prerequisites defined related terms (for consistency)
- The exact template structure
- The quality standards
- Any special notation conventions used in the wiki

Example prompt fragment:
```
You are writing a page for a rigorous math wiki called "Lemma".
Follow this template exactly: [template]
The prerequisite pages are: [prerequisite content]
Use the same notation as the prerequisites. For example, if 
"vector-space" uses "V" for vector space, use "V" here too.
Include at least 3 examples. One must be numerical/concrete.
One must show a non-trivial case. One must be a counterexample 
if the definition's conditions are relaxed.
```

### 2.3 Batch Processing

Instead of writing one page at a time, you process **areas** in batches:

```
Sprint 1: Foundations (10 concepts)
  → Generate all 10 at once
  → Review all 10
  → Publish all 10
  → This unlocks 35 new concepts

Sprint 2: Number Systems (8 concepts)
  → Now possible because Foundations is done
  → Generate, review, publish
  → Unlocks 60 new concepts

Sprint 3: Algebra basics (20 concepts)
  → And so on...
```

---

## Phase 3: Quality Assurance (Ongoing)

### 3.1 Automated Tests

```python
# test_lemma.py

def test_all_refs_resolve():
    """Every [[ref:Concept]] links to an existing page."""
    
def test_prerequisites_published():
    """A published page's prerequisites are all published."""
    
def test_quality_scores():
    """All published pages have score >= 80."""
    
def test_notation_consistency():
    """"Vector space" uses V, W consistently."""
    
def test_no_circular_dependencies():
    """Prerequisite graph has no cycles."""
    
def test_template_compliance():
    """Every page has Definition, Examples, Related sections."""
```

### 3.2 Regression Testing

When you update a definition (e.g., change how "vector space" is defined), the pipeline:
1. Finds all pages that depend on it
2. Checks if they still make sense
3. Flags pages that need updating

---

## Phase 4: Collaboration (Month 6+)

### 4.1 Contributor Onboarding

```
New contributor workflow:
1. Pick from "unblocked and unclaimed" list
2. Claim it (prevents duplicate work)
3. Write spec → generate → review → publish
4. Quality score determines contribution credit
```

### 4.2 Review System

- Every page has a "last reviewed" date
- Pages auto-flag for review after 12 months
- Changing a definition triggers review of all dependents

---

## The Dashboard

```
╔══════════════════════════════════════════╗
║  Lemma Dashboard (2026-06-27)            ║
╠══════════════════════════════════════════╣
║  Concepts: 487 / 10,000 (4.9%)           ║
║  Published: 21 (quality ≥ 80)            ║
║  In Review: 3                            ║
║  Drafts: 5 (quality < 80)              ║
║  Unblocked (ready to write): 127         ║
║  Blocked (waiting on prerequisites): 334 ║
║  Avg Quality: 72.4                       ║
║  ─────────────────────────────────────── ║
║  Ready to write:                         ║
║  1. truth-table ← unblocked              ║
║  2. quantifier ← unblocked               ║
║  3. relation ← unblocked                 ║
║  4. function ← unblocked                 ║
║  5. injection ← unblocked                ║
║  ─────────────────────────────────────── ║
║  This sprint: Foundations (10 concepts)  ║
║  Progress: 6/10 done                     ║
╚══════════════════════════════════════════╝
```

---

## What We Build Now vs Later

### Now (Month 1)
- [ ] Dependency graph data structure (`concepts.json`)
- [ ] Quality score calculator
- [ ] Basic dashboard (status, unblocked count)
- [ ] Page generator from spec (AI-assisted)
- [ ] Link checker
- [ ] CI pipeline (build + check + deploy)

### Later (Month 2–3)
- [ ] Batch generation (multiple pages at once)
- [ ] Notation consistency checker
- [ ] Prerequisite change propagation
- [ ] Contributor claim system
- [ ] Search index optimization
- [ ] Cross-link suggestions ("This page mentions X but doesn't link to it")

### Much Later (Month 6+)
- [ ] Automated theorem proof checking (Lean integration?)
- [ ] Interactive diagrams (D3.js, Manim)
- [ ] Multi-language support
- [ ] Community review system

---

## Key Decisions Needed

1. **Source format**: Keep markdown, or move to structured YAML/JSON for machine processing?
2. **AI model**: Kimi ACP sessions? Or cheaper bulk API for generation?
3. **Page ownership**: Do you want to be the only human reviewer, or eventually let others publish?
4. **Scope prioritization**: Should I build the full 10,000-concept graph now, or start with 500 and expand?

This is the difference between a "website with math articles" and a **production-grade mathematical encyclopedia**. What's your priority: get the infrastructure right first, or start generating content with a basic system and iterate?
