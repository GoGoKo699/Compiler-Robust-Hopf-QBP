# Claim support map

[← Verification](VERIFICATION.md) · [Complete narrative](../REVIEW.md) · [Source map →](SOURCE_MAP.md)

This page maps each material claim to its proof type, executable support, and
scope boundary. It is an audit table after the main proof, not a substitute for
the proof itself.

## Evidence classes

| Class | Meaning |
|---|---|
| **Algebraic proof** | dimension-independent identity proved in the documentation |
| **Explicit construction** | complete register or logical-gate schedule supplied locally |
| **Imported theorem** | exact circuit result used under the hypotheses of its source |
| **Exact finite check** | independently built operators, records, or schedules compared numerically |
| **Explicit counterexample** | closed-form instance disproving a stronger compiler claim |
| **Exact term ledger** | integer or rational bookkeeping, not an asymptotic fit |
| **Internal audit** | separate re-derivation within this project, not external review |

## 1. Hopf geometry and compiler contract

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| The balanced real Hopf chart prepares every normalized real state | inherited from the first Hopf paper; restated in [Minimal Hopf interface](HOPF_INTERFACE.md) | [`frames.py`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) | real state-vector sphere |
| Unrestricted-angle differential is `partial_(theta_j)|psi>=a_j|e_j>` with `g_(j,j)=a_j^2` | recursive Hopf differential identity | `incoming_amplitude`, `metric`, and derivative tests | `a_j` is oriented and may be negative outside the canonical chart |
| On the canonical domains `a_j=sqrt(g_(j,j))` | nonnegative ancestor sine/cosine factors | domain masks and canonical-domain tests | real final-depth angles may lie in `[0,2pi)` because they do not enter ancestor weights |
| At `g_(j,j)=0`, the raw differential vanishes while the unit marker column remains a frame continuation | direct consequence of the differential identity | singular-coordinate test | continuation is not normalization of a nonzero derivative |
| Computational markers place the state and all continuation vectors in one unitary frame | inherited from Hopf-QBP and restated here | [`conventions.py`](../compiler_robust_hopf/conventions.py), [`frames.py`](../compiler_robust_hopf/frames.py) | balanced Hopf chart |
| A frame-safe implementation preserves the global QBP distribution | reducing-subspace proof in [`FRAME_SAFE_COMPILATION.md`](FRAME_SAFE_COMPILATION.md) | compiler-boundary tests | requires complete clean-input operator equality |
| State-column equality alone is insufficient | explicit two-qubit counterexample | [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py), tests | marker decoder held fixed |

## 2. Strict zero workspace

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| The four-toggle half-angle echo equals one nonfinal addressed layer | complete four-sector proof in [Compiler theorem](COMPILER_THEOREM.md) | every nonfinal depth through `n=8` | exact Hopf `R_y` convention |
| The original suffix qubit is restored exactly | same complete-operator proof | sector and full-matrix tests | borrowed qubit may be unknown and entangled |
| No ancillary wire is used | explicit register audit | source implementation and resource rows | borrowed wire remains logical system data |
| Each half-angle UCG has total width `d+2` | exact participant count | layer resource tests | `d` prefix controls, one borrowed control, one target |
| Predicate toggles require no ancillary qubit | Yuan–Zhang Lemma 5 plus negative-control wrappers | strict-zero ledger | exact all-to-all standard-circuit model |
| Strict-zero real frame has `Theta(N)` size and `Theta(n+N/n)` depth | upper-bound sums plus real-family parameter lower bound | exact-rational audit tests | constants not optimized |

## 3. Positive-workspace construction

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| First `t` depths equal a `t`-qubit frame conditioned on a zero external suffix | complete-operator proof | every cut through finite test range | balanced addressed frame |
| Tail below a cut is a direct sum of subtree frames | exact angle map and invariant-subspace proof | every cut through finite test range | complete operator, not one column |
| Binary–one-hot decoder maps `|x>|0>` to `|0>|e_x>|0>` | explicit X/CNOT/Toffoli construction | basis permutation, inverse, and layer-disjointness tests | clean decoder input |
| Decoder workspace is `3*2^t-2-t`, depth `O(t)`, size `O(2^t)` | exact register and layer count | closed-form and explicit schedule checks | fixed-width gates have constant elementary cost |
| Coherent router sends suffix and token to the prefix-selected branch | explicit CNOT-fanout/Fredkin construction | every basis input and arbitrary complex entangled inputs | all-to-all logical connectivity |
| Prefix-copy count is `(2^t-1)(s+1)-t` and forward Fredkin count is `(2^t-1)(s+1)` | exact schedule count | explicit schedule versus resource-ledger tests | branch block width `s+1` |
| Token-controlled subtree frames equal the ideal tail direct sum | route–operate–unroute proof | arbitrary complex-state and complete-cut tests | UCG/MCT elementary synthesis imported |
| Copies, branch flags, tokens, and extra data return clean | inverse-route construction | zero-leakage and cleanup tests | clean workspace input |
| Prefix and tail fit inside `2B(s+1)` clean workspace | simultaneous live-register ledger | explicit router ledger and broad-grid tests | `B=2^t`, `s=n-t` |
| Maximal feasible cut gives optimal positive-workspace depth | algebraic cut inequality | exact integer diagnostics | asymptotic threshold, not finite crossover |

## 4. All-workspace real and complex magnitude frames

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| Unified compiler selects strict-zero echo at `m=0` | explicit dispatch | unified/strict-zero ledger equality | top-level real frame |
| Requested workspace is never exceeded | simultaneous peak ledger | broad grid of `n,m` values | clean ancillary model |
| Real frame has `Theta(N)` size for every `m>=0` | three upper-bound schedules plus parameter lower bound | both ledgers | exact standard circuit |
| Real frame has `Theta(n+N/(n+m))` depth for every `m>=0` | three schedules plus matching lower bounds | integer diagnostics | all-to-all logical depth |
| Arbitrary leaf-phase diagonal is one exact `n`-qubit UCG | direct block identity | complete diagonal matrices | arbitrary `U(2)` blocks allowed |
| Phase layer reuses real-frame workspace | sequential clean composition | complex resource rows | both blocks return workspace zero |
| Phase-dressed complex magnitude frame has the same frontier | real theorem plus one phase UCG | magnitude-frame matrices and ledgers | leaf-phase derivatives use a separate direct stream |

## 5. Quantum-backpropagation consequence

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| One global magnitude outcome contributes to every magnitude coordinate | inherited Hopf-QBP record identity | decoder parity/FWHT tests | phase-calibrated controlled Hermitian-unitary observable |
| Fixed raw-coordinate `l_infinity` accuracy uses `O((1+log(n/delta))/epsilon^2)` magnitude executions | inherited fixed-norm concentration theorem | norm and decoder checks | absolute raw coordinate target |
| Complete-vector, relative, frame, and natural-gradient targets differ | inherited task-boundary analysis from current Hopf-QBP | local [QBP consequence](QBP_CONSEQUENCE.md) | conditioning may depend on gradient norm or metric weights |
| Best documented materialized decoder costs `O(S+N min{S,n})` | minimum of record-wise and signed-histogram/FWHT routes | direct/FWHT parity tests | output length is `Theta(N)` |
| Frame-safe compilation adds no asymptotic per-execution depth factor | optimal frame compiler and substitution theorem | walkthrough and complete suite | matched general-family logical programs |
| Matched fixed-accuracy overhead is `O(log n)=O(log log M)` | sample count and constant per-execution depth ratio | [QBP consequence](QBP_CONSEQUENCE.md) | same preparation, controlled observable, and accuracy convention; output materialization excluded |

## 6. Source version and contribution boundaries

The active compiler framework and QSP benchmark are Yuan and Zhang, *Quantum*
**7**, 956 (2023). The published article is arXiv v2; Theorem 2 and Lemmas 5, 6,
and 9 were checked in v3 and retain the statements used here. The earlier Sun
et al. paper is the historical predecessor.

The current `Hopf-QBP/main` baseline is
`faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582`. Its statistical and output-task
clarifications were reviewed and reflected locally; exact reconciliation is in
[`SYNC.md`](../SYNC.md).

The repository does not claim invention of UCGs, borrowed qubits, toggle
detection, or square-root/conjugation identities. The narrow strict-zero
contribution is the Hopf-specific reduction of one addressed depth to two
width-`d+2` UCGs using a restored logical suffix qubit, together with the
resulting optimal complete-frame theorem.

## 7. Internal review records

| Record | Purpose |
|---|---|
| [Consolidated proof audit](PROOF_AUDIT.md) | register, operator, and asymptotic reconstruction |
| [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | order, phases, hidden workspace, endpoints, and sums |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem rederived from the target operator and imported primitives |

These records document internal checking. They do not replace independent
technical review.

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
