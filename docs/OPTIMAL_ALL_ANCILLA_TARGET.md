# Optimal all-ancilla target

## 1. Current benchmark

Yuan and Zhang proved that arbitrary `n`-qubit state preparation with `m` clean
ancillary qubits has optimal depth and size

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right),
\qquad
S_{\mathrm{QSP}}(n,m)=\Theta(2^n)
```

for every `m>=0`. Their controlled state-preparation construction also achieves

```math
O\left(n+k+\frac{2^{n+k}}{n+k+m}\right)
```

depth for `k` control qubits and `m` ancillary qubits.

Reference: P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023),
[arXiv:2202.11302](https://arxiv.org/abs/2202.11302).

## 2. Gap left by the current Hopf-frame compiler

The audited real and separated complex constructions give

```math
D_{\mathrm{frame}}(n,m)
=O\left(n(n-t+1)+\frac{2^n}{n+m}\right),
```

where

```math
t=
\min\left\{
n,
\max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\}.
```

They match the optimal QSP scale in the low-workspace and linear-workspace
regimes, but may be larger by `O(log n)` in the intermediate regime.

The uniform comparison requires a case split; it does not follow from claiming
`n-t=O(log n)` for every `m`.

### Low workspace

When

```math
m\leq\frac{2^n}{n^2},
```

the geometric term is at least of order `n**2`, up to finite small-`n`
constants. It absorbs the sequential term `O(n**2)`, so the frame-to-QSP depth
ratio is `O(1)`.

### Remaining workspace

When

```math
m>\frac{2^n}{n^2},
```

```math
\log_2m>n-2\log_2n,
```

and therefore `n-t=O(log n)`. Since

```math
\frac{n(n-t+1)+G}{n+G}
\leq n-t+1,
\qquad
G=\frac{2^n}{n+m},
```

the ratio is `O(log n)`.

Consequently, uniformly over all `m`,

```math
\boxed{
\frac{D_{\mathrm{frame}}(n,m)}
{D_{\mathrm{QSP}}(n,m)}
=O(\log n).
}
```

For `M=Theta(2**n)` Hopf coordinates, this compiler-depth overhead is
`O(log log M)`. This is already a strong compiler-robust result, but it is not
the strongest possible theorem.

## 3. Primary research question

Determine whether the complete clean Hopf differential frame satisfies

```math
\boxed{
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
}
```

for every ancillary budget.

There are two scientifically meaningful outcomes.

### Outcome A: optimal frame compilation

Construct a frame-safe circuit attaining the QSP frontier. Since applying the
frame to `|0>` prepares an arbitrary Hopf state, an appropriate state-preparation
lower bound should transfer, producing an optimality theorem for a complete
moving frame rather than one state column.

### Outcome B: a genuine frame/state separation

Prove that clean coherent access to all Hopf tangent columns requires greater
depth or workspace than preparing the state alone in some regime. This would
identify a resource cost intrinsic to quantum differentiation.

Either outcome would be a central theorem for the new paper.

## 4. Why controlled state preparation is relevant but not sufficient

The optimal controlled-QSP theorem implements

```math
|i\rangle|0^n\rangle
\longmapsto
|i\rangle|\psi_i\rangle
```

for a family of target states. The Hopf frame instead requires an in-place
unitary whose columns are the state and an organized set of tangent vectors:

```math
|0\rangle\mapsto|\psi\rangle,
\qquad
|\lambda(j)\rangle\mapsto|e_j\rangle.
```

Naively preparing a different output state in a fresh target register leaves the
input index present and does not implement this frame unitary. Erasing or
swapping the index without losing coherence is the nontrivial bridge.

The optimal CQSP theorem therefore provides powerful compiler primitives and a
benchmark, but it does not automatically solve frame compilation.

## 5. Candidate routes

### Route 1: recursive controlled subframes

Exploit the exact conditioned-prefix identity and compile larger blocks of Hopf
subframes recursively, using optimal controlled state preparation only for
cleanly isolated subspaces.

### Route 2: direct parallelization of addressed Givens layers

Replace the current sequential tail UCG schedule by a global routing and control
layout that shares predicate computations and balances all tree depths under the
same workspace budget.

### Route 3: frame-to-CQSP reduction

Seek an exact clean reduction from the Hopf frame to one or a constant number of
controlled-state-preparation calls plus reversible index transformations. The
reduction must return every index and work register to zero.

### Route 4: lower-bound obstruction

Use parameter counting, light-cone arguments, or clean-workspace constraints to
show that a complete orthogonal frame cannot always be realized at the state
column's optimum.

## 6. Required proof checks

Any proposed optimal compiler must establish all of the following:

1. Full clean-frame action on arbitrary system inputs.
2. No workspace leakage.
3. Uniform validity at singular Hopf coordinates.
4. Exact size, depth, and ancillary counts in one circuit model.
5. Reversibility with the same resources.
6. Compatibility with the audited common-workspace complex phase layer.
7. Output-sensitive magnitude and phase decoder accounting.
8. A lower bound for the same state class and workspace convention.

## 7. Stop conditions

Do not claim the optimal theorem from:

- equality of only the prepared state;
- finite numerical scaling fits;
- generic unitary synthesis, which costs too much;
- separately optimized subcircuits whose ancillary budgets cannot coexist;
- a controlled-state-preparation oracle that leaves the index entangled;
- asymptotic notation that hides an additional exponential workspace register.
