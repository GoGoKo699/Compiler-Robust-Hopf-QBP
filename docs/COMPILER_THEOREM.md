# Complete all-workspace compiler theorem

[← Minimal Hopf interface](HOPF_INTERFACE.md) · [Read the complete narrative](../REVIEW.md) · [Next: QBP consequence →](QBP_CONSEQUENCE.md)

This page gives the operator and resource proof for the real Hopf differential
frame and the phase-dressed complex magnitude frame. The proof uses one external
circuit framework—Yuan and Zhang, *Quantum* **7**, 956 (2023)—and three
Hopf-specific schedules covering every clean-workspace budget `m>=0`.

The large-workspace schedule is specified as an explicit coherent router, not
only as an ideal direct sum or a resource formula.

## 1. Circuit model and imported primitives

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits available to the
compiler. The circuit model is exact and logical:

- arbitrary one-qubit gates;
- CNOTs;
- all-to-all logical connectivity;
- clean ancillas initialized in `|0>` and returned exactly to `|0>`.

Toffoli, Fredkin, and controlled one-qubit gates are used as readable
constant-width primitives in explicit schedules. Each has a constant-size,
constant-depth exact decomposition into arbitrary one-qubit gates and CNOTs, so
this notation changes only constant factors.

The proof imports the following Yuan–Zhang results.

| Imported result | Role in this proof |
|---|---|
| Theorem 2 | optimal arbitrary-state-preparation benchmark: `Theta(N)` size and `Theta(n+N/(n+m))` depth |
| Lemma 5 | exact ancilla-free multi-controlled X with linear size and depth |
| Lemma 6 | exact total-width-`q` UCG with `O(2^q)` size and `O(q+2^q/(q+w))` depth using `w` clean work qubits |
| Lemma 9 | coherent CNOT-tree copy–use–uncopy in logarithmic depth |

The published article corresponds to `arXiv:2202.11302v2`. The imported
statements were also checked in `arXiv:2202.11302v3` and retain the conclusions
and model conventions used here.

The earlier work of Sun, Tian, Yang, Yuan, and Zhang is the historical
predecessor. The active proof does not switch between the two state-preparation
papers according to workspace regime. The Yuan–Zhang primitives can be adapted
after the complete-operator structure of the Hopf frame is exposed; that
adaptation is not a direct consequence of preparing one initialized state
column.

## 2. Main theorem

### Theorem: optimal exact compilation of Hopf differential frames

For every integer `n>=1` and `m>=0`, the complete real Hopf differential frame
has an exact frame-safe implementation using at most `m` clean ancillary qubits
with

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(2^n)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
}
```

The phase-dressed complex magnitude frame

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}
```

has the same asymptotic size, depth, and clean-workspace frontier:

```math
S_{\mathbb C,\mathrm{mag}}(n,m)=\Theta(2^n),
```

```math
D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
```

The leaf-phase derivatives of the complex chart form a separate direct
measurement stream; they are not additional columns of this `N`-dimensional
unitary.

The real compiler uses three schedules.

| Workspace regime | Schedule | Mechanism |
|---:|---|---|
| `m=0` | strict-zero echo | borrow one logical suffix bit and restore it exactly |
| `1<=m<4n` | direct flagged UCG | store the common suffix-zero predicate in one reusable clean flag |
| larger `m` | routed parallel subframes | cut the tree, route the suffix coherently, and run disjoint subtree frames in parallel |

The threshold `4n` is selected for a simple uniform proof, not as the best
finite-size crossover.

## 3. Local target: one addressed Hopf depth

At depth `d`, write a computational basis label as

```math
|p\rangle_P|x\rangle_T|z\rangle_Z,
```

where `p` is the `d`-bit prefix, `x` the target, and `z` a suffix of length

```math
s=n-d-1.
```

The exact addressed layer is

```math
\boxed{
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^s\rangle\!\langle0^s|.
}
```

The complete frame is

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_0^{(n)},
```

with `L_0` acting first. All schedules below implement these same operators on
every system input.

## 4. Schedule Z: strict zero workspace

### 4.1 Exact borrowed-suffix echo

Assume `d<n-1`. Split the suffix into one borrowed system bit `b` and the
remaining string `r`:

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R.
```

Define

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Let `T_h` toggle `b` iff `r=0`. Apply chronologically

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

<p align="center">
  <img src="../assets/strict-zero-echo.svg" width="1000" alt="Strict-zero borrowed-suffix echo circuit." />
</p>

The Hopf convention gives

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
XC_pX=C_p^{-1}.
```

For fixed `p` and `r`, the invariant sectors are:

| `h(r)` | original `b` | chronological target word | resulting matrix | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_pXC_pX=I` | 1 |
| 1 | 0 | `C_p,C_p` | `C_p^2=R_y(theta_(d,p))` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

The desired rotation occurs exactly when the original complete suffix is zero.
Every other sector receives identity. The borrowed bit is restored and no
sector-dependent phase appears. Since the sectors form an orthogonal direct
sum, this proves complete-operator equality on arbitrary superpositions and
entangled inputs.

At `d=n-2`, `r` is empty and `T_h=X_b`; the same table applies. For `n=1`, there
is no nonfinal layer.

### 4.2 No hidden work wire

Each nonfinal layer uses:

- two half-angle UCGs;
- four ancilla-free predicate toggles;
- two CNOT target echoes.

A half-angle UCG contains `d` prefix controls, the borrowed bit as one control,
and the Hopf target. Its total width is

```math
q=d+2.
```

The remaining suffix bits are controls of `T_h`, not workspace. Lemma 5
implements `T_h` without an ancillary wire.

### 4.3 Strict-zero resources

Lemma 6 gives

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^d),
```

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^d}{d+2}\right).
```

Four toggles contribute `O(n-d)` size and depth. Therefore

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

The final depth is one total-width-`n` UCG. Hence

```math
S(W_{\mathbb R})
=O\left(\sum_{d=0}^{n-2}2^d+n^2+2^n\right)
=O(2^n).
```

Also

```math
\sum_{q=2}^{n}\frac{2^q}{q}
=O(2^n/n)
```

and `n^2=O(2^n/n)`, giving

```math
\boxed{
D(W_{\mathbb R})
=O\left(n+\frac{2^n}{n}\right).
}
```

### Executable counterpart

- [Strict-zero construction](../compiler_robust_hopf/strict_zero_echo.py)
- [Complete operator tests](../tests/test_strict_zero_echo.py)
- [Exact-rational audit](../compiler_robust_hopf/strict_zero_audit.py)

## 5. Schedule P1: small positive workspace

Assume `m>=1`. At each nonfinal depth:

1. compute `[z=0]` into one clean flag;
2. apply one UCG selected by the prefix and flag;
3. uncompute the flag.

The UCG has total width `d+2` and receives only `m-1` additional work qubits.
At the final depth there is no predicate flag, so all `m` work qubits are
available.

The predicate computations contribute `O(n^2)` total size and depth. The UCG
sizes sum geometrically to `O(N)`, while Lemma 6 gives

```math
D_{\mathrm{direct}}(n,m)
=O\left(n^2+\frac{N}{n+m}\right).
```

For `1<=m<4n`, `n+m<5n`; because `n^3=O(2^n)`,

```math
n^2=O\left(\frac{N}{n+m}\right).
```

Thus

```math
S_{\mathrm{direct}}(n,m)=O(N),
```

```math
D_{\mathrm{direct}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

throughout the small-positive-workspace regime.

## 6. Exact tree cut

Cut after the first `t` depths and define

```math
B=2^t,
\qquad
s=n-t.
```

Write

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

where `F_t` contains depths `0,...,t-1` and `R_t` contains depths
`t,...,n-1`.

### 6.1 Conditioned prefix identity

```math
\boxed{
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I_{2^t}\otimes\left(I-|0^s\rangle\!\langle0^s|\right).
}
```

Every layer above the cut includes all `s` external suffix bits in its
zero-suffix predicate. On `|0^s>` the layers form the `t`-qubit Hopf frame; on
the orthogonal complement every layer is identity.

### 6.2 Tail direct sum

For prefix `r`, let `W_s^(r)` be the Hopf frame of the subtree below that prefix.
A local subtree node `(ell,u)` uses global breadth-first node

```math
2^{t+\ell}+r2^\ell+u.
```

Every tail layer preserves the `t`-bit prefix. Therefore each fixed-prefix
subspace is invariant and

```math
\boxed{
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
}
```

These are complete-operator identities, not state-column statements.

## 7. Conditioned prefix via a binary–one-hot decoder

The prefix frame must run only when the external suffix is zero. The repository
uses an explicit reversible decoder

```math
D_t|x\rangle|0\cdots0\rangle
=|0^t\rangle|e_x\rangle|0\cdots0\rangle.
```

For `B=2^t`, the work registers are:

| Register | Qubits |
|---|---:|
| one-hot leaves | `B` |
| internal indicators | `B-1` |
| shared fanout/parity pool | `B-1-t` |
| **total** | `3B-2-t` |

The decoder propagates one active tree indicator according to the binary
address, reconstructs each address bit as a parity of active right-child
indicators, and clears the original address. Its explicit X/CNOT/Toffoli layers
have disjoint support within each declared layer, depth `11t-4=O(t)`, and size
`O(B)`. Reversing the layers gives the exact inverse.

On the one-hot code, all Givens pairs at one Hopf depth are disjoint. The
external suffix-zero predicate is computed, fanned out to the live Givens
controls, used, and uncomputed. Internal decoder wires that are clean after
encoding are reused for these control copies.

Consequently

```math
S(F_t)=O(B+s),
\qquad
D(F_t)=O(n).
```

### Executable counterpart

- [Decoder layers](../compiler_robust_hopf/tree_decoder.py)
- [Decoder and encoded-frame tests](../tests/test_tree_decoder.py)

## 8. Explicit coherent router

The routed tail uses `B` possible data locations and `B` one-hot activation
tokens. Branch zero reuses the original `s` system suffix wires; the other
branches require `(B-1)s` clean data wires. Initially the root token is set to
one.

Treat each branch's `s` data wires and one token as a block of width

```math
w=s+1.
```

### 8.1 Prefix fanout

At routing level `j=0,...,t-1`, the `j`-th prefix bit must control

```math
2^j w
```

simultaneous Fredkin gates. One original prefix wire is already available, so
the number of clean copies at level `j` is

```math
2^j(s+1)-1.
```

Summing gives

```math
\boxed{
C=(B-1)(s+1)-t
}
```

copy wires. Each prefix bit is copied with a balanced CNOT tree. All `t` trees
start together because their wire sets are disjoint. The maximum fanout depth is

```math
(t-1)+\lceil\log_2(s+1)\rceil.
```

### 8.2 Fredkin tree

At level `j`, for every lower branch index `r<2^j`, swap block `r` with block
`r+2^j`, controlled by the `j`-th prefix bit and its copies. All gates at one
level are disjoint. Processing prefix bits from least to most significant sends
the data-token block to the branch whose binary label equals the prefix.

The forward number of Fredkin gates is

```math
\boxed{
(B-1)(s+1).
}
```

After the swaps, the prefix copies are uncomputed. Thus for arbitrary amplitudes
`c_r` and arbitrary, possibly prefix-entangled suffix states `|xi_r>`,

```math
\sum_r c_r|r\rangle_P|\xi_r\rangle_X|0\rangle_{\mathrm{work}}
\longmapsto
\sum_r c_r|r\rangle_P
|\xi_r\rangle_{X_r}|1\rangle_{z_r}|0\rangle_{\mathrm{rest}}.
```

This follows because the router is a coherently controlled permutation. No
measurement or classical branch selection occurs.

### 8.3 Controlled subtree frames and cleanup

Once prefix copies are zero, their wires are reused as one clean suffix flag per
branch when `s>1`. Token `z_r` controls the complete frame `W_s^(r)` on branch
`r`. At each nonfinal local depth, the branch's lower-suffix predicate is
computed into its flag, a token-and-flag-controlled UCG is applied, and the flag
is uncomputed. Final local depth needs no flag.

All branch circuits act on disjoint data, token, and flag registers and therefore
run in parallel. After every branch flag is zero, the prefix copies are
recomputed, the Fredkin levels are reversed, the copies are uncomputed, and the
root token is reset. The original suffix then contains the transformed data and
all work registers are zero.

The explicit schedule and sparse-state simulator are in
[`router.py`](../compiler_robust_hopf/router.py). Tests apply the construction to
arbitrary complex states with prefix–suffix entanglement and verify

```math
U_{\mathrm{route}}^{\dagger}
\left(\bigotimes_r\Lambda_{z_r}(W_s^{(r)})\right)
U_{\mathrm{route}}
=
\bigoplus_r W_s^{(r)}
```

on the clean-workspace subspace, together with exact token, flag, and copy-pool
cleanup.

### 8.4 Router resources

The live tail registers are:

| Register | Clean qubits |
|---|---:|
| additional branch data | `(B-1)s` |
| activation tokens | `B` |
| copied routing controls | `(B-1)(s+1)-t` |
| simultaneous branch flags | `B` when `s>1`, reusing cleared copy wires |

The tail peak is

```math
(B-1)s+B+
\max\{(B-1)(s+1)-t,\,B\}.
```

The conditioned prefix and routed tail run sequentially, so the complete peak is
the maximum of their peaks, not their sum. Both fit inside the convenient
envelope

```math
\boxed{
2B(s+1).
}
```

The route and inverse route have `O(n)` depth and `O(B(s+1))` size. Since
`s+1<=2^s`, routing size is `O(N)`.

### Executable counterpart

- [Explicit router and sparse-state simulator](../compiler_robust_hopf/router.py)
- [Router operator and cleanup tests](../tests/test_router.py)
- [Resource selection](../compiler_robust_hopf/unified_compiler.py)

## 9. Parallel subtree resources and cut selection

A token-controlled direct `s`-qubit subtree frame has

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

The `B` branches are disjoint, so their combined size is

```math
B\,O(2^s)=O(N),
```

while their depth is the depth of one branch.

For `m>=4n`, choose the largest `t` such that

```math
2\,2^t(n-t+1)\leq m.
```

This envelope guarantees the complete prefix and tail workspace fits inside
`m`. If `s=n-t>1`, failure of the next cut gives

```math
m<4\,2^t s.
```

Hence

```math
\frac{2^s}{s}
=\frac{N}{2^t s}
<4\frac{N}{m}
=O\left(\frac{N}{n+m}\right),
```

because `m>=4n` implies `n+m=Theta(m)`. Also

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

Therefore the routed schedule satisfies

```math
S_{\mathrm{routed}}(n,m)=O(N),
```

```math
D_{\mathrm{routed}}(n,m)
=O\left(n+\frac{N}{n+m}\right).
```

Together with Schedules Z and P1, this proves the real-frame upper bound for
every `m>=0`.

## 10. Matching lower bounds

Every valid frame compiler is also a real-state-preparation circuit when applied
to `|0^n>|0^m>`, because its first column covers an open family of real
normalized states of dimension `N-1`.

### Size

A circuit with `G` arbitrary one-qubit gates has `O(G)` continuous parameters.
A countable union of lower-dimensional circuit families cannot cover an open
subset of an `(N-1)`-dimensional manifold. Therefore

```math
S_{\mathbb R}(n,m)=\Omega(N).
```

### Workspace-dependent depth

A depth-`D` circuit on `n+m` wires has `O(D(n+m))` parameterized one-qubit gate
locations. Thus

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

### Linear depth

Each of the `n` system outputs has a backward light cone containing at most
`2^D` wires. The union contains at most `O(n2^D)` relevant wires and
`O(Dn2^D)` parameterized locations. Covering the real-state family requires

```math
Dn2^D=\Omega(2^n),
```

which implies `D=Omega(n)`. At `m=0`, the preceding parameter bound
`Omega(N/n)` already dominates `n` asymptotically.

Combining the two depth terms gives

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right).
```

The upper and lower bounds therefore match.

## 11. Phase-dressed complex magnitude frame

Choose the final system qubit as a UCG target and write `x=zb`. Then

```math
D_{\mathrm{ph}}
=
\sum_z|z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
```

This is one exact total-width-`n` UCG, including the common phase. Lemma 6 gives

```math
S_{\mathrm{diag}}(n,m)=O(N),
```

```math
D_{\mathrm{diag}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`.

Both the real frame and phase UCG return their workspace clean. They execute
sequentially and reuse one pool, so workspace takes a maximum rather than a sum.
The real subfamily supplies matching lower bounds. This proves the complex
magnitude-frame theorem.

## 12. Evidence boundary

The repository implements different objects at appropriate levels:

- frame and strict-zero identities as complete dense matrices;
- the binary–one-hot decoder as explicit reversible layers;
- the coherent router as explicit CNOT/Fredkin layers and a sparse-state
  route–operate–unroute simulator;
- UCG and multi-controlled-X elementary synthesis through the published
  Yuan–Zhang theorems;
- resource bounds through integer and exact-rational ledgers.

The finite tests support, but do not replace, the analytic proof. Hardware
connectivity, approximate Clifford+T synthesis, native-gate constants, and noise
are outside the theorem.

---

[← Minimal Hopf interface](HOPF_INTERFACE.md) · [Read the complete narrative](../REVIEW.md) · [Next: QBP consequence →](QBP_CONSEQUENCE.md)
