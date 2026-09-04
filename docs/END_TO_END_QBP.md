# End-to-end cost ledger for compiler-robust Hopf QBP

[← QBP consequence](QBP_CONSEQUENCE.md) · [Complete technical note](../REVIEW.md) · [Verification →](VERIFICATION.md)

The compiler theorem controls one component of a larger algorithmic cost: the
logical depth of the complete inverse frame. This page keeps that cost separate
from quantum executions, classical decoding, output materialization, and
controlled-observable access.

The preparation-depth benchmark is the optimal all-workspace theorem of P. Yuan
and S. Zhang. Their framework and the Hopf-frame compiler use the same exact
all-to-all arbitrary-one-qubit+CNOT model.

## 1. Cost axes

Four quantities should not be collapsed into one runtime symbol.

| Cost axis | What it measures | Main dependence here |
|---|---|---|
| quantum executions | independent circuit repetitions needed for the stated statistical target | raw magnitude `l_infinity`: `O((1+log(n/delta))/epsilon_infinity^2)` |
| per-execution logical depth | one state preparation, one controlled observable, and one inverse frame | `D_prep + D_O + D_frame` |
| classical decoding | transform recorded outcomes into gradient coordinates | `O(S+N min{S,n})` for magnitude decoding |
| output materialization | write or transmit an explicit `M`-entry gradient | at least `Omega(M)` classical work |

The result that survives compiler replacement is a statement about the first
two axes. The output-size lower bound remains present even when all coordinates
share the same quantum executions.

## 2. Coordinate count

For the real Hopf chart,

```math
M_{\mathbb R}=N-1.
```

For the separated complex chart,

```math
M_{\mathbb C}=(N-1)+N=2N-1,
```

with `N-1` magnitude coordinates and `N` leaf phases. The phase-dressed complex
magnitude frame is still an `N`-dimensional unitary. The leaf-phase derivatives
use a separate direct record.

Thus in either case

```math
M=\Theta(N),
\qquad
n=\Theta(\log M).
```

## 3. Quantum executions for the raw coordinate target

The primary statistical target is

```math
\|\widehat{\nabla E_O}-\nabla E_O\|_\infty
\leq\varepsilon_\infty
```

with failure probability at most `delta`.

The global magnitude record has deterministic norm two within each depth block.
A fixed-norm concentration argument gives

```math
S_{\nabla,\infty}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\right).
```

At fixed accuracy and confidence,

```math
S_{\nabla,\infty}=O(\log n)=O(\log\log M).
```

The direct phase stream has the same fixed-norm form and does not change the
asymptotic execution count.

This conclusion is not a statement about every gradient-output norm. In
particular:

- fixed complete-vector `l_2` accuracy has an `O(n)` leading record-norm
  dependence for the full magnitude block;
- relative and directional accuracy can depend on `1/||nabla E||`;
- normalized-frame coefficients divide by `sqrt(g_(j,j))`;
- natural-gradient coordinates divide by `g_(j,j)`.

Small metric weights therefore condition inverse-metric outputs even though the
raw coordinate records remain bounded.

## 4. Per-execution logical depth

Let

```math
D_{\mathrm{prep}}(n,m)
```

be the chosen forward-preparation depth,

```math
D_O
```

be the depth charged to the same controlled observable in scalar and gradient
programs, and

```math
D_{\mathrm{frame}}(n,m)
```

be the compiled inverse-frame depth.

The Yuan–Zhang all-workspace QSP theorem gives

```math
D_{\mathrm{prep}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for the general arbitrary-state family. The present compiler theorem gives

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for the complete real frame and phase-dressed complex magnitude frame.

The inverse frame therefore adds only a constant asymptotic factor to the
preparation-scale part of one execution.

## 5. Matched scalar and gradient programs

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

The comparison is matched in four ways:

1. the same general state family;
2. the same preparation convention;
3. the same phase-calibrated controlled observable;
4. comparable fixed absolute-accuracy and confidence conventions.

At fixed comparable scalar and raw-coordinate accuracy and confidence,
`S_E=Theta(1)` in `n` and `S_nabla=O(log n)`. Hence

```math
\boxed{
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)
=O(\log\log M).
}
```

The statement does not compare with an unusually easy instance-specific scalar
circuit. It also does not count classical materialization of all `M`
coordinates as quantum depth.

## 6. Classical decoding

One magnitude outcome contributes a parity sign to every marker. Two exact
decoding routes are useful.

### Record-wise accumulation

For each of `S` records, update all `N-1` magnitude coordinates:

```math
O(SN)
```

time and `O(N)` output storage.

### Signed histogram plus fast Walsh–Hadamard transform

Accumulate a signed histogram over the `N` X-basis outcomes, then apply one
FWHT:

```math
O(S+Nn)
```

time and `O(N)` storage.

Taking the better route gives

```math
\boxed{
O\left(S+N\min\{S,n\}\right).
}
```

The direct leaf-phase stream is sparse: each record updates one observed leaf.
Dense output still requires `Omega(N)` materialization if every coordinate is
written explicitly.

## 7. Controlled-observable cost

The compiler theorem does not make a generic observable unitary. The validated
core assumes

```math
O=O^{\dagger},
\qquad
O^2=I,
```

and phase-calibrated access to

```math
\mathrm{ctrl}(O)
=|0\rangle\!\langle0|\otimes I
+|1\rangle\!\langle1|\otimes O.
```

A real linear combination of reflections can be estimated termwise, with
coefficient-dependent overhead. Generic nonunitary access, block encodings, and
application-specific construction costs are distinct interfaces.

The matched ratio leaves `D_O` explicit so the compiler claim does not hide the
observable-access problem.

## 8. Workspace accounting

The forward state preparation and inverse frame may reuse the same clean
workspace sequentially, provided each block restores it before the next block.
The all-workspace theorem guarantees this for the compiled frame.

The phase-dressed complex magnitude frame also reuses the pool sequentially:

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

The required workspace is the larger peak of the real frame and phase UCG, not
their sum.

At `m=0`, both blocks are ancilla-free.

## 9. Checkpoint schedule

A displayed complete checkpoint schedule may run one checkpoint experiment for
each of `n` depths. If each depth uses the same `O(log n)` record count, the
complete schedule has

```math
O(n\log n)=O(\log M\log\log M)
```

independent executions.

That quantity is different from the global-frame result. The checkpoint method
trades cross-depth record reuse for reverse-circuit locality and a weaker active-
interface compiler promise.

## 10. Summary ledger

At fixed raw-coordinate absolute accuracy and confidence:

| Component | Scalar matched program | Global gradient matched program |
|---|---:|---:|
| executions | `Theta(1)` in `n` | `O(log n)` |
| preparation depth | `Theta(n+N/(n+m))` | same |
| inverse-frame depth | absent | `Theta(n+N/(n+m))` |
| controlled observable | `D_O` | same `D_O` |
| quantum-depth ratio | 1 | `O(log n)` |
| classical output | scalar | `O(S+N min{S,n})`, plus `Omega(N)` if fully materialized |

The compiler theorem removes a possible extra asymptotic depth penalty from the
inverse frame. The remaining displayed factor comes from the shared-record
statistical target, not from frame compilation.

---

[← QBP consequence](QBP_CONSEQUENCE.md) · [Complete technical note](../REVIEW.md) · [Verification →](VERIFICATION.md)
