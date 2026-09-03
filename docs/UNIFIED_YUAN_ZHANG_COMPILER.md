# Unified all-workspace compiler for Hopf differential frames

## Status

This document summarizes the active compiler architecture. The complete proof is
in [COMPILER_THEOREM.md](COMPILER_THEOREM.md). The architecture uses one
external compiler framework—Yuan and Zhang, *Quantum* **7**, 956 (2023)—and
three Hopf-specific schedules covering every clean-workspace budget `m>=0`.

The published Yuan–Zhang article corresponds to arXiv v2. Theorem 2 and Lemmas
5, 6, and 9 were also checked in v3 and retain the statements used here.

## 1. Result

Let `N=2^n`. The real Hopf differential frame satisfies

```math
S_{\mathbb R}(n,m)=\Theta(N),
```

```math
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`. The phase-dressed complex magnitude frame

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}
```

has the same frontier. Complex leaf-phase derivatives use a separate direct
record.

| Workspace | Schedule |
|---:|---|
| `m=0` | borrowed-suffix half-angle echo |
| `1<=m<4n` | direct flagged UCGs |
| larger `m` | binary–one-hot prefix decoder plus coherent routed parallel subframes |

These are internal schedules of one Hopf-frame compiler, not a choice between
two state-preparation papers.

## 2. Local operator target

At tree depth `d`, with prefix `p`, target `x`, and lower suffix `z` of length
`s=n-d-1`, the compiler must implement

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

The complete frame is the ordered product of these addressed layers. The target
is a complete operator on arbitrary inputs, not only a state-preparation map.

For unrestricted angles, the coordinate differential is

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical Hopf domains, `a_j>=0` and `a_j=sqrt(g_(j,j))`. At a singular
coordinate the raw derivative vanishes while the unit marker column remains a
canonical frame continuation.

## 3. Imported Yuan–Zhang primitives

| Result | Role |
|---|---|
| Theorem 2 | optimal QSP benchmark for every ancillary budget |
| Lemma 5 | exact ancilla-free multi-controlled X |
| Lemma 6 | exact all-workspace UCG synthesis |
| Lemma 9 | coherent CNOT-tree copy–use–uncopy |

The earlier Sun et al. paper is retained as the historical predecessor. The
active proof uses the Yuan–Zhang framework throughout.

## 4. Strict zero workspace

At a nonfinal depth, split the lower suffix into one original system bit `b` and
remaining string `r`. Let

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Four toggles of `b` conditioned on `h(r)`, interleaved with two
borrowed-bit-controlled half-angle UCGs and two target CNOT echoes, yield

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
XC_pX=C_p^{-1},
\qquad
C_pXC_pX=I.
```

The desired original-zero-suffix sector receives the full rotation, every other
sector receives identity, and the borrowed logical bit is restored. Each
half-angle UCG has total width `d+2`.

The resulting layer resources are

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right),
```

and summation gives `Theta(N)` size and `Theta(n+N/n)` depth at `m=0`.

## 5. Direct positive-workspace schedule

For `m>=1`, compute the lower-suffix-zero predicate into one reusable clean
flag, apply a prefix-plus-flag UCG, and uncompute the flag. The UCG receives only
`m-1` additional work qubits at nonfinal depths.

The schedule has

```math
S=O(N),
```

```math
D=O\left(n^2+\frac{N}{n+m}\right).
```

For `1<=m<4n`, the exponential term absorbs `n^2`, so this already matches the
optimal frontier.

## 6. Tree cut and conditioned prefix

For a cut after `t` depths, set `B=2^t` and `s=n-t`. The complete factorization
is

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right),
```

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

The prefix uses an explicit clean binary–one-hot decoder with workspace
`3B-2-t`, depth `O(t)`, and size `O(B)`.

## 7. Explicit coherent router

The router treats each branch's `s` data wires and one activation token as a
block of width `s+1`. At routing level `j`, prefix bit `j` controls
`2^j(s+1)` disjoint Fredkin gates. One original control is available, so the
clean-copy count at that level is `2^j(s+1)-1`.

The exact totals are

```math
\text{copy wires}=(B-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(B-1)(s+1).
```

Balanced CNOT trees copy all prefix bits coherently. Fredkin levels are applied
least-significant-prefix-bit first, sending the suffix-and-token block to the
prefix-selected branch. Copies are then uncomputed.

The cleared copy pool is reused as one local suffix flag per branch. All
token-controlled subtree frames run on disjoint registers in parallel. Their
flags are cleared, prefix copies are recomputed, the Fredkin tree is reversed,
copies are cleared, and the root token is reset.

The exact schedule and sparse complex-state simulator are in
[`../compiler_robust_hopf/router.py`](../compiler_robust_hopf/router.py). Tests
in [`../tests/test_router.py`](../tests/test_router.py) verify basis routing,
arbitrary prefix–suffix-entangled inputs, equality to the ideal tail direct sum,
complete routed-cut equality, and zero workspace leakage.

The complete prefix and routed tail fit in the envelope

```math
2B(s+1).
```

## 8. Routed resources

One token-controlled `s`-qubit subtree frame has

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

All `B` branches run in parallel. Their total size is `B O(2^s)=O(N)`, while
their depth is the depth of one branch. Route and unroute have `O(n)` depth and
`O(B(s+1))=O(N)` size.

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

Maximality implies `2^s/s=O(N/(n+m))`, so the routed schedule has

```math
S=O(N),
\qquad
D=O\left(n+\frac{N}{n+m}\right).
```

## 9. Matching lower bounds

The first frame column covers the `N-1` dimensional real sphere. Parameter
counting gives `Omega(N)` size and `Omega(N/(n+m))` depth. Backward light cones
of the `n` system outputs give the independent `Omega(n)` depth term. Therefore
the upper bounds are optimal for every `m>=0`.

## 10. Complex magnitude frame

Writing a leaf label as `x=zb`,

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\mathrm{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right)
```

is one total-width-`n` UCG. It returns the same workspace pool clean and is
composed sequentially with the real frame. This proves the phase-dressed complex
magnitude-frame frontier. Leaf-phase derivatives remain a direct QBP stream.

## 11. Evidence boundary

- strict-zero and frame identities: complete dense logical operators;
- binary–one-hot decoder: explicit reversible layers;
- coherent router: explicit CNOT/Fredkin layers and sparse-state simulation;
- UCG and multi-controlled-X elementary circuits: imported Yuan–Zhang theorems;
- asymptotic resources: exact term ledgers and analytic sums.

Finite tests support but do not replace the dimension-independent proof.
