# End-to-end Hopf-QBP accounting

This page combines the chart-level gradient records with the unified
all-workspace Hopf-frame compiler. It keeps quantum executions, per-execution
logical depth, workspace, classical decoding, output length, and requested
accuracy separate.

## 1. Parameters and frame compiler

Let

```math
N=2^n
```

and let `M=Theta(N)` denote the number of Hopf coordinates. The compiler has
`m>=0` clean workspace qubits.

The exact real frame and phase-dressed complex magnitude frame satisfy

```math
S_{\mathrm{frame}}(n,m)=\Theta(N),
```

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every ancillary budget. This matches the optimal arbitrary-state-
preparation frontier in the Yuan–Zhang model.

The real compiler uses:

- the borrowed-suffix echo at `m=0`;
- a direct flagged-UCG schedule for `1<=m<4n`;
- a binary–one-hot decoder and explicit coherent router for larger `m`.

## 2. Global magnitude stream

For an expectation objective

```math
E(\boldsymbol\theta)
=\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
```

the unrestricted-angle magnitude differential is

```math
\partial_{\theta_j}E
=2a_j\,\mathrm{Re}\langle e_j|O|\psi\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical Hopf domains `a_j>=0`, so `a_j=sqrt(g_(j,j))`. At
`g_(j,j)=0`, the raw differential vanishes while the unit marker column remains
a frame continuation.

The global protocol prepares coherent reference and response branches, applies
controlled `O`, applies the inverse frame, and measures the ancilla and system
in the designated bases. One outcome contributes a signed Walsh record to every
magnitude coordinate.

Frame-safe compilation preserves the complete measurement distribution, so the
record identity and concentration argument are independent of the elementary
frame compiler and of `m`.

## 3. Statistical target

The primary finite-shot target is simultaneous absolute accuracy of the **raw
Hopf-coordinate gradient**:

```math
\|\widehat{\nabla E}-\nabla E\|_{\infty}
\leq\varepsilon_{\infty}.
```

At each magnitude depth, the weighted record has deterministic Euclidean norm
two. There are `n` depth families. Fixed-norm concentration gives

```math
S_{\mathrm{mag}}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_{\infty}^2}
\right).
```

At fixed raw-coordinate accuracy and confidence,

```math
S_{\mathrm{mag}}=O(\log n)=O(\log\log M).
```

This does not imply the same execution count for complete raw-gradient `l_2`
accuracy, relative or directional accuracy, normalized-frame coefficients, or
natural-gradient coordinates. Those tasks have different dimensional or
metric conditioning. Small metric weights suppress raw records; division by
`sqrt(g_(j,j))` or `g_(j,j)` may be ill-conditioned.

## 4. Direct complex phase stream

For leaf phase `phi_l`,

```math
\partial_{\phi_\ell}|\psi\rangle
=i\psi_\ell|\ell\rangle.
```

The direct phase protocol uses the complex forward state, controlled `O`, an
ancilla-Y measurement, and a system computational-basis measurement. It does
not apply an inverse differential frame.

Each outcome contributes a signed one-hot vector of norm two. The phase
gradient lies in the zero-sum gauge subspace, and a zero-amplitude leaf has zero
phase differential without division by an amplitude.

The complete complex coordinate gradient combines:

1. the inverse-frame **magnitude** stream using
   `W_(C,mag)=D_ph W_R`;
2. the direct leaf-phase stream.

## 5. Matched logical programs

Let:

- `D_prep(n,m)` be the depth of the chosen forward preparation;
- `D_O` be the cost assigned to the same controlled observable in both
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

For the general arbitrary-state family,

```math
D_{\mathrm{prep}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right),
```

and the compiler theorem gives the same order for `D_frame` for every `m>=0`.
The inverse frame therefore changes per-execution logical depth by at most a
constant asymptotic factor.

At fixed comparable scalar and raw-coordinate absolute accuracy and confidence,
`S_E` is constant-order in `n` while `S_grad=O(log n)`. Hence

```math
\boxed{
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)=O(\log\log M).
}
```

This is a matched general-family logical-depth statement. It is not a
comparison with an instance-specialized scalar shortcut, and it excludes
classical materialization of the `M`-entry output.

## 6. Quantum workspace

For `m>0`, the real-frame and complex phase blocks reuse the same `m` clean
compiler qubits sequentially. For `m=0`, both the borrowed-suffix real frame and
the phase UCG are ancilla-free.

The gradient protocol itself adds one interferometric ancilla. Thus its
workspace difference from the matched scalar program is additive constant
order. The borrowed suffix data qubit is never counted as ancillary workspace.

## 7. Magnitude decoding

Let `S` outcomes be `(b_s,y_s)`. One outcome contributes the complete Walsh
character

```math
(-1)^{b_s}
\left((-1)^{k\cdot y_s}\right)_{k=0}^{N-1}.
```

Direct record-wise accumulation costs `O(SN)`. A signed histogram followed by a
fast Walsh–Hadamard transform costs `O(S+Nn)`. Selecting the better route gives

```math
\boxed{
T_{\mathrm{mag}}
=O\left(S+N\min\{S,n\}\right).
}
```

At fixed raw-coordinate accuracy, `S=O(log n)`, so the materialized magnitude
decoder is `O(N log n)`. The output itself has `N-1` entries.

## 8. Phase decoding

Phase outcomes accumulate directly into signed leaf bins. For `S` samples,

```math
T_{\mathrm{phase}}=O(S+N)
```

with `O(N)` output storage. Optional projection onto the known zero-sum gauge
subspace is `O(N)`.

## 9. Compiler parameter generation

The Hopf tree contains `N-1` magnitude angles.

- At `m=0`, all half-angle prefix tables are generated in `O(N)` arithmetic.
- In the routed schedule, one pass partitions angles into the prefix and
  `2^t` local subtree lists in `O(N)` work.
- The phase UCG pairs `N` leaf phases in `O(N)` work and storage.

The explicit router schedule is generated from the cut parameters. Elementary
UCG decomposition follows the published Yuan–Zhang compiler. The quantum depth
theorem counts the resulting logical circuit, not host-language synthesis wall
time.

## 10. Resource summary

For every `m>=0`:

| Resource | Magnitude stream | Direct phase stream |
|---|---:|---:|
| Primary executions at fixed raw `l_infinity` accuracy/confidence | `O(log n)` | no larger asymptotically |
| Forward preparation depth | `Theta(n+N/(n+m))` | same |
| Reverse magnitude-frame depth | `Theta(n+N/(n+m))` | none |
| Compiler workspace | at most `m` clean qubits | same pool; zero when `m=0` |
| Additional protocol ancilla | one | one |
| Classical decoding | `O(S+N min{S,n})` | `O(S+N)` |
| Output length | `N-1` | `N` with one gauge redundancy |

## 11. Correctness and evidence boundary

The all-workspace resource statement applies only to frame-safe compilation. A
state-equivalent preparation circuit is not automatically a valid inverse
frame.

The strict-zero echo, binary–one-hot decoder, and coherent router have explicit
logical constructions and finite exact tests. UCG and multi-controlled-X
elementary synthesis are imported from Yuan–Zhang. The theorem remains subject
to independent technical review.

This accounting excludes application-independent controlled-`O` synthesis,
hardware connectivity, approximate Clifford+T compilation, noise-dependent
sample complexity, optimizer convergence, and generic coordinate charts beyond
the Hopf structure.
