---
title: Cartesian Product
area: foundations
difficulty: 2
prerequisites:
  - set
  - element
  - ordered-pair
related:
  - relation
  - function
  - tuple
tags:
  - foundations
  - sets
  - definition
---

# Cartesian Product

## Definition

The **Cartesian product** of two sets $A$ and $B$, denoted $A \times B$, is the set of all ordered pairs where the first element is from $A$ and the second is from $B$:

$$A \times B = \{(a, b) : a \in A, b \in B\}$$

## Generalization

For $n$ sets $A_1, A_2, \ldots, A_n$:

$$A_1 \times A_2 \times \cdots \times A_n = \{(a_1, a_2, \ldots, a_n) : a_i \in A_i\}$$

## Properties

### Cardinality
$$|A \times B| = |A| \cdot |B|$$

### Not Commutative
$$A \times B \neq B \times A \quad \text{(in general)}$$

### Not Associative
$$(A \times B) \times C \neq A \times (B \times C)$$

(though they are naturally isomorphic)

## Examples

### Example 1
Let $A = \{1, 2\}$ and $B = \{x, y\}$.

$$A \times B = \{(1, x), (1, y), (2, x), (2, y)\}$$

### Example 2: $\mathbb{R}^2$
$$\mathbb{R} \times \mathbb{R} = \mathbb{R}^2$$

The Euclidean plane.

## Related

- [Set](set.md) — The fundamental building block
- [Relation](relation.md) — A subset of a Cartesian product
- [Function](function.md) — A special kind of relation
