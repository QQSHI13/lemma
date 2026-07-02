---
title: Proof by Contradiction
area: foundations
difficulty: 2
prerequisites:
  - proposition
  - logical-connective
  - direct-proof
related:
  - proof-by-contrapositive
  - proof-by-induction
tags:
  - foundations
  - proof
  - technique
---

# Proof by Contradiction

## Definition

**Proof by contradiction** (or *reductio ad absurdum*) is a proof technique where we assume the negation of what we want to prove and derive a logical contradiction.

## Structure

1. Assume $\neg P$ (the negation of the statement to prove)
2. Deduce a logical contradiction (e.g., $Q \land \neg Q$)
3. Conclude that $\neg P$ must be false, therefore $P$ is true

## Example: $\sqrt{2}$ is irrational

### Proof

Assume $\sqrt{2}$ is rational.

Then $\sqrt{2} = \frac{p}{q}$ for integers $p, q$ with no common factors (lowest terms).

Squaring: $2 = \frac{p^2}{q^2}$, so $p^2 = 2q^2$.

This means $p^2$ is even, so $p$ is even. Let $p = 2k$.

Then $(2k)^2 = 2q^2$, so $4k^2 = 2q^2$, thus $q^2 = 2k^2$.

So $q^2$ is even, meaning $q$ is even.

But then both $p$ and $q$ are even, contradicting our assumption that they have no common factors.

**QED**

## Related

- [Direct Proof](direct-proof.md) — The basic proof technique
- [Proposition](proposition.md) — What we prove
- [Logical Connective](logical-connective.md) — Used in constructing contradictions
