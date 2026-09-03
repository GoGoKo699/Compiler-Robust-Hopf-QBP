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
| Exact term ledger | Integer or rational bookkeeping; not asymptotic fitting |
| Internal audit | Independent re-derivation within this project; not external review |
| Prior-art boundary | Conservative technical comparison; not a legal novelty opinion |

## Literature roles

| Source | Active role |
|---|---|
| Yuan--Zhang, *Quantum* 7, 956 (2023) | Sole active external compiler framework; Theorem 2 benchmark; Lemmas 5, 6, and 9 primitives |
| Sun et al., *IEEE TCAD* 42, 3301--3314 (2023) | Historical predecessor and original attribution; not an alternative compiler |
| Möttönen et al. and Bergholm et al. (2005) | Uniformly controlled-gate lineage and earlier `Hopf-QBP` robustness context |
| Barenco et al. (1995), Claudon et al. (2024) | Square-root controlled-unitary and borrowed-ancilla lineage |
| Khattar--Gidney (2024) | Conditionally clean ancillas and toggle-detection lineage |
| Xu et al. (2025) | Restricted/sparse UCG context |

The machine-readable record is [`../provenance/literature.json`](../provenance/literature.json).

## Geometry and operator contracts

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Recursive Hopf state and normalized tangent columns form the real differential frame | Algebraic construction | `frames.py`, `test_frames.py` | Hopf-specific chart |
| Addressed real frame equals recursive real frame | Algebraic layer construction and finite checks | `frames.py`, `test_frames.py` | Formula general; matrices checked finitely |
| Separated complex frame is `D_ph W_R` | Algebraic identity and unitarity checks | `frames.py`, complex tests | Exact separated construction |
| Frame-safe substitution preserves the global distribution | Reducing-subspace proof | `FRAME_SAFE_COMPILATION.md` | Requires full clean-input operator action |
| State-column equality is insufficient for global QBP | Exact two-qubit counterexample | `compiler_boundaries.py`, tests | Original decoder held fixed |
| Checkpoint active-interface equality preserves designated means | Algebraic interface theorem | boundary docs/tests | Full distributions may change |
| Checkpoint state-column equality is insufficient | Exact counterexample | boundary implementation/tests | Factorization-specific |

## Strict-zero addressed layers

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Four-toggle half-angle echo equals one addressed nonfinal layer | Four-sector algebraic proof | `strict_zero_echo.py`, every nonfinal depth through `n=8` | Exact Hopf `R_y` convention |
| Borrowed suffix qubit is restored exactly | Same complete-operator proof | sector tests and full matrices | Qubit may be unknown and entangled |
| No ancillary wire is used | Explicit register audit | source and audit document | Borrowed wire is original system data |
| Half-angle UCG total width is `d+2` | Exact participant count | resource-row tests | `d` prefix controls, borrowed control, target |
| Predicate toggle uses zero ancillary qubits | Imported theorem and negative-control wrappers | resource audit | Yuan--Zhang Lemma 5 |
| Nonfinal layer has size `O(2**d+n-d)` | Two UCGs plus four MCTs and two CNOTs | strict-zero ledger | Exact constants not claimed |
| Nonfinal layer has depth `O(n+2**d/(d+2))` | Yuan--Zhang Lemmas 5 and 6 | strict-zero ledger | All-to-all standard circuit |
| Complete strict-zero real frame has size `Theta(N)` | Geometric size sum plus parameter lower bound | strict-zero audit tests | Internal theorem audit |
| Complete strict-zero real frame has depth `Theta(n+N/n)` | Dyadic-harmonic upper bound and exact-wire parameter lower bound | exact-rational audit tests | Internal theorem audit |
| Inverse has the same resources | Adjoint of exact unitary circuit | inverse matrix tests | Exact circuit model |

## Positive-workspace Hopf tree structure

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| First `t` depths are a `t`-qubit frame conditioned on zero external suffix | Complete-operator proof | `tree_structure.py`, unified tests | Every cut checked through `n=8` |
| Tail below a cut is a direct sum of subtree frames | Algebraic proof and exact angle map | tree structure/tests | Every cut checked through `n=8` |
| Prefix and tail reconstruct the frame | Exact factorization | unified tests | Complete matrix equality |

## Binary--one-hot decoder

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Decoder maps `|x>|0>` to `|0>|e_x>|0>` | Explicit reversible construction | `tree_decoder.py`, tests | Clean input subspace; inverse exact on code |
| Decoder is a full basis permutation | X/CNOT/Toffoli schedule | arbitrary-register reversal tests | Fixed-width gate decomposition |
| Workspace is `3*2**t-2-t` | Exact register count | closed-form tests | Clean ancillary count |
| Depth is `11t-4=O(t)` | Explicit disjoint layer schedule | support-disjointness tests | Fixed-width Toffoli constant cost |
| Size is `O(2**t)` | Exact high-level count | generated schedule versus formula | Constant factors suppressed |
| One-hot Givens network equals complete prefix frame | Mode-pair proof and matrices | code-action tests | One-excitation code |
| Conditioned prefix has depth `O(n)` and size `O(2**t+n-t)` | Decoder, predicate, fanout, controlled Givens | resource row and identity tests | Decoder scratch reused sequentially |

## Positive-workspace unified compiler

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Direct nonfinal layer is suffix flag plus one UCG | Explicit construction | `direct_frame_resource_row` | Yuan--Zhang Lemmas 5 and 6 |
| Direct schedule has size `O(N)` | Geometric UCG-size sum | unified ledger | Positive workspace |
| For `1<=m<4n`, direct depth is optimal order | Polynomial absorption | exact integer regression | Positive workspace |
| Router acts coherently on entangled inputs | Controlled permutation proof | small routed matrices | All-to-all logical model |
| Copied-control count is `(B-1)(s+1)-t` | Combinatorial count | workspace tests | `B=2**t`, `s=n-t` |
| Prefix and routed tail fit in `2B(s+1)` workspace | Exact peak ledger | broad-grid tests | Nontrivial cuts |
| Controlled subtree frame has size `O(2**s)` and depth `O(s**2+2**s/s)` | UCG/MCT sum | controlled resource row | Imported exact primitives |
| All subtree frames run in parallel | Disjoint branch registers | construction/tests | Requires allocated branch registers |
| Maximal feasible cut gives optimal depth | Algebraic cut inequality | exact diagnostics | Routed regime |
| Positive-workspace real frame is optimal | Unified upper and lower bounds | compiler/ledger/tests | Internal proof audit |

## All-workspace theorem

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Unified compiler selects echo at `m=0` | Explicit dispatch | `unified_compiler.py`, cross-check tests | Top-level real frame only |
| Unified compiler respects every requested `m>=0` | Workspace ledger | broad-grid tests | Clean workspace model |
| Real frame has `Theta(N)` size for every `m>=0` | Strict-zero and positive theorems | unified and dedicated ledgers | Internal proof audit |
| Real frame has `Theta(n+N/(n+m))` depth for every `m>=0` | Schedule union and lower bounds | exact term diagnostics | Internal proof audit |

## Complex frame

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Arbitrary phase diagonal is one `n`-qubit UCG | Direct block identity | `diagonal_ucg_matrix`, tests | One target, `n-1` controls |
| Diagonal size/depth match the QSP scale for every `m>=0` | Yuan--Zhang Lemma 6 | resource row | Exact standard circuit |
| Common phase is retained exactly | Arbitrary `U(2)` blocks | complete-matrix tests | No gauge repair needed |
| Block table generation is `O(N)` | Direct phase pairing | implementation | Host decomposition time not benchmarked |
| Real and diagonal blocks reuse one workspace pool | Sequential clean composition | complex resource row | Both blocks return workspace |
| Complex frame has the all-workspace optimum | Real theorem plus phase UCG | complex tests/ledger | Internal audited corollary |

## Backpropagation and classical work

| Claim | Evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Magnitude sampling is compiler-independent under frame safety | Substitution theorem | contract proof | Same frame and measurement convention |
| Fixed-accuracy magnitude executions are `O(log n)` | Norm-two records and vector concentration | established `Hopf-QBP` result | Controlled-observable model |
| Record-wise magnitude decoder costs `O(SN)` | Direct character generation | decoder/FWHT parity tests | Output length `Theta(N)` |
| Histogram plus FWHT costs `O(S+Nn)` | Standard FWHT count | decoder tests | Alternative route |
| Direct phase decoder costs `O(S+N)` | Signed-bin accumulation | exact sample tests | One gauge redundancy |
| Compiler-robust QBP overhead is `O(log n)=O(log log M)` for every `m>=0` | Optimal per-execution frame depth and sample count | `END_TO_END_QBP.md` | Controlled `O` charged comparably |

## Prior-art boundary

| Statement | Status |
|---|---|
| Square-root/conjugation controlled-unitary techniques predate this project | Established lineage |
| Borrowed/dirty-bit toggle detection predates this project | Established lineage |
| Standard UCG synthesis is imported | Established lineage |
| Same Hopf-specific two-UCG borrowed-suffix reduction found in current search | Not found, but search not conclusive |
| Novelty claim to use | Hopf-specific aggregation and optimal complete-frame consequence |

See [`STRICT_ZERO_PRIOR_ART.md`](STRICT_ZERO_PRIOR_ART.md).

## Active files

```text
compiler_robust_hopf/frames.py
compiler_robust_hopf/tree_structure.py
compiler_robust_hopf/tree_decoder.py
compiler_robust_hopf/strict_zero_echo.py
compiler_robust_hopf/strict_zero_audit.py
compiler_robust_hopf/unified_compiler.py
compiler_robust_hopf/resource_bounds.py
compiler_robust_hopf/decoders.py
compiler_robust_hopf/compiler_boundaries.py

docs/THEOREM_OVERVIEW.md
docs/UNIFIED_YUAN_ZHANG_COMPILER.md
docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md
docs/STRICT_ZERO_ECHO_AUDIT.md
docs/STRICT_ZERO_PRIOR_ART.md
docs/FRAME_SAFE_COMPILATION.md
docs/COMPILER_BOUNDARIES.md
docs/END_TO_END_QBP.md
docs/RELATED_WORK.md
```

## Reproduction

```bash
python -m pip install -r requirements.txt
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```
