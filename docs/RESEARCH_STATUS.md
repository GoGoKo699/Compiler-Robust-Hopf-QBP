# Research status and release gates

Last updated: 2026-09-02.

## Current conclusion

The project now has an internally audited optimal compiler theorem for every
**positive** clean-workspace budget.

Let

```math
N=2^n.
```

For every integer `m>=1`, the complete real Hopf differential frame has an
exact frame-safe implementation using at most `m` clean ancillary qubits, with

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

inherits the same positive-workspace size and depth profile by sequential clean
reuse of the exact diagonal compiler.

The upper bound uses:

1. the exact tree-cut identity

   ```math
   R_t^{(n)}=\bigoplus_{r=0}^{2^t-1}W_{n-t}^{(r)};
   ```

2. coherent route--parallel-subframes--unroute under the workspace envelope

   ```math
   2\,2^t(n-t+1)\leq m;
   ```

3. the previously audited low-workspace compiler when `1<=m<4n`.

The lower bound follows from the `(N-1)`-dimensional real unit sphere:
parameter counting gives `Omega(N)` size and `Omega(N/(n+m))` depth, while the
backward light cone of the `n` system outputs gives `Omega(n)` depth.

The result matches the QSP frontier in Theorem 2 of Yuan and Zhang,
*Quantum* 7, 956 (2023). Figure 1 of that paper concerns general unitary
synthesis and is not the source of the QSP benchmark.

The second internal audit is in
[`OPTIMALITY_AUDIT_ISSUE_9.md`](OPTIMALITY_AUDIT_ISSUE_9.md). It sharpened the
exact copied-control count and the light-cone parameter bound but found no
failure of the routed construction.

## Strict zero-workspace boundary

The optimal theorem above is stated only for `m>=1`. At strict zero additional
workspace, the current exact alternatives are:

| Clean ancillary qubits | Size | Depth |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

It remains open whether one can obtain simultaneously

```math
S=O(N),
\qquad
D=O\left(n+\frac{N}{n}\right),
\qquad
m=0.
```

The cumulative near-optimal theorem package is frozen on
`near-optimal-audited-2026-09` at commit
`24f339b863faa2ac92e1adb3917cbef7dc24d3b8`.

## Claim ledger

| Claim | Status | Evidence | Remaining work |
|---|---|---|---|
| Recursive and addressed real Hopf frames coincide | Proved and tested | Independent matrix constructions through `n=7` | External review only |
| Conditioned-prefix identity | Proved and audited | Algebraic proof; every cut through `n=8` | External review only |
| Tail below a cut is a direct sum of subtree frames | Proved and audited | Exact angle map; every cut through `n=8` | External review only |
| Coherent router acts correctly on arbitrary prefix--suffix entanglement | Proved and audited | Basis-permutation proof; dense arbitrary-state checks | External review only |
| Router auxiliary registers return clean | Proved and tested | Exact inverse routing and leakage checks | External review only |
| Exact copied-control count is `(2**t-1)(s+1)-t` | Proved and tested | Independent combinatorial ledger | None internally |
| Routed construction fits in `2*2**t*(s+1)` clean ancillas | Proved and tested | Complete data/token/copy/flag ledger | External review only |
| One controlled `s`-qubit subtree frame has size `O(2**s)` and depth `O(s**2+2**s/s)` | Proved relative to exact UCG/MCT lemmas | Width-by-width summation | External review only |
| All subtree frames run in parallel | Proved | Disjoint branch data, token, and flag registers | External review only |
| Positive-workspace real frame has `O(N)` size and optimal depth | Internally audited theorem | Routed construction plus low-workspace reduction | External review |
| Real-frame size lower bound is `Omega(N)` | Proved | Real-state manifold dimension | External review |
| Real-frame depth lower bound is `Omega(n+N/(n+m))` | Proved | Parameter count and light-cone argument | External review |
| Positive-workspace separated complex frame has the same optimal profile | Internally audited corollary | Clean diagonal reuse | External review |
| Strict zero-ancilla frame has depth `O(N)` and size `O(nN)` | Proved relative to exact UCG synthesis | Full-width zero-angle UCG fallback | Sharp endpoint open |
| Exact arbitrary diagonal has size `O(N)` and depth `O(n+N/(n+m))` | Proved relative to exact synthesis results | Common-workspace audit | External review |
| Frame-safe recompilation preserves global estimator distribution | Proved algebraically | Reducing-subspace substitution theorem | External review |
| State-column equality is insufficient for global Hopf QBP | Proved by explicit counterexample | Two-qubit marker SWAP | None internally |
| Checkpoint active-interface safety preserves estimator means | Proved algebraically | Interface adjoint theorem | External review |
| Checkpoint state-column equality is insufficient | Proved by explicit counterexample | Two-qubit sign-flip suffix | None internally |
| Active-interface equality need not preserve full checkpoint distributions | Proved by explicit example | Same mean, TV distance `1/4` | None internally |
| Record-wise magnitude decoding costs `O(SN)` | Established constructively | Exact parity/FWHT equivalence tests | Constants only if useful |
| Direct phase decoding costs `O(S+N)` | Established constructively | Signed-bin tests; norm-two records | None internally |
| Parameter generation costs `O(Nn)` classical work | Accounted for | UCG angle transforms and diagonal FWHT | Finite implementation constants |
| General theorem for arbitrary charts | Not claimed | Current geometry and routing are Hopf-specific | Identify a proved larger class first |

## Source and theorem hierarchy

### Theorem A: frame-safe substitution

A clean implementation of the same differential-frame operator preserves the
complete global output distribution and every derived estimator property.

### Proposition B: state-column obstruction

Preparing the same state does not determine the tangent-marker columns. The
original decoder can therefore return an incorrect gradient.

### Theorem C: optimal positive-workspace real frame

For every `m>=1`,

```math
S_{\mathbb R}(n,m)=\Theta(N),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

### Theorem D: optimal positive-workspace separated complex frame

The exact diagonal compiler reuses the same clean workspace pool and is
asymptotically no larger than the real-frame block. Hence the same size and
depth profile holds for `W_C`.

### Theorem E: checkpoint active-interface substitution

A clean suffix compiler equal to the designated suffix on the complete active
interface, up to one common phase, preserves every checkpoint estimator mean.
State-column equality alone is insufficient.

### Corollary: compiler-robust Hopf backpropagation

Combine the frame-safe theorem, optimal compiler, shared global magnitude
record, direct phase record, and output-sensitive decoders. Accuracy and
controlled-observable assumptions must be stated separately.

### Open endpoint problem

Resolve the simultaneous strict-zero-workspace, sharp-size, optimal-depth
triple, or prove that one clean flag changes the achievable tradeoff.

## Paper threshold

1. Frame-safe substitution theorem. **Met internally.**
2. Explicit compiler-boundary counterexamples. **Met internally.**
3. Audited real and separated-complex compiler theorem for all `m>=1`.
   **Met internally.**
4. Matching size and depth lower bounds. **Met internally.**
5. Quantum size, depth, workspace, parameter-generation, and classical-decoder
   accounting. **Met for the compiler/decoder core.**
6. Clear strict `m=0` positioning. **Met as an explicit open endpoint; stronger
   resolution remains desirable.**
7. Controlled-observable and statistical-accuracy conventions. **To freeze for
   the manuscript.**
8. External proof review. **Open.**
9. Full manuscript drafting and cross-check against the earlier Hopf papers.
   **Open.**

## Present release decision

- Suitable for private research development: **yes**.
- Positive-workspace optimal theorem internally audited: **yes**.
- Suitable for public release as an externally checked theorem: **not yet**.
- Suitable as the main technical basis of the new manuscript: **yes**.
- Strict `m=0` endpoint fully solved: **no**.
- Suitable for merging into the established `Hopf-QBP` paper repository: **no**.
