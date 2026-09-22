# Manuscript architecture

[Read the argument](../REVIEW.md) · [Exact theorem](../docs/COMPILER_THEOREM.md) · [T-count theorem](../docs/FAULT_TOLERANT_COMPILER.md)

This is one compiler paper about a prescribed Hopf differential frame, with
exact logical and fault-tolerant resource theorems. The same complete-input
contract connects both to the inverse-frame gradient protocol.

## Working title

**Exact and Fault-Tolerant Compilation of Hopf Differential Frames**

Quantum backpropagation motivates the required completion and supplies the
application. The compiler theorem remains meaningful independently of that
application. Keep the title Hopf-specific unless a broader frame theorem is
proved.

## Central question and results

A state-preparation circuit can choose all columns except its prepared state.
The prescribed Hopf frame fixes the marker columns used to resolve coordinate
responses. What resources are needed to retain that stronger interface?

| Result | Model and domain |
|---|---|
| Optimal size and depth | exact arbitrary one-qubit gates and CNOTs; every clean-workspace budget; real and phase-dressed complex magnitude frames |
| Matched T-count | coherent finite precision; real full frame; separate clean/dirty promises; sufficient clean reservation |
| Constant-clean improvement | two clean qubits; real frames with $`b\ge L+n+7`$ or phase-dressed complex magnitude frames with $`b\ge L+n+8`$; $`T=O(N+nL)`$ with a sharper bank tradeoff, leaving a logarithmic endpoint gap |
| QBP consequence | fixed-parameter raw-gradient records with matched access assumptions and an explicit approximation-bias budget |

For every integer $m\geq0$, the exact theorem has $S=\Theta(N)$ and
$D=\Theta(n+N/(n+m))$. The real-frame T theorem has the sufficient clean
condition $a\geq C(n+h)$, with the definitions and full quantifiers in its
formal chapter. A separate [operator-source construction](../research/constant_clean/OPERATOR_SOURCE_COMPILER.md) gives the stated constant-clean upper bound, its matching lower-precision subregimes, and the phase-dressed complex magnitude extension. The high-precision endpoint still has a logarithmic gap.

These statements do not assert a single jointly optimal circuit or optimal
complexity among all gradient algorithms.

## Preferred paper structure

1. **Problem and significance.** One prepared column versus a prescribed
   differential frame; the two-qubit readout obstruction; the two resource
   models and the scope of the main results.
2. **Shared mathematical interface.** Hopf tree and markers, oriented incoming
   weights, singular coordinates, full-input compilation, actual adjoints, and
   the separate complex leaf-phase stream.
3. **Exact logical compilation.** Borrowed-suffix echo, small clean flag,
   conditioned tree cut and coherent routing, with the all-workspace size/depth
   theorem and lower bounds.
4. **Fault-tolerant compilation.** Coarse structured residual, compact source,
   accepted-branch reuse, global amplification, full resource ledger and
   matching theorem in the stated regime; then the operator-source construction
   and its two-clean improvement, dirty-bank tradeoff, and literal complex
   magnitude extension, using the same full-input contract.
5. **Compiler-robust QBP.** Exact substitution and finite-precision bounded-score
   bias; quantum executions, per-execution circuit costs, classical output, and
   observable access kept separate.
6. **Discussion.** The remaining logarithmic constant-clean gap, T-depth, elementary emission,
   and scope of the mathematical model.

The main text should explain why the source can be reused, why failed branches
cannot re-enter the accepted block, and where every workspace region is
charged. Detailed reversible arithmetic, exact small fixtures, and repeated
register ledgers can go in appendices.

## Source and contribution discipline

The exact toolkit follows P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023),
with the established multiplexor and borrowed-workspace lineage. Its local
contribution is the Hopf complete-operator factorization and workspace schedule.

The finite-precision toolkit credits Gosset–Kothari–Wu for optimal synthesis
benchmarks, Low–Kliuchnikov–Schaeffer for dirty lookup/counting, and Bausch for
geometric digit weighting and the bit-indexed oracle. Ordinary LCU, compression,
and oblivious amplification retain their original lineage. The main technical
candidate is the precision-uniform full-frame composition with a charged,
reusable source. See the [source map](../docs/SOURCE_MAP.md).

The supporting source-channel obstruction is not needed to prove the positive
T theorem. Keep its role focused on the [open endpoint](../research/CONSTANT_CLEAN_ENDPOINT.md);
it must not become a claimed general frame lower bound. Most failed routes and
the research chronology belong outside the main narrative.

Alternative shadow-based gradient estimators, learned scores, and classical
validation algorithms are outside this compiler paper's selected scope. They
can inform comparisons without becoming a third central storyline.

## Accuracy and geometry

The primary gradient target is simultaneous absolute error for the raw
Hopf-coordinate gradient. Relative, normalized-frame, natural-gradient, and
complete-vector targets have different conditioning. An oriented incoming
amplitude multiplies the corresponding marker; at zero magnitude weight the
raw derivative vanishes but the chart-selected continuation remains prescribed.

Approximate compilation is evaluated at a fixed parameter tuple. The proof
controls measurement-score bias using the actual synthesized circuit and its
actual inverse. It does not differentiate a potentially discontinuous compiler.
The complex magnitude frame and its separate phase stream retain their own
resource statements.

## Remaining work

The repository now carries the integrated proof and evidence reading route.
The constant-clean continuation now improves the endpoint upper bound to
$`O(N\log N)`$ at the explicit two-clean allocation. The
[research brief](../research/CONSTANT_CLEAN_ENDPOINT.md) records the remaining
question: share the precision cost across depths or prove a stronger general
lower bound. The [progress report](../research/CONSTANT_CLEAN_PROGRESS.md) gives
the current reading route.

For a submission package, prepare the full LaTeX manuscript, align notation
with the earlier Hopf papers, check all imported theorem hypotheses, and obtain
external technical feedback. Existing internal checks are not external review
or a certification of priority. Update `CITATION.cff` when a manuscript
identifier is available.
