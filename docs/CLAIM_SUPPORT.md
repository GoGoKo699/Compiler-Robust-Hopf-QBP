# Claim support map

This page separates exact finite checks, algebraic proofs, imported synthesis
theorems, audited deductions, explicit counterexamples, and open targets.

## Evidence classes

| Class | Meaning |
|---|---|
| Exact matrix check | Two independently built finite-dimensional operators are compared numerically |
| Algebraic proof | Dimension-independent identity written in the documentation or manuscript |
| Explicit counterexample | Closed-form finite instance disproving a stronger claim |
| Imported synthesis theorem | Resource deduction uses a published compiler theorem under its stated circuit model |
| Audited deduction | Every logical and asymptotic step has been independently re-derived within this project |
| Term ledger | Code exposes each contribution but does not prove an asymptotic theorem numerically |
| Open target | No claim of proof |

Finite tests supplement but do not replace algebraic and synthesis arguments.

## Compiler contracts and boundaries

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Frame-safe recompilation preserves the complete global protocol distribution | Algebraic reducing-subspace substitution theorem | `FRAME_SAFE_COMPILATION.md` | Requires complete system action on every clean-workspace input |
| State-column equality is insufficient for global Hopf QBP | Explicit two-qubit counterexample | `compiler_boundaries.py`, `test_compiler_boundaries.py`, `COMPILER_BOUNDARIES.md` | SWAP fixes `|00>` but exchanges root and child markers |
| Correct global gradient in the counterexample is `(2,0,0)` | Analytic Hopf derivative calculation and exact decoder | same | Observable is `-Z tensor I`; all angles are `pi/4` |
| State-equivalent compiled decoder returns `(0,sqrt(2),0)` | Exact output distribution and Walsh decoding | same | Original decoder is kept fixed, as required for compiler substitution |
| Checkpoint active-interface equality preserves all designated estimator means | Algebraic adjoint/interface theorem | `FRAME_SAFE_COMPILATION.md`, `COMPILER_BOUNDARIES.md` | Sufficient objective-independent contract; full distribution need not agree |
| Checkpoint state-column equality is insufficient | Explicit two-qubit counterexample | `compiler_boundaries.py`, tests | Final state remains `|++>` while derivative changes from `2` to `-2` |
| Active-interface equality need not preserve checkpoint distributions | Explicit positive example | same | Mean is unchanged; total-variation distance is `1/4` |
| Complete frame safety implies active-interface safety | Direct restriction of the operator contract | compiler-boundary documents | Converse fails because off-interface action is arbitrary |
| Active-interface safety implies state-column equality | Prefix state lies in the active interface | compiler-boundary documents | Converse fails by the checkpoint sign-flip example |

## Real-frame map

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Recursive and addressed real Hopf frames coincide | Algebraic construction plus exact matrix checks | `frames.py`, `test_frames.py` | Through `n=7` numerically; formula is general |
| Real frame is orthogonal | Recursive formula plus exact checks | `frames.py`, `test_frames.py` | Floating-point tests supplement the proof |
| Conditioned-prefix identity | Proved and audited; exact checks for every cut | `ancilla_depth.py`, `test_ancilla_depth.py`, proof audit | Through `n=8` numerically |
| Tail times conditioned prefix recovers complete frame | Exact factorization plus algebraic layer ordering | `ancilla_depth.py`, `test_ancilla_depth.py` | Through `n=7` numerically |
| Unary Givens network equals prefix frame | Proved code-subspace identity plus dense checks | `ancilla_depth.py`, `test_ancilla_depth.py` | Dense unary Hilbert space through `t=3` |
| Unary network has no code leakage | Excitation-number preservation plus exact checks | same | Dense checks through `t=3` |
| Unary layers consist of disjoint pairs | Algebraic indexing plus combinatorial check | `unary_layer_pairs`, tests | Through `t=8` numerically |
| Unary prefix requires at most `3*2**t-t` clean ancillary wires | Audited register ledger using Sun et al. Lemma 28 | `ancilla_depth.py`, proof audit | Conversion theorem imported |
| Isolated unary-prefix size is `O(2**t+n-t)` | Corrected audited deduction | proof audit, size proxy | Earlier `O(2**t)` wording was too strong locally |
| Tail UCG width is `d+2` nonfinal and `n` final | Audited exact register count | `frame_layer_ucg_qubits`, tests | All-to-all logical circuit |
| Real frame uses at most `max(1,m)` clean ancillas | Audited construction | workspace ledger and tests | Same `m` for `m>=1`; one flag at nominal `m=0` |
| Uniform geometric-tail estimate | Proved with explicit constant 6 and tested | `geometric_tail_sum`, upper bound, tests | Width shifts alter constants only |
| Real clean frame has `O(N)` size | Audited deduction from prefix, predicate, and UCG sums | size ledger and proof audit | Exact constants not claimed |
| Real clean frame has depth `O(n(n-t+1)+N/(n+m))` | Audited deduction plus imported Lemmas 12, 28, and 41 | depth ledger and proof audit | Not a finite elementary-depth implementation |
| Three older Figure 1 upper profiles follow for the real frame | Audited regime reduction | robustness document and proof audit | Does not close later optimal-QSP gap |

## Complex-frame and diagonal map

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Separated frame is `W_C=D_ph W_R` and is unitary | Algebraic factorization plus exact checks | `frames.py`, `test_frames.py`, `test_complex_analysis.py` | Exact separated construction |
| Complex frame contains state and phase-dressed magnitude tangents | Algebraic derivative identity plus exact checks | `complex_analysis.py`, tests | Tested through `n=5` |
| Normalized diagonal with `2n<=w<=N/n` has clean depth `O(log w+N/w)` and size `O(N)` | Imported Sun et al. synthesis results | `complex_resources.py`, common-workspace document | Exact synthesis theorem imported |
| Normalized diagonal has no-ancilla depth `O(N/n)` and size `O(N)` | Imported Sun et al. result | same | Exact synthesis theorem imported |
| Arbitrary diagonal has all-budget depth `O(n+N/(n+m))`, size `O(N)`, and at most `m` clean ancillas | Audited piecewise deduction, common-phase gate, and clean reset | `complex_resources.py`, `test_complex_resources.py` | Numeric rows are term proxies |
| Ancillary diagonal registers return to zero | Imported construction cleanup | source theorem and common-workspace proof | Source circuit not reimplemented gate by gate |
| Real and diagonal blocks reuse one clean pool | Algebraic sequential-composition argument | `COMPLEX_COMMON_WORKSPACE.md`, resource rows | Blocks must each be clean full operators |
| Separated complex frame has `O(N)` size and real-frame depth bound | Audited deduction | `complex_resources.py`, common-workspace document | Same `m` for `m>=1`; one flag at nominal `m=0` |
| Every addressed layer is a full-width UCG with zero inactive angles | Algebraic angle table plus exact matrix checks | `test_complex_resources.py` | Wire relabeling in all-to-all model |
| Strict zero-ancilla complex fallback has depth `O(N)` and size `O(nN)` | Audited UCG summation plus no-ancilla diagonal | `complex_resources.py`, tests | Does not retain sharp `O(N)` size |
| Common phase multiplies state and frame by one scalar | Algebraic identity plus exact checks | `complex_analysis.py`, tests | Exact compiler restores the scalar gate |
| Exact phase gradient is zero-sum | Algebraic gauge proof plus exact checks | `phase_gauge_residual`, tests | Hermitian expectation objectives |
| Zero-amplitude leaf has zero phase derivative and gradient | Direct formula plus singular tests | `complex_analysis.py`, tests | No division by amplitude |
| Diagonal parity parameters are generated in `O(Nn)` work | Explicit FWHT formula plus direct reconstruction | `diagonal_parity_angles`, tests | Arithmetic model; finite constants not benchmarked |
| Direct phase sample decoder costs `O(S+N)` | Signed-bin accumulation plus exact distribution parity | `decoders.py`, `test_decoders.py` | Output array has length `N` |
| Phase records have deterministic norm two | Direct record definition plus exhaustive finite checks | `phase_record`, tests | Fixed-norm concentration premise |
| Three older Figure 1 upper profiles follow for separated complex frame | Audited absorption of diagonal depth | common-workspace document | Later optimal-QSP gap remains open |

## End-to-end and open map

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Record-wise magnitude decoder equals empirical FWHT decoder | Exact sample-level checks | `decoders.py`, `test_decoders.py` | Through `n=6` numerically |
| Record-wise magnitude decoder costs `O(SN)` | Direct operation count | decoder documentation | Python constants not benchmarked |
| Checkpoint exact-distribution decoder implements the signed target-prefix score | Direct formula and counterexample parity checks | `decode_checkpoint_gradient`, boundary tests | Lower suffix is summed out |
| Complex magnitude stream uses one inverse complex frame | Protocol factorization | common-workspace document | Controlled observable cost excluded |
| Direct phase stream uses no inverse frame | Protocol factorization | common-workspace document | Forward preparation still required |
| Complete frame reaches `Theta(n+N/(n+m))` for every `m` | Open target | `OPTIMAL_ALL_ANCILLA_TARGET.md` | No claim |
| Sharp `O(N)` size and strict zero extra workspace coexist | Open target | strict fallback gives `O(nN)` size | No impossibility claim |
| Generic chart-level theorem | Open target | research discussion only | Current evidence is Hopf-specific |

## Audit refinements

The real proof audit established

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

The complex audit added the clean all-budget diagonal lemma, common-workspace
composition, exact common-phase treatment, strict zero-ancilla fallback,
phase-parameter FWHT, and direct phase decoder.

The compiler-boundary audit added exact global and checkpoint counterexamples
and separated three contracts: state-column equality, checkpoint
active-interface equality, and complete frame safety.

## Reproduction

```bash
python -m pip install -r requirements.txt
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
python scripts/complex_workspace_ledger.py --n 10
python scripts/check_upstream_sync.py --offline
```

GitHub Actions runs the deterministic suite on Python 3.11 and 3.13.
