---
title: Injection (One-to-One Function)
area: foundations
difficulty: 2
prerequisites:
  - function
  - set
  - element
related:
  - surjection
  - bijection
  - composition
  - inverse
tags:
  - foundations
  - sets
  - definition
---

# Injection (One-to-One Function)

## Definition

A function $f: A \to B$ is an **injection** (or **one-to-one**) if:

$$\forall a_1, a_2 \in A, f(a_1) = f(a_2) \implies a_1 = a_2$$

Equivalently: distinct inputs map to distinct outputs.

## Examples

### Example 1: $f(x) = 2x$ on $\mathbb{R}$
$$f(x_1) = f(x_2) \implies 2x_1 = 2x_2 \implies x_1 = x_2$$

This is an injection.

### Example 2: $f(x) = x^2$ on $\mathbb{R}$
$$f(1) = f(-1) = 1$$

Not an injection (unless domain is restricted to $[0, \infty)$).

### Example 3: Identity Function
$id_A: A \to A$ is always an injection.

## Composition of Injections

If $f: A \to B$ and $g: B \to C$ are injections, then $g \circ f: A \to C$ is an injection.

## Related

- [Function](function.md) — The general concept
- [Surjection](surjection.md) — Every output is hit (dual concept)
- [Bijection](bijection.md) — Both injection and surjection
- [Direct Proof](direct-proof.md) — Proving a function is injective
