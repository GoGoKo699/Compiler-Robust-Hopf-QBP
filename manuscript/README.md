# Manuscript workspace

The repository now contains a single internally audited compiler architecture.
A paper draft may begin after the consolidation branch is reviewed and merged.
No theorem should be described as externally verified until an independent human
proof review is complete.

## Working title

**Optimal Compilation of Hopf Differential Frames for Quantum Backpropagation**

The title should remain Hopf-specific unless a theorem is later proved for a
larger class of coordinate charts.

## Central claim

Let `N=2**n`. For every positive clean-workspace budget `m>=1`, the complete
real Hopf differential frame and the separated complex frame admit exact
frame-safe implementations with

```math
S=\Theta(N),
\qquad
D=\Theta\left(n+\frac{N}{n+m}\right),
```

using at most the requested `m` clean ancillary qubits. Complete coherent access
to the Hopf state and all normalized magnitude-coordinate directions therefore
matches the optimal arbitrary-state-preparation space--time frontier.

The strict `m=0` endpoint remains separate and must be stated explicitly.

## One-source compiler policy

The active external compiler framework and QSP benchmark are Yuan and Zhang,
*Quantum* **7**, 956 (2023):

- Theorem 2 for the optimal QSP frontier;
- Lemma 5 for multi-controlled X;
- Lemma 6 for uniformly controlled gates;
- Lemma 9 for coherent copy--use--uncopy.

Sun et al., *IEEE TCAD* **42**, 3301--3314 (2023), should be cited for the
historical ancilla--depth development and original attribution of selected
primitives. It is not presented as an alternative compiler chosen in some
workspace regime.

The manuscript should not mention an imported unary-to-binary compiler or a
separately sourced phase-polynomial diagonal compiler. The active construction
uses the project's own reversible tree decoder and one Yuan--Zhang UCG for the
entire phase diagonal.

## Intended contribution chain

1. Define the Hopf coherent differential frame.
2. Prove frame-safe substitution for the global gradient protocol.
3. Give the two-qubit state-column obstruction.
4. Prove the conditioned-prefix identity.
5. Prove the tree-cut tail direct sum.
6. Construct the clean binary--one-hot tree decoder.
7. Construct coherent branch routing and parallel controlled subtree frames.
8. Prove the optimal positive-workspace real-frame upper bound.
9. Prove the matching real-state size and depth lower bounds.
10. Implement the complete complex phase layer as one UCG and reuse the same
    workspace pool.
11. Include output-sensitive magnitude and phase decoding.
12. State the checkpoint active-interface theorem and counterexamples.
13. Isolate the strict-zero and broader-chart questions.

## Provisional theorem hierarchy

- **Theorem 1: Hopf differential frame.**
- **Theorem 2: frame-safe substitution.**
- **Proposition 3: state-column equality is insufficient.**
- **Lemma 4: conditioned-prefix identity.**
- **Lemma 5: tail direct-sum identity.**
- **Lemma 6: clean binary--one-hot tree decoder.**
- **Lemma 7: coherent routed parallel tail.**
- **Theorem 8: optimal positive-workspace real Hopf frame.**
- **Corollary 9: optimal positive-workspace separated complex frame.**
- **Theorem 10: checkpoint active-interface substitution.**
- **Corollary 11: compiler-robust global Hopf backpropagation.**

The numbering is provisional.

## Preferred paper structure

1. Introduction
2. Hopf coordinates and coherent differential frames
3. Compiler contracts and state-column obstruction
4. Exact Hopf tree factorization
5. Unified optimal frame compiler
6. Size and depth optimality
7. Separated complex frame
8. End-to-end quantum backpropagation
9. Checkpoint interfaces and limitations
10. Discussion and open endpoints

Detailed reversible-gate schedules, lower-bound constants, and exhaustive
workspace ledgers can be placed in appendices while the tree-cut identity and
main compiler remain in the main text.

## Completed internal gates

- frame-safe global substitution;
- exact global and checkpoint compiler-boundary examples;
- conditioned-prefix and tail direct-sum identities;
- self-contained reversible tree decoder with explicit disjoint layers;
- unified direct/routed real-frame compiler;
- one-UCG complex phase compiler;
- optimal positive-workspace upper and lower bounds;
- complete workspace reuse;
- output-sensitive magnitude and direct-phase decoders;
- frozen earlier fallback branch;
- unified internal proof audit and claim-support map.

## Remaining drafting and release gates

- complete the consolidation pull request and remove obsolete active modules;
- external human review of the tree decoder, routed register ledger, cut
  inequality, and lower bound;
- decide whether to pursue strict `m=0` before submission or leave it as an
  explicit open problem;
- freeze the controlled-observable and accuracy notation;
- cross-check notation against both earlier Hopf papers;
- decide the minimum useful construction diagrams and resource plots;
- compile and audit a complete manuscript package;
- update `CITATION.cff` only after a manuscript identifier exists.

## Abstract discipline

Until external review, the abstract should avoid language implying community
verification. It may state the theorem as the paper's proved result while the
repository status separately records that the proof has only been checked
internally.
