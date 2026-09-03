# Verification and evidence

[← QBP consequence](QBP_CONSEQUENCE.md) · [Read the complete narrative](../REVIEW.md) · [Next: source map →](SOURCE_MAP.md)

The repository uses three distinct kinds of evidence:

1. dimension-independent analytic proofs;
2. exact finite-dimensional executable checks;
3. internal proof reviews that reconstruct the argument and audit its resource
   assumptions.

These layers are complementary. Finite matrix equality can expose an indexing,
sign, order, or workspace error, but it cannot prove an asymptotic theorem.
Conversely, a correct asymptotic argument does not guarantee that the reference
implementation follows the same conventions.

## 1. Analytic verification

The load-bearing mathematical statements are proved in the narrative and
compiler documents.

| Statement | Analytic basis |
|---|---|
| Hopf state and tangent-marker columns | recursive split-and-complement geometry |
| Addressed depth operator | exact prefix-selected rotation on the zero-suffix sector |
| State-column obstruction | explicit two-qubit unitary completion and observable |
| Strict-zero echo | complete four-sector operator identity |
| Borrowed-bit restoration | zero or four predicate toggles in every invariant sector |
| Conditioned-prefix identity | direct decomposition into the zero-suffix sector and its orthogonal complement |
| Tail direct sum | invariance of each fixed-prefix subspace |
| Binary–one-hot decoder | explicit reversible tree construction |
| Routed compiler | coherent route–operate–unroute on orthogonal prefix sectors |
| Workspace envelope | simultaneous register ledger and sequential workspace reuse |
| Upper bounds | UCG/MCT/copy primitives plus exact geometric sums |
| Lower bounds | real-state parameter dimension and output light cones |
| Complex corollary | one exact phase UCG composed sequentially with the real frame |
| QBP invariance | reducing clean-workspace subspace and exact inverse action |

The canonical proof route is:

- [Minimal Hopf interface](HOPF_INTERFACE.md)
- [Complete compiler theorem](COMPILER_THEOREM.md)
- [QBP consequence](QBP_CONSEQUENCE.md)

## 2. Exact finite-dimensional checks

The implementation constructs the two sides of each identity independently
where practical. It uses exact gate permutations or dense NumPy matrices and
compares them up to floating-point roundoff.

### Frame geometry

The tests compare:

- recursive real frames with independently composed addressed layers;
- real-frame orthogonality;
- separated complex-frame unitarity;
- state and normalized-tangent marker columns;
- common-phase and zero-amplitude complex-chart behavior.

Files:

- [Frame implementation](../compiler_robust_hopf/frames.py)
- [Frame tests](../tests/test_frames.py)
- [Complex geometry tests](../tests/test_complex_analysis.py)

### State-column and checkpoint boundaries

The two-qubit fixtures verify:

- identical prepared state columns;
- different complete frame actions;
- exact response-marker movement;
- the gradient corruption
  ```math
  (2,0,0)\longmapsto(0,\sqrt2,0);
  ```
- a checkpoint suffix that preserves one prepared state but flips a derivative;
- an active-interface-safe suffix that preserves the checkpoint mean while
  changing the complete output distribution.

Files:

- [Boundary constructions](../compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](../tests/test_compiler_boundaries.py)

### Strict-zero borrowed-suffix echo

The strict-zero suite checks:

- the identities `C^2=R_y(theta)` and `X C X=C^(-1)`;
- all four `(h,b)` sectors;
- exact restoration of the borrowed logical qubit;
- self-inverse predicate-toggle and target-echo permutations;
- every nonfinal addressed layer through `n=8`;
- complete real frames through `n=8`;
- inverse frames;
- separated complex frames;
- `n=1`, `d=0`, `d=n-2`, and final-depth endpoints.

Files:

- [Strict-zero construction](../compiler_robust_hopf/strict_zero_echo.py)
- [Operator tests](../tests/test_strict_zero_echo.py)
- [Exact-rational audit helpers](../compiler_robust_hopf/strict_zero_audit.py)
- [Audit tests](../tests/test_strict_zero_audit.py)

### Positive-workspace compiler

The positive-workspace suite checks:

- every tree cut through `n=8`;
- exact global-to-local angle partitioning;
- conditioned-prefix reconstruction;
- tail direct-sum reconstruction;
- binary–one-hot decoder reversibility on clean and arbitrary basis inputs;
- disjointness of every declared reversible layer;
- exact one-hot Givens action;
- route–subframe–unroute action on arbitrary complex inputs for small cases;
- zero workspace leakage;
- branch, token, control-copy, and flag counts;
- selected schedules over a broad grid of `n` and `m`.

Files:

- [Tree identities](../compiler_robust_hopf/tree_structure.py)
- [Tree decoder](../compiler_robust_hopf/tree_decoder.py)
- [Unified compiler ledger](../compiler_robust_hopf/unified_compiler.py)
- [Tree-decoder tests](../tests/test_tree_decoder.py)
- [Unified compiler tests](../tests/test_unified_compiler.py)

### Resource inequalities

The tests use integer or exact-rational arithmetic for the inequalities that
carry the asymptotic proof. They do not estimate slopes numerically.

Checked statements include:

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq 6\frac{2^n}{n},
```

```math
n^2=O(2^n/n),
```

```math
n^2
=O\left(\frac{2^n}{n+m}\right)
\quad (1\leq m<4n),
```

and, for the maximal routed cut,

```math
\frac{2^s}{s}
=O\left(\frac{2^n}{n+m}\right).
```

Files:

- [General resource diagnostics](../compiler_robust_hopf/resource_bounds.py)
- [Strict-zero exact sums](../compiler_robust_hopf/strict_zero_audit.py)
- [Resource tests](../tests/test_resource_bounds.py)
- [Strict-zero resource tests](../tests/test_strict_zero_audit.py)

### Gradient decoders

The decoder suite compares direct parity averages, dense Walsh transforms, and
fast Walsh–Hadamard decoding. It also checks direct complex phase records and
their deterministic norm-two property.

Files:

- [Decoders](../compiler_robust_hopf/decoders.py)
- [Decoder tests](../tests/test_decoders.py)

## 3. Internal proof reviews

The detailed review records remain visible because they document what was
re-derived, which assumptions were imported, and which corrections were made.
They are evidence about the checking process, not substitutes for the proof.

| Review record | Distinct role |
|---|---|
| [Consolidated proof audit](PROOF_AUDIT.md) | register accounting, all-workspace upper and lower bounds, complex composition |
| [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | chronological order, four sectors, endpoint cases, no hidden workspace |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem re-derived from operator definitions rather than construction chronology |
| [Strict-zero prior-art analysis](STRICT_ZERO_PRIOR_ART.md) | separates familiar ingredients from the narrow Hopf-specific claim |
| [Expanded search record](PRIOR_ART_SEARCH_2026_09.md) | broader technical search and explicit limits of a negative search result |

The audits consistently classify the result as internally supported but not yet
independently verified.

## 4. A short reviewer walkthrough

The quickest executable orientation is:

```bash
python scripts/reviewer_walkthrough.py
```

It checks, in order:

1. the canonical two-qubit frame identity;
2. the state-column obstruction;
3. the strict-zero four-sector identity;
4. borrowed-qubit restoration and layer equality;
5. the complex phase diagonal as one UCG;
6. schedule selection at representative workspace budgets;
7. the peak-workspace constraint;
8. the exact resource inequalities used by the proof.

The script prints one readable PASS/FAIL line per step and exits nonzero on any
failure. It is intended as an orientation tool, not as a proof certificate.

## 5. Complete reproduction

Use Python 3.11 or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the short walkthrough:

```bash
python scripts/reviewer_walkthrough.py
```

Run the complete deterministic suite:

```bash
python validate.py
```

Print the all-workspace ledger:

```bash
python scripts/unified_resource_ledger.py --n 12
```

Print the strict-zero layer ledger:

```bash
python scripts/strict_zero_echo_ledger.py --n 12
```

Check the recorded upstream versions without network access:

```bash
python scripts/check_upstream_sync.py --offline
```

## 6. Evidence limits

The repository does not use finite experiments to establish asymptotic
optimality. It also does not test:

- routed-device depth;
- a hardware-native gate set;
- approximate Clifford+T synthesis;
- noisy execution or readout mitigation;
- application-specific controlled-observable implementations;
- arbitrary non-Hopf differential frames.

A useful technical review should therefore distinguish three questions:

1. Are the Hopf operator identities correct?
2. Do the proposed circuits implement those operators within the stated
   workspace?
3. Do the imported synthesis bounds and the resource sums imply the displayed
   asymptotic frontier?

The repository is designed so that each question has a separate analytic and
executable counterpart.

---

[← QBP consequence](QBP_CONSEQUENCE.md) · [Read the complete narrative](../REVIEW.md) · [Next: source map →](SOURCE_MAP.md)
