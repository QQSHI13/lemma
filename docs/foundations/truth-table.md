---
title: Truth Table
area: foundations
difficulty: 1
prerequisites:
  - proposition
  - logical-connective
related:
  - quantifier
  - boolean-algebra
tags:
  - foundations
  - logic
  - definition
---

# Truth Table

## Definition

A **truth table** is a systematic listing of all possible truth values for a logical expression, showing the output for every combination of inputs.

## Construction

For $n$ propositional variables, a truth table has $2^n$ rows.

## Example: AND

| $P$ | $Q$ | $P \land Q$ |
|-----|-----|-------------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

## Example: Implication

| $P$ | $Q$ | $P \implies Q$ |
|-----|-----|----------------|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

Note: $P \implies Q$ is false only when $P$ is true and $Q$ is false.

## Related

- [Proposition](proposition.md) — The basic building block
- [Logical Connective](logical-connective.md) — AND, OR, NOT, IMPLIES
- [Direct Proof](direct-proof.md) — Using truth tables to prove validity
