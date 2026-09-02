# Research status and release gates

Last updated: 2026-09-02.

## Current conclusion

The evidence now supports the following real-frame statement, relative to the
exact compiler lemmas cited in the proof audit:

> The balanced Hopf chart supplies the coherent differential frame, metric
> weights, marker structure, and shared gradient records. The complete real
> global frame admits a frame-safe compiler of size `O(2**n)` and depth
>
> ```math
> O\left(
> n(n-t+1)+\frac{2^n}{n+m}
> \right),
> ```
>
> where
>
> ```math
> t=
> \min\left\{
> n,
> \max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
> \right\}.
> ```
>
> It uses the same `m` clean ancillary qubits as the matched state compiler for
> every `m>=1`; the present `m=0` construction uses one clean suffix flag.

The internal proof audit is in
[`PROOF_AUDIT_ISSUE_1.md`](PROOF_AUDIT_ISSUE_1.md). It corrected the isolated
unary-prefix size to `O(2**t+n-t)` and strengthened the workspace bound from
`m+1` to `max(1,m)`.

This is not yet the final paper theorem. The project still lacks the
common-workspace complex result, the explicit negative example, and a decision
on whether the complete frame reaches the later optimal all-ancilla frontier.

## Claim ledger

| Claim | Status | Evidence | Remaining work |
|---|---|---|---|
| Recursive balanced real Hopf frame equals the addressed layer product | Established here | Independent matrix constructions through `n=7` | Retain notation audit |
| The first `t` full-system frame layers equal a `t`-qubit frame conditioned on a zero external suffix | Proved and internally audited | Algebraic proof; every cut through `n=8` | External review before submission |
| The prefix frame acts as disjoint two-mode Givens layers in unary encoding | Proved and internally audited | Exact code action, unitarity, and zero leakage through `t=3`; pair check through `t=8` | Optional gate diagram |
| A frame-safe recompilation preserves the global estimator | Proved algebraically | Clean reducing-subspace substitution theorem | Include formal theorem in manuscript |
| Real-frame unary-prefix/UCG construction has size `O(2**n)` | Proved relative to imported synthesis lemmas | Corrected prefix size plus geometric UCG-size sum | External review |
| Real-frame construction has depth `O(n(n-t+1)+2**n/(n+m))` | Proved relative to imported synthesis lemmas | Independent term derivation and uniform geometric-tail lemma | External review |
| Real frame uses at most `max(1,m)` clean ancillas | Proved for the stated construction | Same-`m` tail schedule for `m>=1`; one flag for `m=0` | Determine whether zero-extra `m=0` is possible |
| The construction reproduces all three Figure 1 upper profiles of Sun et al. | Proved from the audited bound | Explicit regime reductions | None for the older profiles |
| The separated complex frame has the same profiles | Theorem candidate | `W_C=D_ph W_R` plus diagonal-synthesis bounds | Complete common-workspace audit |
| Record-wise Walsh decoding costs `O(S 2**n)` and matches FWHT decoding | Established here | Exact deterministic tests for `n=1,...,6` | Benchmark constants only if useful |
| The complete frame reaches `Theta(n+2**n/(n+m))` for every `m` | Open target | Optimal QSP benchmark known | New compiler construction or obstruction |
| Compiler robustness extends automatically to checkpoints | Not claimed | State-equivalent compilation can erase intermediate interfaces | Separate sufficient condition or counterexample |
| The framework applies to arbitrary state charts | Not claimed | Hopf orthogonality and marker structure are special | Identify a broader proved class before renaming |

## Corrections produced by the first proof audit

### Prefix size

The external-suffix predicate contributes `O(n-t)` size. Therefore the prefix
block has

```math
S_{\mathrm{prefix}}=O(2^t+n-t),
```

not uniformly `O(2^t)`. The complete frame size remains `O(2**n)`.

### Ancillary workspace

The prefix may use all `m` workspace qubits and returns them clean. In each
nonfinal tail layer, one of those qubits is then reserved as the suffix flag and
the UCG receives the remaining `m-1`. The final layer needs no flag. Hence:

```math
a_{\mathrm{frame}}(m)=
\begin{cases}
1,&m=0,\\
m,&m\geq1.
\end{cases}
```

## Paper threshold

The project is ready for a standalone paper only after the following minimum
conditions are met:

1. Frame-safe substitution theorem with exact register contracts. **Met.**
2. Internal line-by-line proof audit of the real conditioned-prefix and unary
   construction. **Met.**
3. A real-frame theorem valid for every ancillary budget, even if within an
   explicitly bounded factor of optimal QSP. **Met.**
4. Complete quantum executions, size, depth, workspace, parameter-generation,
   and classical-decoding accounting. **Partly met.**
5. Precise common-workspace complex-chart theorem. **Open.**
6. Explicit negative result for arbitrary state-column and checkpoint
   recompilation. **Open.**
7. Claim-support map separating finite checks, algebraic proofs, imported
   compiler theorems, and open targets. **Met and maintained.**
8. External proof review before public release or submission. **Open.**

## Preferred theorem hierarchy

### Theorem A: frame-safe invariance

A clean implementation of the same differential-frame unitary preserves the
exact global protocol distribution and all record-level concentration premises.

### Theorem B: audited all-workspace real-frame upper bound

For every `m>=0`, the real global Hopf frame has an exact implementation with
`O(2**n)` size, at most `max(1,m)` clean ancillary qubits, and

```math
D_{\mathrm{frame}}(n,m)
=
O\left(
n(n-t+1)+\frac{2^n}{n+m}
\right).
```

### Corollary: compiler-robust real Hopf backpropagation

Combine Theorems A and B with the global gradient record and output-sensitive
decoder. State the accuracy and resource models explicitly.

### Complex corollary

Add only after the diagonal and real-frame blocks share one audited workspace
schedule.

### Target Theorem C: optimal frame compilation

Either prove

```math
D_{\mathrm{frame}}(n,m)
=
\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every `m`, or establish a separation showing why coherent access to a
complete differential frame can be harder than preparing one state column.

## Present release decision

- Suitable for private research development: **yes**.
- Real-frame theorem internally proof-audited: **yes**.
- Suitable for a public theorem claim without external review: **no**.
- Suitable for merging into the established `Hopf-QBP` repository: **no**.
- Suitable as the technical basis of the new manuscript: **yes**, after the
  complex and negative-result gates are completed.
