# Claim support map

[← Documentation index](README.md) · [Complete compiler proof](COMPILER_THEOREM.md) · [Verification →](VERIFICATION.md)

This page connects each principal claim to its analytic argument, local
implementation, executable support, and scope boundary. It is an audit map, not
a substitute for the proof.

## 1. Structured unitary target

| Claim | Analytic support | Implementation | Tests | Boundary |
|---|---|---|---|---|
| the real Hopf frame contains the state and `N-1` prescribed marker directions | [Minimal Hopf interface](HOPF_INTERFACE.md) | [`frames.py`](../compiler_robust_hopf/frames.py) | [`test_frames.py`](../tests/test_frames.py) | frame directions at zero metric weight are chart-selected continuations, not normalized nonzero derivatives |
| unrestricted differentials use the oriented weight `a_j`, with `g_(j,j)=a_j^2` | [Hopf interface, Section 3](HOPF_INTERFACE.md#3-differential-weights-and-coordinate-domains) | `RealTreeData.incoming_amplitude` | frame and complex-analysis tests | `a_j=sqrt(g_(j,j))` only on the canonical domains |
| the complete frame is the product of addressed zero-suffix layers | [Hopf interface, Section 4](HOPF_INTERFACE.md#4-complete-addressed-layers) | independent recursive and addressed constructions in [`frames.py`](../compiler_robust_hopf/frames.py) | complete operator comparison | layer order and basis convention are fixed by the marker map |

## 2. Compiler contract

| Claim | Analytic support | Implementation | Tests | Boundary |
|---|---|---|---|---|
| complete frame safety implies exact inverse action | [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) | clean-subspace contract used throughout the compiler | boundary tests | requires exact workspace return and unitarity |
| one correct state column is insufficient | [Compiler boundaries, Section 1](COMPILER_BOUNDARIES.md#1-global-frame-the-first-column-obstruction) | [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) | two-qubit state, response, and decoder tests | does not say that a preparation compiler cannot be adapted; it says the promise must be strengthened |
| checkpoint methods require their complete active interface | [Compiler boundaries, Sections 2–4](COMPILER_BOUNDARIES.md) | exact checkpoint fixtures | checkpoint boundary tests | active-interface equality may preserve the mean without preserving the complete distribution |

## 3. Strict zero workspace

| Claim | Analytic support | Implementation | Tests | Boundary |
|---|---|---|---|---|
| the borrowed-suffix echo equals one addressed layer on the complete Hilbert space | [Compiler theorem, Section 4](COMPILER_THEOREM.md#4-schedule-z-strict-zero-workspace) | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py) | four sectors and every nonfinal depth through `n=8` | borrowed bit is logical data and must be restored exactly |
| no hidden ancillary wire is used | same four-sector and participant count | explicit permutations and block matrices | resource-width and endpoint tests | remaining suffix bits are controls, not work qubits |
| strict-zero size is `Theta(N)` | layer sum plus real-state parameter lower bound | strict-zero resource row | exact size-sum tests | exact logical circuit model |
| strict-zero depth is `Theta(n+N/n)` | UCG harmonic sum plus depth lower bound | strict-zero depth proxy | exact-rational inequality tests | imports Yuan–Zhang Lemmas 5–6 |

## 4. Positive workspace

| Claim | Analytic support | Implementation | Tests | Boundary |
|---|---|---|---|---|
| one reusable clean suffix flag attains the frontier for `1<=m<4n` | [Compiler theorem, Section 5](COMPILER_THEOREM.md#5-schedule-p1-small-positive-workspace) | direct resource rows in [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) | endpoint and absorption tests | threshold is proof-oriented, not a tuned finite crossover |
| the conditioned prefix identity is exact | [Compiler theorem, Section 6.1](COMPILER_THEOREM.md#61-exact-tree-cut) | [`tree_structure.py`](../compiler_robust_hopf/tree_structure.py) | every cut through small `n` | complete-operator statement |
| the tail is a direct sum of subtree frames | same | subtree angle map and ideal direct sum | complete cut tests | relies on prefix invariance of lower layers |
| the binary–one-hot decoder has `3*2^t-2-t` workspace and `O(t)` depth | [Compiler theorem, Section 6.2](COMPILER_THEOREM.md#62-conditioned-prefix) | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py) | clean labels, arbitrary basis reversibility, layer disjointness, exact counts | Toffoli and fixed-width controlled Givens gates are constant-width readable primitives |
| the router coherently implements route–operate–unroute | [Compiler theorem, Section 6.3](COMPILER_THEOREM.md#63-explicit-coherent-router) | [`router.py`](../compiler_robust_hopf/router.py) | arbitrary complex entangled inputs, direct-sum equality, complete cut equality | logical all-to-all model |
| every routed work register returns to zero | same schedule | sparse-state simulator | token, copy, flag, and data leakage tests | cleanup is checked before the inverse route |
| copy wires can be reused as branch flags | [Compiler theorem, Section 6.4](COMPILER_THEOREM.md#64-simultaneous-workspace-peak) | router layout | exact ledger tests | displayed inequality assumes `t>=1` and `s>=2`; `s=1` uses no suffix flag |
| the largest feasible cut gives `N/(n+m)` | [Compiler theorem, Section 6.5](COMPILER_THEOREM.md#65-largest-feasible-cut) | `choose_routed_cut` | broad-grid integer checks | `s=1` treated separately |

## 5. Optimality

| Claim | Analytic support | Implementation | Tests | Boundary |
|---|---|---|---|---|
| size lower bound `Omega(N)` | real-state family dimension | diagnostic helper | safe parameter-count tests | general exact real-state family |
| depth lower bound `Omega(N/(n+m))` | parameterized gate locations per layer | diagnostic helper | broad budget checks | arbitrary one-qubit parameters and fixed circuit topology families |
| depth lower bound `Omega(n)` | backward light cones of the `n` system outputs | diagnostic helper | integer checks | logical two-qubit-gate model |
| all-workspace real-frame frontier is tight | upper schedules plus lower bounds | unified resource row | broad-grid resource tests | exact all-to-all logical model |

## 6. Phase-dressed complex magnitude frame

| Claim | Analytic support | Implementation | Tests | Boundary |
|---|---|---|---|---|
| an arbitrary leaf-phase diagonal is one total-width-`n` UCG | [Compiler theorem, Section 8](COMPILER_THEOREM.md#8-phase-dressed-complex-magnitude-frame) | phase blocks in [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py) | complete diagonal and inverse tests | arbitrary `U(2)` blocks are allowed by the imported UCG theorem |
| the complex magnitude frame reuses the real-frame workspace | sequential clean composition | complex resource row | composition and workspace tests | leaf-phase derivatives remain a separate direct stream |
| complex magnitude size and depth match the real frontier | one phase UCG plus the real theorem | complex resource row | broad-grid tests | theorem is not a single-frame claim for all `2N-1` complex coordinates |

## 7. Quantum-backpropagation consequence

| Claim | Analytic support | Implementation | Tests | Boundary |
|---|---|---|---|---|
| frame-safe compilation preserves the complete global magnitude distribution | [QBP consequence, Section 4](QBP_CONSEQUENCE.md#4-frame-safe-substitution) | compiled frame interface | boundary and decoder tests | assumes exact frame safety and clean return |
| one outcome contributes to every magnitude coordinate | [QBP consequence, Section 3](QBP_CONSEQUENCE.md#3-one-outcome-contributes-to-every-magnitude-coordinate) | parity and FWHT decoders | decoder cross-checks | raw coordinate target |
| raw coordinatewise accuracy uses `O((1+log(n/delta))/epsilon_infinity^2)` executions | [QBP consequence, Section 5](QBP_CONSEQUENCE.md#5-accuracy-target-and-conditioning-boundary) | record norm and decoder | empirical and algebraic record checks | not a complete-vector, relative, normalized-frame, or natural-gradient bound |
| matched quantum-depth ratio is `O(log n)=O(log log M)` | [QBP consequence, Section 6](QBP_CONSEQUENCE.md#6-matched-scalar-and-gradient-programs) | state preparation, controlled observable, and compiled inverse frame | technical walkthrough | same general state family, access model, accuracy, and confidence; excludes output materialization |

## 8. External circuit results

The active imported source is P. Yuan and S. Zhang, *Quantum* **7**, 956
(2023):

| Imported statement | Use |
|---|---|
| Theorem 2 | optimal all-workspace QSP benchmark |
| Lemma 5 | exact ancilla-free multi-controlled `X` |
| Lemma 6 | all-workspace UCG size–depth tradeoff |
| Lemma 9 | coherent copy–use–uncopy |

The published article corresponds to arXiv v2. The imported statements were also
checked in v3. The earlier state-preparation paper remains the historical
predecessor and original-source citation for selected primitives.

## 9. What is not claimed

The repository does not claim:

- a generic `O(N)` compiler for arbitrary `N`-dimensional unitaries;
- a universal theorem for arbitrary coordinate frames;
- hardware-native or connectivity-aware depth;
- approximate Clifford+T complexity;
- noise-dependent execution guarantees;
- optimizer convergence;
- a generic construction for controlled nonunitary observables;
- novelty of UCGs, controlled-unitary square roots, borrowed qubits, or toggle
  detection.

The theorem is specific to the balanced Hopf differential frame and to the
exact circuit model stated above.

---

[← Documentation index](README.md) · [Complete compiler proof](COMPILER_THEOREM.md) · [Verification →](VERIFICATION.md)
