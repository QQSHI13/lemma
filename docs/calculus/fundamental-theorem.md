---
title: Fundamental Theorem
area: calculus
difficulty: 1
prerequisites:

related:

tags:
  - calculus
  - theorem
  - definition
---

# Fundamental Theorem of Calculus

The fundamental theorem of calculus links the concept of differentiation with that of integration.

## Statement

!!! theorem "Fundamental Theorem of Calculus (Part 1)" {#thm:ftc1}
    If $f$ is continuous on $[a,b]$ and $F$ is an antiderivative of $f$, then:

    $$ \int_a^b f(x) , dx = F(b) - F(a) $$

!!! theorem "Fundamental Theorem of Calculus (Part 2)" {#thm:ftc2}
    If $f$ is continuous on $[a,b]$, then the function $g$ defined by:

    $$ g(x) = \int_a^x f(t) , dt $$

    is continuous on $[a,b]$ and differentiable on $(a,b)$, with $g'(x) = f(x)$.

## Proof

### Proof of Theorem 1

By [[thm:ftc2]], we know $g'(x) = f(x)$, so $g$ is an antiderivative of $f$. Let $F$ be any antiderivative of $f$, so $F(x) = g(x) + C$. Then:

$$ F(b) - F(a) = (g(b) + C) - (g(a) + C) = g(b) - g(a) $$

$$ g(b) - g(a) = \int_a^b f(t) , dt - \int_a^a f(t) , dt = \int_a^b f(t) , dt $$

Thus $F(b) - F(a) = \int_a^b f(x) , dx$.

### Proof of Theorem 2

For $x \in (a,b)$:

$$ g'(x) = \lim_{h \to 0} \frac{g(x+h) - g(x)}{h} = \lim_{h \to 0} \frac{\int_x^{x+h} f(t) , dt}{h} $$

By the mean value theorem for integrals, there exists $c \in [x, x+h]$ such that:

$$ \int_x^{x+h} f(t) , dt = f(c) \cdot h $$

Therefore $g'(x) = \lim_{h \to 0} f(c) = f(x)$, by continuity of $f$.

## Key Equation

$$ \frac{d}{dx} \int_a^x f(t) , dt = f(x) $$

## Applications

### Computing a Definite Integral

$$ \int_0^1 x^2 , dx = \left[ \frac{x^3}{3} \right]_0^1 = \frac{1}{3} $$

### Relationship with Area

The integral $\int_a^b f(x) , dx$ represents the net signed area under the curve $y = f(x)$ from $x = a$ to $x = b$.

## Related

- [[ref:Limit of a Function]] — Foundation for continuity
- [[ref:Continuity]] — Required for FTC
- [[ref:Derivative]] — Inverse operation
- [[ref:Mean Value Theorem]] — Used in proof of FTC part 2