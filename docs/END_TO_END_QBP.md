# Resource accounting after frame compilation

[← Compiler theorem](COMPILER_THEOREM.md) · [QBP consequence](QBP_CONSEQUENCE.md) · [Verification →](VERIFICATION.md)

This page collects the end-to-end resources after the prescribed Hopf frame has
been compiled.  It keeps six quantities separate:

1. size and depth of one compiled frame;
2. clean compiler workspace;
3. independent quantum executions;
4. controlled-observable access;
5. classical decoding;
6. output length and requested accuracy.

Let

```math
N=2^n,
\qquad
M=\Theta(N),
```

where $M$ is the number of Hopf coordinates.

## 1. Compiled frame

For every clean-workspace budget $m\geq0$,

```math
S_{\mathrm{frame}}(n,m)=\Theta(N),
```

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

The real compiler uses:

- the borrowed-suffix echo at $m=0$;
- the direct clean-flag schedule for small positive workspace;
- the tree cut, binary–one-hot decoder, and coherent router for larger
  workspace.

The phase-dressed complex magnitude frame adds one exact phase UCG and reuses
the same work pool sequentially.

## 2. Magnitude-coordinate response

For

```math
E_O(\boldsymbol\theta)
=\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
```

```math
\partial_{\theta_j}E_O
=2a_j\,\mathrm{Re}\langle e_j|O|\psi\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical domains, $a_j\geq0$ and equals the principal metric square root.
At zero metric weight, the raw coordinate derivative is zero.

The global magnitude circuit prepares reference and objective-response branches,
applies the inverse frame, and measures one branch bit and one $n$-bit system
string.  The same outcome contributes a parity record to every magnitude
coordinate.

Frame-safe compilation preserves the complete output distribution, so the
record identity is independent of the selected workspace schedule.

## 3. Raw-coordinate execution count

The primary finite-shot target is

```math
\|\widehat{\nabla E_O}-\nabla E_O\|_{\infty}
\leq\varepsilon_{\infty}
```

with failure probability at most $\delta$.

The magnitude records have fixed Euclidean norm at each tree depth.  The
sufficient execution count is

```math
S_{\nabla,\infty}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_{\infty}^2}
\right).
```

At fixed accuracy and confidence,

```math
S_{\nabla,\infty}
=O(\log n)
=O(\log\log M).
```

This statement concerns the raw coordinate gradient.  Complete-vector,
relative, normalized-frame, and natural-gradient tasks may carry additional
dimension, norm, or metric-conditioning factors.

## 4. Direct phase stream

For leaf phase $\phi_l$,

```math
\partial_{\phi_\ell}|\psi\rangle
=i\psi_\ell|\ell\rangle.
```

The phase circuit uses the complex forward state, the same controlled
observable, an ancilla-Y measurement, and a computational-basis system
measurement.  It does not apply the inverse magnitude frame.

Each outcome contributes a signed one-hot record.  A zero-amplitude leaf has
zero phase differential, and the complete phase gradient lies in the expected
zero-sum gauge subspace.

The complete complex coordinate output combines:

1. the inverse-frame magnitude stream using $W_{\mathbb C,\mathrm{mag}}$;
2. the direct leaf-phase stream.

## 5. Matched logical time

Let

- $D_{\mathrm{prep}}(n,m)$ be the depth of the general-family forward preparation;
- $D_O$ be the depth charged for the same controlled observable;
- $D_{\mathrm{frame}}(n,m)$ be the depth of one frame-safe inverse frame;
- $S_E$ and $S_{\mathrm{grad}}$ be the execution counts for the declared scalar and raw
  coordinatewise targets.

Define

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E(D_{\mathrm{prep}}+D_O),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}).
```

The all-workspace state-preparation frontier and the frame theorem give

```math
D_{\mathrm{prep}}(n,m)
=D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

at the level of asymptotic order.  The inverse frame therefore adds only a
constant per-execution depth factor.

At fixed comparable scalar and raw-coordinate accuracy and confidence,

```math
\boxed{
\frac{T_{\mathrm{grad}}^{\mathrm{matched}}}
     {T_{\mathrm{scalar}}^{\mathrm{matched}}}
=O(\log n)
=O(\log\log M).
}
```

The comparison uses the same state family and controlled observable.  It does
not compare against an instance-specialized scalar shortcut and does not include
classical materialization of the $M$-entry gradient.

## 6. Quantum workspace

The frame compiler uses at most $m$ clean qubits and returns them to zero.  The
real frame and phase UCG reuse the same pool sequentially.  At $m=0$, both are
ancilla free.

The interference protocol adds one branch ancilla beyond the matched scalar
program.  The borrowed suffix bit in the strict-zero compiler is logical data,
not ancillary workspace.

## 7. Classical magnitude decoding

For $S$ measured pairs $(b_s,y_s)$, direct record-wise decoding costs

```math
O(SN).
```

A signed histogram followed by a fast Walsh–Hadamard transform costs

```math
O(S+Nn).
```

Choosing the better route gives

```math
\boxed{
T_{\mathrm{mag}}
=O\left(S+N\min\{S,n\}\right).
}
```

At fixed raw-coordinate accuracy, $S=O(\log n)$, so dense materialization costs
$O(N \log n)$.  The output itself has `N-1` entries.

The phase stream accumulates directly into signed leaf bins in

```math
O(S+N)
```

time and $O(N)$ output storage.

## 8. Classical compiler preprocessing

The Hopf tree has `N-1` magnitude angles.

- Half-angle tables for the strict-zero schedule are generated in $O(N)$ work.
- A routed cut partitions the angles into one prefix list and $2^t$ subtree
  lists in $O(N)$ work.
- The phase UCG pairs $N$ leaf phases in $O(N)$ work and storage.
- The explicit decoder and router schedules are generated from `n,t` and the
  chosen register layout.

The logical depth theorem counts the resulting quantum circuit, not the host
language's synthesis wall time.

## 9. Summary

| Resource | Magnitude stream | Direct phase stream |
|---|---:|---:|
| primary executions at fixed raw $\ell_\infty$ accuracy/confidence | $O(\log n)$ | no larger asymptotically |
| forward preparation depth | $\Theta\!\left(n+\frac{N}{n+m}\right)$ | same |
| reverse magnitude-frame depth | $\Theta\!\left(n+\frac{N}{n+m}\right)$ | none |
| clean compiler workspace | at most $m$ | same pool |
| additional protocol ancilla | one | one |
| classical decoding | $O\!\left(S+N\min\{S,n\}\right)$ | $O(S+N)$ |
| materialized output length | $N-1$ | $N$, with one gauge redundancy |

## 10. Boundary of the accounting

The table above is an exact logical-circuit and raw-coordinate accounting.  It
does not include:

- synthesis of a generic nonunitary observable into a controlled reflection;
- device-connectivity routing;
- native-gate or approximate Clifford+T depth;
- noise-dependent execution counts;
- optimizer convergence;
- the conditioning of outputs obtained by dividing by small metric weights.

The [QBP consequence](QBP_CONSEQUENCE.md) gives the operator and statistical
premises; the [verification map](VERIFICATION.md) gives the executable evidence.

---

[← Compiler theorem](COMPILER_THEOREM.md) · [QBP consequence](QBP_CONSEQUENCE.md) · [Verification →](VERIFICATION.md)
