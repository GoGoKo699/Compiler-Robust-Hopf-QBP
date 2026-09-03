# Clean-room review of the optimal all-workspace Hopf-frame compiler

## Status

This document records a third internal proof review performed from the operator
definitions and the cited elementary synthesis theorems. It was developed on a
branch separated from the construction history. It is **not external peer
review**, and it is not a legal novelty opinion.

**Verdict.** No blocking operator, workspace, size, depth, endpoint, inverse, or
separated-complex error was found. Under the exact standard-circuit hypotheses
stated below, the reviewed construction supports the theorem candidate

```math
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(2^n),
```

```math
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every integer `m>=0`.

The strongest remaining gate is independent human review, especially of the
routed positive-workspace register schedule and of the prior-art boundary for
the strict-zero construction.

## 1. Review method

The review was reconstructed in the following order.

1. Start from the complete addressed Hopf-layer operator, rather than from the
   state-preparation column.
2. Derive the strict-zero echo sector by sector, with chronological and matrix
   multiplication orders written separately.
3. Recount every participating qubit in the UCGs and predicate toggles.
4. Sum the layer resources without using numerical slope fitting.
5. Re-derive the positive-workspace tree cut, conditioned prefix, routed tail,
   and maximal-cut inequality.
6. Re-derive the real-family lower bounds independently of the upper-bound
   construction.
7. Check the separated complex phase layer as a complete UCG, including common
   phases.
8. Compare the construction against the nearest circuit-synthesis and
   borrowed-qubit literature.

Finite tests are treated only as regression evidence. They are not used as the
logical basis of any asymptotic claim.

## 2. Imported circuit results and exact model

The active external framework is P. Yuan and S. Zhang, *Quantum* **7**, 956
(2023), [doi:10.22331/q-2023-03-20-956](https://doi.org/10.22331/q-2023-03-20-956).
The review uses:

- their standard model of arbitrary one-qubit gates and CNOTs with all-to-all
  logical connectivity;
- Lemma 5: exact ancilla-free multi-controlled X with linear size and depth;
- Lemma 6: a total-width-`q` UCG with `w` clean work qubits has size
  `O(2**q)` and depth `O(q+2**q/(q+w))`;
- Lemma 9: coherent CNOT-tree copying and exact uncopying;
- Theorem 2: exact state preparation has size `Theta(2**n)` and depth
  `Theta(n+2**n/(n+m))` for every ancillary budget.

Lemma 6 is restated there from the earlier work of Sun, Tian, Yang, Yuan, and
Zhang. The earlier paper therefore remains an original-source and historical
citation, but it is not a second active compiler path.

Every conclusion below is conditional on those exact synthesis statements and
on their circuit model. No hardware-routing, Clifford+T approximation, or
noise-dependent claim is inferred.

## 3. Complete addressed layer

Let `N=2**n`. At nonfinal tree depth `d`, split a computational-basis label as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R,
```

where:

- `p` contains the `d` upper-prefix bits;
- `x` is the Hopf rotation target;
- `b` is the first lower-suffix bit;
- `r` contains the other `n-d-2` lower-suffix bits.

The desired complete layer is

```math
L_d
=I+\sum_p |p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_p)-I\bigr)
\otimes |0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

This equation fixes the compiler contract on the whole Hilbert space. A circuit
that agrees only on the forward state-preparation input is insufficient for the
global gradient protocol.

## 4. Strict-zero borrowed-suffix echo

Put

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_p/2),
```

and let `T_h` toggle the original system qubit `b` exactly when `h(r)=1`.
Consider the chronological sequence

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

For the repository convention

```math
R_y(\alpha)=e^{-i\alpha Y},
```

we have

```math
C_p^2=R_y(\theta_p),
\qquad
X C_p X=C_p^{-1}.
```

Fixing `p` and `r`, the four sectors are:

| `h(r)` | original `b` | chronological target word | resulting matrix | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_p X C_p X=I` | 1 |
| 1 | 0 | `C_p,C_p` | `C_p^2=R_y(theta_p)` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

The chronological word `X,C_p,X,C_p` acts on column vectors as
`C_p X C_p X`, so the cancellation order is correct. There is no scalar phase
in any sector.

Because the prefix and remaining-suffix sectors are orthogonal and invariant,
this proves a complete operator identity by linearity. The original suffix
qubit may begin in an arbitrary state and may be entangled with every other
system qubit. It is restored exactly.

### 4.1 No hidden ancillary wire

`T_h` is a negative-control multi-controlled X with target `b`. Parallel X
wrappers convert the all-zero controls to all-one controls; Yuan--Zhang Lemma 5
then supplies an exact zero-ancilla decomposition. The target `b` is one of the
original logical system wires, not an allocated clean or dirty ancillary wire.

Each half-angle operation is one UCG with:

- `d` prefix controls;
- one borrowed-bit control;
- one target.

Its exact total width is therefore

```math
q=d+2.
```

The remaining suffix bits are idle during the UCG and are not counted as work
qubits.

### 4.2 Strict-zero upper bound

Two width-`d+2` UCGs contribute `O(2**d)` size and

```math
O\left(d+2+\frac{2^d}{d+2}\right)
```

depth. Four predicate toggles contribute `O(n-d)` size and depth, and the two
target echoes are CNOTs. Hence

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

The final tree depth has no lower suffix and is one ordinary total-width-`n`
UCG. Summing the sizes gives

```math
\sum_{d=0}^{n-2}O(2^d+n-d)+O(2^n)=O(2^n).
```

For the depth-dependent geometric terms, putting `q=d+2` gives the uniform
bound

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\le 6\frac{2^n}{n}.
```

The linear-width and predicate terms total `O(n**2)`, and
`n**2=O(2**n/n)`. Therefore

```math
D_{\mathbb R}(n,0)
=O\left(n+\frac{2^n}{n}\right).
```

The `n=1` endpoint consists only of the final one-qubit rotation. At `d=n-2`,
the remaining suffix is empty and `T_h=X_b`; the same four-sector identity
continues to hold.

## 5. Positive-workspace direct schedule

For `m>=1`, each nonfinal addressed layer may instead compute the complete
lower-suffix-zero predicate into one clean flag, apply one prefix-and-flag UCG,
and uncompute the flag. The flag is reused between depths. The final depth has
no suffix predicate.

Yuan--Zhang Lemmas 5 and 6 give

```math
S_{\mathrm{direct}}=O(2^n),
```

```math
D_{\mathrm{direct}}
=O\left(n^2+\frac{2^n}{n+m}\right).
```

When `1<=m<4n`, `n+m<5n`, while `n**3=O(2**n)`. Thus the polynomial term is
absorbed by `2**n/(n+m)`, and the direct schedule already has optimal-order
depth throughout the small-positive-workspace regime.

## 6. Tree-cut identities

For a cut after `t` depths, write

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
\qquad
B=2^t,
\qquad
s=n-t.
```

The first `t` depths obey

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes |0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right).
```

Every lower layer leaves the upper prefix unchanged, so the tail is block
diagonal:

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A local subtree node `(ell,u)` in branch `r` uses the global breadth-first angle
at index

```math
2^{t+\ell}+r2^\ell+u.
```

These are complete-operator identities; no state-column restriction enters.

## 7. Conditioned-prefix decoder

The explicit reversible decoder moves a `t`-bit binary prefix into a one-hot
register and clears the original prefix:

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle.
```

The workspace consists of:

```math
2^t
```

one-hot leaves,

```math
2^t-1
```

internal indicators, and

```math
2^t-1-t
```

shared scratch qubits, for a total of

```math
3\,2^t-2-t.
```

The supplied X/CNOT/Toffoli circuit is a permutation of the complete
computational basis. Its disjoint layer schedule has depth `O(t)` and size
`O(2**t)`. On the one-excitation code, the Hopf Givens pairs at each depth are
disjoint, so the encoded complete prefix frame is implemented in `O(t)`
additional depth and `O(2**t)` size.

Computing and fanning out the external suffix-zero predicate, applying the
controlled Givens layers, and reversing all work gives the required conditioned
prefix in depth `O(n)`, size `O(2**t+s)`, and the stated decoder workspace.

## 8. Routed parallel tail

The coherent router allocates:

```math
(B-1)s
```

branch-data qubits,

```math
B
```

activation-token qubits, and

```math
(B-1)(s+1)-t
```

copied routing controls. After routing, the copied controls are uncomputed and
their wires can be reused as branch suffix flags. The exact prefix and tail
peaks fit inside

```math
2B(s+1)
```

clean ancillary qubits.

Route and unroute have `O(n)` depth and `O(B(s+1))` size. Each controlled
`s`-qubit subtree frame has size `O(2**s)` and depth

```math
O\left(s^2+\frac{2^s}{s}\right).
```

The `B` branches have disjoint physical support, so their size multiplies by
`B` while their depth does not. The total branch size is `O(B2**s)=O(2**n)`.
All branch data, tokens, copied controls, and flags are returned to zero by the
inverse schedule.

## 9. Maximal-cut argument

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\le m.
```

For `s=n-t>1`, failure of the next cut implies

```math
m<4\,2^t s.
```

Therefore

```math
\frac{2^s}{s}
=\frac{2^n}{2^t s}
<4\frac{2^n}{m}
=O\left(\frac{2^n}{n+m}\right),
```

where the last equivalence uses `m>=4n`. Also

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

The routed depth is consequently

```math
O\left(n+\frac{2^n}{n+m}\right).
```

The bounded-`s`, `s=1`, and arbitrarily large-`m` endpoints are absorbed by the
linear term. Together with the direct schedule, this covers every `m>=1`.

## 10. Matching lower bounds

Applying the frame to `|0^n>` prepares the full real unit sphere, a manifold of
dimension `2**n-1`.

- A fixed circuit topology with `G` arbitrary one-qubit gates has only `O(G)`
  continuous real parameters. Countably many lower-dimensional circuit
  families cannot cover an open subset of the real-state manifold, so
  `G=Omega(2**n)`.
- A depth-`D` circuit on `n+m` wires has `O(D(n+m))` parameterized one-qubit
  locations, giving `D=Omega(2**n/(n+m))`.
- For positive workspace, the union of the backward light cones of the `n`
  system outputs contains `O(n2**D)` continuously parameterized locations.
  Covering a `2**n-1` dimensional output family therefore requires
  `D=Omega(n)`.
- At `m=0`, the layer-parameter bound already gives `D=Omega(2**n/n)`, which
  asymptotically dominates the required linear term.

Thus

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{2^n}{n+m}\right)
```

for every `m>=0`, and the size lower bound is `Omega(2**n)`.

## 11. Separated complex frame

Writing a basis label as `x=zb`, the full leaf-phase layer is

```math
D_{\mathrm{ph}}
=\sum_z |z\rangle\!\langle z|\otimes
\operatorname{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

This is one total-width-`n` UCG with arbitrary `U(2)` blocks. Yuan--Zhang Lemma
6 gives size `O(2**n)` and depth
`O(n+2**n/(n+m))` for every `m>=0`. Because both the real frame and diagonal
return their workspace clean, the two blocks reuse one pool sequentially. The
complex upper bound follows, and the real subfamily supplies the lower bound.

## 12. Backpropagation consequence

The global Hopf estimator uses the complete inverse differential frame. A
frame-safe implementation acts as the logical frame on every clean-workspace
system input and returns all workspace to zero. The reducing-subspace argument
therefore preserves the full gradient measurement distribution under every
reviewed schedule.

At fixed simultaneous coordinatewise accuracy and confidence, the magnitude
stream uses `O(log n)=O(log log M)` executions for `M=Theta(2**n)` coordinates.
Since the compiled frame matches the optimal state-preparation depth for every
`m>=0`, compilation adds no further asymptotic depth ratio. This final time
comparison remains conditional on charging controlled access to the observable
comparably in scalar and gradient programs.

## 13. Prior-art conclusion

The strict-zero circuit combines familiar ingredients:

- square-root and conjugation identities in controlled-unitary decompositions;
- uniformly controlled one-qubit gates;
- borrowed/dirty or conditionally clean qubits and toggle detection;
- ancilla-free multi-controlled gates.

The review did not locate, in the searched sources, the same use of one original
suffix data qubit to reduce a complete Hopf addressed layer to two total-width-
`d+2` UCGs and linear predicate toggles. This absence is not a proof of novelty.
The claim should remain Hopf-specific and should not describe the abstract echo
as newly invented.

The detailed search record is in
[`PRIOR_ART_SEARCH_2026_09.md`](PRIOR_ART_SEARCH_2026_09.md) and
[`../provenance/prior_art_search.json`](../provenance/prior_art_search.json).

## 14. Final clean-room verdict

The review found no mathematical reason to retain an `m>=1` exception. The
single internally supported theorem candidate is

```math
\boxed{
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(2^n),
\qquad
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
}
```

for every integer `m>=0`.

This conclusion is ready for independent specialist review. It should not be
represented as independently or externally verified until such a review is
recorded.