# Proof and executable correspondence

[← QBP consequence](QBP_CONSEQUENCE.md) · [Complete narrative](../REVIEW.md) · [Source map →](SOURCE_MAP.md)

The repository uses executable checks to test the conventions and constructions
that are easiest to get wrong: column labels, chronological order, relative
phases, coherent routing, work-register cleanup, and simultaneous resource
peaks.  The asymptotic theorem itself is established analytically.

## 1. Evidence levels

| Level | Meaning in this repository |
|---|---|
| analytic proof | a dimension-independent operator or resource argument |
| explicit construction | a complete reversible or logical-gate schedule is supplied |
| imported exact synthesis | an elementary compiler theorem is used under its stated model |
| finite regression check | independently constructed matrices, states, schedules, or ledgers are compared |
| internal reconstruction | the proof is re-derived separately to search for hidden assumptions |

These levels are kept distinct.  A matrix test does not prove an asymptotic
bound, and an asymptotic bound does not certify an implementation's bit order.

The [constant-clean progress report](../research/CONSTANT_CLEAN_PROGRESS.md)
links the new [operator-source proof](../research/constant_clean/OPERATOR_SOURCE_COMPILER.md)
and its [finite circuit checks](../tests/test_operator_source_compiler.py).
These test the native geometric operator, its programmable scalar block,
the two-flag rotation, coherent amplification, dirty word-bank routing, the
restored suffix echo, and literal phase-diagonal composition on arbitrary dirty
inputs. The [graph-source reuse checks](../tests/test_operator_source_reuse.py)
separately test Pauli support, exact acceptance arithmetic and code leakage.
The analytic proof establishes the improved upper bound; finite matrices test
its fragile identities and conventions.

The earlier [structural checks](../tests/test_constant_clean_structure.py) cover
Pauli restrictions, full program-space echoes, Fourier-rank witnesses, dirty
modular echoes, and phase-bank reductions. Separate suites cover
[masked phase batching](../tests/test_identical_phase_batching.py) and
[the coherent modular adder](../tests/test_modular_lookup_compiler.py).
All are included in `python validate.py`. The arbitrary-angle tensor-batch
hypothesis remains unproved; the new frame compiler uses an addressed operator
construction instead.

## 2. What is represented locally

| Component | Local representation | Principal executable check | Imported ingredient |
|---|---|---|---|
| Hopf states and frames | dense matrices from independent recursive and addressed-layer constructions | complete equality, orthogonality, state and marker columns, chart domains, singular coordinates | Hopf geometry inherited from the earlier work |
| strict-zero echo | dense logical gates and exact reversible permutations | all four sectors, every nonfinal depth, full frames, inverse, and complex composition | UCG and ancilla-free MCT resource theorems |
| binary–one-hot decoder | explicit X/CNOT/Toffoli layers | basis action, arbitrary-basis reversibility, disjoint layers, counts, and clean return | constant-cost elementary decompositions |
| coherent router | explicit CNOT-fanout and Fredkin layers with sparse complex-state simulation | basis routing, entangled inputs, tail direct sum, complete cut, and zero leakage | coherent copy and constant-cost controlled gates |
| controlled subtree frames | exact logical token/flag-controlled rotations | equality to the ideal block-diagonal tail and flag cleanup | UCG and MCT synthesis |
| leaf-phase diagonal | exact block-diagonal UCG matrix | complete diagonal, inverse, common phase, and complex magnitude composition | UCG synthesis |
| resource theorem | integer and exact-rational ledgers | workspace peaks, schedule dispatch, endpoints, geometric sums, and cut inequalities | asymptotic primitive bounds |
| gradient records | parity, signed-histogram, and fast Walsh–Hadamard decoders | agreement of routes, empirical means, and deterministic record norms | QBP record identities |

The repository does not reproduce the elementary UCG or multi-controlled-X
compiler.  Those exact results are imported from the all-workspace
state-preparation framework.  Toffoli, Fredkin, controlled one-qubit gates, and
fixed-width controlled Givens rotations have exact constant-size,
constant-depth decompositions in the declared arbitrary-one-qubit+CNOT model.

## 3. Geometry and compiler contract

The frame suite checks:

- equality of the recursive and addressed-layer frames;
- real-frame orthogonality;
- phase-dressed complex magnitude-frame unitarity;
- the breadth-first marker convention;
- $g_{j,j}=a_j^2$ for unrestricted angles;
- $a_j=\sqrt{g_{j,j}}$ on the canonical domains;
- tolerance-aware regularity at floating-point chart boundaries;
- zero raw derivative and a unit chart-selected marker continuation at a
  singular coordinate.

The compiler-boundary fixtures check:

- two unitaries with the same prepared state but different marker columns;
- the resulting gradient change
  ```math
  (2,0,0)\longmapsto(0,\sqrt2,0);
  ```
- a checkpoint suffix that preserves one state but changes a derivative;
- an active-interface-safe suffix that preserves designated means without
  preserving the complete distribution.

Files:

- [frame implementation](../compiler_robust_hopf/frames.py)
- [frame tests](../tests/test_frames.py)
- [complex geometry tests](../tests/test_complex_analysis.py)
- [compiler-boundary implementation](../compiler_robust_hopf/compiler_boundaries.py)
- [compiler-boundary tests](../tests/test_compiler_boundaries.py)

## 4. Strict-zero construction

The strict-zero suite checks:

1. $C^2=R_y(\theta)$ and $XCX=C^{-1}$;
2. all four $(h,b)$ sectors;
3. exact restoration of the borrowed logical suffix bit;
4. absence of hidden workspace;
5. every nonfinal addressed depth through $n=8$;
6. complete real frames through $n=8$;
7. inverse frames and phase-dressed complex magnitude frames;
8. the endpoints $n=1$, $d=0$, $d=n-2$, and the final depth.

The resource audit checks, using exact arithmetic,

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq6\frac{2^n}{n}
```

and the absorption of the polynomial predicate terms into $O(2^n/n)$.

Files:

- [strict-zero construction](../compiler_robust_hopf/strict_zero_echo.py)
- [operator tests](../tests/test_strict_zero_echo.py)
- [exact-rational resource audit](../compiler_robust_hopf/strict_zero_audit.py)
- [resource-audit tests](../tests/test_strict_zero_audit.py)

## 5. Binary–one-hot prefix decoder

The decoder is tested as a complete reversible permutation, not only on its
intended clean input.  The suite verifies:

- $\lvert x\rangle\lvert0\rangle$ maps to $\lvert0\rangle\lvert e_x\rangle\lvert0\rangle$ and returns under the inverse;
- arbitrary computational-basis contents return after forward and inverse;
- every declared layer has disjoint wire support;
- the exact workspace formula
  ```math
  3\,2^t-2-t;
  ```
- the exact gate and depth formulas;
- the one-hot Givens network equals the complete prefix Hopf frame on the code.

Files:

- [decoder schedule](../compiler_robust_hopf/tree_decoder.py)
- [decoder tests](../tests/test_tree_decoder.py)

## 6. Coherent route–operate–unroute

The router is supplied as an explicit schedule.  The tests cover:

- branch-data, token, copy, and reusable-flag register allocation;
- balanced prefix fanout and exact uncopy;
- disjoint Fredkin layers;
- every clean basis input routed to its prefix-selected branch;
- forward route followed by inverse route on arbitrary complex inputs;
- prefix–suffix-entangled inputs;
- token-controlled action of all subtree frames;
- cleanup of every branch flag before inverse routing;
- equality to
  ```math
  \bigoplus_r W_s^{(r)};
  ```
- equality of the complete routed cut to the direct Hopf frame;
- zero probability outside the clean-workspace subspace.

The explicit schedule is cross-checked against

```math
\text{copy wires}=(2^t-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(2^t-1)(s+1).
```

The simulator iterates over branches for convenience.  The circuit-depth claim
uses the declared parallel schedule: branch data, tokens, flags, and subtree
frames have disjoint physical support.

Files:

- [router and sparse-state simulator](../compiler_robust_hopf/router.py)
- [router operator tests](../tests/test_router.py)
- [tree identities](../compiler_robust_hopf/tree_structure.py)

## 7. Resource theorem

The ledgers use integer or exact-rational checks rather than fitted slopes.  They
cover:

- strict zero workspace;
- the one-clean-flag endpoint;
- the direct-to-routed transition;
- maximal feasible cuts over broad $n,m$ grids;
- copy-pool reuse as branch flags;
- the $s=1$ routed endpoint;
- arbitrarily large workspace;
- matching real-state parameter and light-cone lower bounds.

Representative checked implications are

```math
n^2
=O\left(\frac{2^n}{n+m}\right)
\qquad(1\leq m<4n),
```

and

```math
\frac{2^s}{s}
=O\left(\frac{2^n}{n+m}\right)
```

for the maximal routed cut.

Files:

- [all-workspace resource selection](../compiler_robust_hopf/unified_compiler.py)
- [resource diagnostics](../compiler_robust_hopf/resource_bounds.py)
- [general resource tests](../tests/test_resource_bounds.py)
- [unified compiler tests](../tests/test_unified_compiler.py)

## 8. Gradient records

The decoder suite compares:

- direct record-wise parity averages;
- dense Walsh transforms;
- the fast Walsh–Hadamard implementation;
- direct phase-stream signed one-hot records.

It verifies the deterministic norm-two record property used by the
coordinatewise concentration statement.

Files:

- [decoders](../compiler_robust_hopf/decoders.py)
- [decoder tests](../tests/test_decoders.py)

## 9. Internal reconstructions

The proof has been re-derived in three complementary ways.

| Record | Distinct role |
|---|---|
| [consolidated proof audit](PROOF_AUDIT.md) | operator, register, workspace, upper-bound, and lower-bound reconstruction |
| [strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | chronological order, phases, hidden workspace, endpoints, and sums |
| [clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem re-derived from the target operator and imported compiler results |

The [claim support map](CLAIM_SUPPORT.md) provides the corresponding
claim-by-claim ledger.  These documents record internal checking; independent
technical judgment remains separate.

## 10. Reproduce the checks

Use Python 3.11 or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the short orientation:

```bash
python scripts/reviewer_walkthrough.py
```

Run the complete deterministic suite:

```bash
python validate.py
```

Print the two resource ledgers:

```bash
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

Check the recorded upstream versions without network access:

```bash
python scripts/check_upstream_sync.py --offline
```

## 11. Evidence boundary

The repository does not use finite experiments to establish asymptotic
optimality.  It also does not test:

- device connectivity or routing overhead;
- a hardware-native gate set;
- a general elementary-gate emitter for the full asymptotic Clifford+T compiler;
- noisy execution or readout mitigation;
- application-specific controlled-observable implementations;
- arbitrary non-Hopf differential frames.

The proof should be assessed in four separate steps:

1. the Hopf operator identities;
2. the logical circuits and workspace cleanup;
3. the imported synthesis bounds and resource sums;
4. the matched QBP output and access conventions.

---

[← QBP consequence](QBP_CONSEQUENCE.md) · [Complete narrative](../REVIEW.md) · [Source map →](SOURCE_MAP.md)

## 12. Fault-tolerant evidence and approximate QBP

The [fault-tolerant theorem](FAULT_TOLERANT_COMPILER.md) separates the analytic
resource proof from the [focused finite checks](../verification/fault_tolerant/README.md).
Run `python scripts/verify_fault_tolerant.py` from the repository root. Four
stdlib-only suites reproduce the retained exact Gray-source, shift-kernel,
resource, and reflection receipts without changing their saved reference files.
The runner identifies nondeterministic provenance fields separately from
scientific output.

The shift fixtures test complete finite kernel columns, actual inverses, source
defects, failure tracking, and negative controls. They do not instantiate all
production parameters or an elementary emitter of the full asymptotic circuit.
The resource suite checks rational scales and ledgers; those rows are not
measured gate counts. The source-specific receipt map states each boundary.

The [approximation bridge](QBP_APPROXIMATION.md) has tests for full-input error,
actual-adjoint transfer, leakage, reference-entangled borrowed inputs, and
bounded estimator bias. These validate the finite examples behind the general
proof, not differentiation of a synthesized family.
