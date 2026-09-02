# Claim support map

This page separates exact finite checks, analytic proofs, imported synthesis
theorems, audited deductions, and open targets.

## Evidence classes

| Class | Meaning |
|---|---|
| Exact matrix check | Two independently built finite-dimensional operators are compared numerically |
| Algebraic proof | Dimension-independent identity written in the documentation or manuscript |
| Imported synthesis theorem | Resource deduction uses a published compiler theorem under its stated circuit model |
| Audited deduction | Every logical and asymptotic step has been independently re-derived within this project |
| Term ledger | Code exposes each contribution but does not prove an asymptotic theorem numerically |
| Open target | No claim of proof |

Finite tests supplement but do not replace algebraic and synthesis arguments.

## Current map

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Recursive and addressed real Hopf frames coincide | Algebraic construction plus exact matrix checks | `frames.py`, `test_frames.py` | Through `n=7` numerically; formula is general |
| Real frame is orthogonal and separated complex frame is unitary | Recursive formula plus exact checks | `frames.py`, `test_frames.py` | Floating-point tests supplement the proof |
| Conditioned-prefix identity | Proved and audited; exact checks for every cut | `ancilla_depth.py`, `test_ancilla_depth.py`, proof audit | Through `n=8` numerically |
| Tail times conditioned prefix recovers the complete frame | Exact factorization plus algebraic layer ordering | `ancilla_depth.py`, `test_ancilla_depth.py` | Through `n=7` numerically |
| Unary Givens network equals the prefix frame | Proved code-subspace identity plus dense checks | `ancilla_depth.py`, `test_ancilla_depth.py` | Dense unary Hilbert space through `t=3` |
| Unary network has no code leakage | Proved by excitation-number preservation plus exact checks | same | Dense checks through `t=3` |
| Unary layers consist of disjoint pairs | Algebraic indexing plus combinatorial check | `unary_layer_pairs`, `test_ancilla_depth.py` | Through `t=8` numerically |
| Frame-safe recompilation preserves the complete global protocol distribution | Algebraic reducing-subspace substitution theorem | `FRAME_SAFE_COMPILATION.md` | Requires complete system action on clean workspace |
| Unary prefix requires at most `3*2**t-t` clean ancillary wires | Audited register ledger using Sun et al. Lemma 28 | `ancilla_depth.py`, proof audit | Conversion theorem imported |
| Isolated unary-prefix size is `O(2**t+n-t)` | Corrected audited deduction | proof audit, size proxy | Earlier `O(2**t)` wording was too strong locally |
| Tail UCG width is `d+2` nonfinal and `n` final | Audited exact register count | `frame_layer_ucg_qubits`, tests | All-to-all logical circuit |
| Real frame uses at most `max(1,m)` clean ancillas | Audited construction | `frame_ancilla_upper_bound`, UCG-work ledger, tests | Same `m` for `m>=1`; one flag for `m=0` |
| Uniform geometric-tail estimate | Proved with explicit constant 6 and tested | `geometric_tail_sum`, `geometric_tail_upper_bound`, tests | Base inequality; width shifts change constants only |
| Real clean frame has `O(N)` size | Audited deduction from prefix, predicate, and UCG sums | size term ledger and proof audit | Exact constants not claimed |
| Real clean frame has depth `O(n(n-t+1)+N/(n+m))` | Audited deduction plus imported Lemmas 12, 28, and 41 | depth ledger and proof audit | Not a finite elementary-depth implementation |
| Three older Figure 1 upper profiles follow | Audited regime reduction | robustness document and proof audit | Does not close later optimal-QSP gap |
| Record-wise decoder equals empirical FWHT decoder | Exact sample-level checks | `decoders.py`, `test_decoders.py` | Through `n=6` numerically |
| Record-wise decoder costs `O(SN)` | Direct operation count | decoder documentation | Python constants not benchmarked |
| Separated complex frame shares the same complete resource profile | Theorem candidate | `W_C=D_ph W_R`; diagonal bounds | One common-workspace audit still open |
| Optimal all-ancilla Hopf frame depth | Open target | `OPTIMAL_ALL_ANCILLA_TARGET.md` | No claim |
| Generic chart-level theorem | Open target | research discussion only | Current evidence is Hopf-specific |
| Arbitrary checkpoint recompilation | Not claimed | Issue #4 | Needs interface condition or counterexample |

## Audit corrections

The first proof audit made two substantive refinements without changing the
depth exponent or complete-frame size:

```math
S_{\mathrm{prefix}}
=
O(2^t+n-t)
```

and

```math
a_{\mathrm{frame}}(m)
=
\max\{1,m\}.
```

The full classification and proofs are in
[`PROOF_AUDIT_ISSUE_1.md`](PROOF_AUDIT_ISSUE_1.md).

## Reproduction

```bash
python -m pip install -r requirements.txt
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
python scripts/check_upstream_sync.py --offline
```

GitHub Actions runs the deterministic suite on Python 3.11 and 3.13.
