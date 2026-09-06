# Claim ledger

[← Verification](VERIFICATION.md) · [Complete narrative](../REVIEW.md) · [Source map →](SOURCE_MAP.md)

This ledger maps each material claim to its analytic basis, local executable
support, and scope boundary.  It is a navigation aid after the proof.

## Evidence notation

| Label | Meaning |
|---|---|
| analytic | dimension-independent proof supplied in the documentation |
| construction | complete local register or logical-gate schedule |
| imported | exact synthesis theorem used under its source hypotheses |
| finite check | independently built finite objects compared exactly or numerically |
| counterexample | explicit instance separating two compiler promises |
| ledger | integer or rational resource bookkeeping |
| internal reconstruction | separate proof pass within this project |

## 1. Geometry and compiler contract

| Claim | Basis | Executable support | Boundary |
|---|---|---|---|
| the balanced Hopf chart prepares arbitrary normalized real states | inherited chart theorem; [Hopf interface](HOPF_INTERFACE.md) | [`frames.py`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) | real state sphere |
| $\partial_{\theta_j}\lvert\psi\rangle=a_j\lvert e_j\rangle$ and $g_{j,j}=a_j^2$ | analytic recursive differential identity | incoming-amplitude, metric, and derivative checks | $a_j$ may be negative outside the canonical chart |
| on the canonical domains $a_j=\sqrt{g_{j,j}}$ | nonnegative ancestor factors | domain checks in [`test_frames.py`](../tests/test_frames.py) | the final real depth may use $[0,2\pi)$ because it does not enter ancestor weights |
| at zero metric weight the raw differential vanishes and the parameter tuple still selects a unit marker-frame continuation | analytic boundary consequence | singular and tolerance-aware regularity tests | continuation is not a normalized nonzero derivative |
| marker columns place the state and coordinate directions in one unitary frame | inherited frame interface | [`conventions.py`](../compiler_robust_hopf/conventions.py), frame tests | balanced Hopf chart |
| frame-safe compilation preserves the global QBP distribution | reducing-subspace proof in [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) | boundary fixtures and tests | requires complete clean-input equality |
| one state column is insufficient | exact two-qubit counterexample | [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py) | marker decoder held fixed |

## 2. Strict zero workspace

| Claim | Basis | Executable support | Boundary |
|---|---|---|---|
| the four-toggle half-angle echo equals one addressed nonfinal layer | analytic four-sector proof | every nonfinal depth through the documented test range | Hopf $R_y(\alpha)=e^{-i\alpha Y}$ convention |
| the original suffix bit is restored exactly | same complete-operator proof | sector and full-matrix checks | borrowed bit may be unknown and entangled |
| the construction uses no ancillary wire | explicit register count | strict-zero source and resource rows | borrowed bit remains logical data |
| each half-angle UCG has total width $d+2$ | participant count | layer-resource checks | $d$ prefix controls, one borrowed control, one target |
| the predicate toggle is ancilla free | imported MCT theorem plus negative-control wrappers | strict-zero ledger | exact all-to-all logical model |
| the complete strict-zero frame has $\Theta(N)$ size and $\Theta(n+N/n)$ depth | analytic sums plus real-state lower bound | exact-rational resource tests | asymptotic constants not optimized |

## 3. Positive workspace

| Claim | Basis | Executable support | Boundary |
|---|---|---|---|
| the first $t$ depths are a $t$-qubit frame conditioned on the external suffix being zero | complete-operator sector proof | all finite cuts in the test range | balanced addressed frame |
| the tail is a direct sum of subtree frames | prefix invariance and exact angle map | all finite cuts in the test range | complete operator, not state column |
| the binary–one-hot decoder realizes $\lvert x\rangle\lvert0\rangle\mapsto\lvert0\rangle\lvert e_x\rangle\lvert0\rangle$ | explicit X/CNOT/Toffoli construction | basis action, arbitrary-basis reversibility, layer disjointness, clean return | clean intended input for the forward encoding |
| decoder workspace is $3\cdot2^t-2-t$, depth $O(t)$, and size $O(2^t)$ | exact register and layer count | closed formulas and explicit schedule checks | fixed-width gates have constant elementary cost |
| the coherent router sends the suffix-token block to the prefix-selected branch | explicit CNOT/Fredkin construction | every clean basis input and arbitrary complex entangled inputs | all-to-all logical connectivity |
| copy and forward-Fredkin counts are $(2^t-1)(s+1)-t$ and $(2^t-1)(s+1)$ | exact schedule count | router schedule versus ledger | branch-block width $s+1$ |
| the cleared copy pool contains all simultaneous branch flags when $s\geq2$ | inequality $C-B=(B-1)s-t-1\geq0$ | register assertions and resource tests | $t\geq1$ |
| route–controlled-subframes–unroute equals the ideal tail | complete route and inverse proof | arbitrary complex-state and complete-cut checks | elementary UCG/MCT synthesis imported |
| data, tokens, copies, and flags return clean | explicit inverse schedule | zero-leakage and cleanup tests | clean workspace input |
| prefix and tail fit inside $2B(s+1)$ clean qubits | simultaneous live-register ledger | broad-grid workspace tests | sequential prefix and tail stages |
| the maximal feasible cut gives optimal depth, including $s=1$ | algebraic cut argument | exact integer diagnostics | proof threshold is asymptotic, not an optimized crossover |

## 4. Complete all-workspace theorem

| Claim | Basis | Executable support | Boundary |
|---|---|---|---|
| $m=0$ dispatches to the borrowed-suffix echo | explicit top-level schedule selection | unified/strict-zero ledger equality | complete real frame |
| every requested workspace budget is respected | simultaneous peak formula | broad $(n,m)$ grid | clean-ancillary model |
| the real frame has $\Theta(N)$ size for every $m\geq0$ | three upper-bound schedules and parameter lower bound | both ledgers | exact logical circuit |
| the real frame has $\Theta\!\left(n+\frac{N}{n+m}\right)$ depth for every $m\geq0$ | three schedules, parameter capacity, and output light cones | integer and rational diagnostics | all-to-all logical depth |
| the arbitrary leaf-phase diagonal is one exact total-width-$`n`$ UCG | block decomposition | complete diagonal matrices and inverse | arbitrary one-qubit blocks allowed |
| real frame and phase diagonal reuse one workspace pool | clean sequential composition | complex resource rows | both blocks return the pool to zero |
| the phase-dressed complex magnitude frame has the same frontier | real theorem plus phase UCG | complex frame matrices and resource ledgers | leaf-phase derivatives use a separate direct stream |

## 5. Quantum-backpropagation consequence

| Claim | Basis | Executable support | Boundary |
|---|---|---|---|
| one magnitude outcome contributes to every magnitude coordinate | inherited parity-record identity | parity and FWHT decoder checks | phase-calibrated controlled Hermitian-unitary observable |
| fixed raw-coordinate $\ell_\infty$ accuracy needs $O\!\left((1+\log(n/\delta))/\varepsilon^2\right)$ magnitude executions | inherited fixed-norm concentration theorem | deterministic record-norm checks | absolute raw-coordinate target |
| other gradient outputs have different conditioning | output-task analysis | [QBP consequence](QBP_CONSEQUENCE.md) | may depend on dimension, gradient norm, or metric weights |
| materialized decoding costs $O\!\left(S+N\min\{S,n\}\right)$ | minimum of record-wise and histogram/FWHT routes | decoder-route equality tests | output length is $\Theta(N)$ |
| frame-safe compilation adds no asymptotic per-execution depth factor | all-workspace frame theorem and substitution lemma | walkthrough and complete suite | matched general-family programs |
| fixed-accuracy matched overhead is $O(\log n)=O(\log\log M)$ | execution count and constant per-execution depth ratio | [QBP consequence](QBP_CONSEQUENCE.md) | same state family, observable access, and accuracy convention; output materialization excluded |

## 6. Sources and claim boundary

The active exact compiler framework and comparison benchmark is P. Yuan and S.
Zhang, *Quantum* **7**, 956 (2023).  The proof uses the published v2 statements,
checked against arXiv v3, for optimal QSP, ancilla-free multi-controlled X,
all-workspace UCG synthesis, and coherent copy–uncopy.

The preceding state-preparation paper is retained as the historical predecessor
and original source of selected primitives.  The Hopf chart and differential
geometry are inherited from the first Hopf work; the global, direct-phase,
checkpoint, and statistical interfaces are inherited from `Hopf-QBP`.

The repository does not claim the invention of UCGs, controlled-unitary roots,
borrowed qubits, conditional cleanliness, toggle detection, or reversible
routing.  The new statements are the Hopf-specific complete-operator
factorizations and schedules that attain the all-workspace frontier.

## 7. Internal reconstructions

| Record | Purpose |
|---|---|
| [consolidated proof audit](PROOF_AUDIT.md) | operator, register, workspace, and asymptotic reconstruction |
| [strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | order, phase, hidden workspace, endpoints, and sums |
| [clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem re-derived from the target operator and imported compiler toolkit |

## 8. Reproduction

```bash
python -m pip install -r requirements.txt
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```

---

[← Verification](VERIFICATION.md) · [Complete narrative](../REVIEW.md) · [Source map →](SOURCE_MAP.md)
