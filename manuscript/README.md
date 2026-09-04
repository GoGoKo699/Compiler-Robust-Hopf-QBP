# Manuscript architecture

The repository contains the complete proof and executable support for one
all-workspace Hopf-frame compiler.  The intended paper should preserve the same
compiler-first question chain as [`REVIEW.md`](../REVIEW.md), while moving
constant-bearing ledgers and repeated verification material to appendices.

## Working title

**Optimal Compilation of Hopf Differential Frames for Quantum Backpropagation**

The title should remain Hopf-specific unless a broader prescribed-frame theorem
is proved.

## Central statement

Let $N=2^n$.  For every clean-workspace budget $m\geq0$, the real Hopf
differential frame and phase-dressed complex magnitude frame have exact
frame-safe implementations with

```math
S=\Theta(N),
\qquad
D=\Theta\left(n+\frac{N}{n+m}\right).
```

The complete complex coordinate gradient combines this magnitude-frame stream
with a separate direct leaf-phase stream.

The compiler theorem matches the optimal arbitrary-state-preparation frontier
in the same exact logical model.  Its distinguishing requirement is that a
prescribed unitary completion, rather than one initialized state column, must be
preserved.

## Opening question chain

The introduction should establish the following sequence before presenting the
construction.

1. Exact state preparation fixes one initialized column of a unitary.
2. The global Hopf gradient circuit applies the inverse of a prescribed
   state-and-marker frame.
3. A state-equivalent completion can therefore corrupt the gradient.
4. The Hopf frame has addressed zero-suffix tree structure absent from a generic
   unitary.
5. That structure permits the all-workspace state-preparation toolkit to be
   adapted without losing the prescribed columns.
6. The resulting complete frame reaches the same optimal size–depth frontier.
7. Compiler-robust QBP follows as a matched-program consequence.

The numerical two-qubit obstruction should appear immediately after the
compiler-contract distinction.

## Geometric convention

For unrestricted magnitude angles,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where $a_j$ is the oriented incoming amplitude.  On the canonical Hopf domains,
$a_j\geq0$ and equals the principal metric square root.

Canonical domains:

- real depths $0,\ldots,n-2$: $[0,\pi/2]$;
- final real depth: $[0,2\pi)$;
- complex magnitude angles: $[0,\pi/2]$.

If $g_{j,j}=0$, the raw differential vanishes.  The marker column is the
chart-selected orthogonal continuation determined by the complete parameter
tuple, not a normalized nonzero derivative.

## Compiler source policy

The active exact compiler framework and QSP comparison benchmark is P. Yuan and
S. Zhang, *Quantum* **7**, 956 (2023):

- Theorem 2: optimal QSP frontier;
- Lemma 5: ancilla-free multi-controlled X;
- Lemma 6: all-workspace UCG synthesis;
- Lemma 9: coherent copy–uncopy.

The published article corresponds to `arXiv:2202.11302v2`; the imported
statements were checked against v3.  The preceding state-preparation paper is
cited as the historical predecessor and original source of selected primitives.
Möttönen and Bergholm supply the multiplexor/UCG lineage.

The preferred relational wording is:

> Once the Hopf completion is exposed as a product of addressed
> complete-operator layers, the state-preparation primitives can be adapted
> while preserving the designated marker columns.

## Theorem chain

1. **Hopf differential-frame interface.** State column, marker columns,
   oriented differential weights, and canonical domains.
2. **Frame-safe substitution.** Complete clean-input equality implies the exact
   inverse-frame relation.
3. **State-column obstruction.** The two-qubit completion changes the decoded
   gradient while preserving the state.
4. **Borrowed-suffix echo.** One addressed nonfinal layer is implemented at
   strict zero workspace.
5. **Strict-zero optimality.** The complete real frame has $\Theta(N)$ size and
   $\Theta(n+N/n)$ depth.
6. **Conditioned-prefix identity.** The first $t$ depths are a smaller frame
   conditioned on the external zero suffix.
7. **Tail direct sum.** The remaining depths split into $2^t$ subtree frames.
8. **Binary–one-hot decoder.** The prefix frame is implemented in $O(t)$ depth
   and $O(2^t)$ size.
9. **Coherent router.** Route–controlled-subframes–unroute realizes the tail and
   clears all workspace.
10. **All-workspace real theorem.** Direct and routed schedules attain the upper
    bound; parameter capacity and light cones provide the lower bound.
11. **Complex magnitude corollary.** One phase UCG preserves the same frontier.
12. **Matched QBP corollary.** Frame-safe compilation adds no new asymptotic
    depth factor to the global inverse-frame record.
13. **Checkpoint interface theorem.** A factorization-specific active interface
    supports a weaker substitution statement.

## Preferred paper structure

1. Introduction: from one prepared column to a prescribed completion
2. Hopf differential-frame interface
3. Compiler contracts and the two-qubit obstruction
4. Exact circuit model and imported state-preparation toolkit
5. Strict-zero borrowed-suffix echo
6. Tree cut and conditioned prefix
7. Coherent routing and workspace parallelism
8. All-workspace optimality
9. Phase-dressed complex magnitude frame
10. Compiler-robust global QBP
11. Checkpoint interface and limitations
12. Discussion

The four-sector echo proof, explicit router action, simultaneous workspace peak,
maximal-cut inequality, and main theorem belong in the main text.  Detailed gate
and register ledgers may move to appendices.

## Runtime and statistical wording

The primary finite-shot target is simultaneous absolute accuracy of the raw
Hopf-coordinate gradient.  Complete-vector, relative, normalized-frame, and
natural-gradient targets have different conditioning.

The scalar and gradient programs should be compared as

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E(D_{\mathrm{prep}}+D_O),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}).
```

At fixed comparable scalar and raw-coordinate absolute accuracy and confidence,
the inverse frame changes per-execution depth only by a constant asymptotic
factor and the execution overhead is $O(\log n)=O(\log \log M)$.  The statement is
for the same general state family and controlled observable; it excludes
classical output materialization and instance-specific scalar shortcuts.

## Contribution boundary

Do not claim invention of UCGs, controlled-unitary roots, Pauli-conjugation
echoes, borrowed or conditionally clean qubits, toggle detection, or reversible
routing.

The strict-zero statement is the Hopf-specific reduction of one addressed depth
to two total-width-$d+2$ UCGs and linear predicate toggles using one restored
logical suffix bit.  The positive-workspace statement is the Hopf-specific tree
cut, clean decoder, and coherent router attaining the full workspace frontier.

## Evidence already available

- complete frame and strict-zero operator tests;
- canonical-domain and singular-coordinate tests;
- exact global and checkpoint compiler-boundary fixtures;
- explicit decoder and router schedules;
- arbitrary-entangled-input routing tests;
- token, copy, flag, and additional-data cleanup;
- one-UCG phase diagonal;
- integer and exact-rational resource ledgers;
- output-sensitive magnitude and direct-phase decoders;
- source, claim, and evidence maps;
- three internal proof reconstructions.

## Remaining manuscript work

- obtain independent technical review of the strict-zero echo, router,
  workspace peak, maximal-cut bound, lower bounds, and matched QBP statement;
- complete the closest-prior-art check and freeze claim wording;
- cross-check notation against both Hopf manuscripts;
- decide whether any resource plot adds information beyond the circuit and tree
  diagrams;
- prepare and audit the complete LaTeX package;
- update `CITATION.cff` after a manuscript identifier is available.

The abstract may state the theorem directly, while distinguishing internal
verification from independent review and keeping the contribution claim
Hopf-specific.
