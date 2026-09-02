# Compiler-Robust Hopf Quantum Backpropagation

Theory, compiler constructions, exact boundaries, and deterministic validation
for quantum backpropagation from Hopf differential frames.

## Research status

This repository is the source of truth for a new research project.

The established starting point is that global Hopf quantum backpropagation
survives an exact Möttönen-style multiplexed recompilation with `O(N)` circuit
size. The present project asks a broader question:

> Which parts of Hopf quantum backpropagation belong to the Hopf chart itself,
> and which compiler transformations preserve its resource scaling?

The real and separated complex compiler theorems have passed internal
line-by-line audits relative to the exact synthesis lemmas they import. Let

```math
N=2^n,
\qquad
t=
\min\left\{
n,
\max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\}.
```

The complete real frame and the separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

admit exact frame-safe implementations with size

```math
O(N)
```

and depth

```math
O\left(
n(n-t+1)+\frac{N}{n+m}
\right).
```

For every `m>=1`, the real and diagonal blocks reuse the same `m` clean
ancillary qubits as the matched state-preparation budget. At nominal `m=0`, the
sharp-size construction uses one reusable real-frame flag. A strict
zero-ancilla fallback has depth `O(N)` and size `O(nN)`.

The diagonal block itself has an exact all-budget clean implementation of size
`O(N)` and depth

```math
O\left(n+\frac{N}{n+m}\right).
```

The current frame compiler reproduces all three depth upper profiles in Figure
1 of Sun, Tian, Yang, Yuan, and Zhang. Whether the complete frame attains the
later optimal all-ancilla frontier

```math
\Theta\left(n+\frac{N}{n+m}\right)
```

for every `m` remains open.

The compiler boundary is also now exact. State-column equality alone is
insufficient for both global and checkpoint reverse circuits. The global method
requires the complete differential-frame action. A checkpoint compiler may be
weaker, but it must preserve the complete active checkpoint interface rather
than only the one prepared prefix state. Exact two-qubit counterexamples and an
active-interface substitution theorem are in
[`docs/COMPILER_BOUNDARIES.md`](docs/COMPILER_BOUNDARIES.md).

The main technical documents are:

- [`docs/PROOF_AUDIT_ISSUE_1.md`](docs/PROOF_AUDIT_ISSUE_1.md): audited real-frame construction;
- [`docs/COMPLEX_COMMON_WORKSPACE.md`](docs/COMPLEX_COMMON_WORKSPACE.md): separated complex common-workspace theorem;
- [`docs/COMPILER_BOUNDARIES.md`](docs/COMPILER_BOUNDARIES.md): exact negative results and checkpoint interface theorem.

These are internal mathematical audits, not external peer review.

## Conceptual claim

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
the complete differential frame cleanly and at cost sufficiently close to
forward state preparation. A checkpoint compiler instead needs a
factorization-specific active-interface contract.

## Exact compiler hierarchy

| Compiler promise | Scalar state | Checkpoint means | Global distribution |
|---|---:|---:|---:|
| One prepared state column | sufficient | insufficient | insufficient |
| Complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| Complete frame-safe operator | sufficient | sufficient where applicable | sufficient |

The repository includes:

- a two-qubit global example in which a SWAP of two marker columns preserves the
  state but changes the decoded gradient from `(2,0,0)` to `(0,sqrt(2),0)`;
- a two-qubit checkpoint suffix that preserves the final state but flips the
  decoded derivative from `2` to `-2`;
- an interface-safe suffix whose full output distribution changes by total
  variation `1/4` while the checkpoint mean remains exact.

## Scope

This repository studies:

- frame-safe compilation;
- checkpoint active-interface compilation;
- exact state-column counterexamples;
- exact conditioned-prefix identities for addressed Hopf frames;
- unary realizations by parallel two-mode Givens layers;
- ancillary-space versus circuit-depth tradeoffs;
- clean arbitrary-diagonal synthesis under a common workspace budget;
- output-sensitive classical decoding;
- lower-bound transfer from universal state preparation;
- common phase, phase gauge, and singular leaves;
- limits of compiler invariance.

The main positive resource theorem concerns the **global differential-frame
protocol**. Checkpoint protocols remain tied to a chosen factorization, even
though compilers may act arbitrarily outside the certified active interface.

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
python scripts/complex_workspace_ledger.py --n 10
```

## Repository map

| Path | Role |
|---|---|
| `docs/RESEARCH_STATUS.md` | Current claim status, unresolved points, and release gates |
| `docs/FRAME_SAFE_COMPILATION.md` | Global and checkpoint logical contracts |
| `docs/COMPILER_BOUNDARIES.md` | Explicit counterexamples and active-interface theorem |
| `docs/ANCILLA_DEPTH_ROBUSTNESS.md` | Audited real-frame theorem and proof architecture |
| `docs/PROOF_AUDIT_ISSUE_1.md` | Real-frame line-by-line audit and corrections |
| `docs/COMPLEX_COMMON_WORKSPACE.md` | Complex-frame theorem, gauge, and end-to-end accounting |
| `docs/OPTIMAL_ALL_ANCILLA_TARGET.md` | Stronger optimal-frontier question and research routes |
| `docs/OUTPUT_SENSITIVE_DECODING.md` | Classical decoding complexity |
| `docs/CLAIM_SUPPORT.md` | Claim-by-claim evidence map |
| `compiler_robust_hopf/` | Independent analytic implementation and resource ledgers |
| `tests/` | Deterministic exact checks |
| `scripts/ancilla_depth_ledger.py` | Real-frame term ledger |
| `scripts/complex_workspace_ledger.py` | Complex common-workspace ledger |
| `SYNC.md` | Authority, provenance, and synchronization procedure |
| `provenance/upstream.json` | Exact upstream commits and file lineage |
| `manuscript/` | Reserved for the paper after the remaining scientific decision |

## Current work queue

1. [Real-frame proof audit](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/1) — addressed by stacked PR #5.
2. [Optimal all-ancilla depth](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/2) — open central research target.
3. [Complex common-workspace theorem](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/3) — addressed by stacked PR #6.
4. [State-column and checkpoint boundary](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/issues/4) — addressed by the current stacked branch.

## Evidence boundary

Finite tests establish exact matrix identities, clean-subspace action,
unary-code preservation, diagonal parameter transforms, phase gauge, singular
leaves, decoder parity, explicit counterexample distributions, endpoint
bookkeeping, and resource inequalities. They do not prove imported
circuit-synthesis theorems. Those deductions are tied separately to the cited
compiler literature.

The current project does not claim:

- that an arbitrary state-preparation inverse is a valid reverse frame;
- that one prepared checkpoint state determines a valid reverse interface;
- preservation of one Hopf coordinate as one elementary gate angle;
- optimal all-ancilla frame depth;
- simultaneous `O(N)` size and strict zero additional workspace at `m=0`;
- equality of full checkpoint distributions under active-interface compilation;
- routed-device depth or noise robustness;
- approximate Clifford+T error bounds;
- a general theorem for arbitrary coordinate charts.

## License

MIT. See [`LICENSE`](LICENSE).
