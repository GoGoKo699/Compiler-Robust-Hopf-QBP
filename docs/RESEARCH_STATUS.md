# Research status

[Landing page](../README.md) · [Complete narrative](../REVIEW.md) · [Verification](VERIFICATION.md)

Last updated: September 2026.

## Current scientific conclusion

The repository contains one exact all-workspace compiler architecture for the
real Hopf differential frame and the phase-dressed complex magnitude frame.

Let

```math
N=2^n.
```

For every integer `m>=0`, the internally supported theorem is

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

The compiled circuit uses at most the requested `m` clean ancillary qubits,
implements the complete logical frame on every clean-workspace system input,
and returns its workspace to zero. The complex leaf-phase gradient uses a
separate direct record.

This matches the optimal arbitrary-state-preparation frontier of Yuan and Zhang
in the same exact logical circuit model.

## Active construction

| Workspace | Schedule | Current evidence |
|---:|---|---|
| `m=0` | borrowed-suffix half-angle echo | complete operator proof, exact resource proof, full-layer and full-frame tests |
| `1<=m<4n` | direct suffix-flagged UCG layers | complete operator argument and all-workspace resource proof |
| larger `m` | binary–one-hot prefix decoder plus coherent routed subtree frames | exact tree identities, explicit CNOT/Fredkin router, arbitrary-entangled-input tests, cleanup tests, register ledger, and cut proof |

The complex phase diagonal is one exact `n`-qubit UCG and reuses the same
workspace pool sequentially.

## Peer-review revision completed

A repository-wide adversarial audit identified two major presentation/evidence
gaps and several precision issues. The revision now includes:

1. an explicit coherent router in
   [`compiler_robust_hopf/router.py`](../compiler_robust_hopf/router.py), with
   operator-level route–operate–unroute tests in
   [`tests/test_router.py`](../tests/test_router.py);
2. oriented incoming-amplitude notation
   ```math
   \partial_{\theta_j}|\psi\rangle=a_j|e_j\rangle,
   \qquad g_{j,j}=a_j^2,
   ```
   together with canonical angle domains and singular-coordinate tests;
3. consistent use of **phase-dressed complex magnitude frame**, keeping the
   direct leaf-phase stream separate;
4. a matched-program definition of the scalar-versus-gradient runtime ratio;
5. an implementation-level evidence taxonomy distinguishing explicit circuits,
   ideal matrices, imported elementary synthesis, and resource ledgers;
6. reconciliation with `Hopf-QBP/main` at
   `faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582`;
7. exact source-version policy for the published Yuan–Zhang v2 and checked v3.

No obstruction to the all-workspace theorem was found during this revision.
Independent human verification remains pending.

## Source policy

The sole active external compiler framework and state-preparation benchmark is:

> P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023).

The published article corresponds to `arXiv:2202.11302v2`. Theorem 2 and Lemmas
5, 6, and 9 were also checked in v3 and retain the statements used here. The
earlier work of Sun, Tian, Yang, Yuan, and Zhang is retained as the historical
predecessor and original source credited for selected primitives.

The Hopf chart, canonical domains, and differential geometry are inherited from
the first Hopf paper. The global, direct-phase, checkpoint, and statistical task
boundaries are inherited from `Hopf-QBP`. The frame-safe contracts and all-
workspace compiler are developed here.

The exact division is in [the source map](SOURCE_MAP.md).

## Evidence completed

### Analytic proofs

The repository contains dimension-independent arguments for:

- the addressed Hopf frame and marker interface;
- oriented incoming amplitudes and canonical metric notation;
- singular-coordinate frame continuation;
- frame-safe substitution;
- state-column and checkpoint obstructions;
- the strict-zero four-sector echo;
- conditioned-prefix and tail direct-sum identities;
- the binary–one-hot decoder;
- the explicit coherent router and routed parallel tail;
- all workspace peaks and cut inequalities;
- matching size and depth lower bounds;
- the phase-dressed complex magnitude corollary;
- the matched global-QBP compiler consequence.

### Executable checks

The deterministic suite covers complete frame matrices, canonical domains,
singular coordinates, compiler counterexamples, strict-zero sectors and frames,
decoder reversibility, explicit coherent routing, branch-flag and copy cleanup,
route–operate–unroute equality, one-UCG phase diagonals, resource inequalities,
and gradient decoders.

```bash
python scripts/reviewer_walkthrough.py
python validate.py
```

The complete evidence taxonomy is in [Verification and evidence](VERIFICATION.md).

### Internal proof reviews

- [Consolidated proof audit](PROOF_AUDIT.md)
- [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md)
- [Clean-room all-workspace reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md)

They record re-derivations, corrections, and evidence limits. They do not
constitute independent external verification.

## Statistical and runtime boundary

The primary finite-shot target is simultaneous absolute accuracy of the **raw
Hopf-coordinate gradient**. Complete-vector, relative, normalized-frame, and
natural-gradient outputs have distinct conditioning and sample requirements.

The displayed `O(log n)=O(log log M)` overhead is a matched-program statement:
scalar and gradient executions use the same state family and controlled
observable, while the gradient program adds one inverse frame of optimal
state-preparation-order depth. It is not a comparison with an instance-specific
scalar shortcut and does not include materializing the complete classical
output.

## Contribution boundary

The repository does not claim invention of UCGs, controlled-unitary square
roots, borrowed or conditionally clean qubits, or toggle detection.

The narrow strict-zero contribution is the use of one original suffix data
qubit as a restored in-place predicate carrier, reducing all prefix-dependent
Hopf rotations at depth `d` to two total-width-`d+2` UCGs and linear predicate
toggles. Combined with the positive-workspace schedules, this yields the
optimal complete-frame frontier for every ancillary budget.

## Review status

The theorem is **ready for independent technical review**. The intended route
is:

1. [Complete narrative](../REVIEW.md)
2. [Minimal Hopf interface](HOPF_INTERFACE.md)
3. [Complete compiler theorem](COMPILER_THEOREM.md)
4. [QBP consequence](QBP_CONSEQUENCE.md)
5. [Verification and evidence](VERIFICATION.md)
6. [Source map](SOURCE_MAP.md)

## Scope not presently claimed

The result does not establish device-connectivity depth, fault-tolerant T-count,
approximate synthesis error, noise-dependent guarantees, optimizer convergence,
a universal controlled-observable implementation cost, finite-size constant
optimality, or compiler invariance for arbitrary non-Hopf charts.
