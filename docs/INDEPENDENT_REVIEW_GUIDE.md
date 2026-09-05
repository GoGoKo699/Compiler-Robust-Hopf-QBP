# Technical reading map

[Landing page](../README.md) · [Complete technical narrative](../REVIEW.md)

The repository is organized as a linear technical note with linked proof and
verification pages.  Its development history is not needed.

## Pass I: statement and construction map

Read the [landing page](../README.md) for:

- the distinction between one prepared column and a prescribed unitary
  completion;
- the all-workspace theorem;
- the three compiler schedules;
- the relation to the state-preparation framework;
- the exact circuit model and scope boundary.

The central comparison is

```math
|0^n\rangle|0^m\rangle
\longmapsto
|\psi\rangle|0^m\rangle
```

versus

```math
|x\rangle|0^m\rangle
\longmapsto
W|x\rangle|0^m\rangle
\qquad\text{for every }x.
```

## Pass II: complete proof chain

The [complete narrative](../REVIEW.md) proceeds in the following order:

1. frame-safe compilation and the two-qubit state-column obstruction;
2. the minimal Hopf operator interface;
3. the exact compiler toolkit;
4. the strict-zero borrowed-suffix echo;
5. the direct positive-workspace schedule;
6. the tree cut, binary–one-hot decoder, and coherent router;
7. matching lower bounds;
8. the phase-dressed complex magnitude frame;
9. the matched quantum-backpropagation consequence.

All load-bearing operator identities and asymptotic estimates appear in that
single route.

## Pass III: focused derivations and executable evidence

| Page | Main use |
|---|---|
| [Hopf interface](HOPF_INTERFACE.md) | tree coordinates, marker columns, chart domains, singular coordinates, and addressed layers |
| [Compiler theorem](COMPILER_THEOREM.md) | theorem-and-lemma proof, exact register schedules, and optimality |
| [QBP consequence](QBP_CONSEQUENCE.md) | frame-safe substitution, statistical target, and matched-program cost |
| [Verification map](VERIFICATION.md) | proof-to-code correspondence and evidence levels |
| [Source map](SOURCE_MAP.md) | exact inherited facts, imported results, local proofs, implementations, and tests |
| [Related work](RELATED_WORK.md) | state-preparation lineage, borrowed workspace, and contribution boundary |

The internal audits remain available after the primary proof:

- [consolidated proof audit](PROOF_AUDIT.md);
- [strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md);
- [clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md).

They document independent internal reconstructions and do not replace the
formal proof.

## The theorem

Let $N=2^n$.  In the exact all-to-all logical model with arbitrary one-qubit
gates and CNOTs, for every $m\geq0$,

```math
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(N),
```

```math
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

The complex leaf-phase derivatives use a separate direct measurement stream.

## Imported compiler results

The proof uses four statements from the all-workspace state-preparation
framework:

| Result | Role |
|---|---|
| optimal QSP theorem | target frontier and comparison benchmark |
| ancilla-free multi-controlled X | suffix predicates and toggles |
| all-workspace UCG synthesis | multiplexed rotations, subtree frames, and phase diagonal |
| coherent CNOT copy–uncopy | decoder and router control fanout |

Formal source versions and theorem numbers are listed in the
[source map](SOURCE_MAP.md).

## High-leverage proof checkpoints

The proof is most efficiently assessed at the following interfaces:

1. $\widetilde WJ=JW$ is a complete clean-input equality and implies the adjoint
   relation on the same subspace.
2. The strict-zero echo restores the original suffix qubit on all four sectors
   without a relative phase.
3. Each half-angle UCG has total width $d+2$ and no hidden work wire.
4. The binary–one-hot decoder clears the binary address and returns every
   temporary register clean.
5. The CNOT/Fredkin router is coherent on prefix–suffix-entangled inputs.
6. Cleared copy wires are reused as branch flags only after exact uncomputation.
7. The workspace bound is a simultaneous peak over live registers.
8. The maximal-cut argument includes the $s=1$ endpoint.
9. Parameter capacity and output light cones match the upper-bound depth.
10. The complex magnitude frame and direct phase stream are kept distinct.
11. The runtime ratio compares matched general-family programs with the same
    controlled observable and raw-coordinate accuracy target.

## Reproduce the executable checks

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

The walkthrough and finite tests are falsification tools for conventions,
indices, phases, cleanup, and resource accounting.  The asymptotic theorem rests
on the dimension-independent proof.

## Scope

The theorem is exact and logical.  It does not cover device connectivity,
native-gate depth, approximate Clifford+T synthesis, noise, arbitrary non-Hopf
charts, optimizer convergence, or application-specific controlled-observable
implementations.

[Begin the complete technical narrative →](../REVIEW.md)
