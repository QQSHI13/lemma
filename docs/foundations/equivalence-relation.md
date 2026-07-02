---
title: Equivalence Relation
area: foundations
difficulty: 2
prerequisites:
  - relation
  - set
  - reflexive
  - symmetric
  - transitive
related:
  - partition
  - quotient-set
  - congruence
  - isomorphism
tags:
  - foundations
  - sets
  - definition
---

# Equivalence Relation

## Definition

An **equivalence relation** on a set $A$ is a relation $\sim$ that is:

1. **Reflexive**: $\forall a \in A, a \sim a$
2. **Symmetric**: $\forall a, b \in A, a \sim b \implies b \sim a$
3. **Transitive**: $\forall a, b, c \in A, a \sim b \land b \sim c \implies a \sim c$

## Equivalence Class

For $a \in A$, the **equivalence class** of $a$ is:

$$[a] = \{x \in A : x \sim a\}$$

## Partition

The equivalence classes form a **partition** of $A$:
- Every element is in some class
- Classes are disjoint

## Examples

### Example 1: Equality
The equality relation $=$ is an equivalence relation.

$[a] = \{a\}$ for all $a \in A$.

### Example 2: Congruence Modulo $n$
$$a \equiv b \pmod{n} \iff n \mid (a - b)$$

This is an equivalence relation on $\mathbb{Z}$.

$[a] = \{\ldots, a-2n, a-n, a, a+n, a+2n, \ldots\}$

### Example 3: Same Parity
$$a \sim b \iff a \text{ and } b \text{ are both even or both odd}$$

Two equivalence classes: $[0]$ (even integers) and $[1]$ (odd integers).

## Related

- [Relation](relation.md) — The general concept
- [Set](set.md) — The underlying set
- [Cartesian Product](cartesian-product.md) — Where relations live
- [Direct Proof](direct-proof.md) — Proving the three properties
