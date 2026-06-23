# Set

## Definition

A **set** is a well-defined collection of distinct objects, considered as an object in its own right.

Formally, a set $S$ is determined by a property $P$ such that for any object $x$:

$$x \in S \iff P(x)$$

## Notation

| Symbol | Meaning |
|--------|---------|
| $x \in S$ | $x$ is an element of $S$ |
| $x \notin S$ | $x$ is not an element of $S$ |
| $\emptyset$ | The empty set (contains no elements) |
| $\{a, b, c\}$ | The set containing $a$, $b$, and $c$ |
| $\{x : P(x)\}$ | The set of all $x$ satisfying property $P$ |

## Properties

### Well-definedness
For any object $x$ and any set $S$, exactly one of the following holds: $x \in S$ or $x \notin S$.

### Distinctness
The elements of a set are distinct. $\{1, 1, 2\} = \{1, 2\}$.

### Unordered
The order of elements does not matter. $\{1, 2, 3\} = \{3, 1, 2\}$.

## Axioms (ZFC)

Modern set theory is built on the Zermelo-Fraenkel axioms with Choice (ZFC):

1. **Extensionality**: Two sets are equal if they have the same elements.
2. **Empty Set**: There exists a set with no elements.
3. **Pairing**: For any two sets, there is a set containing exactly those two.
4. **Union**: For any set of sets, there is a set containing all their elements.
5. **Power Set**: For any set, there is a set of all its subsets.
6. **Infinity**: There exists an infinite set.
7. **Separation**: Given a set and a property, there is a subset satisfying that property.
8. **Replacement**: The image of a set under a definable function is a set.
9. **Foundation**: Every non-empty set contains an element disjoint from itself.
10. **Choice**: Every set of non-empty sets has a choice function.

## Theorem: Uniqueness of the Empty Set

### Statement
There is exactly one empty set.

### Proof
By the Empty Set axiom, there exists a set $\emptyset$ with no elements.

Suppose $E$ is another set with no elements. By Extensionality, for any $x$:
$$x \in \emptyset \iff x \in E$$

Since both are false for all $x$, we have $\emptyset = E$.

**QED**

## Examples

### Example 1
$$A = \{1, 2, 3\}$$

$1 \in A$, $4 \notin A$.

### Example 2: Set-builder notation
$$B = \{n \in \mathbb{N} : n \text{ is even}\}$$

$B$ is the set of all even natural numbers.

### Example 3: The empty set
$$\emptyset = \{\}$$

Note: $\emptyset \neq \{\emptyset\}$. The latter is a set containing one element (the empty set).

## Related

- [[ref:Element]] — Membership relation
- [[ref:Subset]] — Containment
- [[ref:Union]] — Combining sets
- [[ref:Intersection]] — Common elements
- [Cartesian Product](cartesian-product.md) — Pairs of elements
