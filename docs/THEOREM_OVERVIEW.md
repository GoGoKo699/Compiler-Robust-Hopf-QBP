# Theorem map

[← Documentation index](README.md) · [Complete technical note](../REVIEW.md) · [Full compiler proof](COMPILER_THEOREM.md)

This page gives the shortest theorem-level route through the repository. It is
intended as a map, not as a replacement for the proofs.

## 1. Setting

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits. The exact logical model
uses arbitrary one-qubit gates and CNOTs with all-to-all connectivity. Toffoli,
Fredkin, controlled one-qubit, and fixed-width controlled Givens gates have
constant-size, constant-depth decompositions in this model.

The active external compiler line is represented by P. Yuan and S. Zhang,
*Quantum* **7**, 956 (2023). The proof imports Theorem 2 and Lemmas 5, 6, and 9.
The earlier state-preparation paper remains the historical predecessor and
original-source reference for selected primitives.

## 2. Structured unitary target

For the real Hopf chart,

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
```

```math
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

For unrestricted angles,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical domains, `a_j>=0` and `a_j=sqrt(g_(j,j))`. At zero metric
weight, the raw differential vanishes while the marker column remains a
chart-selected orthogonal frame direction.

The phase-dressed complex magnitude frame is

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

Leaf-phase derivatives use a separate direct record.

## 3. Frame-safe substitution

Let `J|varphi>=|varphi>|0^m>`. A compiled frame is frame-safe when

```math
\widetilde WJ=JW
```

on every system input. Unitarity makes the clean subspace reducing, so

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

The complete global Hopf record is therefore unchanged. An exact two-qubit
example shows that first-column equality alone can change the decoded gradient
from `(2,0,0)` to `(0,sqrt(2),0)`.

## 4. Strict-zero layer lemma

At a nonfinal depth, split the lower suffix into original bit `b` and remaining
string `r`. Let

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

The original logical bit `b` is restored on every input. No additional wire is
used.

Each nonfinal layer has

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

Summation and the real-state lower bound give

```math
S_{\mathbb R}(n,0)=\Theta(N),
```

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

## 5. Tree-cut lemmas

For a cut after `t` depths, put

```math
B=2^t,
\qquad
s=n-t.
```

Then

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

## 6. Clean prefix decoder

There is an explicit reversible circuit

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle
```

using

```math
3\,2^t-2-t
```

clean qubits, depth `O(t)`, and size `O(2^t)`. On the one-hot code, the Hopf
Givens pairs at one depth are disjoint. Adding the external suffix predicate
gives the conditioned prefix in `O(n)` depth and `O(2^t+s)` size.

## 7. Coherent routed tail

Treat each branch's `s` data wires and activation token as one block. The
explicit router uses

```math
(B-1)(s+1)-t
```

prefix-control copies and

```math
(B-1)(s+1)
```

forward Fredkin gates.

It coherently routes the suffix and token into the prefix-selected branch,
clears the control copies, runs all token-controlled subtree frames in parallel,
recreates the controls, reverses the route, and resets every work register.

The conditioned prefix and routed tail each fit in

```math
2B(s+1)
```

clean ancillary qubits.

## 8. Positive-workspace theorem

For `1<=m<4n`, the direct one-flag schedule gives

```math
S=O(N),
\qquad
D=O\left(n+\frac{N}{n+m}\right).
```

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

Maximality bounds the subtree term `2^s/s` by `O(N/(n+m))`. The explicit routed
construction has the same size and depth orders, including the `s=1` endpoint.

## 9. Matching lower bounds

The first frame column covers an open `(N-1)`-dimensional real-state family.
Parameter counting gives

```math
S=\Omega(N),
\qquad
D=\Omega\left(\frac{N}{n+m}\right).
```

Backward light cones of the `n` system outputs give the independent
`Omega(n)` depth term. At `m=0`, `Omega(N/n)` already dominates `n`.

## 10. All-workspace theorem

Combining the strict-zero, direct, and routed schedules with the lower bounds
gives, for every `m>=0`,

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The phase diagonal is one total-width-`n` UCG and reuses the real-frame
workspace sequentially. Therefore

```math
\boxed{
S_{\mathbb C,\mathrm{mag}}(n,m)=\Theta(N),
\qquad
D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

## 11. QBP corollary

The complete inverse-frame global record is unchanged under frame-safe
substitution. For simultaneous absolute accuracy of the raw coordinate
gradient, the magnitude stream uses

```math
O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\right)
```

executions.

At fixed comparable accuracy and confidence, matched scalar and gradient
programs satisfy

```math
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)=O(\log\log M),
```

because the compiled inverse frame has the same general-family depth order as
optimal state preparation. The comparison excludes classical output
materialization and instance-specialized scalar shortcuts.

## 12. Evidence boundary

The decoder and router are explicit reversible constructions. Frame and
strict-zero identities are checked as complete operators. UCG and
multi-controlled-`X` elementary synthesis is imported from the state-preparation
framework. Resource bounds use integer or exact-rational ledgers.

The complete proof is in [the compiler theorem](COMPILER_THEOREM.md), and the
implementation levels are listed in [Verification and evidence](VERIFICATION.md).

---

[← Documentation index](README.md) · [Complete technical note](../REVIEW.md) · [Full compiler proof](COMPILER_THEOREM.md)
