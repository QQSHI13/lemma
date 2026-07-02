---
title: Logical Connective
area: foundations
difficulty: 1
prerequisites:
  - proposition
  - truth-table
  - quantifier
related:

tags:
  - foundations
  - definition
---

# Logical Connective

## Definition

A **logical connective** is an operator that combines propositions to form new propositions.

## Basic Connectives

| Connective | Symbol | Meaning |
|-----------|--------|---------|
| Negation | $\neg P$ | NOT $P$ |
| Conjunction | $P \land Q$ | $P$ AND $Q$ |
| Disjunction | $P \lor Q$ | $P$ OR $Q$ |
| Implication | $P \implies Q$ | IF $P$ THEN $Q$ |
| Biconditional | $P \iff Q$ | $P$ IF AND ONLY IF $Q$ |

## Truth Tables

### Negation
| $P$ | $\neg P$ |
|-----|---------|
| T | F |
| F | T |

### Conjunction
| $P$ | $Q$ | $P \land Q$ |
|-----|-----|-------------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

### Disjunction
| $P$ | $Q$ | $P \lor Q$ |
|-----|-----|-------------|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

### Implication
| $P$ | $Q$ | $P \implies Q$ |
|-----|-----|---------------|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

Note: $P \implies Q$ is false **only** when $P$ is true and $Q$ is false.

## Properties

### De Morgan's Laws
$$\neg(P \land Q) \iff \neg P \lor \neg Q$$
$$\neg(P \lor Q) \iff \neg P \land \neg Q$$

### Contrapositive
$$P \implies Q \iff \neg Q \implies \neg P$$

## Related

- [Proposition](proposition.md)
- [Truth Table](truth-table.md)
- [Quantifier](quantifier.md)
