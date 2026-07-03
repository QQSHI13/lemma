---
title: Recurrence Relation
area: foundations
prerequisites:
  - sequence
  - function
related:
  - recursion
  - proof-by-induction
  - generating-function
difficulty: 2
status: draft
quality_score: 0
---

# Recurrence Relation

An equation that defines a sequence based on its previous terms.

## Definition

A **recurrence relation** for a sequence $\{a_n\}$ is an equation of the form:

$$a_n = f(a_{n-1}, a_{n-2}, \ldots, a_{n-k})$$

## Example: Fibonacci Sequence

$$F_n = F_{n-1} + F_{n-2} \quad \text{with} \quad F_0 = 0, F_1 = 1$$

## Related Concepts

- [Recursion](recursion.md)
- [Proof by Induction](proof-by-induction.md)
