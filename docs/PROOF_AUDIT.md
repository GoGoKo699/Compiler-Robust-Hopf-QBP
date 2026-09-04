# Internal proof audit: optimal all-workspace Hopf-frame compilation

[← Complete compiler theorem](COMPILER_THEOREM.md) · [Verification](VERIFICATION.md) · [Clean-room reconstruction →](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md)

## Status and audit question

This document records an internal proof audit of the complete compiler theorem.
It is not external peer review.

The audit question is:

> Does the structured Hopf-frame completion attain the optimal arbitrary-state-
> preparation frontier using only the declared clean workspace, while preserving
> every logical marker column and returning all work registers exactly to zero?

No blocking operator, workspace, size, depth, endpoint, inverse, chart-domain,
router, or complex-magnitude problem was found. Under the exact circuit model
and the imported Yuan–Zhang primitives, the audited theorem is

```math
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(2^n),
```

```math
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every integer `m>=0`.

## 1. Source and circuit-model discipline

The active external framework is P. Yuan and S. Zhang, *Quantum* **7**, 956
(2023):

- Theorem 2: optimal QSP size–depth frontier;
- Lemma 5: exact ancilla-free multi-controlled `X`;
- Lemma 6: exact all-workspace UCG synthesis;
- Lemma 9: coherent CNOT copy–use–uncopy.

The published article corresponds to `arXiv:2202.11302v2`. The imported
statements were checked in v3 and retain the forms used here. The earlier
state-preparation paper remains the historical predecessor and original-source
reference for selected primitives. The active proof does not switch between the
two papers according to workspace budget.

The exact logical model consists of arbitrary one-qubit gates and CNOTs with
all-to-all connectivity. Toffoli, Fredkin, controlled one-qubit gates, and
fixed-width controlled Givens rotations are constant-width readable primitives
with exact constant-size, constant-depth decompositions in that model.

**Audit classification:** source versions and model assumptions recorded.

## 2. Structured operator target

The real Hopf frame satisfies

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
```

```math
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

For unrestricted magnitude angles,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where `a_j` is the oriented incoming amplitude. On the canonical Hopf domains,
`a_j>=0` and equals the principal metric square root. At `g_(j,j)=0`, the raw
differential vanishes while the marker column remains a chart-selected
orthogonal frame direction determined by the complete parameter tuple.

At tree depth `d`, the complete addressed layer is

```math
L_d
=I+
\sum_p|p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The full frame is the ordered product of these layers.

**Audit classification:** geometric and operator conventions cross-checked by
independent recursive and addressed constructions.

## 3. Frame-safe compiler contract

Let `J` append the clean workspace. The required contract is

```math
\widetilde WJ=JW
```

on every system input. Since the clean subspace is mapped unitarily onto itself,
it is reducing, and

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

The complete global Hopf record is therefore preserved.

The two-qubit obstruction gives a strict separation from first-column equality:
two exact preparation completions share the state column but place the objective
response on different marker columns, changing the decoded gradient from
`(2,0,0)` to `(0,sqrt(2),0)`.

**Audit classification:** complete operator contract proved and enforced by an
exact counterexample.

## 4. Schedule Z: strict zero workspace

At a nonfinal depth, split the suffix into original logical bit `b` and
remaining string `r`, and define

```math
h=[r=0],
\qquad
C=R_y(\theta_p/2),
\qquad
J=X.
```

The chronological sequence

```text
controlled_b(J), T_h, controlled_b(C), T_h,
controlled_b(J), T_h, controlled_b(C), T_h
```

uses

```math
C^2=R_y(\theta_p),
\qquad
JCJ=C^{-1},
\qquad
CJCJ=I.
```

The four `(h,b)` sectors apply the addressed rotation only when the original
complete suffix is zero. The logical bit is restored, and no relative phase is
introduced. Orthogonality of the sectors proves complete operator equality on
arbitrary entangled inputs.

The two UCGs have total width `d+2`. The predicate toggles use no ancillary wire.
Thus

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

Summing the layers and applying the real-state parameter lower bound gives

```math
S_{\mathbb R}(n,0)=\Theta(2^n),
```

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{2^n}{n}\right).
```

**Audit classification:** proved relative to Lemmas 5–6 and tested as complete
operators.

## 5. Schedule P1: small positive workspace

For `m>=1`, each nonfinal depth may compute the full suffix-zero predicate into
one clean flag, apply one prefix-and-flag UCG, and uncompute the flag. The same
flag is reused between depths.

The direct schedule has

```math
S_{\mathrm{direct}}=O(2^n),
```

```math
D_{\mathrm{direct}}
=O\left(n^2+\frac{2^n}{n+m}\right).
```

When `1<=m<4n`, `n+m<5n`, and `n^3=O(2^n)`. The polynomial term is therefore
absorbed by `2^n/(n+m)`.

**Audit classification:** workspace endpoint and uniform absorption verified.

## 6. Tree-cut identities

For a cut after `t` depths, let

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

A local subtree node `(ell,u)` in branch `r` uses global breadth-first node

```math
2^{t+\ell}+r2^\ell+u.
```

These are complete operator identities. No state-column restriction enters.

**Audit classification:** algebraically proved and matrix-tested for every small
cut.

## 7. Conditioned-prefix decoder

The explicit reversible decoder implements

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle
```

using

```math
3B-2-t
```

clean qubits. Its X/CNOT/Toffoli schedule has disjoint layers, depth `11t-4`,
and size `O(B)`. On the one-hot code, the Hopf Givens pairs at one depth are
disjoint.

Computing and fanning out the external suffix-zero predicate, applying the
fixed-width controlled Givens layers, and reversing all work gives the
conditioned prefix in depth `O(n)` and size `O(B+s)`.

**Audit classification:** explicit reversible construction and encoded operator
action tested.

## 8. Explicit coherent router

The routed tail allocates:

- `(B-1)s` additional data wires;
- `B` activation-token wires;
- `C=(B-1)(s+1)-t` copied routing controls.

Treat each branch's data and token as a block of width `s+1`. At routing level
`j`, prefix bit `j` controls `2^j(s+1)` disjoint Fredkin gates. One original
prefix wire is available, leaving `2^j(s+1)-1` required copies. Summation yields
`C`, while the number of forward Fredkin gates is

```math
(B-1)(s+1).
```

Balanced CNOT trees create and erase the prefix copies. Processing prefix bits
from least to most significant routes an arbitrary state

```math
\sum_r c_r|r\rangle_P|\xi_r\rangle_S
```

coherently into the branch selected by `r`, including prefix–suffix-entangled
inputs.

After routing, all copies are zero. When `s>1`, the cleared copy pool contains
all `B` branch flags because

```math
C-B=(B-1)s-t-1\geq0
```

for `B=2^t`, `t>=1`, and `s>=2`. The token-controlled subtree frames act on
disjoint branch registers and run in parallel. Every flag is cleared, the prefix
copies are recreated, the Fredkin tree is reversed, the copies are erased, and
the root token is reset.

The explicit schedule and sparse-state simulator verify equality to the ideal
tail direct sum and zero leakage from data, token, copy, and flag registers.

**Audit classification:** explicitly constructed, counted, and operator-tested.

## 9. Workspace envelope and maximal cut

The tail peak is

```math
(B-1)s+B+
\max\left\{(B-1)(s+1)-t,\,B\right\}.
```

The conditioned prefix and tail run sequentially. Both fit inside

```math
2B(s+1).
```

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If `s=n-t>1`, failure of the next cut gives

```math
m<4\,2^t s,
```

and therefore

```math
\frac{2^s}{s}
=O\left(\frac{2^n}{n+m}\right).
```

The subtree polynomial term obeys

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

If `s=1`, every subtree frame has constant depth. Feasibility requires
`m>=2^{n+1}=2N`, so `2^n/(n+m)=O(1)` and the target depth is `Theta(n)`.

**Audit classification:** peak-workspace and endpoint inequalities checked by
integer ledgers.

## 10. Matching lower bounds

The first frame column covers an open real-state family of dimension `2^n-1`.
Parameter counting gives

```math
S=\Omega(2^n),
```

```math
D=\Omega\left(\frac{2^n}{n+m}\right).
```

The union of backward light cones of the `n` system outputs yields the independent
`Omega(n)` depth term. At `m=0`, the parameter bound `Omega(2^n/n)` already
dominates `n` asymptotically.

**Audit classification:** lower bounds rederived independently of the compiler.

## 11. Phase-dressed complex magnitude frame

The phase diagonal is one total-width-`n` UCG with blocks

```math
\mathrm{diag}(e^{i\phi_{z0}},e^{i\phi_{z1}}).
```

It has `O(2^n)` size and `O(n+2^n/(n+m))` depth. The real frame and phase UCG
return their workspaces clean and reuse one pool sequentially. The result applies
to the phase-dressed complex magnitude frame; leaf-phase derivatives remain a
separate direct stream.

**Audit classification:** proved relative to Lemma 6 and tested as a complete
operator.

## 12. Matched QBP consequence

Frame-safe inverse action preserves the complete global magnitude-record
distribution. The primary finite-shot target is simultaneous absolute accuracy
of the raw Hopf-coordinate gradient.

The scalar and gradient logical costs are compared as

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E(D_{\mathrm{prep}}+D_O),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}).
```

Since `D_frame` matches the general QSP order, the inverse frame adds only a
constant per-execution factor. At fixed comparable scalar and raw-coordinate
accuracy and confidence, the shared-record execution overhead is
`O(log n)=O(log log M)`.

The statement excludes classical output materialization and instance-specific
scalar shortcuts.

**Audit classification:** valid under the declared access and task conventions.

## 13. Evidence-level boundary

The repository distinguishes:

- complete dense logical operators for frames and strict-zero identities;
- explicit reversible layers for the decoder and router;
- exact logical block action for controlled subtree UCGs;
- imported elementary UCG and multi-controlled-`X` synthesis;
- integer and exact-rational resource ledgers.

Finite validation supports but does not replace the analytic theorem.

## 14. Audit conclusion

The all-workspace construction is internally coherent:

```text
strict-zero borrowed-suffix echo
+ direct positive-workspace suffix flag
+ clean binary–one-hot decoder
+ explicit coherent route–parallel-subframes–unroute
+ one-UCG phase dressing
+ matching state-preparation lower bounds.
```

Independent technical and prior-art assessment remains the next scientific
step. Hardware routing, approximate fault-tolerant synthesis, noise, and
application-specific controlled-observable cost remain outside the theorem.

---

[← Complete compiler theorem](COMPILER_THEOREM.md) · [Verification](VERIFICATION.md) · [Clean-room reconstruction →](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md)
