# Implementation map

[← Repository landing page](../README.md) · [Complete technical narrative](../REVIEW.md) · [Verification map](../docs/VERIFICATION.md)

The Python package follows the same order as the proof.  It contains reference
operators, explicit reversible schedules, resource ledgers, and decoder checks.
It is not a hardware backend.

## 1. Geometric target

| Module | Role |
|---|---|
| [`conventions.py`](conventions.py) | breadth-first tree indices, computational markers, and bit conventions |
| [`frames.py`](frames.py) | real states, oriented incoming amplitudes, metric weights, marker frames, addressed layers, and complex phase dressing |
| [`complex_analysis.py`](complex_analysis.py) | magnitude and leaf-phase differentials, gradients, gauge checks, and zero-amplitude behavior |

Two independent constructions of the real frame are maintained:

1. recursive tree states and complements;
2. the product of addressed complete-operator layers.

Their equality is a central convention check.

## 2. Compiler-contract boundaries

| Module | Role |
|---|---|
| [`compiler_boundaries.py`](compiler_boundaries.py) | exact two-qubit examples separating state-column, checkpoint-interface, and complete-frame promises |

These fixtures are deliberately small enough to inspect as complete matrices
and output distributions.

## 3. Strict zero workspace

| Module | Role |
|---|---|
| [`strict_zero_echo.py`](strict_zero_echo.py) | borrowed-suffix half-angle echo, full layer and frame operators, and strict-zero resource rows |
| [`strict_zero_audit.py`](strict_zero_audit.py) | exact-rational summation and lower-bound diagnostics |

The borrowed suffix qubit is logical data.  It is not counted as an ancillary
wire and is restored exactly on every input.

## 4. Positive workspace

| Module | Role |
|---|---|
| [`tree_structure.py`](tree_structure.py) | conditioned-prefix identity, subtree angle map, and tail direct sum |
| [`tree_decoder.py`](tree_decoder.py) | explicit clean binary–one-hot decoder and encoded prefix-frame schedule |
| [`router.py`](router.py) | explicit CNOT/Fredkin route–controlled-subframes–unroute schedule and sparse complex-state simulator |
| [`unified_compiler.py`](unified_compiler.py) | schedule selection, workspace peaks, depth/size proxies, and the one-UCG phase diagonal |
| [`resource_bounds.py`](resource_bounds.py) | integer forms of the cut, absorption, and lower-bound inequalities |

The decoder and router are supplied as explicit reversible layers.  The
underlying elementary UCG and multi-controlled-X synthesis theorems are imported
from the all-workspace state-preparation framework.

## 5. Gradient records

| Module | Role |
|---|---|
| [`decoders.py`](decoders.py) | direct parity records, signed histograms, fast Walsh–Hadamard decoding, and direct phase-stream records |

The decoder module concerns the output of the logical QBP circuit.  It is
separate from the frame compiler so that quantum execution count, circuit depth,
and classical materialization remain distinct.

## 6. Public entry points

The package root re-exports the principal reference objects and resource rows.
For a first inspection, the most useful functions are:

```python
from compiler_robust_hopf import (
    real_frame_matrix,
    direct_real_frame,
    strict_zero_echo_real_frame,
    unified_real_frame_resource_row,
    routed_tail_residual,
)
```

- `real_frame_matrix(theta)` constructs the frame recursively.
- `direct_real_frame(n, theta)` constructs it from addressed layers.
- `strict_zero_echo_real_frame(n, theta)` constructs the ancilla-free frame.
- `unified_real_frame_resource_row(n, m)` selects the schedule and reports its
  resource terms.
- `routed_tail_residual(...)` compares the explicit coherent router with the
  ideal tail direct sum on a supplied state.

## 7. Interpretation of resource rows

Resource dataclasses expose transparent integer proxies for the terms used in
the asymptotic proof.  They are not claimed to be optimized finite elementary-
gate counts.

The declared logical model is exact, all-to-all, and based on arbitrary
one-qubit gates plus CNOTs.  Toffoli, Fredkin, controlled one-qubit gates, and
fixed-width controlled Givens rotations are readable constant-width primitives.

## 8. Run the checks

```bash
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

See the [verification map](../docs/VERIFICATION.md) for the evidence level and
test coverage of each module.
