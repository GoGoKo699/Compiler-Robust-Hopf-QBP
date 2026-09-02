# Research status and release gates

Last updated: 2026-09-02.

## Current conclusion

The evidence now supports the following real and separated-complex frame
statements, relative to the exact compiler lemmas cited in the proof documents.

Let

```math
N=2^n,
\qquad
t=
\min\left\{
n,
\max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\}.
```

The complete real global frame and the separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

have exact frame-safe implementations of size `O(N)` and depth

```math
O\left(
n(n-t+1)+\frac{N}{n+m}
\right).
```

They use the same `m` clean ancillary qubits as the matched state compiler for
every `m>=1`. At the nominal `m=0` endpoint, the sharp-size construction uses
one clean real-frame suffix flag. A strict zero-ancilla fallback exists with
depth `O(N)` and size `O(nN)`.

The arbitrary diagonal block has an all-budget clean implementation of size
`O(N)`, depth

```math
O\left(n+\frac{N}{n+m}\right),
```

and at most `m` clean ancillary qubits. Its workspace is reused sequentially
with the real-frame workspace, not added to it.

The internal real proof audit is in
[`PROOF_AUDIT_ISSUE_1.md`](PROOF_AUDIT_ISSUE_1.md). The complex theorem,
diagonal regime audit, common phase, singular leaves, parameter transform, and
end-to-end accounting are in
[`COMPLEX_COMMON_WORKSPACE.md`](COMPLEX_COMMON_WORKSPACE.md).

This is not yet the final paper theorem. The project still lacks the explicit
state-column/checkpoint negative result and a decision on whether the complete
frame reaches the later optimal all-ancilla frontier.

## Claim ledger

| Claim | Status | Evidence | Remaining work |
|---|---|---|---|
| Recursive balanced real Hopf frame equals the addressed layer product | Established here | Independent matrix constructions through `n=7` | Retain notation audit |
| First `t` full-system layers equal a `t`-qubit frame conditioned on a zero external suffix | Proved and internally audited | Algebraic proof; every cut through `n=8` | External review before submission |
| Prefix frame acts as disjoint two-mode Givens layers in unary encoding | Proved and internally audited | Exact code action, unitarity, and zero leakage through `t=3`; pair check through `t=8` | Optional gate diagram |
| Frame-safe recompilation preserves the global estimator | Proved algebraically | Clean reducing-subspace substitution theorem | Include formal theorem in manuscript |
| Real-frame unary-prefix/UCG construction has size `O(N)` | Proved relative to imported synthesis lemmas | Corrected prefix size plus geometric UCG-size sum | External review |
| Real-frame construction has depth `O(n(n-t+1)+N/(n+m))` | Proved relative to imported synthesis lemmas | Independent term derivation and uniform geometric-tail lemma | External review |
| Real frame uses at most `max(1,m)` clean ancillas | Proved for the stated sharp-size construction | Same-`m` schedule for `m>=1`; one flag at nominal `m=0` | Determine whether sharp size and strict zero workspace can coexist |
| Exact arbitrary diagonal has size `O(N)`, depth `O(n+N/(n+m))`, and at most `m` clean ancillas | Proved by piecewise use of imported Lemmas 10 and 11 | All-budget regime ledger and cleanup audit | External review |
| Separated complex frame has the same sharp size and depth bound as the real frame | Proved relative to imported synthesis lemmas | Sequential clean reuse of one workspace pool | External review |
| Strict zero-ancilla complex frame has depth `O(N)` and size `O(nN)` | Proved relative to the UCG theorem | Full-width zero-angle UCG representation of every addressed layer | Determine whether `O(N)` size is possible at strict zero workspace |
| Common phase is a gauge and phase gradients sum to zero | Proved and tested | Algebraic identities through random finite cases | None for the identity |
| Zero-amplitude leaves have zero phase differential and gradient | Proved and tested | Exact singular cases | None for the identity |
| Diagonal parity parameters are generated in `O(Nn)` classical work | Established constructively | FWHT formula and exact reconstruction tests | Finite constants only if useful |
| Record-wise magnitude decoding costs `O(SN)` and matches FWHT decoding | Established here | Exact sample-level tests through `n=6` | Benchmark constants only if useful |
| Direct phase decoding costs `O(S+N)` and phase records have norm two | Established here | Signed-bin implementation and exact tests | None for asymptotic count |
| Older Figure 1 upper profiles hold for real and separated complex global frames | Proved from the audited bounds | Explicit regime reductions | None for the older profiles |
| Complete frame reaches `Theta(n+N/(n+m))` for every `m` | Open target | Optimal QSP benchmark known | New compiler construction or obstruction |
| Compiler robustness extends automatically to checkpoints | Not claimed | State-equivalent compilation can erase intermediate interfaces | Separate sufficient condition or counterexample |
| Framework applies to arbitrary state charts | Not claimed | Hopf orthogonality and marker structure are special | Identify a broader proved class before renaming |

## Corrections and refinements produced by the audits

### Prefix size

The external-suffix predicate contributes `O(n-t)` size. Therefore

```math
S_{\mathrm{prefix}}=O(2^t+n-t),
```

not uniformly `O(2^t)`. The complete frame size remains `O(N)`.

### Ancillary workspace

For `m>=1`, the real prefix may use all `m` workspace qubits and returns them
clean. In each nonfinal tail layer, one of those qubits is reserved as the
suffix flag and the UCG receives the remaining `m-1`. The final layer needs no
flag. The subsequent diagonal block reuses at most the same `m` clean qubits.
Thus the sharp-size real and complex constructions have

```math
a_{\mathrm{frame}}(m)=
\begin{cases}
1,&m=0,\\
m,&m\geq1.
\end{cases}
```

### Strict zero workspace

When absolutely no additional clean qubit is available, each addressed real
layer can instead be synthesized as one full-width UCG with zero rotations on
the inactive suffix sectors. This yields exact depth `O(N)` and size `O(nN)`.
The tradeoff is explicit rather than hidden.

## Paper threshold

The project is ready for a standalone paper only after the following minimum
conditions are met:

1. Frame-safe substitution theorem with exact register contracts. **Met.**
2. Internal line-by-line proof audit of the real conditioned-prefix and unary
   construction. **Met.**
3. A real-frame theorem valid for every ancillary budget, even if within an
   explicitly bounded factor of optimal QSP. **Met.**
4. Quantum executions, circuit size, depth, workspace, parameter generation,
   and classical-decoding accounting. **Met for the compiler/decoder core;
   controlled-observable cost remains application-dependent.**
5. Precise common-workspace complex-chart theorem. **Met internally.**
6. Explicit negative result for arbitrary state-column and checkpoint
   recompilation. **Open.**
7. Claim-support map separating finite checks, algebraic proofs, imported
   compiler theorems, and open targets. **Met and maintained.**
8. Decision on whether to prove the optimal all-ancilla frontier or publish the
   near-optimal theorem with an explicit gap. **Open.**
9. External proof review before public release or submission. **Open.**

## Preferred theorem hierarchy

### Theorem A: frame-safe invariance

A clean implementation of the same differential-frame unitary preserves the
exact global protocol distribution and all record-level concentration premises.

### Theorem B: audited all-workspace real-frame upper bound

For every `m>=0`, the real global Hopf frame has an exact sharp-size
implementation with `O(N)` size, at most `max(1,m)` clean ancillary qubits, and

```math
D_{\mathbb R}(n,m)
=
O\left(
n(n-t+1)+\frac{N}{n+m}
\right).
```

### Theorem C: common-workspace separated complex frame

The exact clean diagonal compiler reuses the same workspace pool and is
asymptotically absorbed by the real-frame block. Hence `W_C=D_ph W_R` has the
same sharp size, depth, and workspace profile. A strict zero-ancilla fallback
has depth `O(N)` and size `O(nN)`.

### Corollary: compiler-robust complex Hopf backpropagation

Combine Theorems A--C with the global magnitude record, direct phase record,
and output-sensitive decoders. State the accuracy allocation and
controlled-observable model explicitly.

### Target Theorem D: optimal frame compilation

Either prove

```math
D_{\mathrm{frame}}(n,m)
=
\Theta\left(n+\frac{N}{n+m}\right)
```

for every `m`, or establish a separation showing why coherent access to a
complete differential frame can be harder than preparing one state column.

## Present release decision

- Suitable for private research development: **yes**.
- Real-frame theorem internally proof-audited: **yes**.
- Common-workspace complex theorem internally completed: **yes**.
- Suitable for a public theorem claim without external review: **no**.
- Suitable for merging into the established `Hopf-QBP` repository: **no**.
- Suitable as the technical basis of the new manuscript: **yes**, after the
  negative-result gate and optimality-scope decision are completed.
