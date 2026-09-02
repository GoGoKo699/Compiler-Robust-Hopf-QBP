# Audited near-optimal baseline — September 2026

## Purpose

This branch is the immutable internal fallback for the compiler-robust Hopf-QBP
paper. New optimality research must branch from this checkpoint rather than
modifying it.

The cumulative scientific head before this manifest is:

```text
ab1f363b94d6a13fa996da51c85a7eb466dd44f4
```

It contains the complete stacked work from:

```text
PR #5  real-frame proof audit
PR #6  separated-complex common-workspace theorem
PR #7  exact global and checkpoint compiler boundaries
```

The pull requests remain drafts and unmerged. This checkpoint preserves their
combined content independently of later optimality experiments.

## Frozen theorem package

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

### Real global frame

The complete real Hopf differential frame has an exact frame-safe
implementation with

```math
S_{\mathbb R}(n,m)=O(N),
```

```math
D_{\mathbb R}(n,m)
=
O\left(
n(n-t+1)+\frac{N}{n+m}
\right),
```

and at most

```math
\max\{1,m\}
```

clean ancillary qubits. For every `m>=1`, it uses the same `m`-qubit clean
workspace budget as the matched state-preparation compiler. At nominal `m=0`,
the sharp-size construction uses one reusable suffix flag.

### Separated complex global frame

For

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R},
```

the real and diagonal blocks sequentially reuse one clean workspace pool. The
complete complex frame has the same sharp asymptotic size, depth, and workspace
profile as the real frame.

The arbitrary diagonal block itself has

```math
S_{\mathrm{diag}}(n,m)=O(N),
```

```math
D_{\mathrm{diag}}(n,m)
=
O\left(n+\frac{N}{n+m}\right),
```

using at most `m` clean ancillary qubits.

### Strict zero-workspace fallback

An exact strict-zero-ancilla implementation exists for the real and separated
complex frames with

```math
D^{(0)}=O(N),
\qquad
S^{(0)}=O(nN).
```

This is separate from the sharp `O(N)`-size construction.

### Uniform comparison with optimal state preparation

Against

```math
D_{\mathrm{QSP}}(n,m)
=
\Theta\left(n+\frac{N}{n+m}\right),
```

the audited frame compiler is uniformly within an `O(log n)` depth factor. The
proof is split into the low-workspace range, where the geometric term absorbs
the sequential term, and the remaining range, where `n-t=O(log n)`.

## Frozen logical boundaries

The checkpoint also contains the following exact results.

1. State-column equality does not preserve global Hopf backpropagation. A
   two-qubit SWAP example changes the decoded gradient from `(2,0,0)` to
   `(0,sqrt(2),0)` while preserving the prepared state.
2. A checkpoint suffix is safely substitutable under the active-interface
   condition

   ```math
   \widetilde B_d J P_d=e^{i\chi}J B_dP_d.
   ```

   This preserves designated checkpoint estimator means, not necessarily the
   complete output distribution.
3. Checkpoint state-column equality alone can flip a derivative from `2` to
   `-2`.

## Frozen implementation evidence

At the cumulative scientific head:

- 32 deterministic tests passed;
- validation passed on Python 3.11 and Python 3.13;
- both real and complex resource ledgers executed successfully;
- synchronization metadata validated successfully.

Finite tests support exact identities and bookkeeping. The asymptotic compiler
theorems also import the exact UCG, unary-to-binary, multi-controlled-X, and
diagonal-synthesis results cited in the corresponding proof documents.

## What is not frozen as solved

This baseline does not claim:

- optimal all-ancilla frame depth;
- simultaneous strict zero workspace and `O(N)` size;
- approximate Clifford+T error bounds;
- routed-device or noisy-hardware costs;
- arbitrary checkpoint-compiler invariance;
- a theorem for general coordinate charts.

## Freeze policy

No new scientific development should be committed to this branch. A discovered
error in the baseline must be handled by:

1. opening a dedicated correction branch from this checkpoint;
2. documenting the correction and its effect on every dependent result; and
3. creating a successor baseline rather than rewriting this record.

The optimal all-ancilla investigation begins from this branch and must preserve
this theorem package as its fallback result.
