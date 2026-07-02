---
title: Function
area: foundations
difficulty: 2
prerequisites:
  - set
  - cartesian-product
  - relation
related:
  - injection
  - surjection
  - bijection
  - composition
  - inverse
tags:
  - foundations
  - sets
  - definition
---

# Function

## Definition

A **function** (or **mapping**) $f$ from a set $A$ to a set $B$ is a relation that assigns to each element of $A$ exactly one element of $B$.

$$f: A \to B$$

Formally, $f \subseteq A \times B$ such that for every $a \in A$, there exists exactly one $b \in B$ with $(a, b) \in f$.

## Notation

| Symbol | Meaning |
|--------|---------|
| $f: A \to B$ | $f$ is a function from $A$ to $B$ |
| $f(a)$ | The image of $a$ under $f$ |
| $A$ | Domain |
| $B$ | Codomain |
| $\{f(a) : a \in A\}$ | Range (or image) |

## Properties

### Well-definedness
For every $a \in A$, there exists exactly one $b \in B$ such that $f(a) = b$.

### Domain and Codomain
The domain is the set of all inputs. The codomain is the set of all possible outputs. The range is the set of actual outputs.

## Examples

### Example 1: Identity Function
$$id_A: A \to A, \quad id_A(a) = a$$

### Example 2: Square Function
$$f: \mathbb{R} \to \mathbb{R}, \quad f(x) = x^2$$

Range: $[0, \infty)$

### Example 3: Constant Function
$$g: A \to B, \quad g(a) = b_0 \text{ for all } a \in A$$

## Related

- [Cartesian Product](cartesian-product.md) — The domain of a function is a subset of this
- [Relation](relation.md) — A function is a special kind of relation
- [Set](set.md) — Functions map between sets
