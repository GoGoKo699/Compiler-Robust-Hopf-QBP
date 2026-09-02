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
every `m>=1`. At nominal `m=0`, the sharp-size construction uses one clean
real-frame suffix flag. A strict zero-ancilla fallback exists with depth `O(N)`
and size `O(nN)`.

The arbitrary diagonal block has an all-budget clean implementation of size
`O(N)`, depth

```math
O\left(n+\frac{N}{n+m}\right),
```

and at most `m` clean ancillary qubits. Its workspace is reused sequentially
with the real-frame workspace, not added to it.

The compiler boundary is now explicit:

- preserving one prepared state column is insufficient for the global reverse
  frame;
- preserving one checkpoint prefix state is insufficient for a checkpoint
  reverse suffix;
- equality on the complete active checkpoint interface is sufficient for every
  designated checkpoint estimator mean, but need not preserve the complete
  output distribution.

The internal real proof audit is in
[`PROOF_AUDIT_ISSUE_1.md`](PROOF_AUDIT_ISSUE_1.md). The complex theorem and
common-workspace audit are in
[`COMPLEX_COMMON_WORKSPACE.md`](COMPLEX_COMMON_WORKSPACE.md). The exact negative
results and checkpoint substitution theorem are in
[`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md).

The remaining central scientific decision is whether to close the later optimal
all-ancilla gap or publish the current uniformly near-optimal theorem with that
gap stated explicitly.

## Claim ledger

| Claim | Status | Evidence | Remaining work |
|---|---|---|---|
| Recursive balanced real Hopf frame equals the addressed layer product | Established here | Independent matrix constructions through `n=7` | Retain notation audit |
| First `t` full-system layers equal a `t`-qubit frame conditioned on a zero external suffix | Proved and internally audited | Algebraic proof; every cut through `n=8` | External review before submission |
| Prefix frame acts as disjoint two-mode Givens layers in unary encoding | Proved and internally audited | Exact code action, unitarity, and zero leakage through `t=3`; pair check through `t=8` | Optional gate diagram |
| Frame-safe recompilation preserves the global protocol distribution | Proved algebraically | Clean reducing-subspace substitution theorem | External review |
| State-column equality is insufficient for global Hopf QBP | Proved by explicit counterexample | Two-qubit SWAP of marker columns; exact distributions and decoded gradients | None internally |
| Real-frame unary-prefix/UCG construction has size `O(N)` | Proved relative to imported synthesis lemmas | Corrected prefix size plus geometric UCG-size sum | External review |
| Real-frame construction has depth `O(n(n-t+1)+N/(n+m))` | Proved relative to imported synthesis lemmas | Independent term derivation and uniform geometric-tail lemma | External review |
| Real frame uses at most `max(1,m)` clean ancillas | Proved for the sharp-size construction | Same-`m` schedule for `m>=1`; one flag at nominal `m=0` | Determine whether sharp size and strict zero workspace can coexist |
| Exact arbitrary diagonal has size `O(N)`, depth `O(n+N/(n+m))`, and at most `m` clean ancillas | Proved by piecewise use of imported Lemmas 10 and 11 | All-budget regime ledger and cleanup audit | External review |
| Separated complex frame has the same sharp size and depth bound as the real frame | Proved relative to imported synthesis lemmas | Sequential clean reuse of one workspace pool | External review |
| Strict zero-ancilla complex frame has depth `O(N)` and size `O(nN)` | Proved relative to the UCG theorem | Full-width zero-angle UCG representation of every addressed layer | Determine whether `O(N)` size is possible at strict zero workspace |
| Common phase is a gauge and phase gradients sum to zero | Proved and tested | Algebraic identities through random finite cases | None internally |
| Zero-amplitude leaves have zero phase differential and gradient | Proved and tested | Exact singular cases | None internally |
| Diagonal parity parameters are generated in `O(Nn)` classical work | Established constructively | FWHT formula and exact reconstruction tests | Finite constants only if useful |
| Record-wise magnitude decoding costs `O(SN)` and matches FWHT decoding | Established here | Exact sample-level tests through `n=6` | Benchmark constants only if useful |
| Direct phase decoding costs `O(S+N)` and phase records have norm two | Established here | Signed-bin implementation and exact tests | None for asymptotic count |
| Checkpoint active-interface equality preserves every designated estimator mean | Proved algebraically | Clean-interface adjoint argument and exact positive example | External review |
| State-column equality is insufficient for checkpoints | Proved by explicit counterexample | Exact two-qubit suffix changes decoded derivative from `2` to `-2` | None internally |
| Active-interface equality need not preserve the full checkpoint distribution | Proved by explicit example | Same mean with total-variation distance `1/4` | None internally |
| Older Figure 1 upper profiles hold for real and separated complex global frames | Proved from the audited bounds | Explicit regime reductions | None for the older profiles |
| Complete frame reaches `Theta(n+N/(n+m))` for every `m` | Open target | Optimal QSP benchmark known | New compiler construction or obstruction |
| Framework applies to arbitrary state charts | Not claimed | Hopf orthogonality and marker structure are special | Identify a broader proved class before renaming |

## Exact compiler-contract hierarchy

The audits establish a strict hierarchy:

```math
\text{complete frame safety}
\Longrightarrow
\text{checkpoint active-interface safety}
\Longrightarrow
\text{one prepared state column}.
```

The converses fail.

### Global obstruction

At the regular two-qubit point `theta_j=pi/4`, a SWAP of marker columns fixes
`|00>` and therefore preserves the Hopf state. For `O=-Z tensor I`, however,
the exact global gradient changes under the original decoder from

```math
(2,0,0)
```

to

```math
(0,\sqrt2,0).
```

### Checkpoint obstruction

At depth zero, a recompiled suffix may fix the one prefix state `|+0>` while
flipping its tangent partner. The final state remains `|++>`, but the decoded
root derivative changes from `2` to `-2`.

### Checkpoint positive contract

If a clean suffix compiler agrees with the designated suffix on the complete
active interface, up to one common phase, then consistent forward/reverse use
preserves all checkpoint estimator means. Behavior outside the interface may
still change the full distribution.

## Corrections and refinements produced by the audits

### Prefix size

The external-suffix predicate contributes `O(n-t)` size. Therefore

```math
S_{\mathrm{prefix}}=O(2^t+n-t),
```

not uniformly `O(2^t)`. The complete frame size remains `O(N)`.

### Ancillary workspace

For `m>=1`, the real prefix may use all `m` workspace qubits and returns them
clean. In each nonfinal tail layer, one qubit is reserved as the suffix flag and
the UCG receives the remaining `m-1`. The final layer needs no flag. The
subsequent diagonal block reuses at most the same `m` clean qubits. Thus

```math
a_{\mathrm{frame}}(m)=
\begin{cases}
1,&m=0,\\
m,&m\geq1.
\end{cases}
```

### Strict zero workspace

When absolutely no additional clean qubit is available, each addressed real
layer can be synthesized as one full-width UCG with zero rotations on inactive
suffix sectors. This yields exact depth `O(N)` and size `O(nN)`.

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
6. Explicit negative results for arbitrary state-column and checkpoint
   recompilation. **Met internally.**
7. Objective-independent checkpoint interface condition. **Met internally.**
8. Claim-support map separating finite checks, algebraic proofs, imported
   compiler theorems, and open targets. **Met and maintained.**
9. Decision on whether to prove the optimal all-ancilla frontier or publish the
   near-optimal theorem with an explicit gap. **Open.**
10. External proof review before public release or submission. **Open.**

## Preferred theorem hierarchy

### Theorem A: frame-safe invariance

A clean implementation of the same differential-frame unitary preserves the
exact global protocol distribution and all record-level concentration premises.

### Proposition B: state-column obstruction

Preparing the same state does not determine the tangent-marker columns. An
explicit two-qubit compiler returns the wrong global gradient under the
original decoder.

### Theorem C: audited all-workspace real-frame upper bound

For every `m>=0`, the real global Hopf frame has an exact sharp-size
implementation with `O(N)` size, at most `max(1,m)` clean ancillary qubits, and

```math
D_{\mathbb R}(n,m)
=
O\left(
n(n-t+1)+\frac{N}{n+m}
\right).
```

### Theorem D: common-workspace separated complex frame

The exact clean diagonal compiler reuses the same workspace pool and is
asymptotically absorbed by the real-frame block. Hence `W_C=D_ph W_R` has the
same sharp size, depth, and workspace profile.

### Theorem E: checkpoint active-interface substitution

A suffix compiler equal to the designated suffix on the complete active
interface preserves all checkpoint estimator means. State-column equality is
insufficient, and full output distributions need not be preserved.

### Corollary: compiler-robust complex Hopf backpropagation

Combine Theorems A, C, and D with the global magnitude record, direct phase
record, and output-sensitive decoders. State the accuracy allocation and
controlled-observable model explicitly.

### Target Theorem F: optimal frame compilation

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
- Compiler boundary and checkpoint interface theorem internally completed:
  **yes**.
- Suitable for a public theorem claim without external review: **no**.
- Suitable for merging into the established `Hopf-QBP` repository: **no**.
- Suitable as the technical basis of the new manuscript: **yes**, once the
  optimality-scope decision is made.
