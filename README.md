# Compiler-Robust Hopf Quantum Backpropagation

Theory, exact compiler constructions, compiler boundaries, and deterministic
validation for quantum backpropagation from Hopf differential frames.

## Research status

This repository is the source of truth for a new research project. The central
positive-workspace compiler result has now passed two internal proof audits,
relative to the exact circuit-synthesis lemmas cited in the audit documents.
It has not received external peer review.

Let

```math
N=2^n.
```

For every positive clean-workspace budget `m>=1`, the complete real Hopf
frame and the separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

have exact frame-safe implementations using at most the requested `m` clean
ancillary qubits, with

```math
\boxed{
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The upper bound uses a tree-cut direct sum and a coherent
route--parallel-subframes--unroute construction. The lower bound follows by
applying the frame to `|0^n>` and adapting parameter-count and backward-light-
cone arguments to the `(N-1)`-dimensional real state sphere.

This matches the optimal arbitrary-state-preparation frontier of Yuan and Zhang
for every `m>=1`. The relevant QSP benchmark is their **Theorem 2**. Figure 1
of that paper concerns general unitary synthesis, not the QSP frontier.

The strict `m=0` endpoint remains deliberately separate:

| Clean ancillary qubits | Exact size | Exact depth upper bound |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

It remains open whether strict zero workspace can simultaneously achieve
`O(N)` size and `O(n+N/n)` depth.

The cumulative audited near-optimal fallback is preserved on
`near-optimal-audited-2026-09` at manifest commit
`24f339b863faa2ac92e1adb3917cbef7dc24d3b8`. Optimality work does not rewrite
that branch.

## Main documents

- [`docs/OPTIMALITY_AUDIT_ISSUE_9.md`](docs/OPTIMALITY_AUDIT_ISSUE_9.md):
  independent audit of the optimal positive-workspace theorem and source map;
- [`docs/OPTIMALITY_CHECKPOINT_1.md`](docs/OPTIMALITY_CHECKPOINT_1.md):
  routed parallel-subframe construction;
- [`docs/PROOF_AUDIT_ISSUE_1.md`](docs/PROOF_AUDIT_ISSUE_1.md):
  audited near-optimal real-frame construction;
- [`docs/COMPLEX_COMMON_WORKSPACE.md`](docs/COMPLEX_COMMON_WORKSPACE.md):
  exact diagonal synthesis, separated complex frame, gauge, and end-to-end
  accounting;
- [`docs/COMPILER_BOUNDARIES.md`](docs/COMPILER_BOUNDARIES.md):
  state-column counterexamples and checkpoint active-interface theorem;
- [`docs/CLAIM_SUPPORT.md`](docs/CLAIM_SUPPORT.md): claim-by-claim evidence map.

## Why this is a chart-and-compiler result

For the balanced real Hopf chart,

```math
\partial_{\theta_j}|\psi(\boldsymbol\theta)\rangle
=
\sqrt{g_{j,j}}\,|e_j(\boldsymbol\theta)\rangle,
```

and the state together with the normalized coordinate tangents forms a coherent
differential frame. The chart supplies:

- the orthogonal tangent geometry;
- the metric weights;
- the computational marker structure;
- the shared norm-controlled gradient record.

The resource theorem additionally needs a **frame-safe compiler**. A compiled
unitary with clean workspace is frame-safe when, for every system input,

```math
\widetilde W
\bigl(|\varphi\rangle|0^w\rangle\bigr)
=
\bigl(W|\varphi\rangle\bigr)|0^w\rangle.
```

Equality on the prepared state column alone is insufficient. A two-qubit
counterexample in this repository preserves the Hopf state exactly while
changing the decoded gradient from `(2,0,0)` to `(0,sqrt(2),0)`.

## Optimal compiler architecture

Cut the addressed frame after `t` prefix qubits and write `s=n-t`, `B=2^t`.
The tail has the exact full-operator decomposition

```math
R_t^{(n)}
=
\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A coherent binary-tree router moves the existing suffix register and a one-hot
activation token into one of `B` disjoint branch registers. All controlled
subtree frames then run in parallel, after which inverse routing returns every
auxiliary data, token, copied-control, and branch-flag register to zero.

The routed construction fits in the conservative workspace envelope

```math
2B(s+1)\leq m.
```

Choosing the largest feasible cut gives the optimal positive-workspace depth.
For `1<=m<4n`, the separately audited low-workspace compiler is already of
optimal order.

The generic controlled-state-preparation shortcut is not used. Treating all
`N` frame columns as unrelated targets gives generic size `O(N^2)` and leaves a
coherent input column label that still has to be removed.

## Exact compiler hierarchy

| Compiler promise | Scalar state | Checkpoint means | Global Hopf distribution |
|---|---:|---:|---:|
| One prepared state column | sufficient | insufficient | insufficient |
| Complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| Complete frame-safe operator | sufficient | sufficient where applicable | sufficient |

For a checkpoint factorization `U=B_dA_d`, a clean suffix compiler is
active-interface safe when

```math
\widetilde B_d J P_d
=e^{i\chi}J B_dP_d.
```

This preserves every designated checkpoint estimator mean under consistent
forward/reverse use. It need not preserve the complete checkpoint output
distribution.

## Complex chart and classical work

The exact arbitrary diagonal has an all-budget clean implementation of size
`O(N)` and depth

```math
O\left(n+\frac{N}{n+m}\right)
```

using at most `m` clean ancillas. It reuses the real-frame workspace
sequentially, so workspace costs take a maximum rather than a sum.

Compiler phase parameters are generated by one length-`N` Walsh transform in
`O(Nn)` classical arithmetic. Complete-gradient decoding is output-sensitive:

```math
T_{\mathrm{mag}}=O(S_{\mathrm{mag}}N),
\qquad
T_{\mathrm{phase}}=O(S_{\mathrm{phase}}+N).
```

The direct phase stream uses no inverse differential frame.

## Relationship to earlier repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | Balanced Hopf coordinates, inverse map, metric, and tangent preparation |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | Established Hopf gradient protocols and Möttönen-style compiler robustness |
| **This repository** | Frame-safe compilation, optimal positive-workspace depth, compiler boundaries, and the new manuscript |

Shared definitions are copied only when needed and are tracked in
[`SYNC.md`](SYNC.md) and [`provenance/upstream.json`](provenance/upstream.json).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
python scripts/complex_workspace_ledger.py --n 10
python scripts/optimality_ledger.py --n 12
```

## Repository map

| Path | Role |
|---|---|
| `compiler_robust_hopf/frames.py` | Independent real and separated complex frame constructions |
| `compiler_robust_hopf/ancilla_depth.py` | Audited near-optimal compiler ledger |
| `compiler_robust_hopf/optimal_parallel.py` | Tree-cut direct sum, coherent router, and optimality planner |
| `compiler_robust_hopf/optimal_audit.py` | Independent register and inequality audit helpers |
| `compiler_robust_hopf/complex_resources.py` | Common-workspace diagonal and complex-frame ledger |
| `compiler_robust_hopf/compiler_boundaries.py` | Exact global and checkpoint counterexamples |
| `compiler_robust_hopf/decoders.py` | Output-sensitive magnitude and phase decoders |
| `tests/` | Deterministic exact checks |
| `docs/RESEARCH_STATUS.md` | Current theorem status and release gates |
| `docs/CLAIM_SUPPORT.md` | Evidence classification for every material statement |
| `manuscript/` | Paper planning and, after review, manuscript source |

## Current work queue

1. External proof review of the positive-workspace theorem and its lower bound.
2. Resolve or sharply characterize the strict `m=0` endpoint.
3. Freeze controlled-observable and statistical-accuracy conventions for the
   manuscript.
4. Draft the paper around the audited theorem hierarchy without broadening the
   claim to arbitrary coordinate charts.

## Evidence boundary

The repository contains dimension-independent proofs, exact finite operator
checks, explicit counterexamples, resource ledgers, and CI. The asymptotic
compiler theorems import exact synthesis results from the cited literature; the
repository does not reimplement every elementary decomposition gate by gate.

The project does not currently claim:

- strict-zero-workspace optimality;
- routed-hardware or noise-optimal depth;
- approximate Clifford+T error bounds;
- compiler-invariant checkpoint distributions;
- a theorem for arbitrary state-space charts;
- external peer-review status.

## License

MIT. See [`LICENSE`](LICENSE).
