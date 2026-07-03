---
title: Composition
area: foundations
prerequisites:
  - function
related:
  - function
  - bijection
  - injection
  - surjection
difficulty: 1
status: draft
quality_score: 0
---

# Composition

The combination of two functions to create a new function.

## Definition

Given functions $f: A \to B$ and $g: B \to C$, the **composition** $g \circ f: A \to C$ is defined by:

$$(g \circ f)(x) = g(f(x))$$

## Properties

- Composition is **associative**: $(h \circ g) \circ f = h \circ (g \circ f)$
- Composition is **not commutative**: $g \circ f \neq f \circ g$ in general

## Related Concepts

- [Function](function.md)
- [Bijection](bijection.md)
