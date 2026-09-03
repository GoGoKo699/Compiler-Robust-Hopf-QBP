# From frame compilation to quantum backpropagation

[← Compiler theorem](COMPILER_THEOREM.md) · [Read the complete narrative](../REVIEW.md) · [Next: verification →](VERIFICATION.md)

The compiler theorem can be audited independently of quantum backpropagation.
This page explains the downstream consequence: once the complete Hopf
differential frame is available at the optimal state-preparation frontier, the
global Hopf gradient protocol retains its shared-record scaling without an
additional compilation-depth factor.

## 1. The state-space response

Let

```math
E_O(\boldsymbol\theta)
=
\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
```

where `O` is Hermitian. For a real magnitude coordinate,

```math
\partial_{\theta_j}E_O
=
2\operatorname{Re}
\langle\partial_{\theta_j}\psi|O|\psi\rangle.
```

The Hopf differential identity is

```math
|\partial_{\theta_j}\psi\rangle
=
\sqrt{g_{j,j}}\,|e_j\rangle,
```

and the frame marker identity is

```math
W|\lambda(j)\rangle=|e_j\rangle.
```

Therefore

```math
\boxed{
\partial_{\theta_j}E_O
=
2\sqrt{g_{j,j}}
\operatorname{Re}
\langle\lambda(j)|W^{\dagger}O|\psi\rangle.
}
```

The inverse frame resolves the common response `O|psi>` into all normalized
Hopf directions at once. The metric factors then convert the normalized-frame
components into raw coordinate derivatives.

## 2. Controlled-observable interface

The validated global protocol assumes:

```math
O=O^{\dagger},
\qquad
O^2=I,
```

and exact phase-calibrated controlled access

```math
\operatorname{ctrl}(O)
=|0\rangle\!\langle0|\otimes I
+|1\rangle\!\langle1|\otimes O.
```

The controlled-branch phase must be known or calibrated. An unknown relative
phase rotates the measured quadrature and changes the fixed classical decoder.
Real-coefficient sums of reflections can be handled termwise, with the
coefficient-one-norm sampling factor recorded separately.

One global magnitude execution prepares the coherent branches, applies the
controlled observable, applies the inverse frame, and measures the branch
ancilla and system in the X basis. The reference branch satisfies

```math
W^{\dagger}|\psi\rangle=|0^n\rangle,
```

while the reflected branch contains

```math
W^{\dagger}O|\psi\rangle.
```

The interference parity exposes all designated frame amplitudes.

> **What should be checked here?**  The observable assumption, controlled-branch
> phase, and requested accuracy notion are part of the algorithmic statement.
> The compiler theorem does not remove these access assumptions.

## 3. One outcome contributes to every magnitude coordinate

Let `(b,y)` denote the branch-ancilla outcome and the `n`-bit system outcome in
the X basis. For internal node `j`, define

```math
Z_j
=
2\sqrt{g_{j,j}}
(-1)^{b+\lambda(j)\cdot y},
```

where the inner product is modulo two. Then

```math
\mathbb E[Z_j]
=
\partial_{\theta_j}E_O.
```

The same measured pair `(b,y)` determines the parity for **every** marker
`lambda(j)`. Thus one physical outcome is reused across the complete magnitude
block.

A practical decoder first accumulates the signed histogram

```math
h(y)=\sum_{t:y_t=y}(-1)^{b_t}
```

and applies one fast Walsh–Hadamard transform. The transform evaluates all
marker parities together. The decoder uses

```math
O(S+N\log N)
```

classical operations and `O(N)` auxiliary storage for `S` recorded outcomes,
while returning `N-1` real magnitude derivatives.

For the complex chart, the magnitude stream uses

```math
W_{\mathbb C}^{\dagger}
=W_{\mathbb R}^{\dagger}D_{\mathrm{ph}}^{\dagger}.
```

The leaf-phase derivatives are already localized in the computational basis. A
separate ancilla-Y/system-Z record contributes

```math
Z^{\mathrm{ph}}=2(-1)^b e_{\ell}
```

to the observed leaf `ell`, so the phase block requires no inverse
differential frame.

### Executable counterpart

- [Output-sensitive magnitude and phase decoders](../compiler_robust_hopf/decoders.py)
- [Decoder parity and empirical-distribution tests](../tests/test_decoders.py)
- [Complex phase-gradient identities](../compiler_robust_hopf/complex_analysis.py)

## 4. Frame-safe substitution theorem

Let `J` append the clean compiler workspace:

```math
J|\varphi\rangle
=|\varphi\rangle|0^m\rangle.
```

A compiled frame `W_tilde` is frame-safe when

```math
\boxed{
\widetilde WJ=JW.
}
```

This equality holds for every system input, not only `|0^n>`.

Because `W_tilde` is unitary and maps the clean-workspace subspace onto itself,
that subspace is reducing. Hence the inverse action is also exact:

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

Replacing `W` and `W^dagger` by their frame-safe compiled circuits therefore
leaves both coherent branches of the global protocol unchanged after the clean
workspace is ignored. It follows that the replacement preserves:

- the complete measurement distribution;
- every decoded gradient mean;
- the almost-sure record-norm bounds;
- the concentration argument;
- the output-sensitive classical decoder.

This is why the operator contract matters. State-column equality would preserve
only the forward reference state; it need not preserve the response resolution
performed by the inverse frame.

<p align="center">
  <img src="../assets/state-vs-frame.svg" width="900" alt="The global QBP protocol needs the complete differential frame, not only a state-preparation column." />
</p>

> **What should be checked here?**  Verify that the compiler returns its
> workspace exactly to zero on every clean input, that the clean subspace is
> invariant in both directions, and that the same logical frame is used by the
> fixed marker decoder.

### Executable counterpart

- [Frame-safe and checkpoint-interface contracts](FRAME_SAFE_COMPILATION.md)
- [State-column and checkpoint counterexamples](COMPILER_BOUNDARIES.md)
- [Exact compiler-boundary implementation](../compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](../tests/test_compiler_boundaries.py)

## 5. Fixed-norm records and execution count

At each magnitude depth, the simultaneous vector record has deterministic
Euclidean norm two. The direct phase and checkpoint records are signed one-hot
vectors of the same norm. A fixed-norm vector concentration bound therefore
controls each complete depth block without a union bound over every coordinate
inside that block.

For simultaneous coordinatewise accuracy `epsilon` and total failure
probability `delta`, one sufficient global magnitude allocation has the order

```math
S_{\mathrm{mag}}
=O\left(
\frac{1+\log(n/\delta)}{\epsilon^2}
\right).
```

At fixed `epsilon` and `delta`,

```math
S_{\mathrm{mag}}=O(\log n).
```

The complete Hopf chart has

```math
M=N-1
```

real coordinates or

```math
M=2N-1
```

complex state-vector coordinates. Since `n=Theta(log M)`,

```math
\boxed{
S_{\mathrm{global}}=O(\log\log M)
}
```

at fixed simultaneous absolute coordinate accuracy and confidence.

This counts independent controlled-observable executions. It does not make the
`M`-entry classical output sublinear, and it does not hide the cost of
implementing `ctrl(O)`.

## 6. Compilation no longer adds a depth penalty

The all-workspace compiler theorem gives

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`. Yuan–Zhang give the same optimal frontier for arbitrary state
preparation.

A matched scalar execution prepares the state and applies the same controlled
observable, but omits the reverse frame and returns a scalar record. A global
gradient execution adds one inverse frame of the same asymptotic depth as the
forward preparation. Thus, within the exact logical model and charging the
controlled observable comparably in both programs, compilation changes the
per-execution depth by at most a constant asymptotic factor.

The total logical-depth comparison is therefore governed by the number of
independent gradient records:

```math
\boxed{
\frac{\mathrm{TIME}(\nabla E_O)}
     {\mathrm{TIME}(E_O)}
=O(\log n)
=O(\log\log M),
}
```

under the stated fixed-accuracy and controlled-observable assumptions.

The earlier direct-angle Hopf ledger remains useful when preservation of one
coordinate–one physical angle is the desired engineering contract. The present
result establishes that state-equivalent, frame-safe recompilation can also
match the optimal state-preparation depth frontier.

> **What should be checked here?**  Keep three quantities separate: independent
> executions, per-execution logical depth, and materialized output size. The
> displayed ratio assumes the same controlled-observable call in scalar and
> gradient executions and does not claim routed or fault-tolerant hardware
> depth.

## 7. Checkpoint methods have a different compiler contract

The checkpoint method reverses only the suffix below a selected Hopf depth. It
does not require the complete global frame, but it does require correctness on
the complete active checkpoint interface.

For a forward factorization

```math
U=B_dA_d,
```

let `P_d` project onto the interface reached by the prefix `A_d`. A sufficient
compiled-suffix contract is

```math
\widetilde B_d J P_d
=e^{i\chi}J B_dP_d
```

for one common phase `chi` independent of the interface input. This preserves
the designated checkpoint-gradient means, although the complete output
distribution may change.

Thus the compiler hierarchy is:

| Compiler promise | Scalar state | Checkpoint means | Global frame distribution |
|---|---:|---:|---:|
| one prepared state column | sufficient | insufficient | insufficient |
| complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| complete frame-safe action | sufficient | sufficient where applicable | sufficient |

The optimal all-workspace theorem on this page concerns the complete global
frame. It does not claim that an arbitrary checkpoint factorization may be
recompiled without checking its active interface.

## 8. Scope of the consequence

The compiler result strengthens the global Hopf-QBP resource statement in the
exact logical model. It does not by itself establish:

- controlled access to a generic nonunitary observable;
- hardware routing or native-gate depth;
- approximate Clifford+T complexity;
- noise-dependent sampling guarantees;
- an optimal measurement strategy for every application;
- compiler invariance for arbitrary state-space charts.

The global record, phase record, concentration proof, and checkpoint protocol
are developed fully in the Hopf-QBP paper and repository. This repository
isolates the compiler question and proves that the complete Hopf differential
frame can meet the optimal state-preparation frontier without losing its
backpropagation interface.

---

[← Compiler theorem](COMPILER_THEOREM.md) · [Read the complete narrative](../REVIEW.md) · [Next: verification →](VERIFICATION.md)
