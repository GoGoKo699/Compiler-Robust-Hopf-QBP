# Claim support map

This page maps every material claim to its proof type, executable support, and
boundary. Finite tests supplement but do not replace dimension-independent
arguments.

## Evidence classes

| Class | Meaning |
|---|---|
| Algebraic proof | Dimension-independent identity proved in project documentation |
| Explicit construction | Register and gate schedule supplied in the repository |
| Imported theorem | Exact circuit result used under the hypotheses of its source |
| Exact finite check | Independently built operators or records compared numerically |
| Explicit counterexample | Closed-form finite instance disproving a stronger claim |
| Term ledger | Integer bookkeeping and regression diagnostics, not asymptotic fitting |
| Open boundary | No proof claim |

## Literature roles

| Source | Active role |
|---|---|
| Yuan--Zhang, *Quantum* 7, 956 (2023) | Sole active external compiler framework; Theorem 2 benchmark; Lemmas 5, 6, and 9 primitives |
| Sun et al., *IEEE TCAD* 42, 3301--3314 (2023) | Historical predecessor and original attribution credited by Yuan--Zhang; not an active alternative compiler |
| Möttönen et al. and Bergholm et al. (2005) | Historical uniformly controlled state-preparation lineage and earlier `Hopf-QBP` robustness context |

The machine-readable record is [`../provenance/literature.json`](../provenance/literature.json).

## Geometry and operator contracts

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Recursive balanced Hopf state and normalized tangent columns form the real differential frame | Algebraic construction | `frames.py`, `test_frames.py` | Hopf-specific chart |
| Addressed real frame equals recursive real frame | Algebraic layer construction plus exact finite checks | `frames.py`, `test_frames.py` | Checked through finite `n`; formula general |
| Separated complex frame is `D_ph W_R` | Algebraic identity plus unitarity checks | `frames.py`, complex tests | Exact separated construction |
| Frame-safe substitution preserves the complete global distribution | Algebraic reducing-subspace theorem | `FRAME_SAFE_COMPILATION.md` | Requires full operator action on clean workspace inputs |
| State-column equality is insufficient for global Hopf QBP | Explicit two-qubit counterexample | `compiler_boundaries.py`, `test_compiler_boundaries.py` | Original decoder held fixed |
| Checkpoint active-interface equality preserves designated means | Algebraic interface theorem | `FRAME_SAFE_COMPILATION.md`, `COMPILER_BOUNDARIES.md` | Full distributions may change |
| Checkpoint state-column equality is insufficient | Explicit two-qubit counterexample | boundary implementation/tests | Factorization-specific result |

## Exact Hopf tree structure

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| First `t` depths equal a `t`-qubit frame conditioned on a zero external suffix | Algebraic operator proof | `tree_structure.py`, `test_unified_compiler.py` | Every cut checked through `n=8` |
| Tail below a cut is a direct sum of subtree frames | Algebraic operator proof and exact angle map | `tree_structure.py`, unified tests | Every cut checked through `n=8` |
| Prefix and tail reconstruct the complete frame | Exact factorization | `reconstructed_frame`, unified tests | Complete matrix equality |

## Self-contained tree decoder

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Decoder maps `|x>|0>` to `|0>|e_x>|0>` | Explicit reversible construction and basis proof | `tree_decoder.py`, `test_tree_decoder.py` | Clean input subspace; inverse exact on one-hot code |
| Decoder is a full basis permutation | X/CNOT/Toffoli circuit | arbitrary-register reversal tests | Fixed-width gates compiled in standard model |
| Workspace is `3*2**t-2-t` | Exact register count | closed-form tests through `t=40` | Clean ancillary count |
| High-level depth is `11t-4=O(t)` | Explicit disjoint layer schedule | every returned layer checked for disjoint support | Fixed-width Toffoli has constant standard-circuit cost |
| High-level size is `11*2**t-10-5t=O(2**t)` | Exact gate count | generated schedule versus formula | Constant decomposition factors suppressed |
| One-hot Givens network equals the complete `t`-qubit Hopf frame | Algebraic mode-pair map plus exact matrices | `unary_hopf_code_action`, tests through `t=8` | One-excitation code |
| Conditioned prefix has depth `O(n)` and size `O(2**t+n-t)` | Decoder, suffix predicate, coherent fanout, controlled disjoint Givens | resource row and operator identity tests | Uses decoder scratch sequentially |

## Unified real compiler

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Direct nonfinal layer is suffix predicate plus one UCG | Explicit construction | `direct_frame_resource_row` | Yuan--Zhang Lemmas 5 and 6 |
| Direct small-workspace schedule has size `O(N)` | Geometric UCG-size sum | unified ledger | Exact constants not claimed |
| For `1<=m<4n`, direct depth is `O(N/(n+m))` | Algebraic absorption of `n**2` | broad integer regression | Positive workspace only |
| Router acts coherently on arbitrary prefix--suffix entanglement | Controlled basis-permutation proof | retained router tests | All-to-all logical model |
| Exact copied-control count is `(B-1)(s+1)-t` | Combinatorial count | workspace tests | `B=2**t`, `s=n-t` |
| Prefix and routed tail fit in `2B(s+1)` workspace | Exact data/token/copy/flag and decoder ledger | `route_workspace_row`, broad-grid tests | Nontrivial cuts `1<=t<n` |
| One controlled subtree frame has size `O(2**s)` and depth `O(s**2+2**s/s)` | Width-by-width UCG/MCT sum | direct controlled resource row | Yuan--Zhang Lemmas 5 and 6 |
| All subtree frames run in parallel | Disjoint branch registers | construction and small routed checks | Requires allocated branch registers |
| Maximal feasible cut gives depth `O(n+N/(n+m))` | Algebraic cut inequality | term diagnostics | `m>=4n`; direct schedule covers smaller positive `m` |
| Complete real frame has size `O(N)` and optimal depth for every `m>=1` | Unified upper bound | `unified_compiler.py`, ledger/tests | Internal proof audit; external review open |
| Real-frame size lower bound is `Omega(N)` | Real-state manifold parameter count | proof audit | Exact universal real family |
| Real-frame depth lower bound is `Omega(n+N/(n+m))` | Layer parameter count and backward light cone | proof audit | Standard circuit model |

## Complex frame

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Arbitrary leaf-phase diagonal is exactly one `n`-qubit UCG | Direct block-diagonal identity | `diagonal_ucg_matrix`, tests through `n=9` | Choose one target and `n-1` controls |
| Diagonal size is `O(N)` and depth is `O(n+N/(n+m))` | Yuan--Zhang Lemma 6 | `diagonal_ucg_resource_row` | Exact standard circuit |
| Common phase is retained exactly | Arbitrary `U(2)` blocks | complete-matrix tests | No phase-polynomial gauge repair required |
| Phase block table takes `O(N)` generation work | Direct pairing of leaf phases | implementation | Host time of elementary UCG synthesis not benchmarked |
| Real and diagonal blocks reuse one clean workspace pool | Sequential clean composition | `unified_complex_frame_resource_row` | Both blocks must return workspace zero |
| Separated complex frame has `Theta(N)` size and optimal depth for every `m>=1` | Real theorem plus one-UCG diagonal | complex resource row and composition tests | External review open |

## Backpropagation and classical work

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Global magnitude sampling is compiler-independent under frame safety | Frame-safe substitution | contract theorem | Same logical frame and measurement convention |
| Fixed-accuracy magnitude executions are `O(log n)` | Norm-two depth records and vector concentration | established `Hopf-QBP` result | Controlled-observable model unchanged |
| Record-wise magnitude decoder costs `O(SN)` | Direct character generation | `decoders.py`, exact FWHT parity tests | Output length `Theta(N)` |
| Histogram plus FWHT costs `O(S+Nn)` | Standard FWHT operation count | decoder tests | Alternative implementation |
| Direct phase decoder costs `O(S+N)` | Signed-bin accumulation | exact sample tests | One gauge redundancy |
| Complete compiler-robust QBP overhead is `O(log n)=O(log log M)` at fixed accuracy | Optimal per-execution frame depth plus magnitude execution count | `END_TO_END_QBP.md` | Controlled `O` charged comparably to scalar evaluation |

## Strict zero-workspace boundary

| Statement | Status | Evidence |
|---|---|---|
| Strict `m=0` exact frame with size `O(nN)` and depth `O(N)` | Proved relative to Lemma 6 | Full-width UCG per addressed depth |
| One clean qubit gives size `O(N)` and depth `O(n+N/n)` | Positive-workspace theorem at `m=1` | Unified compiler |
| Strict `m=0` with simultaneous `O(N)` size and `O(n+N/n)` depth | Open boundary | No construction or impossibility proof |

## Active files

```text
compiler_robust_hopf/frames.py
compiler_robust_hopf/tree_structure.py
compiler_robust_hopf/tree_decoder.py
compiler_robust_hopf/unified_compiler.py
compiler_robust_hopf/decoders.py
compiler_robust_hopf/compiler_boundaries.py

docs/THEOREM_OVERVIEW.md
docs/FRAME_SAFE_COMPILATION.md
docs/UNIFIED_YUAN_ZHANG_COMPILER.md
docs/COMPILER_BOUNDARIES.md
docs/END_TO_END_QBP.md
docs/RELATED_WORK.md
```

## Reproduction

```bash
python -m pip install -r requirements.txt
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```

The resource ledger exposes integer contributions and regime choices. The proof
does not infer asymptotics by fitting numerical slopes.
