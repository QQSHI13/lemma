# Lemma — Dependency Model v2 (Cycles Allowed)

> **Insight:** Math dependency graphs have cycles at the foundational level and feedback loops everywhere. A strict DAG kills the wiki at 50 pages.

---

## The Problem with Strict DAGs

```
ZFC ──needs──► Peano arithmetic
 ▲                │
 └──needs─────────┘

Group theory ◄──motivates── Lagrange's theorem
     │                           │
     └──formally-depends-on──────┘
```

**Cycles happen because:**
1. **Foundational cycles:** ZFC ↔ arithmetic, sets ↔ logic
2. **Motivational cycles:** calculus motivates physics, physics motivates calculus
3. **Pedagogical cycles:** introduce groups informally → prove Lagrange → define groups formally
4. **Duality cycles:** vector space ↔ dual space, topology ↔ algebra

**The solution:** Don't ban cycles. **Classify dependency strength** and let the pipeline handle them intelligently.

---

## 1. Dependency Types (Not Just "Prerequisite")

```json
{
  "id": "zfc",
  "name": "Zermelo-Fraenkel with Choice",
  "dependencies": [
    {
      "target": "propositional-logic",
      "type": "formal-depends",
      "strength": "strict",
      "layer": "meta"
    },
    {
      "target": "natural-number",
      "type": "can-construct",
      "strength": "defines",
      "layer": "constructs"
    },
    {
      "target": "peano-arithmetic",
      "type": "motivates",
      "strength": "informs",
      "layer": "motivation"
    }
  ]
}
```

### Dependency Type Taxonomy

| Type | Meaning | Example |
|------|---------|---------|
| `formal-depends` | You cannot define X without Y | eigenvalue → linear-map |
| `can-construct` | Y can be constructed from X | zfc → natural-number |
| `motivates` | X motivates Y historically | physics → calculus |
| `generalizes` | Y is a special case of X | group → abelian-group |
| `dual` | X and Y are dual concepts | vector-space → dual-space |
| `informs` | Knowing X helps understand Y | topology → analysis |
| `applies` | X is a tool for Y | linear-algebra → machine-learning |
| `historical` | X historically preceded Y | euclidean-geometry → non-euclidean |

### Strength Levels

| Strength | CI Behavior | Example |
|----------|-------------|---------|
| `strict` | Build fails if Y not published | eigenvalue needs linear-map |
| `recommended` | Warning if Y not published | topology helps analysis |
| `optional` | No warning | historical context |
| `circular` | Special handling — both can be draft | zfc ↔ arithmetic |

---

## 2. Pedagogical Layers

Not everything needs full rigor. A concept can exist at multiple layers:

```json
{
  "id": "group",
  "name": "Group",
  "layers": {
    "intuitive": {
      "status": "published",
      "page": "docs/algebra/group-intuitive.md",
      "content": "A group is symmetries of an object. Rotations of a square form a group."
    },
    "formal": {
      "status": "published",
      "page": "docs/algebra/group.md",
      "content": "A group (G, ·) is a set G with binary operation satisfying associativity, identity, inverses.",
      "formal-depends": ["set", "binary-operation", "associativity"]
    },
    "axiomatic": {
      "status": "draft",
      "page": "docs/algebra/group-axiomatic.md",
      "content": "In ZFC, a group is a tuple (G, ·, e, ⁻¹) where...",
      "formal-depends": ["zfc", "tuple", "function"]
    }
  }
}
```

**How it works:**
- Learner at level N reads `group-intuitive.md`
- Learner at level N+1 reads `group.md` (links back to intuitive version)
- Researcher reads `group-axiomatic.md`

**The pipeline generates cross-layer links:**
```markdown
## Related
- **Intuitive version**: [[group-intuitive]]
- **Formal version**: [[group]]
- **Axiomatic version**: [[group-axiomatic]]
```

---

## 3. Cycle Handling

### 3.1 Foundational Cycles (ZFC ↔ Arithmetic)

```
Flag as: "foundational-cycle"
Resolution: Pick a bootstrap concept
```

The pipeline detects the cycle and asks: "Which concept is the bootstrap?"

```json
{
  "cycles": [
    {
      "members": ["zfc", "peano-arithmetic", "propositional-logic"],
      "type": "foundational",
      "resolution": "zfc",
      "note": "ZFC is the bootstrap. Arithmetic is constructed within ZFC, but ZFC's metatheory uses intuitive arithmetic."
    }
  ]
}
```

**Build behavior:**
- Bootstrap concept (`zfc`) can be published without its cycle-mates
- Other cycle members need at least the intuitive layer of bootstrap
- No infinite regress: once bootstrap is published, cycle resolves

### 3.2 Motivational Cycles (Calculus ↔ Physics)

```
Flag as: "motivational-cycle"
Resolution: Both can be draft, both can be published
```

```json
{
  "cycles": [
    {
      "members": ["calculus", "classical-mechanics"],
      "type": "motivational",
      "resolution": "allow"
    }
  ]
}
```

**Build behavior:**
- Motivational cycles don't block publication
- Both pages can reference each other
- Pipeline adds note: "See also: [[classical-mechanics]] for historical motivation"

### 3.3 Pedagogical Cycles (Groups ↔ Lagrange)

```
Flag as: "pedagogical-cycle"
Resolution: Introduce informally first
```

```json
{
  "cycles": [
    {
      "members": ["group", "lagrange-theorem"],
      "type": "pedagogical",
      "resolution": "group-intuitive-first"
    }
  ]
}
```

**Build behavior:**
- `group-intuitive.md` published first (no formal deps)
- `lagrange-theorem.md` can reference `group-intuitive`
- `group-formal.md` published later with full rigor

---

## 4. Multiple Paths to a Concept

A concept can be reached through different routes:

```
Route A: Foundations → Sets → Functions → Relations → Group theory
Route B: Foundations → Numbers → Modular arithmetic → Group theory
Route C: Foundations → Geometry → Symmetries → Group theory
```

The pipeline tracks all paths:

```json
{
  "id": "group",
  "paths": [
    {
      "name": "Algebraic",
      "concepts": ["set", "function", "relation", "binary-operation", "group"],
      "length": 5
    },
    {
      "name": "Number-theoretic",
      "concepts": ["natural-number", "modular-arithmetic", "group"],
      "length": 3
    },
    {
      "name": "Geometric",
      "concepts": ["transformation", "symmetry", "group"],
      "length": 3
    }
  ]
}
```

**Dashboard shows:** "Learn group theory via: [Algebraic path] [Number path] [Geometric path]"

---

## 5. The Build Algorithm (Cycle-Aware)

```python
def build_in_order(concepts: dict) -> List[str]:
    """
    Return build order that handles cycles gracefully.
    
    Strategy:
    1. Topological sort for strict-DAG portion
    2. For cycles: bootstrap-first, then layers
    3. For motivational cycles: parallel build
    """
    
    # Phase 1: Separate strict deps from circular/motivational
    strict_graph = {id: [] for id in concepts}
    circular_graph = {id: [] for id in concepts}
    
    for id, c in concepts.items():
        for dep in c.get("dependencies", []):
            if dep["strength"] == "strict" and dep["type"] != "circular":
                strict_graph[id].append(dep["target"])
            else:
                circular_graph[id].append(dep["target"])
    
    # Phase 2: Topological sort of strict graph
    order = topological_sort(strict_graph)
    
    # Phase 3: Handle cycles
    for cycle in find_cycles(strict_graph):
        resolution = get_cycle_resolution(concepts, cycle)
        if resolution == "bootstrap":
            # Move bootstrap to front of cycle
            bootstrap = concepts[cycle[0]]["bootstrap"]
            order = [bootstrap] + [c for c in order if c != bootstrap]
    
    # Phase 4: Add circular/motivational (can be built in any order)
    remaining = [id for id in concepts if id not in order]
    order.extend(remaining)
    
    return order
```

---

## 6. Updated concepts.json Schema

```json
{
  "version": "2.0.0",
  "bootstrap_concepts": ["proposition", "set", "natural-number"],
  "concepts": [
    {
      "id": "zfc",
      "name": "Zermelo-Fraenkel with Choice",
      "area": "foundations",
      "layers": {
        "axiomatic": {
          "status": "published",
          "quality_score": 88,
          "formal_depends": ["propositional-logic", "first-order-logic"]
        }
      },
      "dependencies": [
        {
          "target": "propositional-logic",
          "type": "formal-depends",
          "strength": "strict"
        },
        {
          "target": "peano-arithmetic",
          "type": "can-construct",
          "strength": "defines"
        },
        {
          "target": "natural-number",
          "type": "motivates",
          "strength": "informs"
        }
      ],
      "cycles": [
        {
          "with": "peano-arithmetic",
          "type": "foundational",
          "resolution": "bootstrap"
        }
      ]
    },
    {
      "id": "group",
      "name": "Group",
      "area": "algebra",
      "layers": {
        "intuitive": {
          "status": "published",
          "quality_score": 75,
          "formal_depends": []
        },
        "formal": {
          "status": "published",
          "quality_score": 90,
          "formal_depends": ["set", "binary-operation", "associativity"]
        }
      },
      "dependencies": [
        {
          "target": "symmetry",
          "type": "motivates",
          "strength": "informs"
        },
        {
          "target": "modular-arithmetic",
          "type": "example-of",
          "strength": "optional"
        }
      ]
    }
  ]
}
```

---

## 7. What This Enables (That v1 Couldn't)

| Feature | v1 (DAG) | v2 (Cycles) |
|--------|----------|-------------|
| Foundations | ZFC must be first | ZFC and arithmetic co-evolve |
| Physics in math | Not allowed | Calculus ↔ Mechanics cross-reference |
| Pedagogy | Rigid order | Intuitive → Formal → Axiomatic layers |
| Duality | Not modeled | Vector space ↔ Dual space |
| Research math | Breaks | Handles mutually-defining concepts |
| Contributor paths | One path | Multiple entry points to same concept |

---

## 8. Implementation Impact

**What changes in the pipeline:**

1. `concepts.json` adds `layers`, `cycles`, `paths` fields
2. `lemma_pipeline.py` uses cycle-aware topological sort
3. CI allows `circular` and `motivational` deps without failing
4. Dashboard shows "Bootstrap concepts" and "Cycle groups"
5. Page generator creates cross-layer links automatically

**What stays the same:**
- Wikilink syntax: `[[concept-id]]`
- Auto-generated Related sections
- Quality scoring
- CI link validation (for `strict` deps only)

---

## 9. Example Cycle Resolution

**Cycle detected:** `zfc ↔ peano-arithmetic`

```
Pipeline output:
⚠️ Foundational cycle detected: zfc ↔ peano-arithmetic
Resolution: zfc is bootstrap (configured in concepts.json)
Build order:
  1. proposition (bootstrap)
  2. set (bootstrap)
  3. zfc (bootstrap — cycle resolved)
  4. peano-arithmetic (now allowed, bootstrap published)
  5. natural-number
```

**Dashboard shows:**
```
Foundational Cycles (3):
  • zfc ↔ arithmetic ↔ logic [bootstrap: zfc]
  • category-theory ↔ set-theory [bootstrap: set-theory]
  • type-theory ↔ logic [bootstrap: logic]
```

---

## Summary

**Math is not a tree. It's a web with knots.** The wiki should reflect that.

| | v1 (Strict DAG) | v2 (Cycles + Layers) |
|---|----------------|---------------------|
| Foundations | ZFC first, always | ZFC + arithmetic co-evolve |
| Pedagogy | One path | Multiple layers + paths |
| Cycles | Build fails | Classified + resolved |
| Scale | Breaks at cycles | Handles 10K+ with cycles |

Ready to update the pipeline for cycle-aware builds?
