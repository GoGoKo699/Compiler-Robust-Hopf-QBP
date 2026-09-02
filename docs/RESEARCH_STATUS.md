# Research status and release gates

Last updated: 2026-09-02.

## Current conclusion

The active project now uses one compiler architecture and one general
state-preparation benchmark.

- **Active framework:** Yuan and Zhang, *Quantum* **7**, 956 (2023).
- **Historical predecessor:** Sun et al., *IEEE TCAD* **42**, 3301--3314
  (2023).
- **Hopf-specific construction:** this repository.

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
Theorem 2 for every positive workspace budget.

The active proof is in
[`UNIFIED_YUAN_ZHANG_COMPILER.md`](UNIFIED_YUAN_ZHANG_COMPILER.md), with the
short theorem chain in [`THEOREM_OVERVIEW.md`](THEOREM_OVERVIEW.md) and the
line-by-line internal check in [`PROOF_AUDIT.md`](PROOF_AUDIT.md).

## Active construction

The real compiler has two internal schedules inside one algorithm.

### Direct schedule

When no useful tree cut fits, every addressed Hopf depth is synthesized with a
suffix-zero predicate and one Yuan--Zhang uniformly controlled gate. For
`1<=m<4n`, this already has optimal-order depth.

### Routed schedule

For larger workspace, cut after `t` Hopf depths, put `B=2**t` and `s=n-t`, and
use

```math
R_t^{(n)}=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A coherent router moves the existing suffix into one of `B` branch registers,
the controlled subtree frames run in parallel, and inverse routing cleans every
auxiliary register. The prefix is implemented by a new self-contained
binary--one-hot tree decoder with depth `O(t)`, size `O(B)`, and workspace

```math
3B-2-t.
```

Both prefix and tail fit inside the common routed envelope

```math
2B(s+1).
```

The complex phase layer is one exact `n`-qubit UCG, not a separate
phase-polynomial compiler.

## Strict zero-workspace boundary

The optimal theorem is stated for `m>=1`. At strict zero additional workspace,
the current exact alternatives are:

| Clean ancillary qubits | Size | Depth |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

It remains open whether one can achieve simultaneously

```math
S(n,0)=O(N),
\qquad
D(n,0)=O\left(n+\frac{N}{n}\right).
```

The repository never identifies one clean flag with zero workspace.

## Compiler correctness boundary

A state compiler is not automatically a frame compiler. The required clean
operator contract is

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input. Exact two-qubit counterexamples show that equality on
one prepared state column can corrupt both global and checkpoint gradient
readout.

Checkpoint recompilation has a weaker but factorization-specific sufficient
condition: equality on the complete active checkpoint interface, up to one
common phase. This preserves designated checkpoint means but need not preserve
the full output distribution.

## Claim ledger

| Claim | Internal status | Main evidence | Remaining gate |
|---|---|---|---|
| Recursive and addressed Hopf frames coincide | Proved and tested | Independent matrix constructions | External review |
| Conditioned-prefix identity | Proved and tested | Algebraic operator identity; every cut through `n=8` | External review |
| Tail is a direct sum of subtree frames | Proved and tested | Exact angle map; every cut through `n=8` | External review |
| Binary--one-hot tree decoder is clean and reversible | Proved and tested | Explicit X/CNOT/Toffoli schedule and basis permutation checks | External review |
| Tree decoder has `O(t)` depth and `O(2**t)` size | Proved and scheduled | Pairwise-disjoint layer list; closed-form counts | External review |
| Conditioned prefix has `O(n)` depth and `O(2**t+n-t)` size | Proved | Decoder, suffix predicate, copied control, disjoint Givens layers | External review |
| Direct small-workspace compiler is optimal order | Proved relative to Yuan--Zhang Lemmas 5 and 6 | Width sum and low-workspace absorption | External review |
| Routed tail is clean on arbitrary entangled inputs | Proved and tested | Coherent router and inverse; zero-leakage checks | External review |
| Complete routed construction fits in `2*2**t*(n-t+1)` workspace | Proved and tested | Data/token/copy/flag ledger | External review |
| Positive-workspace real frame has optimal size and depth | Internally audited theorem | Direct/routed upper bound plus real-state lower bound | External review |
| Complex phase diagonal is exactly one UCG | Proved and tested | Complete block-diagonal matrix identity | External review |
| Positive-workspace separated complex frame has the same optimum | Internally audited corollary | Sequential reuse of one clean pool | External review |
| State-column equality is insufficient | Proved by counterexample | Exact two-qubit distributions and gradients | None internally |
| Checkpoint active-interface safety preserves means | Proved algebraically | Interface adjoint theorem | External review |
| Record-wise magnitude decoding costs `O(SN)` | Constructive | Exact parity/FWHT equivalence tests | Constants only if useful |
| Direct phase decoding costs `O(S+N)` | Constructive | Signed-bin tests and norm-two records | None internally |
| Phase UCG block table takes `O(N)` generation work | Constructive | Direct pairing of leaf phases | Elementary compiler host-time benchmark optional |
| Strict-zero sharp joint frontier | Open | Current fallback is `O(nN)` size and `O(N)` depth | New construction or obstruction |
| General theorem for arbitrary charts | Not claimed | Current frame and routing are Hopf-specific | Prove a larger class first |

## End-to-end QBP status

Frame-safe substitution preserves the global magnitude distribution. At fixed
simultaneous coordinatewise accuracy and confidence, the magnitude stream uses

```math
O(\log n)=O(\log\log M)
```

executions for `M=Theta(N)` coordinates. Because frame depth matches optimal
state-preparation depth, the compiler contributes no additional asymptotic
factor. The direct phase stream uses no inverse frame.

The full accounting is in [`END_TO_END_QBP.md`](END_TO_END_QBP.md). Any quoted
wall-clock ratio remains conditional on the declared controlled-observable
access model.

## Source discipline

The active proof uses Yuan--Zhang Theorem 2 and Lemmas 5, 6, and 9. Sun et al.
remains cited for the historical ancilla--depth development and original source
attribution, but no active module invokes its unary-to-binary construction or
selects its QSP compiler in any ancillary regime.

The exact policy is recorded in [`RELATED_WORK.md`](RELATED_WORK.md) and
[`../provenance/literature.json`](../provenance/literature.json).

## Frozen fallback

The cumulative earlier package is preserved on

```text
near-optimal-audited-2026-09
```

at manifest commit

```text
24f339b863faa2ac92e1adb3917cbef7dc24d3b8
```

The unified refactor does not rewrite this checkpoint.

## Release gates

- Unified proof and deterministic validation: **met internally**.
- Historical and active-source separation: **met**.
- Removal of obsolete active modules and chronological audit documents:
  **in progress on the refactor branch**.
- One clean consolidation pull request to `main`: **pending**.
- External human proof review: **open**.
- Strict `m=0` resolution: **open but not required for a positive-workspace
  paper if stated explicitly**.
- Controlled-observable and statistical notation freeze: **pending manuscript
  work**.
- Public release or submission: **not yet**.
