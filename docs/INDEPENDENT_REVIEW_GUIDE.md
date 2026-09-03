# Technical reading guide

[Landing page](../README.md) · [Start the complete narrative](../REVIEW.md)

This repository is designed to be read as a small technical website. No
knowledge of its development history is required. The central theorem is
motivated, proved, and connected to executable checks in one linear document:

> **[Read `REVIEW.md`](../REVIEW.md)**

The intended reader may know exact state-preparation compilers without knowing
Hopf coordinates. The compiler theorem can be assessed before the full
quantum-backpropagation protocol.

## Recommended route

### 1. Read the complete narrative

[`REVIEW.md`](../REVIEW.md) introduces:

- the synthesis problem in state-preparation language;
- canonical Hopf angle domains and the oriented incoming amplitude;
- regular differential directions and singular frame continuations;
- a numerical two-qubit obstruction to state-column-only compilation;
- the strict-zero borrowed-suffix echo;
- the clean binary–one-hot prefix decoder;
- the explicit coherent CNOT/Fredkin router;
- matching upper and lower resource bounds;
- the phase-dressed complex magnitude frame and separate phase stream;
- the matched-program quantum-backpropagation consequence.

Every major construction is accompanied by a short list of possible failure
points and direct links to its implementation and tests.

### 2. Use focused pages when a derivation needs expansion

| Page | Use |
|---|---|
| [Minimal Hopf interface](HOPF_INTERFACE.md) | exact domains, oriented differential, singular coordinates, markers, and addressed layers |
| [Complete compiler theorem](COMPILER_THEOREM.md) | the three all-workspace schedules, explicit router, resource proof, and lower bounds |
| [QBP consequence](QBP_CONSEQUENCE.md) | frame-safe substitution, statistical task boundaries, and matched runtime definition |
| [Verification and evidence](VERIFICATION.md) | implementation levels, exact finite tests, resource ledgers, and internal audits |
| [Source map](SOURCE_MAP.md) | paper version, theorem, implementation, and test dependencies |
| [Related work](RELATED_WORK.md) | compiler lineage and conservative contribution boundary |

### 3. Run the executable orientation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/reviewer_walkthrough.py
```

The walkthrough checks representative frame, compiler-boundary, strict-zero,
phase-UCG, schedule, workspace, and resource identities. The complete
deterministic suite and ledgers are:

```bash
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

These commands are falsification tools for finite conventions and
implementations, not proof certificates.

## The theorem being assessed

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits. In the exact all-to-all
model with arbitrary one-qubit gates and CNOTs, the real Hopf differential frame
and the phase-dressed complex magnitude frame are claimed to have frame-safe
implementations with

```math
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(N),
```

```math
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every integer `m>=0`.

The result is stronger than state preparation because the circuit must preserve
the complete state-and-marker frame on every system input and return all
workspace to zero. The complex leaf-phase derivatives are recovered by a
separate direct record rather than by additional columns of the magnitude
frame.

## Geometric convention to check first

For unrestricted real angles,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where `a_j` is the oriented incoming amplitude. On the canonical Hopf domains,
`a_j>=0`, so `a_j=sqrt(g_(j,j))`. If `g_(j,j)=0`, the raw differential vanishes;
the unit marker column is a canonical orthogonal continuation, not the
normalization of a nonzero derivative.

This distinction is encoded in both the proof and tests.

## Imported circuit results

The sole active external compiler framework and state-preparation benchmark is
P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023). The published article
corresponds to `arXiv:2202.11302v2`. The proof uses:

- Theorem 2 for the optimal state-preparation frontier;
- Lemma 5 for exact ancilla-free multi-controlled X;
- Lemma 6 for exact all-workspace UCG synthesis;
- Lemma 9 for coherent CNOT-tree copy–uncopy.

The same statements were checked in `arXiv:2202.11302v3` and retain the forms
used here. The earlier Sun et al. paper is cited as the historical predecessor.
The Möttönen/Bergholm, controlled-unitary, borrowed-workspace, and restricted-
UCG lines are credited where they enter the construction or claim boundary.

## Main points that merit close inspection

1. Frame safety is a complete clean-input operator equality, not first-column
   equality.
2. The strict-zero four-sector echo restores the borrowed logical bit without a
   sector-dependent phase.
3. Each half-angle UCG has total width `d+2` and no hidden work wire.
4. The binary–one-hot decoder clears its address and returns every temporary
   register clean.
5. The explicit router's fanout and Fredkin layers are coherent, disjoint, and
   correct on prefix–suffix-entangled inputs.
6. Branch flags reuse only prefix-copy wires that have already been cleared.
7. The peak workspace is a simultaneous live-register count, not a sum of
   sequential stages.
8. The maximal-cut inequality covers every large-workspace endpoint.
9. The real-state parameter and light-cone lower bounds match the upper bound.
10. The phase diagonal is one exact UCG, while phase derivatives remain a
    separate direct stream.
11. The runtime ratio compares matched general-family programs with the same
    controlled observable and raw-coordinate accuracy convention.
12. Finite tests, explicit schedules, imported elementary synthesis, and
    asymptotic ledgers are not conflated.

## Evidence boundary

The binary–one-hot decoder and coherent router are explicit reversible
constructions. Frame and strict-zero identities are checked as complete logical
operators. Elementary UCG and multi-controlled-X synthesis is imported from
Yuan–Zhang. Resource bounds use analytic sums and integer or exact-rational
ledgers.

The result remains subject to independent technical verification. Hardware
routing, Clifford+T approximation, noise, optimizer convergence, and
application-specific controlled-observable implementations are separate
questions.

[Start the complete narrative →](../REVIEW.md)
