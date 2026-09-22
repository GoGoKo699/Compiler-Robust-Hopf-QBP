# Current theorem status

[Landing page](../README.md) · [Complete narrative](../REVIEW.md) · [Verification](VERIFICATION.md)

Last updated: 22 September 2026.

The repository supports one compiler paper with two resource models. The exact
logical frontier is established at every clean-workspace budget. The real-frame
T-count frontier is matched above a sufficient clean reservation. The
constant-clean endpoint is the active research question. The new operator-source
construction improves its upper bound to $O(N\log N)$ for three clean qubits
and the explicit dirty allocation below; the lower bound remains $\Omega(N)$.

## Exact logical result

Let

```math
N=2^n.
```

For every integer $m\geq0$, the repository supports the exact logical-circuit
theorem

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

The two compiled objects are:

- the complete real Hopf differential frame;
- the phase-dressed complex magnitude frame.

The complex leaf-phase derivatives use a separate direct record.  Every
compiler schedule respects the requested clean-workspace budget, implements the
complete logical frame on clean workspace input, and returns the workspace to
zero.

## Fault-tolerant result

Let $a$ count clean qubits, $b$ count borrowed qubits, and $q=n+a+b$. For
$0<\eta\leq1/64$, put $`L=\max\{6,\lceil\log_2(1/\eta)\rceil\}`$ and
$h=1+\lceil\log_2(L+n+2)\rceil$. For sufficiently large fixed $C$,

```math
T^\star_{F,\mathbb R}(n,a,b,\eta)
=\Theta\left(\sqrt{NL}+L+\frac{NL}{q}\right),
\qquad a\geq C(n+h).
```

The construction charges $O(NL)$ Clifford work and every precision source.
It implements the prescribed real frame on every initialized-clean and arbitrary
borrowed/reference input. The [formal chapter](FAULT_TOLERANT_COMPILER.md)
states the complete error contract and proof.

The [operator-source construction](../research/constant_clean/OPERATOR_SOURCE_COMPILER.md)
adds a sufficient constant-clean regime:

```math
a\ge3,\qquad b\ge L+n+6,
\qquad T=O(N+nL),\qquad G=O(NL).
```

At $L=N$ this gives $O(N\log N)$ T gates with three clean qubits and
$N+O(\log N)$ dirty qubits, improving the earlier $O(N^{3/2})$ upper bound.
The lower bound remains $\Omega(N)$. The explicit width condition matters;
this theorem does not cover every smaller constant clean or dirty allocation.
The [continuation brief](../research/CONSTANT_CLEAN_ENDPOINT.md) records the
remaining logarithmic gap.

The source-channel obstruction is a supporting interface theorem, not an
additive or stronger general frame lower bound. Optimal T-depth remains open.

## Construction

| Workspace | Schedule | Supporting structure |
|---:|---|---|
| $m=0$ | borrowed-suffix half-angle echo | complete four-sector operator proof and strict-zero resource sum |
| $1\leq m<4n$ | direct suffix-flagged UCG layers | one reusable clean predicate flag and all-workspace UCG synthesis |
| larger $m$ | conditioned prefix plus coherently routed subtree frames | exact tree cut, clean binary–one-hot decoder, explicit CNOT/Fredkin router, and maximal feasible cut |

The phase diagonal is one exact $n$-qubit UCG and reuses the same workspace pool
sequentially.

## Exact circuit model

The theorem is stated in the exact all-to-all logical model with:

- arbitrary one-qubit gates;
- CNOTs;
- clean ancillary qubits initialized and returned in $\lvert0\rangle$.

The active external compiler framework and optimal state-preparation benchmark
is P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023).  The proof uses Theorem 2
and Lemmas 5, 6, and 9.  The published v2 statements were checked against arXiv
v3 for the uses made here.

The preceding state-preparation paper is retained as the historical predecessor
and original source of selected primitives.  The complete source division is in
[the dependency map](SOURCE_MAP.md).

## Evidence available

The finite-precision branch includes [four reproducible suites](../verification/fault_tolerant/README.md)
and a [fixed-parameter estimator proof](QBP_APPROXIMATION.md). Its source and
kernel fixtures use exact arithmetic. Its resource grids are finite algebraic
checks. Neither constitutes a general elementary emitter or a proof of the
asymptotic theorem by enumeration.


### Dimension-independent proofs

- addressed Hopf layers and marker columns;
- frame-safe forward and inverse substitution;
- strict-zero borrowed-suffix echo;
- conditioned-prefix and tail direct-sum identities;
- clean binary–one-hot decoder;
- coherent route–operate–unroute construction;
- simultaneous workspace peaks and maximal-cut inequalities;
- matching size and depth lower bounds;
- one-UCG complex phase dressing;
- matched global-QBP consequence.

### Explicit constructions and finite checks

- independent recursive and addressed frame matrices;
- every strict-zero layer and complete frames through the documented finite
  range;
- explicit X/CNOT/Toffoli decoder layers;
- explicit CNOT/Fredkin router layers;
- arbitrary complex prefix–suffix-entangled router inputs;
- token, copy, flag, and additional-data cleanup;
- integer and exact-rational resource ledgers;
- parity, histogram, and fast Walsh–Hadamard decoders.

Run:

```bash
python scripts/reviewer_walkthrough.py
python validate.py
```

The [verification map](VERIFICATION.md) identifies the evidence level of every
component.

### Internal reconstructions

- [consolidated proof audit](PROOF_AUDIT.md);
- [strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md);
- [clean-room all-workspace reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md).

These records document internal re-derivations and corrections.  They do not
constitute independent external verification.

## Geometric convention

For unrestricted angles,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where $a_j$ is the oriented incoming amplitude.  On the canonical Hopf domains,
$a_j\geq0$ and equals the principal metric square root.  At zero metric weight,
the raw differential vanishes while the complete parameter tuple selects a unit
orthogonal marker-frame continuation.

The numerical API uses a tolerance-aware regular-coordinate mask at chart
boundaries.

## QBP consequence

The primary finite-shot target is simultaneous absolute accuracy of the raw
Hopf-coordinate gradient.  At fixed accuracy and confidence, the global
magnitude stream uses

```math
O(\log n)=O(\log\log M)
```

independent executions for $M=\Theta(N)$ coordinates.

The runtime ratio is a matched-program statement: scalar and gradient programs
use the same general state family and controlled observable, and the gradient
program adds one inverse frame with the same asymptotic logical depth as optimal
state preparation.  Classical output materialization and differently
conditioned gradient targets are separate resources.

## Contribution boundary

The repository does not claim the invention of UCGs, controlled-unitary roots,
borrowed or conditionally clean qubits, toggle detection, or reversible
routing.

The strict-zero contribution is the Hopf-specific use of one original suffix
data qubit as a restored predicate carrier, reducing one addressed depth to two
total-width-$`d+2`$ UCGs and linear predicate toggles.  The positive-workspace
contribution combines the exact Hopf tree cut with a clean decoder and explicit
coherent router.  Together they yield the optimal complete-frame frontier for
every clean-workspace budget.

The finite-precision contribution is the structural residual composition with
one source reused across accepted branches, together with its charged workspace
and precision ledger. Geometric digit encoding, Boolean lookup, ordinary LCU,
and amplification are credited to their sources. The novelty audit supports a
specific contribution claim; it does not certify priority.

## Review status

Research on the constant-clean endpoint has resumed. The
[checked-progress report](../research/CONSTANT_CLEAN_PROGRESS.md) records
the arbitrary-angle operator-source compiler, one-clean compilation for
shared-generator phase tables, batching equivalence, dirty-rank compression,
and scoped architecture restrictions. The new upper bound has a full analytic
proof and finite regression checks. The sufficient-clean matching theorem and
the general lower bounds are unchanged.

The repository has completed its internal analytic and executable checks and is
ready for independent technical review.  The shortest route is:

1. [complete narrative](../REVIEW.md);
2. [exact theorem](COMPILER_THEOREM.md) and [fault-tolerant theorem](FAULT_TOLERANT_COMPILER.md);
3. [verification and evidence](VERIFICATION.md);
4. [source and dependency map](SOURCE_MAP.md).

## Scope

No claim is made about device-connectivity depth, native hardware gates,
physical noise thresholds, finite-size constant optimality,
optimizer convergence, generic non-Hopf charts, or application-independent
controlled-observable cost.
