# Compiler-Robust Hopf Quantum Backpropagation

Exact differential-frame compilation, compiler boundaries, and end-to-end
resource accounting for Hopf-coordinate quantum backpropagation.

## Main result

Let

```math
N=2^n
```

and let `m` be the number of clean ancillary qubits. For every `m>=1`, the
complete real Hopf differential frame and the separated complex frame have
exact frame-safe implementations with

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

The construction uses at most the requested `m` clean ancillary qubits and
returns them to zero. Its size and depth match the optimal arbitrary-state-
preparation frontier of Yuan and Zhang for every positive workspace budget.

This is stronger than compiling one state column. The global gradient protocol
needs the complete differential-frame action on every clean-workspace input.
Exact counterexamples in this repository show that a state-equivalent compiler
can preserve the Hopf state while returning the wrong gradient.

The result has passed internal mathematical and deterministic validation. It has
not received external peer review.

## One active compiler framework

The active external framework and state-preparation benchmark are:

> P. Yuan and S. Zhang, "Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits," *Quantum* **7**, 956 (2023).

The active proof uses their Theorem 2 and Lemmas 5, 6, and 9. It does not choose
between two prior compilers as a function of the ancillary budget.

The earlier work of Sun, Tian, Yang, Yuan, and Zhang remains cited as the
historical predecessor and as the original source credited for selected
primitives. It is not a second active construction. See
[`docs/RELATED_WORK.md`](docs/RELATED_WORK.md).

## Compiler architecture

Cut the addressed Hopf frame after `t` tree depths and write

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

The compiler has two internal schedules.

### Direct schedule

For small positive workspace, each addressed depth is one suffix-zero predicate
followed by one Yuan--Zhang uniformly controlled gate. This already has
optimal-order depth when `1<=m<4n`.

### Routed schedule

For larger workspace:

1. a self-contained reversible tree decoder converts the binary prefix to a
   one-hot branch code in `O(t)` depth and `O(B)` size;
2. controlled disjoint Givens layers implement the conditioned prefix;
3. a coherent router moves the existing suffix and an activation token to the
   selected branch;
4. all controlled subtree frames run on disjoint registers in parallel;
5. inverse routing and decoding return every auxiliary register to zero.

The prefix decoder uses exactly

```math
3B-2-t
```

clean ancillary qubits. The complete prefix and routed tail fit inside

```math
2B(s+1).
```

Choosing the largest feasible cut gives the optimal positive-workspace depth.

The complex phase layer is exactly one additional `n`-qubit uniformly
controlled gate:

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\operatorname{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

It reuses the same clean workspace pool sequentially.

## Consequence for quantum backpropagation

The balanced Hopf chart supplies the orthogonal coordinate tangents, metric
weights, computational markers, and bounded shared gradient records. A
frame-safe compiler transports that differential interface without changing the
measurement distribution.

At fixed simultaneous coordinatewise accuracy and confidence, the global
magnitude stream uses

```math
O(\log n)=O(\log\log M)
```

executions for `M=Theta(N)` Hopf coordinates. Since one compiled frame has the
same asymptotic depth as optimal state preparation, compilation adds no further
asymptotic factor. The direct complex phase stream uses no inverse frame.

The complete quantum and classical accounting is in
[`docs/END_TO_END_QBP.md`](docs/END_TO_END_QBP.md).

## Compiler correctness hierarchy

| Compiler promise | Scalar state | Checkpoint means | Global Hopf distribution |
|---|---:|---:|---:|
| One prepared state column | sufficient | insufficient | insufficient |
| Complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| Complete frame-safe operator | sufficient | sufficient where applicable | sufficient |

For checkpoint factorization `U=B_dA_d`, the sufficient clean interface contract
is

```math
\widetilde B_dJP_d=e^{i\chi}JB_dP_d.
```

This preserves the designated checkpoint means but need not preserve the full
output distribution. See
[`docs/COMPILER_BOUNDARIES.md`](docs/COMPILER_BOUNDARIES.md).

## Strict zero-workspace boundary

The optimal theorem begins at `m=1`.

| Clean ancillary qubits | Exact size upper bound | Exact depth upper bound |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

Whether strict zero workspace can attain both `O(N)` size and `O(n+N/n)` depth
is open. The repository does not count one clean flag as zero workspace.

## Start here

- [`docs/THEOREM_OVERVIEW.md`](docs/THEOREM_OVERVIEW.md): theorem chain in one
  document;
- [`docs/UNIFIED_YUAN_ZHANG_COMPILER.md`](docs/UNIFIED_YUAN_ZHANG_COMPILER.md):
  full construction and resource proof;
- [`docs/PROOF_AUDIT.md`](docs/PROOF_AUDIT.md): internal line-by-line audit;
- [`docs/FRAME_SAFE_COMPILATION.md`](docs/FRAME_SAFE_COMPILATION.md): operator
  contracts;
- [`docs/COMPILER_BOUNDARIES.md`](docs/COMPILER_BOUNDARIES.md): exact negative
  examples and checkpoint theorem;
- [`docs/END_TO_END_QBP.md`](docs/END_TO_END_QBP.md): quantum and classical
  accounting;
- [`docs/CLAIM_SUPPORT.md`](docs/CLAIM_SUPPORT.md): claim-by-claim evidence map;
- [`docs/RESEARCH_STATUS.md`](docs/RESEARCH_STATUS.md): release gates and open
  boundaries.

## Repository map

```text
compiler_robust_hopf/
  frames.py                 exact real and separated complex frames
  tree_structure.py         prefix and tail operator identities
  tree_decoder.py           explicit binary--one-hot reversible decoder
  unified_compiler.py       active direct/routed compiler and resource ledger
  decoders.py               output-sensitive magnitude and phase decoders
  compiler_boundaries.py    global and checkpoint counterexamples

tests/
  test_frames.py
  test_tree_decoder.py
  test_unified_compiler.py
  test_decoders.py
  test_compiler_boundaries.py

scripts/
  unified_resource_ledger.py
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
python scripts/check_upstream_sync.py --offline
```

The resource ledger reports explicit integer contributions and selected
schedules. The asymptotic theorem is proved analytically rather than inferred
from numerical fits.

## Relationship to earlier repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | Hopf coordinates, inverse map, metric, and tangent preparation |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | Established gradient protocols and Möttönen-style compiler robustness |
| **This repository** | Frame-safe optimal compilation, exact compiler boundaries, and the new paper |

Shared definitions and upstream commits are recorded in [`SYNC.md`](SYNC.md) and
[`provenance/upstream.json`](provenance/upstream.json). Compiler-literature roles
are recorded in [`provenance/literature.json`](provenance/literature.json).

The cumulative earlier fallback remains preserved on
`near-optimal-audited-2026-09` at commit
`24f339b863faa2ac92e1adb3917cbef7dc24d3b8`.

## Scope boundary

The current theorem does not cover:

- strict-zero-workspace optimality;
- routed hardware or native-gate depth;
- approximate Clifford+T error bounds;
- noise-dependent sampling;
- arbitrary state-space charts; or
- external peer-review status.

## License

MIT. See [`LICENSE`](LICENSE).
