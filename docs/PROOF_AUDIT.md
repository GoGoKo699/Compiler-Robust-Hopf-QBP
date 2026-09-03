# Internal proof audit of the all-workspace compiler

## Status

This is the consolidated internal audit of the exact Hopf-frame compiler. It
combines the positive-workspace audit with the separate strict-zero echo audit.
It is not external peer review.

The audit question is:

> Does the claimed all-workspace theorem follow from the Hopf operator
> identities, the explicit constructions in this repository, and the exact
> Yuan--Zhang standard-circuit primitives, without silently borrowing workspace
> or weakening complete frame safety to state-column equality?

**Internal verdict:** no operator, workspace, size, depth, endpoint, inverse, or
separated-complex obstruction was found. The supported theorem candidate is

```math
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(2^n),
```

```math
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every integer `m>=0`.

## 1. Source discipline

The following Yuan--Zhang results were checked against the published
*Quantum* paper:

- Theorem 2 gives the optimal QSP frontier for every ancillary budget.
- Lemma 5 gives exact linear-size, linear-depth multi-controlled X without
  ancillary qubits.
- Lemma 6 gives exact UCG size `O(2**q)` and depth
  `O(q+2**q/(q+w))` for total width `q` and `w` ancillary qubits.
- Lemma 9 gives coherent CNOT-tree copying in logarithmic depth.
- Theorem 1 gives the generic controlled-state-preparation comparison.

Sun et al. remain the historical predecessor and original source credited by
Yuan--Zhang for selected primitives. No active construction invokes their
unary-to-binary compiler or selects their older regime theorem as a separate
compiler path.

Classification: **verified**.

## 2. Frame-safe logical target

The compiler must satisfy

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input. It is not sufficient to prepare only the first column.
The repository's exact two-qubit counterexamples show that state-column equality
can permute tangent markers and corrupt both global and checkpoint estimators.

Every construction audited below is therefore checked as a complete operator on
the relevant clean-workspace subspace.

Classification: **proved and enforced by counterexample**.

## 3. Strict-zero borrowed-suffix echo

For a nonfinal depth `d`, fix a prefix `p` and split the suffix into borrowed
system bit `b` and remaining string `r`. Let

```math
h=[r=0],
\qquad
C=R_y(\theta_p/2),
\qquad
J=X.
```

The chronological sequence is

```text
controlled_b(J)
T_h
controlled_b(C)
T_h
controlled_b(J)
T_h
controlled_b(C)
T_h.
```

The Hopf convention gives

```math
C^2=R_y(\theta_p),
\qquad
JCJ=C^{-1},
\qquad
CJCJ=I.
```

The four sectors are:

| `h` | original `b` | chronological target word | final action | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `J,C,J,C` | `CJCJ=I` | 1 |
| 1 | 0 | `C,C` | `R_y(theta_p)` | 0 |
| 1 | 1 | `J,J` | `I` | 1 |

The operator therefore equals the addressed Hopf layer on every computational
sector. The borrowed bit is restored, and no relative phase is introduced.
Orthogonality of the sectors extends the identity to arbitrary superpositions
and entanglement.

Classification: **proved**.

Finite support: every nonfinal layer and complete frame through `n=8`, inverse
checks, and separated-complex checks.

## 4. Strict-zero hidden-workspace audit

The strict-zero schedule uses only original system wires:

- `d` prefix wires;
- one Hopf target;
- one borrowed suffix data wire;
- `n-d-2` remaining suffix wires.

The predicate toggle is a zero-controlled multi-controlled X whose target is
the borrowed data wire. Negative controls are handled by X wrappers. The two
half-angle UCGs act only on the prefix, borrowed wire, and target. The borrowed
wire is not assumed clean, separable, or classical and is restored by the
complete-operator identity.

No clean or dirty ancillary wire is hidden.

Classification: **proved relative to Yuan--Zhang Lemmas 5 and 6**.

## 5. Strict-zero endpoints

- `n=1`: no echo layer; the real frame is one one-qubit rotation.
- `d=0`: the half-angle UCG has total width two.
- `d=n-2`: the remaining suffix is empty, so `T_h=X` on the borrowed bit.
- `d=n-1`: no suffix exists; the final depth is one ordinary `n`-qubit UCG.

All endpoints are represented explicitly in the implementation and tests.

Classification: **verified**.

## 6. Strict-zero resource summation

A half-angle UCG has total width

```math
q=d+2.
```

Two such UCGs, four predicate toggles, and two CNOT echoes give

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

The complete size is

```math
O\left(
\sum_{d=0}^{n-2}2^d+
\sum_{d=0}^{n-2}(n-d)+N
\right)
=O(N).
```

The dyadic-harmonic estimate

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq 6\frac{2^n}{n}
```

and polynomial absorption `n**2=O(2**n/n)` give

```math
D(W_{\mathbb R})=O(n+N/n).
```

Exact-rational regression tests check the displayed inequalities over broad
ranges without floating-point fitting.

Classification: **proved**.

## 7. Tree-cut identities for positive workspace

For a cut after `t` depths,

```math
F_t^{(n)}
=W_t\otimes|0^s\rangle\!\langle0^s|
+I\otimes(I-|0^s\rangle\!\langle0^s|),
```

and

```math
R_t^{(n)}=\bigoplus_r W_s^{(r)}.
```

The global-to-local subtree angle map is exact. Products reconstruct the
complete frame.

Classification: **proved**.

Finite support: every cut through `n=8` with independently built matrices.

## 8. Binary--one-hot decoder and conditioned prefix

For `B=2**t`, the decoder uses `B` one-hot leaves, `B-1` internal indicators,
and `B-1-t` shared scratch qubits. Its clean workspace is

```math
3B-2-t.
```

The explicit reversible schedule satisfies

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle,
```

has depth `11t-4=O(t)`, size `O(B)`, and pairwise-disjoint support inside every
reported circuit layer. The one-hot Givens network equals the complete
`t`-qubit Hopf frame on the code.

After forward decoding, the cleaned internal/scratch wires are reused for the
external suffix predicate and its coherent copies. The complete conditioned
prefix has depth `O(n)`, size `O(B+s)`, and no hidden additional workspace.

Classification: **proved**.

## 9. Positive low-workspace schedule

For `m>=1`, every nonfinal addressed depth computes one suffix flag, applies one
prefix-and-flag UCG, and uncomputes the flag. The final depth needs no flag.
Yuan--Zhang Lemmas 5 and 6 give

```math
S=O(N),
```

```math
D=O\left(n^2+\frac{N}{n+m}\right).
```

For `1<=m<4n`, the polynomial term is absorbed by the exponential term.

Classification: **proved relative to imported primitives**.

## 10. Routed positive-workspace schedule

The exact routed-tail workspace includes branch data, one-hot activation tokens,
coherent prefix-control copies, and simultaneous branch flags. The copied
control count is

```math
(B-1)(s+1)-t.
```

After routing, the copies are uncomputed and their clean wires are reused as
branch flags. The routed tail and conditioned prefix both fit inside

```math
2B(s+1).
```

Route and unroute have depth `O(n)` and size `O(B(s+1))`. One controlled
subtree frame has size `O(2**s)` and depth `O(s**2+2**s/s)`. The `B` branches
have disjoint support and run in parallel.

Classification: **proved relative to Yuan--Zhang Lemmas 5, 6, and 9**.

## 11. Positive-workspace cut choice

For `m>=4n`, choose the largest feasible cut satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If `s=n-t>1`, maximality gives `m<4*2**t*s`, hence

```math
\frac{2^s}{s}<4\frac{N}{m}
=O\left(\frac{N}{n+m}\right).
```

Together with `s**2=O(n+2**s/s)`, this gives routed depth

```math
O\left(n+\frac{N}{n+m}\right).
```

Classification: **proved**.

## 12. Lower bounds

Applying the frame to `|0^n>` prepares every real unit vector, a manifold of
dimension `N-1`.

- At most four real continuous parameters occur per arbitrary one-qubit gate,
  giving size `Omega(N)`.
- A depth layer on `n+m` wires has at most `n+m` one-qubit gate locations,
  giving `Omega(N/(n+m))` depth.
- For positive workspace, a backward-light-cone count gives the independent
  `Omega(n)` term.
- At `m=0`, `Omega(N/n)` follows directly from parameter counting on exactly
  `n` wires and asymptotically dominates `n`.

Thus

```math
D=\Omega\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`.

Classification: **proved**.

## 13. Complex frame

The leaf-phase diagonal is one total-width-`n` UCG with blocks

```math
\operatorname{diag}(e^{i\phi_{z0}},e^{i\phi_{z1}}).
```

Yuan--Zhang Lemma 6 gives size `O(N)` and depth
`O(n+N/(n+m))` for every `m>=0`. It reuses the real-frame workspace
sequentially; at `m=0` both blocks are ancilla-free. The real subfamily gives the
matching lower bounds.

Classification: **proved relative to Lemma 6**.

## 14. QBP composition

Frame-safe substitution preserves the complete global gradient distribution.
The magnitude and phase decoders do not depend on the elementary compiler.
Therefore the all-workspace compiler adds no asymptotic factor beyond the
`O(log n)` magnitude execution count at fixed coordinatewise accuracy and
confidence, subject to the declared controlled-observable access model.

Classification: **proved under the stated access model**.

## 15. Prior-art and novelty audit

The abstract strict-zero echo combines two familiar themes:

- square-root/conjugation decompositions of controlled unitaries;
- borrowed or dirty-bit toggle detection.

It should not be advertised as a wholly new general identity. The present prior-
art search did not identify a source deriving the same Hopf addressed-layer
aggregation or the resulting optimal complete-frame strict-zero frontier.
Nevertheless, the search is not a legal novelty opinion and should be expanded
before submission.

The claim-safe project contribution is:

> use one original suffix data qubit as a restored predicate carrier, aggregate
> all prefix-dependent Hopf rotations into two width-`d+2` UCGs per nonfinal
> depth, and combine this with the positive-workspace schedules to attain the
> optimal complete-frame frontier for every ancillary budget.

Classification: **conservative internal prior-art assessment; broader review
pending**.

## 16. Audit conclusion

The active all-workspace theorem is internally supported by one coherent
construction:

```text
strict-zero borrowed-suffix echo
+ direct positive-workspace flagged UCGs
+ self-contained tree decoder
+ Hopf tree direct sum and coherent routing
+ Yuan--Zhang UCG/MCT/copy primitives
+ one-UCG complex phase layer.
```

Remaining gates:

- independent human proof review;
- broader prior-art review and final novelty wording;
- hardware and approximate-gate extensions;
- application-specific controlled-observable costs.
