# Manuscript workspace

The repository contains one internally audited all-workspace compiler
architecture. This page records the intended paper structure, theorem hierarchy,
and claim boundaries. The reader-facing mathematical route begins in
[`../REVIEW.md`](../REVIEW.md).

## Working title

**Optimal Compilation of Hopf Differential Frames for Quantum Backpropagation**

The title should remain Hopf-specific unless a theorem is established for a
broader class of coordinate charts.

## Central claim

Let `N=2**n`. For every clean-workspace budget `m>=0`, the real Hopf
differential frame and the phase-dressed complex magnitude frame admit exact
frame-safe implementations with

```math
S=\Theta(N),
\qquad
D=\Theta\left(n+\frac{N}{n+m}\right),
```

using at most the requested `m` clean ancillary qubits. The complete complex
coordinate gradient combines this magnitude-frame stream with a separate direct
leaf-phase stream.

The compiler theorem matches the optimal arbitrary-state-preparation
size–depth frontier in the Yuan–Zhang model for every ancillary budget. The
result has passed internal analytic and executable checks and is presented for
independent technical review.

## Geometric convention

For unrestricted real magnitude angles, use the oriented incoming amplitude
`a_j`:

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical Hopf domains, `a_j>=0`, so `a_j=sqrt(g_(j,j))`. At a singular
coordinate `g_(j,j)=0`, the raw differential vanishes while the unit marker
column remains a canonical orthogonal continuation of the frame. The manuscript
should not describe that continuation as normalization of a nonzero derivative.

Canonical domains:

- real depths `0,...,n-2`: `[0,pi/2]`;
- real final magnitude depth: `[0,2pi)`;
- complex magnitude angles: `[0,pi/2]` throughout.

## One-source compiler policy

The active external compiler framework and QSP benchmark are Yuan and Zhang,
*Quantum* **7**, 956 (2023):

- Theorem 2 for the optimal QSP frontier;
- Lemma 5 for exact ancilla-free multi-controlled X;
- Lemma 6 for uniformly controlled gates;
- Lemma 9 for coherent copy–use–uncopy.

The published article corresponds to `arXiv:2202.11302v2`. The imported
statements were also checked in `arXiv:2202.11302v3` and retain the forms used
here.

Sun et al., *IEEE TCAD* **42**, 3301–3314 (2023), are cited as the historical
predecessor. The paper is not presented as an alternative compiler selected in
another workspace regime. Möttönen and Bergholm are cited for the UCG and
multiplexor lineage and for the context of the earlier `Hopf-QBP` robustness
result.

## Compiler contribution chain

1. Define the real Hopf frame and phase-dressed complex magnitude frame.
2. State canonical angle domains, oriented incoming amplitudes, and the singular
   coordinate boundary.
3. Prove frame-safe substitution for the global gradient protocol.
4. Give the two-qubit state-column obstruction.
5. Prove the strict-zero borrowed-suffix echo for one addressed layer.
6. Derive optimal strict-zero real and complex-magnitude resources.
7. Prove the conditioned-prefix identity and tree-cut tail direct sum.
8. Construct the clean binary–one-hot tree decoder.
9. Construct the explicit coherent CNOT/Fredkin branch router.
10. Prove route–controlled-subframes–unroute equals the ideal tail direct sum and
    clears data, tokens, copies, and flags.
11. Prove the optimal positive-workspace upper bound and matching real-state
    lower bounds.
12. Combine the schedules into one all-workspace theorem.
13. Implement the complete leaf-phase diagonal as one UCG.
14. Include output-sensitive magnitude and direct-phase decoding.
15. State the matched-program QBP consequence and its statistical task boundary.
16. State the checkpoint active-interface theorem and counterexamples.

## Provisional theorem hierarchy

- **Theorem 1: Hopf differential frame and canonical-domain interpretation.**
- **Theorem 2: frame-safe substitution.**
- **Proposition 3: state-column equality is insufficient.**
- **Lemma 4: borrowed-suffix echo for an addressed Hopf layer.**
- **Theorem 5: optimal strict-zero real Hopf frame.**
- **Lemma 6: conditioned-prefix identity.**
- **Lemma 7: tail direct-sum identity.**
- **Lemma 8: clean binary–one-hot tree decoder.**
- **Lemma 9: explicit coherent routed parallel tail.**
- **Theorem 10: optimal all-workspace real Hopf frame.**
- **Corollary 11: optimal all-workspace phase-dressed complex magnitude frame.**
- **Corollary 12: matched compiler-robust global Hopf backpropagation.**
- **Theorem 13: checkpoint active-interface substitution.**

The numbering is provisional.

## Preferred paper structure

1. Introduction
2. Hopf coordinates and coherent differential frames
3. Compiler contracts and state-column obstruction
4. Ancilla-free borrowed-suffix echo
5. Exact Hopf tree factorization
6. Clean prefix decoding and coherent branch routing
7. All-workspace size and depth optimality
8. Phase-dressed complex magnitude frame and direct phase stream
9. Matched end-to-end quantum backpropagation
10. Checkpoint interfaces and limitations
11. Discussion and broader applicability

The strict-zero echo should appear before the routed construction because it
closes the endpoint not handled by workspace parallelism. The four-sector echo
proof, the explicit router action, and the all-workspace theorem belong in the
main text. Constant-bearing register ledgers may be placed in appendices, but
the simultaneous peak and cut inequality must remain visible.

## Runtime and statistical wording

The primary finite-shot target is simultaneous absolute accuracy of the **raw
Hopf-coordinate gradient**. Complete-vector, relative, normalized-frame, and
natural-gradient targets have different conditioning and execution counts.

The scalar-versus-gradient statement should be written for matched programs:

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E(D_{\mathrm{prep}}+D_O),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}).
```

At fixed comparable scalar and raw-coordinate absolute accuracy and confidence,
the inverse frame adds only a constant per-execution depth factor and the total
overhead is `O(log n)=O(log log M)`. This is a general-family logical-depth
comparison, not a claim against an instance-specialized scalar shortcut, and it
excludes classical output materialization.

## Novelty discipline

The paper should not claim that square-root controlled-unitary decompositions,
borrowed qubits, conditionally clean workspace, toggle detection, or UCGs are
new. Those ideas have established lineages.

The narrow strict-zero contribution is:

> one original suffix data qubit is used as a restored predicate carrier so that
> all prefix-dependent Hopf rotations at tree depth `d` are implemented by two
> total-width-`d+2` UCGs and linear predicate toggles, yielding an optimal
> ancilla-free complete-frame compiler.

The detailed comparison is in
[`../docs/RELATED_WORK.md`](../docs/RELATED_WORK.md).

## Completed internal checks

- frame-safe global substitution;
- exact global and checkpoint compiler-boundary examples;
- canonical-domain, oriented-amplitude, and singular-coordinate checks;
- strict-zero layer and complete-frame operator proofs;
- strict-zero upper/lower resource proof and exact-rational diagnostics;
- conditioned-prefix and tail direct-sum identities;
- self-contained reversible tree decoder;
- explicit coherent router and arbitrary-entangled-input tests;
- token, copy, flag, and data-workspace cleanup;
- direct and routed positive-workspace resource proofs;
- one-UCG complex phase compiler;
- all-workspace upper and lower bounds;
- output-sensitive magnitude and direct-phase decoders;
- current `Hopf-QBP` upstream reconciliation;
- consolidated proof, source, verification, and claim-support maps.

## Remaining scientific work

- obtain independent technical review of the strict-zero echo, explicit router,
  register peak, cut inequality, lower bounds, and matched QBP statement;
- verify the narrow claim boundary against the closest circuit-synthesis
  literature;
- cross-check final manuscript notation against both earlier Hopf papers;
- decide the minimum useful resource plots beyond the current circuit diagrams;
- compile and audit a complete manuscript package;
- update `CITATION.cff` after a manuscript identifier exists.

## Abstract discipline

The abstract may state the theorem as the paper's mathematical result. The
repository should continue to distinguish internal audit from independent
verification and should not describe the general echo ingredients as newly
invented.
