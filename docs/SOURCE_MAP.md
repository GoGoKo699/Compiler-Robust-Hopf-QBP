# Source and dependency map

[← Verification](VERIFICATION.md) · [Complete narrative](../REVIEW.md) · [Related work →](RELATED_WORK.md)

This page separates the proof into three layers:

1. an exact state-preparation compiler toolkit imported from the literature;
2. a compact Hopf frame and QBP interface inherited from the earlier Hopf work;
3. complete-operator factorizations, schedules, and bounds proved in this
   repository.

The tables identify the precise fact used, rather than citing an entire paper as
a premise.

## 1. Imported state-preparation toolkit

The normative compiler citation is:

> P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits,” *Quantum* **7**, 956 (2023),
> doi:10.22331/q-2023-03-20-956.

The published article corresponds to `arXiv:2202.11302v2`.  The imported
statements below were also checked in `arXiv:2202.11302v3`; their conclusions and
exact arbitrary-one-qubit+CNOT model are unchanged for the uses made here.

| ID | Imported result | Exact use in this repository | Local consumer |
|---|---|---|---|
| C1 | Theorem 2: exact arbitrary state preparation has $\Theta(2^n)$ size and $\Theta\!\left(n+\frac{2^n}{n+m}\right)$ depth for every clean-workspace budget | comparison frontier and target lower-bound scale | [compiler theorem](COMPILER_THEOREM.md), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| C2 | Lemma 5: exact ancilla-free multi-controlled X has linear size and depth | strict-zero toggles, direct suffix flags, and branch predicates | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`router.py`](../compiler_robust_hopf/router.py) |
| C3 | Lemma 6: a total-width-$q$ UCG with $w$ clean work qubits has $O(2^q)$ size and $O\!\left(q+\frac{2^q}{q+w}\right)$ depth | half-angle UCGs, flagged layers, subtree frames, and the phase diagonal | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| C4 | Lemma 9: coherent CNOT-tree copying and exact uncopying | control fanout in the conditioned prefix and coherent router | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py), [`router.py`](../compiler_robust_hopf/router.py) |
| C5 | Theorem 1: generic controlled state preparation depends on combined index and target width | comparison showing why a generic all-column construction would have quadratic Hilbert-space scale | [`resource_bounds.py`](../compiler_robust_hopf/resource_bounds.py), [related work](RELATED_WORK.md) |

The preceding state-preparation paper by Sun, Tian, Yang, Yuan, and Zhang is
retained as the historical source of the earlier time–space landscape and of
selected primitives credited by the later article.  The active proof uses the
uniform all-workspace framework above rather than selecting between the two
papers by regime.

## 2. Inherited Hopf operator interface

The compiler construction does not depend on the complete optimization
framework.  It consumes the following facts.

| ID | Inherited fact | Source role | Local restatement or implementation |
|---|---|---|---|
| H1 | a balanced complete binary tree with $N=2^n$ leaves gives $N-1$ real magnitude coordinates | chart definition | [Hopf interface](HOPF_INTERFACE.md), [`frames.py`](../compiler_robust_hopf/frames.py) |
| H2 | the sine–cosine path map covers normalized real states; leaf phases give the complex chart | forward state map | [`real_tree_data`](../compiler_robust_hopf/frames.py), [`complex_state`](../compiler_robust_hopf/complex_analysis.py) |
| H3 | real nonfinal angles use $[0,\pi/2]$, the final real depth uses $[0,2\pi)$, and complex magnitudes use $[0,\pi/2]$ | canonical chart domains | [`canonical_magnitude_angle_mask`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) |
| H4 | the oriented incoming amplitude obeys $\partial_{\theta_j}\lvert\psi\rangle=a_j\lvert e_j\rangle$ and $g_{j,j}=a_j^2$ | differential geometry | [`RealTreeData.incoming_amplitude`](../compiler_robust_hopf/frames.py), [`test_complex_analysis.py`](../tests/test_complex_analysis.py) |
| H5 | on the canonical domains $a_j\geq0$, so $a_j=\sqrt{g_{j,j}}$ | canonical-domain consequence | [`test_frames.py`](../tests/test_frames.py) |
| H6 | if $g_{j,j}=0$, the raw differential vanishes while the parameter tuple still selects a unit marker-frame continuation | singular-coordinate boundary | [`regular_coordinate_mask`](../compiler_robust_hopf/frames.py), singular tests in [`test_frames.py`](../tests/test_frames.py) |
| H7 | the marker $\lambda(j)$ places the state and coordinate-frame directions in one known computational basis | differential-frame interface | [`conventions.py`](../compiler_robust_hopf/conventions.py), [`frames.py`](../compiler_robust_hopf/frames.py) |
| H8 | the complete real frame is a product of prefix-selected rotations restricted to the zero-suffix sector | addressed-frame structure | [Hopf interface](HOPF_INTERFACE.md), [`direct_addressed_depth_layer`](../compiler_robust_hopf/frames.py) |
| H9 | the phase-dressed complex magnitude frame is $W_{\mathbb C,\mathrm{mag}}=D_{\mathrm{ph}}W_{\mathbb R}$ | complex magnitude interface | [`complex_magnitude_frame_matrix`](../compiler_robust_hopf/frames.py) |

The complete inverse map and optimization context are contained in the first
Hopf paper and repository.  The addressed frame, global magnitude record,
direct phase record, checkpoint interface, and statistical task boundaries are
contained in `Hopf-QBP`.

## 3. Inherited QBP interface

The tracked `Hopf-QBP/main` baseline is

```text
faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582
```

and is reconciled in [`SYNC.md`](../SYNC.md) and
[`provenance/upstream.json`](../provenance/upstream.json).

| ID | QBP fact used here | Role in the compiler consequence | Local counterpart |
|---|---|---|---|
| Q1 | the global magnitude circuit applies the complete inverse differential frame | fixes the required compiler contract | [frame-safe compilation](FRAME_SAFE_COMPILATION.md) |
| Q2 | one X-basis outcome contributes a parity record to every magnitude coordinate | shared-record mechanism | [`decoders.py`](../compiler_robust_hopf/decoders.py), [`test_decoders.py`](../tests/test_decoders.py) |
| Q3 | leaf-phase derivatives use a separate signed one-hot stream | separates the complex magnitude frame from the phase record | [`decoders.py`](../compiler_robust_hopf/decoders.py), [`complex_analysis.py`](../compiler_robust_hopf/complex_analysis.py) |
| Q4 | the primary finite-shot target is simultaneous absolute accuracy of the raw coordinate gradient | defines the $O(\log n)$ execution statement | [QBP consequence, Section 5](QBP_CONSEQUENCE.md#5-statistical-target) |
| Q5 | complete-vector, relative, normalized-frame, and natural-gradient targets have different conditioning | prevents overextension of the raw-coordinate claim | [QBP consequence, Section 5](QBP_CONSEQUENCE.md#5-statistical-target) |
| Q6 | the validated core assumes phase-calibrated controlled access to a Hermitian unitary observable | access-model premise | [QBP consequence, Section 2](QBP_CONSEQUENCE.md#2-controlled-observable-interface) |
| Q7 | a checkpoint compiler needs equality on its active interface, not merely one state column | separate checkpoint boundary | [compiler boundaries](COMPILER_BOUNDARIES.md) |

## 4. Results established in this repository

| ID | Result | Analytic proof | Implementation and finite evidence |
|---|---|---|---|
| R1 | complete frame safety implies exact inverse-frame substitution | [frame-safe compilation](FRAME_SAFE_COMPILATION.md) | boundary fixtures in [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) |
| R2 | one correct state column need not preserve the decoded gradient | [two-qubit argument](../REVIEW.md#12-a-complete-two-qubit-obstruction) | [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py) |
| R3 | the borrowed-suffix echo implements one nonfinal addressed layer with no ancillary wire | [compiler theorem, Lemma Z](COMPILER_THEOREM.md#lemma-z-borrowed-suffix-echo) | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`test_strict_zero_echo.py`](../tests/test_strict_zero_echo.py) |
| R4 | the strict-zero frame has $\Theta(N)$ size and $\Theta(n+N/n)$ depth | [compiler theorem, Proposition Z](COMPILER_THEOREM.md#proposition-z-strict-zero-resources) | [`strict_zero_audit.py`](../compiler_robust_hopf/strict_zero_audit.py), exact-rational tests |
| R5 | the prefix is a conditioned smaller frame and the tail is a direct sum of subtree frames | [compiler theorem, Lemmas T1–T2](COMPILER_THEOREM.md#6-exact-tree-cut) | [`tree_structure.py`](../compiler_robust_hopf/tree_structure.py), cut tests |
| R6 | a clean binary–one-hot decoder has $3\cdot2^t-2-t$ workspace, $O(t)$ depth, and $O(2^t)$ size | [compiler theorem, Lemma P](COMPILER_THEOREM.md#lemma-p-clean-binaryone-hot-decoder) | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py), [`test_tree_decoder.py`](../tests/test_tree_decoder.py) |
| R7 | an explicit coherent router realizes the tail direct sum and clears all data, token, copy, and flag work registers | [compiler theorem, Lemma R](COMPILER_THEOREM.md#lemma-r-explicit-coherent-router) | [`router.py`](../compiler_robust_hopf/router.py), [`test_router.py`](../tests/test_router.py) |
| R8 | the maximal feasible cut attains $O\!\left(n+\frac{N}{n+m}\right)$ depth for every large workspace, including $s=1$ | [compiler theorem, Proposition R](COMPILER_THEOREM.md#proposition-r-maximal-cut-depth) | [`resource_bounds.py`](../compiler_robust_hopf/resource_bounds.py), broad-grid tests |
| R9 | parameter capacity and output light cones give matching lower bounds | [compiler theorem, Section 9](COMPILER_THEOREM.md#9-matching-lower-bounds) | diagnostic checks in [`test_resource_bounds.py`](../tests/test_resource_bounds.py) |
| R10 | the real frame and phase-dressed complex magnitude frame attain the all-workspace optimum | [compiler theorem, main theorem](COMPILER_THEOREM.md#main-theorem-optimal-exact-hopf-frame-compilation) | [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py), both resource ledgers |
| R11 | frame-safe compilation preserves the global record and introduces no additional asymptotic depth factor in the matched program | [QBP consequence](QBP_CONSEQUENCE.md) | decoder and boundary tests; reviewer walkthrough |

## 5. Evidence classification

The local evidence has four distinct levels.

| Level | Examples |
|---|---|
| analytic identity | addressed layers, echo sectors, tree cut, lower bounds |
| explicit reversible construction | binary–one-hot decoder and coherent router |
| imported exact synthesis | elementary UCG and multi-controlled-X circuits |
| finite regression evidence | matrix equality, entangled-input routing, cleanup, and resource ledgers |

The finite checks are designed to expose convention, indexing, order, phase,
cleanup, and resource errors.  They do not replace the asymptotic proofs.

## 6. Provenance records

- [`provenance/upstream.json`](../provenance/upstream.json): upstream commits,
  file lineage, and reconciliation;
- [`provenance/literature.json`](../provenance/literature.json): compiler source
  versions and role assignments;
- [`provenance/prior_art_search.json`](../provenance/prior_art_search.json):
  bounded technical search and claim limits;
- [`SYNC.md`](../SYNC.md): human-readable synchronization policy.

These records preserve provenance and source discipline; they are not additional
scientific assumptions.

---

[← Verification](VERIFICATION.md) · [Complete narrative](../REVIEW.md) · [Related work →](RELATED_WORK.md)
