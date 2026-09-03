# Research status

[Landing page](../README.md) · [Complete narrative](../REVIEW.md) · [Verification](VERIFICATION.md)

Last updated: September 2026.

## Current scientific conclusion

The repository contains one exact all-workspace compiler architecture for the
complete real Hopf differential frame and the separated complex frame.

Let

```math
N=2^n.
```

For every integer `m>=0`, the internally supported theorem is

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

The compiled circuit uses at most the requested `m` clean ancillary qubits,
implements the complete frame on every clean-workspace system input, and
returns its workspace to zero.

This matches the optimal arbitrary-state-preparation frontier of Yuan and Zhang
in the same exact logical circuit model.

## Active construction

The real-frame compiler has three internal schedules.

| Workspace | Schedule | Status |
|---:|---|---|
| `m=0` | borrowed-suffix half-angle echo | complete operator proof, resource proof, and exact finite validation |
| small positive `m` | direct suffix-flagged UCG layers | complete operator and all-workspace resource proof |
| larger `m` | binary–one-hot prefix decoder and routed parallel subtree frames | complete tree identities, register ledger, cut proof, and exact finite validation |

The complex phase layer is one exact `n`-qubit UCG and reuses the same
workspace pool sequentially.

## Source policy

The sole active external compiler framework and state-preparation benchmark is:

> P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023).

The proof uses their Theorem 2 and Lemmas 5, 6, and 9. The earlier work of Sun,
Tian, Yang, Yuan, and Zhang is retained as the historical predecessor and
original source credited for selected primitives.

The Hopf chart and normalized tangent geometry are inherited from the first
Hopf paper. The global, phase, and checkpoint gradient records are inherited
from the Hopf-QBP paper. The frame-safe compiler contracts, all-workspace frame
construction, and optimality proof are developed in this repository.

The exact fact-level division is in [the source map](SOURCE_MAP.md).

## Evidence completed

### Analytic proofs

The repository contains dimension-independent proofs of:

- the addressed Hopf frame and marker interface;
- frame-safe substitution;
- the state-column and checkpoint obstructions;
- the strict-zero four-sector echo;
- exact restoration of the borrowed logical suffix qubit;
- the conditioned-prefix and tail direct-sum identities;
- the binary–one-hot decoder and coherent router;
- all workspace peaks and cut inequalities;
- matching size and depth lower bounds;
- the separated complex corollary;
- the global QBP compiler consequence.

### Executable checks

The deterministic suite covers complete frame matrices, exact compiler
counterexamples, strict-zero sectors and full frames, decoder reversibility,
routed workspace, one-UCG phase diagonals, resource inequalities, and gradient
decoders. A short orientation run is available through

```bash
python scripts/reviewer_walkthrough.py
```

The complete commands and evidence taxonomy are in
[Verification and evidence](VERIFICATION.md).

### Internal proof reviews

Three detailed internal review records remain visible:

- [Consolidated proof audit](PROOF_AUDIT.md)
- [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md)
- [Clean-room all-workspace reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md)

They record re-derivations, resource checks, corrections, and evidence limits.
They do not constitute independent external verification.

## Contribution boundary

The repository does not claim invention of uniformly controlled gates,
controlled-unitary square-root identities, borrowed or conditionally clean
qubits, or toggle detection.

The narrow strict-zero contribution is the use of one original suffix data
qubit as a restored in-place predicate carrier, reducing all prefix-dependent
Hopf rotations at depth `d` to two total-width-`d+2` UCGs and linear predicate
toggles. Combined with the positive-workspace schedules, this yields the
optimal complete-frame frontier for every ancillary budget.

The broader literature position and conservative claim wording are in
[Related work](RELATED_WORK.md).

## Review status

The theorem is **under independent technical review**. The repository has been
organized so that a reader can assess it without following development history
or learning GitHub workflow concepts.

The intended route is:

1. [Complete narrative](../REVIEW.md)
2. [Minimal Hopf interface](HOPF_INTERFACE.md)
3. [Complete compiler theorem](COMPILER_THEOREM.md)
4. [QBP consequence](QBP_CONSEQUENCE.md)
5. [Verification and evidence](VERIFICATION.md)
6. [Source map](SOURCE_MAP.md)

## Scope not presently claimed

The result does not establish:

- device-connectivity or routed hardware depth;
- a native fault-tolerant gate count or T-depth;
- approximate synthesis error bounds;
- noise-dependent execution guarantees;
- a universal implementation cost for controlled observable access;
- optimal finite constants or crossover points;
- compiler invariance for arbitrary non-Hopf charts.

These are separate extensions rather than hidden premises of the exact theorem.
