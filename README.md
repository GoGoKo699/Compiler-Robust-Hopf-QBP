# Compiler-Robust Hopf Quantum Backpropagation

Theory, compiler constructions, and exact validation for quantum backpropagation
from Hopf differential frames.

## Research status

This repository is the source of truth for a new research project.

The established starting point is that global Hopf quantum backpropagation
survives an exact Möttönen-style multiplexed recompilation with `O(N)` circuit
size. The present project asks a broader question:

> Which parts of Hopf quantum backpropagation belong to the Hopf chart itself,
> and which compiler transformations preserve its resource scaling?

The real-frame construction has now passed an internal line-by-line proof audit
relative to the exact synthesis lemmas it imports. Let

```math
N=2^n,
\qquad
t=
\min\left\{
n,
\max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\}.
```

The audited theorem gives a frame-safe implementation of the complete real
global Hopf frame with size

```math
O(N)
```

and depth

```math
O\left(
n(n-t+1)+\frac{N}{n+m}
\right).
```

It uses the same `m` clean ancillary qubits as the matched state compiler for
every `m>=1`. At the strict `m=0` endpoint, the present construction uses one
clean reusable suffix flag. Equivalently, the uniform workspace bound is

```math
\max\{1,m\}.
```

This reproduces the three depth upper profiles in Figure 1 of Sun, Tian, Yang,
Yuan, and Zhang. Whether the complete Hopf frame attains the later optimal
all-ancilla frontier

```math
\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every `m` remains an open target.

The proof audit, including its corrections and boundaries, is in
[`docs/PROOF_AUDIT_ISSUE_1.md`](docs/PROOF_AUDIT_ISSUE_1.md). A
common-workspace complex theorem and an explicit compiler-obstruction example
are still required before the project is ready for a public manuscript claim.

## Conceptual claim under investigation

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

A compiler inherits global Hopf backpropagation scaling only when it implements
the complete differential frame cleanly and at cost comparable to forward state
preparation. State-column equality alone is insufficient.

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

The main target is the **global differential-frame protocol**. Checkpoint
protocols depend on intermediate circuit factorizations and are not assumed to
survive arbitrary recompilation.

## Relationship to the earlier repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | Balanced Hopf coordinates, inverse map, metric, and tangent preparation |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | Established global, direct-phase, and checkpoint gradient protocols for the designated Hopf realization, plus Möttönen-style robustness |
| **This repository** | New paper on chart-native differential frames and compiler-robust resource scaling |

This repository is independently executable. Shared definitions are copied only
when needed and are tracked in [`SYNC.md`](SYNC.md) and
[`provenance/upstream.json`](provenance/upstream.json).

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
| `docs/ANCILLA_DEPTH_ROBUSTNESS.md` | Audited real-frame theorem and proof architecture |
| `docs/PROOF_AUDIT_ISSUE_1.md` | Line-by-line audit, corrections, endpoints, and source-theorem map |
| `docs/OPTIMAL_ALL_ANCILLA_TARGET.md` | Stronger optimal-frontier question and research routes |
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

Issue #1 is addressed by the current proof-audit branch. It should be closed
only after the audited changes are reviewed and merged.

## Evidence boundary

Finite tests establish exact matrix identities, clean-subspace action,
unary-code preservation, decoder parity, endpoint bookkeeping, and the explicit
geometric-tail inequality. They do not prove imported circuit-synthesis
theorems. Those deductions are stated separately and tied to the hypotheses of
the cited compiler literature.

The current project does not claim:

- that the inverse of an arbitrary state-preparation compiler is a valid reverse
  frame;
- preservation of one Hopf coordinate as one elementary gate angle;
- strict zero-extra-ancilla compilation at `m=0`;
- the common-workspace complex theorem;
- routed-device depth or noise robustness;
- approximate Clifford+T error bounds;
- compiler-invariant checkpoint interfaces;
- a general theorem for arbitrary coordinate charts.

## License

MIT. See [`LICENSE`](LICENSE).
