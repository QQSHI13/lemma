---
title: Direct Proof
area: foundations
difficulty: 1
prerequisites:
  - proof-by-contradiction
  - proof-by-contrapositive
  - proof-by-induction
related:
  - truth-table
  - quantifier
  - proposition
tags:
  - foundations
  - definition
---

# Direct Proof

## Definition

A **direct proof** is a method of proving a statement of the form $P \implies Q$ by assuming $P$ is true and deducing that $Q$ must therefore be true.

## Structure

To prove $P \implies Q$ directly:

1. **Assume** $P$ is true.
2. **Deduce** intermediate statements using definitions, axioms, and previously proved theorems.
3. **Conclude** that $Q$ is true.

## Why It Matters

Direct proof is the most straightforward proof technique. When it works, it provides the clearest path from hypothesis to conclusion.

## Theorem: Sum of Two Even Integers is Even

### Statement
For all integers $a$ and $b$, if $a$ is even and $b$ is even, then $a + b$ is even.

### Proof

Let $a$ and $b$ be even integers.

By the definition of even, there exist integers $k$ and $m$ such that:
$$a = 2k \quad \text{and} \quad b = 2m$$

Then:
$$a + b = 2k + 2m = 2(k + m)$$

Since $k + m$ is an integer, $a + b$ is of the form $2n$ where $n = k + m$.

Therefore, $a + b$ is even.

**QED**

## Theorem: Product of Two Odd Integers is Odd

### Statement
For all integers $a$ and $b$, if $a$ is odd and $b$ is odd, then $ab$ is odd.

### Proof

Let $a$ and $b$ be odd integers.

By definition, there exist integers $k$ and $m$ such that:
$$a = 2k + 1 \quad \text{and} \quad b = 2m + 1$$

Then:
$$\begin{aligned}
ab &= (2k + 1)(2m + 1) \\
&= 4km + 2k + 2m + 1 \\
&= 2(2km + k + m) + 1
\end{aligned}$$

Since $2km + k + m$ is an integer, $ab$ is of the form $2n + 1$.

Therefore, $ab$ is odd.

**QED**

## Theorem: If $n^2$ is Even, Then $n$ is Even

### Statement
For all integers $n$, if $n^2$ is even, then $n$ is even.

### Proof

We prove the contrapositive: if $n$ is odd, then $n^2$ is odd.

This follows directly from the theorem above (product of two odd integers is odd, and $n^2 = n \cdot n$).

Since the contrapositive is true, the original statement is true.

**QED**

## When to Use Direct Proof

Direct proof works best when:
- The conclusion follows naturally from the hypothesis
- There is a clear chain of implications from $P$ to $Q$
- The definitions provide an immediate path forward

## When Direct Proof Fails

Direct proof may not work when:
- The path from $P$ to $Q$ is not obvious
- You need to reason about what happens when $Q$ is false
- The statement involves existence or universal quantification in a complex way

In such cases, consider:
- [Proof by Contradiction](proof-by-contradiction.md)
- [Proof by Contrapositive](proof-by-contrapositive.md)
- [Proof by Induction](proof-by-induction.md)
- [Truth Table](truth-table.md) — For analyzing logical validity
- [Quantifier](quantifier.md) — For formalizing statements with FOR ALL and EXISTS

## Related

- [Proposition](proposition.md) — What we prove
- [Proof by Contradiction](proof-by-contradiction.md) — Alternative technique
- [Proof by Contrapositive](proof-by-contrapositive.md) — Alternative technique
- [Proof by Induction](proof-by-induction.md) — Alternative technique
