---
title: Recursion
area: foundations
prerequisites:
  - natural-number
  - function
related:
  - proof-by-induction
  - recurrence-relation
  - algorithm
difficulty: 2
status: draft
quality_score: 0
---

# Recursion

A method where a function calls itself to solve a problem by breaking it into smaller subproblems.

## Definition

A **recursive** definition specifies:
1. **Base case(s)**: Simple cases that can be solved directly
2. **Recursive case**: The solution is defined in terms of smaller instances of the same problem

## Example: Factorial

$$n! = \begin{cases} 1 & \text{if } n = 0 \\ n \cdot (n-1)! & \text{otherwise} \end{cases}$$

## Related Concepts

- [Proof by Induction](proof-by-induction.md)
- [Recurrence Relation](recurrence-relation.md)
- [Algorithm](algorithm.md)
