# Technical reading guide

[Landing page](../README.md) · [Start the complete narrative](../REVIEW.md)

This repository is designed to be read as a small technical website. No
knowledge of its development history is required.

The central result is stated, motivated, proved, and connected to executable
checks in one linear document:

> **[Read `REVIEW.md`](../REVIEW.md)**

A first complete reading is intended to take approximately 35–45 minutes for a
reader familiar with quantum circuit synthesis but not with Hopf coordinates.

## Recommended route

### 1. Read the narrative

[`REVIEW.md`](../REVIEW.md) introduces:

- the synthesis problem in state-preparation language;
- the minimal Hopf interface;
- a fully numerical two-qubit obstruction to state-column-only compilation;
- the strict-zero borrowed-suffix echo;
- the positive-workspace tree-cut and routing compiler;
- matching lower bounds;
- the separated complex frame;
- the quantum-backpropagation consequence.

Every major section ends with two aids:

- **What should be checked here?** identifies the possible failure points;
- **Executable counterpart** links directly to the relevant implementation and
  tests.

### 2. Inspect the focused proof pages as needed

| Page | Use |
|---|---|
| [Minimal Hopf interface](HOPF_INTERFACE.md) | exact state, tangent, marker, and addressed-layer conventions |
| [Complete compiler theorem](COMPILER_THEOREM.md) | full all-workspace operator and resource proof |
| [QBP consequence](QBP_CONSEQUENCE.md) | frame-safe substitution, shared records, and scaling consequence |
| [Verification and evidence](VERIFICATION.md) | exact finite checks, resource ledgers, and internal audit roles |
| [Source map](SOURCE_MAP.md) | fact-level paper, theorem, implementation, and test dependencies |
| [Related work](RELATED_WORK.md) | compiler lineage and narrow contribution boundary |

### 3. Run the short executable walkthrough

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/reviewer_walkthrough.py
```

The walkthrough checks eight representative identities in a readable order. It
is an orientation tool, not a proof certificate.

The complete deterministic suite and resource ledgers are:

```bash
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

## The theorem being assessed

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits. In the exact all-to-all
model with arbitrary one-qubit gates and CNOTs, the complete real Hopf
differential frame and the separated complex frame are claimed to have
frame-safe implementations with

```math
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(N),
```

```math
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every integer `m>=0`.

The result is stronger than state preparation because the circuit must preserve
the complete state-and-tangent frame on every system input and return all
workspace to zero.

## Imported circuit results

The sole active external compiler framework and state-preparation benchmark is
P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023). The proof uses their:

- Theorem 2 for the optimal state-preparation frontier;
- Lemma 5 for exact ancilla-free multi-controlled X;
- Lemma 6 for exact all-workspace UCG synthesis;
- Lemma 9 for coherent CNOT-tree copy–uncopy.

The earlier Sun et al. paper is cited as the historical predecessor. The
Möttönen/Bergholm, controlled-unitary, borrowed-workspace, and restricted-UCG
lines are credited where they enter the construction or contribution boundary.

## Main points that merit close inspection

1. The frame-safe contract is genuinely stronger than state-column equality.
2. The strict-zero four-sector echo restores the borrowed logical bit with no
   relative phase.
3. The half-angle UCG has total width `d+2` and uses no hidden work wire.
4. The binary–one-hot decoder clears its input address and returns all temporary
   registers clean.
5. The routed compiler remains correct on prefix–suffix entangled inputs.
6. The peak workspace is a simultaneous register count, not a sum of sequential
   stages.
7. The maximal-cut argument covers every large-workspace endpoint.
8. The real-state parameter and light-cone lower bounds match the upper bound.
9. The complex phase diagonal is one exact UCG and reuses the same workspace.
10. The final QBP comparison keeps executions, logical depth, output size, and
    controlled-observable cost separate.

## Evidence boundary

The repository contains multiple internal proof audits and exact finite tests.
These make the assumptions and likely failure points visible, but they do not
constitute independent verification.

The result is confined to the declared exact logical model. Hardware routing,
Clifford+T approximation, noise, and application-specific controlled-observable
costs are separate questions.

[Start the complete narrative →](../REVIEW.md)
