# Optimal Compilation of Hopf Differential Frames

### Compiler-robust quantum backpropagation at the optimal state-preparation frontier

Yuan and Zhang determine the optimal size–depth frontier for preparing one
arbitrary quantum state. This repository asks whether a stronger structured
unitary can attain the same frontier.

The **Hopf differential frame** contains the target state as one column and its
normalized coordinate tangents as designated additional columns. Quantum
backpropagation uses the inverse of this complete frame, so preserving only the
prepared state is not enough. The compiler must preserve the full logical
operator on every system input while returning its workspace to zero.

This repository gives exact frame-safe constructions for the real and separated
complex Hopf frames. The result has passed internal analytic and executable
checks and is presented for independent technical review.

<p align="center">
  <img src="assets/state-vs-frame.svg" width="900" alt="State preparation fixes one column; Hopf differential-frame compilation fixes the state and tangent-marker columns." />
</p>

## Main result under technical review

Let

```math
N=2^n
```

and let `m>=0` be the number of available clean ancillary qubits. In the exact
all-to-all circuit model with arbitrary one-qubit gates and CNOTs, the complete
real Hopf frame and the separated complex frame admit frame-safe
implementations with

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
the same asymptotic size–depth frontier as optimal arbitrary state preparation
in the Yuan–Zhang model.

## Begin here

The repository is arranged as a linear technical narrative rather than as a
software manual.

| Reading route | Purpose |
|---|---|
| **[Start the complete narrative](REVIEW.md)** | A self-contained 35–45 minute route from the synthesis question to the QBP consequence |
| **[Learn the minimal Hopf interface](docs/HOPF_INTERFACE.md)** | The state, tangent columns, marker convention, and addressed layers used by the compiler |
| **[Audit the compiler theorem](docs/COMPILER_THEOREM.md)** | The three workspace schedules, workspace ledger, upper bounds, and matching lower bounds |
| **[See what compilation changes for QBP](docs/QBP_CONSEQUENCE.md)** | Frame-safe substitution, gradient records, and the final scaling consequence |
| **[Inspect the verification](docs/VERIFICATION.md)** | Analytic identities, exact finite tests, resource ledgers, and internal proof reviews |
| **[Trace every dependency](docs/SOURCE_MAP.md)** | Exact paper results, inherited Hopf facts, local implementations, and tests |
| **[Read the literature context](docs/RELATED_WORK.md)** | State preparation, UCGs, borrowed workspace, and the narrow claim boundary |

A circuit-synthesis reader can audit the central theorem through the first four
links without first learning the full Hopf optimization framework.

## Why ordinary state preparation is insufficient

A state-preparation compiler is required only to satisfy

```math
U_{\mathrm{prep}}|0^n\rangle=|\psi\rangle.
```

The global Hopf gradient protocol instead applies the inverse of a unitary `W`
whose designated columns obey

```math
W|0^n\rangle=|\psi\rangle,
\qquad
W|\lambda(j)\rangle=|e_j\rangle.
```

Here `|e_j>` is the normalized tangent associated with coordinate `j`, and
`|lambda(j)>` is its computational marker. A compiler may preserve the first
column while permuting the tangent-marker columns.

The repository includes an exact two-qubit example in which the state is
unchanged but the decoded gradient changes from

```math
(2,0,0)
\quad\longmapsto\quad
(0,\sqrt2,0).
```

<p align="center">
  <img src="assets/two-qubit-obstruction.svg" width="900" alt="A two-qubit state-equivalent compiler swaps two tangent-marker columns and changes the decoded gradient." />
</p>

The correct compiler contract is therefore operator-level **frame safety**, not
state-column equality.

## One compiler, three internal schedules

The real-frame compiler chooses a schedule according to the available clean
workspace.

| Workspace | Internal schedule | Main idea |
|---:|---|---|
| `m=0` | borrowed-suffix echo | use one original suffix data qubit as a restored in-place predicate carrier |
| `1<=m<4n` | direct flagged UCG | compute one reusable clean suffix flag and apply a smaller uniformly controlled gate |
| larger `m` | routed parallel subframes | cut the Hopf tree, route the suffix coherently, and run disjoint subtree frames in parallel |

These are three schedules of one Hopf-specific compiler. They are not a
regime-by-regime choice between two published state-preparation constructions.
The threshold `4n` is a convenient asymptotic scheduling threshold, not a claim
about the best finite-size crossover.

The complex phase layer is one additional exact `n`-qubit uniformly controlled
gate and reuses the same workspace pool sequentially, including the empty pool
at `m=0`.

## Compiler lineage and contribution boundary

The sole active external compiler framework and optimal state-preparation
benchmark are from:

> P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits,” *Quantum* **7**, 956 (2023).

Their results supply the optimal state-preparation frontier and the exact
multi-controlled-X, uniformly controlled-gate, and coherent-copy primitives.
Those primitives can be adapted once the complete-operator structure of the
Hopf frame is exposed; the adaptation is not direct because the frame must
preserve many designated columns rather than one prepared state.

The earlier result of Sun, Tian, Yang, Yuan, and Zhang is retained as the
historical predecessor. Möttönen and Bergholm supply the multiplexor/UCG
lineage that also motivated the earlier Hopf-QBP compilation.

<p align="center">
  <img src="assets/literature-lineage.svg" width="940" alt="The compiler-synthesis and Hopf-geometry lines meet in the optimal complete-frame compiler." />
</p>

The strict-zero circuit combines familiar square-root, conjugation, and
borrowed-workspace ideas. The narrow Hopf-specific contribution is the reduction
of every addressed depth to two total-width-`d+2` UCGs using one restored
logical suffix qubit, together with the resulting optimal strict-zero
complete-frame frontier. The repository does not claim invention of borrowed
qubits, toggle detection, controlled-unitary square roots, or generic UCGs.

## Consequence for quantum backpropagation

The balanced Hopf chart supplies orthogonal coordinate tangents, known metric
weights, and computational markers. A frame-safe compiler transports this
interface without changing the global gradient measurement distribution.

For a complete chart with `M=Theta(N)` coordinates, the global magnitude stream
uses

```math
O(\log n)=O(\log\log M)
```

independent executions at fixed simultaneous coordinatewise accuracy and
confidence. Because one compiled forward or inverse frame now matches the
optimal state-preparation depth for every `m>=0`, compilation adds no further
asymptotic depth factor to this execution overhead. This comparison is made
under the controlled-observable and accuracy assumptions stated in the QBP
paper and in [the QBP consequence page](docs/QBP_CONSEQUENCE.md).

## Verification boundary

The repository checks complete operators at finite dimensions, exact borrowed-
qubit restoration, reversible decoder schedules, workspace peaks, resource
inequalities, gradient decoders, and compiler counterexamples. The validation
suite and ledgers do not replace the dimension-independent proofs.

The result does not address device routing, native-gate depth, approximate
Clifford+T synthesis, hardware noise, arbitrary state-space charts, or an
application-independent implementation cost for controlled observable access.

## Reproduce the checks

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

## Relationship to the two Hopf repositories

| Repository | Role |
|---|---|
| [`Hopf-ansatz`](https://github.com/GoGoKo699/Hopf-ansatz) | Hopf coordinates, inverse map, metric, tangent preparation, and optimization interface |
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | Global, direct-phase, and checkpoint gradient records, together with Möttönen-style robustness |
| **This repository** | Complete-frame compiler contracts, optimal all-workspace synthesis, and the resulting compiler-robust QBP consequence |

The exact fact-level dependencies are listed in
[`docs/SOURCE_MAP.md`](docs/SOURCE_MAP.md).

## License

MIT. See [`LICENSE`](LICENSE).
