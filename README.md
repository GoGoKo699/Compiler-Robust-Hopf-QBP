# Optimal Compilation of Hopf Differential Frames

### Compiler-robust quantum backpropagation at the optimal state-preparation frontier

Yuan and Zhang determine the optimal exact size–depth frontier for preparing one
arbitrary quantum state. This repository asks whether a stronger structured
unitary can attain the same frontier.

The **Hopf differential frame** contains the target state as one column and
designated coordinate directions as the remaining columns. Quantum
backpropagation applies the inverse of this frame, so preserving only the
prepared state is insufficient: compilation must preserve the complete logical
operator and return every work qubit to zero.

The repository gives exact frame-safe constructions for the real Hopf frame and
the phase-dressed complex **magnitude** frame. The complex leaf-phase
derivatives use a separate direct record. The result has passed internal
analytic and executable checks and is presented for independent technical
review.

<p align="center">
  <img src="assets/state-vs-frame.svg" width="900" alt="State preparation fixes one column; Hopf differential-frame compilation fixes the state and tangent-marker columns." />
</p>

## Main result under technical review

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits available to the
compiler. In the exact all-to-all logical model with arbitrary one-qubit gates
and CNOTs,

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

The circuit uses at most the requested `m` clean ancillary qubits and returns
them to zero. Thus coherent access to the real frame and the phase-dressed
complex magnitude frame has the same asymptotic size–depth frontier as optimal
arbitrary state preparation in the Yuan–Zhang model.

## Begin here

The repository is arranged as a linear technical narrative rather than as a
software manual.

| Reading route | Purpose |
|---|---|
| **[Start the complete narrative](REVIEW.md)** | A self-contained route from the synthesis question to the QBP consequence |
| **[Learn the minimal Hopf interface](docs/HOPF_INTERFACE.md)** | Canonical angle domains, oriented incoming amplitudes, marker columns, singular coordinates, and addressed layers |
| **[Audit the compiler theorem](docs/COMPILER_THEOREM.md)** | The three workspace schedules, explicit coherent router, workspace ledger, upper bounds, and matching lower bounds |
| **[See what compilation changes for QBP](docs/QBP_CONSEQUENCE.md)** | Frame-safe substitution, statistical task boundaries, and the matched-program depth comparison |
| **[Inspect the verification](docs/VERIFICATION.md)** | Analytic identities, exact operator tests, implementation levels, resource ledgers, and internal proof reviews |
| **[Trace every dependency](docs/SOURCE_MAP.md)** | Exact paper versions, inherited Hopf facts, imported compiler results, local implementations, and tests |
| **[Read the literature context](docs/RELATED_WORK.md)** | State preparation, UCGs, borrowed workspace, and the narrow contribution boundary |

A circuit-synthesis reader can audit the compiler theorem before learning the
complete Hopf optimization framework.

## Why ordinary state preparation is insufficient

A state-preparation compiler need only satisfy

```math
U_{\mathrm{prep}}|0^n\rangle=|\psi\rangle.
```

The global Hopf gradient protocol instead uses a unitary `W` with designated
columns

```math
W|0^n\rangle=|\psi\rangle,
\qquad
W|\lambda(j)\rangle=|e_j\rangle.
```

At a regular chart point, the coordinate differential is

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

Here `a_j` is the oriented incoming amplitude. On the canonical Hopf domains,
`a_j>=0` and therefore `a_j=sqrt(g_(j,j))`. If `g_(j,j)=0`, the raw differential
vanishes; the unit marker column remains a **chart-selected orthogonal
continuation determined by the complete parameter tuple**, rather than a
normalized nonzero derivative. The numerical implementation uses a
tolerance-aware regular-coordinate mask at chart boundaries.

A compiler may preserve the first column while permuting the marker columns.
The repository gives an exact two-qubit example in which the state is unchanged
but the decoded gradient changes from

```math
(2,0,0)
\quad\longmapsto\quad
(0,\sqrt2,0).
```

<p align="center">
  <img src="assets/two-qubit-obstruction.svg" width="900" alt="A two-qubit state-equivalent compiler swaps two tangent-marker columns and changes the decoded gradient." />
</p>

The correct contract is therefore operator-level **frame safety**, not
state-column equality.

## One compiler, three internal schedules

| Workspace | Internal schedule | Main idea |
|---:|---|---|
| `m=0` | borrowed-suffix echo | use one original suffix data qubit as a restored in-place predicate carrier |
| `1<=m<4n` | direct flagged UCG | compute one reusable clean suffix flag and apply a smaller uniformly controlled gate |
| larger `m` | routed parallel subframes | cut the Hopf tree, route the suffix coherently, and run disjoint subtree frames in parallel |

The large-workspace route is an explicit reversible construction in
[`compiler_robust_hopf/router.py`](compiler_robust_hopf/router.py), not only a
resource formula. Exact tests route arbitrary complex prefix–suffix-entangled
inputs, apply all token-controlled subtree frames, unroute, and verify zero
workspace leakage.

These are three schedules of one Hopf-specific compiler. They are not a
regime-by-regime choice between two published state-preparation constructions.
The threshold `4n` is a convenient asymptotic scheduling threshold, not a claim
about the best finite-size crossover.

The complex phase diagonal is one additional exact `n`-qubit UCG. It reuses the
same workspace pool sequentially, including the empty pool at `m=0`.

## Compiler lineage and contribution boundary

The sole active external compiler framework and optimal state-preparation
benchmark are from:

> P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
> improved unitary synthesis by quantum circuits with any number of ancillary
> qubits,” *Quantum* **7**, 956 (2023).

The published article corresponds to arXiv v2. The imported statements—Theorem
2 and Lemmas 5, 6, and 9—were also checked in arXiv v3 and retain the forms used
here. Their results supply the optimal state-preparation frontier and the exact
multi-controlled-X, UCG, and coherent-copy primitives. Those primitives can be
adapted after the complete-operator structure of the Hopf frame is exposed; the
adaptation is not direct because the frame fixes many designated columns rather
than one initialized state column.

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

The primary finite-shot target inherited from `Hopf-QBP` is simultaneous
absolute accuracy of the **raw Hopf-coordinate gradient**. Complete-vector,
relative, normalized-frame, and natural-gradient targets have different
conditioning and execution requirements.

For a chart with `M=Theta(N)` coordinates, the global magnitude stream uses

```math
O(\log n)=O(\log\log M)
```

independent executions at fixed raw-coordinate `l_infinity` accuracy and
confidence. The runtime statement is a matched-program comparison: scalar and
gradient executions use the same forward preparation and controlled observable,
and the gradient program adds one inverse frame whose logical depth has the
same asymptotic order as optimal state preparation. It is not a comparison with
an instance-specialized scalar circuit, and it does not make materializing an
`M`-entry classical output sublinear.

The complete statement and its assumptions are in
[the QBP consequence page](docs/QBP_CONSEQUENCE.md).

## Verification boundary

The repository checks:

- complete real and phase-dressed magnitude-frame operators at finite sizes;
- exact borrowed-qubit restoration;
- explicit binary–one-hot decoder layers;
- explicit coherent route–operate–unroute on arbitrary complex inputs;
- branch-flag, copy-pool, and total-workspace cleanup;
- resource inequalities, gradient decoders, and compiler counterexamples.

The elementary UCG and multi-controlled-X decompositions are imported from
Yuan–Zhang rather than regenerated locally. Finite tests and ledgers support but
do not replace the dimension-independent proofs.

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
| [`Hopf-QBP`](https://github.com/GoGoKo699/Hopf-QBP) | Global, direct-phase, and checkpoint gradient records, together with Möttönen-style robustness and statistical task boundaries |
| **This repository** | Complete-frame compiler contracts, optimal all-workspace synthesis, and the resulting compiler-robust QBP consequence |

The exact fact-level dependencies are listed in
[`docs/SOURCE_MAP.md`](docs/SOURCE_MAP.md).

## License

MIT. See [`LICENSE`](LICENSE).
