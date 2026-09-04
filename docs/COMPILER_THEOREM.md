# Complete all-workspace compiler theorem

[← Minimal Hopf interface](HOPF_INTERFACE.md) · [Complete technical note](../REVIEW.md) · [Next: verification →](VERIFICATION.md)

This page isolates the circuit-synthesis theorem. Quantum backpropagation is not
needed for the proof. The input is one structured unitary family, the Hopf
differential frame, and the output is an exact circuit with the optimal
state-preparation time–space tradeoff.

## 1. Compilation problem

Let `W_R(theta)` be the real Hopf differential frame on `n` system qubits, with

```math
N=2^n.
```

Given `m>=0` clean ancillary qubits, construct a unitary `W_tilde` satisfying

```math
\boxed{
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=
\bigl(W_{\mathbb R}|\varphi\rangle\bigr)|0^m\rangle
}
```

for every system input `|varphi>`.

The equality is on the complete clean-input subspace. All work qubits must be
returned exactly to zero.

The target frame is not a general `N`-dimensional unitary. It is determined by
`N-1` tree angles and factors into addressed layers

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_0^{(n)},
```

where

```math
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The prefix selects one angle, and the complete lower suffix supplies a shared
all-zero predicate.

## 2. Circuit model and imported primitives

The circuit model is exact and logical:

- arbitrary one-qubit gates;
- CNOT gates;
- all-to-all logical connectivity;
- clean ancillary qubits initialized in `|0>` and restored to `|0>`.

Toffoli, Fredkin, controlled one-qubit gates, and fixed-width controlled Givens
rotations are used as readable primitives in explicit schedules. Each has an
exact constant-size, constant-depth decomposition in this model.

The active state-preparation framework is P. Yuan and S. Zhang, *Quantum* **7**,
956 (2023). The proof uses:

| Result | Role here |
|---|---|
| Theorem 2 | optimal QSP benchmark `Theta(N)` size and `Theta(n+N/(n+m))` depth |
| Lemma 5 | exact ancilla-free multi-controlled `X` with linear size and depth |
| Lemma 6 | exact total-width-`q` UCG with `O(2^q)` size and `O(q+2^q/(q+w))` depth using `w` clean work qubits |
| Lemma 9 | balanced coherent CNOT copy–use–uncopy |

The published article corresponds to `arXiv:2202.11302v2`. The imported
statements were also checked in v3 and retain the forms and circuit-model
conventions used here.

The earlier state-preparation paper is the historical predecessor and original
source credited for selected primitives. For this proof, the two papers form one
compiler line. The later theorem supplies the uniform all-workspace framework.

The external primitives are used as stated. The Hopf-specific operator
factorizations, predicate constructions, routing schedule, live-register ledger,
and schedule selection are proved locally.

## 3. Main theorem

### Theorem: optimal compilation of Hopf differential frames

For every integer `n>=1` and every clean-workspace budget `m>=0`, the real Hopf
differential frame has an exact frame-safe circuit with

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

has the same size, depth, and workspace frontier:

```math
S_{\mathbb C,\mathrm{mag}}(n,m)=\Theta(2^n),
```

```math
D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
```

The leaf-phase derivatives form a separate direct measurement stream. They are
not additional columns of this `N`-dimensional unitary.

The real compiler uses three schedules.

| Workspace budget | Schedule | Mechanism |
|---:|---|---|
| `m=0` | Z: in-place echo | borrow one original suffix bit and restore it exactly |
| `1<=m<4n` | P1: direct flag | store the common suffix predicate in one reusable clean bit |
| larger `m` | P2: routed subframes | cut the tree and convert workspace into coherent branch parallelism |

The threshold `4n` is a convenient uniform proof threshold, not an optimized
finite-size crossover.

<p align="center">
  <img src="../assets/frontier-match.svg" width="980" alt="The three Hopf-frame schedules combine to match the optimal arbitrary-state-preparation depth frontier for every workspace budget." />
</p>

## 4. Schedule Z: strict zero workspace

### 4.1 In-place predicate carrier

Consider a nonfinal depth `d<n-1`. Split the system register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R,
```

where `p` is the `d`-bit prefix, `x` is the Hopf target, `b` is the first bit of
the lower suffix, and `r` contains the remaining `n-d-2` suffix bits.

Define

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Let `T_h` toggle the original logical bit `b` exactly when `r=0`:

```math
T_h:
|b\rangle|r\rangle
\longmapsto
|b\oplus h(r)\rangle|r\rangle.
```

Apply the chronological sequence

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
  <img src="../assets/strict-zero-echo.svg" width="1020" alt="Ancilla-free half-angle echo for one addressed Hopf depth." />
</p>

The Hopf rotation convention gives

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
XC_pX=C_p^{-1}.
```

For fixed `p` and `r`, the four invariant sectors are:

| `h(r)` | original `b` | chronological target word | resulting target matrix | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_pXC_pX=I` | 1 |
| 1 | 0 | `C_p,C_p` | `C_p^2=R_y(theta_(d,p))` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

The desired rotation occurs exactly when the original complete suffix `br` is
zero. Every other sector receives identity. The borrowed bit is restored, and
no sector-dependent phase remains.

Since the prefix and remaining-suffix labels define orthogonal invariant
subspaces, the sector calculation proves complete operator equality on
arbitrary superpositions and on inputs in which the borrowed bit is entangled
with the rest of the system:

```math
\boxed{E_d=L_d^{(n)}.}
```

### 4.2 No hidden work wire

`T_h` is a negative-control multi-controlled `X` whose target is the borrowed
logical bit. `X` wrappers convert the all-zero condition into an all-one
condition, and Lemma 5 supplies an exact ancilla-free implementation.

Each controlled `C_p` is one UCG with:

- `d` prefix controls;
- the borrowed bit as one additional control;
- one target.

Its exact total width is

```math
q=d+2.
```

The remaining suffix bits are controls of `T_h`, not work qubits.

### 4.3 Resource sum

Lemma 6 gives

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^d),
```

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^d}{d+2}\right).
```

Two half-angle UCGs, four predicate toggles, and two CNOT echoes give

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

The final depth has no lower suffix and is one total-width-`n` UCG. Therefore

```math
S(W_{\mathbb R})
=O\left(
\sum_{d=0}^{n-2}2^d
+
\sum_{d=0}^{n-2}(n-d)
+
2^n
\right)
=O(N).
```

Also,

```math
\sum_{d=0}^{n-2}\frac{2^d}{d+2}=O(N/n)
```

and `n^2=O(N/n)`. Thus

```math
\boxed{
D_{\mathbb R}(n,0)
=O\left(n+\frac{N}{n}\right).
}
```

The endpoints are explicit:

- `n=1`: only one one-qubit rotation remains;
- `d=0`: each half-angle UCG has total width two;
- `d=n-2`: `r` is empty and `T_h=X_b`;
- `d=n-1`: no borrowed bit is used.

> **Technical checkpoint.** The borrowed wire is logical data whose original
> value participates in the predicate. Correctness therefore requires a full
> operator proof and exact restoration, not only valid action on the
> preparation input.

### Executable counterpart

- [Strict-zero construction](../compiler_robust_hopf/strict_zero_echo.py)
- [Complete operator tests](../tests/test_strict_zero_echo.py)
- [Exact-rational resource audit](../compiler_robust_hopf/strict_zero_audit.py)

## 5. Schedule P1: small positive workspace

Assume `m>=1`. For each nonfinal depth:

1. compute the complete lower-suffix-zero predicate into one clean flag;
2. apply one UCG selected by the prefix and the flag;
3. uncompute the flag.

The same flag is reused at every depth. The UCG has total width `d+2` and may
use the remaining `m-1` clean work qubits. At the final depth there is no
predicate flag, so all `m` work qubits are available.

The predicate computations contribute `O(n^2)` total size and depth. The UCG
sizes sum geometrically to `O(N)`, and Lemma 6 gives

```math
D_{\mathrm{direct}}(n,m)
=O\left(n^2+\frac{N}{n+m}\right).
```

For

```math
1\leq m<4n,
```

we have `n+m<5n`. Since `n^3=O(2^n)`,

```math
n^2=O\left(\frac{N}{n+m}\right).
```

Hence

```math
\boxed{
S_{\mathrm{direct}}(n,m)=O(N),
\qquad
D_{\mathrm{direct}}(n,m)
=O\left(n+\frac{N}{n+m}\right).
}
```

### Executable counterpart

- [Direct resource rows](../compiler_robust_hopf/unified_compiler.py)
- [Workspace and endpoint tests](../tests/test_unified_compiler.py)
- [Absorption inequalities](../tests/test_resource_bounds.py)

## 6. Schedule P2: larger workspace

### 6.1 Exact tree cut

Cut after the first `t` depths and define

```math
B=2^t,
\qquad
s=n-t.
```

Factor

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

where `F_t` contains depths `0,...,t-1` and `R_t` contains depths
`t,...,n-1`.

The prefix obeys

```math
\boxed{
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I_{2^t}\otimes\left(I-|0^s\rangle\!\langle0^s|\right).
}
```

On the zero external suffix, the first `t` layers form the `t`-qubit frame. On
every nonzero external suffix, all those addressed layers are identity.

Every lower layer preserves the upper prefix, so

```math
\boxed{
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
}
```

A local subtree node `(ell,u)` in branch `r` uses global breadth-first node

```math
2^{t+\ell}+r2^\ell+u.
```

Both identities hold on the complete logical Hilbert space.

<p align="center">
  <img src="../assets/tree-cut-routing.svg" width="1040" alt="A Hopf tree cut separates a conditioned prefix from a direct sum of subtree frames realized by coherent routing." />
</p>

### 6.2 Conditioned prefix

The prefix frame must act only when the external suffix is zero. The explicit
reversible decoder implements

```math
D_t|x\rangle|0\cdots0\rangle
=|0^t\rangle|e_x\rangle|0\cdots0\rangle.
```

For `B=2^t`, its work registers are:

| Register | Qubits |
|---|---:|
| one-hot leaves | `B` |
| internal indicators | `B-1` |
| shared scratch and fanout pool | `B-1-t` |
| **total** | `3B-2-t` |

The explicit X/CNOT/Toffoli layers are disjoint within each declared circuit
layer. Their depth is `11t-4=O(t)` and their size is `O(B)`.

On the one-hot code, every Givens pair at one Hopf depth is disjoint. The
external zero-suffix predicate is computed, copied to the live fixed-width
controlled Givens gates, used, and uncomputed. Clean decoder wires are reused
for those control copies.

Consequently,

```math
S(F_t)=O(B+s),
\qquad
D(F_t)=O(n).
```

### 6.3 Explicit coherent router

The tail uses `B` possible locations for the `s`-qubit suffix and one activation
token per branch. Branch zero reuses the original suffix. The remaining data
registers require

```math
(B-1)s
```

clean qubits.

Treat each branch data register and token as a block of width

```math
w=s+1.
```

At routing level `j=0,...,t-1`, prefix bit `j` controls `2^jw` disjoint Fredkin
gates. One original prefix wire is available, so the number of clean copies at
that level is

```math
2^j(s+1)-1.
```

Summing gives

```math
\boxed{
C=(B-1)(s+1)-t
}
```

copy wires and

```math
\boxed{
F=(B-1)(s+1)
}
```

forward Fredkin gates.

Balanced CNOT trees create the prefix copies. Processing routing levels from
the least significant prefix bit to the most significant sends the data-token
block to the branch named by the prefix.

For an arbitrary, possibly prefix–suffix-entangled state

```math
\sum_{r=0}^{B-1}c_r|r\rangle_P|\xi_r\rangle_S,
```

the route acts coherently on every branch amplitude. The prefix copies are then
uncomputed. Each activation token controls its local subtree frame. Since the
branch data, tokens, and flags are disjoint, all subtree frames run in parallel.

After the branch operations:

1. every local suffix flag is uncomputed;
2. the prefix copies are recreated;
3. the Fredkin levels are reversed;
4. all copies are erased;
5. the root token is reset.

The complete clean-input action is exactly

```math
\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

### 6.4 Simultaneous workspace peak

When `s>1`, each branch uses one local suffix flag. The cleared copy pool already
contains at least `B` wires because

```math
\begin{aligned}
C-B
&=(B-1)(s+1)-t-B\\
&=(B-1)s-t-1\\
&\geq0
\end{aligned}
```

for `B=2^t`, `t>=1`, and `s>=2`.

Thus the flags reuse allocated copy wires rather than increasing the peak. The
tail peak is

```math
(B-1)s+B+
\max\left\{(B-1)(s+1)-t,\,B\right\}.
```

The prefix and tail execute sequentially, and each fits within

```math
\boxed{2B(s+1)}
```

clean ancillary qubits.

Route and unroute have `O(n)` depth and `O(B(s+1))` size. Each controlled
`s`-qubit subtree frame has size `O(2^s)` and depth

```math
O\left(s^2+\frac{2^s}{s}\right).
```

The branches are disjoint, so their size multiplies by `B`, while their depth
does not. The total branch size is

```math
O(B2^s)=O(N).
```

### 6.5 Largest feasible cut

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If `s=n-t>1`, failure of the next cut implies

```math
m<4\,2^t s.
```

Therefore

```math
\frac{2^s}{s}
=
\frac{N}{2^t s}
<
4\frac{N}{m}
=
O\left(\frac{N}{n+m}\right),
```

using `m>=4n`. Also,

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

If `s=1`, every controlled subtree frame has constant depth. Feasibility of
`t=n-1` requires

```math
m\geq2\,2^{n-1}(1+1)=2^{n+1}=2N.
```

Hence `N/(n+m)=O(1)`, and the target depth is `Theta(n)`, matching the
conditioned-prefix and route–unroute depth.

Thus

```math
\boxed{
S_{\mathrm{routed}}(n,m)=O(N),
\qquad
D_{\mathrm{routed}}(n,m)
=O\left(n+\frac{N}{n+m}\right).
}
```

> **Technical checkpoint.** Coherent correctness, exact cleanup, and peak
> workspace are separate obligations. The workspace count is the maximum set of
> simultaneously live registers, not the sum of all registers used at different
> stages.

### Executable counterpart

- [Tree identities](../compiler_robust_hopf/tree_structure.py)
- [Binary–one-hot decoder](../compiler_robust_hopf/tree_decoder.py)
- [Explicit router and sparse-state simulator](../compiler_robust_hopf/router.py)
- [Decoder tests](../tests/test_tree_decoder.py)
- [Router operator and cleanup tests](../tests/test_router.py)
- [Unified resource selection](../compiler_robust_hopf/unified_compiler.py)

## 7. Matching lower bounds

The first frame column ranges over an open family of normalized real states of
dimension `N-1`.

A fixed circuit topology with `G` arbitrary one-qubit gates has only `O(G)`
continuous real parameters. Countably many lower-dimensional circuit families
cannot cover that open state family. Therefore

```math
S_{\mathbb R}(n,m)=\Omega(N).
```

A depth-`D` circuit on `n+m` wires has `O(D(n+m))` parameterized one-qubit gate
locations, giving

```math
D_{\mathbb R}(n,m)
=\Omega\left(\frac{N}{n+m}\right).
```

For positive workspace, the union of the backward light cones of the `n` system
outputs contains at most `O(n2^D)` parameterized locations. Covering the full
real-state family therefore requires

```math
D=\Omega(n).
```

At `m=0`, the parameter-location bound `Omega(N/n)` already asymptotically
dominates the linear term.

Combining the bounds,

```math
\boxed{
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right).
}
```

The upper and lower bounds now match for every `m>=0`.

## 8. Phase-dressed complex magnitude frame

Writing a basis label as `x=zb`, with the final qubit as target,

```math
D_{\mathrm{ph}}
=
\sum_z
|z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
```

This is one total-width-`n` UCG with arbitrary `U(2)` blocks. Lemma 6 gives

```math
S(D_{\mathrm{ph}})=O(N),
```

```math
D(D_{\mathrm{ph}})
=O\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`.

The real frame and phase UCG each restore their workspace, so they reuse one
pool sequentially, including the empty pool at `m=0`. The real subfamily
supplies the lower bounds. Hence the complex magnitude-frame frontier is
identical to the real one.

## 9. Comparison with the state-preparation frontier

| Quantity | Optimal arbitrary QSP | Hopf differential frame |
|---|---:|---:|
| continuous family dimension | `Theta(N)` | `Theta(N)` |
| exact size | `Theta(N)` | `Theta(N)` |
| exact depth with `m` clean qubits | `Theta(n+N/(n+m))` | `Theta(n+N/(n+m))` |
| operator promise | one initialized column | complete structured frame |
| additional local structure used | QSP recursion | addressed suffix predicates and Hopf tree direct sums |

The equality of frontiers is not obtained by replacing the frame with an
arbitrary preparation completion. It follows from the three exact schedules
above.

## 10. Scope

The theorem is an exact logical-circuit result. It does not include:

- hardware connectivity or native-gate routing;
- approximate Clifford+T synthesis;
- noise or fault-tolerance overhead;
- optimizer convergence;
- an arbitrary coordinate-frame family;
- application-specific controlled-observable implementation cost.

The downstream QBP statement is given separately in
[From frame compilation to quantum backpropagation](QBP_CONSEQUENCE.md).

---

[← Minimal Hopf interface](HOPF_INTERFACE.md) · [Complete technical note](../REVIEW.md) · [Next: verification →](VERIFICATION.md)
