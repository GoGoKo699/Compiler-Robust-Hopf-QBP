# From frame compilation to quantum backpropagation

[← Compiler theorem](COMPILER_THEOREM.md) · [Complete narrative](../REVIEW.md) · [Verification →](VERIFICATION.md)

The compiler theorem is independent of the gradient protocol.  Its algorithmic
consequence follows from one exact interface: the global magnitude circuit
applies the inverse of the prescribed Hopf frame.  A frame-safe compiler
therefore preserves the complete measurement record, not only the prepared
state.

This page keeps four resources separate:

1. independent quantum executions;
2. logical depth of one execution;
3. classical decoding and output materialization;
4. controlled access to the observable.

## 1. Coordinate response in the frame basis

Let

```math
E_O(\boldsymbol\theta)
=\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
```

where $O$ is Hermitian.  For a real magnitude coordinate,

```math
\partial_{\theta_j}E_O
=2\,\mathrm{Re}
\langle\partial_{\theta_j}\psi|O|\psi\rangle.
```

Using

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
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

For unrestricted angles, $a_j$ is the oriented incoming amplitude and
$g_{j,j}=a_j^2$.  On the canonical Hopf domains, $a_j\geq0$ and
$a_j=\sqrt{g_{j,j}}$.  If $g_{j,j}=0$, the raw coordinate derivative is zero;
no inverse metric weight is needed for the raw estimator.

For the complex chart, the inverse-frame stream uses

```math
W_{\mathbb C,\mathrm{mag}}^{\dagger}
=W_{\mathbb R}^{\dagger}D_{\mathrm{ph}}^{\dagger}
```

and resolves the magnitude coordinates.  The leaf-phase coordinates use a
separate direct signed one-hot stream.

## 2. Controlled-observable interface

The validated global protocol assumes

```math
O=O^{\dagger},
\qquad
O^2=I,
```

with phase-calibrated controlled access

```math
\mathrm{ctrl}(O)
=|0\rangle\!\langle0|\otimes I
+|1\rangle\!\langle1|\otimes O.
```

An unknown relative phase between the two control branches rotates the measured
quadrature and changes the decoder.  A real linear combination of reflections
may be treated term by term, with the coefficient one-norm charged separately.

One magnitude execution prepares coherent reference and response branches,
applies the controlled observable, applies the inverse frame, and measures the
branch ancilla and system in the X basis.  Before measurement, the two system
branches contain

```math
W^{\dagger}|\psi\rangle=|0^n\rangle
```

and

```math
W^{\dagger}O|\psi\rangle.
```

The second vector contains all magnitude-coordinate responses in the marker
basis.

The interference protocol requires one clean branch ancilla in addition to
the frame compiler's workspace. Any work needed for controlled-observable
access is charged separately. The strict-zero compiler's borrowed suffix bit
is logical data and does not supply this protocol ancilla.

## 3. One outcome gives one record for every magnitude coordinate

Let $(b,y)$ denote the branch-ancilla outcome and the $n$-bit system outcome in
the X basis.  Define

```math
Z_j
=2a_j(-1)^{b+\lambda(j)\cdot y}.
```

Then

```math
\mathbb E[Z_j]
=\partial_{\theta_j}E_O.
```

On the canonical chart, replace $a_j$ by $\sqrt{g_{j,j}}$.  The same observed
pair $(b,y)$ determines the parity for every marker $\lambda(j)$, so one quantum
outcome contributes a full magnitude-gradient record.

For $S$ outcomes, two classical routes are useful.

### Record-wise decoding

Evaluate every requested marker parity for every outcome.

### Signed-histogram decoding

Accumulate

```math
h(y)=\sum_{t:y_t=y}(-1)^{b_t}
```

and apply one fast Walsh–Hadamard transform.

Taking the better route gives

```math
\boxed{
O\left(S+N\min\{S,n\}\right)
}
```

time, with $O(N)$ storage for the dense transform.  This is a classical output
cost; it is not an additional quantum execution count.

For the complex phase stream, each observed leaf contributes a signed one-hot
record directly. Accumulating $S$ outcomes and materializing the phase gradient
costs $O(S+N)$ classical time and $O(N)$ output storage. No inverse magnitude
frame is used in that stream.

### Executable counterpart

- [Magnitude and phase decoders](../compiler_robust_hopf/decoders.py)
- [Decoder tests](../tests/test_decoders.py)
- [Complex coordinate identities](../compiler_robust_hopf/complex_analysis.py)

## 4. Frame-safe substitution

Let

```math
J|\varphi\rangle
=|\varphi\rangle|0^m\rangle.
```

Suppose the compiled frame satisfies

```math
\widetilde WJ=JW.
```

Since $\widetilde W$ is unitary and maps the clean subspace onto itself,

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

Replacing $W$ and $W^{\dagger}$ by the compiled circuit therefore preserves:

- both coherent branches;
- the complete output distribution;
- every raw-coordinate mean;
- the almost-sure record-norm bound;
- the concentration argument;
- either classical decoding route.

This implication is exact and compiler independent.  The all-workspace theorem
supplies one family of implementations satisfying its premise.

By contrast, equality only on $\lvert0^n\rangle$ preserves the reference state but leaves
the response resolution unconstrained.  The two-qubit example in the
[complete narrative](../REVIEW.md#12-a-complete-two-qubit-obstruction) shows the
resulting gradient corruption explicitly.

## 5. Statistical target

The primary finite-shot statement is simultaneous absolute accuracy of the
**raw Hopf-coordinate gradient**:

```math
\|\widehat{\nabla E_O}-\nabla E_O\|_{\infty}
\leq\varepsilon_{\infty}
```

with failure probability at most $\delta$.

Each depth record has deterministic Euclidean norm two.  A fixed-norm vector
concentration bound gives the sufficient magnitude execution count

```math
S_{\nabla,\infty}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_{\infty}^2}
\right).
```

At fixed $\varepsilon_\infty$ and $\delta$,

```math
S_{\nabla,\infty}=O(\log n).
```

For $M=\Theta(N)$ Hopf coordinates and $n=\Theta(\log M)$, this is

```math
O(\log\log M).
```

This is not the execution complexity of every possible gradient task.
Different guarantees include:

| Requested output | Additional sensitivity |
|---|---|
| complete raw-gradient $\ell_2$ accuracy | concatenated record norm grows as $\sqrt{n}$ |
| relative or directional accuracy | depends on the gradient norm |
| normalized-frame coefficients | division by $\sqrt{g_{j,j}}$ conditions small metric weights |
| natural-gradient coordinates | division by $g_{j,j}$ is still more sensitive |

At a singular magnitude coordinate, the raw coordinate record is exactly zero.  The
compiler theorem concerns the frame operator and does not remove conditioning
from a subsequently rescaled output task.

## 6. Matched scalar and gradient programs

The depth comparison is made between matched logical programs.  Let

- $D_{\mathrm{prep}}(n,m)$ be the depth of the chosen general-family forward preparation;
- $D_O$ be the depth charged for the same controlled observable in both
  programs;
- $D_{\mathrm{frame}}(n,m)$ be the depth of one frame-safe inverse frame;
- $S_E$ and $S_\nabla$ be the execution counts for the stated scalar and raw
  coordinatewise accuracy targets.

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

For the general arbitrary-state family in the all-workspace state-preparation
model,

```math
D_{\mathrm{prep}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right),
```

and the compiler theorem gives

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

The inverse frame therefore changes the per-execution logical depth by only a
constant asymptotic factor.  At fixed comparable scalar and raw-coordinate
absolute accuracy and confidence,

```math
\boxed{
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)
=O(\log\log M).
}
```

The statement uses the same state family, preparation convention, controlled
observable, and accuracy convention on both sides.  It does not compare against
an instance-specialized scalar shortcut, and it excludes classical
materialization of the $M$-entry output.

### Classical compiler preprocessing

In the exact model, generating the strict-zero half-angle tables, partitioning
the $N-1$ magnitude angles into a prefix and subtree lists, and pairing the
$N$ leaf phases each require $O(N)$ table operations on the supplied angle
data. These are classical preprocessing costs, separate from the quantum
size and depth bounds. They do not bound the bit complexity of angle
evaluation or the running time of elementary UCG synthesis.

## 7. Checkpoint protocols use a different interface

A checkpoint protocol reverses only a suffix below a selected Hopf depth.  It
does not require the complete global frame, but it does require correctness on
the complete active checkpoint interface.

For

```math
U=B_dA_d,
```

let $P_d$ project onto the interface reached by $A_d$.  A sufficient compiled
suffix contract is

```math
\widetilde B_dJP_d
=e^{i\chi}JB_dP_d,
```

where $\chi$ is independent of the interface input.

| Compiler promise | Scalar state | Checkpoint means | Global-frame distribution |
|---|---:|---:|---:|
| one prepared state column | sufficient | insufficient | insufficient |
| complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| complete frame-safe action | sufficient | sufficient where applicable | sufficient |

The all-workspace theorem concerns the complete global frame.  It does not
replace the separate active-interface analysis required by an arbitrary
checkpoint factorization.

## 8. Scope

The compiler result establishes that exact compilation introduces no additional
asymptotic logical-depth factor into the matched global Hopf-QBP program.  It
does not by itself supply:

- controlled access to a generic nonunitary observable;
- routed-device or hardware-native depth;
- approximate Clifford+T complexity;
- noise-dependent sampling guarantees;
- optimizer convergence;
- a compiler theorem for arbitrary coordinate charts.

The full global, phase, and checkpoint protocols are developed in `Hopf-QBP`.
This repository isolates and resolves the prescribed-completion question on
which their compiler robustness depends.

---

[← Compiler theorem](COMPILER_THEOREM.md) · [Complete narrative](../REVIEW.md) · [Verification →](VERIFICATION.md)

For finite synthesis error, [the approximation contract](QBP_APPROXIMATION.md)
proves that a shared compiled frame and its actual adjoint preserve the raw
sampling order, with explicit full-workspace and controlled-observable error
budgets.
