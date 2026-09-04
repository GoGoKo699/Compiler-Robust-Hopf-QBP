# Optimal Compilation of Hopf Differential Frames

### A prescribed unitary completion at the all-workspace state-preparation frontier

Exact state preparation normally specifies one initialized input:

```math
|0^n\rangle|0^m\rangle
\longmapsto
|\psi\rangle|0^m\rangle.
```

The Hopf backpropagation circuit uses a more structured map.  Its preparation
unitary contains the target state in the first column and prescribed coordinate
frame directions in designated nonzero columns.  The inverse of this complete
unitary is then used to read a common objective response.

| Synthesis task | Required action |
|---|---|
| Exact state preparation | fix $U\lvert 0^n\rangle$ |
| Hopf differential-frame compilation | fix $W\lvert x\rangle$ for every system basis state $\lvert x\rangle$ and return all workspace clean |

This repository asks whether the prescribed Hopf completion can retain the same
size–depth frontier as arbitrary state preparation.  It can.

<p align="center">
  <img src="assets/state-vs-frame.svg" width="900" alt="State preparation fixes one column, whereas Hopf differential-frame compilation fixes the state and designated frame columns." />
</p>

## Main theorem

Let

```math
N=2^n
```

and let $m\geq0$ be the number of clean ancillary qubits.  In the exact all-to-all
logical model with arbitrary one-qubit gates and CNOTs,

```math
\boxed{
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The real result concerns the complete Hopf differential frame.  The complex
result concerns the phase-dressed magnitude frame

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

The leaf-phase derivatives form a separate direct measurement stream; they are
not additional columns of the same $N$-dimensional unitary.

The construction uses at most the requested $m$ clean ancillary qubits and
returns them exactly to zero.  Thus a prescribed Hopf completion reaches the
optimal arbitrary-state-preparation frontier for every clean-workspace budget.

## Construction at a glance

The Hopf frame is a product of addressed tree layers.  At depth $d$, the prefix
selects one rotation angle and the complete lower suffix supplies a shared
all-zero predicate.  Three schedules exploit this structure.

| Workspace | Schedule | Mechanism |
|---:|---|---|
| $m=0$ | borrowed-suffix echo | one original suffix data qubit carries the predicate temporarily and is restored exactly |
| $1\leq m<4n$ | direct flagged UCG | one reusable clean flag stores the suffix-zero predicate |
| larger $m$ | routed parallel subframes | a tree cut turns the tail into a direct sum; the suffix is routed coherently and the subtree frames run in parallel |

The threshold $4n$ is a convenient uniform proof threshold, not an optimized
finite-size crossover.

<p align="center">
  <img src="assets/literature-lineage.svg" width="940" alt="The all-workspace state-preparation line and the Hopf differential-frame line meet in the optimal complete-frame compiler." />
</p>

## Read the repository in three passes

The repository is arranged as a technical website.  No knowledge of its branch,
issue, or pull-request history is needed.

| Time | Route | Purpose |
|---:|---|---|
| 5 minutes | this page | problem, theorem, and construction map |
| 30–40 minutes | **[complete technical narrative](REVIEW.md)** | the proof chain from one prescribed completion to compiler-robust QBP |
| full audit | **[compiler theorem](docs/COMPILER_THEOREM.md)** and **[verification map](docs/VERIFICATION.md)** | register schedules, upper and lower bounds, exact tests, and source dependencies |

Focused pages are available for the unfamiliar parts:

| Page | Contents |
|---|---|
| [Minimal Hopf interface](docs/HOPF_INTERFACE.md) | tree coordinates, marker columns, chart domains, singular coordinates, and addressed layers |
| [Complete compiler theorem](docs/COMPILER_THEOREM.md) | all three workspace schedules, explicit router, workspace ledger, and optimality |
| [QBP consequence](docs/QBP_CONSEQUENCE.md) | frame-safe substitution, raw-coordinate accuracy, and the matched-program cost statement |
| [Verification and evidence](docs/VERIFICATION.md) | proof-to-code correspondence and exact finite checks |
| [Source map](docs/SOURCE_MAP.md) | every inherited fact, imported theorem, local proof, implementation, and test |
| [Related work](docs/RELATED_WORK.md) | state preparation, UCGs, borrowed workspace, and the narrow contribution boundary |

## Why the completion matters

The complete frame satisfies

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
\qquad
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

At a regular coordinate,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where $a_j$ is the oriented amplitude entering the corresponding tree node.  On
the canonical Hopf domains, $a_j\geq0$ and equals the principal metric square
root.  At zero metric weight the raw derivative vanishes, while the marker
column remains the chart-selected orthogonal continuation determined by the
complete parameter tuple.

A state-preparation-equivalent completion may move these marker columns.  The
repository contains an exact two-qubit example in which the state is unchanged
but the decoded gradient changes from

```math
(2,0,0)
\quad\longmapsto\quad
(0,\sqrt2,0).
```

The relevant compiler contract is therefore

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input $\lvert \varphi\rangle$, not only the forward preparation input.

## Relation to the all-workspace state-preparation framework

The proof uses four exact results from the all-workspace state-preparation
framework.

| Imported result | Role here |
|---|---|
| optimal QSP frontier | benchmark and matching comparison |
| ancilla-free multi-controlled X | zero-suffix predicates and toggles |
| all-workspace UCG synthesis | prefix-selected rotations, subtree frames, and the phase diagonal |
| coherent CNOT copy–uncopy | control fanout for the decoder and router |

Once the Hopf frame is written as addressed complete-operator layers, these
primitives can be adapted without surrendering the designated marker columns.
The Hopf-specific work is the operator factorization and the three workspace
schedules, not a replacement for the underlying state-preparation toolkit.

The normative compiler citation is:

> P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits,” *Quantum* **7**, 956 (2023).

The earlier state-preparation paper is retained as the historical predecessor
and original source of selected primitives.  Möttönen and Bergholm provide the
multiplexor and UCG lineage used throughout the discussion.

## Consequence for quantum backpropagation

Frame-safe compilation preserves the complete inverse-frame measurement
distribution.  Under the primary finite-shot target of simultaneous absolute
accuracy for the raw Hopf-coordinate gradient, the global magnitude stream uses

```math
O(\log n)=O(\log\log M)
```

independent executions at fixed accuracy and confidence, where
$M=\Theta(2^n)$ is the number of coordinates.

This is a matched-program statement: scalar and gradient programs use the same
forward preparation family and controlled observable, while the gradient
program adds one inverse frame of the same asymptotic logical depth as optimal
state preparation.  Classical materialization of an $M$-entry output is not
included in that quantum-depth ratio.

## Verification boundary

The repository supplies:

- complete logical matrices for the frame identities and strict-zero echo;
- explicit reversible X/CNOT/Toffoli layers for the binary–one-hot decoder;
- explicit CNOT/Fredkin routing layers and arbitrary-entangled-input tests;
- exact integer or rational resource ledgers;
- parity, histogram, and fast Walsh–Hadamard gradient decoders.

The elementary UCG and multi-controlled-X decompositions are imported from the
state-preparation framework rather than regenerated locally.  Finite checks are
used to expose indexing, phase, order, cleanup, and resource errors; the
asymptotic theorem rests on the dimension-independent proof.

The result does not address device connectivity, native-gate depth,
approximate Clifford+T synthesis, noise, arbitrary non-Hopf charts, or the
application-specific cost of controlled observable access.

## Reproduce the checks

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

## Relationship to the Hopf repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | coordinate chart, inverse map, metric, tangent preparation, and optimization interface |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | global, direct-phase, and checkpoint gradient records, including the earlier Möttönen-style robustness result |
| **This repository** | complete-frame compiler contracts, optimal all-workspace synthesis, and the compiler-robust QBP consequence |

The exact fact-level dependencies are listed in
[the source map](docs/SOURCE_MAP.md).

## Status and license

The theorem has passed the analytic and executable checks documented in this
repository and is ready for independent technical review.  The repository is
licensed under MIT; see [`LICENSE`](LICENSE).