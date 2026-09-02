# Research status and release gates

Last updated: 2026-09-03.

## Current conclusion

This repository now has one active compiler architecture and one general
state-preparation benchmark.

- **Active compiler framework and benchmark:** P. Yuan and S. Zhang,
  *Quantum* **7**, 956 (2023).
- **Historical predecessor:** X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang,
  *IEEE TCAD* **42**, 3301--3314 (2023).
- **Hopf-specific frame construction and compiler-boundary results:** this
  repository.

Let

```math
N=2^n.
```

For every integer `m>=1`, the complete real Hopf differential frame and the
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
Theorem 2 for every positive workspace budget. The result is internally audited
but has not received external proof review.

## Active construction

The real-frame compiler is one algorithm with two internal schedules.

### Direct schedule

When no useful routed cut fits, every addressed Hopf depth is synthesized using
a lower-suffix-zero predicate and one Yuan--Zhang uniformly controlled gate.
For `1<=m<4n`, its `O(n**2)` sequential term is absorbed by the exponential
state-preparation scale.

### Routed schedule

For larger workspace, cut after `t` Hopf depths and write

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
and inverse routing returns every auxiliary register to zero. The prefix and
tail fit inside

```math
2B(s+1)
```

clean workspace qubits. Choosing the largest feasible cut gives the optimal
positive-workspace depth.

The complex phase diagonal is one exact `n`-qubit UCG and reuses the real-frame
workspace pool sequentially.

The full construction and proof are in
[`UNIFIED_YUAN_ZHANG_COMPILER.md`](UNIFIED_YUAN_ZHANG_COMPILER.md), with the
short theorem chain in [`THEOREM_OVERVIEW.md`](THEOREM_OVERVIEW.md) and the
internal line-by-line audit in [`PROOF_AUDIT.md`](PROOF_AUDIT.md).

## Compiler correctness boundary

A state-preparation circuit is not automatically a differential-frame circuit.
The global method requires the clean operator contract

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input. Exact two-qubit examples show that equality on one
prepared state column can preserve the scalar state while corrupting the global
or checkpoint gradient readout.

Checkpoint recompilation has a weaker but factorization-specific sufficient
condition: equality on the complete active checkpoint interface, up to one
common phase. It preserves designated checkpoint means but need not preserve the
complete output distribution.

## Internal evidence status

| Claim | Status | Main evidence |
|---|---|---|
| Recursive and addressed real Hopf frames coincide | Proved and tested | Independent exact matrix constructions |
| Conditioned-prefix identity | Proved and tested | Complete-operator proof; every cut through `n=8` |
| Tail is a direct sum of subtree frames | Proved and tested | Exact angle map; every cut through `n=8` |
| Binary--one-hot decoder is clean and reversible | Proved and tested | Explicit X/CNOT/Toffoli schedule; basis-permutation and inverse checks |
| Decoder has `O(t)` depth and `O(2**t)` size | Proved and scheduled | Pairwise-disjoint layer list and closed-form ledger |
| Routed compiler respects the requested workspace | Proved and tested | Data, token, copied-control, and branch-flag peak ledger |
| Positive-workspace real frame has optimal size and depth | Internally audited theorem | Direct/routed upper bound plus real-state lower bounds |
| Complex phase diagonal is one exact UCG | Proved and tested | Complete block-diagonal operator equality |
| Separated complex frame has the same optimum | Internally audited corollary | Clean sequential workspace reuse |
| State-column equality is insufficient | Proved by counterexample | Exact two-qubit distributions and decoded gradients |
| Checkpoint active-interface safety preserves means | Proved algebraically | Interface adjoint theorem and finite examples |
| Record-wise magnitude decoding costs `O(SN)` | Constructive and tested | Direct parity records agree with histogram plus FWHT |
| Direct phase decoding costs `O(S+N)` | Constructive and tested | Signed-bin estimator and norm-two records |
| Strict-zero sharp joint frontier | Open | Current exact fallback is larger |
| General theorem for arbitrary charts | Not claimed | Present geometry and routing are Hopf-specific |

Finite validation supplements but does not replace the analytic proof. The
MCT, UCG, coherent-copy, and optimal-QSP statements are imported under the exact
standard-circuit hypotheses of Yuan--Zhang.

## Repository consolidation status

Draft PR [#14](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/pull/14)
is the single consolidation candidate for `main`.

At commit

```text
2448cea951bb5e0cd36eab42bd4fdb37397ed76c
```

both the branch push and pull-request merge ref passed on Python 3.11 and 3.13.
Each job completed:

- source compilation;
- 46 deterministic tests;
- the unified Yuan--Zhang resource ledger; and
- the offline synchronization audit.

The active package exports only the unified modules. Development-stage
near-optimal, separate-complex, and checkpoint-audit modules and tests are absent
from the consolidation tree; their history remains in Git and on the frozen
fallback branch.

## Strict zero-workspace boundary

The optimal theorem begins at `m=1`.

| Clean ancillary qubits | Exact size upper bound | Exact depth upper bound |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

It remains open whether strict zero workspace can achieve simultaneously

```math
S(n,0)=O(N),
\qquad
D(n,0)=O\left(n+\frac{N}{n}\right).
```

The repository never counts one clean flag as zero workspace.

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

- Unified proof and deterministic validation: **met internally**.
- One-framework source policy: **met**.
- Repository consolidation and PR-level CI: **met**.
- Final diff-level repository audit: **met internally**.
- External human proof review: **open in Issue #12**.
- Controlled-observable and statistical-accuracy notation freeze: **pending
  manuscript work**.
- Strict `m=0` resolution: **open, but not required for a paper explicitly
  scoped to `m>=1`**.
- Merge into private `main`: **deferred until the external-review decision**.
- Public release or submission: **not yet**.
