# Ancilla--depth robustness of the global Hopf frame

## Status

The **real-frame theorem** on this page has passed an internal line-by-line proof
audit relative to the exact synthesis lemmas cited below. The audit found no
failure of the construction, but made two corrections:

1. the isolated unary prefix has size `O(2**t+n-t)`, not uniformly
   `O(2**t)`;
2. the workspace bound strengthens from `m+1` to `max(1,m)`.

Thus the construction uses the same `m` clean ancillary qubits as the matched
state compiler whenever `m>=1`; only the strict `m=0` endpoint uses one clean
suffix flag.

The separated complex-frame statement remains provisional until its blocks are
placed under one common workspace ledger. Reaching the later optimal
all-ancilla frontier is also a separate open target.

See [`PROOF_AUDIT_ISSUE_1.md`](PROOF_AUDIT_ISSUE_1.md) for the complete audit.

## 1. Setup

Let `n>=1` be the number of system qubits and

```math
N=2^n.
```

Write the addressed real Hopf frame as

```math
W_{\mathbb R}^{(n)}
=
L_{n-1}^{(n)}\cdots L_1^{(n)}L_0^{(n)}.
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
F_t^{(n)}
=
L_{t-1}^{(n)}\cdots L_0^{(n)}
```

and

```math
P_{n-t}
=
|0^{n-t}\rangle\!\langle0^{n-t}|.
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

For every `d<t`, the addressed condition in `L_d^(n)` requires all bits below
the depth-`d` target to be zero. On the external zero-suffix sector, the layer
is precisely `L_d^(t)` on the prefix. On the orthogonal suffix sector it is the
identity. The two sectors are invariant under every factor, so multiplying the
layers proves the identity.

This is a complete operator statement. It is stronger than equality on the
initialized state column.

## 3. Unary realization of the prefix frame

Let `E_t` encode the `t`-qubit computational basis into the
single-excitation code of `2**t` unary modes:

```math
E_t|r\rangle=|e_r\rangle.
```

Replace each computational two-level rotation in `W_R^(t)` by the same
number-preserving Givens rotation on the corresponding unary modes. Let the
resulting network be `G_t`. Then

```math
E_t^\dagger G_tE_t=W_{\mathbb R}^{(t)}
```

and

```math
\bigl(I-E_tE_t^\dagger\bigr)G_tE_t=0.
```

At a fixed tree depth, all mode pairs are disjoint. The unary frame is therefore
a sequence of `t` parallel Givens layers containing `2**t-1` logical rotations
in total.

A predicate-controlled two-mode Givens gate is a fixed three-qubit unitary, so
it has constant exact cost in the arbitrary-one-qubit-plus-CNOT model. Distinct
copies of the predicate control allow all Givens gates within one depth to run
in parallel.

## 4. Clean unary-prefix circuit

Lemma 28 of Sun et al. gives a clean unary-to-binary unitary on `2**t` register
qubits:

```math
|e_r\rangle
\longmapsto
|r\rangle|0^{2^t-t}\rangle.
```

It has depth `O(t)`, size `O(2**t)`, and uses `2**(t+1)` clean ancillary
qubits. Its inverse encodes a binary prefix into the unary register.

Use the first `t` system qubits as part of the unary register. The remaining
unary wires and conversion workspace require

```math
(2^t-t)+2^{t+1}
=
3\,2^t-t
```

ancillary qubits.

After the inverse conversion, the conversion workspace is clean. When `t<n`,
reuse part of it to compute the external-suffix-zero predicate, fan that
predicate out to distinct controls, apply the controlled Givens layers, and
uncompute both fanout and predicate. The unary-to-binary unitary then restores
all conversion workspace to zero.

The prefix resources are

```math
D_{\mathrm{prefix}}=O(n+t)=O(n)
```

and

```math
S_{\mathrm{prefix}}=O(2^t+n-t).
```

For a matched state-compiler budget `m`, choose

```math
t=
\min\left\{
n,
\max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\}.
```

This conservative choice guarantees `3*2**t-t<=m`.

## 5. Remaining addressed layers

For each remaining nonfinal depth `d>=t`:

1. compute the lower-suffix-zero predicate into one clean flag;
2. apply a uniformly controlled `R_y`, selected by the `d` prefix bits and the
   flag;
3. uncompute the predicate.

The UCG has `d` prefix controls, one flag control, and one target, so its total
width is

```math
k=d+2.
```

At the final depth `d=n-1`, there is no suffix predicate and the UCG width is
`n`.

For `m>=1`, reserve one of the `m` clean ancillary qubits as the nonfinal
suffix flag and apply the UCG synthesis theorem with the remaining `m-1`
workspace qubits. The final layer may use all `m`. At `m=0`, add one clean flag
and use zero UCG workspace.

Hence the total ancillary bound is

```math
a_{\mathrm{frame}}(m)=\max\{1,m\}.
```

The uniformly controlled-gate theorem gives depth

```math
O\left(k+\frac{2^k}{k+w}\right)
```

and size `O(2**k)` with `w` clean work qubits. The all-zero predicate is an
ancilla-free multi-controlled X, up to local `X` gates, and has linear depth and
size in the suffix width.

## 6. Uniform geometric estimate

For every `n>=1` and `s>=0`,

```math
\sum_{k=1}^{n}\frac{2^k}{k+s}
\leq
6\,\frac{2^n}{n+s}.
```

Split the sum at `h=floor(n/2)`. The upper half is at most
`4*2**n/(n+s)`. The lower half is at most `2**(h+1)/(s+1)`, which is no more
than `2*2**n/(n+s)` because

```math
\frac{n+s}{s+1}\leq n
```

and `n*2**(h+1-n)<=2`.

For the actual tail, the width shift from `d` to `d+2`, the replacement of
`m` by `m-1` on nonfinal layers, and the duplicate final-width contribution
change only the constant. Therefore all exponential UCG terms sum to

```math
O\left(\frac{N}{n+m}\right)
```

uniformly for all `m>=0`.

## 7. Audited real-frame theorem

> **Theorem (clean ancilla--depth robustness of the real global frame).**
> Let `n>=1`, `m>=0`, `N=2**n`, and choose `t` as in Section 4. In the exact
> all-to-all circuit model with arbitrary one-qubit gates and CNOTs, the
> addressed real Hopf frame has a frame-safe implementation using at most
> `max(1,m)` clean ancillary qubits, size
>
> ```math
> O(N),
> ```
>
> and depth
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
> For `m>=1`, the total workspace equals the matched state-compiler budget
> `m`. At `m=0`, the present construction uses one clean reusable suffix flag.
> Reversing the clean circuit implements `W_R^dagger` with the same resources.

The theorem is conditional only in the ordinary sense that it imports the
exact UCG, unary-to-binary, and multi-controlled-X synthesis theorems rather
than reproving their elementary circuits here. It is not an optimality theorem.

## 8. Reduction to the older three regimes

The theorem reproduces the three state-preparation upper profiles in the
Sun--Tian--Yang--Yuan--Zhang analysis.

### Low ancillary budget

For

```math
m=O\left(\frac{N}{n\log n}\right),
```

the sequential term is dominated by `N/(n+m)`, giving

```math
D_{\mathrm{frame}}
=
O\left(\frac{N}{n+m}\right).
```

### Intermediate ancillary budget

For

```math
m=\omega\left(\frac{N}{n\log n}\right),
\qquad
m=o(N),
```

we have `n-t=O(log n)`, so

```math
D_{\mathrm{frame}}=O(n\log n).
```

### Linear or larger ancillary budget

For `m=Omega(N)`, `n-t=O(1)`, and therefore

```math
D_{\mathrm{frame}}=O(n).
```

The later Yuan--Zhang state-preparation construction closes the intermediate
QSP gap. Whether the complete Hopf frame reaches that optimal frontier remains
open.

## 9. Separated complex frame

The portable complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

Exact diagonal synthesis has `O(N)` size and appropriate depth bounds in the
same circuit model. A complete complex theorem still requires one common
workspace schedule that treats `D_ph` and `W_R` together. That audit is tracked
separately and is not silently included in the real-frame theorem.

The direct complex phase-gradient stream does not apply an inverse differential
frame and is unaffected by this compiler question.

## 10. Executable support

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

The suite checks the exact Hopf identities, unary-code action and leakage,
workspace bookkeeping, endpoint cases, and the explicit uniform geometric
bound. It does not infer asymptotic correctness from finite scaling fits.

## 11. Boundaries

This theorem does not establish:

- that an arbitrary state-preparation inverse is a valid Hopf reverse frame;
- strict zero-extra-ancilla compilation at `m=0`;
- the optimal all-ancilla depth frontier;
- the common-workspace complex-frame theorem;
- compiler-invariant checkpoint interfaces;
- approximate Clifford+T error propagation;
- routed-device depth or noise robustness;
- finite optimal synthesis constants;
- a theorem for arbitrary coordinate charts.

## 12. Primary references

- X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang,
  [Asymptotically Optimal Circuit Depth for Quantum State Preparation and
  General Unitary Synthesis](https://arxiv.org/abs/2108.06150),
  *IEEE Transactions on Computer-Aided Design of Integrated Circuits and
  Systems* **42**, 3301--3314 (2023).
- P. Yuan and S. Zhang,
  [Optimal (controlled) quantum state preparation and improved unitary
  synthesis by quantum circuits with any number of ancillary
  qubits](https://arxiv.org/abs/2202.11302),
  *Quantum* **7**, 956 (2023).
