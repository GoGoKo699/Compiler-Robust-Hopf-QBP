# Unified all-workspace compiler for Hopf differential frames

## Status

This document gives the active compiler architecture of the project. It uses
one external compiler framework—Yuan and Zhang, *Quantum* **7**, 956 (2023)—and
three Hopf-specific internal schedules covering every clean-workspace budget.

The resulting all-workspace theorem has passed internal proof audits and exact
finite validation. It has not received independent external proof review.

## 1. Result

Let

```math
N=2^n.
```

For every integer `m>=0`, the complete real Hopf differential frame has an exact
frame-safe implementation using at most `m` clean ancillary qubits with

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

has the same size, depth, and workspace frontier.

The compiler selects among three internal schedules:

| Workspace | Schedule |
|---:|---|
| `m=0` | borrowed-suffix half-angle echo |
| small positive `m` | direct flagged UCGs |
| larger `m` | tree-decoder routed parallel subframes |

These are components of one Hopf-frame compiler, not a choice between two prior
state-preparation papers.

## 2. Yuan--Zhang results used

The active proof uses the following statements from Yuan and Zhang.

| Result | Role |
|---|---|
| Standard circuit model | arbitrary one-qubit gates, CNOTs, clean ancillary qubits, all-to-all logical connectivity |
| Lemma 5 | exact ancilla-free multi-controlled X with linear size and depth |
| Lemma 6 | exact total-width-`q` UCG with size `O(2**q)` and depth `O(q+2**q/(q+w))` using `w` ancillary qubits |
| Lemma 9 | coherent CNOT-tree copy--use--uncopy in logarithmic depth |
| Theorem 1 | generic controlled-state-preparation comparison |
| Theorem 2 | optimal arbitrary-state-preparation size and depth for every ancillary budget |

The earlier Sun--Tian--Yang--Yuan--Zhang paper remains a historical and
original-source citation. It is not an alternative active compiler path.

## 3. Addressed Hopf frame

Write the real frame as

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_1^{(n)}L_0^{(n)}.
```

At depth `d`, let `p` be the `d`-bit upper prefix, let the next qubit be the
target, and let `z` be the lower suffix of length

```math
s=n-d-1.
```

The addressed layer applies the prefix-selected rotation only on the zero-suffix
sector:

```math
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^s\rangle\!\langle0^s|.
```

The compiler problem is to implement this complete operator, not only its
action on the forward state-preparation input.

## 4. Schedule Z: strict-zero borrowed-suffix echo

Assume `m=0` and `d<n-1`. Split the lower suffix as one borrowed system qubit
`b` followed by the remaining suffix `r`. Define

```math
h(r)=[r=0],
```

```math
C_p=R_y(\theta_{d,p}/2),
```

and let `T_h` toggle `b` iff `h(r)=1`.

Use the chronological circuit

```text
controlled_b(X)
T_h
controlled_b(C_p)
T_h
controlled_b(X)
T_h
controlled_b(C_p)
T_h.
```

The controlled `C_p` operation is one UCG whose controls are the `d` prefix
qubits and the borrowed bit; its target is the Hopf target. The remaining suffix
qubits are idle during that UCG.

### 4.1 Complete-operator proof

The Hopf convention is

```math
R_y(\alpha)=e^{-i\alpha Y}
=
\begin{pmatrix}
\cos\alpha&-\sin\alpha\\
\sin\alpha&\cos\alpha
\end{pmatrix}.
```

Therefore

```math
C_p^2=R_y(\theta_{d,p}),
```

```math
X C_p X=C_p^{-1},
```

and

```math
C_pXC_pX=I.
```

Fix a prefix `p` and remaining suffix `r`. The target word and final borrowed
bit in each sector are:

| `h(r)` | initial `b` | chronological target word | final target action | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_pXC_pX=I` | 1 |
| 1 | 0 | `C_p,C_p` | `C_p^2=R_y(theta)` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

Thus the desired rotation occurs exactly when the **original** complete suffix
is zero. Every other sector receives identity. The borrowed system qubit is
restored and no sector-dependent phase appears.

The prefix and remaining suffix label mutually orthogonal invariant sectors, so
this proves equality as a complete operator on arbitrary superpositions and
entangled inputs.

### 4.2 No hidden workspace

`T_h` is a zero-controlled multi-controlled X whose target is the borrowed
system wire. Negative controls are converted to ordinary controls by parallel X
wrappers. Yuan--Zhang Lemma 5 supplies an exact implementation using no
ancillary qubit.

The half-angle UCG acts only on:

- `d` prefix controls;
- one borrowed-bit control;
- one target.

Its total width is therefore

```math
q=d+2.
```

The borrowed bit is data, not a clean or dirty ancillary wire. It is part of the
original system and the complete-operator identity proves its exact restoration.

### 4.3 Strict-zero size and depth

Yuan--Zhang Lemma 6 gives, at zero ancillary workspace,

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^d),
```

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^d}{d+2}\right).
```

Four predicate toggles contribute `O(n-d)` size and depth; the two target echoes
are CNOTs. Hence

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

The final depth has no lower suffix and is compiled as one ordinary `n`-qubit
UCG. Therefore

```math
\begin{aligned}
S(W_{\mathbb R})
&=O\left(
\sum_{d=0}^{n-2}2^d
+\sum_{d=0}^{n-2}(n-d)
+N
\right)\\
&=O(N).
\end{aligned}
```

For depth,

```math
\sum_{d=0}^{n-2}\frac{2^d}{d+2}
=O(N/n),
```

and all linear UCG-width and predicate terms sum to `O(n**2)`. Since
`n**2=O(N/n)`,

```math
D(W_{\mathbb R})
=O\left(n+\frac{N}{n}\right).
```

The dedicated proof and second audit are in
[`STRICT_ZERO_BORROWED_SUFFIX_ECHO.md`](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) and
[`STRICT_ZERO_ECHO_AUDIT.md`](STRICT_ZERO_ECHO_AUDIT.md).

## 5. Exact Hopf tree factorization for positive workspace

For a cut after the first `t` tree depths, define

```math
F_t^{(n)}=L_{t-1}^{(n)}\cdots L_0^{(n)},
```

```math
R_t^{(n)}=L_{n-1}^{(n)}\cdots L_t^{(n)},
```

and put

```math
B=2^t,
\qquad
s=n-t.
```

The prefix and tail obey two complete-operator identities.

### 5.1 Conditioned prefix

Let

```math
P_s=|0^s\rangle\!\langle0^s|.
```

Then

```math
\boxed{
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes P_s
+I_{2^t}\otimes(I-P_s).
}
```

### 5.2 Tail direct sum

For prefix `r`, define the local `s`-qubit subtree frame `W_s^(r)` by assigning
local node `(ell,u)` the global breadth-first angle at node

```math
2^{t+\ell}+r2^\ell+u.
```

Then

```math
\boxed{
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
}
```

The repository constructs both sides independently and checks every cut through
`n=8`.

## 6. Clean binary--one-hot tree decoder

For `B=2**t`, the reversible decoder allocates:

- the existing `t`-qubit binary prefix register;
- a clean `B`-qubit one-hot leaf register;
- `B-1` clean internal-tree indicators;
- `B-1-t` clean shared scratch qubits.

The exact clean workspace count is

```math
3B-2-t.
```

The decoder satisfies

```math
D_t
\bigl(|x\rangle|0\rangle\bigr)
=|0^t\rangle|e_x\rangle|0\rangle
```

for every binary address `x`. Its explicit X/CNOT/Toffoli layer schedule has
depth `O(t)` and size `O(B)`, and the inverse is exact on the complete one-hot
code.

Using this decoder, one suffix-zero predicate, coherent predicate fanout, and
`t` controlled disjoint Givens layers realizes the conditioned-prefix operator
with depth `O(n)` and size `O(B+s)`.

## 7. Schedule P1: direct flagged UCGs

For `m>=1`, a nonfinal depth may be implemented by:

1. computing the lower-suffix-zero predicate into one clean flag;
2. applying one UCG controlled by the prefix and flag;
3. uncomputing the flag.

The flag is returned to zero before the next layer. The final depth has no suffix
predicate. Yuan--Zhang Lemmas 5 and 6 give

```math
S_{\mathrm{direct}}=O(N),
```

```math
D_{\mathrm{direct}}
=O\left(n^2+\frac{N}{n+m}\right).
```

For `1<=m<4n`, the polynomial term is absorbed by the exponential term, so the
direct schedule already has depth `O(N/(n+m))`.

## 8. Schedule P2: routed parallel subframes

For larger workspace, coherently route the existing suffix into one of `B`
disjoint branch registers selected by the prefix.

The routed tail allocates:

```math
(B-1)s
```

additional data qubits,

```math
B
```

activation-token qubits, and

```math
(B-1)(s+1)-t
```

copied routing controls. After routing, those copied controls are uncomputed and
their clean wires are reused as one suffix flag per branch when needed.

The exact routed-tail peak and the conditioned prefix both fit in the common
envelope

```math
2B(s+1).
```

Route and unroute have depth `O(n)` and size `O(B(s+1))`. One controlled
`s`-qubit subtree frame has

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

All `B` branches have disjoint support and execute in parallel, giving total
branch size `O(B2**s)=O(N)` without multiplying the branch depth.

## 9. Positive-workspace cut selection

For `m>=4n`, choose the largest `t` with `1<=t<n` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

For `s=n-t>1`, maximality gives

```math
m<4\,2^t s.
```

Hence

```math
\frac{2^s}{s}
=\frac{N}{2^t s}
<4\frac{N}{m}
=O\left(\frac{N}{n+m}\right).
```

Also

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

The routed schedule therefore has size `O(N)` and depth

```math
O\left(n+\frac{N}{n+m}\right).
```

Together with Schedule P1, this proves the upper bound for every `m>=1`.

## 10. Matching lower bounds

Applying the frame to `|0^n>` prepares every real normalized `n`-qubit state, a
family of dimension `N-1`.

A circuit with `G` arbitrary one-qubit gates has at most `4G` continuous real
parameters, so

```math
S_{\mathbb R}(n,m)=\Omega(N).
```

A depth-`D` circuit on `n+m` wires has at most `D(n+m)` one-qubit-gate locations,
giving

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

For positive workspace, the backward light cone of the `n` system outputs gives
the independent `Omega(n)` term. At `m=0`, parameter counting on exactly `n`
wires already gives `Omega(N/n)`, which asymptotically includes the required
linear term. Thus

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`.

## 11. All-workspace theorem

Combining Schedules Z, P1, and P2 with the lower bounds yields

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
}
```

for every integer `m>=0`.

## 12. Separated complex frame

For leaf phases `phi_x`, choose the final system qubit as a UCG target and write
`x=zb`. Then

```math
\boxed{
D_{\mathrm{ph}}
=\sum_z |z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
}
```

This is one total-width-`n` UCG. Yuan--Zhang Lemma 6 gives

```math
S_{\mathrm{diag}}(n,m)=O(N),
```

```math
D_{\mathrm{diag}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`. The blocks are arbitrary `U(2)` matrices, so the common phase
is retained exactly.

The real frame and diagonal are sequential frame-safe operators. They reuse one
workspace pool, including the empty pool at `m=0`. The real subfamily supplies
the matching lower bounds. Therefore

```math
\boxed{
S_{\mathbb C}(n,m)=\Theta(N),
\qquad
D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
}
```

for every integer `m>=0`.

## 13. Compiler and novelty boundaries

The theorem concerns full frame safety:

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input. State-column equality is insufficient.

The abstract strict-zero echo is not claimed as a wholly new general circuit
identity. Square-root/conjugation decompositions and borrowed/dirty-bit toggle
detection have close precedents. The claimed project contribution is the
Hopf-specific use of one restored suffix data qubit to aggregate every
prefix-dependent rotation into two width-`d+2` UCGs per tree depth, yielding the
optimal strict-zero complete-frame frontier.

See [`STRICT_ZERO_PRIOR_ART.md`](STRICT_ZERO_PRIOR_ART.md) for the conservative
claim boundary.

## 14. Evidence boundary

The active repository contains:

- independent exact matrices for every Hopf factor;
- an explicit reversible gate list for the binary--one-hot decoder;
- exact strict-zero echo matrices and sector tests;
- exact one-UCG phase-diagonal checks;
- workspace and resource ledgers;
- exact-rational inequality checks;
- compiler-boundary counterexamples.

Finite tests support but do not replace the dimension-independent proof. The
UCG, multi-controlled-X, coherent-copy, and QSP statements are imported from
Yuan--Zhang under their declared exact standard-circuit hypotheses.

The theorem does not address routed hardware, approximate Clifford+T synthesis,
noise, arbitrary coordinate charts, or external peer review.
