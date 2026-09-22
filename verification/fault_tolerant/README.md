# Fault-tolerant compiler verification

This directory contains the bounded, reproducible evidence supporting the shared
capped-geometric source and lowering-shift construction (research checkpoint
CP28). All decisions use exact integer/Fraction arithmetic in
$\mathbb{Q}(\sqrt{2},i)$. The tests are finite evidence for the analytic compiler argument;
they are not an implementation of the complete fault-tolerant compiler.

## Reproduce

Python **3.10 or newer** is sufficient. There are no third-party dependencies,
network calls, solver installations, or references to an external research tree.
From the repository root:

```bash
python -B scripts/verify_fault_tolerant.py
```

The runner executes all four suites in a temporary directory, checks their
receipts, and removes generated output when finished. To retain fresh receipts:

```bash
python -B scripts/verify_fault_tolerant.py --output-dir verification/fault_tolerant/results
```

Both commands work from any current directory when the runner is addressed by
its absolute path. A relative `--output-dir` is resolved from the caller's
working directory. Each suite also accepts `--output /path/to/receipt.json`.
Standalone defaults write to `results/`, which is ignored by Git. The full run
normally takes about a minute on a workstation; the default limit is 300 seconds
per suite and can be changed with `--timeout`.

## What the suites establish

| Suite | Exact finite evidence | Boundary of the evidence |
| --- | --- | --- |
| `gray_geometric_checks.py` | Applies the emitted logical Gray-chain gate words at widths `t=1..5`, covering 124 initialized-scratch data/enable columns. Checks the positive capped source, actual inverse, scratch return, five coherent reference witnesses, two structural negative controls, and emitted gate-count recurrences. Separately checks every column of a two-T controlled-H decomposition. | Scratch starts clean. CCX gates are simulated as exact logical permutations; the entire source circuit is not compiled to Clifford+T. The asymptotic recurrence solution and seven-T Toffoli substitution remain analytic. The unconditional Gray decoder is checked only in the enable-one state-preparation wrapper. |
| `shift_kernel_checks.py` | Checks 1,360 shift-permutation inputs, 26 valid nonzero shift defects, 30 invalid-offset defects, 1,536 full local inverse columns, 24 accepted-block columns, and 16 streamed-product columns. Checks one initial source preparation and one final inverse. Six negative controls detect omitted failure flags/history or incorrect overflow handling. | Kernel fixtures use `M=4`, `Q=J=2`, `p=1/2`, and arbitrary digit tables, including `f_0=1`. They check the local algebra, not production `M=4J`, tightened residual coefficients, or emitted outer amplitude amplification. |
| `shift_resource_checks.py` | Checks 152 parameter choices, 589 stage scales, 4,712 coefficient-rounding cases and 4,712 certified interval-rounding cases. Also checks exact bit lengths, padded domains, finite rational sparse frames, and scalar error budgets. | These are resource **proxies and scalar inequalities**, not counts from emitted T/Clifford circuits. Sampled values do not prove all-size bounds, and sparse support does not imply a general frame T lower bound. |
| `geometric_reflection_checks.py` (supporting evidence) | Checks small source/reflection matrices and denominator formulas, 304 Pauli-transfer entries, 32 initialized/mixed helper coefficients, 1,312 algebraic norm-separation instances, and exact tail constants. Its exact matrix arithmetic also supports the kernel suite. | These CP25 fixtures support source-cost reasoning. They do not prove the general channel-lattice theorem, approximate synthesis bounds, or an additive lower bound for a sequence of operations. |

The all-size controlled-source recurrence, complete-work error propagation,
global normalization/amplification, arbitrary table synthesis with dirty
workspace, and the final mixed-memory compiler tradeoff require the analytic
arguments in the manuscript. Passing these checks alone does not prove those
claims. In particular, there is no end-to-end production-parameter circuit,
QASM artifact, or full compiler resource benchmark in this directory.

## Saved evidence and dependency closure

`expected/` preserves four historical research receipts byte for byte. The
runner compares **every parsed scientific JSON field** against those receipts,
including exact amplitudes, counts, negative controls, scope statements, and
all matrix digests. Only the top-level `source_sha256` and `helper_sha256`
provenance fields are excluded from this comparison because the source files
were relocated and adapted. Current generated source hashes are checked
independently. No timestamps, runtime measurements, or absolute output paths
participate in the scientific comparison.

`PROVENANCE.json` records the original file hashes, the imported source hashes,
the preserved receipt hashes, and the limited portability changes. It also pins
the exact source text of the two scalar classes extracted into
`exact_arithmetic.py`. The runner checks these hashes before and after execution
and refuses an output directory inside `expected/`. It also rejects output-file
symlinks and hard links before executing any suite.
It never has an option to regenerate the expected receipts.

The complete Python dependency closure is six files:

- `gray_geometric_checks.py` imports `gray_geometric.py` and `exact_arithmetic.py`.
- `shift_kernel_checks.py` imports `geometric_reflection_checks.py`.
- `shift_resource_checks.py` and `geometric_reflection_checks.py` use only the standard library.

`Q2` and `CQ2` were extracted verbatim from `boolean_frame_certificate.py` and
`residual_precision_correction.py`. Their unrelated frame certificates and
residual constructions are omitted. Float-based display methods survive only
to preserve the extracted classes; no verification decision calls them.
Historical checkpoint labels and the reference to `positive_support.md` inside
saved receipts identify the original research argument, not an additional
runtime dependency or an included all-size proof.

Fresh output includes `verification_summary.json` with elapsed times and current
source hashes. A failure in a suite, source-integrity check, or scientific
comparison makes the runner exit nonzero. The runner does not change root tests,
validation entry points, or CI configuration.
