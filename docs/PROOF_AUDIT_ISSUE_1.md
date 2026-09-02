# Proof audit of the clean real-frame ancilla--depth theorem

## Audit status

Completed: 2026-09-02.

Scope: the exact **real global Hopf differential frame** in the all-to-all
circuit model with arbitrary one-qubit gates and CNOT gates.

Outcome:

- the conditioned-prefix and unary-frame constructions are correct;
- the depth bound survives a line-by-line re-derivation;
- the complete frame size remains `O(2**n)`;
- the workspace statement can be strengthened;
- one local size statement required correction.

The corrected theorem uses the same `m` clean ancillary qubits as the matched
state compiler whenever `m>=1`. At the strict `m=0` endpoint, the present
construction uses one reusable clean suffix flag. Thus the uniform workspace
bound is

```math
a_{\mathrm{frame}}(m)=\max\{1,m\},
```

rather than the previous, weaker `m+1` bound.

The unary prefix by itself has size

```math
O(2^t+n-t),
```

not uniformly `O(2^t)`, because its external-suffix predicate costs
`O(n-t)`. This correction does not change the complete `O(2**n)` frame-size
theorem.

The audit is a mathematical derivation relative to the exact synthesis lemmas
cited below. It does not reproduce their complete elementary circuits and is
not external peer review.

## 1. Statement audited

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

The audited real-frame theorem is:

> For every `n>=1` and `m>=0`, the addressed real Hopf frame
> `W_R^(n)` has an exact frame-safe implementation of size `O(N)` and depth
>
> ```math
> O\left(
> n(n-t+1)+\frac{N}{n+m}
> \right)
> ```
>
> using at most `max(1,m)` clean ancillary qubits. For `m>=1`, the total
> ancillary count is the same `m` used by the matched state-preparation
> benchmark. For `m=0`, the present construction uses one clean suffix flag.
> The inverse frame has the same resources.

“Frame-safe” means that for every system input,

```math
\widetilde W_{\mathbb R}
\bigl(|\varphi\rangle|0^a\rangle\bigr)
=
\bigl(W_{\mathbb R}|\varphi\rangle\bigr)|0^a\rangle.
```

The theorem is an upper-bound construction. It does not claim the later optimal
all-ancilla frontier.

## 2. Imported synthesis results

The audit uses the following exact results from Sun, Tian, Yang, Yuan, and
Zhang, arXiv:2108.06150v3 / IEEE TCAD 42, 3301--3314 (2023).

1. **Uniformly controlled gate, Lemma 12.** A `k`-qubit UCG has size
   `O(2**k)` and depth

   ```math
   O\left(k+\frac{2^k}{k+w}\right)
   ```

   with `w>=0` ancillary qubits.

2. **Unary-to-binary unitary, Lemma 28.** On `2**t` register qubits, the
   basis transformation

   ```math
   |e_r\rangle
   \longmapsto
   |r\rangle|0^{2^t-t}\rangle
   ```

   for every one-excitation basis state has depth `O(t)`, size `O(2**t)`,
   and uses `2**(t+1)` clean ancillary qubits.

3. **Ancilla-free multi-controlled X, Lemma 41.** A multi-controlled X on
   `s` controls and one target has depth and size `O(s)` without ancillary
   qubits.

The paper defines ancillary workspace as initialized and restored to zero. Its
Appendix K also exhibits the reset operations inside the unary-to-binary
construction. The present proof uses those clean-output properties, not merely
a state-preparation promise.

## 3. Conditioned-prefix operator identity

Write

```math
W_{\mathbb R}^{(n)}
=
L_{n-1}^{(n)}\cdots L_0^{(n)},
```

where `L_d^(n)` is the addressed Hopf layer at tree depth `d`. For
`0<=t<=n`, define

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
F_t^{(n)}
=
W_{\mathbb R}^{(t)}\otimes P_{n-t}
+
I_{2^t}\otimes(I-P_{n-t}).
```

### Independent derivation

At depth `d<t`, each addressed rotation acts between

```math
|r\,0\,0^{n-d-1}\rangle
\quad\text{and}\quad
|r\,1\,0^{n-d-1}\rangle.
```

The final `n-t` bits are therefore zero for every basis state touched by the
layer. On the external zero-suffix sector, the remaining condition and basis
pair are exactly those of the `t`-qubit layer `L_d^(t)`. On the orthogonal
external-suffix sector, the full layer is the identity. Hence

```math
L_d^{(n)}
=
L_d^{(t)}\otimes P_{n-t}
+
I_{2^t}\otimes(I-P_{n-t}).
```

Both suffix sectors are invariant under every factor. Multiplying the factors
gives the claimed identity. No initialized-state-column argument is used.

Classification: **proved**.

Finite support: every cut through `n=8` is checked against an independently
constructed recursive frame.

## 4. Unary-code realization and ordering

Let `E_t` embed the binary basis into the one-excitation code of `2**t`
unary modes:

```math
E_t|r\rangle=|e_r\rangle.
```

For every addressed computational pair `(a,b)`, place the same Hopf rotation on
unary modes `(a,b)`, acting as identity on `|00>` and `|11>` and as the
Hopf `R_y` block on the ordered one-excitation pair. Call the complete unary
network `G_t`.

Each unary gate preserves Hamming weight. Therefore the one-excitation code is
invariant and there is no leakage. Restricted to that code, each gate acts
exactly as the corresponding computational two-level rotation. Applying tree
depths in the same increasing-depth order gives

```math
E_t^\dagger G_tE_t=W_{\mathbb R}^{(t)},
```

and

```math
(I-E_tE_t^\dagger)G_tE_t=0.
```

At a fixed depth, the addressed pairs are disjoint. The entire depth is
therefore executable in parallel once each gate has a distinct copy of the
common predicate control.

Classification: **proved**.

Finite support: complete unary-Hilbert-space checks through `t=3`, plus a
combinatorial disjoint-pair check through `t=8`.

## 5. Unary register and workspace ledger

Use the first `t` system qubits as part of a `2**t`-wire unary register `A`.
The remaining unary wires require

```math
2^t-t
```

ancillary qubits. Lemma 28 uses a second register `B` of

```math
2^{t+1}
```

clean ancillary qubits. The total additional workspace for the conversion is

```math
(2^t-t)+2^{t+1}
=
3\,2^t-t.
```

The conservative choice of `t` ensures

```math
3\,2^t-t\leq m.
```

Let `U_t` denote the unary-to-binary unitary. Lemma 28 gives, on the complete
one-excitation code,

```math
U_t
\bigl(|e_r\rangle_A|0\rangle_B\bigr)
=
|r\rangle|0^{2^t-t}\rangle_A|0\rangle_B.
```

Taking the inverse gives

```math
U_t^\dagger
\bigl(|r\rangle|0^{2^t-t}\rangle_A|0\rangle_B\bigr)
=
|e_r\rangle_A|0\rangle_B.
```

By linearity, this holds for arbitrary superpositions and for states entangled
with the untouched external suffix. Thus `B` is clean immediately after the
binary-to-unary encoding and can be reused temporarily.

When `t<n`, use clean wires in `B` to:

1. compute the external-suffix-zero predicate;
2. fan it out coherently to distinct controls;
3. execute the controlled unary Givens layers;
4. undo the fanout and predicate.

The unary network preserves the code and never targets those controls. After
uncomputation, `B` is again zero, so `U_t` can decode the unary register and
return all conversion workspace to zero.

Classification: **proved**.

Correction: the isolated prefix size is

```math
O(2^t+n-t),
```

because predicate computation and uncomputation cost `O(n-t)`. The complete
frame size remains `O(N)`.

## 6. Controlled Givens gates

A two-mode number-preserving Givens gate acts on two qubits. Adding one
predicate control produces a fixed three-qubit unitary. Any fixed-width unitary
has an exact constant-size, constant-depth decomposition in the declared gate
model. No asymptotically growing ancillary workspace is required.

After coherent fanout, different Givens gates in one tree layer have distinct
control copies and disjoint target pairs. They can therefore be executed in
parallel.

Classification: **proved**.

Boundary: no particular finite CNOT-optimal three-qubit decomposition is
claimed.

## 7. Suffix-zero predicates

For a suffix of width `s`, apply `X` to every suffix qubit, use an
`s`-controlled X into a clean flag, and undo the `X` gates. By Lemma 41 this
has depth and size `O(s)` without additional workspace.

The subsequent UCG leaves the suffix unchanged and uses the flag only as a
logical control. Its workspace is returned to zero. Reversing the predicate
circuit therefore resets the flag exactly, including when the system is in a
superposition across suffix sectors.

Classification: **proved**.

## 8. Tail UCG widths and same-`m` workspace

At a nonfinal depth `d`, the UCG has:

- `d` prefix controls;
- one suffix flag control;
- one target.

Its total width is

```math
k=d+2.
```

At the final depth `d=n-1`, there is no lower suffix, so there are
`n-1` prefix controls and one target:

```math
k=n.
```

For `m>=1`, reserve one of the `m` clean ancillary qubits as the suffix flag
during every nonfinal tail layer. Apply Lemma 12 with the remaining `m-1`
ancillary qubits. The final layer needs no flag and may use all `m`. All these
blocks are sequential and clean, so the same register is reused at every
depth.

For `m=0`, add one reusable flag and invoke the UCG compiler with zero work
ancillas.

Therefore the total workspace is

```math
\max\{1,m\}.
```

Classification: **corrected and strengthened**. The prior `m+1` statement was
valid but unnecessarily loose.

## 9. Uniform geometric-tail bound

The required denominator shift is harmless. The base estimate is the following
uniform inequality for every `n>=1` and `s>=0`:

```math
\sum_{k=1}^{n}\frac{2^k}{k+s}
\leq
6\,\frac{2^n}{n+s}.
```

### Proof

Let `h=floor(n/2)`. For the upper half,

```math
\sum_{k=h+1}^{n}\frac{2^k}{k+s}
\leq
\frac{2}{n+s}\sum_{k=h+1}^{n}2^k
\leq
4\,\frac{2^n}{n+s}.
```

For the lower half,

```math
\sum_{k=1}^{h}\frac{2^k}{k+s}
\leq
\frac{2^{h+1}}{s+1}.
```

Since

```math
\frac{n+s}{s+1}\leq n
```

and

```math
n\,2^{h+1-n}\leq2,
```

the lower half is at most

```math
2\,\frac{2^n}{n+s}.
```

Adding both halves proves the inequality.

For nonfinal tail layers, `s=max(0,m-1)` and the UCG width is shifted from
`d` to `d+2`. The geometric numerator shift contributes only a constant.
When `m>=1`,

```math
\frac{1}{n+m-1}
\leq
\frac{2}{n+m}.
```

The final width-`n` layer contributes one additional term of the target order.
Consequently all exponential UCG terms sum to

```math
O\left(\frac{N}{n+m}\right)
```

uniformly for every `m>=0`.

Classification: **proved**.

The code now exposes and tests the explicit constant-6 base inequality through
broad endpoint and intermediate grids.

## 10. Depth and size summation

The unary prefix has:

```math
D_{\mathrm{prefix}}=O(n+t)=O(n),
```

and corrected size

```math
S_{\mathrm{prefix}}=O(2^t+n-t).
```

The nonfinal predicate depths sum to

```math
O\left(
\sum_{d=t}^{n-2}(n-d-1)
\right)
=
O((n-t)^2).
```

The linear UCG terms sum to

```math
O\left(
\sum_{d=t}^{n-1}(d+2)
\right)
=
O(n(n-t+1)).
```

The geometric terms were bounded in Section 9. Hence

```math
D_{\mathrm{frame}}(n,m)
=
O\left(
n(n-t+1)+\frac{N}{n+m}
\right).
```

The UCG sizes form a geometric series of order `O(N)`. Prefix and predicate
sizes are at most `O(N)`, so

```math
S_{\mathrm{frame}}(n,m)=O(N).
```

Classification: **proved relative to the imported synthesis lemmas**.

## 11. Endpoint audit

| Endpoint | Result |
|---|---|
| `t=0` | No unary prefix. Every frame layer is in the flagged/UCG tail. |
| `t=n` | The conditioned prefix is the complete frame. There is no suffix predicate or tail. |
| `m=0`, `n>1` | One additional clean flag is used; every UCG receives zero work ancillas. |
| `m=0`, `n=1` | The frame is one local rotation; the uniform one-ancilla bound is not tight. |
| `m=1` | The single ancillary qubit is the suffix flag; nonfinal UCGs use zero work ancillas. |
| small `n` | Absorbed by the theorem constants and explicitly exercised by the deterministic suite. |
| `m\gg N` | Clamp `t=n` and ignore surplus workspace; depth is `O(n)`. |

Classification: **proved**.

## 12. Older three-regime reduction

The audited theorem reproduces the three state-preparation upper profiles in
Sun et al.

### Low ancillary budget

For

```math
m=O\left(\frac{N}{n\log n}\right),
```

the sequential term is dominated by `N/(n+m)`. If `m<n`, this follows from
`n^3=O(2^n)`. If `m>=n`, set `f=N/m`; the regime gives
`f=Omega(n log n)`, while

```math
n(n-t+1)=O(n\log f)=O(f).
```

Thus

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

we have

```math
n-t
=
O\left(1+\log\frac{N}{m}\right)
=
O(\log n).
```

Therefore

```math
D_{\mathrm{frame}}=O(n\log n).
```

### Linear or larger ancillary budget

For `m=Omega(N)`, `n-t=O(1)`, so

```math
D_{\mathrm{frame}}=O(n).
```

Classification: **proved**.

This does not close the intermediate gap removed for state preparation by the
later Yuan--Zhang construction.

## 13. Audit classification

| Required check | Classification | Note |
|---|---|---|
| Conditioned-prefix operator identity | Proved | Complete operator identity, not state-column equality |
| Unary Givens action and ordering | Proved | Exact on the complete one-excitation code |
| Unary-code no leakage | Proved | Every gate preserves excitation number |
| Lemma 28 register count | Proved | `3*2**t-t` additional wires |
| Conversion workspace clean before reuse | Proved | Follows from the clean unitary mapping and its inverse |
| Controlled-Givens constant-width assumption | Proved | Fixed three-qubit unitary |
| Suffix-zero predicate and uncomputation | Proved | Negative controls plus Lemma 41 |
| UCG width at each tail depth | Proved | `d+2` nonfinal, `n` final |
| Uniform geometric-tail estimate | Proved | Explicit constant-6 base inequality |
| Endpoint cases | Proved | Includes `m=0`, `m=1`, `t=0`, `t=n`, and surplus workspace |
| Uniform `m+1` workspace statement | Corrected | Strengthened to `max(1,m)` |
| Isolated prefix size `O(2**t)` | Corrected | Correct form is `O(2**t+n-t)` |

## 14. What remains outside this audit

The following are not defects in the audited real-frame theorem, but they
remain separate research or release gates:

- an explicit elementary implementation of every imported synthesis block;
- finite optimal CNOT and depth constants;
- strict zero-extra-ancilla compilation at `m=0`;
- the common-workspace complex-frame theorem;
- the optimal all-ancilla frontier
  `Theta(n+2**n/(n+m))`;
- approximate Clifford+T synthesis and error propagation;
- routed-device depth and noise;
- compiler-invariant checkpoint interfaces;
- external human or peer review.

## 15. Reproduction

```bash
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
```

The deterministic suite checks the exact Hopf identities, endpoint bookkeeping,
the corrected workspace ledger, and the uniform geometric-tail inequality. The
asymptotic conclusion still rests on the cited synthesis theorems rather than on
finite numerical scaling fits.
