# Compiler architecture at a glance

[← Theorem overview](THEOREM_OVERVIEW.md) · [Complete narrative](../REVIEW.md) · [Formal proof →](COMPILER_THEOREM.md)

This page shows how one exact state-preparation toolkit is adapted to a
prescribed Hopf completion.  The three workspace regimes are internal schedules
of one compiler.

Let

```math
N=2^n.
```

For every clean-workspace budget $m\geq0$,

```math
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(N),
```

```math
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

## 1. The local synthesis target

At tree depth $d$, the Hopf frame applies

```math
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The prefix chooses the rotation angle, the next bit is the target, and the
complete lower suffix supplies one shared all-zero predicate.  The equality is
required on every input column.

## 2. Compiler toolkit

The active exact compiler framework is P. Yuan and S. Zhang, *Quantum* **7**,
956 (2023).  The proof uses:

| Imported result | Use in the Hopf compiler |
|---|---|
| optimal QSP theorem | target size–depth frontier |
| ancilla-free multi-controlled X | suffix predicates and toggles |
| all-workspace UCG synthesis | prefix-selected rotations, subtree frames, and phase diagonal |
| coherent CNOT copy–uncopy | decoder and router fanout |

The complete-operator structure above determines how these primitives are
assembled.  The earlier state-preparation paper remains the historical
predecessor and original source of selected ingredients.

## 3. Schedule map

| Workspace | Schedule | Width or parallelism gained |
|---:|---|---|
| $m=0$ | borrowed-suffix echo | each nonfinal depth uses two UCGs of total width $d+2$ |
| $1\leq m<4n$ | direct clean flag | one shared suffix predicate reduces the UCG to prefix plus flag |
| $m\geq4n$ | tree cut and coherent routing | $2^t$ disjoint subtree frames run in parallel |

The threshold $4n$ is selected for a uniform asymptotic proof rather than as a
finite-size tuning rule.

## 4. Strict zero workspace

For one nonfinal depth, split the lower suffix into original bit $b$ and
remaining string $r$.  Set

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

The chronological sequence

```text
controlled_b(X)
T_h
controlled_b(C_p)
T_h
controlled_b(X)
T_h
controlled_b(C_p)
T_h
```

uses

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
XC_pX=C_p^{-1}.
```

The original complete-zero-suffix sector receives the full rotation.  The other
three sectors receive identity, and the original suffix bit is restored.

Each half-angle UCG has total width $d+2$; the predicate toggles are
ancilla-free multi-controlled X gates.  Therefore

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right),
```

which sums to the optimal strict-zero frontier.

## 5. Direct positive workspace

With one clean qubit, compute the complete lower-suffix-zero predicate into one
reusable flag, apply one prefix-plus-flag UCG, and uncompute the flag.

The complete direct schedule has

```math
S=O(N),
```

```math
D=O\left(n^2+\frac{N}{n+m}\right).
```

For $1\leqm<4n$, the $\frac{N}{n+m}$ term absorbs $n^2$, so no routed construction is
needed.

## 6. Tree cut and conditioned prefix

For larger workspace, cut after $t$ depths and define

```math
B=2^t,
\qquad
s=n-t.
```

The exact operator factorization is

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right),
```

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A reversible binary–one-hot decoder realizes the conditioned prefix using
$3B-2-t$ clean qubits, $O(t)$ decoder depth, and $O(B)$ size.

## 7. Coherent routed tail

Treat each branch's $s$ data wires and activation token as a block of width
$s+1$.  At routing level $j$, prefix bit $j$ controls $2^j(s+1)$ disjoint
Fredkin gates.  The exact counts are

```math
\text{copy wires}=(B-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(B-1)(s+1).
```

Balanced CNOT trees create the controls.  The Fredkin tree moves the
suffix-token block coherently to the branch selected by the prefix.  The copies
are then uncomputed and their cleared wires reused as local branch flags.

All subtree frames act on disjoint branch registers in parallel.  Every flag is
cleared; the copies are recreated; the route is reversed; copies and tokens are
reset.  The prefix and tail fit within

```math
2B(s+1)
```

clean ancillary qubits.

For the largest feasible cut, the subtree term obeys

```math
\frac{2^s}{s}
=O\left(\frac{N}{n+m}\right),
```

including the separate $s=1$ endpoint.  The routed schedule therefore reaches
the target frontier.

## 8. Complex magnitude frame

The leaf-phase diagonal is one total-width-$n$ UCG:

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
```

It is composed sequentially with $W_{\mathbb R}$ and reuses the same clean workspace.
The direct leaf-phase record remains a separate QBP stream.

## 9. Implementation map

| Component | File |
|---|---|
| addressed layers and frames | [`frames.py`](../compiler_robust_hopf/frames.py) |
| strict-zero echo | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py) |
| binary–one-hot decoder | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py) |
| coherent router | [`router.py`](../compiler_robust_hopf/router.py) |
| workspace dispatch and resource rows | [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| integer and rational inequalities | [`resource_bounds.py`](../compiler_robust_hopf/resource_bounds.py), [`strict_zero_audit.py`](../compiler_robust_hopf/strict_zero_audit.py) |

The [verification map](VERIFICATION.md) states which components are represented
as complete logical operators, explicit reversible layers, imported elementary
synthesis, or finite regression checks.

---

[← Theorem overview](THEOREM_OVERVIEW.md) · [Complete narrative](../REVIEW.md) · [Formal proof →](COMPILER_THEOREM.md)
