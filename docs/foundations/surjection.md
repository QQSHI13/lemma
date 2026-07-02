---
title: Surjection (Onto Function)
area: foundations
difficulty: 2
prerequisites:
  - function
  - set
  - element
related:
  - injection
  - bijection
  - composition
  - inverse
tags:
  - foundations
  - sets
  - definition
---

# Surjection (Onto Function)

## Definition

A function $f: A \to B$ is a **surjection** (or **onto**) if:

$$\forall b \in B, \exists a \in A : f(a) = b$$

Equivalently: every element in the codomain is the image of some element in the domain.

## Examples

### Example 1: $f(x) = x^3$ on $\mathbb{R}$
For any $y \in \mathbb{R}$, take $x = \sqrt[3]{y}$. Then $f(x) = y$.

This is a surjection.

### Example 2: $f(x) = x^2$ on $\mathbb{R} \to \mathbb{R}$
There is no $x$ such that $f(x) = -1$.

Not a surjection (but is a surjection onto $[0, \infty)$).

### Example 3: Projection
$\pi_1: A \times B \to A$ given by $\pi_1(a, b) = a$ is a surjection.

## Composition of Surjections

If $f: A \to B$ and $g: B \to C$ are surjections, then $g \circ f: A \to C$ is a surjection.

## Related

- [Function](function.md) — The general concept
- [Injection](injection.md) — Distinct inputs map to distinct outputs (dual concept)
- [Bijection](bijection.md) — Both injection and surjection
- [Cartesian Product](cartesian-product.md) — Used in projection example
- [Direct Proof](direct-proof.md) — Proving a function is surjective
