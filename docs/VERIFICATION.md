# Verification and evidence

[← QBP consequence](QBP_CONSEQUENCE.md) · [Read the complete narrative](../REVIEW.md) · [Next: source map →](SOURCE_MAP.md)

The repository uses three complementary evidence layers:

1. dimension-independent analytic proofs;
2. exact finite-dimensional executable checks;
3. internal proof reviews that reconstruct the argument and audit its resource
   assumptions.

Finite matrix equality can expose an indexing, sign, order, phase, or workspace
error, but cannot prove an asymptotic theorem. Conversely, a correct asymptotic
argument does not guarantee that the reference implementation follows the same
conventions. This page states exactly which objects are implemented and at what
level.

## 1. Implementation levels

| Component | Local representation | What is tested | External ingredient |
|---|---|---|---|
| Hopf state, frame, and addressed layers | dense NumPy matrices built by independent recursions | complete operator equality, orthogonality, marker columns, canonical-domain and singular-coordinate behavior | Hopf chart identities inherited from the earlier papers |
| Strict-zero borrowed-suffix echo | dense logical gate matrices and exact reversible permutations | four sectors, complete addressed layers, complete frames, inverse, complex magnitude composition, zero hidden workspace | elementary UCG and multi-controlled-X resource bounds from Yuan–Zhang |
| Binary–one-hot prefix decoder | explicit X/CNOT/Toffoli layers | basis action, arbitrary-basis reversibility, layer disjointness, exact clean return, one-hot Givens action | constant-size standard decompositions of Toffoli and controlled one-qubit gates |
| Coherent branch router | explicit CNOT-fanout and Fredkin layers plus sparse complex-state simulation | basis routing, arbitrary prefix–suffix-entangled inputs, token location, copy cleanup, branch-flag cleanup, route–operate–unroute, complete routed cut | coherent-copy depth and elementary controlled-gate decompositions |
| Controlled subtree frames | exact logical token/flag-controlled rotations in the router simulator | equality to the ideal tail direct sum and clean flag return | UCG and multi-controlled-X synthesis bounds from Yuan–Zhang |
| Leaf-phase diagonal | exact block-diagonal UCG matrix | equality to the complete diagonal, inverse, common phase, complex magnitude-frame composition | UCG size–depth theorem from Yuan–Zhang |
| Resource theorem | integer and exact-rational ledgers | workspace peaks, endpoint dispatch, geometric sums, cut inequalities, lower-bound diagnostics | published asymptotic primitive bounds |
| QBP decoder | direct parity, signed histogram, and fast Walsh–Hadamard implementations | agreement of decoding routes, empirical means, fixed record norms | global and phase-record identities inherited from `Hopf-QBP` |

The repository does not locally reproduce the complete elementary Yuan–Zhang
UCG or multi-controlled-X compiler. It imports those exact synthesis theorems
under their stated all-to-all arbitrary-one-qubit+CNOT model. Toffoli, Fredkin,
and controlled one-qubit gates used in explicit reversible schedules have
constant-size and constant-depth decompositions in that same model, so replacing
them by elementary gates changes only constants.

## 2. Analytic verification

| Statement | Dimension-independent basis |
|---|---|
| Hopf state and marker columns | recursive split-and-complement geometry |
| Oriented differential identity | `partial_(theta_j)|psi> = a_j|e_j>`, with `g_(j,j)=a_j^2` |
| Canonical geometric notation | canonical angle domains imply `a_j>=0` and `a_j=sqrt(g_(j,j))` |
| Singular-coordinate boundary | `a_j=0` makes the raw differential vanish while the unit marker column remains a frame continuation |
| Addressed depth operator | exact prefix-selected rotation on the zero-suffix sector |
| State-column obstruction | explicit two-qubit unitary completion and observable |
| Strict-zero echo | complete four-sector operator identity |
| Borrowed-bit restoration | zero or four predicate toggles in each invariant sector |
| Conditioned-prefix identity | direct decomposition into the zero-external-suffix sector and its orthogonal complement |
| Tail direct sum | invariance of every fixed-prefix subspace |
| Binary–one-hot decoder | explicit reversible tree construction |
| Coherent router | copied-prefix Fredkin tree acting as a permutation on orthogonal prefix sectors |
| Routed tail | route, token-controlled subtree frames, and inverse route equal the tail direct sum |
| Workspace envelope | simultaneous live-register ledger and sequential reuse |
| Upper bounds | UCG/MCT/copy primitives plus geometric sums |
| Lower bounds | real-state parameter dimension and output light cones |
| Complex magnitude corollary | one exact phase UCG composed with the real frame |
| QBP invariance | reducing clean-workspace subspace and exact inverse action |
| Matched runtime comparison | same preparation and controlled observable, plus one optimal-order inverse frame |

The canonical proof route is:

- [Minimal Hopf interface](HOPF_INTERFACE.md)
- [Complete compiler theorem](COMPILER_THEOREM.md)
- [QBP consequence](QBP_CONSEQUENCE.md)

## 3. Exact finite-dimensional checks

### 3.1 Frame geometry and coordinate domains

The frame tests compare recursive and addressed-layer constructions and verify:

- real-frame orthogonality;
- phase-dressed complex magnitude-frame unitarity;
- state and marker columns;
- `g_(j,j)=a_j^2` for unrestricted angles;
- `a_j=sqrt(g_(j,j))` on the canonical domains;
- a singular coordinate with zero raw derivative and a unit marker-column
  continuation;
- common-phase and zero-amplitude complex-chart behavior.

Files:

- [Frame implementation](../compiler_robust_hopf/frames.py)
- [Frame tests](../tests/test_frames.py)
- [Complex geometry tests](../tests/test_complex_analysis.py)

### 3.2 Compiler-contract boundaries

The two-qubit fixtures verify:

- identical prepared state columns;
- different complete frame actions;
- exact response-marker movement;
- gradient corruption
  ```math
  (2,0,0)\longmapsto(0,\sqrt2,0);
  ```
- a checkpoint suffix that preserves one prepared state but flips a derivative;
- an active-interface-safe suffix that preserves the checkpoint mean while
  changing the complete output distribution.

Files:

- [Boundary constructions](../compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](../tests/test_compiler_boundaries.py)

### 3.3 Strict-zero borrowed-suffix echo

The strict-zero suite checks:

- `C^2=R_y(theta)` and `XCX=C^(-1)`;
- all four `(h,b)` sectors;
- exact restoration of the borrowed logical qubit;
- self-inverse predicate-toggle and target-echo permutations;
- every nonfinal addressed layer through `n=8`;
- complete real frames through `n=8`;
- inverse frames and phase-dressed complex magnitude frames;
- `n=1`, `d=0`, `d=n-2`, and final-depth endpoints.

Files:

- [Strict-zero construction](../compiler_robust_hopf/strict_zero_echo.py)
- [Operator tests](../tests/test_strict_zero_echo.py)
- [Exact-rational audit helpers](../compiler_robust_hopf/strict_zero_audit.py)
- [Audit tests](../tests/test_strict_zero_audit.py)

### 3.4 Binary–one-hot prefix decoder

The explicit decoder tests cover:

- clean binary labels mapped to one-hot labels and back;
- reversibility on arbitrary computational-basis contents;
- exact layer disjointness and gate counts;
- the closed workspace formula `3*2^t-2-t`;
- exact one-hot Givens action for the prefix Hopf frame.

Files:

- [Decoder schedule](../compiler_robust_hopf/tree_decoder.py)
- [Decoder tests](../tests/test_tree_decoder.py)

### 3.5 Coherent route–operate–unroute

The routed construction is now represented explicitly rather than only by an
ideal direct-sum matrix. Tests cover:

- the allocated branch-data, token, copy, and reusable-flag registers;
- balanced prefix-bit fanout and exact uncopy;
- disjoint Fredkin layers at every routing level;
- every clean basis input routed to the prefix-selected branch;
- route followed by inverse route on arbitrary complex inputs whose prefix and
  suffix are entangled;
- token-controlled subtree-frame action on all branches;
- exact branch-flag and copy-pool cleanup before inverse routing;
- equality of the complete routed tail to
  ```math
  \bigoplus_r W_s^{(r)};
  ```
- equality of the complete routed cut to the direct Hopf frame;
- zero probability outside the clean-workspace subspace.

The simulator loops over disjoint branches for convenience; the declared
circuit schedule executes them in parallel because their data, token, and flag
registers are disjoint.

Files:

- [Explicit router and sparse-state simulator](../compiler_robust_hopf/router.py)
- [Router operator tests](../tests/test_router.py)
- [Tree identities](../compiler_robust_hopf/tree_structure.py)
- [All-workspace resource selection](../compiler_robust_hopf/unified_compiler.py)

### 3.6 Resource inequalities

The tests use integer or exact-rational arithmetic rather than numerical slope
fitting. Checked statements include

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

The explicit router schedule is also cross-checked against the resource ledger:

```math
\text{copy wires}=(2^t-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(2^t-1)(s+1).
```

Files:

- [General resource diagnostics](../compiler_robust_hopf/resource_bounds.py)
- [Strict-zero exact sums](../compiler_robust_hopf/strict_zero_audit.py)
- [Router schedule ledger](../compiler_robust_hopf/router.py)
- [Resource tests](../tests/test_resource_bounds.py)
- [Router resource tests](../tests/test_router.py)

### 3.7 Gradient decoders

The decoder suite compares direct parity averages, dense Walsh transforms, and
fast Walsh–Hadamard decoding. It also checks direct complex phase records and
their deterministic norm-two property.

Files:

- [Decoders](../compiler_robust_hopf/decoders.py)
- [Decoder tests](../tests/test_decoders.py)

## 4. Internal proof reviews

The detailed review records remain visible because they document what was
re-derived, which assumptions were imported, and which corrections were made.
They are evidence about the checking process, not substitutes for the proof.

| Review record | Distinct role |
|---|---|
| [Consolidated proof audit](PROOF_AUDIT.md) | register accounting, all-workspace upper and lower bounds, complex magnitude composition |
| [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | chronological order, four sectors, endpoints, and hidden-workspace check |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem re-derived from operator definitions rather than development chronology |
| [Strict-zero prior-art analysis](STRICT_ZERO_PRIOR_ART.md) | familiar ingredients versus the narrow Hopf-specific claim |
| [Expanded search record](PRIOR_ART_SEARCH_2026_09.md) | broader technical search and explicit limits of negative-search evidence |

The peer-review revision additionally introduced an explicit router, canonical
chart-domain tests, oriented incoming-amplitude notation, and a matched-program
QBP cost definition in response to an adversarial repository-wide audit.

## 5. Short walkthrough and complete reproduction

Use Python 3.11 or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the readable orientation:

```bash
python scripts/reviewer_walkthrough.py
```

Run the complete deterministic suite:

```bash
python validate.py
```

Print the all-workspace and strict-zero ledgers:

```bash
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

Check recorded upstream versions without network access:

```bash
python scripts/check_upstream_sync.py --offline
```

The walkthrough is an orientation tool, not a proof certificate.

## 6. Evidence limits

The repository does not use finite experiments to establish asymptotic
optimality. It also does not test:

- routed-device connectivity;
- a hardware-native gate set;
- approximate Clifford+T synthesis;
- noisy execution or readout mitigation;
- application-specific controlled-observable implementations;
- arbitrary non-Hopf differential frames.

A technical review should distinguish:

1. whether the Hopf operator identities are correct;
2. whether the proposed logical circuits implement those operators within the
   stated workspace;
3. whether the imported synthesis bounds and resource sums imply the displayed
   asymptotic frontier;
4. whether the QBP consequence uses the same output task, state family, and
   controlled-observable cost on both sides of its matched comparison.

---

[← QBP consequence](QBP_CONSEQUENCE.md) · [Read the complete narrative](../REVIEW.md) · [Next: source map →](SOURCE_MAP.md)
