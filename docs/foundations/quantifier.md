---
title: Quantifier
area: foundations
difficulty: 1
prerequisites:
  - proposition
  - set
related:
  - predicate
  - truth-table
tags:
  - foundations
  - logic
  - definition
---

# Quantifier

## Definition

A **quantifier** is a logical operator that specifies the quantity of elements in a domain that satisfy a given predicate.

## Types

### Universal Quantifier ($\forall$)

$$\forall x \in S, P(x)$$

"For all $x$ in $S$, property $P$ holds."

### Existential Quantifier ($\exists$)

$$\exists x \in S, P(x)$$

"There exists an $x$ in $S$ such that property $P$ holds."

### Uniqueness Quantifier ($\exists!$)

$$\exists! x \in S, P(x)$$

"There exists exactly one $x$ in $S$ such that $P$ holds."

## Negation

| Original | Negation |
|----------|----------|
| $\forall x, P(x)$ | $\exists x, \neg P(x)$ |
| $\exists x, P(x)$ | $\forall x, \neg P(x)$ |

## Examples

### Example 1
$$\forall n \in \mathbb{N}, n \geq 0$$

"Every natural number is non-negative."

### Example 2
$$\exists n \in \mathbb{N}, n \text{ is even}$$

"There exists an even natural number." (True: $n = 2$)

## Related

- [Proposition](proposition.md) — Simple statements without quantifiers
- [Set](set.md) — The domain of quantification
- [Truth Table](truth-table.md) — Quantifiers extend propositional logic
