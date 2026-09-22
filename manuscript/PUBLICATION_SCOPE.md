# Publication scope

[Paper architecture](README.md) · [Read the argument](../REVIEW.md) · [Verification](../docs/VERIFICATION.md)

The selected publication is **one full-length theoretical compiler paper
targeting PRX Quantum**. Its scientific ingredients are developed and checked
in this repository before final manuscript writing.
Its subject is the prescribed Hopf differential frame, studied in two resource
models. The constant-clean endpoint is an open problem in the discussion;
resolving it is not a prerequisite for this paper.

Working title: **Exact and Fault-Tolerant Compilation of Hopf Differential Frames**.

## The central claim

Preparing a state fixes one column of a unitary. Hopf quantum backpropagation
uses a prescribed completion containing the state and its coordinate-frame
directions. This paper shows how to compile that stronger operator interface
with optimal exact size/depth and explicit fault-tolerant precision/workspace
tradeoffs. The QBP consequence explains why preserving the extra columns
matters operationally.

This is the connection between CNOT-based logical synthesis and T-count:
they price the same prescribed operator under different gate models. The
theorems use different constructions and do not assert that one circuit
jointly minimizes CNOT count, T-count, depth, and workspace.

## Three principal results

Write $`N=2^n`$, $`n\ge1`$. The exact model uses arbitrary one-qubit gates
and CNOTs with all-to-all connectivity. Its workspace budget is $`m`$ clean
qubits. The coherent Clifford+T model uses $`a`$ clean and $`b`$ dirty
qubits, $`q=n+a+b`$, and

```math
0<\eta\le1/64,\qquad
L=\max\{6,\lceil\log_2(1/\eta)\rceil\},\qquad
h=1+\lceil\log_2(L+n+2)\rceil.
```

Upper bounds hold for every prescribed parameter tuple. Matching lower bounds
are worst-case statements over the specified family, not costs imposed on
every individual frame.

Write $`T^\star_{F,\mathbb R}(n,a,b,\eta)`$ for the worst-case minimum
T-count over real frames, and $`T^\star_{F,\mathbb C,\mathrm{mag}}`$ for
the corresponding complex magnitude family. A displayed $`T^\star`$ bound
applies to each family explicitly named in its row. Supplied angles and phases admit certified evaluation;
classical coefficient generation and table preprocessing are excluded from
the quantum gate counts.

| Result | Statement selected for the paper | Required scope |
|---|---|---|
| **A. Exact complete-frame compilation** | Total elementary size $`\Theta(N)`$, CNOT count $`\Theta(N)`$ for $`n\ge2`$, and depth $`\Theta(n+N/(n+m))`$ | Every integer $`m\ge0`$; real and phase-dressed complex magnitude frames; workspace returned exactly; CNOT count is zero for $`n=1`$ |
| **B. Matching fault-tolerant frontier** | $`T^\star=\Theta(\sqrt{NL}+L+NL/q)`$, with $`O(NL)`$ Clifford cost for the upper construction | Real frame and, by Corollary 7, the phase-dressed complex magnitude frame; sufficient clean reservation $`a\ge C(n+h)`$ for a sufficiently large fixed $`C`$; literal-phase, complete-input error |
| **C. Two-clean compilation** | $`T=O(N+nL)`$, $`G=O(NL)`$ | Real Hopf frame; $`a=2`$, $`b\ge L+n+7`$; complete-input error including operator-core return |

Result A includes a separate CNOT lower bound with arbitrary one-qubit gates
free: a circuit with $`K`$ CNOTs has at most $`n+4K`$ relevant one-qubit
slots after removing inactive clean ancillas. No optimal leading constant is
claimed. Result B is precision-uniform under its clean reservation;
Result C is a different construction with a constant clean allocation.

Proofs: [A](../docs/COMPILER_THEOREM.md),
[B](../docs/FAULT_TOLERANT_COMPILER.md),
[C](../docs/OPERATOR_SOURCE_COMPILER.md).

## A compiler capability beyond Hopf frames

The two-clean mechanism also compiles **every literal diagonal and every
complete one-target U(2) multiplexor**. These corollaries are part of the
scientific case for PRX Quantum, rather than incidental applications.

For a multiplexor with $`k`$ address qubits, one target, and $`M=2^k`$
arbitrary U(2) blocks, the [proof](../docs/OPERATOR_SOURCE_COMPILER.md#81-general-one-qubit-multiplexors-with-two-clean-qubits)
gives

```math
a=2,\quad b\ge2(L+k+7),\qquad
T^\star_{\mathrm{mux}}
=\Theta\!\left(\sqrt{ML}+L+\frac{ML}{k+3+b}\right),
\qquad G=O(ML).
```

The unbanked construction gives $`O(M+L)`$ T gates already at
$`b\ge L+k+7`$. Four addressed Euler factors reuse the same two initialized
flags and arbitrary dirty pool. Certified approximate Euler coordinates
avoid singular inversion assumptions; their classical computation is
separate and has no universal efficiency guarantee for arbitrary input
evaluators. Literal block phases and complete-input error are preserved.

This is one full addressed operation, not a claim for arbitrary many-qubit
unitaries. Composing the noncommuting Hopf layers still incurs the stated
$`nL`$ term with two clean qubits. The [current literature comparison](../docs/RELATED_WORK.md#12-contemporary-comparisons-and-the-broader-compiler-contribution)
distinguishes this clean-workspace guarantee from prior complete multiplexor
and arbitrary-unitary synthesis.

## Corollaries that stay in the paper

These complete the resource picture without becoming separate storylines.

| Corollary | Statement and placement |
|---|---|
| Dirty-bank refinement | With $`a=2`$, $`b\ge2(L+n+7)`$, Result C sharpens to $`T=O(\sqrt{NL}+nL+NL/b)`$. It matches the existing lower bound if $`n^2L\le N`$ or $`b\le N/n`$, subject to that allocation. State beside C; give bank scheduling in the appendix. |
| Literal diagonal synthesis | For $`\ell\ge6`$, two clean qubits give $`O(N+\ell)`$ T gates at error $`2^{-\ell}`$ with $`b\ge\ell+n+5`$. For $`b\ge2(\ell+n+5)`$, the bound $`O(\sqrt{N\ell}+\ell+N\ell/b)`$ matches the diagonal lower bound. Use as a supporting compiler corollary. |
| Complex magnitude frame | Compile $`D_\phi W_{\mathbb R}`$ using independently supplied phases and real Hopf angles. In the two-clean model, splitting the error gives $`b\ge L+n+8`$ for $`O(N+nL)`$ T gates, or $`b\ge2(L+n+8)`$ for the banked bound. This is not arbitrary complex-unitary synthesis. |
| Smaller clean/dirty allocations | Retain the borrowed-workspace upper bound and its restricted all-clean-budget matching splice as an appendix comparison. The splice requires $`h+b\le c\sqrt N`$ for fixed $`c>0`$; it is not an unrestricted constant-clean theorem. |
| Fixed-parameter QBP robustness | Exact substitution preserves the global record. Magnitude bias is at most $`4\lvert a_j\rvert(\eta+\eta_O)`$; the separate phase-vector bias is at most $`4(\eta+\eta_O)`$. The full complex gradient, reflection-sum observables, rounded classical weights, and correlated dirty-bank reuse have explicit error and cost budgets. |

The exact, sufficient-clean, and two-clean complex extensions have their
own proofs. Leaf-phase derivatives use a separate measurement stream;
they are not extra columns of the magnitude frame.

## The common error contract

Let $`J_a`$ append the initialized clean work. The finite-precision target is

```math
\|VJ_a-J_a(W\otimes I_b)\|_{\rm op}\le\eta.
```

This includes all system inputs, arbitrary dirty inputs and their external
references, and leakage outside the clean-work subspace. Literal phases are
retained. No measurements, resets, postselection, or free supplied precision
sources are used.

The sufficient-clean compiler returns its dirty work exactly. In the
two-clean construction, lookup banks, selectors, and suffix-control work
return exactly, while the operator core returns approximately within the
displayed norm. The paper must preserve this distinction wherever it states
workspace return.

QBP concerns simultaneous absolute accuracy of the raw coordinate gradient
at a fixed ideal parameter tuple. It assumes phase-calibrated controlled
access to the specified Hermitian-unitary observable. The matched-program
comparison separately charges quantum executions, per-execution circuit
cost, and classical output. It neither differentiates a discretely synthesized
gate word nor proves optimality among all gradient algorithms.

## The unresolved endpoint

The selected high-precision point is

```math
a=2,\qquad b=N+n+7,\qquad L=N,
\qquad
\Omega(N)\le T^\star\le O(N\log N).
```

This gap is stated once in the main results and revisited in the discussion.
The paper does not claim that the repeated $`nL`$ charge is necessary, or
that every constant clean allocation and every linear dirty allocation has
the same upper bound. Restrictions on particular source-processing interfaces
do not supply an additive full-frame lower bound.

## Main text and appendices

| Location | Contents |
|---|---|
| Main text | Operational necessity of the full frame; shared contract; Results A–C and resource regimes; two-clean diagonal and multiplexor capability; proof mechanisms; complex-gradient consequence; open endpoint |
| Technical appendices | Echo, decoder, and router schedules; source preparation and exact primitive costs; residual composition and inherited failure compression; amplification and error sums; dirty queries/banks; Euler and diagonal proofs; lower-bound reductions; QBP concentration and classical preprocessing |

Exploratory attenuation, modular, batching, clock, and catalysis investigations
are outside the selected manuscript and the active repository. Their earlier
versions remain recoverable through the snapshot identified in
[provenance](../provenance/README.md). The current proof chapters contain all
dependencies of the three principal results and retained corollaries.

## Contribution and evidence boundaries

The local claims concern the complete-operator factorizations, workspace
schedules, precision-uniform residual composition, and two-clean geometric
operator construction that yield these resource guarantees. Hopf geometry
and QBP records are inherited from the earlier Hopf work. UCG synthesis,
dirty lookup, Clifford-algebra loaders, geometric weighting, and oblivious
amplification, and block-product compression retain their established attribution in the
[source map](../docs/SOURCE_MAP.md).

The submission is a theoretical construction paper with executable finite
checks. Those checks support fragile identities, conventions, and resource
ledgers; they do not prove universal statements, certify priority, or supply
a general elementary Clifford+T emitter. Hardware connectivity, physical
noise thresholds, optimal T-depth, optimizer convergence, and practical
end-to-end speedups are outside the selected claims.

## Scientific ingredients before final writing

Each ingredient has one primary home; the final manuscript draws on this
package rather than introducing unsupported research claims during writing.

| Ingredient | Scientific content and primary home |
|---|---|
| Necessity of the target | [Frame-safe contract](../docs/FRAME_SAFE_COMPILATION.md): universal fixed-decoder means force the full frame at regular points, up to common phase; sharp sensitivity and singular exceptions |
| Exact resources | [Exact theorem](../docs/COMPILER_THEOREM.md): complete constructions, all clean budgets, total size, CNOT-only count, and depth lower bounds |
| Precision sharing | [Fault-tolerant proof](../docs/FAULT_TOLERANT_COMPILER.md): sufficient-clean frontier, residual-dictionary sufficient condition, all charged source/history work, and complex extension |
| Constant-clean capability | [Operator-source proof](../docs/OPERATOR_SOURCE_COMPILER.md): two-clean frame, matched diagonal and multiplexor frontiers, exact source T minima, dirty/reference return, and finite certified preprocessing |
| Operational consequence | [Approximation proof](../docs/QBP_APPROXIMATION.md): complete complex gradients, general reflection sums, weight errors, conditional-mean concentration under dirty-bank reuse, and quantum/classical costs |
| Comparisons and attribution | [Related work](../docs/RELATED_WORK.md) and [source map](../docs/SOURCE_MAP.md): input families, precision, initialized/borrowed work, current general-unitary baselines, and inherited compression |
| Reproducible evidence | [Verification](../docs/VERIFICATION.md): native finite two-clean circuits, actual inverse and rejected-work composition, source witnesses, gradient fixtures, and exact receipts |
| Honest unresolved question | [Open endpoint](../docs/OPEN_PROBLEM.md): the remaining logarithmic full-frame gap, the limit of the exact-source lower bound, and the sufficient global-block contract still to be constructed |

Final writing assembles these established statements and proofs into one
argument with consistent notation and bibliography. No general elementary
Clifford+T emitter, hardware experiment, or solution of the open endpoint is
asserted by this package. External technical feedback on the complete draft
and final submission preparation follow. Selecting PRX Quantum does not itself
establish that the journal's exceptionality threshold has been met.
