# End-to-end Hopf-QBP accounting

This page combines the chart-level gradient records with the unified
Yuan--Zhang frame compiler. It keeps quantum executions, logical circuit depth,
workspace, classical decoding, and output size separate.

## 1. Parameters

Let

```math
N=2^n
```

and let `M=Theta(N)` denote the number of Hopf coordinates. The compiler has
`m` clean workspace qubits. The positive-workspace theorem applies for
`m>=1`.

The exact real and separated complex frames satisfy

```math
S_{\mathrm{frame}}(n,m)=\Theta(N),
```

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

This is the same size and depth order as optimal arbitrary state preparation in
the Yuan--Zhang circuit model.

## 2. Global magnitude stream

For an expectation objective

```math
E(\boldsymbol\theta)
=\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
```

the magnitude derivatives are

```math
\partial_{\theta_j}E
=2\sqrt{g_{j,j}}\,
\operatorname{Re}\langle e_j|O|\psi\rangle.
```

The global protocol prepares the state coherently with an interferometric
ancilla, applies controlled `O`, applies the inverse differential frame, and
measures the ancilla and system in the designated bases. One physical outcome
produces a signed Walsh record for every magnitude depth.

At each tree depth the weighted record has deterministic Euclidean norm two.
There are only `n` depth families, so vector concentration followed by a union
bound over depths gives

```math
S_{\mathrm{mag}}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\right)
```

executions for simultaneous coordinatewise error `epsilon_infinity` and failure
probability `delta`. At fixed accuracy and confidence,

```math
S_{\mathrm{mag}}=O(\log n)=O(\log\log M).
```

Frame-safe compilation preserves the complete measurement distribution, so the
sample bound is independent of the elementary frame compiler.

## 3. Direct complex phase stream

For leaf phase `phi_l`,

```math
\partial_{\phi_\ell}|\psi\rangle
=i\psi_\ell|\ell\rangle.
```

The direct phase protocol uses the complex forward state, controlled `O`, an
ancilla-Y measurement, and a system computational-basis measurement. It does
not apply an inverse differential frame.

Each outcome contributes a signed one-hot vector of norm two. The exact phase
gradient lies in the zero-sum gauge subspace, and zero-amplitude leaves have
zero phase derivative without division by an amplitude.

The phase stream therefore has bounded-vector concentration without a union
bound over `N` coordinates. Its fixed-accuracy execution requirement does not
exceed the global magnitude stream and does not alter the overall
`O(log n)` execution scaling.

## 4. Quantum circuit cost per execution

Write

```math
D_{\mathrm{prep}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for the matched optimal state-preparation depth, and let `D_O` denote the cost
assigned to the controlled observable response under the declared access model.

A magnitude execution has depth

```math
O\left(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}\right)
=O\left(D_{\mathrm{prep}}+D_O\right).
```

A phase execution has depth

```math
O\left(D_{\mathrm{prep}}+D_O\right).
```

Thus the differential frame introduces no asymptotic compiler penalty relative
to state preparation for `m>=1`.

If controlled access to `O` is charged comparably in scalar and gradient
programs, the total global-gradient quantum time at fixed accuracy and
confidence has overhead

```math
O(\log n)=O(\log\log M)
```

relative to one matched scalar evaluation. The observable-access assumption
must be stated whenever this ratio is quoted.

## 5. Quantum workspace

The real frame, complex phase UCG, and their inverses reuse the same `m` clean
compiler workspace qubits sequentially. The gradient measurement adds one
interferometric ancilla. Consequently the workspace difference from the matched
state-preparation program is additive constant order.

At strict `m=0`, the current exact frame fallback has different size and depth
and is reported separately. The theorem does not silently count one clean flag
as zero workspace.

## 6. Magnitude decoding

Let `S` measured outcomes be `(b_s,y_s)`, where `b_s` is the ancilla bit and
`y_s` is the system label. One outcome contributes the complete Walsh character

```math
(-1)^{b_s}
\left((-1)^{k\cdot y_s}\right)_{k=0}^{N-1}.
```

All `N` entries can be generated recursively in `O(N)` arithmetic. Direct
record-wise averaging therefore costs

```math
T_{\mathrm{mag,record}}=O(SN)
```

and uses `O(N)` storage.

Alternatively, a signed histogram followed by a fast Walsh--Hadamard transform
costs

```math
T_{\mathrm{mag,FWHT}}=O(S+Nn).
```

Selecting the better decoder gives

```math
T_{\mathrm{mag}}
=O\bigl(S+N\min\{S,n\}\bigr).
```

At fixed accuracy, `S=O(log n)`, so the record-wise route costs

```math
O(N\log n).
```

The output itself contains `Theta(N)` magnitude coordinates.

## 7. Phase decoding

Phase outcomes are accumulated directly into signed leaf bins. For `S` samples,

```math
T_{\mathrm{phase}}=O(S+N)
```

with `O(N)` output storage. Projection onto the known zero-sum gauge subspace is
an optional `O(N)` postprocessing step and does not change the expectation.

## 8. Compiler parameter generation

The Hopf tree contains `N-1` magnitude angles. The exact cut decomposition
partitions these angles into one prefix and `2**t` local subtree lists in
`O(N)` indexing work.

The complex phase layer is represented directly as one UCG with blocks

```math
\operatorname{diag}
\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

Building this block table from the `N` leaf phases takes `O(N)` arithmetic and
storage. The earlier phase-polynomial Walsh transform is not part of the active
compiler.

Generation of the final elementary UCG decomposition follows the published
Yuan--Zhang compiler. The quantum depth theorem counts the resulting logical
circuit, not the host-language wall time of a particular synthesis software
implementation.

## 9. Complete resource summary

For `m>=1`:

| Resource | Real magnitude stream | Complex phase stream |
|---|---:|---:|
| Executions at fixed accuracy/confidence | `O(log n)` | no larger asymptotically |
| Forward preparation depth | `Theta(n+N/(n+m))` | same |
| Reverse frame depth | `Theta(n+N/(n+m))` | none |
| Compiler workspace | `m` clean qubits | same pool for forward phase UCG |
| Additional protocol ancilla | one | one |
| Classical decoding | `O(SN)` or `O(S+Nn)` | `O(S+N)` |
| Output length | `N-1` | `N` with one gauge redundancy |

The complete complex gradient combines both streams. Constant allocation of
accuracy and failure probability between them does not change the asymptotic
scaling.

## 10. Boundaries

This accounting does not include:

- an application-independent cost for implementing controlled `O`;
- strict-zero-workspace optimality;
- hardware routing or native-gate constraints;
- approximate Clifford+T synthesis and accumulated bias;
- noise-dependent sample complexity; or
- the factorization-specific checkpoint schedule.

Those resources must be added explicitly when the model is broadened.
