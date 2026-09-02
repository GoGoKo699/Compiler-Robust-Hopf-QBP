# Compiler-Robust Hopf Quantum Backpropagation

Theory, compiler constructions, and exact validation for quantum backpropagation from Hopf differential frames.

## Research status

This repository is the source of truth for a new research project. Its central theorem is still under audit.

The established starting point is that global Hopf quantum backpropagation survives an exact Möttönen-style multiplexed recompilation with `O(N)` circuit size. The present project asks a broader question:

> Which parts of Hopf quantum backpropagation belong to the Hopf chart itself, and which compiler transformations preserve its resource scaling?

The current theorem candidate gives an exact clean implementation of the real global Hopf frame with size `O(N)` and a Sun-style ancilla--depth upper bound

```math
D_{\mathrm{frame}}(n,m)
=
O\left(
 n(n-t+1)+\frac{2^n}{n+m}
\right),
\qquad
t=\min\left\{n,\max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)\right\},
```

using at most `m+1` clean ancillary qubits when the matched state compiler uses `m`. This reproduces the three depth upper profiles in Figure 1 of Sun, Tian, Yang, Yuan, and Zhang. Whether the complete Hopf frame attains the later optimal all-ancilla frontier

```math
\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every `m` remains an open target of this project.

No manuscript-level theorem should be cited from this repository until the status page marks it as proved.

## Conceptual claim under investigation

For the balanced real Hopf chart,

```math
\partial_{\theta_j}|\psi(\boldsymbol\theta)\rangle
=
\sqrt{g_{j,j}}\,|e_j(\boldsymbol\theta)\rangle,
```

and the state together with the normalized coordinate tangents forms a coherent differential frame. The chart supplies:

- the orthogonal tangent geometry;
- the metric weights;
- the computational marker structure;
- the shared norm-controlled gradient record.

A compiler inherits global Hopf backpropagation scaling only when it implements the complete differential frame cleanly and at cost comparable to forward state preparation. State-column equality alone is insufficient.

## Scope

This repository studies:

- frame-safe compilation;
- exact conditioned-prefix identities for addressed Hopf frames;
- unary realizations by parallel two-mode Givens layers;
- ancillary-space versus circuit-depth tradeoffs;
- output-sensitive classical decoding;
- lower-bound transfer from universal state preparation;
- the separated complex Hopf frame;
- limits of compiler invariance.

The main target is the **global differential-frame protocol**. Checkpoint protocols depend on intermediate circuit factorizations and are not assumed to survive arbitrary recompilation.

## Relationship to the earlier repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | Balanced Hopf coordinates, inverse map, metric, and tangent preparation |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | Established global, direct-phase, and checkpoint gradient protocols for the designated Hopf realization, plus Möttönen-style robustness |
| **This repository** | New paper on chart-native differential frames and compiler-robust resource scaling |

This repository is independently executable. Shared definitions are copied only when needed and are tracked in [`SYNC.md`](SYNC.md) and [`provenance/upstream.json`](provenance/upstream.json).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
```

## Repository map

| Path | Role |
|---|---|
| `docs/RESEARCH_STATUS.md` | Current claim status, unresolved points, and release gates |
| `docs/FRAME_SAFE_COMPILATION.md` | Logical contracts and the state-column obstruction |
| `docs/ANCILLA_DEPTH_ROBUSTNESS.md` | Current compiler theorem candidate and proof architecture |
| `docs/OPTIMAL_ALL_ANCILLA_TARGET.md` | Stronger optimal-frontier question and candidate research routes |
| `docs/OUTPUT_SENSITIVE_DECODING.md` | Classical decoding complexity |
| `docs/CLAIM_SUPPORT.md` | Claim-by-claim evidence map |
| `compiler_robust_hopf/` | Independent analytic implementation |
| `tests/` | Deterministic exact checks |
| `scripts/ancilla_depth_ledger.py` | Machine-readable asymptotic term ledger |
| `SYNC.md` | Authority, provenance, and synchronization procedure |
| `provenance/upstream.json` | Exact upstream commits and file lineage |
| `manuscript/` | Reserved for the new paper after theorem stabilization |

## Current work queue

1. [Independent proof audit of the current theorem candidate](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/1)
2. [Optimal all-ancilla depth of the complete Hopf frame](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/2)
3. [Common-workspace theorem for the separated complex frame](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/3)
4. [Minimal state-column counterexample and checkpoint boundary](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/4)

## Evidence boundary

Finite tests can establish exact matrix identities, clean-subspace action, unary-code preservation, decoder parity, and resource bookkeeping premises. They do not prove asymptotic synthesis theorems. Those deductions must be stated separately and tied to the exact hypotheses of the cited compiler literature.

The current project does not claim:

- that the inverse of an arbitrary state-preparation compiler is a valid reverse frame;
- preservation of one Hopf coordinate as one elementary gate angle;
- routed-device depth or noise robustness;
- approximate Clifford+T error bounds;
- compiler-invariant checkpoint interfaces;
- a general theorem for arbitrary coordinate charts.

## License

MIT. See [`LICENSE`](LICENSE).
