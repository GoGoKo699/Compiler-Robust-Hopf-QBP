# Claim support map

This page separates exact finite checks, analytic proofs, imported synthesis
theorems, and open targets.

## Evidence classes

| Class | Meaning |
|---|---|
| Exact matrix check | Two independently built finite-dimensional operators are compared numerically |
| Algebraic proof | Dimension-independent identity written in the documentation/manuscript |
| Imported synthesis theorem | Resource deduction uses a published compiler theorem under its stated circuit model |
| Term ledger | Code exposes every contribution but does not prove the asymptotic theorem numerically |
| Open target | No claim of proof |

## Current map

| Statement | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Recursive and addressed real Hopf frames coincide | Algebraic construction plus exact matrix checks | `frames.py`, `test_frames.py` | Through `n=7` numerically; formula is general |
| Real frame is orthogonal and separated complex frame is unitary | Recursive formula plus exact checks | `frames.py`, `test_frames.py` | Exact floating-point tests only supplement the proof |
| Conditioned-prefix identity | Algebraic proof plus exact checks for every cut | `ancilla_depth.py`, `test_ancilla_depth.py` | Through `n=8` numerically |
| Tail times conditioned prefix recovers the complete frame | Exact factorization check | `ancilla_depth.py`, `test_ancilla_depth.py` | Through `n=7` numerically |
| Unary Givens network equals the prefix frame | Algebraic code-subspace identity plus dense checks | `ancilla_depth.py`, `test_ancilla_depth.py` | Dense unary Hilbert space checked through `t=3` |
| Unary layers consist of disjoint pairs | Exact combinatorial check | `unary_layer_pairs`, `test_ancilla_depth.py` | Through `t=8` numerically; definition is general |
| Current clean frame has `O(N)` size and candidate depth bound | Exact bridge, term ledger, imported synthesis theorems | `ancilla_depth.py`, ledger script, companion | Not an exact finite gate-depth implementation |
| Frame uses at most matched `m` plus one reusable tail flag | Explicit workspace ledger | `ancilla_depth.py`, tests | Source-compiler wire reuse still needs human audit |
| Three older Figure 1 upper profiles follow | Analytic regime reduction | companion | Does not close the later all-ancilla gap |
| Record-wise decoder equals empirical FWHT decoder | Exact sample-level checks | `decoders.py`, `test_decoders.py` | Through `n=6` numerically |
| Record-wise decoder costs `O(SN)` | Direct operation count | decoder documentation | Python constants are not benchmarked |
| Optimal all-ancilla Hopf frame depth | Open target | `OPTIMAL_ALL_ANCILLA_TARGET.md` | No claim |
| Generic chart-level theorem | Open target | research discussion only | Current evidence is Hopf-specific |

## Reproduction

```bash
python -m pip install -r requirements.txt
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
python scripts/check_upstream_sync.py --offline
```

GitHub Actions runs the deterministic suite on Python 3.11 and 3.13.
