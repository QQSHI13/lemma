# Lemma — User-Facing Navigation Design

> **Goal:** A 12-year-old studying algebra should navigate as easily as a PhD researcher.
> **Principle:** The graph exists, but users see paths, not nodes.

---

## The Problem

```
Bad:  "This concept has 47 prerequisites"
Good: "Start here → Learn this → Then this → Now you understand"
```

A dependency graph is **infrastructure**. A learning path is **UX**.

---

## 1. Three User Modes

| Mode | Who | Sees |
|------|-----|------|
| **Explorer** | Curious browser, maybe 12 years old | Visual map, big buttons, "Start here" |
| **Student** | Learning a topic systematically | Guided paths, checkpoints, practice problems |
| **Researcher** | Looking up specific theorem | Full graph, formal proofs, citations |

**Default mode:** Explorer. One click to switch to Student or Researcher.

---

## 2. Page Layout (Per Mode)

### 2.1 Explorer Mode (Default)

```
┌─────────────────────────────────────────────────────┐
│  🔍 Search...    [Explorer ▼]  [Student] [Researcher] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │                                             │   │
│  │     EIGENVALUE                              │   │
│  │                                             │   │
│  │     "Numbers that tell you how much a       │   │
│  │      transformation stretches space"         │   │
│  │                                             │   │
│  │     [Visual: Interactive matrix widget]     │   │
│  │                                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  🎮 Play    │  │  📖 Learn   │  │  🔬 Dive    │ │
│  │  with it    │  │  the path   │  │  deeper     │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  📍 You Are Here                            │   │
│  │                                             │   │
│  │  Linear Map ──► Vector Space ──► [Eigenvalue]│  │
│  │       │              │             │         │   │
│  │       ▼              ▼             ▼         │   │
│  │    Matrix        Field        Eigenvector    │   │
│  │                                             │   │
│  │  [◄ Previous]  [Next ►]  [Related ▼]        │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2.2 Student Mode

```
┌─────────────────────────────────────────────────────┐
│  🔍 Search...    [Explorer] [Student ▼] [Researcher] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📚 Linear Algebra — Module 3 of 12                 │
│  ████████░░░░░░░░░░ 67% complete                    │
│                                                     │
│  ✅ 1. Vector Spaces                                │
│  ✅ 2. Linear Maps                                  │
│  ▶  3. Eigenvalues  ← You are here                  │
│  ⬜ 4. Diagonalization                              │
│  ⬜ 5. Inner Product Spaces                         │
│                                                     │
│  [📋 Take Notes]  [✏️ Practice Problems]  [🎯 Quiz]  │
│                                                     │
│  ─── Content ───                                    │
│                                                     │
│  (Full lesson with examples, exercises, hints)      │
│                                                     │
│  [Mark Complete ▼]                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2.3 Researcher Mode

```
┌─────────────────────────────────────────────────────┐
│  🔍 Search...    [Explorer] [Student] [Researcher ▼] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Eigenvalue                                         │
│  Algebra > Linear Algebra > Spectral Theory         │
│                                                     │
│  Definition | Theorems | Proofs | References | History│
│                                                     │
│  (Full formal content with LaTeX, citations, etc)   │
│                                                     │
│  Dependency Graph:                                  │
│  [Visual graph showing all 47 connections]          │
│                                                     │
│  Used in 23 proofs:                                 │
│  • Spectral Theorem (von Neumann, 1929)             │
│  • ...                                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 3. The "You Are Here" Map

Not a full graph — a **local neighborhood**.

```
        [Matrix] ───────┐
            │            │
            ▼            ▼
    [Vector Space] ──► [Linear Map] ──► [Eigenvalue] ◄── You
            │            │            │       │
            ▼            ▼            ▼       ▼
        [Field]      [Kernel]    [Eigenvector]
```

**Rules:**
- Show 1–2 steps in each direction
- Highlight the current concept
- Gray out concepts the user hasn't visited
- Click any concept to jump
- Hover for 1-sentence preview

---

## 4. Learning Paths (Curated Sequences)

The system offers **guided journeys**, not just free exploration.

### Path Examples

| Path | Concepts | Time | For |
|------|----------|------|-----|
| **What is math?** | Proposition → Set → Number → Function | 30 min | Absolute beginner |
| **Why does algebra work?** | Group → Ring → Field → Vector Space | 2 hours | Curious student |
| **How Google works** | Matrix → Eigenvalue → PageRank | 1 hour | Applied learner |
| **What is infinity?** | Set → Cardinality → Ordinal → ZFC | 3 hours | Philosophy-minded |
| **Crash course: Linear Algebra** | Vector → Matrix → Eigenvalue → SVD | 4 hours | ML practitioner |

### Path UI

```
┌─────────────────────────────────────────────┐
│  🗺️ Path: "How Google Works"                │
│  5 concepts • ~1 hour • Beginner friendly   │
├─────────────────────────────────────────────┤
│                                             │
│  ✅ 1. Matrix (5 min)                       │
│     "A grid of numbers that does things"    │
│                                             │
│  ✅ 2. Eigenvalue (10 min)                  │
│     "Secret numbers inside a matrix"        │
│                                             │
│  ▶  3. PageRank (15 min)  ← You are here   │
│     "How Google ranks websites"             │
│                                             │
│  ⬜  4. Markov Chain (10 min)               │
│  ⬜  5. Random Walk (10 min)                │
│                                             │
│  [◀ Back]  [Next ▶]  [Exit Path]           │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 5. Progressive Disclosure

Don't dump everything at once.

### Layer 1: The Hook (1 sentence)
```
"Eigenvalues are the secret numbers that tell you
how much a transformation stretches space."
```

### Layer 2: The Intuition (1 paragraph)
```
Imagine stretching a rubber sheet. Most points move sideways,
but some points only move straight outward — those directions
are eigenvectors, and how much they stretch is the eigenvalue.
```

### Layer 3: The Example (Concrete)
```
Take the matrix [[2, 0], [0, 3]]. It stretches x by 2 and y by 3.
The eigenvalues are 2 and 3. The eigenvectors are (1,0) and (0,1).
```

### Layer 4: The Formal Definition
```
A scalar λ ∈ F is an eigenvalue of T: V → V if ∃v ≠ 0: T(v) = λv.
```

### Layer 5: The Proof
```
Proof that eigenvalues of a symmetric matrix are real...
```

**UI:** Expandable sections. Default shows Layer 1–3. "Show formal definition" reveals Layer 4. "Show proof" reveals Layer 5.

---

## 6. Visual Navigation

### 6.1 Concept Cards

Each concept is a card, not just a page.

```
┌─────────────────────────┐
│  🎯 Eigenvalue          │
│                         │
│  "Secret stretch numbers"│
│                         │
│  [🎮 Play] [📖 Learn]   │
│                         │
│  🔓 Unlocks:            │
│  Diagonalization        │
│  PCA                    │
│                         │
└─────────────────────────┘
```

### 6.2 Area Browsers

Browse by topic area with visual previews.

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│             │ │             │ │             │
│  Numbers    │ │  Shapes     │ │  Patterns   │
│             │ │             │ │             │
│  1 2 3 ∞    │ │  △ ○ □     │ │  ~ ≈ =      │
│             │ │             │ │             │
│  24 topics  │ │  31 topics  │ │  19 topics  │
│             │ │             │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
```

### 6.3 Search That Understands

```
Search: "why do matrices rotate"

Results:
  1. Orthogonal Matrix — "Matrices that preserve angles"
  2. Rotation Matrix — "A specific orthogonal matrix"
  3. Eigenvalue — "Reveals rotation vs stretching"

Did you mean:
  • "How to rotate a vector" → Rotation Matrix
  • "What matrices don't change lengths" → Orthogonal Matrix
```

---

## 7. Accessibility

| Feature | Implementation |
|---------|---------------|
| **No LaTeX by default** | MathJax renders, but plain text shown on hover |
| **Mobile-first** | Cards stack, paths scroll horizontally |
| **Dark mode** | Toggle, saves preference |
| **Reading level** | Slider: "Explain like I'm 10" to "Formal proof" |
| **Text-to-speech** | Built-in for definitions |
| **Offline** | Service Worker caches visited pages |
| **Print-friendly** | Strip UI, keep content + diagrams |

---

## 8. Technical Implementation

### 8.1 Frontend Stack

```
Lemma Site
├── DocsForge (static site generator)
├── Vanilla JS (no framework bloat)
├── MathJax (rendering)
├── D3.js (graph visualization)
└── LocalStorage (progress tracking)
```

### 8.2 Progressive Enhancement

```html
<!-- Base: Linked concept -->
<a href="/algebra/eigenvalue/">Eigenvalue</a>

<!-- Enhanced: Card with preview -->
<div class="concept-card" data-concept="eigenvalue">
  <h3>Eigenvalue</h3>
  <p>"Secret stretch numbers"</p>
  <a href="/algebra/eigenvalue/">Explore →</a>
</div>

<!-- Fully enhanced: Inline preview on hover -->
<a href="/algebra/eigenvalue/" class="wiki-link" data-preview>
  eigenvalue
</a>
<!-- Hover shows: popup with 1-sentence definition -->
```

### 8.3 Mode Switching

```javascript
// URL-based mode switching
// /algebra/eigenvalue/?mode=explorer (default)
// /algebra/eigenvalue/?mode=student
// /algebra/eigenvalue/?mode=researcher

// Persist in localStorage
localStorage.setItem('lemma-mode', 'student');
```

---

## 9. The Linking System (Backend → Frontend)

The pipeline generates multiple views from the same graph:

```
concepts.json (graph)
    │
    ├──► docs/ (markdown pages)
    │     ├── explorer view (friendly)
    │     ├── student view (structured)
    │     └── researcher view (formal)
    │
    ├──► paths/ (curated sequences)
    │     ├── what-is-math.json
    │     ├── how-google-works.json
    │     └── crash-course-linear-algebra.json
    │
    ├──► graph/ (visualization data)
    │     └── d3-force-data.json
    │
    └──► api/ (search index)
          └── search-index.json
```

---

## 10. Success Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Time to first understanding | < 2 min | "Get it" button on pages |
| Path completion rate | > 60% | Track path progress |
| Return visits | > 3/page | Analytics |
| Student → Researcher switch | < 5% | Most stay in Student/Explorer |
| Mobile usage | > 50% | Analytics |

---

## Summary

| Bad Wiki | Good Wiki |
|----------|-----------|
| "Click to see definition" | "You already know this from [previous concept]" |
| Full graph dump | "Here's what you need right now" |
| LaTeX first | Plain English first, math on demand |
| One size fits all | Explorer / Student / Researcher |
| Search only | Guided paths + search |
| Desktop only | Mobile-first |

**The graph is invisible infrastructure. The user sees paths.**
