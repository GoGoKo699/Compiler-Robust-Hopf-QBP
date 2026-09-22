# Open problem: the two-clean high-precision endpoint

[Publication scope](../manuscript/PUBLICATION_SCOPE.md) · [Two-clean compiler](OPERATOR_SOURCE_COMPILER.md)

The publication establishes its compiler theorems without resolving this
endpoint. Let $`N=2^n`$, and let $`T^\star_{F,\mathbb R}`$ be the worst-case
minimum T-count for the prescribed real Hopf frame under the complete-input
error contract. At

```math
a=2,\qquad b=N+n+7,\qquad L=N,
```

the retained results give

```math
\Omega(N)\le T^\star_{F,\mathbb R}\le O(N\log N).
```

Here $`a`$ and $`b`$ count initialized clean and arbitrary dirty qubits, and
$`L=\max\{6,\lceil\log_2(1/\eta)\rceil\}`$ for
$`0<\eta\le1/64`$. Literal phases, clean-work leakage, and dirty/reference
return error are included in the same operator norm as the
[fault-tolerant theorem](FAULT_TOLERANT_COMPILER.md#1-target-resources-and-theorem).

The [operator-source compiler](OPERATOR_SOURCE_COMPILER.md) has
$`T=O(N+nL)`$ with $`b\ge L+n+7`$. It pays the precision cost at each
tree depth. Neither its dirty-bank refinement nor its literal-diagonal
corollary removes that repeated cost for a general real frame.

With a sufficiently large $`a=\Theta(n)`$ clean reservation and
$`b=\Theta(N)`$, the shared-source compiler instead attains
$`T^\star=\Theta(N)`$ at $`L=N`$. This sufficient clean reservation is
not proved necessary.

The open question is whether two clean qubits permit a jointly charged
$`O(N)`$ construction at the explicit allocation above, or whether a stronger
general lower bound holds. The current upper bound does not establish the
same cost for fewer clean qubits or every prefactor in $`b=\Theta(N)`$.
Restrictions proved for particular source-processing interfaces do not
settle the unrestricted frame problem.
