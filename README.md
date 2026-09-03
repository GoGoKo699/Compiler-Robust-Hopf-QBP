# Compiler-Robust Hopf Quantum Backpropagation

Exact differential-frame compilation, compiler boundaries, and end-to-end
resource accounting for Hopf-coordinate quantum backpropagation.

## Main theorem candidate

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits available to the
compiler. The complete real Hopf differential frame and the separated complex
frame admit exact frame-safe implementations with

```math
\boxed{
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The circuit uses at most the requested `m` clean ancillary qubits and returns
them to zero. Thus coherent access to the complete Hopf differential frame has
the same asymptotic size--depth frontier as optimal arbitrary state preparation
in the exact Yuan--Zhang circuit model.

This result has passed multiple internal proof audits and deterministic
validation. It has not received independent external proof review.

## One active compiler framework

The sole active external compiler framework and optimal state-preparation
benchmark are:

> P. Yuan and S. Zhang, "Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits," *Quantum* **7**, 956 (2023).

The proof uses their Theorem 2 and Lemmas 5, 6, and 9. It does not choose between
two published state-preparation compilers as a function of the workspace.

The earlier work of Sun, Tian, Yang, Yuan, and Zhang remains cited as the
historical predecessor and as the original source credited for selected
primitives. Möttönen and Bergholm provide the earlier uniformly controlled-gate
lineage. See [`docs/RELATED_WORK.md`](docs/RELATED_WORK.md).

## Why a frame compiler is needed

Ordinary state preparation requires only

```math
U_{\mathrm{prep}}|0^n\rangle=|\psi\rangle.
```

Global Hopf backpropagation requires the stronger clean operator contract

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input `|varphi>`. Exact two-qubit counterexamples in this
repository show that a compiler can preserve the prepared Hopf state while
permuting tangent-marker columns and returning the wrong gradient.

The positive result is therefore not a generic consequence of state
preparation. It comes from the structured Hopf frame and a compiler that
preserves its complete action.

## Unified compiler architecture

The active compiler has three internal schedules.

### 1. Strict-zero borrowed-suffix echo (`m=0`)

At a nonfinal Hopf depth `d`, borrow one original suffix data qubit `b`, let
`h(r)` test whether the remaining suffix `r` is zero, and set

```math
C_p=R_y(\theta_p/2).
```

The chronological echo

```text
controlled-X
T_h
controlled-C_p
T_h
controlled-X
T_h
controlled-C_p
T_h
```

uses no ancillary wire. Here `T_h` toggles the borrowed bit iff `r=0`. The
identities

```math
C_p^2=R_y(\theta_p),
\qquad
X C_p X=C_p^{-1}
```

make the unwanted borrowed-bit sector cancel while the original full-suffix-zero
sector receives the desired rotation. The borrowed qubit is restored exactly on
all inputs.

Each nonfinal layer uses two zero-ancilla UCGs of total width `d+2`, four
zero-ancilla predicate toggles, and two CNOT echoes. Summing the layers gives
size `O(N)` and depth `O(n+N/n)`.

The abstract square-root/conjugation and borrowed-bit ideas have close prior
art. The project-specific contribution is their Hopf-layer aggregation and the
resulting optimal strict-zero complete-frame frontier. See
[`docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md`](docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md),
[`docs/STRICT_ZERO_ECHO_AUDIT.md`](docs/STRICT_ZERO_ECHO_AUDIT.md), and
[`docs/STRICT_ZERO_PRIOR_ART.md`](docs/STRICT_ZERO_PRIOR_ART.md).

### 2. Direct flagged-UCG schedule (small positive workspace)

For a nonfinal addressed depth, compute the lower-suffix-zero predicate into one
clean flag, apply one prefix-and-flag Yuan--Zhang UCG, and uncompute the flag.
For `1<=m<4n`, the polynomial sequential term is absorbed by the
state-preparation scale, so this schedule already has optimal asymptotic depth.

### 3. Tree-cut routed schedule (larger workspace)

Cut the addressed frame after `t` depths and write

```math
B=2^t,
\qquad
s=n-t.
```

The exact operator factorization is

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

with

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right)
```

and

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A self-contained reversible binary--one-hot decoder realizes the conditioned
prefix. A coherent router moves the existing suffix to the branch selected by
the prefix, all controlled subtree frames run on disjoint registers in
parallel, and inverse routing returns every auxiliary register to zero.
Choosing the largest feasible cut gives depth

```math
O\left(n+\frac{N}{n+m}\right).
```

### Complex frame

The leaf-phase diagonal is exactly one additional `n`-qubit UCG:

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\operatorname{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

It reuses the real-frame workspace pool sequentially, including at `m=0`.

## Consequence for quantum backpropagation

The balanced Hopf chart supplies orthogonal coordinate tangents, metric weights,
computational markers, and bounded shared gradient records. A frame-safe
compiler transports that differential interface without changing the global
measurement distribution.

At fixed simultaneous coordinatewise accuracy and confidence, the global
magnitude stream uses

```math
O(\log n)=O(\log\log M)
```

executions for `M=Theta(N)` Hopf coordinates. Since one forward or inverse frame
matches the optimal state-preparation depth for every `m>=0`, compilation adds
no asymptotic factor to this execution overhead. The direct complex phase stream
uses no inverse frame.

The quantum and classical accounting is in
[`docs/END_TO_END_QBP.md`](docs/END_TO_END_QBP.md).

## Compiler correctness hierarchy

| Compiler promise | Scalar state | Checkpoint means | Global Hopf distribution |
|---|---:|---:|---:|
| One prepared state column | sufficient | insufficient | insufficient |
| Complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| Complete frame-safe operator | sufficient | sufficient where applicable | sufficient |

For checkpoint factorization `U=B_dA_d`, the sufficient interface contract is

```math
\widetilde B_dJP_d=e^{i\chi}JB_dP_d.
```

It preserves the designated checkpoint means but need not preserve the complete
output distribution. See
[`docs/COMPILER_BOUNDARIES.md`](docs/COMPILER_BOUNDARIES.md).

## Start here

- [`docs/THEOREM_OVERVIEW.md`](docs/THEOREM_OVERVIEW.md): theorem chain;
- [`docs/UNIFIED_YUAN_ZHANG_COMPILER.md`](docs/UNIFIED_YUAN_ZHANG_COMPILER.md):
  complete all-workspace compiler and resource proof;
- [`docs/PROOF_AUDIT.md`](docs/PROOF_AUDIT.md): consolidated internal audit;
- [`docs/FRAME_SAFE_COMPILATION.md`](docs/FRAME_SAFE_COMPILATION.md): operator
  contracts;
- [`docs/COMPILER_BOUNDARIES.md`](docs/COMPILER_BOUNDARIES.md): exact negative
  examples and checkpoint theorem;
- [`docs/END_TO_END_QBP.md`](docs/END_TO_END_QBP.md): execution, depth,
  workspace, and decoder accounting;
- [`docs/CLAIM_SUPPORT.md`](docs/CLAIM_SUPPORT.md): claim-by-claim evidence map;
- [`docs/RESEARCH_STATUS.md`](docs/RESEARCH_STATUS.md): review and release gates.

## Repository map

```text
compiler_robust_hopf/
  frames.py                 exact real and separated complex frames
  tree_structure.py         prefix and tail operator identities
  tree_decoder.py           explicit binary--one-hot reversible decoder
  strict_zero_echo.py       exact ancilla-free addressed-layer compiler
  unified_compiler.py       all-workspace compiler and resource selection
  resource_bounds.py        exact integer proof diagnostics
  decoders.py               output-sensitive magnitude and phase decoders
  compiler_boundaries.py    global and checkpoint counterexamples

tests/
  test_frames.py
  test_tree_decoder.py
  test_strict_zero_echo.py
  test_strict_zero_audit.py
  test_unified_compiler.py
  test_decoders.py
  test_compiler_boundaries.py

scripts/
  unified_resource_ledger.py
  strict_zero_echo_ledger.py
  check_upstream_sync.py
```

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```

The ledgers expose explicit integer contributions and selected schedules. The
asymptotic theorem is proved analytically rather than inferred from numerical
fits.

## Relationship to earlier repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | Hopf coordinates, inverse map, metric, and tangent preparation |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | Established gradient protocols and Möttönen-style robustness |
| **This repository** | Optimal all-workspace frame compilation, compiler boundaries, and the new paper |

Shared definitions and upstream commits are recorded in [`SYNC.md`](SYNC.md) and
[`provenance/upstream.json`](provenance/upstream.json). Literature roles are
recorded in [`provenance/literature.json`](provenance/literature.json).

The earlier fallback remains preserved on `near-optimal-audited-2026-09` at
commit `24f339b863faa2ac92e1adb3917cbef7dc24d3b8`.

## Evidence boundary

The current theorem is internally audited, not externally verified. The result
does not address routed hardware, native-gate depth, approximate Clifford+T
synthesis, noise-dependent sampling, arbitrary state-space charts, or an
application-independent cost for controlled access to the observable.

## License

MIT. See [`LICENSE`](LICENSE).
