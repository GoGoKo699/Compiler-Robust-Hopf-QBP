# Publication scope

[Paper architecture](README.md) · [Read the argument](../REVIEW.md) · [Sanity check](../docs/SANITY_CHECK.md)

The selected publication is **one full-length theoretical compiler paper**.
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

Here $`T^\star=T^\star_{F,\mathbb R}(n,a,b,\eta)`$ denotes the worst-case
minimum T-count over the prescribed real Hopf-frame family at those declared
resources and error. Supplied angles and phases admit certified evaluation;
classical coefficient generation and table preprocessing are excluded from
the quantum gate counts.

| Result | Statement selected for the paper | Required scope |
|---|---|---|
| **A. Exact complete-frame compilation** | Total elementary size $`\Theta(N)`$ and depth $`\Theta(n+N/(n+m))`$ | Every integer $`m\ge0`$; real Hopf frame and phase-dressed complex magnitude frame; workspace returned exactly |
| **B. Matching fault-tolerant frontier** | $`T^\star=\Theta(\sqrt{NL}+L+NL/q)`$, with $`O(NL)`$ Clifford cost for the upper construction | Real Hopf frame; sufficient clean reservation $`a\ge C(n+h)`$ for a sufficiently large fixed $`C`$; literal-phase, complete-input error |
| **C. Two-clean compilation** | $`T=O(N+nL)`$, $`G=O(NL)`$ | Real Hopf frame; $`a=2`$, $`b\ge L+n+7`$; complete-input error including operator-core return |

Result A is a total elementary gate-size theorem in the arbitrary-one-qubit
and CNOT model. It is not presented as a separately proved optimum for CNOT
count alone. Result B is precision-uniform under its clean reservation;
Result C is a different construction with a constant clean allocation.

Proofs: [A](../docs/COMPILER_THEOREM.md),
[B](../docs/FAULT_TOLERANT_COMPILER.md),
[C](../research/constant_clean/OPERATOR_SOURCE_COMPILER.md).

## Corollaries that stay in the paper

These complete the resource picture without becoming separate storylines.

| Corollary | Statement and placement |
|---|---|
| Dirty-bank refinement | With $`a=2`$, $`b\ge2(L+n+7)`$, Result C sharpens to $`T=O(\sqrt{NL}+nL+NL/b)`$. It matches the existing lower bound if $`n^2L\le N`$ or $`b\le N/n`$, subject to that allocation. State beside C; give bank scheduling in the appendix. |
| Literal diagonal synthesis | For $`\ell\ge6`$, two clean qubits give $`O(N+\ell)`$ T gates at error $`2^{-\ell}`$ with $`b\ge\ell+n+5`$. For $`b\ge2(\ell+n+5)`$, the bound $`O(\sqrt{N\ell}+\ell+N\ell/b)`$ matches the diagonal lower bound. Use as a supporting compiler corollary. |
| Complex magnitude frame | Compile $`D_\phi W_{\mathbb R}`$ using independently supplied phases and real Hopf angles. In the two-clean model, splitting the error gives $`b\ge L+n+8`$ for $`O(N+nL)`$ T gates, or $`b\ge2(L+n+8)`$ for the banked bound. This is not arbitrary complex-unitary synthesis. |
| Smaller clean/dirty allocations | Retain the borrowed-workspace upper bound and its restricted all-clean-budget matching splice as an appendix comparison. The splice requires $`h+b\le c\sqrt N`$ for fixed $`c>0`$; it is not an unrestricted constant-clean theorem. |
| Fixed-parameter QBP robustness | Exact substitution preserves the global record. Approximate synthesis using the actual circuit and its actual adjoint gives raw-coordinate bias at most $`4|a_j|(\eta+\eta_O)`$. Keep this as the operational consequence, with its observable-access and sampling assumptions. |

The exact complex extension and the two-clean complex extension have their
own proofs. Result B's sufficient-clean matching theorem remains stated for
the real frame. Leaf-phase derivatives use a separate measurement stream;
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
the same upper bound. The graph-source attenuation theorem restricts one
returned encoding; it supplies no additive full-frame lower bound.

## Main text, appendices, and retained research

| Location | Contents |
|---|---|
| Main text | One-column obstruction; shared frame contract; Results A–C and their resource-regime table; proof mechanisms; short complex and QBP corollaries; the open endpoint |
| Technical appendices | Full echo, decoder, and router schedules; source preparation; residual composition and failure tracking; amplification and error sums; dirty queries/banks; literal diagonal proof; lower-bound reductions; detailed QBP concentration and accounting |
| Repository research supplement | Graph-source and supplied-source attenuation barriers; dirty-rank compression; modular addition, phase batching, clock, and catalysis investigations; unsuccessful or unresolved routes |

The research supplement remains available and cited when useful. Its full
contents are not part of the selected manuscript. In particular, the
graph-source restriction is optional discussion support, not a fourth main
theorem or a prerequisite for the positive constructions.

## Contribution and evidence boundaries

The new claims concern the complete-operator factorizations, workspace
schedules, precision-uniform residual composition, and two-clean geometric
operator construction that yield these resource guarantees. Hopf geometry
and QBP records are inherited from the earlier Hopf work. UCG synthesis,
dirty lookup, Clifford-algebra loaders, geometric weighting, and oblivious
amplification retain their established attribution in the
[source map](../docs/SOURCE_MAP.md).

The submission is a theoretical construction paper with executable finite
checks. Those checks support fragile identities, conventions, and resource
ledgers; they do not prove universal statements, certify priority, or supply
a general elementary Clifford+T emitter. Hardware connectivity, physical
noise thresholds, optimal T-depth, optimizer convergence, and practical
end-to-end speedups are outside the selected claims.

## When manuscript preparation can proceed

The [internal sanity check](../docs/SANITY_CHECK.md) supports drafting this
scope now. The remaining publication work is to assemble the complete LaTeX
argument, align notation and citations with the earlier Hopf papers, and
obtain external technical feedback on the complete draft. The endpoint can
be pursued separately; the present manuscript does not wait for its solution.
