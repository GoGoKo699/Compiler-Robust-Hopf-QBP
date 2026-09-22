# Validation suite

[← Repository landing page](../README.md) · [Verification map](../docs/VERIFICATION.md) · [Implementation map](../compiler_robust_hopf/README.md)

The tests are organized around the proof interfaces rather than around one
particular circuit library.  They are designed to expose convention, operator,
workspace, and asymptotic-accounting errors.

Finite tests support the analytic proof; they do not establish the asymptotic
theorem by numerical extrapolation.

## Test groups

| Test file | Principal questions |
|---|---|
| [`test_frames.py`](test_frames.py) | Do the recursive and addressed constructions give the same frame? Are marker columns, chart domains, metric weights, and singular continuations consistent? |
| [`test_complex_analysis.py`](test_complex_analysis.py) | Do magnitude and leaf-phase differentials, gauge relations, and zero-amplitude behavior match the frame convention? |
| [`test_compiler_boundaries.py`](test_compiler_boundaries.py) | State-only failure, sharp all-observable sensitivity, common phases, leakage, singular markers, and checkpoint interfaces |
| [`test_strict_zero_echo.py`](test_strict_zero_echo.py) | Does the four-sector echo implement every addressed layer, restore the borrowed data bit, and compose to the complete frame? |
| [`test_strict_zero_audit.py`](test_strict_zero_audit.py) | Do the strict-zero size, depth, and lower-bound inequalities hold in exact arithmetic? |
| [`test_tree_decoder.py`](test_tree_decoder.py) | Is the binary–one-hot decoder a reversible permutation with disjoint layers, exact counts, and the intended code-space frame action? |
| [`test_router.py`](test_router.py) | Does the explicit CNOT/Fredkin router work on entangled complex inputs and return data, tokens, copies, and flags clean? |
| [`test_unified_compiler.py`](test_unified_compiler.py) | Does schedule selection cover every workspace budget and does the phase diagonal equal one exact UCG? |
| [`test_resource_bounds.py`](test_resource_bounds.py) | Do the low-workspace absorption, maximal-cut, workspace-envelope, and lower-bound diagnostics hold? |
| [`test_decoders.py`](test_decoders.py) | Do direct parity, histogram, Walsh–Hadamard, and direct phase-record decoders agree? |
| [`test_approximation_contract.py`](test_approximation_contract.py) | Actual-adjoint bias, complex phase records, reflection sums, finite weights, and conditional means with correlated dirty reuse |
| [`test_operator_source_compiler.py`](test_operator_source_compiler.py) | Native two-clean frame composition, optimal source words and witnesses, dirty echoes/banks, and literal U(2) multiplexor phases |
| [`test_provenance.py`](test_provenance.py) | Are upstream commits, source roles, and local lineage recorded consistently? |
| [`test_literature_policy.py`](test_literature_policy.py) | Does the active proof use one compiler framework and maintain the declared contribution boundary? |
| [`test_reviewer_narrative.py`](test_reviewer_narrative.py) | Do the primary reading route, diagrams, links, terminology, and source-version statements remain coherent? |
| [`test_math_typography.py`](test_math_typography.py) | Do notation, quantifiers, adjoints, and mathematical prose retain their intended meaning? |
| [`test_hyphen_inline_math.py`](test_hyphen_inline_math.py) | Does inline mathematics next to a word hyphen use the protected GitHub syntax? |
| [`test_presentation.py`](test_presentation.py) | Does the presentation checker detect damaged math handoffs, diagram overflow, overlapping labels, and obscured connectors? |

## Highest-leverage operator checks

The following checks are especially useful when modifying the scientific code:

1. recursive frame equals addressed-layer frame;
2. state-equivalent completion changes the two-qubit decoded gradient;
3. each strict-zero echo layer equals the corresponding addressed layer;
4. route followed by inverse route is identity on arbitrary complex inputs;
5. routed tail equals the exact subtree direct sum;
6. complete routed cut equals the direct frame;
7. exact-compiler work registers return to their promised inputs;
8. one-UCG phase blocks reproduce the complete leaf-phase diagonal;
9. two-clean operator-source blocks satisfy full-output error bounds, including
   core return, while lookup banks and suffix controls return exactly;
10. actual inverse circuits and sequential composition retain their bounds
    after intermediate leakage.

All exact-frame, resource, QBP, and two-clean compiler checks are retained.
Exploratory endpoint investigations are preserved in repository history;
finite checks for those excluded constructions are outside this suite.

## Run the suite

```bash
python validate.py
```

The validation entry point prints the Python and NumPy versions and executes the
complete unittest collection. The standalone exact receipt suites are run
separately with `python scripts/verify_fault_tolerant.py`.

The shorter orientation is:

```bash
python scripts/reviewer_walkthrough.py
```

The [verification map](../docs/VERIFICATION.md) explains which statements are
proved analytically, represented as explicit schedules, imported from the
compiler literature, or checked only in finite dimensions.
