# Subset

## Definition

A set $A$ is a **subset** of a set $B$, written $A \subseteq B$, if every element of $A$ is also an element of $B$.

$$A \subseteq B \iff \forall x \, (x \in A \implies x \in B)$$

## Properties

### Reflexivity
For any set $A$:
$$A \subseteq A$$

### Transitivity
If $A \subseteq B$ and $B \subseteq C$, then $A \subseteq C$.

### Antisymmetry
If $A \subseteq B$ and $B \subseteq A$, then $A = B$.

## Proper Subset

$A$ is a **proper subset** of $B$, written $A \subsetneq B$, if $A \subseteq B$ and $A \neq B$.

## Examples

### Example 1
$$\{1, 2\} \subseteq \{1, 2, 3\}$$

### Example 2
$$\{1, 2, 3\} \subseteq \{1, 2, 3\}$$ (but not proper)

### Example 3
$$\emptyset \subseteq A$$ for any set $A$.

## Theorem: Empty Set is Subset of Every Set

### Statement
For every set $A$, $\emptyset \subseteq A$.

### Proof
We must show: $\forall x \, (x \in \emptyset \implies x \in A)$.

Since $x \in \emptyset$ is always false, the implication is vacuously true.

**QED**

## Related

- [Set](set.md)
- [Union](union.md)
- [Intersection](intersection.md)
- [Power Set](power-set.md) — The set of all subsets
