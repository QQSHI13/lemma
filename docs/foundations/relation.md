---
title: Relation
area: foundations
difficulty: 2
prerequisites:
  - set
  - cartesian-product
  - element
related:
  - function
  - equivalence-relation
  - partial-order
  - binary-relation
  - reflexive
  - symmetric
  - transitive
tags:
  - foundations
  - sets
  - definition
---

# Relation

## Definition

A **relation** $R$ from a set $A$ to a set $B$ is a subset of the Cartesian product $A \times B$:

$$R \subseteq A \times B$$

If $(a, b) \in R$, we write $a \, R \, b$ or $R(a, b)$.

## Special Relations

| Property | Definition | Notation |
|----------|-----------|----------|
| Reflexive | $\forall a \in A, (a, a) \in R$ | $a \, R \, a$ |
| Symmetric | $(a, b) \in R \implies (b, a) \in R$ | $a \, R \, b \implies b \, R \, a$ |
| Transitive | $(a, b) \in R \land (b, c) \in R \implies (a, c) \in R$ | chain rule |
| Antisymmetric | $(a, b) \in R \land (b, a) \in R \implies a = b$ | partial order |

## Examples

### Example 1: Equality
$$R = \{(a, a) : a \in A\}$$

The equality relation on $A$ is reflexive, symmetric, and transitive.

### Example 2: Less Than on $\mathbb{R}$
$$R = \{(x, y) \in \mathbb{R}^2 : x < y\}$$

Transitive and antisymmetric, but not reflexive or symmetric.

### Example 3: Divisibility on $\mathbb{Z}^+$
$$R = \{(a, b) : a \text{ divides } b\}$$

Reflexive, transitive, antisymmetric. This is a partial order.

## Relation as a Matrix

For finite $A = \{a_1, \ldots, a_n\}$ and $B = \{b_1, \ldots, b_m\}$, a relation can be represented as an $n \times m$ matrix:

$$M_{ij} = \begin{cases} 1 & \text{if } a_i \, R \, b_j \\ 0 & \text{otherwise} \end{cases}$$

## Related

- [Cartesian Product](cartesian-product.md) — Relations live inside this
- [Function](function.md) — A special relation with exactly one output per input
- [Set](set.md) — The domain and codomain of a relation
- [Proposition](proposition.md) — Properties of relations are propositions
- [Direct Proof](direct-proof.md) — Proving relation properties
