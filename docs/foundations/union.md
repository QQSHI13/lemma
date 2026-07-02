---
title: Union
area: foundations
difficulty: 1
prerequisites:
  - set
  - intersection
  - complement
related:

tags:
  - foundations
  - definition
---

# Union

## Definition

The **union** of two sets $A$ and $B$, written $A \cup B$, is the set of all elements that are in $A$ or in $B$ (or in both).

$$A \cup B = \{x : x \in A \lor x \in B\}$$

## Properties

### Commutativity
$$A \cup B = B \cup A$$

### Associativity
$$(A \cup B) \cup C = A \cup (B \cup C)$$

### Identity
$$A \cup \emptyset = A$$

### Idempotence
$$A \cup A = A$$

## Examples

### Example 1
$$\{1, 2\} \cup \{2, 3\} = \{1, 2, 3\}$$

### Example 2
$$\{a, b\} \cup \{c, d\} = \{a, b, c, d\}$$

## Related

- [Set](set.md)
- [Intersection](intersection.md) — Common elements
- [Complement](complement.md)
