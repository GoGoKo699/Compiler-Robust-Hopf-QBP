# From frame compilation to Hopf quantum backpropagation

[← Compiler theorem](COMPILER_THEOREM.md) · [Complete technical note](../REVIEW.md) · [Next: verification →](VERIFICATION.md)

The compiler theorem can be checked without the quantum-backpropagation
protocol. This page records the downstream statement only: an exact frame-safe
compiler preserves the inverse-frame gradient record, and the compiled frame
adds no asymptotic depth factor beyond optimal state preparation.

The comparison is between matched logical programs. Quantum executions,
per-execution depth, classical output materialization, and controlled-observable
access remain separate costs.

## 1. Why the inverse frame appears

Let

```math
E_O(\boldsymbol\theta)
=\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
```

with `O` Hermitian. For a magnitude coordinate,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where `a_j` is the oriented incoming amplitude. Since

```math
W|\lambda(j)\rangle=|e_j\rangle,
```

we obtain

```math
\boxed{
\partial_{\theta_j}E_O
=2a_j\,\mathrm{Re}
\langle\lambda(j)|W^{\dagger}O|\psi\rangle.
}
```

On the canonical Hopf domains, `a_j=sqrt(g_(j,j))`. At a singular coordinate,
`a_j=0`, so the raw coordinate derivative vanishes. The marker column remains a
chart-selected frame direction, but no inverse metric is needed for the raw
gradient.

For the complex chart, the inverse-frame stream uses

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}
```

and resolves the magnitude directions. The leaf-phase derivatives use a
separate direct signed one-hot record.

## 2. Controlled-observable interface

The validated global record assumes

```math
O=O^{\dagger},
\qquad
O^2=I,
```

and phase-calibrated controlled access

```math
\mathrm{ctrl}(O)
=|0\rangle\!\langle0|\otimes I
+|1\rangle\!\langle1|\otimes O.
```

The relative phase between the controlled branches is part of the interface.
An unknown phase rotates the measured quadrature and changes the fixed decoder.
A real linear combination of reflections can be treated termwise, with its
coefficient one-norm accounted for separately.

One global magnitude execution prepares coherent reference and response
branches, calls the controlled observable, applies the inverse frame, and
measures the branch ancilla and system in the X basis.

## 3. One outcome contributes to every magnitude coordinate

Let `(b,y)` denote the branch-ancilla outcome and the `n`-bit system outcome. On
the canonical chart, define

```math
Z_j
=2\sqrt{g_{j,j}}
(-1)^{b+\lambda(j)\cdot y}.
```

For unrestricted algebraic coordinates, replace the principal square root by
the oriented amplitude `a_j`. Then

```math
\mathbb E[Z_j]
=\partial_{\theta_j}E_O.
```

The same pair `(b,y)` determines the parity for every marker `lambda(j)`, so one
execution contributes to the complete magnitude block.

For `S` recorded outcomes, a decoder may use either record-wise accumulation or
a signed histogram followed by one fast Walsh–Hadamard transform. The better
route has classical complexity

```math
\boxed{
O\left(S+N\min\{S,n\}\right)
}
```

and `O(N)` storage when the dense transform is materialized. This is a classical
output cost, not an additional quantum execution count.

For the complex chart, the direct leaf-phase stream contributes one signed
one-hot vector at the observed leaf and does not use the inverse magnitude
frame.

### Executable counterpart

- [Magnitude and direct-phase decoders](../compiler_robust_hopf/decoders.py)
- [Decoder cross-checks](../tests/test_decoders.py)
- [Complex magnitude and phase derivatives](../compiler_robust_hopf/complex_analysis.py)

## 4. Frame-safe substitution

Let `J` append the clean compiler workspace:

```math
J|\varphi\rangle
=|\varphi\rangle|0^m\rangle.
```

A compiled frame is frame-safe when

```math
\boxed{
\widetilde WJ=JW.
}
```

This equality holds for every system input. Since `W_tilde` is unitary and maps
the clean-workspace subspace onto itself, that subspace is reducing. Therefore

```math
\boxed{
\widetilde W^{\dagger}J=JW^{\dagger}.
}
```

Replacing the logical frame by any of the three compiled schedules preserves:

- the complete global-record measurement distribution;
- every raw-coordinate expectation;
- the almost-sure record-norm bound;
- the concentration argument;
- the classical decoder.

No compiler-specific statistical proof is needed after complete frame safety is
established.

The two-qubit obstruction explains why the first-column promise is insufficient:
a state-equivalent completion can move the response between marker columns and
change the decoded gradient.

### Executable counterpart

- [Frame-safe operator contract](FRAME_SAFE_COMPILATION.md)
- [State-column and checkpoint boundaries](COMPILER_BOUNDARIES.md)
- [Exact boundary constructions](../compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](../tests/test_compiler_boundaries.py)

## 5. Accuracy target and conditioning boundary

The primary finite-shot statement is simultaneous absolute accuracy of the raw
Hopf-coordinate gradient:

```math
\|\widehat{\nabla E_O}-\nabla E_O\|_{\infty}
\leq\varepsilon_{\infty}
```

with failure probability at most `delta`.

Each magnitude-depth record has deterministic Euclidean norm two. A fixed-norm
concentration bound gives the sufficient execution count

```math
S_{\nabla,\infty}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_{\infty}^2}
\right).
```

At fixed accuracy and confidence,

```math
S_{\nabla,\infty}=O(\log n).
```

For `M=Theta(N)` Hopf coordinates and `n=Theta(log M)`, this becomes

```math
O(\log\log M).
```

This execution statement is specific to the raw coordinatewise target. It does
not automatically apply to:

- complete-vector `l_2` accuracy;
- relative or directional accuracy near a small gradient;
- normalized-frame coefficients obtained by dividing by `sqrt(g_(j,j))`;
- natural-gradient coordinates obtained by dividing by `g_(j,j)`.

For example, concatenating all magnitude-depth records gives norm `2sqrt(n)`,
so fixed complete-vector `l_2` accuracy carries an `O(n)` leading execution
dependence. Small metric weights suppress raw coordinate records but condition
inverse-metric outputs.

## 6. Matched scalar and gradient programs

Let:

- `D_prep(n,m)` be the depth of the chosen forward preparation;
- `D_O` be the depth charged for the same controlled observable in both
  programs;
- `D_frame(n,m)` be the depth of one frame-safe inverse frame;
- `S_E` be the scalar execution count for its stated accuracy and confidence;
- `S_nabla` be the gradient execution count for the raw-coordinate target.

Define

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E\left(D_{\mathrm{prep}}+D_O\right),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}
\left(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}\right).
```

The all-workspace state-preparation theorem of P. Yuan and S. Zhang gives

```math
D_{\mathrm{prep}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for the general arbitrary-state family. The frame theorem gives the same order
for `D_frame`. Adding the inverse frame therefore changes per-execution logical
depth by at most a constant asymptotic factor, provided both programs charge
the same controlled-`O` call.

At fixed comparable scalar and raw-coordinate absolute accuracy and confidence,
`S_E` is constant-order in `n`, while `S_nabla=O(log n)`. Hence

```math
\boxed{
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)
=O(\log\log M).
}
```

This is a general-family logical-depth comparison. It is not a claim against an
instance-specialized scalar shortcut, and it excludes materializing an
`M`-entry classical output from the quantum-depth ratio.

> **Technical checkpoint.** The statement matches the state family,
> preparation convention, controlled observable, accuracy target, and
> confidence convention on both sides. Changing any of those choices changes
the comparison problem.

## 7. Checkpoint methods use a different compiler contract

A checkpoint protocol reverses only a suffix below one selected Hopf depth. It
does not require the complete global frame, but it does require correctness on
the complete active checkpoint interface.

For a factorization

```math
U=B_dA_d,
```

let `P_d` project onto the interface reached by `A_d`. A sufficient compiled
suffix condition is

```math
\widetilde B_dJP_d
=e^{i\chi}JB_dP_d
```

for one phase `chi` independent of the interface input. This preserves the
designated checkpoint-gradient means, although it need not preserve the entire
output distribution.

| Compiler promise | Scalar state | Checkpoint means | Global-frame distribution |
|---|---:|---:|---:|
| one prepared state column | sufficient | insufficient | insufficient |
| complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| complete frame-safe action | sufficient | sufficient where applicable | sufficient |

The all-workspace theorem concerns the complete global frame. It does not claim
that every checkpoint factorization can be recompiled without checking its
active interface.

## 8. Scope

The compiler theorem preserves the global Hopf-QBP record in the exact logical
model. It does not by itself establish:

- controlled access to a generic nonunitary observable;
- hardware-native or routed-device depth;
- approximate Clifford+T complexity;
- noise-dependent sampling guarantees;
- optimizer convergence;
- compiler invariance for arbitrary coordinate charts.

The full global, phase, and checkpoint protocols remain in `Hopf-QBP`. This
repository isolates the compiler question and proves that the complete real
frame and phase-dressed complex magnitude frame can reach the optimal
state-preparation frontier without losing the inverse-frame interface.

---

[← Compiler theorem](COMPILER_THEOREM.md) · [Complete technical note](../REVIEW.md) · [Next: verification →](VERIFICATION.md)
