# Source and dependency map

[← Verification](VERIFICATION.md) · [Complete technical note](../REVIEW.md) · [Next: related work →](RELATED_WORK.md)

This page records every load-bearing dependency of the compiler theorem. Four
statuses are used:

- **inherited:** established in one of the Hopf papers and restated here;
- **imported:** an external circuit theorem used as a primitive or benchmark;
- **proved here:** an operator, compiler, or resource statement developed in
  this repository;
- **tested here:** finite executable evidence supporting an analytic statement.

The two state-preparation papers are treated in the narrative as one coherent
compiler line. Formal citations below retain complete authorship and exact
attribution.

The tracked `Hopf-QBP/main` baseline is

```text
faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582
```

and the reconciliation record is stored in [`SYNC.md`](../SYNC.md).

## 1. Hopf chart and differential-frame interface

| ID | Fact used by the compiler theorem | Status | Source location | Local counterpart |
|---|---|---|---|---|
| H1 | complete balanced tree with `N=2^n` leaves and `N-1` magnitude coordinates | inherited | Hopf-ansatz, Definition 1 | [`frames.py`](../compiler_robust_hopf/frames.py) |
| H2 | sine–cosine path map covers normalized real states; leaf phases give the complex chart | inherited | Hopf-ansatz, Definitions 2–3 | [`real_tree_data`](../compiler_robust_hopf/frames.py), [`complex_state`](../compiler_robust_hopf/complex_analysis.py) |
| H3 | canonical real domains use `[0,pi/2]` above the final depth and `[0,2pi)` at the final depth; complex magnitudes use `[0,pi/2]` throughout | inherited and made executable here | Hopf-ansatz chart-domain definitions | [`canonical_magnitude_angle_mask`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) |
| H4 | the oriented incoming amplitude satisfies `partial_(theta_j)|psi>=a_j|e_j>` and `g_(j,j)=a_j^2` | inherited identity, notation made explicit here | Hopf-ansatz metric and tangent results | [`RealTreeData.incoming_amplitude`](../compiler_robust_hopf/frames.py), [`test_complex_analysis.py`](../tests/test_complex_analysis.py) |
| H5 | on the canonical domains, `a_j>=0` and `a_j=sqrt(g_(j,j))` | consequence of H3–H4 | Hopf-ansatz canonical chart | [`test_frames.py`](../tests/test_frames.py) |
| H6 | at `g_(j,j)=0`, the raw differential vanishes while the marker column remains a chart-selected orthogonal frame direction | boundary clarification | recursive differential identity | tolerance-aware masks and singular tests in [`frames.py`](../compiler_robust_hopf/frames.py) and [`test_frames.py`](../tests/test_frames.py) |
| H7 | objective derivative is `2a_j Re<e_j|O|psi>` and becomes the usual positive metric-weight expression on the canonical chart | inherited | Hopf-ansatz objective-gradient result | [QBP consequence](QBP_CONSEQUENCE.md) |
| H8 | computational marker `lambda(j)` labels the frame direction associated with tree node `j` | inherited | Hopf-QBP frame construction | [`conventions.py`](../compiler_robust_hopf/conventions.py), [`frames.py`](../compiler_robust_hopf/frames.py) |
| H9 | the complete real frame is the ordered product of addressed zero-suffix layers | inherited operator interface | Hopf-QBP frame construction | independent recursive and addressed constructions in [`frames.py`](../compiler_robust_hopf/frames.py) |
| H10 | `W_(C,mag)=D_ph W_R` is the phase-dressed complex magnitude frame | inherited and named precisely here | Hopf-QBP complex magnitude construction | [`complex_magnitude_frame_matrix`](../compiler_robust_hopf/frames.py) |

The compiler proof consumes only the interface in
[Minimal Hopf interface](HOPF_INTERFACE.md). The inverse coordinate map and
optimization architecture remain in the first Hopf paper.

## 2. Hopf quantum-backpropagation interface

| ID | Fact used here | Status | Upstream location | Local counterpart |
|---|---|---|---|---|
| Q1 | the global magnitude circuit applies the complete inverse differential frame | inherited | Hopf-QBP global-frame protocol | [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) |
| Q2 | one X-basis outcome contributes one parity record to every magnitude coordinate | inherited | Hopf-QBP global-record equations | [`decoders.py`](../compiler_robust_hopf/decoders.py), [`test_decoders.py`](../tests/test_decoders.py) |
| Q3 | complex leaf-phase derivatives use a separate signed one-hot stream | inherited | Hopf-QBP direct phase protocol | [`decoders.py`](../compiler_robust_hopf/decoders.py), [`complex_analysis.py`](../compiler_robust_hopf/complex_analysis.py) |
| Q4 | primary finite-shot target is simultaneous absolute accuracy of the raw coordinate gradient | inherited | `Hopf-QBP/docs/STATISTICAL_ACCURACY.md` | [QBP consequence, Section 5](QBP_CONSEQUENCE.md#5-accuracy-target-and-conditioning-boundary) |
| Q5 | complete-vector, relative, directional, normalized-frame, and natural-gradient targets have different sample or conditioning requirements | inherited task boundary | same statistical-accuracy document | [QBP consequence](QBP_CONSEQUENCE.md) |
| Q6 | fixed-norm depth records give `O((1+log(n/delta))/epsilon_infinity^2)` magnitude executions | inherited | Hopf-QBP concentration analysis | [QBP consequence, Section 5](QBP_CONSEQUENCE.md#5-accuracy-target-and-conditioning-boundary) |
| Q7 | the validated core assumes phase-calibrated controlled access to a Hermitian unitary observable | inherited assumption | Hopf-QBP controlled-observable interface | [QBP consequence, Section 2](QBP_CONSEQUENCE.md#2-controlled-observable-interface) |
| Q8 | output-sensitive decoding uses the better of record-wise and histogram/FWHT routes | inherited and consolidated | Hopf-QBP decoder analysis | local bound `O(S+N min{S,n})` in [`decoders.py`](../compiler_robust_hopf/decoders.py) |
| Q9 | checkpoint recompilation depends on the complete active interface, not only one prepared state | inherited question, sharpened here | Hopf-QBP checkpoint protocol | [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md), [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) |

## 3. State-preparation compiler line

### 3.1 Uniform all-workspace framework

Primary active citation:

> P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits,” *Quantum* **7**, 956 (2023),
> doi:10.22331/q-2023-03-20-956.

The published article corresponds to `arXiv:2202.11302v2`. The imported
statements were also checked in `arXiv:2202.11302v3`; their conclusions and exact
arbitrary-one-qubit+CNOT model are unchanged for the uses below.

| ID | Imported statement | Role in the Hopf-frame proof | Local consumer |
|---|---|---|---|
| YZ1 | Theorem 2: exact arbitrary QSP has `Theta(2^n)` size and `Theta(n+2^n/(n+m))` depth for every clean-ancillary budget | target frontier and comparison benchmark | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ2 | Lemma 5: exact ancilla-free multi-controlled `X` with linear size and depth | strict-zero toggles, direct suffix flags, and branch predicates | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`router.py`](../compiler_robust_hopf/router.py) |
| YZ3 | Lemma 6: total-width-`q` UCG with `O(2^q)` size and `O(q+2^q/(q+w))` depth using `w` clean work qubits | half-angle, direct flagged, subtree, and phase UCGs | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ4 | Lemma 9: coherent CNOT-tree copying and exact uncopying | prefix fanout, conditioned prefix, and branch routing | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py), [`router.py`](../compiler_robust_hopf/router.py) |
| YZ5 | Theorem 1: generic controlled state preparation scales with combined index and target width | explains the `O(N^2)` generic all-column route | [`resource_bounds.py`](../compiler_robust_hopf/resource_bounds.py), [Related work](RELATED_WORK.md) |

These primitives can be adapted once the complete-operator structure of the
Hopf frame is exposed. The addressed decomposition and workspace schedules are
proved here rather than inferred from the one-column QSP statement.

### 3.2 Historical predecessor

> X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, “Asymptotically Optimal
> Circuit Depth for Quantum State Preparation and General Unitary Synthesis,”
> *IEEE TCAD* **42**, 3301–3314 (2023),
> doi:10.1109/TCAD.2023.3244885.

This paper established the preceding ancilla–depth landscape and is the
historical and original-source reference for selected primitives. The later
uniform theorem is used as the sole active all-workspace benchmark, so the Hopf
compiler does not switch between the two papers by workspace regime.

## 4. UCG and borrowed-workspace lineage

| ID | Source line | Role and boundary |
|---|---|---|
| U1 | Möttönen et al., uniformly controlled rotations (2005) | state-preparation multiplexor lineage and the language used by the earlier Hopf-QBP compiler |
| U2 | Bergholm et al., uniformly controlled one-qubit gates (2005) | general block-diagonal UCG formulation |
| B1 | Barenco et al., elementary gate constructions (1995) | controlled-unitary roots and conjugation lineage |
| B2 | Claudon et al., borrowed-qubit controlled gates (2024) | exact control constructions using borrowed logical wires |
| B3 | Khattar and Gidney, conditionally clean ancillas (2025) | safe use and restoration of unknown-state wires and toggle-detection patterns |
| B4 | Zindorf and Bose, multi-controlled `SU(2)` gates (2025) | exact ancilla-free controlled-rotation context |
| U3 | recent restricted-UCG work | structured and sparse multiplexor context |

The repository does not claim invention of UCGs, controlled-unitary roots,
borrowed qubits, conditionally clean workspace, or toggle detection.

## 5. Results proved and tested here

| ID | Result | Analytic location | Implementation | Executable evidence |
|---|---|---|---|---|
| R1 | frame-safe substitution preserves the complete global QBP distribution | [`FRAME_SAFE_COMPILATION.md`](FRAME_SAFE_COMPILATION.md) | compiler-contract fixtures | [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py) |
| R2 | state-column equality can preserve the state while corrupting marker decoding | [`HOPF_INTERFACE.md`](HOPF_INTERFACE.md), [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md) | [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) | [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py) |
| R3 | strict-zero borrowed-suffix echo implements one addressed layer exactly | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py) | [`test_strict_zero_echo.py`](../tests/test_strict_zero_echo.py) |
| R4 | strict-zero frame has `Theta(N)` size and `Theta(n+N/n)` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | strict-zero ledger | [`test_strict_zero_audit.py`](../tests/test_strict_zero_audit.py) |
| R5 | conditioned-prefix and tail direct-sum identities | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`tree_structure.py`](../compiler_robust_hopf/tree_structure.py) | [`test_unified_compiler.py`](../tests/test_unified_compiler.py) |
| R6 | clean binary–one-hot decoder with `3*2^t-2-t` workspace and `O(t)` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py) | [`test_tree_decoder.py`](../tests/test_tree_decoder.py) |
| R7 | explicit coherent router with exact copy and Fredkin counts | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`router.py`](../compiler_robust_hopf/router.py) | [`test_router.py`](../tests/test_router.py) |
| R8 | route–controlled-subframes–unroute equals the ideal tail direct sum and returns all workspace clean | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | sparse-state simulator in [`router.py`](../compiler_robust_hopf/router.py) | arbitrary complex and complete-cut tests in [`test_router.py`](../tests/test_router.py) |
| R9 | every positive workspace budget attains the optimal depth order | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | unified schedule selection | [`test_unified_compiler.py`](../tests/test_unified_compiler.py), [`test_resource_bounds.py`](../tests/test_resource_bounds.py) |
| R10 | real and phase-dressed complex magnitude frames match the QSP frontier for every `m>=0` | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) | complete suite and both resource ledgers |
| R11 | frame-safe compilation adds no asymptotic depth factor to the matched global-QBP execution | [`QBP_CONSEQUENCE.md`](QBP_CONSEQUENCE.md) | frame compiler plus inherited decoder | [`technical_walkthrough.py`](../scripts/technical_walkthrough.py), complete suite |

## 6. Machine-readable provenance

- [`provenance/upstream.json`](../provenance/upstream.json): tracked Hopf
  repositories, exact baselines, and local file lineage;
- [`provenance/literature.json`](../provenance/literature.json): state-preparation
  source versions, historical role, UCG lineage, and claim policy;
- [`provenance/prior_art_search.json`](../provenance/prior_art_search.json):
  bounded technical-search record and its limits;
- [`SYNC.md`](../SYNC.md): human-readable source-of-truth policy.

These records preserve provenance. They are not additional scientific
assumptions.

---

[← Verification](VERIFICATION.md) · [Complete technical note](../REVIEW.md) · [Next: related work →](RELATED_WORK.md)
