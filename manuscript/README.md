# Manuscript workspace

The repository contains one internally audited all-workspace compiler
architecture. A full paper draft should begin only after the final consolidation
branch is stable and the independent proof/prior-art review plan is fixed.

## Working title

**Optimal Compilation of Hopf Differential Frames for Quantum Backpropagation**

The title should remain Hopf-specific unless a theorem is proved for a broader
class of coordinate charts.

## Central claim

Let `N=2**n`. For every clean-workspace budget `m>=0`, the complete real Hopf
differential frame and the separated complex frame admit exact frame-safe
implementations with

```math
S=\Theta(N),
\qquad
D=\Theta\left(n+\frac{N}{n+m}\right),
```

using at most the requested `m` clean ancillary qubits. Complete coherent access
to the Hopf state and all normalized magnitude-coordinate directions therefore
matches the optimal arbitrary-state-preparation space--time frontier for every
ancillary budget.

The result is internally audited and should not be described as externally
verified.

## One-source compiler policy

The active external compiler framework and QSP benchmark are Yuan and Zhang,
*Quantum* **7**, 956 (2023):

- Theorem 2 for the optimal QSP frontier;
- Lemma 5 for exact multi-controlled X;
- Lemma 6 for uniformly controlled gates;
- Lemma 9 for coherent copy--use--uncopy.

Sun et al., *IEEE TCAD* **42**, 3301--3314 (2023), should be cited for the
historical ancilla--depth development and original attribution of selected
primitives. It is not presented as an alternative compiler selected in another
workspace regime.

Möttönen and Bergholm should be cited for the UCG/multiplexor lineage and the
earlier `Hopf-QBP` robustness result.

## Compiler contribution chain

1. Define the Hopf coherent differential frame.
2. Prove frame-safe substitution for the global gradient protocol.
3. Give the two-qubit state-column obstruction.
4. Prove the strict-zero borrowed-suffix echo for one addressed layer.
5. Derive optimal strict-zero real and complex frame resources.
6. Prove the conditioned-prefix identity.
7. Prove the tree-cut tail direct sum.
8. Construct the clean binary--one-hot tree decoder.
9. Construct coherent branch routing and parallel controlled subtree frames.
10. Prove the optimal positive-workspace frame upper bound.
11. Prove the matching real-state size and depth lower bounds.
12. Combine the schedules into one all-workspace theorem.
13. Implement the complete complex phase layer as one UCG.
14. Include output-sensitive magnitude and phase decoding.
15. State the checkpoint active-interface theorem and counterexamples.

## Provisional theorem hierarchy

- **Theorem 1: Hopf differential frame.**
- **Theorem 2: frame-safe substitution.**
- **Proposition 3: state-column equality is insufficient.**
- **Lemma 4: borrowed-suffix echo for an addressed Hopf layer.**
- **Theorem 5: optimal strict-zero Hopf frame.**
- **Lemma 6: conditioned-prefix identity.**
- **Lemma 7: tail direct-sum identity.**
- **Lemma 8: clean binary--one-hot tree decoder.**
- **Lemma 9: coherent routed parallel tail.**
- **Theorem 10: optimal all-workspace real Hopf frame.**
- **Corollary 11: optimal all-workspace separated complex frame.**
- **Corollary 12: compiler-robust global Hopf backpropagation.**
- **Theorem 13: checkpoint active-interface substitution.**

The numbering is provisional.

## Preferred paper structure

1. Introduction
2. Hopf coordinates and coherent differential frames
3. Compiler contracts and state-column obstruction
4. Ancilla-free borrowed-suffix echo
5. Exact Hopf tree factorization
6. Positive-workspace routed compiler
7. All-workspace size and depth optimality
8. Separated complex frame
9. End-to-end quantum backpropagation
10. Checkpoint interfaces and limitations
11. Discussion and broader applicability

The strict-zero echo should appear before the routed construction because it
closes the only endpoint not handled by the workspace-parallel architecture.
The complete register schedules and constant-bearing inequalities may be placed
in appendices, but the four-sector echo proof and the all-workspace theorem
belong in the main text.

## Novelty discipline

The paper should not claim that square-root controlled-unitary decompositions,
borrowed ancillas, or toggle detection are new. Those ideas have established
lineages.

The claim-safe strict-zero contribution is:

> one original suffix data qubit is used as a restored predicate carrier so that
> all prefix-dependent Hopf rotations at tree depth `d` are implemented by two
> total-width-`d+2` UCGs and linear-size predicate toggles, yielding an optimal
> ancilla-free complete-frame compiler.

A broader prior-art review is required before this wording is frozen.

## Completed internal gates

- frame-safe global substitution;
- exact global and checkpoint compiler-boundary examples;
- strict-zero layer operator proof and complete-frame construction;
- strict-zero upper/lower resource proof and exact-rational diagnostics;
- conditioned-prefix and tail direct-sum identities;
- self-contained reversible tree decoder;
- unified direct/routed positive-workspace compiler;
- one-UCG complex phase compiler;
- all-workspace upper and lower bounds;
- complete workspace reuse;
- output-sensitive magnitude and direct-phase decoders;
- frozen earlier fallback branch;
- consolidated internal proof and claim-support maps.

## Remaining drafting and release gates

- finish one final all-workspace consolidation pull request;
- obtain independent human review of the strict-zero echo, routed register
  ledger, cut inequality, and lower bounds;
- broaden the prior-art search and freeze novelty wording;
- freeze controlled-observable and accuracy notation;
- cross-check notation against both earlier Hopf papers;
- decide the minimum useful circuit diagrams and resource plots;
- compile and audit a complete manuscript package;
- update `CITATION.cff` after a manuscript identifier exists.

## Abstract discipline

Until independent review, the abstract may state the theorem as the paper's
proved result, but the repository status should continue to distinguish internal
audit from external verification. The abstract should not describe the generic
echo as newly invented.
