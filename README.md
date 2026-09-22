# Optimal Compilation of Hopf Differential Frames

### One prescribed frame, exact logical and fault-tolerant compilation

Exact state preparation normally specifies one initialized input:

```math
|0^n\rangle|0^m\rangle
\longmapsto
|\psi\rangle|0^m\rangle.
```

The Hopf backpropagation circuit uses a prescribed unitary completion.  Its preparation
unitary contains the target state in the first column and prescribed coordinate
frame directions in designated nonzero columns.  The inverse of this complete
unitary is then used to read a common objective response.

| Synthesis task | Required action |
|---|---|
| Exact state preparation | fix $U\lvert 0^n\rangle$ |
| Hopf differential-frame compilation | fix $W\lvert x\rangle$ for every system basis state $\lvert x\rangle$ and restore workspace according to its input promise |

This repository asks whether the prescribed Hopf completion can retain the same
size–depth frontier as arbitrary state preparation, and what implementing the
same frame costs at finite precision. The exact logical theorem covers every
clean-workspace budget. The fault-tolerant theorem gives a matched T-count
frontier in its stated clean/dirty-workspace regime.

<p align="center">
  <img src="assets/state-vs-frame.svg" width="900" alt="State preparation fixes one column, whereas Hopf differential-frame compilation fixes the state and designated frame columns." />
</p>

## Two resource models

The mathematical target is the complete frame in both models. Their resource
bounds describe different compiler constructions; they do not assert one
circuit that simultaneously minimizes every cost.

| Model | Resource question | Scope of the matching theorem |
|---|---|---|
| Arbitrary one-qubit gates and CNOTs | exact size and depth versus clean workspace | real and phase-dressed complex magnitude frames, every clean budget |
| Clifford+T | T-count versus accuracy and clean/dirty workspace | prescribed real frame, every precision above the sufficient clean reservation below |

### Exact logical theorem

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

The upper bounds hold for every parameter tuple. The matching lower bounds
hold in the worst case over the Hopf-frame family, uniformly in the
clean-workspace budget. They do not impose the same cost on every individual
frame.

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

### Fault-tolerant theorem

Let $a$ be the number of initialized clean qubits and $b$ the number of borrowed
qubits in an arbitrary unknown state. Write

```math
q=n+a+b,\qquad
L=\max\{6,\lceil\log_2(1/\eta)\rceil\},\qquad
h=1+\lceil\log_2(L+n+2)\rceil.
```

For $0<\eta\leq1/64$ and a sufficiently large fixed constant $C$, the prescribed
real frame has matching worst-case T-count

```math
\boxed{
T^\star(n,a,b,\eta)
=\Theta\left(\sqrt{NL}+L+\frac{NL}{n+a+b}\right),
\qquad a\geq C(n+h).
}
```

The upper construction uses $O(NL)$ Clifford gates. Every supplied precision
source is prepared and charged. Borrowed qubits are restored jointly with any
external reference; complete-input approximation includes clean-work leakage.
There are no measurements, resets, or free supplied catalysts in this model.

**Why the precision cost can be shared.** First approximate the frame coarsely.
Its structured residual is corrected using binary coefficient tables. One small
geometric source supplies the binary weights across the entire correction
stream. Returning that source accurately on accepted branches permits one
shared preparation per base block. Final amplification repeats that block only
a constant number of times, giving the single additive $L$ term.
The [fault-tolerant chapter](docs/FAULT_TOLERANT_COMPILER.md) gives the proof,
register ledger, and inherited primitives.

At $L=N$, sufficient $a=\Theta(n)$ and $b=\Theta(N)$ give $T^\star=\Theta(N)$.
The new [operator-source construction](research/constant_clean/OPERATOR_SOURCE_COMPILER.md)
uses **three clean qubits** and $N+O(\log N)$ dirty qubits to give
$O(N\log N)$ T gates for arbitrary real frames at the same precision.
The lower bound remains $\Omega(N)$: **a logarithmic gap is still open**.
The [progress report](research/CONSTANT_CLEAN_PROGRESS.md) explains the construction
and its explicit workspace requirement; smaller clean allocations retain the
earlier bounds.

The exact-model complex theorem remains separately stated. The displayed
fault-tolerant theorem is for the real frame; literal complex phase conventions
and a separate leaf-phase stream require their own accounting.

## Exact construction at a glance

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
| 30–40 minutes | **[complete technical narrative](REVIEW.md)** | shared contract, the two resource models, and the QBP consequence |
| full audit | **[exact theorem](docs/COMPILER_THEOREM.md)**, **[T-count theorem](docs/FAULT_TOLERANT_COMPILER.md)**, and **[verification map](docs/VERIFICATION.md)** | proofs, register schedules, evidence limits, and source dependencies |

Focused pages are available for the unfamiliar parts:

| Page | Contents |
|---|---|
| [Minimal Hopf interface](docs/HOPF_INTERFACE.md) | tree coordinates, marker columns, chart domains, singular coordinates, and addressed layers |
| [Complete compiler theorem](docs/COMPILER_THEOREM.md) | all three workspace schedules, explicit router, workspace ledger, and optimality |
| [Finite-precision compiler](docs/FAULT_TOLERANT_COMPILER.md) | complete error contract, shared source, clean/dirty resource bounds |
| [Approximate QBP](docs/QBP_APPROXIMATION.md) | circuit error transferred to fixed-parameter gradient-estimator bias |
| [QBP consequence](docs/QBP_CONSEQUENCE.md) | frame-safe substitution, raw-coordinate accuracy, and the matched-program cost statement |
| [Verification and evidence](docs/VERIFICATION.md) | proof-to-code correspondence and exact finite checks |
| [Source map](docs/SOURCE_MAP.md) | every inherited fact, imported theorem, local proof, implementation, and test |
| [Related work](docs/RELATED_WORK.md) | state preparation, UCGs, borrowed workspace, and the narrow contribution boundary |

A reader needs quantum circuits, operator norms, and basic asymptotic notation.
The [minimal Hopf interface](docs/HOPF_INTERFACE.md) supplies the geometry;
knowledge of the earlier Hopf papers is useful but not required. Begin with the
two-qubit example in the narrative before reading the compiler machinery.

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

for every system input $\lvert\varphi\rangle$, not only the forward preparation input.

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

At finite precision, the [approximation bridge](docs/QBP_APPROXIMATION.md)
controls the bias of the same fixed-parameter, bounded-score estimator. It uses
the actual compiled circuit and its actual adjoint. It does not differentiate a
discontinuous family of compiled words. Frame-synthesis lower bounds alone do
not establish optimal gradient-query or training complexity.

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

The fault-tolerant evidence adds exact finite source/kernel identities and
rational resource checks. It does not yet provide a general elementary emitter
for the complete asymptotic shared-source compiler. See the
[focused reproduction guide](verification/fault_tolerant/README.md).

Device connectivity, physical noise thresholds, optimal T-depth, arbitrary
non-Hopf charts, and application-independent observable costs remain outside
the claims. Clifford work, T work, quantum executions, and classical output
costs are reported separately.

## Reproduce the checks

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/verify_fault_tolerant.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

## Relationship to the Hopf repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | coordinate chart, inverse map, metric, tangent preparation, and optimization interface |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | global, direct-phase, and checkpoint gradient records, including the earlier Möttönen-style robustness result |
| **This repository** | complete-frame contracts, exact and fault-tolerant compilation, and their scoped QBP consequences |

The exact fact-level dependencies are listed in
[the source map](docs/SOURCE_MAP.md).

## Status and license

The exact compiler and fault-tolerant construction have the analytical and
finite evidence identified in the [verification map](docs/VERIFICATION.md).
The [source map](docs/SOURCE_MAP.md) distinguishes inherited ingredients from
local constructions. These records are internal research evidence; no external
review or exhaustive novelty certification is claimed.  The repository is
licensed under MIT; see [`LICENSE`](LICENSE).