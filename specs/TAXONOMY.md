# Lemma Taxonomy — The 10 Pillars of Mathematics

> "The universe cannot be read until we have learned the language and become familiar with the characters in which it is written. It is written in mathematical language." — Galileo Galilei

This document defines the major branches of mathematics covered by Lemma. Each branch is a top-level directory in `docs/`. The taxonomy is designed to be:

- **Comprehensive** — covers all major areas of modern mathematics
- **Rigorous** — every concept has precise definitions and proofs
- **Pedagogical** — prerequisites are explicit, learning paths are clear
- **Extensible** — new areas can be added without restructuring

---

## The 10 Pillars

```
Foundations
    ↓
Number Systems → Number Theory
    ↓
Algebra ←──────┐
    ↓          │
Analysis ←─────┼── Geometry & Topology
    ↓          │
Calculus ──────┘
    ↓
Probability & Statistics
    ↓
Discrete Mathematics
    ↓
Differential Equations & Applied Mathematics
```

---

## 1. Foundations

**The bedrock.** Logic, set theory, and proof techniques. Everything else depends on this.

**Scope:**
- Propositional logic (truth tables, connectives, tautologies)
- Predicate logic (quantifiers, predicates, scope)
- Set theory (ZFC axioms, operations, relations, functions)
- Proof methods (direct, contrapositive, contradiction, induction, construction)
- Mathematical structures (relations, equivalence, order, cardinality)
- Category theory (categories, functors, natural transformations — *advanced*)
- Axiomatic systems (Peano arithmetic, ZFC, choice principles)

**Why first:** Every proof in every other branch depends on these tools.

**Key concepts:** Set, function, relation, bijection, proof, axiom, theorem, lemma, corollary.

---

## 2. Number Systems

**The building blocks.** The numbers we count, measure, and calculate with.

**Scope:**
- Natural numbers (ℕ) — Peano axioms, induction, recursion
- Integers (ℤ) — rings, divisibility, Euclidean algorithm
- Rational numbers (ℚ) — fields, density, decimal expansions
- Real numbers (ℝ) — Dedekind cuts, Cauchy sequences, completeness
- Complex numbers (ℂ) — algebraic closure, polar form, Euler's formula
- Extended systems (p-adic numbers, quaternions, octonions — *advanced*)

**Why early:** Numbers are the raw material of all mathematics.

**Key concepts:** Addition, multiplication, order, absolute value, field, completeness, infinity.

---

## 3. Number Theory

**The study of integers.** The most ancient branch, still one of the deepest.

**Scope:**
- Elementary number theory (divisibility, primes, congruences, Diophantine equations)
- Analytic number theory (Riemann zeta function, prime number theorem, Dirichlet characters)
- Algebraic number theory (number fields, algebraic integers, ideals, class groups)
- Arithmetic geometry (elliptic curves, modular forms, Diophantine geometry — *advanced*)
- Additive number theory (partitions, Waring's problem, Goldbach)

**Why early:** Accessible, beautiful, and connects to almost every other branch.

**Key concepts:** Prime number, congruence, modular arithmetic, Euler's totient, quadratic reciprocity, Riemann hypothesis.

---

## 4. Algebra

**The study of structure.** Operations, symmetries, and the patterns they create.

**Scope:**
- Linear algebra (vector spaces, matrices, linear transformations, eigenvalues, inner products)
- Group theory (groups, subgroups, homomorphisms, actions, Sylow theorems, simple groups)
- Ring theory (rings, ideals, polynomial rings, factorization, principal ideal domains)
- Field theory (field extensions, Galois theory, finite fields, algebraic closure)
- Representation theory (modules, characters, representations of finite groups — *advanced*)
- Commutative algebra (Noetherian rings, Hilbert's basis theorem, affine schemes — *advanced*)
- Homological algebra (chain complexes, homology, cohomology, derived functors — *advanced*)
- Category theory (categories, limits, adjunctions, abelian categories — *advanced*)
- Lie theory (Lie groups, Lie algebras, representations — *advanced*)

**Why central:** Algebra is the language of structure. It appears in every other branch.

**Key concepts:** Group, ring, field, vector space, homomorphism, isomorphism, kernel, image, ideal, quotient.

---

## 5. Analysis

**The study of the infinite.** Limits, continuity, and the deep structure of the real numbers.

**Scope:**
- Real analysis (sequences, series, limits, continuity, differentiation, integration, Riemann integral)
- Measure theory (Lebesgue measure, measurable functions, Lebesgue integral, convergence theorems)
- Complex analysis (holomorphic functions, Cauchy's theorem, residues, conformal mapping, Riemann surfaces)
- Functional analysis (Banach spaces, Hilbert spaces, operators, spectral theory — *advanced*)
- Harmonic analysis (Fourier series, Fourier transforms, distributions — *advanced*)
- Several complex variables (sheaves, Stein manifolds — *advanced*)

**Why central:** Analysis provides the rigorous foundation for calculus and most of applied mathematics.

**Key concepts:** Limit, continuity, convergence, uniform convergence, derivative, integral, measure, Lebesgue, Fourier series.

---

## 6. Calculus

**The mathematics of change.** Derivatives, integrals, and their applications.

**Scope:**
- Differential calculus (limits, derivatives, optimization, related rates, implicit differentiation)
- Integral calculus (antiderivatives, definite integrals, Fundamental Theorem, techniques of integration)
- Multivariable calculus (partial derivatives, gradients, multiple integrals, Jacobians)
- Vector calculus (line integrals, surface integrals, Green's theorem, Stokes' theorem, divergence theorem)
- Differential forms (exterior derivative, wedge product, generalized Stokes — *advanced*)
- Tensor calculus (covariant derivatives, curvature, Einstein notation — *advanced*)

**Why separate from Analysis:** Calculus is the computational, applied side. Analysis is the theoretical foundation. Most learners start here.

**Key concepts:** Derivative, integral, limit, continuity, chain rule, optimization, gradient, divergence, curl, Stokes' theorem.

---

## 7. Geometry & Topology

**The study of shape.** From ancient constructions to modern manifolds.

**Directory:** `docs/geometry/` (covers both geometry and topology)

**Scope:**
- Euclidean geometry (axioms, congruence, similarity, constructions, area, volume)
- Non-Euclidean geometry (hyperbolic, elliptic, spherical geometry)
- Affine & projective geometry (transformations, duality, homogeneous coordinates)
- Differential geometry (curves, surfaces, curvature, first/second fundamental forms)
- Riemannian geometry (metric tensors, geodesics, curvature tensors, manifolds — *advanced*)
- Algebraic geometry (varieties, schemes, sheaves, cohomology — *advanced*)
- Symplectic geometry (symplectic forms, Hamiltonian mechanics, moment maps — *advanced*)
- General topology (topological spaces, continuity, compactness, connectedness, separation axioms)
- Algebraic topology (homotopy, homology, cohomology, fundamental group, covering spaces — *advanced*)
- Differential topology (smooth manifolds, tangent bundles, transversality, Morse theory — *advanced*)
- Knot theory (knot invariants, polynomial invariants, braid groups — *advanced*)

**Why unified:** Geometry and topology are inseparable in modern mathematics. A manifold is a topological space with geometric structure.

**Key concepts:** Point, line, plane, angle, distance, curvature, manifold, topology, homeomorphism, homotopy, Euler characteristic.

---

## 8. Discrete Mathematics

**The study of the finite and countable.** Combinatorics, graphs, and algorithms.

**Scope:**
- Combinatorics (counting, binomial coefficients, generating functions, inclusion-exclusion, Pólya enumeration)
- Graph theory (graphs, trees, connectivity, coloring, matchings, planar graphs, network flows)
- Extremal combinatorics (Turán-type problems, Ramsey theory, Szemerédi's theorem — *advanced*)
- Probabilistic method (random graphs, Lovász local lemma, concentration inequalities — *advanced*)
- Design theory (block designs, Latin squares, finite geometries — *advanced*)
- Algorithms & complexity (time complexity, P vs NP, approximation algorithms, data structures)
- Information theory (entropy, coding, Shannon's theorems, data compression)
- Coding theory (error-correcting codes, linear codes, Reed-Solomon codes — *advanced*)

**Why important:** The language of computer science and modern data analysis.

**Key concepts:** Graph, tree, path, cycle, coloring, matching, combination, permutation, binomial coefficient, generating function, NP-complete, entropy.

---

## 9. Probability & Statistics

**The mathematics of uncertainty.** Randomness, inference, and prediction.

**Directory:** `docs/probability/` (covers both probability and statistics)

**Scope:**
- Probability theory (sample spaces, events, random variables, expectation, variance, distributions)
- Measure-theoretic probability (probability spaces, σ-algebras, Kolmogorov axioms, Borel-Cantelli)
- Stochastic processes (Markov chains, martingales, Brownian motion, Poisson processes)
- Random walks (gambler's ruin, recurrence, limiting distributions — *advanced*)
- Statistics (estimation, confidence intervals, hypothesis testing, regression, Bayesian inference)
- Machine learning (supervised learning, neural networks, optimization, generalization — *advanced*)

**Why important:** Probability is the mathematical language of the real world. Statistics turns data into knowledge.

**Key concepts:** Probability, random variable, distribution, expectation, variance, Bayes' theorem, Markov chain, hypothesis test, confidence interval, regression.

---

## 10. Differential Equations & Applied Mathematics

**The mathematics of the real world.** Models, equations, and numerical solutions.

**Directory:** `docs/applied-mathematics/`

**Scope:**
- Ordinary differential equations (ODEs) — first-order, second-order, systems, Laplace transforms, stability
- Partial differential equations (PDEs) — heat equation, wave equation, Laplace equation, Fourier methods, characteristics
- Dynamical systems (phase portraits, bifurcations, chaos, Lyapunov exponents, strange attractors — *advanced*)
- Numerical analysis (approximation, interpolation, numerical integration, numerical linear algebra, ODE/PDE solvers)
- Optimization (linear programming, convex optimization, Lagrange multipliers, gradient descent, simplex method)
- Operations research (network flows, integer programming, scheduling, game theory)
- Mathematical physics (classical mechanics, quantum mechanics, electromagnetism, general relativity, fluid dynamics)
- Control theory (feedback systems, controllability, observability, optimal control — *advanced*)

**Why last:** Applied mathematics draws on almost every other branch. It requires a solid foundation in analysis, algebra, and differential equations.

**Key concepts:** Differential equation, boundary condition, initial value problem, phase portrait, stability, numerical method, optimization, constraint, Lagrangian, Hamiltonian.

---

## Learning Paths

### Path 1: The Classical Route (historical development)
Foundations → Number Systems → Geometry → Algebra → Calculus → Analysis → Number Theory → Probability

### Path 2: The Modern Route (structural understanding)
Foundations → Number Systems → Algebra → Analysis → Topology → Geometry → Differential Equations → Applied Mathematics

### Path 3: The Applied Route (problem-driven)
Foundations → Calculus → Linear Algebra → Differential Equations → Probability → Numerical Analysis → Optimization → Machine Learning

### Path 4: The Discrete Route (computer science)
Foundations → Number Systems → Discrete Mathematics → Graph Theory → Algorithms → Probability → Information Theory → Cryptography

---

## Area Mapping

| Pillar | Directory | Status | Concepts (target) |
|--------|-----------|--------|-------------------|
| Foundations | `docs/foundations/` | 🟢 Active | ~50 |
| Number Systems | `docs/number-systems/` | 🟡 Planned | ~20 |
| Number Theory | `docs/number-theory/` | 🟡 Planned | ~30 |
| Algebra | `docs/algebra/` | 🟡 Planned | ~60 |
| Analysis | `docs/analysis/` | 🟡 Planned | ~40 |
| Calculus | `docs/calculus/` | 🟡 Active | ~30 |
| Geometry & Topology | `docs/geometry/` | 🟡 Active | ~50 |
| Discrete Mathematics | `docs/discrete-mathematics/` | 🟡 Planned | ~40 |
| Probability & Statistics | `docs/probability/` | 🟡 Planned | ~30 |
| Differential Equations & Applied | `docs/applied-mathematics/` | 🟢 New | ~40 |

**Total target:** ~390 concepts across all pillars.

---

## Prerequisites Graph

```
Foundations
├── Number Systems
│   ├── Number Theory
│   └── Algebra
│       ├── Analysis
│       │   ├── Calculus
│       │   └── Differential Equations
│       └── Geometry & Topology
├── Probability & Statistics
│   ├── Discrete Mathematics
│   └── Differential Equations
└── Discrete Mathematics
    └── Differential Equations
```

**Cross-branch prerequisites:**
- Algebra requires Foundations, Number Systems
- Analysis requires Foundations, Number Systems, Algebra
- Calculus requires Foundations, Number Systems
- Geometry requires Foundations, Algebra, Analysis
- Topology requires Foundations, Algebra, Analysis
- Probability requires Foundations, Number Systems, Calculus, Analysis
- Differential Equations requires Calculus, Analysis, Algebra, Linear Algebra
- Applied Mathematics requires almost everything

---

## Frontmatter Area Values

When writing concept pages, use these `area:` values in frontmatter:

```yaml
area: foundations
area: number-systems
area: number-theory
area: algebra
area: analysis
area: calculus
area: geometry          # includes topology
area: discrete-mathematics
area: probability        # includes statistics
area: applied-mathematics
```

Note: Directory names use hyphens. The `area` field in frontmatter should match the directory name.

---

## Open Questions

1. **Should Category Theory be its own pillar?** Currently under Foundations and Algebra. At advanced levels, it unifies everything.

2. **Should Mathematical Logic be separate?** Model theory, proof theory, recursion theory, and set theory are deep enough to be their own pillar. Currently under Foundations.

3. **Should Statistics be separate from Probability?** They have different cultures and methods. Currently unified.

4. **How to handle History?** Historical context enriches understanding but isn't a mathematical branch. Could be a `docs/history/` section.

5. **Computational mathematics?** Computer algebra, symbolic computation, and numerical methods straddle multiple areas. Currently under Applied Mathematics.

---

## Version

This taxonomy is version 1.0. As Lemma grows, pillars may be split, merged, or reordered. The frontmatter-first architecture makes such changes easy.
