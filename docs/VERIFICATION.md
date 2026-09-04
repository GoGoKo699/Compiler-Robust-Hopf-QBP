# Verification and evidence

[← Compiler theorem](COMPILER_THEOREM.md) · [Complete technical note](../REVIEW.md) · [Next: source map →](SOURCE_MAP.md)

The repository uses three evidence layers:

1. dimension-independent analytic proofs;
2. explicit circuit schedules and exact finite-dimensional checks;
3. independent internal reconstructions of the full argument.

These layers answer different questions. A finite matrix comparison can expose
an indexing, sign, ordering, phase, or cleanup error. It cannot prove an
asymptotic theorem. Conversely, an asymptotic proof does not guarantee that the
reference implementation follows the same conventions. The evidence map below
keeps those roles separate.

## 1. Compact technical walkthrough

The fastest executable route follows the proof order:

```bash
python scripts/technical_walkthrough.py
```

It checks:

1. recursive and addressed two-qubit frames agree;
2. canonical metric weights and singular frame directions are interpreted
   consistently;
3. one correct state column does not guarantee valid marker decoding;
4. the strict-zero four-sector echo is exact;
5. the borrowed logical suffix bit is restored;
6. the explicit router acts correctly on an entangled complex input;
7. the arbitrary phase diagonal is one UCG;
8. the correct schedule is selected at representative workspace budgets;
9. the peak workspace respects the requested budget;
10. the low-workspace and maximal-cut inequalities hold.

The walkthrough is an orientation tool, not a proof certificate.

## 2. Implementation levels

| Component | Local representation | What is checked | Imported ingredient |
|---|---|---|---|
| Hopf state, frame, and addressed layers | independent dense NumPy constructions | complete operator equality, orthogonality, markers, domains, and singular-coordinate behavior | Hopf chart identities |
| Strict-zero echo | dense logical gate matrices and reversible permutations | four sectors, addressed layers, complete frames, inverse, complex composition, and hidden-workspace boundary | UCG and multi-controlled-`X` resource theorems |
| Binary–one-hot decoder | explicit X/CNOT/Toffoli layers | clean basis action, arbitrary-basis reversibility, layer disjointness, gate counts, and exact return | constant-width elementary decompositions |
| Coherent router | explicit CNOT fanout and Fredkin layers plus sparse complex-state simulation | basis routing, entangled inputs, token location, copy cleanup, branch-flag cleanup, route–operate–unroute, and complete routed cuts | coherent copy and constant-width controlled gates |
| Controlled subtree frames | exact token/flag-controlled logical block action | equality to the ideal tail direct sum and clean flag return | UCG and multi-controlled-`X` synthesis bounds |
| Leaf-phase layer | exact block-diagonal UCG matrix | complete diagonal, inverse, common phase, and complex magnitude-frame composition | UCG synthesis theorem |
| Resource frontier | integer and exact-rational ledgers | workspace peaks, endpoints, geometric sums, cut inequalities, and lower-bound diagnostics | published primitive bounds |
| QBP decoder | direct parity, signed histogram, and fast Walsh–Hadamard implementations | agreement of decoding routes, empirical means, and fixed record norms | inherited global and direct-phase record identities |

The repository does not regenerate the complete elementary Yuan–Zhang UCG or
multi-controlled-`X` circuits. It imports those exact synthesis theorems in the
arbitrary-one-qubit+CNOT model. Toffoli, Fredkin, controlled one-qubit, and
fixed-width controlled Givens gates in the explicit schedules have exact
constant-size, constant-depth decompositions in the same model.

## 3. Analytic proof map

| Statement | Dimension-independent basis |
|---|---|
| state and marker columns | recursive split-and-complement geometry |
| differential identity | `partial_(theta_j)|psi> = a_j|e_j>` and `g_(j,j)=a_j^2` |
| canonical positive weight | canonical angle domains imply `a_j>=0` |
| singular-coordinate boundary | `a_j=0` gives a zero raw differential and a chart-selected frame direction |
| addressed layer | prefix-selected rotation on exactly the zero-suffix sector |
| state-column obstruction | explicit two-qubit completion and observable |
| strict-zero echo | complete four-sector operator identity |
| borrowed-bit restoration | zero or four predicate toggles in each invariant sector |
| conditioned prefix | decomposition into zero external suffix and its complement |
| tail direct sum | invariance of every fixed-prefix subspace |
| binary–one-hot decoder | explicit reversible tree construction |
| coherent router | copied-prefix Fredkin tree as a permutation on orthogonal prefix sectors |
| routed tail | route, token-controlled subtree frames, and inverse route equal the direct sum |
| workspace envelope | simultaneous live-register count and sequential reuse |
| upper bounds | imported UCG/MCT/copy primitives plus geometric sums |
| lower bounds | real-state parameter dimension and output light cones |
| complex magnitude frame | one exact phase UCG composed with the real frame |
| QBP invariance | reducing clean-workspace subspace and exact inverse action |
| matched runtime comparison | same state family and controlled observable, plus one optimal-order inverse frame |

The canonical proof route is:

- [Minimal Hopf interface](HOPF_INTERFACE.md)
- [Complete compiler theorem](COMPILER_THEOREM.md)
- [QBP consequence](QBP_CONSEQUENCE.md)

## 4. Exact finite checks

### 4.1 Frame geometry

The frame tests verify:

- recursive and addressed-layer constructions agree;
- the real frame is orthogonal;
- the phase-dressed complex magnitude frame is unitary;
- state and marker columns follow the declared convention;
- `g_(j,j)=a_j^2` for unrestricted angles;
- `a_j=sqrt(g_(j,j))` on the canonical domains;
- singular raw differentials vanish while the marker direction remains unit;
- the public regular-coordinate mask is tolerance-aware.

Files:

- [Frame implementation](../compiler_robust_hopf/frames.py)
- [Frame tests](../tests/test_frames.py)
- [Complex geometry tests](../tests/test_complex_analysis.py)

### 4.2 Compiler-contract boundaries

The two-qubit fixtures verify:

- equal preparation columns;
- unequal complete frames;
- response movement between marker columns;
- the gradient corruption
  ```math
  (2,0,0)\longmapsto(0,\sqrt2,0);
  ```
- a checkpoint suffix that preserves one state but changes a derivative;
- an active-interface-safe suffix that preserves the decoded mean without
  preserving the full output distribution.

Files:

- [Boundary constructions](../compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](../tests/test_compiler_boundaries.py)

### 4.3 Strict-zero echo

The strict-zero suite checks:

- `C^2=R_y(theta)` and `XCX=C^(-1)`;
- all four predicate/borrowed-bit sectors;
- exact restoration of the logical borrowed bit;
- self-inverse predicate and echo permutations;
- every nonfinal addressed layer through `n=8`;
- complete real frames through `n=8`;
- inverse frames and phase-dressed complex magnitude frames;
- `n=1`, `d=0`, `d=n-2`, and final-depth endpoints.

Files:

- [Strict-zero construction](../compiler_robust_hopf/strict_zero_echo.py)
- [Operator tests](../tests/test_strict_zero_echo.py)
- [Exact-rational audit helpers](../compiler_robust_hopf/strict_zero_audit.py)
- [Audit tests](../tests/test_strict_zero_audit.py)

### 4.4 Binary–one-hot decoder

The decoder tests cover:

- clean binary labels mapped to one-hot labels and back;
- reversibility on arbitrary computational-basis contents;
- exact layer disjointness and gate counts;
- the workspace formula `3*2^t-2-t`;
- the one-hot Givens action for the complete prefix frame.

Files:

- [Decoder schedule](../compiler_robust_hopf/tree_decoder.py)
- [Decoder tests](../tests/test_tree_decoder.py)

### 4.5 Coherent route–operate–unroute

The routed tests cover:

- the data, token, copy, and reusable-flag register layout;
- balanced prefix fanout and exact uncopy;
- disjoint Fredkin layers at every routing level;
- every clean basis input routed to the selected branch;
- route followed by inverse route on arbitrary complex inputs whose prefix and
  suffix are entangled;
- token-controlled subtree action on all branches;
- branch-flag and copy-pool cleanup;
- equality to
  ```math
  \bigoplus_r W_s^{(r)};
  ```
- equality of the complete routed cut to the direct Hopf frame;
- zero probability outside the clean-workspace subspace.

The simulator loops over disjoint branches for convenience. The declared
circuit schedule runs them in parallel because their data, token, and flag
registers are disjoint.

Files:

- [Router and sparse-state simulator](../compiler_robust_hopf/router.py)
- [Router tests](../tests/test_router.py)
- [Tree identities](../compiler_robust_hopf/tree_structure.py)
- [Resource selection](../compiler_robust_hopf/unified_compiler.py)

### 4.6 Resource inequalities

The resource tests use integer or exact-rational arithmetic rather than fitted
slopes. They check, among other statements,

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq6\frac{2^n}{n},
```

```math
n^2=O(2^n/n),
```

```math
n^2=O\left(\frac{2^n}{n+m}\right)
\quad(1\leq m<4n),
```

and the maximal-cut implication

```math
\frac{2^s}{s}
=O\left(\frac{2^n}{n+m}\right).
```

The router schedule is cross-checked against

```math
\text{copy wires}=(2^t-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(2^t-1)(s+1).
```

Files:

- [General resource diagnostics](../compiler_robust_hopf/resource_bounds.py)
- [Strict-zero exact sums](../compiler_robust_hopf/strict_zero_audit.py)
- [Router ledger](../compiler_robust_hopf/router.py)
- [Resource tests](../tests/test_resource_bounds.py)
- [Unified compiler tests](../tests/test_unified_compiler.py)

### 4.7 Gradient decoders

The decoder suite compares direct parity averages, dense Walsh transforms, and
fast Walsh–Hadamard decoding. It also checks the direct complex phase records
and their deterministic norm-two property.

Files:

- [Decoders](../compiler_robust_hopf/decoders.py)
- [Decoder tests](../tests/test_decoders.py)

## 5. Independent internal reconstructions

The internal records remain visible because they document what was rederived
and which failure modes were considered.

| Record | Distinct role |
|---|---|
| [Consolidated proof audit](PROOF_AUDIT.md) | full register accounting, upper and lower bounds, and complex composition |
| [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | chronological order, four sectors, endpoints, and hidden-workspace check |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem rebuilt from the operator target and imported primitives |
| [Strict-zero prior-art analysis](STRICT_ZERO_PRIOR_ART.md) | familiar ingredients versus the narrow Hopf-specific contribution |
| [Expanded source search](PRIOR_ART_SEARCH_2026_09.md) | search scope and explicit limits of negative-search evidence |

These records support the checking process. The proof itself is in
[the compiler theorem](COMPILER_THEOREM.md).

## 6. Reproduction

Use Python 3.11 or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/technical_walkthrough.py
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```

## 7. Evidence limits

The repository does not use finite experiments to establish asymptotic
optimality. It also does not test:

- routed hardware connectivity;
- hardware-native gate scheduling;
- approximate Clifford+T synthesis;
- noisy execution or readout mitigation;
- application-specific controlled-observable implementations;
- arbitrary non-Hopf differential frames.

A complete assessment separates four questions:

1. are the Hopf operator identities correct?
2. do the logical schedules implement those operators and restore their
   workspace?
3. do the imported primitive bounds and resource sums imply the displayed
   frontier?
4. does the QBP consequence compare the same state family, output task, access
   model, and accuracy convention on both sides?

---

[← Compiler theorem](COMPILER_THEOREM.md) · [Complete technical note](../REVIEW.md) · [Next: source map →](SOURCE_MAP.md)
