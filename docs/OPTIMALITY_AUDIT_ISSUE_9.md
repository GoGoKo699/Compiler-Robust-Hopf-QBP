# Independent audit of the optimal positive-workspace construction

## Status

Completed internally: 2026-09-02.

Scope: the routed parallel-subframe construction in draft PR #8, for the exact
all-to-all circuit model with arbitrary one-qubit gates and CNOTs.

Outcome:

- the exact tail direct-sum identity survives;
- the coherent router survives on arbitrary prefix--suffix entanglement;
- the peak clean-workspace ledger survives, with a sharper exact control-copy
  count;
- the controlled subtree compiler and all width shifts survive;
- the maximal-cut and low-workspace asymptotics survive;
- the real-state size and depth lower bounds survive, with a sharpened
  light-cone parameter count;
- the separated complex corollary survives by sequential clean reuse;
- strict `m=0` with both sharp size and optimal depth remains unresolved.

Accordingly, the positive-workspace result can be promoted from a construction
proposal to an **internally audited theorem relative to the cited exact
synthesis results**. This is not external peer review.

## 1. Primary source map

The principal benchmark and circuit primitives are taken from:

P. Yuan and S. Zhang, "Optimal (controlled) quantum state preparation and
improved unitary synthesis by quantum circuits with any number of ancillary
qubits," *Quantum* **7**, 956 (2023),
[PDF](https://quantum-journal.org/papers/q-2023-03-20-956/pdf/).

The exact parts used in this audit are:

| Source result | Use here |
|---|---|
| Standard circuit model in Section 2 | Same arbitrary-one-qubit-plus-CNOT model |
| Lemma 5 | Ancilla-free linear-depth multi-controlled X |
| Lemma 6 | Exact UCG size `O(2**q)` and depth `O(q+2**q/(q+w))` |
| Lemma 9 | Coherent CNOT-tree copying and exact uncopying |
| Theorem 1 | Generic CQSP benchmark and its `O(2**(n+k))` size |
| Theorem 2 | Optimal QSP frontier `Theta(n+2**n/(n+m))`, size `Theta(2**n)` |
| Remarks after Lemma 15 | Parameter-count and light-cone lower-bound architecture |

The paper's Figure 1 concerns general unitary synthesis, not the QSP frontier.
The QSP benchmark used here is Theorem 2.

The routed Hopf compiler is not contained in Yuan--Zhang. Their results supply
primitives, the optimal state-preparation benchmark, and a lower-bound template.
The tree-cut decomposition and route--parallel-subframes--unroute construction
are the Hopf-specific contribution audited below.

## 2. Statement audited

Let

```math
N=2^n.
```

The audited positive-workspace theorem is:

> **Theorem.** For every `n>=1` and every integer `m>=1`, the complete real
> Hopf differential frame has an exact frame-safe implementation using at most
> `m` clean ancillary qubits, with
>
> ```math
> S_{\mathbb R}(n,m)=O(N)
> ```
>
> and
>
> ```math
> D_{\mathbb R}(n,m)
> =O\left(n+\frac{N}{n+m}\right).
> ```
>
> Its inverse has the same resources.

The matching lower bounds are

```math
S_{\mathbb R}(n,m)=\Omega(N)
```

and

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right).
```

Thus the size and depth are optimal for every positive clean-workspace budget.

The strict zero-ancilla endpoint is not included in this theorem.

## 3. Tail direct-sum identity

Write

```math
W_{\mathbb R}^{(n)}
=R_t^{(n)}F_t^{(n)},
```

where `F_t^(n)` contains depths `0,...,t-1` and `R_t^(n)` contains depths
`t,...,n-1`. Put

```math
B=2^t,
\qquad
s=n-t.
```

For every prefix `r` of length `t`, define the local `s`-qubit frame
`W_s^(r)` by assigning local node `(ell,u)` the global breadth-first node

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

### Audit proof

Every addressed rotation below the cut leaves the first `t` computational bits
unchanged. The tail is therefore block diagonal in those bits. Inside prefix
block `r`, a global depth `t+ell` addressed pair reduces exactly to the local
depth `ell` addressed pair on the remaining `s` bits, and the displayed node
map gives its angle. Rotations belonging to different prefix blocks are
disjoint and commute; rotations within one block retain increasing local depth.
This proves the direct sum as a full operator identity.

Classification: **proved**.

Finite support: every cut through `n=8`, plus exact partition checks through
`n=12`.

## 4. Coherent router

Let `C` be the `t`-qubit prefix and `X` the original `s`-qubit suffix. Allocate
`B` branch-data registers `X_0,...,X_(B-1)`, with `X_0=X`, and `B` token
qubits `z_0,...,z_(B-1)`. Initialize `z_0` to one.

At routing level `ell`, conditionally swap branch register `u` with
`u+2**ell` for every `u<2**ell`, using the corresponding prefix bit. Apply
the same Fredkin pattern to all `s` data lanes and the token lane.

For each computational prefix `r`, induction over the routing levels gives

```math
|r\rangle_C|x\rangle_{X_0}|1\rangle_{z_0}
\longmapsto
|r\rangle_C|x\rangle_{X_r}|1\rangle_{z_r},
```

with all inactive branch registers zero. Because the router is a basis
permutation controlled by `C`, linearity gives the same identity for arbitrary
superpositions and for inputs in which `C` and `X` are entangled.

The prefix register is never targeted. The inverse Fredkin network therefore
routes the transformed active branch back exactly.

Classification: **proved**.

Finite support: exhaustive basis-permutation and dense arbitrary-state checks
for all small layouts allowed by the repository guard.

## 5. Exact control-copy count and fanout depth

At routing level `ell`, the number of Fredkin gates is

```math
q_\ell=2^\ell(s+1).
```

One gate may use the original prefix qubit as its control. The remaining
`q_ell-1` gates require copied controls. Since different levels use different
prefix bits, all prefix bits can be fanned out concurrently into disjoint
pools. The exact number of copied-control ancillas is therefore

```math
\boxed{
C_{\mathrm{copy}}
=\sum_{\ell=0}^{t-1}(q_\ell-1)
=(B-1)(s+1)-t.
}
```

The candidate used the looser valid upper bound `(B-1)(s+1)`.

A binary CNOT tree produces `q_ell` coherent controls, counting the original,
in depth `ceil(log2(q_ell))`. The maximum concurrent fanout depth is

```math
(t-1)+\left\lceil\log_2(s+1)\right\rceil.
```

After the controlled swaps, inverse fanout resets every copied control. For one
control bit, the algebra is

```math
\mathrm{FANOUT}^{\dagger}
\left(
|0\rangle\!\langle0|\otimes I
+|1\rangle\!\langle1|\otimes U
\right)
\mathrm{FANOUT},
```

where the copies are only controls. The original control is unchanged, so the
inverse fanout returns the copy register to zero even when the control and data
are entangled. This is the same coherent copy--use--uncopy principle made
explicit in Yuan--Zhang Lemma 9.

Forward and reverse routing each require one fanout and one uncopy. Together
with `t` forward and `t` reverse Fredkin stages, the routing depth is `O(n)`.
The routing size is `O(B(s+1))`.

Classification: **proved and sharpened**.

## 6. Peak workspace

The exact routed-tail register counts are:

```math
(B-1)s
```

additional data qubits,

```math
B
```

token qubits, and

```math
(B-1)(s+1)-t
```

copied controls.

When `s>1`, all `B` controlled subtree frames need one simultaneous clean
suffix flag each. The copied-control pool is already large enough:

```math
(B-1)(s+1)-t\geq B.
```

For `t=1`, this is `s>=2`. For `t>=2`, use `t<=B-2` and `s+1>=3`.
When `s=1`, no suffix flag is needed.

The copied controls are uncomputed before the branch frames, so the same wires
can be reused as flags. Hence the exact routed-tail peak is

```math
(B-1)s+B+
\max\left\{(B-1)(s+1)-t,\,B\mathbf 1_{s>1}\right\}.
```

It is strictly smaller than

```math
2B(s+1).
```

The already audited conditioned-prefix compiler uses at most `3B-t` clean
ancillas, also no more than `2B(s+1)` for `s>=1`. Prefix and tail are
sequential, so the complete construction fits whenever

```math
2B(s+1)\leq m.
```

No Fredkin-decomposition ancilla is hidden: a Fredkin gate is a fixed
three-qubit unitary and has an exact constant-size, constant-depth decomposition
in the standard gate model. The subtree UCGs use zero extra UCG workspace, and
the multi-controlled-X predicates use no ancillary qubits beyond their stated
flag targets.

Classification: **proved**.

## 7. Controlled subtree compiler

For one branch, control the local Hopf frame by its token `z_r`.

At local depth `d<s-1`:

1. compute the lower-suffix-zero predicate of width `s-d-1` into the branch
   flag;
2. apply a UCG with controls consisting of the token, the `d` upper-prefix
   qubits, and the flag;
3. uncompute the predicate.

The total UCG width is

```math
k=d+3.
```

At the final local depth, no flag is needed and the width is

```math
k=s+1.
```

Yuan--Zhang Lemma 6, specialized to zero UCG workspace, gives size `O(2**k)`
and depth `O(k+2**k/k)`. Lemma 5 gives linear depth and size for each
ancilla-free multi-controlled-X predicate.

Summing all predicates and linear UCG terms gives `O(s**2)`. The exponential
terms obey

```math
\sum_{k=3}^{s+1}\frac{2^k}{k}
=O\left(\frac{2^s}{s}\right).
```

Therefore one controlled subtree frame has

```math
\boxed{
S_{\mathrm{csub}}(s)=O(2^s),
}
```

```math
\boxed{
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
}
```

The token is only a control, the lower suffix is unchanged while its flag is
live, and every flag is uncomputed exactly.

Classification: **proved relative to Lemmas 5 and 6**.

## 8. Parallel schedule and clean return

After routing, branch `r` uses only

```text
X_r, z_r, flag_r.
```

Different branches use disjoint qubits. All `B` controlled subtree frames can
therefore run in parallel. Their total size is

```math
B\,O(2^s)=O(N),
```

while their depth is that of one branch.

After every branch flag is reset, recreate the prefix-control copies, apply the
inverse router, and uncopy. The transformed suffix returns to `X_0`, all other
data registers and tokens return to zero except `z_0=1`, and one final `X`
resets `z_0`.

Thus the routed block is a clean implementation of the complete direct-sum tail
on every system input. Composing it with the clean conditioned prefix gives a
frame-safe implementation of the complete frame.

Classification: **proved**.

## 9. Size of the routed construction

The three contributions are:

```math
O(B+s)
```

for the conditioned prefix,

```math
O(B(s+1))
```

for route and unroute, and

```math
O(B2^s)=O(N)
```

for all controlled branches.

Since `s+1<=2**s` for `s>=1`, the routing size is also `O(N)`. Therefore

```math
S_{\mathrm{route}}(n,t)=O(N).
```

Classification: **proved**.

## 10. Maximal-cut asymptotics

Assume `n>=2` and `m>=4n`. The cut `t=1` is feasible, so choose the largest
`t<n` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

Let `B=2**t` and `s=n-t`. If `s>1`, failure of the next cut gives

```math
m<4Bs.
```

Therefore

```math
\frac{2^s}{s}
=\frac{N}{Bs}
<4\frac{N}{m}
\leq5\frac{N}{n+m},
```

where the last inequality uses `m>=4n`.

The polynomial term is also absorbed:

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

For `s<=9`, use `s**2<=81n`. For `s>=10`, use `2**s>=s**3`.
When `s=1`, branch depth is constant and the total depth is `O(n)`.

Adding the `O(n)` prefix and routing depths proves

```math
D_{\mathrm{route}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

for all `m>=4n`.

Classification: **proved**.

## 11. Low positive workspace

For `1<=m<4n`, use the frozen audited compiler. Its depth is

```math
O\left(n^2+\frac{N}{n+m}\right).
```

The elementary bound

```math
n^3\leq4\,2^n
```

holds for every `n>=1`: check `n<=4`, then observe that the ratio
`n**3/2**n` decreases for `n>=4`. Since `n+m<5n`,

```math
n^2
\leq20\frac{N}{n+m}.
```

Hence the frozen compiler already has

```math
D=O\left(n+\frac{N}{n+m}\right)
```

throughout the low positive-workspace range, using no more than the requested
`m` clean ancillas.

Classification: **proved with an explicit constant**.

## 12. Real-state lower bounds

The lower bound must be adapted to the real Hopf state family; it is not obtained
by treating the frame columns as an arbitrary CQSP instance.

### Size and `N/(n+m)` depth term

The real unit sphere has dimension `N-1`. A one-qubit `U(2)` gate carries at
most four real continuous parameters, while CNOT locations are discrete. A
circuit family covering an open subset of that sphere therefore needs
`Omega(N)` parameterized gates.

A depth-`D` standard circuit on `n+m` wires contains at most `D(n+m)`
one-qubit gate locations. Thus

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

### Light-cone `n` term

Trace backward from the `n` designated system outputs. At distance `j`, their
union light cone contains at most `n*2**j` wires. The total number of
parameterized one-qubit locations in a depth-`D` light cone is therefore at
most

```math
\sum_{j=0}^{D-1}n2^j
<n2^D.
```

Charging four real parameters per location gives fewer than `4n2**D` relevant
continuous parameters. Gates outside this light cone cannot change the system
output. Covering an `(N-1)`-dimensional real state family therefore requires

```math
4n2^D\geq N-1,
```

so

```math
D\geq n-\log_2(4n)-O(1)=\Omega(n).
```

This sharpens the candidate note's looser `O(Dn2**D)` count; the conclusion is
unchanged and strengthened. The structure matches the parameter-count and
light-cone lower-bound discussion following Yuan--Zhang Lemma 15.

Combining the two independent bounds gives

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right)
```

up to constant equivalence of sum and maximum.

Classification: **proved**.

## 13. Why generic CQSP is not the theorem

Yuan--Zhang Theorem 1 implements

```math
|j\rangle|0^n\rangle
\longmapsto
|j\rangle|\psi_j\rangle
```

with size `O(2**(n+k))` for `k` index qubits. Treating all `N` columns of an
`n`-qubit frame as unrelated targets sets `k=n`, giving generic size

```math
O(4^n)=O(N^2).
```

The coherent input label also remains present. The routed construction avoids
both problems by using the Hopf tail direct sum and physically moving the
existing suffix register. No index register is erased.

Classification: **confirmed from Theorem 1; not used as a black box**.

## 14. Separated complex frame

The already audited diagonal compiler has

```math
S_{\mathrm{diag}}(n,m)=O(N),
```

```math
D_{\mathrm{diag}}(n,m)
=O\left(n+\frac{N}{n+m}\right),
```

uses at most `m` clean ancillary qubits, and returns them to zero. It can reuse
the routed real-frame workspace sequentially. Therefore, for every `m>=1`,

```math
S_{\mathbb C}(n,m)=O(N),
```

```math
D_{\mathbb C}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

with the same `m`-qubit clean pool. The real-family lower bound already applies
to this larger family.

Classification: **proved relative to the audited diagonal theorem**.

## 15. Parameter generation and gradient output

The router is parameter-free. Subtree-angle partitioning is linear in the
number of Hopf angles. Standard exact UCG angle transforms can be carried out
in `O(k2**k)` arithmetic for a width-`k` table. Summed over every layer and all
branches, this is

```math
O(Ns)\subseteq O(Nn)
```

classical preprocessing with `O(N)` working storage. The separated complex
diagonal already uses one length-`N` Walsh transform and has the same
`O(Nn)` preprocessing scale.

The global magnitude record is decoded in `O(S_mag N)` work, and the direct
phase record in `O(S_ph+N)` work. These costs are output-sensitive and remain
separate from logical circuit depth.

Classification: **accounted for; finite implementation constants not claimed**.

## 16. Endpoint audit

| Endpoint | Audited result |
|---|---|
| `n=1`, `m>=1` | One local rotation; optimal constant depth and size |
| `1<=m<4n` | Frozen compiler is already optimal order |
| `m=4n` | Cut `t=1` is feasible exactly |
| maximal cut `t=n-1` | `s=1`; controlled branches have constant depth |
| `m>>N` | Use `t=n-1` and ignore surplus workspace; depth remains `O(n)` |
| singular Hopf angles | Construction contains no divisions and remains a full unitary |
| `m=0` | Not included in the optimal theorem |

At strict zero workspace, the retained exact alternatives are:

| Clean ancillas | Size | Depth |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

Whether strict zero workspace can simultaneously achieve `O(N)` size and
`O(n+N/n)` depth remains open.

## 17. Final classification

| Component | Audit status |
|---|---|
| Tail direct sum and angle map | Proved |
| Coherent routing on arbitrary inputs | Proved |
| Control fanout and uncopy | Proved; exact copy count sharpened |
| Peak clean-workspace ledger | Proved |
| Controlled subtree frame | Proved relative to exact UCG/MCT lemmas |
| Parallel branch schedule | Proved |
| Clean reverse routing | Proved |
| `O(N)` size | Proved |
| Maximal-cut depth reduction | Proved |
| Low-workspace reduction | Proved with explicit constant 20 |
| Real-state size/depth lower bounds | Proved; light-cone count sharpened |
| Separated complex corollary | Proved relative to audited diagonal compiler |
| Parameter-generation and decoder accounting | Accounted for |
| Strict `m=0` sharp-size optimum | Open |

## 18. Audit conclusion

The second internal audit found no failure of the routed construction. The
positive-workspace result is ready to be stated internally as an optimal theorem:

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(2^n),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right),
\qquad m\geq1.
}
```

The same size and depth statement holds for the separated complex frame under
the same positive clean-workspace budget.

Public release and manuscript submission still require external proof review.
Issue #2 remains open only for the strict zero-ancilla sharp-size endpoint and
for final manuscript integration.