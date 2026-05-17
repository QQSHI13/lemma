# Lemma — A Rigorous Mathematical Wiki

## Vision

A rigorous mathematical encyclopedia where **every concept has its own page**. Every definition is precise, every theorem is proved, every proof is explained.

**URL:** https://qqshi13.github.io/lemma/

---

## Page Structure

Every concept gets its own `.md` file. No combining topics.

```
docs/
├── index.md
├── foundations/
│   ├── index.md
│   ├── proposition.md                    # What is a proposition
│   ├── truth-table.md                    # Truth tables
│   ├── logical-connective.md            # AND, OR, NOT, IMPLIES
│   ├── quantifier.md                     # FORALL, EXISTS
│   ├── set.md                            # Definition of a set
│   ├── element.md                        # Element membership
│   ├── subset.md                         # Subset relation
│   ├── union.md                          # Union of sets
│   ├── intersection.md                   # Intersection of sets
│   ├── complement.md                     # Set complement
│   ├── cartesian-product.md             # A × B
│   ├── relation.md                       # Relations
│   ├── function.md                       # Functions as relations
│   ├── injection.md                      # One-to-one
│   ├── surjection.md                     # Onto
│   ├── bijection.md                      # One-to-one correspondence
│   ├── direct-proof.md                   # Proof technique
│   ├── proof-by-contradiction.md        # Proof technique
│   ├── proof-by-contrapositive.md       # Proof technique
│   ├── proof-by-induction.md            # Proof technique
│   └── equivalence-proof.md             # Iff proofs
├── number-systems/
│   ├── index.md
│   ├── natural-number.md                # Peano axioms
│   ├── integer.md                       # Construction from naturals
│   ├── rational-number.md               # Equivalence classes
│   ├── real-number.md                   # Dedekind cuts or Cauchy
│   ├── complex-number.md                # Ordered pairs
│   ├── absolute-value.md                # Definition, properties
│   └── interval.md                      # Open, closed, half-open
├── algebra/
│   ├── index.md
│   ├── vector.md                        # Definition, examples
│   ├── vector-addition.md               # Operation
│   ├── scalar-multiplication.md        # Operation
│   ├── dot-product.md                   # Inner product on R^n
│   ├── cross-product.md                # R^3 only
│   ├── vector-space.md                  # Axioms
│   ├── subspace.md                     # Subset that's a vector space
│   ├── linear-combination.md           # Sum of scalar multiples
│   ├── span.md                         # All linear combinations
│   ├── linear-independence.md          # Definition, tests
│   ├── basis.md                        # Linearly independent spanning set
│   ├── dimension.md                    # Size of any basis
│   ├── linear-map.md                   # Structure-preserving map
│   ├── kernel.md                       # Null space
│   ├── image.md                        # Range/column space
│   ├── rank-nullity-theorem.md         # dim(V) = rank + nullity
│   ├── matrix.md                       # Rectangular array
│   ├── matrix-addition.md              # Entrywise
│   ├── matrix-multiplication.md        # Row by column
│   ├── transpose.md                    # Rows become columns
│   ├── inverse-matrix.md               # A^{-1}
│   ├── determinant.md                  # det(A)
│   ├── minor.md                        # Submatrix determinant
│   ├── cofactor.md                     # Signed minor
│   ├── cofactor-expansion.md           # Laplace expansion
│   ├── eigenvalue.md                   # λ where Av = λv
│   ├── eigenvector.md                  # Nonzero v where Av = λv
│   ├── characteristic-polynomial.md   # det(A - λI)
│   ├── diagonalization.md              # A = PDP^{-1}
│   ├── inner-product-space.md          # General inner product
│   ├── orthogonality.md                # Perpendicular vectors
│   ├── orthogonal-basis.md             # Basis of orthogonal vectors
│   ├── orthonormal-basis.md            # Basis of unit orthogonal vectors
│   ├── gram-schmidt.md                 # Process
│   ├── group.md                        # Set with binary operation
│   ├── subgroup.md                     # Subset that's a group
│   ├── coset.md                        # aH for subgroup H
│   ├── normal-subgroup.md              # aH = Ha
│   ├── quotient-group.md               # G/N
│   ├── group-homomorphism.md           # Structure-preserving
│   ├── kernel-homomorphism.md          # Preimage of identity
│   ├── isomorphism-theorem.md         # First isomorphism theorem
│   ├── ring.md                         # Two operations
│   ├── ideal.md                        # Absorbing subset
│   ├── quotient-ring.md               # R/I
│   ├── field.md                        # Commutative division ring
│   ├── polynomial.md                   # Formal expression
│   ├── polynomial-ring.md             # R[x]
│   ├── root.md                         # f(a) = 0
│   ├── factorization.md               # Into irreducibles
│   ├── irreducible.md                  # Cannot factor further
│   └── euclidean-domain.md             # Division algorithm
├── analysis/
│   ├── index.md
│   ├── sequence.md                     # Function N → R
│   ├── convergence.md                  # lim a_n = L
│   ├── divergence.md                   # Not convergent
│   ├── limit-superior.md               # limsup
│   ├── limit-inferior.md               # liminf
│   ├── cauchy-sequence.md              | Self-test for convergence
│   ├── series.md                       | Sum of sequence
│   ├── partial-sum.md                  | s_n = a_1 + ... + a_n
│   ├── geometric-series.md             | Sum of ar^n
│   ├── harmonic-series.md              | Sum of 1/n
│   ├── p-series.md                     | Sum of 1/n^p
│   ├── comparison-test.md              | For convergence
│   ├── ratio-test.md                   | For convergence
│   ├── root-test.md                    | For convergence
│   ├── alternating-series-test.md      | For convergence
│   ├── absolute-convergence.md        | Sum of |a_n| converges
│   ├── conditional-convergence.md      | Converges but not absolutely
│   ├── function-limit.md               | lim f(x) = L
│   ├── continuity.md                   | lim f(x) = f(a)
│   ├── discontinuity.md                | Not continuous
│   ├── uniform-continuity.md           | δ doesn't depend on point
│   ├── differentiability.md            | f'(a) exists
│   ├── derivative.md                   | Rate of change
│   ├── mean-value-theorem.md           | f'(c) = (f(b)-f(a))/(b-a)
│   ├── rolles-theorem.md               | Special case of MVT
│   ├── taylor-theorem.md               | Polynomial approximation
│   ├── taylor-series.md                | Infinite Taylor polynomial
│   ├── power-series.md                 | Sum a_n x^n
│   ├── radius-of-convergence.md        | Where power series converges
│   ├── riemann-integral.md             | Upper/lower sums
│   ├── fundamental-theorem-calculus.md | Connects derivative and integral
│   ├── integration-by-parts.md        | Technique
│   ├── substitution-rule.md            | u-substitution
│   ├── improper-integral.md            | Infinite bounds
│   ├── complex-number-analysis.md      | a + bi
│   ├── complex-differentiability.md   | Holomorphic
│   ├── cauchy-riemann-equations.md     | Test for holomorphic
│   ├── contour-integral.md             | Integral along path
│   ├── cauchy-theorem.md              | Integral around closed path
│   ├── residue.md                      | Coefficient of 1/(z-a)
│   └── residue-theorem.md              | Sum of residues
├── geometry/
│   ├── index.md
│   ├── euclidean-axioms.md             # Hilbert's axioms
│   ├── point.md                          # Undefined term
│   ├── line.md                           # Undefined term
│   ├── plane.md                          # Undefined term
│   ├── betweenness.md                    # Order on line
│   ├── congruence.md                     # Same size/shape
│   ├── triangle.md                       # Three segments
│   ├── triangle-inequality.md            # |a+b| ≤ |a| + |b|
│   ├── angle.md                          # Union of two rays
│   ├── angle-sum-triangle.md             # 180 degrees
│   ├── polygon.md                        # Closed broken line
│   ├── regular-polygon.md                # Equal sides/angles
│   ├── circle.md                         # Equidistant from center
│   ├── circumference.md                 # Perimeter of circle
│   ├── pi.md                             # Circumference/diameter
│   ├── area-circle.md                    # πr²
│   ├── chord.md                          # Segment connecting two points
│   ├── tangent.md                        # Line touching at one point
│   ├── secant.md                         # Line intersecting at two points
│   ├── arc.md                            # Part of circumference
│   ├── sector.md                         # Wedge-shaped region
│   ├── pythagorean-theorem.md            # a² + b² = c²
│   ├── pythagorean-proof-rearrangement.md # Proof by moving triangles
│   ├── pythagorean-proof-similar.md     # Proof using similar triangles
│   ├── pythagorean-proof-algebraic.md   # Algebraic proof
│   ├── similarity.md                     # Same shape, different size
│   ├── similar-triangles.md              # AAA criterion
│   ├── trigonometric-functions.md        # Sine, cosine, tangent
│   ├── sine-law.md                       # a/sin(A) = 2R
│   ├── cosine-law.md                     # c² = a² + b² - 2ab cos(C)
│   ├── polygon-angle-sum.md             # (n-2) × 180°
│   ├── parallelogram.md                  # Two pairs of parallel sides
│   ├── rectangle.md                     # Right angles
│   ├── rhombus.md                        # Equal sides
│   ├── square.md                         # Equal sides, right angles
│   ├── trapezoid.md                      # One pair parallel sides
│   ├── parallel-postulate.md             # Fifth postulate
│   ├── hyperbolic-geometry.md           # Negate parallel postulate
│   ├── elliptic-geometry.md             # No parallel lines
│   ├── great-circle.md                  | "Lines" on sphere
│   ├── metric-space.md                   # Distance function
│   ├── open-set.md                       # Union of open balls
│   ├── closed-set.md                     | Complement of open
│   ├── boundary.md                       | Points on edge
│   ├── interior.md                       | Points inside
│   ├── closure.md                        | Set plus boundary
│   ├── limit-point.md                    | Every neighborhood intersects
│   ├── compactness.md                    | Every open cover has finite subcover
│   ├── heine-borel-theorem.md           | Compact iff closed and bounded in R^n
│   ├── connectedness.md                  | Cannot split into two open sets
│   ├── path-connected.md                 | Can draw path between any points
│   └── continuity-topology.md           | Preimage of open is open
├── number-theory/
│   ├── index.md
│   ├── divisibility.md                   # a | b
│   ├── division-algorithm.md            # a = bq + r
│   ├── greatest-common-divisor.md       # gcd(a,b)
│   ├── least-common-multiple.md         # lcm(a,b)
│   ├── euclidean-algorithm.md           # Compute gcd
│   ├── bezout-identity.md               # ax + by = gcd(a,b)
│   ├── prime-number.md                  # p > 1, only 1 and p divide
│   ├── composite-number.md              # Not prime, not 1
│   ├── sieve-eratosthenes.md            | Find primes
│   ├── infinitude-primes.md             | Euclid's proof
│   ├── prime-factorization.md           | Product of primes
│   ├── fundamental-theorem-arithmetic.md | Unique factorization
│   ├── congruence.md                    | a ≡ b (mod n)
│   ├── modular-arithmetic.md           | Arithmetic mod n
│   ├── residue-class.md                 | [a] = {a + kn}
│   ├── multiplicative-inverse-mod.md   | ax ≡ 1 (mod n)
│   ├── fermat-little-theorem.md        | a^(p-1) ≡ 1 (mod p)
│   ├── euler-theorem.md                 | a^φ(n) ≡ 1 (mod n)
│   ├── euler-totient-function.md       | φ(n) = count of coprime
│   ├── chinese-remainder-theorem.md     | Solve system of congruences
│   ├── quadratic-residue.md           | Square mod p
│   ├── legendre-symbol.md             | (a/p)
│   └── quadratic-reciprocity.md       | (p/q)(q/p) = (-1)^...
├── discrete-mathematics/
│   ├── index.md
│   ├── graph.md                         # Vertices and edges
│   ├── vertex.md                        # Node
│   ├── edge.md                          # Connection
│   ├── degree.md                        # Number of edges at vertex
│   ├── path.md                          # Sequence of edges
│   ├── cycle.md                         | Path starting/ending at same vertex
│   ├── connected-graph.md              | Path between any two vertices
│   ├── tree.md                         | Connected acyclic graph
│   ├── spanning-tree.md                 | Tree containing all vertices
│   ├── euler-path.md                    | Traverses every edge once
│   ├── hamilton-path.md                 | Visits every vertex once
│   ├── bipartite-graph.md              | Two-colorable
│   ├── complete-graph.md               | Every vertex connected
│   ├── planar-graph.md                 | Can draw without crossings
│   ├── isomorphism.md                  | Structure-preserving bijection
│   ├── adjacency-matrix.md             | Matrix representation
│   ├── adjacency-list.md               | List representation
│   ├── permutation.md                  | Bijection from set to itself
│   ├── combination.md                  | Subset of size k
│   ├── binomial-coefficient.md         | C(n,k)
│   ├── binomial-theorem.md             | (a+b)^n expansion
│   ├── pigeonhole-principle.md         | n items in m containers
│   ├── inclusion-exclusion.md          | |A ∪ B| = |A| + |B| - |A ∩ B|
│   ├── recurrence-relation.md          | a_n defined from previous
│   ├── fibonacci-sequence.md           | F_n = F_{n-1} + F_{n-2}
│   └── generating-function.md          | Formal power series
└── probability/
    ├── index.md
    ├── sample-space.md                  # All possible outcomes
    ├── event.md                         # Subset of sample space
    ├── probability-axioms.md            # Kolmogorov's axioms
    ├── conditional-probability.md       # P(A|B)
    ├── independence.md                  # P(A∩B) = P(A)P(B)
    ├── bayes-theorem.md                 # P(A|B) formula
    ├── random-variable.md              # Function on sample space
    ├── discrete-random-variable.md     # Countable range
    ├── continuous-random-variable.md   # Uncountable range
    ├── probability-mass-function.md     # P(X = x)
    ├── probability-density-function.md  # f(x)
    ├── cumulative-distribution.md      # F(x) = P(X ≤ x)
    ├── expected-value.md                # E[X]
    ├── variance.md                     # E[(X-μ)²]
    ├── standard-deviation.md            | sqrt(variance)
    ├── bernoulli-distribution.md        | 0 or 1
    ├── binomial-distribution.md         | n Bernoulli trials
    ├── geometric-distribution.md        | Trials until first success
    ├── poisson-distribution.md          | Rare events
    ├── normal-distribution.md           | Bell curve
    ├── central-limit-theorem.md         | Sum approaches normal
    ├── law-large-numbers.md            | Sample mean → μ
    └── markov-inequality.md            | P(X ≥ a) ≤ E[X]/a
```

---

## Page Template

Every `.md` file follows this exact structure:

```markdown
# [Concept Name]

## Definition

Precise mathematical definition.

## Formal Statement

If applicable, the formal symbolic statement.

## Why It Matters

1-2 sentences of intuition.

## Properties

- Property 1 (with proof if short)
- Property 2 (with proof if short)

## Theorem [if applicable]

### Statement
Precise theorem statement.

### Proof
Step-by-step proof.

**QED**

## Examples

### Example 1
Concrete example with explanation.

### Example 2
Another example showing edge case.

## Counterexamples [if applicable]

What goes wrong if conditions are relaxed.

## Related

- [Prerequisite 1](link.md) — why you need this first
- [Prerequisite 2](link.md)
- [Used in](link.md) — where this appears
- [Generalization](link.md) — broader concept
- [Specialization](link.md) — specific case
```

---

## Quality Standards

- One concept per file. Never combine.
- Every definition precise.
- Every theorem proved (or marked "proof omitted" with reference).
- Proofs complete. No "it's obvious."
- Every page has at least one example.
- Every page has related links.
- TikZ diagrams where geometric.
