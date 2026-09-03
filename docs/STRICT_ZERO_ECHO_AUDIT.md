# Internal proof audit of the strict-zero borrowed-suffix echo

## Status and verdict

This is a second, line-by-line internal audit of the construction in
[`STRICT_ZERO_BORROWED_SUFFIX_ECHO.md`](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md).
It is not external peer review.

**Verdict.** No operator, workspace, size, depth, endpoint, inverse, or complex-
frame obstruction was found. Relative to the exact no-ancilla multi-controlled-
X and UCG synthesis statements imported from Yuan and Zhang, the construction
supports

```math
S_{\mathbb R}(n,0)=\Theta(2^n),
\qquad
D_{\mathbb R}(n,0)=
\Theta\left(n+\frac{2^n}{n}\right),
```

and the same asymptotic bounds for the separated complex frame.

The scientific status should be **internally audited theorem candidate** until
Issue #17 receives independent review. The abstract echo should not be claimed
as a new general circuit identity: its ingredients are closely related to
classical square-root control decompositions and dirty-ancilla toggle detection.
The project-specific contribution is the way the echo aggregates all
prefix-dependent Hopf rotations into two small UCGs per tree depth and thereby
closes the complete-frame `m=0` size--depth frontier.

## 1. Exact operator statement

Fix a nonfinal Hopf depth `d<n-1`. Work in a sector of the upper-prefix register
`p` and the remaining lower suffix `r`. Let

```math
h=[r=0]
```

and retain one original suffix data qubit `b`. The target is a separate system
qubit. Define

```math
C=C_p=R_y(\theta_p/2),
\qquad
J=X.
```

In the repository convention,

```math
R_y(\alpha)=e^{-i\alpha Y}
=\begin{pmatrix}
\cos\alpha&-\sin\alpha\\
\sin\alpha&\cos\alpha
\end{pmatrix}.
```

Therefore

```math
C^2=R_y(\theta_p),
\qquad
JCJ=C^{-1},
\qquad
CJCJ=I.
```

Let `T_h` map `b` to `b xor h`. The chronological circuit is

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

Neither `p` nor `r` changes. The target words and final borrowed-bit values are:

| `h` | initial `b` | target word in chronological order | final target operator | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `J,C,J,C` | `CJCJ=I` | 1 |
| 1 | 0 | `C,C` | `C^2=R_y(theta_p)` | 0 |
| 1 | 1 | `J,J` | `I` | 1 |

Thus the circuit applies the desired rotation precisely when the **original**
complete suffix is zero. Every other computational sector receives the
identity. The borrowed data qubit returns to its original value, and no
sector-dependent phase is produced.

Because `p` and `r` label mutually orthogonal invariant sectors, this sector
calculation proves equality as a complete operator. It applies to arbitrary
superpositions and arbitrary entanglement among all system qubits. No
initialized-state assumption is used.

## 2. Chronological versus matrix order

A common source of mistakes in echo arguments is reversing the target word. In
the unwanted `h=0,b=1` sector, the chronological gates are

```text
J, C, J, C.
```

For column vectors, the resulting matrix is

```math
CJCJ=C(JCJ)=CC^{-1}=I.
```

The implementation composes every chronological gate by left multiplication,
which matches this convention. The abstract sector test and the complete matrix
test independently enforce the same order.

## 3. No hidden ancillary qubit

The construction uses only the original `n` system wires:

- `d` prefix wires;
- one Hopf target;
- one borrowed suffix data wire;
- `n-d-2` remaining suffix wires.

The borrowed wire is not assumed clean, idle, separable, or classical. It may
begin in an arbitrary state entangled with the rest of the system. The complete-
operator identity proves exact restoration.

The predicate toggle `T_h` is a multi-controlled X whose target is the borrowed
system wire. Its controls are the remaining suffix wires, wrapped by parallel X
gates to turn the all-zero condition into an all-one condition. Yuan--Zhang
Lemma 5 gives an exact standard-circuit implementation with linear size and
depth and no ancillary qubit. The X wrappers introduce no additional wires.

The two half-angle UCGs act only on the prefix, borrowed wire, and Hopf target.
They use no workspace under the `m=0` specialization of Yuan--Zhang Lemma 6.
Idle suffix wires are not counted as hidden compiler ancillas and are not used
by that synthesis claim.

## 4. UCG identification and width

For every prefix string `p`, the half-angle UCG has the two borrowed-bit blocks

```math
U_{p,0}=I,
\qquad
U_{p,1}=R_y(\theta_p/2).
```

The control register has `d+1` qubits (`d` prefix bits and the borrowed bit) and
the target register has one qubit. In the notation where the total UCG width is
`q`,

```math
q=d+2.
```

Yuan--Zhang Lemma 6 therefore gives, at zero ancillary workspace,

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^{d+2})=O(2^d)
```

and

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^{d+2}}{d+2}\right).
```

The complete nonfinal layer uses two such UCGs, four predicate toggles, and two
CNOT echoes. If

```math
s=n-d-1,
```

then

```math
S(L_d)=O(2^d+s)
```

and

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

Replacing `d+2` by `d+1` in an asymptotic summary is harmless, but the audit
uses the exact participating width `d+2`.

## 5. Exact endpoint checks

### `n=1`

There is no borrowed-suffix layer. The complete real frame is one one-qubit
rotation, and the complex phase layer is one one-qubit diagonal gate.

### `d=0`

The half-angle UCG is a two-qubit controlled rotation selected only by the
borrowed bit. No prefix edge case is hidden.

### `d=n-2`

There are no remaining suffix controls. The predicate is identically true and
`T_h=X` on the borrowed wire. The four-sector proof still applies exactly.

### `d=n-1`

There is no lower suffix and no borrowed wire. This final depth is compiled
separately as one ordinary `n`-qubit UCG. It is not passed through the echo.

## 6. Size summation

The two half-angle UCGs at depth `d` contribute `O(2^d)` size. The four
predicate toggles contribute `O(n-d)` size. The final UCG contributes `O(N)`.
Thus

```math
\begin{aligned}
S(W_{\mathbb R})
&=O\left(
\sum_{d=0}^{n-2}2^d
+\sum_{d=0}^{n-2}(n-d)
+N
\right)\\
&=O(N+n^2)\\
&=O(N).
\end{aligned}
```

The exponential sum is geometric. The polynomial absorption follows, for
example, from `n**2=O(2**n)`. No cancellation between adjacent Hopf depths is
needed.

## 7. Depth summation with an explicit bound

Set `q=d+2`. The UCG exponential terms are bounded by

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq 6\frac{2^n}{n}.
```

A direct proof splits the sum at `floor(n/2)`:

- the early half is at most `2**(floor(n/2)+1)`;
- in the late half, `1/q<=2/n` and the geometric numerator sum is below
  `2**(n+1)`.

For `n>=4`, `n<=2**(n/2)`, so the early half is at most `2*2**n/n`; the late
half is at most `4*2**n/n`. The cases `n=1,2,3` are immediate.

All linear UCG-width terms and all predicate depths contribute `O(n**2)`. The
uniform elementary inequality

```math
n^2\leq 4\frac{2^n}{n}
```

holds for every positive integer `n`. One may check `n<=4` directly; after that,
`n**3/2**n` decreases.

Consequently,

```math
D(W_{\mathbb R})
=O\left(n^2+\frac{N}{n}\right)
=O\left(n+\frac{N}{n}\right).
```

The exact-rational regression checks in `strict_zero_audit.py` verify both
uniform inequalities without floating-point arithmetic through a wide finite
range. These checks support but do not replace the preceding proof.

## 8. Lower bound at strict zero workspace

Applying `W_R(theta)` to `|0^n>` ranges over an open `(N-1)`-dimensional family
of real normalized states. A standard circuit with `G` arbitrary one-qubit
gates carries at most `4G` real continuous parameters; CNOTs carry none. Hence

```math
S(W_{\mathbb R})=\Omega(N).
```

At depth `D` on exactly `n` wires, at most `nD` one-qubit-gate locations are
available. Therefore

```math
4nD\geq N-1,
```

which gives

```math
D=\Omega(N/n).
```

Since `n=O(N/n)`, this is equivalent asymptotically to

```math
D=\Omega\left(n+\frac{N}{n}\right).
```

No separate light-cone argument is needed for the strict-zero endpoint. This
simplifies the lower-bound proof and avoids importing more machinery than is
necessary.

## 9. Inverse and complex frame

The real construction is an exact unitary on the original system register.
Taking its adjoint reverses the gate order and adjoints each gate, so
`W_R^dagger` has identical size, depth, and width.

For the separated complex frame,

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

The diagonal `D_ph` is one exact `n`-qubit UCG with arbitrary diagonal `U(2)`
blocks. Yuan--Zhang Lemma 6 gives `O(N)` size and
`O(n+N/n)` depth with zero ancillary qubits. The real and diagonal circuits are
sequential, so the complex frame has the same asymptotic strict-zero resources.
The real subfamily supplies the matching lower bound.

## 10. Imported results checked

The audit uses the following statements from Yuan and Zhang, *Quantum* **7**,
956 (2023):

- Lemma 5: exact multi-controlled X with `O(k)` standard-circuit size and depth
  and no ancillary qubit;
- Lemma 6: any total-width-`q` UCG has size `O(2**q)` and depth
  `O(q+2**q/(q+m))` with `m` ancillary qubits;
- Theorem 2: the optimal QSP frontier for comparison.

The UCG definition allows a separate arbitrary one-qubit block for every
control string, so the identity/half-rotation block table used here is covered.

## 11. Prior-art classification

The audit found close antecedents for the ingredients:

1. Barenco et al., *Elementary gates for quantum computation* (1995), prove
   `X R_y(theta) X=R_y(-theta)` and use square roots of target unitaries to add
   controls. Their fixed-zero-bit construction is also the classical clean-flag
   predecessor of the present problem.
2. Khattar and Gidney, *Quantum* **9**, 1752 (2025), describe dirty-ancilla
   toggle detection: a self-inverse consumed operation can be repeated around a
   dirty predicate target so that the unwanted branch cancels.
3. Möttönen/Bergholm multiplexors provide the uniformly controlled rotation
   viewpoint, while Yuan--Zhang supply the active optimal-depth UCG bound.
4. Linear ancilla-free multi-controlled `SU(2)` decompositions and recent
   restricted-UCG work are relevant comparisons, but applying one
   multi-controlled rotation per prefix would retain an extra factor of `n`, and
   the restricted-UCG sparsity notions checked do not directly yield the
   `O(2^d+n)` addressed-layer bound.

The eight-step echo combines familiar square-root/conjugation and borrowed-bit
ideas. The repository therefore makes no claim that the abstract identity is
new. A defensible novelty target is narrower:

> aggregating all prefix-dependent Hopf rotations into two width-`d+2` UCGs,
> using one original suffix data qubit as the restored predicate carrier, and
> obtaining the optimal complete-frame frontier at `m=0`.

A broader literature search by an independent reviewer remains required before
publication wording is frozen.

## 12. Audit conclusion

Relative to the declared exact circuit model and the cited synthesis lemmas, the
strict-zero construction closes the mathematical gap left in PR #14:

```math
S_{\mathbb R}(n,0)=S_{\mathbb C}(n,0)=\Theta(N),
```

```math
D_{\mathbb R}(n,0)=D_{\mathbb C}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

Combined with the positive-workspace theorem, the internally audited target is
now the all-budget statement

```math
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(N),
```

```math
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every integer `m>=0`.

Promotion into the active consolidation theorem should wait for Issue #17's
independent proof and prior-art review.

## Primary references

- P. Yuan and S. Zhang, [Optimal (controlled) quantum state preparation and
  improved unitary synthesis by quantum circuits with any number of ancillary
  qubits](https://quantum-journal.org/papers/q-2023-03-20-956/pdf/),
  *Quantum* **7**, 956 (2023).
- A. Barenco et al., [Elementary gates for quantum
  computation](https://arxiv.org/abs/quant-ph/9503016), *Physical Review A*
  **52**, 3457 (1995).
- T. Khattar and C. Gidney, [Rise of conditionally clean ancillae for efficient
  quantum circuit constructions](https://quantum-journal.org/papers/q-2025-05-21-1752/),
  *Quantum* **9**, 1752 (2025).
- V. Bergholm, J. J. Vartiainen, M. Möttönen, and M. M. Salomaa, [Quantum
  circuits with uniformly controlled one-qubit
  gates](https://arxiv.org/abs/quant-ph/0410066), *Physical Review A* **71**,
  052330 (2005).
