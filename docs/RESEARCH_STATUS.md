# Research status and release gates

Last updated: 2026-09-03.

## Current conclusion

The repository contains one active all-workspace compiler architecture and one
general state-preparation benchmark.

- **Active compiler framework and benchmark:** P. Yuan and S. Zhang,
  *Quantum* **7**, 956 (2023).
- **Historical predecessor:** X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang,
  *IEEE TCAD* **42**, 3301--3314 (2023).
- **Hopf-specific compiler, frame-safety, and backpropagation results:** this
  repository.

Let

```math
N=2^n.
```

For every integer `m>=0`, the complete real Hopf differential frame and the
separated complex frame have exact frame-safe implementations using at most the
requested `m` clean ancillary qubits, with

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

This matches the optimal arbitrary-state-preparation frontier in Yuan--Zhang
Theorem 2 for every ancillary budget. The theorem has passed multiple internal
audits but has not received independent external proof review.

## Active construction

The real-frame compiler is one algorithm with three internal schedules.

### Strict zero workspace

For `m=0`, a borrowed-suffix echo uses one original suffix data qubit as a
restored predicate carrier. Two half-angle UCGs, four predicate toggles, and two
CNOT echoes implement each nonfinal addressed depth without an ancillary wire.
The final depth is one ordinary UCG.

### Small positive workspace

When no useful routed cut fits, every addressed depth is synthesized with a
lower-suffix-zero flag and one Yuan--Zhang UCG. For `1<=m<4n`, the polynomial
sequential term is absorbed by the state-preparation scale.

### Larger workspace

For a cut after `t` depths, write

```math
B=2^t,
\qquad
s=n-t.
```

The exact tail identity is

```math
R_t^{(n)}=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A self-contained reversible binary--one-hot decoder realizes the conditioned
prefix. A coherent router moves the existing suffix into the branch selected by
the prefix, all controlled subtree frames run on disjoint registers in parallel,
and inverse routing returns every auxiliary register to zero. Choosing the
largest feasible cut gives the optimal positive-workspace depth.

The complex phase diagonal is one exact `n`-qubit UCG and reuses the real-frame
workspace pool sequentially, including the empty pool at `m=0`.

## Compiler correctness boundary

A state-preparation circuit is not automatically a differential-frame circuit.
The global method requires

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input. Exact two-qubit examples show that equality on one
prepared state column can preserve the scalar state while corrupting global or
checkpoint gradient readout.

Checkpoint recompilation has a weaker but factorization-specific sufficient
condition: equality on the complete active checkpoint interface, up to one
common phase. It preserves designated checkpoint means but need not preserve the
complete output distribution.

## Evidence status

| Claim | Status | Main evidence |
|---|---|---|
| Recursive and addressed real frames coincide | Proved and tested | Independent exact matrices |
| Conditioned-prefix identity | Proved and tested | Complete-operator proof; every cut through `n=8` |
| Tail is a direct sum of subtree frames | Proved and tested | Exact angle map; every cut through `n=8` |
| Binary--one-hot decoder is clean and reversible | Proved and tested | Explicit X/CNOT/Toffoli schedule |
| Routed compiler respects the requested workspace | Proved and tested | Complete data/token/copy/flag ledger |
| Positive-workspace frame optimum | Internally audited theorem | Direct/routed upper bounds and real-state lower bounds |
| Strict-zero borrowed-suffix echo | Proved and tested | Four-sector operator identity and complete-frame matrices |
| Strict-zero frame optimum | Internally audited theorem | Echo upper bound and exact-wire parameter lower bound |
| Complex phase diagonal is one exact UCG | Proved and tested | Complete block-diagonal identity |
| Separated complex frame has the same optimum | Internally audited corollary | Sequential workspace reuse |
| State-column equality is insufficient | Proved by counterexample | Exact distributions and decoded gradients |
| Checkpoint active-interface safety preserves means | Proved algebraically | Interface theorem and finite examples |
| Record-wise magnitude decoder costs `O(SN)` | Constructive and tested | Direct parity records versus FWHT |
| Direct phase decoder costs `O(S+N)` | Constructive and tested | Signed-bin estimator and norm-two records |
| Generic theorem for arbitrary charts | Not claimed | Present geometry and routing are Hopf-specific |

Finite validation supplements but does not replace the analytic proof. The MCT,
UCG, coherent-copy, and QSP statements are imported under the exact
Yuan--Zhang hypotheses.

## Strict-zero prior-art boundary

The abstract square-root/conjugation and borrowed-bit ingredients have close
antecedents in controlled-unitary decompositions and dirty/borrowed-ancilla
toggle detection. The repository therefore does not claim a new generic echo
identity.

The project-specific novelty target is:

> using one original suffix data qubit as a restored predicate carrier,
> aggregating all prefix-dependent Hopf rotations into two total-width-`d+2`
> UCGs per nonfinal depth, and closing the optimal strict-zero complete-frame
> size--depth frontier.

The current literature survey is recorded in
[`STRICT_ZERO_PRIOR_ART.md`](STRICT_ZERO_PRIOR_ART.md). A broader independent
prior-art review remains a release gate.

## Consolidation and validation status

Draft PR [#20](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/pull/20)
is the single all-workspace consolidation candidate for `main`. Its branch is

```text
all-workspace-unified-final
```

Both branch-push and pull-request merge-ref validation pass on Python 3.11 and
3.13. Each job completes:

- source compilation;
- **62 deterministic tests**;
- the unified all-workspace resource ledger;
- the dedicated strict-zero echo ledger; and
- the offline upstream-synchronization audit.

The active unified resource row selects the borrowed-suffix echo at `m=0`, the
direct flagged-UCG schedule at small positive workspace, and the routed schedule
when a useful cut fits. Exact cross-checks require the unified strict-zero row to
coincide with the dedicated echo ledger.

The prior positive-workspace PR #14 and strict-zero development PRs #18 and #19
are superseded by PR #20. They remain available as historical review checkpoints
but are not alternative merge paths.

## Frozen fallback

The earlier cumulative theorem package is preserved on

```text
near-optimal-audited-2026-09
```

at manifest commit

```text
24f339b863faa2ac92e1adb3917cbef7dc24d3b8
```

It is retained for provenance and is not an active compiler path.

## Remaining release gates

- All-workspace operator and resource proof: **met internally**.
- One-framework source policy: **met**.
- Strict-zero internal proof audit: **met**.
- All-workspace unified branch and PR-level CI: **met**.
- Final diff-level repository audit: **met internally**.
- Independent human proof review: **open in Issue #12**.
- Broader prior-art review and novelty wording: **open in Issue #17**.
- Controlled-observable and statistical-accuracy notation freeze: **pending
  manuscript work**.
- Merge into private `main`: **deferred until the review decision**.
- Public release or submission: **not yet**.
