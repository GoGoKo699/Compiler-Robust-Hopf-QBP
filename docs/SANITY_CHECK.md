# Full sanity check and publication decision

[Publication scope](../manuscript/PUBLICATION_SCOPE.md) · [Verification map](VERIFICATION.md) · [Source map](SOURCE_MAP.md)

Checked on 22 September 2026. The starting snapshot was commit `98cbedf`;
the documentation corrections below accompany this report.

**Decision:** proceed with one full-length compiler paper containing the
exact all-workspace theorem, the sufficient-clean matching T theorem, and
the two-clean construction. Keep the QBP transfer as the application and the
constant-clean endpoint as an open problem. No proof-blocking error was
found in this internal audit; this is not external peer review or a
certification of priority.

## What was inspected

Five separate review passes examined the exact logical/QBP arguments, the
sufficient-clean fault-tolerant proof and lower bounds, the two-clean proof
and graph-reuse restriction, the primary-source comparisons, and the
evidence/reading route. They read the proof chapters and supporting notes,
not only the landing-page claims.

| Area | Audit result |
|---|---|
| Exact logical construction | Four-sector echo, conditioned prefix, coherent routing, clean return, and worst-case lower bounds are consistent. Corrected a saturated-cut inequality in secondary summaries. |
| Sufficient-clean T theorem | Charged source preparation, shared accepted-branch source, failure history, actual inverses, normalization, and workspace split support the stated regime. |
| Two-clean construction | Native source, sign programming, dirty predicate echo, bank allocation, full-output amplification, and complex composition support the stated upper bounds. Clarified approximate operator-core return. |
| QBP consequence | Exact and approximate substitution use the complete interface and actual adjoint; raw-coordinate bias, controlled-observable assumptions, and classical output costs are distinguished. |
| Restricted lower bounds | Source/graph/rank restrictions retain their hypotheses. None closes the unrestricted constant-clean endpoint or proves an unavoidable per-depth precision charge. |
| Literature positioning | Rechecked the principal imported synthesis, lookup, loader, and amplification sources. Added the missing primary OAA citation and integrated the two-clean comparison. The search remains bounded. |
| Reader route | Established theorems, corollaries, proof appendices, and exploratory notes now have an explicit manuscript placement. |

## Corrections made

1. **Saturated tree cut.** The uniform summary bound is
   $`2^s/s=O(1+N/(n+m))`$. The stronger expression without the constant
   applies to the nonsaturated case. At $`s=1`$ and $`m\gg N`$ the
   subtree cost is constant; the final depth frontier is unchanged.
   The allowed cut and decoder domains are now explicit.
2. **Primitive versus elementary depth.** The decoder's $`11t-4`$ count
   is for disjoint X/CNOT/Toffoli layers. Its elementary gate depth is
   $`O(t)`$ after constant-size decompositions. The QBP branch ancilla is
   charged relative to frame workspace, without assuming a particular
   scalar program's ancillary layout.
3. **Dirty return.** Exact return of lookup work is distinguished from
   the two-clean operator core's approximate return in the full-isometry
   norm. The main sufficient-clean construction retains exact dirty return.
4. **Historical endpoint statements.** Older research notes now label
   $`O(N^{3/2})`$ as the earlier benchmark and point to the two-clean
   $`O(N\log N)`$ bound with its explicit dirty allocation.
5. **Attribution and evidence.** Added Berry et al. for standard
   normalization-two amplification, expanded the two-clean source mapping,
   distinguished the unittest suite from the four standalone exact suites,
   and corrected minor summation and provenance wording.

These changes repair the presentation and intermediate specifications; they
do not enlarge the theorem claims or resolve an open problem.

## Executable verification

| Check | Result |
|---|---|
| Full deterministic suite, `python validate.py` | 165 tests passed |
| Final narrative, links, typography, and presentation guards | 28 tests passed, including the new scope and audit pages |
| Edited-document TeX rendering | 2,133 expressions rendered with no MathJax errors; this is not browser layout verification |
| Standalone fault-tolerant receipts, `python scripts/verify_fault_tolerant.py` | All four exact/scientific receipts reproduced |
| Reviewer walkthrough | Passed |
| Unified and strict-zero resource ledgers at $`n=12`$ | Completed successfully |
| Python source compilation | Passed |
| Recorded upstream metadata, offline check | Passed; checks the recorded baseline, not live upstream freshness |

The receipt suites cover geometric-source preparation, the shifted correction
kernel, rational resource accounting, and geometric reflection. They remain
distinct from the general tests. Finite matrices and arithmetic checks do
not replace the dimension-independent proofs.

Reproduce the verification from the repository root:

```bash
python -m compileall -q compiler_robust_hopf scripts tests validate.py
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/verify_fault_tolerant.py
python scripts/unified_resource_ledger.py --n 12 --format json
python scripts/strict_zero_echo_ledger.py --n 12 --format json
python scripts/check_upstream_sync.py --offline
```

The repository's validation workflow also runs on Python 3.11 and 3.13.
The separate presentation workflow checks rendered diagrams and inline math;
its run on the published commit is the current visual gate. Local test
success alone is not described as a rendered-browser check.

## Publication boundary

The [publication scope](../manuscript/PUBLICATION_SCOPE.md) is the governing
statement for manuscript inclusion. It leaves the high-precision point
$`a=2,\ b=N+n+7,\ L=N`$ between $`\Omega(N)`$ and
$`O(N\log N)`$. It excludes unrestricted constant-clean optimality,
arbitrary complex-unitary synthesis, a joint optimum for all gate resources,
and optimality among all gradient algorithms.

The repository is ready to support manuscript drafting and external
technical reading within that scope. A finished manuscript, external review,
and a submission decision remain separate publication steps.
