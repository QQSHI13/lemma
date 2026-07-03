---
title: Proof by Induction
area: foundations
prerequisites:
  - proposition
  - logical-connective
  - natural-number
related:
  - direct-proof
  - proof-by-contrapositive
  - recursion
difficulty: 2
status: draft
quality_score: 0
---

# Proof by Induction

A proof technique for statements about natural numbers, using a base case and inductive step.

## Principle

To prove $\forall n \in \mathbb{N}: P(n)$:

1. **Base case**: Prove $P(0)$ (or $P(1)$)
2. **Inductive step**: Assume $P(k)$ (inductive hypothesis), prove $P(k+1)$

## Why It Works

The well-ordering principle of natural numbers guarantees that if the base case holds and each step propagates the property, then all natural numbers have the property.

## Example

*To be written.*

## Related Concepts

- [Direct Proof](direct-proof.md)
- [Proof by Contrapositive](proof-by-contrapositive.md)
- [Recursion](recursion.md)
