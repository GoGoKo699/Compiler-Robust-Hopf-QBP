# Source and dependency map

[← Verification](VERIFICATION.md) · [Read the complete narrative](../REVIEW.md) · [Next: related work →](RELATED_WORK.md)

This page identifies every load-bearing fact used by the compiler theorem. It
separates four roles:

- **inherited:** established in an earlier Hopf paper and restated here;
- **imported:** a circuit-synthesis theorem used as a black-box primitive or
  benchmark;
- **proved here:** a new operator, compiler, or resource argument in this
  repository;
- **tested here:** finite executable evidence supporting an analytic statement.

Paper numbering below follows the technical review copies accompanying the
repositories. Equation and appendix labels may move during later editorial
revision; the mathematical statement and repository pointer are the stable
identifiers.

## 1. Hopf chart and differential geometry

| ID | Fact used here | Status | Paper location | Repository counterpart |
|---|---|---|---|---|
| H1 | complete balanced binary tree with `N=2^n` leaves and `N-1` magnitude coordinates | inherited | Hopf-ansatz, Definition 1 | [`Hopf-ansatz/hopf_utils.py`](https://github.com/GoGoKo699/Hopf-ansatz/blob/main/hopf_utils.py); local [`frames.py`](../compiler_robust_hopf/frames.py) |
| H2 | sine–cosine path map prepares every normalized real state; leaf phases give the complex chart | inherited | Hopf-ansatz, Definitions 2–3 | [`Hopf-ansatz/hopf_utils.py`](https://github.com/GoGoKo699/Hopf-ansatz/blob/main/hopf_utils.py); local [`frames.py`](../compiler_robust_hopf/frames.py) |
| H3 | pullback metric is diagonal; a magnitude weight is the probability mass entering its tree node | inherited | Hopf-ansatz, Theorem 1 | [`Hopf-ansatz/hopf_utils.py`](https://github.com/GoGoKo699/Hopf-ansatz/blob/main/hopf_utils.py); local [`frames.py`](../compiler_robust_hopf/frames.py) |
| H4 | normalized magnitude direction satisfies `partial_(theta_j)|psi> = sqrt(g_(j,j)) |e_j>` | inherited | Hopf-ansatz, Definition 5 and Theorem 3 | local [`real_tree_data`](../compiler_robust_hopf/frames.py); [`test_complex_analysis.py`](../tests/test_complex_analysis.py) |
| H5 | objective derivative is the transition moment `2 sqrt(g_(j,j)) Re<e_j|O|psi>` | inherited | Hopf-ansatz, Theorem 2 | [QBP consequence](QBP_CONSEQUENCE.md) |
| H6 | computational marker `lambda(j)` labels the normalized tangent column | inherited and restated | Hopf-QBP, Section III and Appendix A.5 | local [`conventions.py`](../compiler_robust_hopf/conventions.py), [`frames.py`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) |
| H7 | separated complex magnitude frame is `W_C=D_ph W_R` | inherited and restated | Hopf-QBP, Appendix A.6, Eq. (A3) | local [`complex_frame_matrix`](../compiler_robust_hopf/frames.py) |

The complete derivation and optimizer context for H1–H5 remain in the first
paper and repository. The compiler proof consumes only the concise interface in
[Minimal Hopf interface](HOPF_INTERFACE.md).

## 2. Hopf quantum-backpropagation interface

| ID | Fact used here | Status | Paper location | Repository counterpart |
|---|---|---|---|---|
| Q1 | complete-gradient target is simultaneous coordinatewise accuracy | inherited | Hopf-QBP, Definition 1 | [QBP consequence](QBP_CONSEQUENCE.md) |
| Q2 | state-coordinate QBP resolves a coherent objective response into vector-valued differential records | inherited | Hopf-QBP, Definition 2 | [QBP consequence](QBP_CONSEQUENCE.md) |
| Q3 | validated core assumes phase-calibrated controlled access to a Hermitian unitary observable | inherited assumption | Hopf-QBP, Assumption 1 | [QBP consequence, controlled interface](QBP_CONSEQUENCE.md#2-controlled-observable-interface) |
| Q4 | global magnitude circuit applies the complete inverse differential frame | inherited | Hopf-QBP, global-frame protocol and Appendix A | local compiler contract in [`FRAME_SAFE_COMPILATION.md`](FRAME_SAFE_COMPILATION.md) |
| Q5 | one all-X outcome gives `Z_j=2 sqrt(g_(j,j)) (-1)^(b+lambda(j)·y)` for every magnitude coordinate | inherited | Hopf-QBP, Eqs. (23)–(28) | local [`decoders.py`](../compiler_robust_hopf/decoders.py), [`test_decoders.py`](../tests/test_decoders.py) |
| Q6 | complex leaf-phase record is a signed one-hot vector and needs no inverse frame | inherited | Hopf-QBP, direct phase protocol | local [`decoders.py`](../compiler_robust_hopf/decoders.py), [`complex_analysis.py`](../compiler_robust_hopf/complex_analysis.py) |
| Q7 | fixed-norm depth records yield `O((1+log(n/delta))/epsilon^2)` global executions | inherited | Hopf-QBP, Eqs. (48)–(51) | [QBP consequence, execution count](QBP_CONSEQUENCE.md#5-fixed-norm-records-and-execution-count) |
| Q8 | checkpoint recompilation depends on the active interface, not only on the prepared state | inherited question, sharpened here | Hopf-QBP checkpoint protocol and circuit contracts | local [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md), [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) |

The QBP paper proves the record identities and concentration statement. This
repository proves that a frame-safe compiled implementation can replace the
addressed frame without changing the global measurement distribution.

## 3. Yuan–Zhang circuit framework

Primary source:

> P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits,” *Quantum* **7**, 956 (2023),
> [doi:10.22331/q-2023-03-20-956](https://doi.org/10.22331/q-2023-03-20-956).

| ID | Imported statement | Role here | Local consumer |
|---|---|---|---|
| YZ1 | Theorem 2: exact arbitrary state preparation has `Theta(2^n)` size and `Theta(n+2^n/(n+m))` depth for every ancillary budget | optimal comparison frontier | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ2 | Lemma 5: exact ancilla-free multi-controlled X with linear size and depth | suffix predicates and strict-zero toggles | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), direct and branch ledgers in [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ3 | Lemma 6: a total-width-`q` UCG has `O(2^q)` size and `O(q+2^q/(q+w))` depth using `w` clean work qubits | half-angle UCGs, flagged layers, controlled subframes, and phase diagonal | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ4 | Lemma 9: coherent CNOT-tree copying and exact uncopying | prefix-control fanout and coherent routing | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py), [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) |
| YZ5 | Theorem 1: generic controlled state preparation scales with the combined index and state width | explains why treating all frame columns generically would cost `O(4^n)` and retain an index register | [`resource_bounds.py`](../compiler_robust_hopf/resource_bounds.py), [Related work](RELATED_WORK.md) |

Yuan–Zhang is the sole active external compiler framework and QSP benchmark in
this repository. The statements above can be adapted to the Hopf frame once its
complete operator structure is exposed. The Hopf-specific decomposition and
workspace schedules are proved here rather than read directly from the state-
preparation theorem.

## 4. Historical state-preparation predecessor

> X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, “Asymptotically Optimal
> Circuit Depth for Quantum State Preparation and General Unitary Synthesis,”
> *IEEE Transactions on Computer-Aided Design of Integrated Circuits and
> Systems* **42**, 3301–3314 (2023),
> [doi:10.1109/TCAD.2023.3244885](https://doi.org/10.1109/TCAD.2023.3244885).

This paper is cited as the memorable historical predecessor to the uniform
all-workspace theorem and as the original source credited by Yuan–Zhang for
selected primitives. It is not a second active compiler selected in another
workspace regime.

## 5. Uniformly controlled gates and strict-zero lineage

| ID | Source line | Role and boundary |
|---|---|---|
| U1 | M. Möttönen et al., “Transformation of quantum states using uniformly controlled rotations” (2005) | state-preparation and multiplexed-rotation lineage; motivates the earlier Hopf-QBP optimized compiler |
| U2 | V. Bergholm et al., “Quantum circuits with uniformly controlled one-qubit gates” (2005) | general UCG/multiplexor language used throughout the construction |
| B1 | A. Barenco et al., “Elementary gates for quantum computation” (1995) | square-root and Pauli-conjugation lineage for controlled-unitary decompositions |
| B2 | T. Khattar and C. Gidney, “Rise of conditionally clean ancillae for efficient quantum circuit constructions” (2025) | conditionally clean qubits and toggle-detection lineage |
| B3 | B. Zindorf and S. Bose, “Efficient implementation of multi-controlled quantum gates” (2025) | exact ancilla-free multi-controlled `SU(2)` context |
| B4 | C. Xu et al., “A Unified Framework for Optimizing Uniformly Controlled Structures in Quantum Circuits” (2025) | restricted/sparse UCG context |

The repository does **not** claim invention of UCGs, borrowed or conditionally
clean qubits, toggle detection, or square-root/conjugation identities.

The narrow project-specific claim is:

> One original suffix data qubit is used as a restored in-place predicate
> carrier, allowing all prefix-dependent Hopf rotations at depth `d` to be
> aggregated into two total-width-`d+2` UCGs and linear predicate toggles, which
> closes the optimal strict-zero complete-frame frontier.

The detailed and deliberately conservative comparison is in
[Related work](RELATED_WORK.md) and the supporting prior-art records.

## 6. Results proved in this repository

| ID | Result | Proof | Implementation | Executable evidence |
|---|---|---|---|---|
| R1 | frame-safe substitution preserves the complete global QBP distribution | [`FRAME_SAFE_COMPILATION.md`](FRAME_SAFE_COMPILATION.md) | compiler contracts | [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py) |
| R2 | state-column equality can preserve the state while corrupting the gradient | [`HOPF_INTERFACE.md`](HOPF_INTERFACE.md) and [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md) | [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) | [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py) |
| R3 | strict-zero borrowed-suffix echo implements one addressed layer exactly | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py) | [`test_strict_zero_echo.py`](../tests/test_strict_zero_echo.py) |
| R4 | strict-zero frame has `Theta(N)` size and `Theta(n+N/n)` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | strict-zero ledger | [`test_strict_zero_audit.py`](../tests/test_strict_zero_audit.py) |
| R5 | conditioned-prefix and tail direct-sum identities | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`tree_structure.py`](../compiler_robust_hopf/tree_structure.py) | [`test_unified_compiler.py`](../tests/test_unified_compiler.py) |
| R6 | explicit clean binary–one-hot decoder with `3·2^t-2-t` workspace and `O(t)` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py) | [`test_tree_decoder.py`](../tests/test_tree_decoder.py) |
| R7 | routed tail fits in `2B(s+1)` clean workspace and has parallel subtree depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) | [`test_resource_bounds.py`](../tests/test_resource_bounds.py) |
| R8 | all positive workspace budgets attain `Theta(n+N/(n+m))` depth | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | unified resource selection | [`test_unified_compiler.py`](../tests/test_unified_compiler.py) |
| R9 | real and separated complex frames attain the optimal frontier for every `m>=0` | [`COMPILER_THEOREM.md`](COMPILER_THEOREM.md) | [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) | both resource ledgers and complete suite |
| R10 | frame-safe compilation adds no asymptotic depth factor to the shared global QBP execution overhead | [`QBP_CONSEQUENCE.md`](QBP_CONSEQUENCE.md) | frame compiler plus inherited decoder | [`reviewer_walkthrough.py`](../scripts/reviewer_walkthrough.py), complete suite |

## 7. Version and provenance records

The repository keeps machine-readable records for automated consistency checks:

- [`provenance/upstream.json`](../provenance/upstream.json): inherited local code
  lineage and recorded upstream commits;
- [`provenance/literature.json`](../provenance/literature.json): active compiler,
  historical, UCG, and borrowed-workspace literature roles;
- [`provenance/prior_art_search.json`](../provenance/prior_art_search.json):
  bounded technical search record and claim limits;
- [`SYNC.md`](../SYNC.md): human-readable relationship to the two Hopf
  repositories.

These records preserve provenance; they are not additional scientific premises.

---

[← Verification](VERIFICATION.md) · [Read the complete narrative](../REVIEW.md) · [Next: related work →](RELATED_WORK.md)
