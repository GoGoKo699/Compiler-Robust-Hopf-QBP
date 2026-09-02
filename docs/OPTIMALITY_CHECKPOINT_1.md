# Optimality checkpoint 1: routed parallel subframes

## Status

Completed as a **new proof candidate** on 2026-09-02.

This checkpoint gives a tree-specific construction that appears to close the
optimal ancilla--depth gap for every positive clean-workspace budget. It has not
yet received the independent line-by-line audit applied to the near-optimal
baseline. The strict zero-ancilla sharp-size endpoint remains open.

The frozen fallback result is recorded in
[`NEAR_OPTIMAL_BASELINE_2026_09.md`](NEAR_OPTIMAL_BASELINE_2026_09.md).
Nothing in this document weakens that baseline.

## 1. Target

Let

```math
N=2^n.
```

The optimal state-preparation frontier with `m` clean ancillary qubits is

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right),
\qquad
S_{\mathrm{QSP}}(n,m)=\Theta(N).
```

The audited Hopf-frame compiler has size `O(N)` but can carry an additional
`O(log n)` depth factor in the intermediate-workspace range. The purpose of this
checkpoint is to remove that factor without replacing the full-frame contract
by state-column equality.

## 2. Why generic controlled state preparation is not the reduction

Controlled quantum state preparation implements

```math
|j\rangle|0^n\rangle
\longmapsto
|j\rangle|\psi_j\rangle.
```

Applying this primitive to all columns of an arbitrary `n`-qubit unitary uses
`k=n` control qubits and an `n`-qubit target. The generic CQSP theorem then has
size

```math
O(2^{n+n})=O(N^2),
```

before the input column label has been erased. After one column-constructor
call, a superposition becomes

```math
\sum_j c_j|j\rangle W|j\rangle.
```

Obtaining

```math
\sum_j c_j W|j\rangle|0^n\rangle
```

requires coherent removal of the first register. That step is not supplied by
CQSP itself. General unitary-from-column-constructor results use nonconstant
query overhead; those generic lower bounds do not apply directly to the
structured Hopf family, but they prevent treating index erasure as a free
black-box operation.

The construction below instead exploits an exact direct-sum identity of the
Hopf tree. It routes the *existing suffix data* into disjoint branch registers,
applies structured subtree frames in parallel, and routes the data back. No
column label is discarded.

## 3. Exact tree-cut decomposition

Write the addressed real frame as

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_0^{(n)}.
```

For a cut `0<=t<=n`, set

```math
F_t^{(n)}
=L_{t-1}^{(n)}\cdots L_0^{(n)},
```

```math
R_t^{(n)}
=L_{n-1}^{(n)}\cdots L_t^{(n)}.
```

The audited conditioned-prefix identity already gives the first factor. The new
identity concerns the tail.

Let

```math
B=2^t,
\qquad
s=n-t.
```

For each `t`-bit prefix `r`, let `W_s^(r)` be the `s`-qubit Hopf frame whose
local breadth-first angle at local depth `ell` and position `u` is the global
angle at node

```math
2^{t+\ell}+r2^\ell+u.
```

Then

```math
\boxed{
R_t^{(n)}
=
\bigoplus_{r=0}^{B-1}W_s^{(r)}
=
\sum_{r=0}^{B-1}|r\rangle\!\langle r|\otimes W_s^{(r)}.
}
```

### Proof

Every addressed layer at depth `d>=t` leaves the first `t` computational bits
unchanged. Its rotations therefore split into `B` disjoint groups indexed by
that prefix. Inside prefix block `r`, writing `d=t+ell`, the global addressed
pair and angle index are exactly the local addressed pair and breadth-first
angle of `W_s^(r)`. Products preserve the block decomposition and the local
increasing-depth order. Hence the complete tail is the displayed direct sum.

The repository checks this identity for every cut through `n=8` and verifies
that the subtree angle lists form a disjoint partition of every angle below the
cut.

Consequently,

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)}
```

with an inexpensive conditioned prefix and a block-diagonal tail.

## 4. Coherent branch router

The tail acts on a `t`-qubit prefix register `C` and an `s`-qubit suffix register
`X`. Allocate:

1. `B-1` additional `s`-qubit data registers, giving registers
   `X_0,...,X_(B-1)` with `X_0=X`;
2. `B` one-qubit token registers `z_0,...,z_(B-1)`, initialized to zero and
   followed by `X z_0`, so the token begins at branch zero;
3. temporary coherent copies of the prefix controls;
4. one reusable zero-suffix flag for each branch while the subtree frames run.

### Routing network

Process the prefix bits from least significant to most significant. At level
`ell`, for every `u<2^ell`, conditionally swap register `u` with register
`u+2^ell` using the corresponding prefix bit. Apply the same controlled swap to
all `s` data lanes and to the token lane.

For a computational prefix `r`, this moves `X` and the token into branch `r`.
By linearity, on an arbitrary entangled input it implements

```math
\sum_r |r\rangle_C|\xi_r\rangle_X
\longmapsto
\sum_r |r\rangle_C
|\xi_r\rangle_{X_r}
|1\rangle_{z_r},
```

with every inactive branch-data and token register zero.

The controlled swaps at one level have disjoint targets. Copy the relevant
prefix bit to a distinct control for each swap by CNOT fanout trees. All prefix
bits can be fanned out simultaneously. The fanout depth is

```math
O\bigl(t+\log(s+1)\bigr),
```

the route has `t` constant-depth Fredkin stages, and every copy is uncomputed.
The same process is repeated in reverse after the branch frames.

A Fredkin gate is a fixed three-qubit unitary, so it has constant exact size and
depth in the declared arbitrary-one-qubit-plus-CNOT model.

## 5. Exact workspace ledger

The routed tail uses the following clean ancillary registers:

```math
(B-1)s
```

for additional data registers,

```math
B
```

for the routed activation token, and at most

```math
(B-1)(s+1)
```

temporary prefix-control copies. These copies are uncomputed before the branch
frames and can be reused as the `B` branch flags. For `B>=2` and `s>=1`, the
copy pool is large enough for those flags.

Thus the routed-tail peak is no larger than

```math
(B-1)s+B+(B-1)(s+1)
<2B(s+1).
```

The conditioned-prefix compiler uses at most

```math
3B-t
```

clean ancillary qubits. Since `s>=1`, this is also below `2B(s+1)`. The two
blocks are sequential and reuse one pool. Therefore the complete routed
construction fits whenever

```math
\boxed{
2B(s+1)\leq m.
}
```

The code records both the tighter register count and this simple envelope.

## 6. Controlled subtree-frame lemma

After routing, branch `r` contains data only when `z_r=1`. Apply the controlled
frame

```math
|0\rangle\!\langle0|_{z_r}\otimes I
+
|1\rangle\!\langle1|_{z_r}\otimes W_s^{(r)}.
```

All `B` controlled frames act on disjoint registers and therefore run in
parallel.

One controlled `s`-qubit Hopf frame can be implemented with one reusable clean
suffix flag and no additional UCG workspace. At a nonfinal local depth `d`:

1. compute the lower-suffix-zero predicate into the flag;
2. apply one UCG whose controls are the activation token, the `d` prefix bits,
   and the flag;
3. uncompute the flag.

The UCG width is `d+3`. At the final local depth no suffix flag is needed and the
width is `s+1`.

Using the no-workspace UCG bound and the ancilla-free multi-controlled-X bound,
one controlled subtree frame has

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

The `s^2` term contains predicate and linear-UCG contributions. The exponential
terms form a geometric tail of order `2^s/s`. Every branch flag is returned to
zero.

## 7. Routed-frame resources

The conditioned prefix has depth `O(n)` and size `O(B+s)`. Routing and
unrouting have depth `O(n)` and size `O(B(s+1))`. The `B` controlled subtree
frames run in parallel, with total size

```math
B\,O(2^s)=O(N).
```

Because `s+1<=2^s` for `s>=1`, routing size is also `O(N)`. Therefore

```math
S_{\mathrm{route}}(n,t)=O(N),
```

```math
D_{\mathrm{route}}(n,t)
=O\left(n+s^2+\frac{2^s}{s}\right).
```

The inverse route returns all additional data registers to zero, returns the
activation token to `z_0`, and a final local `X` resets that token. The whole
construction is a clean implementation of the complete frame on every input.

Small dense tests explicitly simulate route, controlled parallel subframes, and
unroute for `(n,t)=(2,1),(3,1),(3,2)`. They recover the exact block-diagonal tail
with zero clean-subspace leakage.

## 8. Choosing the cut

Assume `n>=2` and `m>=4n`. Choose the largest `t` in `1,...,n-1` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

Write `B=2^t` and `s=n-t`.

If `t<n-1`, maximality implies that the next cut fails:

```math
m<4Bs.
```

Hence

```math
\frac{2^s}{s}
=
\frac{N}{Bs}
<
4\frac{N}{m}.
```

Because `m>=4n`,

```math
\frac{N}{m}
=O\left(\frac{N}{n+m}\right).
```

Furthermore,

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

For `s<=9`, this follows from `s^2<=81n`. For `s>=10`, the elementary inequality
`2^s>=s^3` gives `s^2<=2^s/s`.

If `t=n-1`, then `s=1`, the routed depth is `O(n)`, and the target expression is
also `Omega(n)`.

Therefore the routed construction has

```math
D_{\mathrm{route}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

whenever `m>=4n`.

## 9. Low-workspace regime

For `1<=m<4n`, use the already audited compiler. Its depth is at most

```math
O\left(n^2+\frac{N}{n+m}\right).
```

Since `n+m<5n` and the sequence `n^3/2^n` is bounded,

```math
n^2
=O\left(\frac{N}{n+m}\right).
```

Thus the audited compiler already has optimal-order depth in this range.

The one-qubit case is a single local rotation and is absorbed separately.

## 10. Candidate optimal positive-workspace theorem

> **Candidate theorem (optimal positive-workspace real Hopf frame).** For every
> `n>=1` and every `m>=1`, the complete real Hopf differential frame has an
> exact frame-safe implementation using at most `m` clean ancillary qubits,
> size
>
> ```math
> O(2^n),
> ```
>
> and depth
>
> ```math
> \boxed{
> O\left(n+\frac{2^n}{n+m}\right).
> }
> ```
>
> Its inverse has the same resources.

The construction uses the audited low-workspace compiler for `m<4n` and the
routed parallel-subframe compiler for `m>=4n`.

## 11. Matching lower bound

The Hopf frame applied to `|0^n>` prepares an arbitrary real unit vector. The
real unit sphere has dimension `N-1`, so a standard circuit family covering it
requires `Omega(N)` continuously parameterized gates. A depth-`D` circuit on
`n+m` wires has only `O(D(n+m))` gate locations, giving

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

For the independent `Omega(n)` term, consider the union of the backward light
cones of the `n` system output qubits. In depth `D`, that union contains at most
`O(Dn2^D)` relevant one- and two-qubit gate locations. Gates outside it cannot
change the final system state. Covering an `(N-1)`-dimensional real family
therefore requires

```math
Dn2^D=\Omega(N),
```

which implies `D=Omega(n)`. Hence

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right)
```

up to constant equivalence between a sum and a maximum.

Combined with the candidate upper bound, this would give

```math
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every `m>=1`, together with `Theta(N)` size.

This lower-bound argument also requires an independent audit before promotion.

## 12. Separated complex corollary candidate

The exact diagonal compiler already has size `O(N)`, depth

```math
O\left(n+\frac{N}{n+m}\right),
```

and uses at most `m` clean ancillary qubits. It can reuse the routed real-frame
workspace sequentially. Consequently the separated complex frame should inherit
the same optimal positive-workspace size and depth theorem.

The direct phase-gradient stream still uses no inverse differential frame.

## 13. Strict zero-ancilla endpoint

The checkpoint does **not** close the simultaneous strict-zero-workspace and
sharp-size endpoint.

Current exact choices are:

| Clean ancillary qubits | Size | Depth |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

The desired strict-zero endpoint is

```math
S=O(N),
\qquad
D=O\left(n+\frac{N}{n}\right).
```

It may require a no-ancilla global synthesis of the tree wavelet transform or a
proof that the one-flag improvement cannot be reproduced without clean
workspace. This remains a separate subproblem.

## 14. Evidence and next audit

Executable support is in:

```text
compiler_robust_hopf/optimal_parallel.py
tests/test_optimal_parallel.py
```

The tests cover:

- exact tail direct-sum identities for every cut through `n=8`;
- disjoint partition of all subtree angles;
- reversible branch-router permutations;
- exact routed-tail action and zero leakage for small dense cases;
- workspace-envelope and maximal-cut checks;
- broad term-ledger diagnostics against the optimal target.

Finite tests do not prove the asymptotic theorem. Before the result is promoted,
a second proof audit must independently verify:

1. control-copy fanout depth and peak workspace;
2. route and unroute cleanliness on arbitrary entangled inputs;
3. controlled subtree-frame width, size, and depth sums;
4. cut maximality and every endpoint;
5. the real-family lower bound;
6. sequential reuse by the complex diagonal block;
7. parameter-generation and end-to-end decoder accounting;
8. the exact scope of the unresolved `m=0` endpoint.
