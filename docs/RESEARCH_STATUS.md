# Research status

[← Repository landing page](../README.md) · [Complete technical note](../REVIEW.md) · [Verification](VERIFICATION.md)

## Central result

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits supplied to the compiler.
The repository supports the exact all-workspace theorem

```math
\boxed{
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

`W_R` is the complete real Hopf differential frame. `W_(C,mag)=D_ph W_R` is
the phase-dressed complex magnitude frame. The complex leaf-phase derivatives
use a separate direct record.

The circuits are exact in the all-to-all arbitrary-one-qubit+CNOT model. They
use at most the requested clean workspace and restore it exactly.

## Position relative to state preparation

The theorem addresses a structured unitary-completion problem.

- QSP fixes one initialized state column.
- The Hopf frame fixes the state and every designated marker column.
- A generic unitary has `Theta(N^2)` parameters; the Hopf frame has `O(N)` tree
  parameters.

The state-preparation primitives can be adapted after the addressed-layer and
tree-cut structure is exposed. The resulting complete frame matches the optimal
QSP size–depth frontier for every workspace budget.

## Active compiler architecture

| Budget | Schedule | Main mechanism |
|---:|---|---|
| `m=0` | borrowed-suffix echo | one original logical suffix bit carries the predicate and is restored |
| `1<=m<4n` | direct flagged UCG | one reusable clean bit stores the complete suffix-zero predicate |
| larger `m` | routed parallel subframes | clean prefix decoding, coherent suffix routing, and disjoint subtree execution |

The complex magnitude compiler adds one phase UCG and reuses the same workspace
pool sequentially.

## Scientific support completed

### Operator and geometry

- recursive and addressed-layer real frames agree as complete operators;
- marker and bit-order conventions are fixed;
- unrestricted differentials use the oriented incoming amplitude `a_j`;
- canonical domains recover `a_j=sqrt(g_(j,j))`;
- singular coordinates have zero raw differential and a chart-selected marker
  direction;
- state-column equality is separated from complete frame safety.

### Strict zero workspace

- complete four-sector echo proof;
- exact restoration of the borrowed logical qubit on arbitrary entangled input;
- no hidden work wire;
- exact UCG width and predicate count;
- `Theta(N)` size and `Theta(n+N/n)` depth;
- inverse and complex magnitude corollaries.

### Positive workspace

- conditioned-prefix identity;
- tail direct-sum identity and angle map;
- explicit clean binary–one-hot decoder;
- explicit CNOT/Fredkin coherent router;
- token, copy, flag, and data cleanup;
- simultaneous peak-workspace ledger;
- low-workspace absorption and maximal-cut argument;
- separate `s=1` endpoint.

### Optimality and QBP

- real-state parameter-count size lower bound;
- parameter-location and output-light-cone depth lower bounds;
- one-UCG phase diagonal;
- frame-safe preservation of the complete global magnitude distribution;
- output-sensitive magnitude and direct-phase decoding;
- matched scalar/gradient logical-depth statement;
- explicit statistical task and conditioning boundaries.

## External circuit framework

The active framework is P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023):

- Theorem 2: optimal all-workspace QSP frontier;
- Lemma 5: exact ancilla-free multi-controlled `X`;
- Lemma 6: all-workspace UCG synthesis;
- Lemma 9: coherent copy–use–uncopy.

The published article corresponds to `arXiv:2202.11302v2`; the imported
statements were checked in v3. The earlier state-preparation paper is retained
as the historical predecessor and original-source reference for selected
primitives.

## Executable support

The repository contains:

- complete dense operator checks for frames and the strict-zero echo;
- explicit X/CNOT/Toffoli decoder layers;
- explicit CNOT/Fredkin router layers and sparse complex-state simulation;
- exact block action for controlled subtree and phase UCGs;
- integer and exact-rational resource ledgers;
- parity, histogram, FWHT, and direct-phase decoder cross-checks.

Run:

```bash
python scripts/technical_walkthrough.py
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

The exact evidence levels are listed in [Verification and evidence](VERIFICATION.md).

## Claim boundary

The strict-zero circuit combines familiar ingredients: UCGs, controlled-unitary
roots, Pauli conjugation, borrowed or conditionally clean workspace, and
toggle-detection cancellation.

The narrow project-specific statement is the reduction of one addressed Hopf
depth to two total-width-`d+2` UCGs and linear predicate toggles using one
restored original suffix bit, together with the resulting optimal complete-frame
frontier.

The repository does not claim a generic compiler for arbitrary unitary or
coordinate-frame families.

## Remaining scientific step

The mathematical and executable checks are complete at the present scope. The
remaining step is independent technical and prior-art assessment of:

- the strict-zero four-sector construction;
- the explicit routed register schedule and simultaneous peak;
- the maximal-cut asymptotic argument;
- the matching lower bounds;
- the matched QBP cost statement;
- the narrow contribution boundary.

The repository is arranged so this assessment can begin from
[`README.md`](../README.md) and proceed linearly through [`REVIEW.md`](../REVIEW.md)
without using repository-management features.

## Scope exclusions

The result does not cover hardware connectivity, native-gate depth, approximate
Clifford+T synthesis, noise, error mitigation, optimizer convergence, or a
generic controlled-observable implementation.

---

[← Repository landing page](../README.md) · [Complete technical note](../REVIEW.md) · [Verification](VERIFICATION.md)
