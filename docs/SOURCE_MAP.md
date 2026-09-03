# Source and dependency map

[← Verification](VERIFICATION.md) · [Read the complete narrative](../REVIEW.md) · [Next: related work →](RELATED_WORK.md)

This page identifies every load-bearing fact used by the compiler theorem. It
separates four roles:

- **inherited:** established in an earlier Hopf paper and restated here;
- **imported:** a circuit-synthesis theorem used as a black-box primitive or
  comparison benchmark;
- **proved here:** an operator, compiler, or resource argument developed in this
  repository;
- **tested here:** finite executable evidence supporting an analytic statement.

Paper numbering follows the technical-review copies accompanying the
repositories. The current tracked `Hopf-QBP/main` baseline is
`faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582`.

## 1. Hopf chart and differential geometry

| ID | Fact used here | Status | Paper location | Repository counterpart |
|---|---|---|---|---|
| H1 | complete balanced binary tree with `N=2^n` leaves and `N-1` magnitude coordinates | inherited | Hopf-ansatz, Definition 1 | upstream chart utilities; local [`frames.py`](../compiler_robust_hopf/frames.py) |
| H2 | sine–cosine path map prepares every normalized real state; leaf phases give the complex chart | inherited | Hopf-ansatz, Definitions 2–3 | local [`real_tree_data`](../compiler_robust_hopf/frames.py) and [`complex_state`](../compiler_robust_hopf/complex_analysis.py) |
| H3 | canonical real domains use `[0,pi/2]` above the final depth and `[0,2pi)` at the final depth; complex magnitudes use `[0,pi/2]` throughout | inherited and made executable here | Hopf-ansatz chart-domain definitions | [`canonical_magnitude_angle_mask`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) |
| H4 | the oriented incoming amplitude satisfies `g_(j,j)=a_j^2` and `partial_(theta_j)|psi>=a_j|e_j>` | inherited identity, notation sharpened here | Hopf-ansatz metric and tangent results | [`RealTreeData.incoming_amplitude`](../compiler_robust_hopf/frames.py), [`test_complex_analysis.py`](../tests/test_complex_analysis.py) |
| H5 | on the canonical domains `a_j>=0`, so `a_j=sqrt(g_(j,j))` | consequence of H3–H4 | Hopf-ansatz canonical chart | [`test_frames.py`](../tests/test_frames.py) |
| H6 | at `g_(j,j)=0`, the raw differential vanishes; the unit marker column is a canonical orthogonal continuation rather than normalization of a nonzero derivative | boundary clarification | implied by the recursive differential identity | [`regular_mask`](../compiler_robust_hopf/frames.py), singular-coordinate test in [`test_frames.py`](../tests/test_frames.py) |
| H7 | objective derivative is `2a_j Re<e_j|O|psi>` and becomes the usual `2sqrt(g_(j,j))` expression on the canonical chart | inherited | Hopf-ansatz objective-gradient theorem | [QBP consequence](QBP_CONSEQUENCE.md) |
| H8 | computational marker `lambda(j)` labels the frame continuation at node `j` | inherited and restated | Hopf-QBP, frame construction | local [`conventions.py`](../compiler_robust_hopf/conventions.py), [`frames.py`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) |
| H9 | the phase-dressed complex magnitude frame is `W_(C,mag)=D_ph W_R` | inherited and renamed for precision | Hopf-QBP complex magnitude-frame appendix | local [`complex_magnitude_frame_matrix`](../compiler_robust_hopf/frames.py) |

The complete optimizer and inverse-map context remains in the first Hopf paper.
The compiler proof consumes the concise interface in
[Minimal Hopf interface](HOPF_INTERFACE.md).

## 2. Hopf quantum-backpropagation interface

| ID | Fact used here | Status | Upstream location | Local counterpart |
|---|---|---|---|---|
| Q1 | primary finite-shot target is simultaneous absolute accuracy of the raw Hopf-coordinate gradient | inherited | `Hopf-QBP/docs/STATISTICAL_ACCURACY.md` at the tracked main commit | [QBP consequence, Section 5](QBP_CONSEQUENCE.md#5-statistical-target-and-conditioning-boundary) |
| Q2 | complete-vector, relative, directional, normalized-frame, and natural-gradient targets have distinct conditioning and sample requirements | inherited task boundary | same statistical-accuracy document | local task-boundary discussion in [`QBP_CONSEQUENCE.md`](QBP_CONSEQUENCE.md) |
| Q3 | validated core assumes phase-calibrated controlled access to a Hermitian unitary observable | inherited assumption | Hopf-QBP controlled-observable interface | [QBP consequence, Section 2](QBP_CONSEQUENCE.md#2-controlled-observable-interface) |
| Q4 | global magnitude circuit applies the complete inverse differential frame | inherited | Hopf-QBP global-frame protocol | local compiler contract in [`FRAME_SAFE_COMPILATION.md`](FRAME_SAFE_COMPILATION.md) |
| Q5 | one all-X outcome contributes one parity record to every magnitude coordinate | inherited | Hopf-QBP global-record equations | local [`decoders.py`](../compiler_robust_hopf/decoders.py), [`test_decoders.py`](../tests/test_decoders.py) |
| Q6 | complex leaf-phase derivatives use a separate signed one-hot stream and do not require the inverse magnitude frame | inherited | Hopf-QBP direct phase protocol | local [`decoders.py`](../compiler_robust_hopf/decoders.py), [`complex_analysis.py`](../compiler_robust_hopf/complex_analysis.py) |
| Q7 | norm-two depth records yield `O((1+log(n/delta))/epsilon_infinity^2)` global executions for raw coordinatewise accuracy | inherited | Hopf-QBP statistical-accuracy analysis | [QBP consequence, Section 5](QBP_CONSEQUENCE.md#5-statistical-target-and-conditioning-boundary) |
| Q8 | output-sensitive decoding can use the better of record-wise and signed-histogram/FWHT routes | inherited and consolidated | Hopf-QBP decoder analysis | local bound `O(S+N min{S,n})` in [`QBP_CONSEQUENCE.md`](QBP_CONSEQUENCE.md) and [`decoders.py`](../compiler_robust_hopf/decoders.py) |
| Q9 | checkpoint recompilation depends on the active interface, not only on one prepared state | inherited question, sharpened here | Hopf-QBP checkpoint protocol | local [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md), [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) |

The ten-commit upstream change from the former tracked baseline to
`faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582` was reviewed explicitly. The
reconciliation record is in [`SYNC.md`](../SYNC.md) and
[`provenance/upstream.json`](../provenance/upstream.json).

## 3. Yuan–Zhang circuit framework

Primary citation:

> P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits,” *Quantum* **7**, 956 (2023),
> doi:10.22331/q-2023-03-20-956.

### Version policy

The published article corresponds to `arXiv:2202.11302v2` and is the normative
bibliographic source. The imported statements below were also checked in
`arXiv:2202.11302v3`; their theorem/lemma conclusions and the exact
arbitrary-one-qubit+CNOT model used here are unchanged.

| ID | Imported statement | Role here | Local consumer |
|---|---|---|---|
| YZ1 | Theorem 2: exact arbitrary state preparation has `Theta(2^n)` size and `Theta(n+2^n/(n+m))` depth for every clean-ancillary budget | optimal comparison frontier | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ2 | Lemma 5: exact ancilla-free multi-controlled X with linear size and depth | strict-zero toggles, suffix flags, and branch predicates | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`router.py`](../compiler_robust_hopf/router.py), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ3 | Lemma 6: a total-width-`q` UCG has `O(2^q)` size and `O(q+2^q/(q+w))` depth using `w` clean work qubits | half-angle UCGs, flagged layers, controlled subtree frames, and phase diagonal | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ4 | Lemma 9: coherent CNOT-tree copying and exact uncopying | prefix fanout, conditioned prefix, and coherent routing | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py), [`router.py`](../compiler_robust_hopf/router.py) |
| YZ5 | Theorem 1: generic controlled state preparation scales with combined index and target width | explains why treating all frame columns generically would cost `O(4^n)` and retain an index register | [`resource_bounds.py`](../compiler_robust_hopf/resource_bounds.py), [Related work](RELATED_WORK.md) |

Yuan–Zhang is the sole active external compiler framework and QSP benchmark in
this repository. Its primitives can be adapted once the special
complete-operator structure of the Hopf frame is exposed. The Hopf decomposition
and workspace schedules are proved here rather than inferred directly from a
state-preparation theorem.

## 4. Historical state-preparation predecessor

> X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, “Asymptotically Optimal
> Circuit Depth for Quantum State Preparation and General Unitary Synthesis,”
> *IEEE TCAD* **42**, 3301–3314 (2023),
> doi:10.1109/TCAD.2023.3244885.

This paper is cited as the historical predecessor to the uniform all-workspace
frontier and as the original source credited by Yuan–Zhang for selected
primitives. It is not a second active compiler selected in another workspace
regime.

## 5. UCG and strict-zero lineage

| ID | Source line | Role and boundary |
|---|---|---|
| U1 | Möttönen et al., “Transformation of quantum states using uniformly controlled rotations” (2005) | multiplexed state-preparation and uniformly controlled rotation lineage |
| U2 | Bergholm et al., “Quantum circuits with uniformly controlled one-qubit gates” (2005) | general UCG/multiplexor language |
| B1 | Barenco et al., “Elementary gates for quantum computation” (1995) | square-root and conjugation lineage for controlled-unitary decompositions |
| B2 | Khattar and Gidney, “Rise of conditionally clean ancillae…” (2025) | conditionally clean workspace and toggle-detection lineage |
| B3 | Zindorf and Bose, efficient multi-controlled-gate work (2025) | exact ancilla-free controlled-rotation context |
| B4 | recent restricted-UCG work | structured and sparse UCG context |

The repository does not claim invention of UCGs, borrowed or conditionally
clean qubits, toggle detection, or square-root/conjugation identities.

The narrow project-specific strict-zero claim is:

> One original suffix data qubit is used as a restored in-place predicate
> carrier, allowing all prefix-dependent Hopf rotations at depth `d` to be
> aggregated into two total-width-`d+2` UCGs and linear predicate toggles,
> thereby attaining the optimal strict-zero complete-frame frontier.

## 6. Results proved and tested here

| ID | Result | Proof | Implementation | Executable evidence |
|---|---|---|---|---|
| R1 | frame-safe substitution preserves the complete global QBP distribution | [`FRAME_SAFE_COMPILATION.md`](FRAME_SAFE_COMPILATION.md) | compiler contracts | [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py) |
| R2 | state-column equality can preserve the state while corrupting the decoded gradient | [`HOPF_INTERFACE.md`](HOPF_INTERFACE.md), [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md) | [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) | [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py) |
| R3 | strict-zero borrowed-suffix echo implements one addressed layer exactly | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py) | [`test_strict_zero_echo.py`](../tests/test_strict_zero_echo.py) |
| R4 | strict-zero frame has `Theta(N)` size and `Theta(n+N/n)` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | strict-zero ledger | [`test_strict_zero_audit.py`](../tests/test_strict_zero_audit.py) |
| R5 | conditioned-prefix and tail direct-sum identities | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`tree_structure.py`](../compiler_robust_hopf/tree_structure.py) | [`test_unified_compiler.py`](../tests/test_unified_compiler.py) |
| R6 | explicit clean binary–one-hot decoder with `3*2^t-2-t` workspace and `O(t)` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py) | [`test_tree_decoder.py`](../tests/test_tree_decoder.py) |
| R7 | explicit coherent router with `(2^t-1)(s+1)-t` copies and `(2^t-1)(s+1)` forward Fredkins | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`router.py`](../compiler_robust_hopf/router.py) | [`test_router.py`](../tests/test_router.py) |
| R8 | route–controlled-subframes–unroute equals the ideal tail direct sum on arbitrary inputs and returns workspace clean | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | sparse-state simulator in [`router.py`](../compiler_robust_hopf/router.py) | arbitrary complex and full-cut tests in [`test_router.py`](../tests/test_router.py) |
| R9 | every positive workspace budget attains `Theta(n+N/(n+m))` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | unified resource selection | [`test_unified_compiler.py`](../tests/test_unified_compiler.py), [`test_resource_bounds.py`](../tests/test_resource_bounds.py) |
| R10 | real frame and phase-dressed complex magnitude frame attain the optimal frontier for every `m>=0` | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) | complete suite and both resource ledgers |
| R11 | frame-safe compilation adds no asymptotic depth factor to the matched global-QBP execution overhead | [`QBP_CONSEQUENCE.md`](QBP_CONSEQUENCE.md) | frame compiler plus inherited decoder | [`reviewer_walkthrough.py`](../scripts/reviewer_walkthrough.py), complete suite |

## 7. Provenance records

- [`provenance/upstream.json`](../provenance/upstream.json): tracked upstream
  commits, exact old file lineage, and the current reconciliation record;
- [`provenance/literature.json`](../provenance/literature.json): published and
  checked Yuan–Zhang versions, historical role, UCG lineage, and claim policy;
- [`provenance/prior_art_search.json`](../provenance/prior_art_search.json):
  bounded technical-search record and claim limits;
- [`SYNC.md`](../SYNC.md): human-readable source-of-truth and synchronization
  policy.

These records preserve provenance; they are not additional scientific premises.

---

[← Verification](VERIFICATION.md) · [Read the complete narrative](../REVIEW.md) · [Next: related work →](RELATED_WORK.md)
