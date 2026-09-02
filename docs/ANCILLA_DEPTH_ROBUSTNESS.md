# Ancilla--depth robustness of the global Hopf frame

## Status

This document contains a theorem candidate. The Hopf-specific matrix identities
are proved and tested. The asymptotic depth result additionally relies on exact
synthesis theorems from:

- X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, *Asymptotically Optimal
  Circuit Depth for Quantum State Preparation and General Unitary Synthesis*,
  IEEE TCAD 42, 3301--3314 (2023), arXiv:2108.06150;
- P. Yuan and S. Zhang, *Optimal (controlled) quantum state preparation and
  improved unitary synthesis by quantum circuits with any number of ancillary
  qubits*, Quantum 7, 956 (2023), arXiv:2202.11302.

The present construction reproduces the older paper's three state-preparation
upper profiles. Reaching the later optimal all-ancilla frontier is a separate
open target described in `OPTIMAL_ALL_ANCILLA_TARGET.md`.

## 1. Setup

Let `n` be the number of system qubits and

```math
N=2^n.
```

Write the addressed real Hopf frame as

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_1^{(n)}L_0^{(n)}.
```

At depth `d`, the layer contains `2**d` disjoint two-level rotations. For
`r=0,...,2**d-1`, define

```math
a_{d,r}=r2^{n-d},
\qquad
b_{d,r}=(2r+1)2^{n-d-1}.
```

Then

```math
L_d^{(n)}
=
\prod_{r=0}^{2^d-1}
G_{a_{d,r},b_{d,r}}
\bigl(\theta_{2^d+r}\bigr),
```

where `G_(a,b)(theta)` embeds the Hopf `R_y(theta)` block on computational
basis states `|a>` and `|b>`.

## 2. Exact conditioned-prefix identity

For `0<=t<=n`, define

```math
F_t^{(n)}=L_{t-1}^{(n)}\cdots L_0^{(n)}
```

and

```math
P_{n-t}=|0^{n-t}\rangle\!\langle0^{n-t}|.
```

Then

```math
\boxed{
F_t^{(n)}
=
W_{\mathbb R}^{(t)}\otimes P_{n-t}
+
I_{2^t}\otimes\bigl(I-P_{n-t}\bigr).
}
```

The smaller frame uses exactly the first `2**t-1` Hopf angles.

### Proof

For every `d<t`, the addressed condition in `L_d^(n)` requires all bits below
the depth-`d` target to be zero. Split those lower bits into the remainder of the
first `t` qubits and the external suffix of length `n-t`. On the external
zero-suffix sector, the layer is precisely `L_d^(t)` on the prefix. On the
orthogonal suffix sector it is the identity. Thus

```math
L_d^{(n)}
=
L_d^{(t)}\otimes P_{n-t}
+
I_{2^t}\otimes\bigl(I-P_{n-t}\bigr).
```

The two projectors are orthogonal and invariant under every factor. Multiplying
the layers proves the boxed identity.

The deterministic suite checks every cut through `n=8` and independently
reconstructs the complete frame after appending the tail layers.

## 3. Unary realization of the prefix frame

Let `E_t` encode a `t`-qubit computational basis state into the
single-excitation code of `2**t` unary modes:

```math
E_t|r\rangle=|e_r\rangle.
```

Replace every computational two-level rotation in `W_R^(t)` by the same Givens
rotation on unary modes `a_(d,r)` and `b_(d,r)`. Let the resulting network be
`G_t`. Then

```math
E_t^\dagger G_tE_t=W_{\mathbb R}^{(t)}
```

and

```math
\bigl(I-E_tE_t^\dagger\bigr)G_tE_t=0.
```

At a fixed tree depth, all mode pairs are disjoint. The unary frame is therefore
a sequence of `t` parallel Givens layers with `2**t-1` logical rotations in
total. A number-preserving two-mode Givens gate has constant exact cost in the
arbitrary-one-qubit-plus-CNOT model; adding one copied predicate control remains
a fixed-width unitary and therefore also has constant exact cost.

The suite checks the complete unary Hilbert-space action through `t=3`, including
unitarity and zero leakage, and checks pair disjointness through `t=8`.

## 4. Clean unary-prefix circuit

The unary-to-binary transformation in Sun et al. maps

```math
|e_r\rangle
\longmapsto
|r\rangle|0^{2^t-t}\rangle
```

in depth `O(t)` and size `O(2**t)`, using `2**(t+1)` clean ancillary qubits. Its
inverse encodes the binary prefix into the unary register.

To implement the conditioned prefix:

1. apply the inverse unary-to-binary transform;
2. compute `[external suffix = 0]` when `t<n`;
3. fan out this predicate to enough clean controls for the widest unary layer;
4. apply the `t` controlled parallel Givens layers;
5. uncompute the fanout and predicate;
6. return from unary to binary encoding.

The widest layer contains `2**(t-1)` rotations. A CNOT tree fans out the coherent
control in depth `O(t)` and size `O(2**t)`. The copied controls are never targets
of the controlled Givens gates and are uncomputed exactly.

The ancillary requirement is bounded by

```math
(2^t-t)+2^{t+1}=3\,2^t-t.
```

The first term supplies unary-register wires not already occupied by the `t`
system qubits. The second is the conversion workspace. After conversion, that
workspace is clean and can be reused for predicate fanout. Thus the prefix block
has depth `O(n+t)=O(n)` and size `O(2**t)`.

For a matched state-compiler budget `m`, use

```math
t=
\min\left\{
 n,
 \max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\}.
```

The constant is not asymptotically important, but the repository keeps it
explicit so workspace assumptions remain auditable.

## 5. Remaining addressed layers

For each remaining nonfinal depth `d>=t`:

1. compute the lower-suffix-zero predicate into one reusable clean flag;
2. apply a uniformly controlled `R_y`, selected by the `d` prefix bits and the
   flag;
3. uncompute the flag.

The uniformly controlled gate has total width `d+2`. The final layer has no
lower suffix and uses the ordinary width `n` without a flag predicate.

The uniformly controlled-gate construction of Sun et al. has size `O(2**k)` and
depth

```math
O\left(k+\frac{2^k}{k+m}\right)
```

for a `k`-qubit UCG with `m` ancillary qubits. Exact multi-controlled-X
predicates have linear depth without extra workspace in the same circuit model.
The tail depth is therefore

```math
O\left(
 n(n-t+1)
 +
 \sum_{d=t}^{n-1}
 \frac{2^{d+O(1)}}{d+m+O(1)}
\right).
```

To bound the sum, split it at `n/2`. The upper half has denominator
`Omega(n+m)` and a geometric numerator, while the lower half is exponentially
smaller than the final scale. Hence

```math
\sum_{k=1}^{n}\frac{2^k}{k+m}
=O\left(\frac{2^n}{n+m}\right)
```

uniformly for `m>=0`. Therefore

```math
D_{\mathrm{tail}}
=O\left(
 n(n-t+1)+\frac{N}{n+m}
\right).
```

The UCG sizes sum geometrically. Predicate size is polynomial in `n` and hence
`O(N)`. The complete frame size is `O(N)`.

## 6. Candidate theorem

> **Clean ancilla--depth robustness of the real global frame.** Let `m>=0`, and
> choose `t` as above. In the exact all-to-all circuit model with arbitrary
> one-qubit gates and CNOTs, the addressed real Hopf frame has a clean
> implementation using at most `m+1` ancillary qubits, size `O(N)`, and depth
>
> ```math
> \boxed{
> D_{\mathrm{frame}}(n,m)
> =
> O\left(
> n(n-t+1)+\frac{N}{n+m}
> \right).
> }
> ```
>
> The possible extra qubit is the reusable tail suffix flag. It returns to zero
> after every layer. Reversing the circuit gives `W_R^dagger` with the same
> resources.

This is an upper-bound construction, not a new optimality statement.

## 7. Reduction to the older three regimes

### Low ancillary budget

For

```math
m=O\left(\frac{N}{n\log n}\right),
```

the sequential term is dominated by `N/(n+m)`, giving

```math
D_{\mathrm{frame}}(n,m)
=O\left(\frac{N}{n+m}\right).
```

### Intermediate budget

For

```math
m=\omega\left(\frac{N}{n\log n}\right),
\qquad
m=o(N),
```

we have `n-t=O(log n)`, so

```math
D_{\mathrm{frame}}(n,m)=O(n\log n).
```

### Linear or larger budget

For

```math
m=\Omega(N),
```

we have `n-t=O(1)`, and therefore

```math
D_{\mathrm{frame}}(n,m)=O(n).
```

These are the three upper profiles displayed for state preparation in the older
Sun et al. analysis. The later Yuan--Zhang result improves the intermediate QSP
benchmark; this construction does not yet match that improvement.

## 8. Separated complex frame

The portable complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

Exact diagonal synthesis has `O(N)` size and depth no larger than the relevant
state-preparation upper profiles when workspace is allocated appropriately. The
separated complex frame is therefore expected to inherit the same candidate
regimes. A manuscript theorem still needs a single common-workspace ledger
rather than two separately optimized statements.

The direct phase-gradient stream does not apply an inverse differential frame
and is unaffected by this compiler question.

## 9. Executable support

```text
compiler_robust_hopf/frames.py
compiler_robust_hopf/ancilla_depth.py
tests/test_frames.py
tests/test_ancilla_depth.py
scripts/ancilla_depth_ledger.py
```

Run:

```bash
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
```

The ledger reports exact structural quantities and unit-coefficient proxies for
asymptotic terms. It is not a finite elementary-gate depth estimator.

## 10. Boundaries

This companion does not establish:

- that an arbitrary state-preparation inverse is a valid Hopf reverse frame;
- the optimal all-ancilla depth frontier;
- a strict same-`m` statement rather than `m+1`;
- compiler-invariant checkpoint interfaces;
- approximate Clifford+T error propagation;
- routed-device depth or noise robustness;
- a theorem for arbitrary coordinate charts.
