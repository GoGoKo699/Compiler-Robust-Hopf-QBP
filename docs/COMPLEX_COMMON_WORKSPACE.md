# Common-workspace theorem for the separated complex Hopf frame

## Status

Completed internally: 2026-09-02.

This document closes the internal common-workspace audit requested in Issue #3.
It combines the audited real-frame compiler with an exact arbitrary-diagonal
compiler under one clean ancillary pool. The result is a theorem relative to
the exact synthesis lemmas imported from Sun, Tian, Yang, Yuan, and Zhang. It is
not external peer review and does not establish the later optimal all-ancilla
frontier for the complete frame.

The principal conclusion is:

> For every matched workspace budget `m>=1`, the separated complex Hopf frame
> `W_C = D_ph W_R` has an exact frame-safe implementation using the same `m`
> clean ancillary qubits, size `O(2**n)`, and the same audited asymptotic depth
> bound as the real frame. At the nominal `m=0` endpoint, the sharp-size
> construction uses one reusable real-frame flag. A strict zero-ancilla
> fallback also exists, with depth `O(2**n)` and size `O(n*2**n)`.

## 1. Setup

Let

```math
N=2^n,
\qquad n\geq1.
```

The separated complex Hopf frame is

```math
W_{\mathbb C}(\boldsymbol\theta,\boldsymbol\phi)
=
D_{\mathrm{ph}}(\boldsymbol\phi)
W_{\mathbb R}(\boldsymbol\theta),
```

where

```math
D_{\mathrm{ph}}(\boldsymbol\phi)
=
\sum_{x=0}^{N-1}e^{i\phi_x}|x\rangle\!\langle x|.
```

The real frame contains the real Hopf state in column zero and normalized
magnitude-coordinate directions in its marker columns. Multiplication by the
diagonal phase layer produces the complex Hopf state and phase-dressed
magnitude directions:

```math
W_{\mathbb C}|0\rangle
=|\psi_{\mathbb C}\rangle,
```

```math
\partial_{\theta_j}|\psi_{\mathbb C}\rangle
=
\sqrt{g_{j,j}}\,
W_{\mathbb C}|\lambda(j)\rangle.
```

Thus the global complex magnitude protocol requires the inverse of the complete
operator `W_C`, not only a circuit preparing its first column.

## 2. Exact arbitrary-diagonal synthesis for every workspace budget

The diagonal results in Sun et al. are stated for matrices whose first entry is
one:

```math
\Lambda_n
=
\mathrm{diag}
\bigl(1,e^{i\vartheta_1},\ldots,e^{i\vartheta_{N-1}}\bigr).
```

An arbitrary Hopf phase layer factors exactly as

```math
D_{\mathrm{ph}}(\boldsymbol\phi)
=
e^{i\phi_0}
\Lambda_n(\boldsymbol\phi-\phi_0\mathbf 1).
```

The scalar factor `e^(i phi_0) I` is implemented by one arbitrary one-qubit
scalar-phase gate. Keeping this gate gives full operator equality rather than
only equality modulo global phase. This is conservative for the Hopf gradient
protocol, where a system-wide global phase would not change the final
measurement distribution.

### Imported diagonal results

For an `n`-qubit diagonal of the normalized form above, Sun et al. prove:

1. with `w` ancillary qubits satisfying

   ```math
   2n\leq w\leq\frac{N}{n},
   ```

   exact depth

   ```math
   O\left(\log w+\frac{N}{w}\right)
   ```

   and size `O(N)`;

2. with no ancillary qubits, exact depth

   ```math
   O\left(\frac{N}{n}\right)
   ```

   and size `O(N)`.

The ancillary construction ends by undoing the copy and phase registers. Hence
it is a clean operator implementation on arbitrary superpositions, not merely a
state-preparation routine.

### All-budget choice

Given any available budget `m>=0`, choose the diagonal workspace `w` by:

```math
w=
\begin{cases}
0,
& m<2n,\\[0.4em]
\min\left\{m,\left\lfloor N/n\right\rfloor\right\},
& m\geq2n
\text{ and }
\left\lfloor N/n\right\rfloor\geq2n,\\[0.4em]
0,
& \left\lfloor N/n\right\rfloor<2n.
\end{cases}
```

Surplus ancillary qubits are simply left unused.

### Uniform diagonal bound

This piecewise schedule gives, for every `n>=1` and `m>=0`,

```math
\boxed{
D_{\mathrm{diag}}(n,m)
=
O\left(
n+rac{N}{n+m}
\right),
}
```

```math
\boxed{
S_{\mathrm{diag}}(n,m)=O(N),
}
```

using at most `m` clean ancillary qubits.

#### Proof

If `m<2n`, use the no-ancilla circuit. Since `n+m<3n`,

```math
\frac{N}{n}
<
3\frac{N}{n+m}.
```

If the ancillary interval is empty, then `N/n<2n`, so `N/n=O(n)` and the
same target bound follows.

If `2n<=m<=N/n`, the ancillary circuit has depth

```math
O\left(\log m+\frac{N}{m}\right).
```

Here `log m<=n`, and `m>=2n` implies `n+m<=3m/2`, so

```math
\frac{N}{m}
\leq
\frac{3N}{2(n+m)}.
```

If `m>N/n`, use only `w=floor(N/n)` ancillary qubits. Then

```math
\log w=O(n),
\qquad
\frac{N}{w}=O(n),
```

and the depth is `O(n)`. The target expression is at least `n`.

The size remains `O(N)` in every case. In the ancillary construction, the
explicit finite expression

```math
3N+nw+\frac{7w}{2}
```

is `O(N)` because `w<=N/n`. The common-phase gate adds only constant size and
depth.

## 3. Clean workspace composition

The audited real-frame theorem gives, for

```math
t=
\min\left\{
n,
\max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\},
```

an exact frame-safe real implementation of size `O(N)` and depth

```math
D_{\mathbb R}(n,m)
=
O\left(
n(n-t+1)+\frac{N}{n+m}
\right).
```

Its workspace is

```math
a_{\mathbb R}(m)=\max\{1,m\}.
```

For `m>=1`, it uses the same `m` clean ancillary qubits as the matched state
compiler. Every real-frame block returns that pool to zero.

The diagonal circuit from Section 2 uses `w<=m` of the same qubits and returns
them to zero. The blocks are sequential, so their workspace requirements are
not added. The schedule is simply

```text
real frame W_R
-> clean workspace
-> diagonal D_ph
-> clean workspace.
```

Its inverse is the reverse clean schedule

```text
D_ph dagger
-> clean workspace
-> W_R dagger
-> clean workspace.
```

Therefore the complete composed operation satisfies, for every system input,

```math
\widetilde W_{\mathbb C}
\bigl(|\varphi\rangle|0^a\rangle\bigr)
=
\bigl(W_{\mathbb C}|\varphi\rangle\bigr)|0^a\rangle.
```

It is frame-safe in exactly the sense required by the global substitution
theorem.

## 4. Main complex-frame theorem

> **Theorem (common-workspace separated complex Hopf frame).** Let `n>=1`,
> `m>=0`, `N=2**n`, and let `t` be defined as in Section 3. In the exact
> all-to-all circuit model with arbitrary one-qubit gates and CNOTs, the
> separated complex Hopf frame
>
> ```math
> W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
> ```
>
> has an exact frame-safe implementation using at most
>
> ```math
> \max\{1,m\}
> ```
>
> clean ancillary qubits, size
>
> ```math
> O(N),
> ```
>
> and depth
>
> ```math
> \boxed{
> D_{\mathbb C}(n,m)
> =
> O\left(
> n(n-t+1)+\frac{N}{n+m}
> \right).
> }
> ```
>
> For every `m>=1`, the complete real and diagonal blocks reuse the same `m`
> clean ancillary qubits. At the nominal `m=0` endpoint, the sharp-size
> construction uses one reusable clean flag in the real block and no workspace
> in the diagonal block. The inverse frame has the same resources.

### Proof

The operator identity follows from the exact composition
`W_C=D_ph W_R`. Cleanliness follows because both blocks implement their full
system operators on arbitrary inputs and return their workspace to zero. The
workspace maximum is therefore the maximum, not the sum, of the two block
requirements.

The sizes add to `O(N)`. The depths add to

```math
O\left(
n(n-t+1)+\frac{N}{n+m}
\right)
+
O\left(n+\frac{N}{n+m}\right).
```

Since `n(n-t+1)>=n`, the second term is absorbed by the first. Reversing the
clean circuit preserves size, depth, and workspace.

## 5. Strict zero-ancilla fallback

The sharp `O(N)`-size theorem uses one real-frame flag when the matched budget
is `m=0`. A separate exact construction removes even that qubit at the cost of
larger circuit size.

At depth `d`, choose the depth-`d` target as the UCG target and treat every other
system qubit as a control. For a complete control string, assign:

- the Hopf angle selected by the upper prefix when the lower suffix is zero;
- angle zero otherwise.

The resulting full-width `n`-qubit UCG is exactly the addressed layer. Wire
relabeling is free in the declared all-to-all logical model. Applying the
zero-workspace UCG theorem to every one of the `n` layers gives

```math
D_{\mathbb R}^{(0)}
=
O\left(
n\left(n+\frac{N}{n}\right)
\right)
=
O(N),
```

and

```math
S_{\mathbb R}^{(0)}=O(nN).
```

Adding the no-ancilla diagonal circuit gives:

> **Proposition (strict zero-ancilla complex fallback).** The exact separated
> complex frame has a zero-ancilla implementation of depth `O(N)` and size
> `O(nN)`.

This fallback resolves exact feasibility at strict zero workspace. It does not
replace the sharp-size theorem, and it is not the preferred matched-resource
implementation for Hopf backpropagation.

## 6. Reduction to the older Figure 1 profiles

Because the diagonal term is absorbed by the audited real-frame depth, the
complex theorem reproduces exactly the same older state-preparation upper
profiles.

### Low ancillary budget

For

```math
m=O\left(\frac{N}{n\log n}\right),
```

```math
D_{\mathbb C}
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

```math
D_{\mathbb C}=O(n\log n).
```

### Linear or larger ancillary budget

For `m=Omega(N)`,

```math
D_{\mathbb C}=O(n).
```

The theorem therefore answers the original Figure 1 compiler-family question
for the separated complex global frame as well as for the real frame. It does
not close the later Yuan--Zhang optimal all-ancilla gap in the intermediate
workspace range.

## 7. Phase parameters and preprocessing

For the normalized phase function

```math
f(x)=\phi_x-\phi_0,
\qquad
f(0)=0,
```

the diagonal construction uses parity phases

```math
f(x)
=
\sum_{s\neq0}\alpha_s
\bigl(\langle s,x\rangle\bmod2\bigr).
```

Writing

```math
\widehat f(s)
=
\sum_x f(x)(-1)^{\langle s,x\rangle},
```

one obtains, for `s!=0`,

```math
\alpha_s
=
-\frac{2}{N}\widehat f(s).
```

Thus all compiler phase parameters can be generated by one fast
Walsh--Hadamard transform in

```math
O(Nn)
```

classical arithmetic and `O(N)` storage. The inverse diagonal uses the same
parameters with signs reversed. No second asymptotic preprocessing pass is
required for `D_ph^dagger`.

The repository implements and exactly checks this transform against the direct
parity expansion.

## 8. Common phase, gauge, and singular leaves

### Common phase

A uniform shift `phi_x -> phi_x+c` gives

```math
W_{\mathbb C}(\boldsymbol\phi+c\mathbf 1)
=
e^{ic}W_{\mathbb C}(\boldsymbol\phi).
```

Expectation objectives are unchanged. The exact compiler nevertheless retains
the scalar phase gate so the operator contract is not weakened silently.

### Null phase direction

The phase derivatives are

```math
\partial_{\phi_\ell}|\psi\rangle
=
i\psi_\ell|\ell\rangle.
```

Summing them gives

```math
\sum_\ell\partial_{\phi_\ell}|\psi\rangle
=i|\psi\rangle.
```

For a Hermitian observable, the corresponding total phase gradient is

```math
2\mathrm{Re}
\langle i\psi|O|\psi\rangle
=0.
```

The exact phase-gradient block therefore lies in the zero-sum subspace. A
finite-shot estimate may be projected onto that subspace without bias.

### Zero-amplitude leaves

If `psi_l=0`, then

```math
\partial_{\phi_\ell}|\psi\rangle=0
```

and the exact phase derivative of every expectation objective is zero. The
phase estimator requires no division by `psi_l`, so singular leaves introduce
no algebraic instability. The complete frame `D_ph W_R` remains unitary even
when one or more state amplitudes vanish.

These properties are geometric consequences of the complex Hopf coordinates;
they do not depend on the elementary diagonal compiler.

## 9. End-to-end complex gradient accounting

The complete complex gradient uses two logically distinct streams.

### Magnitude stream

```text
complex forward preparation
-> controlled observable
-> D_ph dagger
-> W_R dagger
-> global X-basis measurement.
```

Equivalently, the reverse block is `W_C^dagger`. It uses one compiled complex
frame inverse per execution. The output-sensitive record-wise Walsh decoder
costs

```math
O(S_{\mathrm{mag}}N)
```

for `S_mag` outcomes, with `O(N)` storage.

### Direct phase stream

```text
complex forward preparation
-> controlled observable
-> ancilla-Y and system-Z measurement.
```

It applies no inverse differential frame. One outcome contributes the norm-two
signed one-hot record

```math
2(-1)^b e_\ell.
```

Accumulating `S_ph` outcomes costs

```math
O(S_{\mathrm{ph}}+N)
```

arithmetic and `O(N)` storage.

The compiler theorem on this page affects the magnitude reverse block. The
direct phase stream inherits only the chosen forward-preparation cost.

At fixed simultaneous absolute coordinatewise accuracy and confidence, the
magnitude family retains the previously established

```math
S_{\mathrm{mag}}
=
O(\log n)
=
O(\log\log M)
```

execution scaling, while the separate phase family contributes no additional
factor growing with the number of Hopf tree depths. The exact allocation of
accuracy and failure probability between the two streams should be stated in
the final manuscript.

## 10. Matched scalar comparison

An arbitrary complex Hopf state is an arbitrary `n`-qubit pure state. The
optimal state-preparation benchmark with `m` ancillary qubits is

```math
D_{\mathrm{QSP}}(n,m)
=
\Theta\left(
n+rac{N}{n+m}
\right),
```

with size `Theta(N)`.

The uniform frame-to-state depth comparison needs two cases.

If

```math
m\leq\frac{N}{n^2},
```

the geometric term is at least of order `n**2` and absorbs the sequential
`O(n**2)` term. The depth ratio is `O(1)`.

If

```math
m>\frac{N}{n^2},
```

then

```math
\log_2m>n-2\log_2n,
```

so `n-t=O(log n)`. Writing `G=N/(n+m)`,

```math
\frac{n(n-t+1)+G}{n+G}
\leq n-t+1
=
O(\log n).
```

Therefore, uniformly over every ancillary budget,

```math
\boxed{
\frac{D_{\mathbb C}(n,m)}
{D_{\mathrm{QSP}}(n,m)}
=O(\log n).
}
```

For `M=Theta(N)` Hopf coordinates, this compiler-depth overhead is

```math
O(\log\log M).
```

The sharp-size construction has constant asymptotic size ratio to optimal state
preparation. The stronger question of eliminating the remaining intermediate
`O(log n)` depth factor is the optimal all-ancilla target tracked separately.

## 11. Evidence map

| Statement | Status | Support |
|---|---|---|
| `W_C=D_ph W_R` is unitary and contains the phase-dressed magnitude directions | Proved algebraically and checked exactly | `frames.py`, `complex_analysis.py`, tests |
| Arbitrary diagonal has an all-budget clean `O(N)`-size compiler | Imported synthesis theorems plus piecewise reduction | Sun et al. Lemmas 10, 11, and Lemma 20 cleanup |
| Common workspace is `max(1,m)` | Proved by sequential clean reuse | real audit plus `complex_resources.py` |
| Complex depth equals the real asymptotic bound | Proved by absorption of the diagonal term | this document and resource ledger |
| Strict zero-ancilla fallback has depth `O(N)`, size `O(nN)` | Proved using one full-width UCG per addressed layer | `complex_resources.py`, exact layer tests |
| Common phase is gauge and phase gradients sum to zero | Proved algebraically and checked | `complex_analysis.py`, tests |
| Zero-amplitude phase derivatives vanish | Proved directly and checked | `complex_analysis.py`, tests |
| Phase parameter transform costs `O(Nn)` | Explicit FWHT construction and exact reconstruction tests | `complex_analysis.py`, tests |
| Direct phase sample decoder costs `O(S+N)` | Direct signed-bin accumulation and tests | `decoders.py`, tests |

## 12. Boundaries

This theorem does not establish:

- that every state-equivalent complex state-preparation compiler is frame-safe;
- the optimal all-ancilla depth of the complete Hopf frame;
- `O(N)` size and strict zero additional workspace simultaneously at `m=0`;
- compiler-invariant checkpoint interfaces;
- approximate Clifford+T phase-synthesis error bounds;
- routed-device depth or noise robustness;
- finite CNOT-optimal constants;
- a theorem for arbitrary coordinate charts.

## 13. Executable support

```text
compiler_robust_hopf/complex_analysis.py
compiler_robust_hopf/complex_resources.py
compiler_robust_hopf/decoders.py
tests/test_complex_analysis.py
tests/test_complex_resources.py
tests/test_decoders.py
scripts/complex_workspace_ledger.py
```

Run:

```bash
python validate.py
python scripts/complex_workspace_ledger.py --n 10
python scripts/complex_workspace_ledger.py --n 12 --ancillas 0,1,24,256,4096
```

The numeric ledger columns expose asymptotic terms and finite parameter counts.
They are not claims of exact gate-optimal depth or size.

## 14. Primary references

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
