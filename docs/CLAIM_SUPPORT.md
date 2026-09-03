# Claim support map

[← Verification](VERIFICATION.md) · [Complete narrative](../REVIEW.md) · [Source map →](SOURCE_MAP.md)

This page maps each material claim to its proof type, executable support, and
scope boundary. It is intended as a compact audit table after the main proof,
not as a substitute for reading the proof itself.

## Evidence classes

| Class | Meaning |
|---|---|
| **Algebraic proof** | dimension-independent identity proved in the documentation |
| **Explicit construction** | complete register or gate schedule supplied in the repository |
| **Imported theorem** | exact circuit result used under the hypotheses of its source |
| **Exact finite check** | independently built operators, records, or schedules compared numerically |
| **Explicit counterexample** | closed-form instance disproving a stronger compiler claim |
| **Exact term ledger** | integer or rational bookkeeping; not an asymptotic fit |
| **Internal audit** | a separate re-derivation within this project; not independent external review |

Finite checks are valuable because they can expose sign, ordering, marker, and
workspace errors. They do not prove statements for arbitrary `n`.

## 1. Hopf geometry and compiler contract

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| The balanced real Hopf chart prepares every normalized real state | inherited from the first Hopf paper; restated in [Minimal Hopf interface](HOPF_INTERFACE.md) | [`frames.py`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) | real state-vector sphere |
| Normalized tangent columns obey `partial_(theta_j)|psi> = sqrt(g_(j,j)) |e_j>` | inherited from the first Hopf paper | [`real_tree_data`](../compiler_robust_hopf/frames.py), complex tangent tests | regular coordinates; raw differential vanishes at zero metric weight |
| Computational markers place the state and normalized tangents in one unitary frame | inherited from Hopf-QBP and restated here | [`conventions.py`](../compiler_robust_hopf/conventions.py), [`frames.py`](../compiler_robust_hopf/frames.py) | balanced Hopf chart |
| Addressed and recursive real frames coincide | algebraic layer construction | exact matrices through finite sizes | all-size conclusion is analytic |
| A frame-safe implementation preserves the global QBP distribution | reducing-subspace proof in [`FRAME_SAFE_COMPILATION.md`](FRAME_SAFE_COMPILATION.md) | compiler-boundary tests | requires complete clean-input operator equality |
| State-column equality alone is insufficient | explicit two-qubit counterexample | [`compiler_boundaries.py`](../compiler_robust_hopf/compiler_boundaries.py), tests | decoder and marker convention held fixed |

## 2. Strict zero workspace

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| The four-toggle half-angle echo equals one nonfinal addressed layer | complete four-sector proof in [Compiler theorem](COMPILER_THEOREM.md) | every nonfinal depth through `n=8` | exact Hopf `R_y` convention |
| The original suffix qubit is restored exactly | same complete-operator proof | sector and full-matrix tests | qubit may be unknown and entangled |
| No ancillary wire is used | explicit register audit | source implementation and resource rows | borrowed wire remains logical system data |
| Each half-angle UCG has total width `d+2` | exact participant count | layer resource tests | `d` prefix controls, one borrowed control, one target |
| Predicate toggles require no ancillary qubit | Yuan–Zhang Lemma 5 plus negative-control wrappers | strict-zero ledger | exact all-to-all standard-circuit model |
| One nonfinal layer has size `O(2^d+n-d)` and depth `O(n+2^d/(d+2))` | Yuan–Zhang Lemmas 5–6 and direct summation | exact integer ledger | constants are not optimized |
| The strict-zero real frame has size `Theta(N)` and depth `Theta(n+N/n)` | upper-bound sums plus real-family parameter lower bound | exact-rational audit tests | internally audited theorem |
| The inverse has the same resources | adjoint of the exact circuit | inverse matrix tests | exact unitary model |

## 3. Positive workspace structure

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| The first `t` depths equal a `t`-qubit frame conditioned on a zero external suffix | complete-operator proof | every cut through `n=8` | balanced addressed frame |
| The tail below a cut is a direct sum of subtree frames | exact angle map and block proof | every cut through `n=8` | complete operator, not one column |
| The binary–one-hot decoder maps `|x>|0>` to `|0>|e_x>|0>` | explicit X/CNOT/Toffoli construction | basis permutation, inverse, and layer-disjointness tests | clean decoder input |
| Decoder workspace is `3·2^t-2-t`, depth is `O(t)`, and size is `O(2^t)` | exact register and gate-layer count | closed-form schedule checks | fixed-width Toffoli has constant cost |
| The conditioned prefix has depth `O(n)` and size `O(2^t+n-t)` | decoder, predicate, fanout, controlled Givens layers | identity and resource tests | decoder scratch reused sequentially |
| The coherent router is valid on entangled prefix–suffix input | controlled-permutation proof | small exact routed matrices | all-to-all logical connectivity |
| Prefix and routed tail fit inside `2B(s+1)` clean workspace | simultaneous register ledger | broad-grid workspace tests | `B=2^t`, `s=n-t` |
| Controlled subtree frames run in parallel | disjoint physical branch registers | resource rows and finite construction checks | requires the allocated branch registers |
| The maximal feasible cut gives optimal positive-workspace depth | algebraic cut inequality | exact integer diagnostics | asymptotic scheduling threshold, not a finite crossover claim |

## 4. All-workspace real and complex frames

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| The unified compiler selects the strict-zero echo at `m=0` | explicit dispatch | unified/strict-zero cross-check | top-level real frame |
| The requested workspace is never exceeded | simultaneous peak ledger | broad grid of `n,m` values | clean ancillary model |
| The real frame has `Theta(N)` size for every `m>=0` | strict-zero and positive-workspace upper bounds plus parameter lower bound | both resource ledgers | exact standard circuit |
| The real frame has `Theta(n+N/(n+m))` depth for every `m>=0` | three schedules plus matching lower bounds | term diagnostics | all-to-all logical depth |
| An arbitrary leaf-phase diagonal is one exact `n`-qubit UCG | direct block identity | complete diagonal matrices | arbitrary `U(2)` blocks allowed |
| The phase layer reuses the real-frame workspace | sequential clean composition | complex resource rows | both blocks return workspace to zero |
| The separated complex frame has the same all-workspace frontier | real theorem plus one phase UCG | complex matrices and ledgers | separated complex construction |

## 5. Quantum-backpropagation consequence

| Claim | Proof or source | Executable support | Boundary |
|---|---|---|---|
| One global magnitude outcome contributes to every magnitude coordinate | inherited Hopf-QBP record identity | decoder parity/FWHT tests | controlled Hermitian-unitary observable model |
| Fixed-accuracy magnitude executions scale as `O(log n)` | inherited fixed-norm concentration theorem | norm and decoder checks | simultaneous coordinatewise accuracy |
| Record-wise decoding costs `O(SN)` | direct character accumulation | record-wise/FWHT parity tests | materialized output has length `Theta(N)` |
| Histogram plus FWHT costs `O(S+Nn)` | standard FWHT count | dense/FWHT comparisons | alternative decoding route |
| Direct complex phase decoding costs `O(S+N)` | signed one-hot accumulation | phase-record tests | one global-phase redundancy |
| Frame-safe compilation adds no asymptotic per-execution depth factor | optimal frame compiler and substitution theorem | reviewer walkthrough and complete suite | matched exact logical cost model |
| Fixed-accuracy global magnitude overhead is `O(log n)=O(log log M)` | sample count plus constant per-execution compiler ratio | [QBP consequence](QBP_CONSEQUENCE.md) | controlled-observable cost must be charged consistently |

## 6. Source and contribution boundaries

The active compiler framework and optimal state-preparation benchmark are Yuan
and Zhang, *Quantum* **7**, 956 (2023). The earlier Sun et al. paper is retained
as the historical predecessor. Möttönen/Bergholm, controlled-unitary roots, and
borrowed or conditionally clean workspace are credited in
[Related work](RELATED_WORK.md).

The repository does not claim invention of UCGs, borrowed qubits, toggle
detection, or square-root/conjugation identities. The narrow strict-zero
contribution is the Hopf-specific reduction of one addressed depth to two
width-`d+2` UCGs using a restored logical suffix qubit, together with the
resulting optimal complete-frame resource theorem.

Detailed search methodology and any negative search observations are confined
to the supporting prior-art records. They are not premises of the theorem.

## 7. Internal review records

| Record | Purpose |
|---|---|
| [Consolidated proof audit](PROOF_AUDIT.md) | register, operator, and asymptotic reconstruction of the full compiler |
| [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | chronological order, sector phases, hidden-workspace, endpoint, and summation checks |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem rederived from the operator target and imported primitives rather than construction chronology |

These records make the internal checking process visible. They do not replace
independent technical review.

## 8. Reproduction

```bash
python -m pip install -r requirements.txt
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```

The short walkthrough is an orientation tool. The full suite and ledgers are
described in [Verification and evidence](VERIFICATION.md).

---

[← Verification](VERIFICATION.md) · [Complete narrative](../REVIEW.md) · [Source map →](SOURCE_MAP.md)
