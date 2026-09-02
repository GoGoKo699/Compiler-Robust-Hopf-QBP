# End-to-end Hopf-QBP accounting

This page combines the chart-level gradient records with the unified
all-workspace Hopf-frame compiler. It keeps quantum executions, logical circuit
depth, workspace, classical decoding, and output length separate.

## 1. Parameters

Let

```math
N=2^n
```

and let `M=Theta(N)` denote the number of Hopf coordinates. The compiler has
`m>=0` clean workspace qubits.

The exact real and separated complex frames satisfy

```math
S_{\mathrm{frame}}(n,m)=\Theta(N),
```

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every ancillary budget. This matches the optimal arbitrary-state-
preparation frontier in the Yuan--Zhang circuit model.

The active real compiler uses:

- the borrowed-suffix echo at `m=0`;
- a direct flagged-UCG schedule for small positive `m`;
- a tree-decoder routed schedule for larger `m`.

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

Frame-safe compilation preserves the complete measurement distribution, so this
sample bound is independent of the elementary frame compiler and of `m`.

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
exceed the global magnitude stream and does not alter the overall `O(log n)`
execution scaling.

## 4. Quantum circuit cost per execution

Write

```math
D_{\mathrm{prep}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for matched optimal state-preparation depth, and let `D_O` denote the assigned
cost of controlled observable access.

A magnitude execution has depth

```math
O\left(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}\right)
=O\left(D_{\mathrm{prep}}+D_O\right).
```

A phase execution has depth

```math
O\left(D_{\mathrm{prep}}+D_O\right).
```

Thus complete differential-frame access introduces no asymptotic compiler
penalty relative to state preparation for any `m>=0`.

If controlled access to `O` is charged comparably in scalar and gradient
programs, total global-gradient quantum time at fixed accuracy and confidence
has overhead

```math
O(\log n)=O(\log\log M)
```

relative to one matched scalar evaluation. The observable-access assumption
must be stated whenever this ratio is quoted.

## 5. Quantum workspace

For `m>0`, the real-frame and complex phase blocks reuse the same `m` clean
compiler workspace qubits sequentially. For `m=0`, both the borrowed-suffix real
frame and the phase UCG are ancilla-free.

The gradient protocol itself adds one interferometric ancilla. Therefore the
workspace difference from the matched scalar program is additive constant
order. The compiler never counts the borrowed suffix data qubit as an ancillary
wire.

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

Selecting the better route gives

```math
T_{\mathrm{mag}}
=O\bigl(S+N\min\{S,n\}\bigr).
```

At fixed accuracy, `S=O(log n)`, so record-wise decoding costs

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
an optional `O(N)` postprocessing step and does not change the estimator
expectation.

## 8. Compiler parameter generation

The Hopf tree contains `N-1` magnitude angles.

- At `m=0`, each nonfinal echo layer directly uses the corresponding half-angle
  prefix table; generating all half-angle tables is `O(N)` arithmetic.
- In the routed schedule, the exact cut decomposition partitions the angles into
  one prefix and `2**t` local subtree lists in `O(N)` indexing work.
- The complex phase UCG block table pairs the `N` leaf phases directly in
  `O(N)` arithmetic and storage.

Generation of the final elementary UCG decomposition follows the published
Yuan--Zhang compiler. The quantum depth theorem counts the resulting logical
circuit, not host-language wall time of a particular synthesis implementation.

## 9. Complete resource summary

For every `m>=0`:

| Resource | Real magnitude stream | Complex phase stream |
|---|---:|---:|
| Executions at fixed accuracy/confidence | `O(log n)` | no larger asymptotically |
| Forward preparation depth | `Theta(n+N/(n+m))` | same |
| Reverse frame depth | `Theta(n+N/(n+m))` | none |
| Compiler workspace | at most `m` clean qubits | same pool; zero when `m=0` |
| Additional protocol ancilla | one | one |
| Classical decoding | `O(SN)` or `O(S+Nn)` | `O(S+N)` |
| Output length | `N-1` | `N` with one gauge redundancy |

The complete complex gradient combines both streams. Constant allocation of
accuracy and failure probability between them does not change the asymptotic
scaling.

## 10. Correctness and evidence boundary

The all-workspace resource statement applies only to frame-safe compilation. A
state-equivalent preparation circuit is not automatically a valid reverse
frame.

The strict-zero echo has a complete-operator proof and exact finite checks, but
the all-workspace theorem remains internally audited rather than externally
verified. This accounting also excludes:

- an application-independent cost for controlled `O`;
- hardware routing and native-gate restrictions;
- approximate Clifford+T synthesis and accumulated bias;
- noise-dependent sample complexity;
- the factorization-specific checkpoint schedule; and
- generic coordinate charts beyond the Hopf structure.
