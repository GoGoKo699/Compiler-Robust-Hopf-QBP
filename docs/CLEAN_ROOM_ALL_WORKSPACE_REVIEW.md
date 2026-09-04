# Clean-room reconstruction of the optimal all-workspace Hopf-frame compiler

[← Verification](VERIFICATION.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Internal proof audit](PROOF_AUDIT.md)

## Status

This document records a third internal proof review. The theorem is reconstructed
from the operator target and the cited elementary synthesis statements rather
than from the chronological development of the repository.

It is not external peer review, and it is not a legal novelty opinion.

**Verdict.** No blocking operator, workspace, size, depth, endpoint, inverse,
chart-domain, router, or complex-magnitude error was found. Under the exact
circuit model stated below, the reconstructed result is

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

Here `W_(C,mag)=D_ph W_R` is the phase-dressed complex magnitude frame. The
complex leaf-phase derivatives remain a separate direct measurement stream.
Independent specialist review remains the appropriate final scientific check.

## 1. Reconstruction order

The argument was rebuilt in the following order.

1. Define the synthesis task as a structured complete-unitary problem between
   QSP and generic unitary synthesis.
2. Fix the complete addressed Hopf-layer operator rather than the prepared state
   column.
3. Separate unrestricted oriented incoming amplitudes from canonical metric
   square roots and inspect singular coordinates.
4. Derive the strict-zero echo sector by sector, writing chronological and
   matrix orders separately.
5. Recount every UCG participant and predicate-control wire.
6. Derive the positive-workspace tree cut and conditioned prefix.
7. Reconstruct the explicit CNOT/Fredkin router and its live-register peak.
8. Prove the maximal-cut upper bound and the real-state lower bounds.
9. Add the phase-dressed complex magnitude frame.
10. Verify that frame-safe inverse action is the only compiler input needed by
    the global Hopf record.

Finite tests are treated as regression evidence. They are not the logical basis
of the asymptotic theorem.

## 2. Imported circuit results

The active external framework is P. Yuan and S. Zhang, *Quantum* **7**, 956
(2023). The reconstruction uses:

- arbitrary one-qubit gates and CNOTs with all-to-all logical connectivity;
- Lemma 5: exact ancilla-free multi-controlled `X` with linear size and depth;
- Lemma 6: a total-width-`q` UCG using `w` clean work qubits has size `O(2^q)`
  and depth `O(q+2^q/(q+w))`;
- Lemma 9: balanced coherent CNOT copy–use–uncopy;
- Theorem 2: exact arbitrary QSP has size `Theta(2^n)` and depth
  `Theta(n+2^n/(n+m))` for every clean-workspace budget.

The published article corresponds to `arXiv:2202.11302v2`. The imported
statements were checked in v3 and retain the forms used here. Toffoli, Fredkin,
controlled one-qubit gates, and fixed-width controlled Givens rotations admit
constant-size, constant-depth exact decompositions in the same model.

The earlier state-preparation paper remains the historical predecessor and
original-source reference for selected primitives. The later all-workspace
theorem supplies the uniform framework used in every schedule.

## 3. Structured operator target

Let `N=2^n`. The real Hopf frame satisfies

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
g_{j,j}=a_j^2.
```

On the canonical domains, `a_j>=0` and equals the principal metric square root.
At zero metric weight, the raw differential vanishes while the marker column
remains a chart-selected orthogonal frame direction determined by the complete
parameter tuple.

At a nonfinal depth `d`, write the system register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R.
```

The required addressed layer is

```math
L_d
=I+
\sum_p|p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_p)-I\bigr)
\otimes|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

This equation fixes the complete action on the logical Hilbert space.

## 4. Frame-safe compiler contract

Let `J` append the clean workspace. The compiler must satisfy

```math
\widetilde WJ=JW.
```

Since the clean-input subspace is mapped unitarily onto itself, it is reducing,
and

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

The reverse circuit can therefore use the compiled inverse frame without
changing the logical premeasurement state.

First-column equality is strictly weaker. The exact two-qubit construction
preserves the state column while exchanging two marker columns and changes the
decoded gradient from `(2,0,0)` to `(0,sqrt(2),0)`.

## 5. Strict-zero borrowed-suffix echo

Set

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_p/2),
```

and let `T_h` toggle the original system qubit `b` iff `h(r)=1`. Apply
chronologically

```text
controlled_b(X)
T_h
controlled_b(C_p)
T_h
controlled_b(X)
T_h
controlled_b(C_p)
T_h.
```

The identities

```math
C_p^2=R_y(\theta_p),
\qquad
XC_pX=C_p^{-1}
```

give the following invariant sectors.

| `h(r)` | original `b` | target word | result | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_pXC_pX=I` | 1 |
| 1 | 0 | `C_p,C_p` | `R_y(theta_p)` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

The desired rotation appears only when the original complete suffix is zero.
The borrowed logical bit is restored, and no relative phase remains. Orthogonal
sector decomposition extends the identity to arbitrary superpositions and
entangled inputs.

`T_h` is an ancilla-free negative-control multi-controlled `X`. Each half-angle
UCG has `d` prefix controls, one borrowed-bit control, and one target, so

```math
q=d+2.
```

Therefore

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

Summing the addressed layers gives

```math
S_{\mathbb R}(n,0)=O(2^n),
```

```math
D_{\mathbb R}(n,0)
=O\left(n+\frac{2^n}{n}\right).
```

The real-state parameter family supplies matching lower bounds.

## 6. Direct positive-workspace schedule

For `m>=1`, the complete lower-suffix-zero predicate can instead be computed
into one clean reusable flag. One prefix-and-flag UCG is applied and the flag is
uncomputed at each nonfinal depth.

The schedule has

```math
S_{\mathrm{direct}}=O(2^n),
```

```math
D_{\mathrm{direct}}
=O\left(n^2+\frac{2^n}{n+m}\right).
```

When `1<=m<4n`, `n+m<5n` and `n^3=O(2^n)`, so the polynomial term is absorbed
by `2^n/(n+m)`.

## 7. Tree-cut identities

For a cut after `t` depths, put

```math
B=2^t,
\qquad
s=n-t.
```

The exact factorization is

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

with

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
`2^(t+ell)+r2^ell+u`.

These are complete-operator identities.

## 8. Conditioned-prefix decoder

The explicit reversible decoder implements

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle
```

using

```math
3B-2-t
```

clean qubits, depth `O(t)`, and size `O(B)`. On the one-hot code, the Givens
pairs at each Hopf depth are disjoint. Computing and fanning out the external
suffix predicate yields the conditioned prefix in `O(n)` depth and `O(B+s)`
size.

## 9. Explicit coherent router

The routed tail allocates `(B-1)s` additional data wires, `B` activation tokens,
and

```math
C=(B-1)(s+1)-t
```

copied routing controls.

Treat each branch's data and token as a block of width `s+1`. At routing level
`j`, prefix bit `j` controls `2^j(s+1)` disjoint Fredkin gates. Balanced CNOT
trees provide the needed control copies. Processing the prefix bits from least
to most significant routes the data-token block into the prefix-selected branch
coherently on arbitrary entangled input.

After routing, all copies are uncomputed. When `s>1`, the same clean pool holds
all branch flags because

```math
C-B=(B-1)s-t-1\geq0.
```

All token-controlled subtree frames act on disjoint branch registers. The flags
are cleared, prefix copies recreated, the Fredkin tree reversed, the copies
erased, and the root token reset.

The explicit schedule and sparse-state simulator verify equality to the ideal
direct sum and zero leakage from every work register.

The conditioned prefix and tail each fit inside

```math
2B(s+1)
```

clean ancillary qubits.

## 10. Maximal-cut depth

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If `s=n-t>1`, failure of the next cut gives

```math
m<4\,2^t s,
```

hence

```math
\frac{2^s}{s}
=O\left(\frac{2^n}{n+m}\right).
```

Also,

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

If `s=1`, the subtree frames have constant depth and feasibility implies
`m>=2^{n+1}=2N`, so the target depth is `Theta(n)`.

The routed schedule therefore has

```math
S_{\mathrm{routed}}=O(2^n),
```

```math
D_{\mathrm{routed}}
=O\left(n+\frac{2^n}{n+m}\right).
```

## 11. Matching lower bounds

The first frame column covers an open real-state family of dimension `2^n-1`.
Parameter counting gives

```math
S=\Omega(2^n),
```

```math
D=\Omega\left(\frac{2^n}{n+m}\right).
```

Backward light cones of the `n` system outputs give the independent
`Omega(n)` term. At `m=0`, `Omega(2^n/n)` already dominates `n`.

Thus the upper and lower bounds match in every workspace regime.

## 12. Phase-dressed complex magnitude frame

Writing `x=zb`, the phase layer is

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|
\otimes
\mathrm{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

This is one total-width-`n` UCG. The real frame and phase UCG return the same
workspace pool clean and reuse it sequentially. The real subfamily supplies the
lower bounds.

The theorem therefore extends to `W_(C,mag)`. The direct leaf-phase record is a
separate algorithmic stream.

## 13. QBP consequence

Complete frame safety preserves the global inverse-frame measurement
distribution. For simultaneous absolute accuracy of the raw coordinate
gradient, the shared magnitude record uses

```math
O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\right)
```

executions.

The scalar and gradient costs are compared for matched programs using the same
state family and controlled observable. Since the inverse frame has the same
general-family depth order as optimal state preparation, the displayed
fixed-accuracy overhead is `O(log n)=O(log log M)`. Classical output
materialization and instance-specific scalar shortcuts are outside that ratio.

## 14. Contribution boundary

The strict-zero circuit combines familiar ingredients: controlled-unitary
roots, Pauli conjugation, UCGs, borrowed or conditionally clean logical qubits,
toggle detection, and ancilla-free multi-controlled gates.

The narrow project-specific statement is the use of one original suffix bit as
a restored predicate carrier to reduce one addressed Hopf depth to two
width-`d+2` UCGs and linear predicate toggles, together with the resulting
optimal complete-frame frontier.

## 15. Clean-room conclusion

The reconstruction found no reason to retain an `m>=1` exception or to weaken
the complete-frame theorem. The internally supported result is

```math
\boxed{
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(2^n),
\qquad
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
}
```

for every integer `m>=0`.

The router and decoder are explicit reversible constructions. Frame and
strict-zero identities are checked as complete operators. UCG and
multi-controlled-`X` elementary synthesis is imported from the state-preparation
framework. Resource bounds are checked by integer or exact-rational ledgers.

Independent specialist review remains the next scientific gate.

---

[← Verification](VERIFICATION.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Internal proof audit](PROOF_AUDIT.md)
