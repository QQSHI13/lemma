---
title: Complement
area: foundations
difficulty: 1
prerequisites:
  - set
  - element
related:
  - union
  - intersection
  - subset
tags:
  - foundations
  - sets
  - definition
---

# Complement

## Definition

The **complement** of a set $A$ (with respect to a universal set $U$) is the set of all elements in $U$ that are not in $A$:

$$A^c = \{x \in U : x \notin A\}$$

## Notation

| Symbol | Meaning |
|--------|---------|
| $A^c$ | Complement of $A$ |
| $\overline{A}$ | Alternative notation |
| $U \setminus A$ | Set difference with universal set |

## Properties

### Involution
$$(A^c)^c = A$$

The complement of the complement is the original set.

### De Morgan's Laws

$$(A \cup B)^c = A^c \cap B^c$$
$$(A \cap B)^c = A^c \cup B^c$$

## Examples

### Example 1
Let $U = \{1, 2, 3, 4, 5\}$ and $A = \{1, 2\}$.

Then $A^c = \{3, 4, 5\}$.

### Example 2
Let $U = \mathbb{R}$ and $A = \{x : x > 0\}$.

Then $A^c = \{x : x \leq 0\}$.

## Related

- [Set](set.md) — The fundamental concept
- [Union](union.md) — Combining sets
- [Intersection](intersection.md) — Common elements
- [Subset](subset.md) — Containment relation
