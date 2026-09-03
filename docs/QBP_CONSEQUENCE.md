# From frame compilation to quantum backpropagation

[← Compiler theorem](COMPILER_THEOREM.md) · [Read the complete narrative](../REVIEW.md) · [Next: verification →](VERIFICATION.md)

The compiler theorem can be audited independently of quantum backpropagation.
This page states the downstream consequence precisely: once the real Hopf frame
and the phase-dressed complex magnitude frame are available at the optimal
state-preparation frontier, the global Hopf gradient protocol retains its
shared-record scaling without an additional asymptotic compilation-depth
factor.

The statement is about a matched pair of exact logical programs. It keeps
independent executions, per-execution depth, classical output materialization,
and controlled-observable access separate.

## 1. Coordinate differentials and the inverse frame

Let

```math
E_O(\boldsymbol\theta)
=\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
```

where `O` is Hermitian. For a real magnitude coordinate,

```math
\partial_{\theta_j}E_O
=2\,\mathrm{Re}
\langle\partial_{\theta_j}\psi|O|\psi\rangle.
```

For unrestricted angles, write the Hopf differential as

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where `a_j` is the oriented incoming amplitude. On the canonical Hopf domains,
`a_j>=0` and therefore `a_j=sqrt(g_(j,j))`. The marker identity is

```math
W|\lambda(j)\rangle=|e_j\rangle.
```

Hence

```math
\boxed{
\partial_{\theta_j}E_O
=2a_j\,\mathrm{Re}
\langle\lambda(j)|W^{\dagger}O|\psi\rangle.
}
```

On the canonical chart this is the familiar formula with `sqrt(g_(j,j))`.
When `g_(j,j)=0`, the raw differential and raw coordinate derivative vanish.
The unit marker column remains a frame continuation, but no division by the
zero metric weight is needed for the raw estimator.

For the complex chart, the inverse-frame stream uses

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}
```

and resolves only the magnitude directions. Leaf-phase derivatives are handled
by a separate direct signed one-hot record.

## 2. Controlled-observable interface

The validated global protocol assumes

```math
O=O^{\dagger},
\qquad
O^2=I,
```

and exact phase-calibrated controlled access

```math
\mathrm{ctrl}(O)
=|0\rangle\!\langle0|\otimes I
+|1\rangle\!\langle1|\otimes O.
```

The controlled-branch phase must be known or calibrated. An unknown relative
phase rotates the measured quadrature and changes the fixed decoder. A real
linear combination of reflections can be treated termwise, with its coefficient
one-norm recorded separately.

One global magnitude execution prepares coherent reference and response
branches, applies the controlled observable, applies the inverse frame, and
measures the branch ancilla and system in the X basis. The reference branch
satisfies

```math
W^{\dagger}|\psi\rangle=|0^n\rangle,
```

while the response branch contains

```math
W^{\dagger}O|\psi\rangle.
```

> **What should be checked here?** The observable assumption, controlled-branch
> phase, and requested accuracy notion are part of the algorithmic statement.
> The compiler theorem does not remove these access assumptions.

## 3. One outcome contributes to every magnitude coordinate

Let `(b,y)` be the branch-ancilla outcome and the `n`-bit system outcome in the
X basis. On the canonical chart define

```math
Z_j
=2\sqrt{g_{j,j}}
(-1)^{b+\lambda(j)\cdot y}.
```

For unrestricted algebraic coordinates, replace the principal square root by
the oriented incoming amplitude `a_j`. Then

```math
\mathbb E[Z_j]
=\partial_{\theta_j}E_O.
```

The same measured pair `(b,y)` determines the parity for every marker
`lambda(j)`, so one physical outcome is reused across the complete magnitude
block.

A practical decoder accumulates the signed histogram

```math
h(y)=\sum_{t:y_t=y}(-1)^{b_t}
```

and applies one fast Walsh–Hadamard transform. For `S` recorded outcomes, the
best of the record-wise and histogram routes has complexity

```math
\boxed{
O\left(S+N\min\{S,n\}\right)
}
```

with `O(N)` storage when the dense transform is used. This classical cost is
separate from the number of quantum executions.

For the complex chart, the magnitude stream uses

```math
W_{\mathbb C,\mathrm{mag}}^{\dagger}
=W_{\mathbb R}^{\dagger}D_{\mathrm{ph}}^{\dagger}.
```

The leaf-phase stream instead contributes a signed one-hot vector at the
observed leaf and uses no inverse differential frame.

### Executable counterpart

- [Output-sensitive magnitude and phase decoders](../compiler_robust_hopf/decoders.py)
- [Decoder parity and empirical-distribution tests](../tests/test_decoders.py)
- [Complex magnitude and phase-gradient identities](../compiler_robust_hopf/complex_analysis.py)

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
that subspace is reducing. Therefore

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

Replacing `W` and `W^dagger` by a frame-safe implementation leaves both
coherent branches of the global protocol unchanged after the clean workspace is
ignored. The replacement preserves:

- the complete measurement distribution;
- every decoded raw-coordinate mean;
- the almost-sure record-norm bounds;
- the concentration argument;
- the output-sensitive classical decoder.

This is why operator-level frame safety matters. State-column equality preserves
only the forward reference state and need not preserve the response resolution
performed by the inverse frame.

<p align="center">
  <img src="../assets/state-vs-frame.svg" width="900" alt="The global QBP protocol needs the complete differential frame, not only a state-preparation column." />
</p>

### Executable counterpart

- [Frame-safe and checkpoint-interface contracts](FRAME_SAFE_COMPILATION.md)
- [State-column and checkpoint counterexamples](COMPILER_BOUNDARIES.md)
- [Exact compiler-boundary implementation](../compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](../tests/test_compiler_boundaries.py)

## 5. Statistical target and conditioning boundary

The primary finite-shot statement inherited from `Hopf-QBP` is simultaneous
absolute accuracy of the **raw Hopf-coordinate gradient**:

```math
\|\widehat{\nabla E_O}-\nabla E_O\|_{\infty}
\leq\varepsilon_{\infty}
```

with prescribed failure probability.

Each magnitude-depth vector record has deterministic Euclidean norm two. A
fixed-norm concentration bound therefore gives a sufficient global magnitude
count

```math
S_{\nabla,\infty}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_{\infty}^2}
\right).
```

At fixed `epsilon_infinity` and `delta`,

```math
S_{\nabla,\infty}=O(\log n).
```

For `M=Theta(N)` Hopf coordinates and `n=Theta(log M)`, this becomes

```math
O(\log\log M).
```

This statement does **not** automatically imply the same execution count for:

- complete raw-gradient `l_2` accuracy;
- relative or directional accuracy near a small gradient;
- normalized-frame coefficients obtained by dividing by `sqrt(g_(j,j))`;
- natural-gradient coordinates obtained by dividing by `g_(j,j)`.

For example, concatenating all `n` magnitude-depth records gives norm
`2sqrt(n)`, so fixed complete-vector `l_2` accuracy has an `O(n)` rather than
`O(log n)` leading execution dependence. Small metric weights suppress raw
coordinate records but condition inverse-metric outputs. At `g_(j,j)=0`, the
raw record is exactly zero.

These are output-task distinctions, not failures of the raw-coordinate
protocol.

## 6. Matched scalar and gradient programs

The displayed runtime ratio is defined for a matched pair of logical programs.
Let:

- `D_prep(n,m)` be the depth of the chosen forward preparation;
- `D_O` be the depth charged for the same controlled observable in both
  programs;
- `D_frame(n,m)` be the depth of one frame-safe inverse frame;
- `S_E` be the scalar execution count for its declared scalar accuracy and
  confidence;
- `S_grad` be the gradient execution count for its declared raw-coordinate
  accuracy and confidence.

Define

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E\left(D_{\mathrm{prep}}+D_O\right),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}\left(
D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}
\right).
```

For the general arbitrary-state family in the Yuan–Zhang model,

```math
D_{\mathrm{prep}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right),
```

and the compiler theorem gives

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`. Therefore adding the inverse frame changes per-execution
depth by at most a constant asymptotic factor, provided the same controlled-`O`
call is charged in both programs.

At fixed comparable scalar and raw-coordinate absolute accuracy and confidence,
`S_E` is constant-order in `n` while

```math
S_{\nabla}=O(\log n).
```

Thus

```math
\boxed{
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)
=O(\log\log M).
}
```

This is a worst-case/general-family logical-depth comparison. It is not a claim
against an instance-specialized scalar circuit for an unusually easy state. It
also excludes classical materialization of the `M`-entry output from the ratio.

> **What should be checked here?** Keep independent executions,
> per-execution depth, classical output size, and controlled-observable cost
> separate. Verify that scalar and gradient programs use the same state family,
> access model, and accuracy convention.

## 7. Checkpoint methods have a different compiler contract

A checkpoint method reverses only the suffix below a selected Hopf depth. It
does not require the complete global frame, but it does require correctness on
the complete active checkpoint interface.

For a factorization

```math
U=B_dA_d,
```

let `P_d` project onto the interface reached by `A_d`. A sufficient compiled
suffix contract is

```math
\widetilde B_dJP_d
=e^{i\chi}JB_dP_d
```

for one phase `chi` independent of the interface input. This preserves the
designated checkpoint-gradient means, although the complete output distribution
may change.

| Compiler promise | Scalar state | Checkpoint means | Global frame distribution |
|---|---:|---:|---:|
| one prepared state column | sufficient | insufficient | insufficient |
| complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| complete frame-safe action | sufficient | sufficient where applicable | sufficient |

The all-workspace theorem concerns the complete global frame. It does not claim
that an arbitrary checkpoint factorization may be recompiled without checking
its active interface.

## 8. Scope of the consequence

The compiler result strengthens the global Hopf-QBP resource statement in the
exact logical model. It does not by itself establish:

- controlled access to a generic nonunitary observable;
- routed-device or native-gate depth;
- approximate Clifford+T complexity;
- noise-dependent sampling guarantees;
- optimizer convergence;
- compiler invariance for arbitrary coordinate charts.

The global record, direct phase record, concentration proof, and checkpoint
protocol are developed fully in `Hopf-QBP`. This repository isolates the
compiler question and proves that the complete real frame and phase-dressed
complex magnitude frame can meet the optimal state-preparation frontier without
losing their backpropagation interface.

---

[← Compiler theorem](COMPILER_THEOREM.md) · [Read the complete narrative](../REVIEW.md) · [Next: verification →](VERIFICATION.md)
