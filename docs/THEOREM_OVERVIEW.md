# Theorem overview

This page gives the shortest complete route through the mathematical claims. It
separates chart geometry, compiler correctness, all-workspace resource
optimality, and the matched quantum-backpropagation consequence.

## Notation and circuit model

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits. The exact logical model
uses arbitrary one-qubit gates and CNOTs with all-to-all connectivity. Toffoli,
Fredkin, and controlled one-qubit gates in explicit schedules have constant-size
and constant-depth decompositions in this model.

The sole active external compiler framework is Yuan–Zhang, *Quantum* **7**, 956
(2023). The published source is arXiv v2; Theorem 2 and Lemmas 5, 6, and 9 were
also checked in v3 and retain the statements used here. Sun et al. are the
historical predecessor.

## Theorem A: Hopf differential frame

For unrestricted magnitude angles, let `a_j` be the oriented incoming amplitude
to internal node `j`. Then

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical Hopf domains, `a_j>=0`, so `a_j=sqrt(g_(j,j))`. At
`g_(j,j)=0`, the raw differential vanishes while the unit marker column remains
a canonical frame continuation.

The real frame satisfies

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
\qquad
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

The phase-dressed complex magnitude frame is

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

Leaf-phase derivatives use a separate direct record.

## Theorem B: frame-safe substitution

Let `J|varphi>=|varphi>|0^m>`. A clean implementation is frame-safe when

```math
\widetilde WJ=JW
```

for every system input. Unitarity makes the clean subspace reducing, so

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

Substitution therefore preserves the complete global-QBP distribution. An
exact two-qubit example shows that first-column equality alone can change the
decoded gradient from `(2,0,0)` to `(0,sqrt(2),0)`.

## Lemma C: strict-zero borrowed-suffix echo

At a nonfinal addressed depth, split the suffix into original system bit `b` and
remaining string `r`. Let

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_p/2).
```

Four predicate toggles interleaved with two controlled half-angle rotations and
two target echoes implement the addressed layer exactly. The identities are

```math
C_p^2=R_y(\theta_p),
\qquad
XC_pX=C_p^{-1},
\qquad
C_pXC_pX=I.
```

The original `b` is restored on every input. No ancillary wire is used.

## Theorem D: optimal strict-zero frame

Each nonfinal layer has

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

Summation and the real-state parameter lower bound give

```math
S_{\mathbb R}(n,0)=\Theta(N),
```

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

## Lemma E: tree-cut identities

For a cut after `t` depths, set `B=2^t` and `s=n-t`. Then

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

Both are complete-operator identities.

## Lemma F: clean binary–one-hot decoder

There is an explicit reversible circuit

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle
```

using `3*2^t-2-t` clean qubits, depth `O(t)`, and size `O(2^t)`. Its X/CNOT/
Toffoli layers are supplied explicitly and tested for clean return.

## Lemma G: explicit coherent routed tail

Treat each branch's `s` data wires and activation token as a block of width
`s+1`. At routing level `j`, copy prefix bit `j` to control
`2^j(s+1)` disjoint Fredkin gates. The exact counts are

```math
\text{copy wires}=(B-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(B-1)(s+1).
```

The router coherently sends the original suffix and token to the prefix-selected
branch. After token-controlled subtree frames, every local flag is cleared,
the route is reversed, all copies and tokens are reset, and the transformed
suffix returns to the system register.

The explicit schedule and arbitrary-complex-input simulator are in
[`router.py`](../compiler_robust_hopf/router.py); complete operator and cleanup
tests are in [`test_router.py`](../tests/test_router.py).

The conditioned prefix and routed tail fit in

```math
2B(s+1)
```

clean ancillary qubits.

## Theorem H: optimal positive-workspace frame

For `1<=m<4n`, the direct flagged-UCG schedule has

```math
S=O(N),
\qquad
D=O\left(n+\frac{N}{n+m}\right).
```

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

Maximality bounds the subtree term `2^s/s` by `O(N/(n+m))`. The routed
construction therefore has the same size and depth orders.

The real-state parameter dimension gives `Omega(N)` size and
`Omega(N/(n+m))` depth. System-output backward light cones give `Omega(n)`
depth. Hence the upper bounds are optimal.

## Theorem I: optimal all-workspace real frame

Combining the strict-zero, direct, and routed schedules gives, for every
`m>=0`,

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

## Corollary J: phase-dressed complex magnitude frame

The phase diagonal is one exact `n`-qubit UCG:

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\mathrm{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

It reuses the real-frame workspace sequentially. Therefore

```math
\boxed{
S_{\mathbb C,\mathrm{mag}}(n,m)=\Theta(N),
\qquad
D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
}
```

for every `m>=0`.

## Corollary K: matched compiler-robust global QBP

The primary finite-shot target is simultaneous absolute accuracy of the raw
Hopf-coordinate gradient. At fixed accuracy and confidence, the global
magnitude stream uses `O(log n)=O(log log M)` independent executions.

Define matched logical costs

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E(D_{\mathrm{prep}}+D_O),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}).
```

Because `D_frame` has the same general-family asymptotic order as optimal state
preparation for every `m>=0`, adding the inverse frame changes per-execution
depth only by a constant factor. Under the same controlled-observable and
accuracy conventions,

```math
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)=O(\log\log M).
```

This excludes output materialization and is not a comparison with an
instance-specialized scalar shortcut. The best documented materialized decoder
cost is `O(S+N min{S,n})`.

## Theorem L: checkpoint active-interface substitution

For checkpoint factorization `U=B_dA_d`, let `P_d` be the active-interface
projector and `J` append clean workspace. The sufficient contract is

```math
\widetilde B_dJP_d=e^{i\chi}JB_dP_d.
```

Consistent forward and reverse use preserves designated checkpoint estimator
means. Equality on only one prepared prefix state is insufficient, while
active-interface equality need not preserve the complete output distribution.

## Evidence boundary

The router and decoder are explicit reversible constructions; strict-zero and
frame identities are checked as complete operators; UCG and multi-controlled-X
elementary synthesis are imported from Yuan–Zhang; resource bounds use integer
or exact-rational ledgers. Finite tests support but do not replace the analytic
proof.
