# Internal audit of the strict-zero borrowed-suffix echo

[← Focused construction](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) · [Verification overview](VERIFICATION.md) · [Complete narrative](../REVIEW.md)

## Status and verdict

This document records a line-by-line internal reconstruction of the strict-zero
compiler. It is not independent external review.

No operator, workspace, size, depth, endpoint, inverse, or separated-complex
obstruction was found. Relative to the exact no-ancilla multi-controlled-X and
UCG statements imported from Yuan and Zhang, the construction supports

```math
S_{\mathbb R}(n,0)=S_{\mathbb C}(n,0)=\Theta(2^n),
```

```math
D_{\mathbb R}(n,0)=D_{\mathbb C}(n,0)
=\Theta\left(n+\frac{2^n}{n}\right).
```

The audit also narrows the contribution claim: the abstract echo has close
precedents, while the Hopf-specific two-UCG aggregation and complete-frame
resource consequence are the relevant new statements.

## 1. Exact operator target

At a nonfinal depth `d<n-1`, split the register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R.
```

The desired addressed layer is

```math
L_d
=I+
\sum_p|p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_p)-I\bigr)
\otimes|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The audit treats this as a complete operator equality. No initialized-state or
first-column restriction is used.

## 2. Sector reconstruction

Set

```math
h=[r=0],
\qquad
C=R_y(\theta_p/2),
\qquad
J=X.
```

Let `T_h` map `b` to `b xor h`. The chronological sequence is

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

The rotation convention gives

```math
C^2=R_y(\theta_p),
\qquad
JCJ=C^{-1},
\qquad
CJCJ=I.
```

The four sectors are:

| `h` | original `b` | chronological target word | final target operator | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `J,C,J,C` | `CJCJ=I` | 1 |
| 1 | 0 | `C,C` | `C^2=R_y(theta_p)` | 0 |
| 1 | 1 | `J,J` | `I` | 1 |

The desired rotation appears only when the original complete suffix is zero.
All other sectors receive identity. The borrowed bit is restored and no
sector-dependent phase is produced.

Because `p` and `r` label orthogonal invariant sectors, this proves equality on
arbitrary superpositions and entangled inputs.

**Audit classification:** algebraically proved.

## 3. Chronological versus matrix order

The unwanted sector has chronological target word

```text
J, C, J, C.
```

For column vectors, the matrix is

```math
CJCJ=C(JCJ)=CC^{-1}=I.
```

The implementation composes chronological gates by left multiplication, so its
matrix order agrees with the proof. Both the abstract sector test and the full
layer matrix test enforce this convention.

**Audit classification:** checked independently in algebra and implementation.

## 4. Restoration and hidden-workspace audit

The circuit uses only the original system wires:

- `d` prefix wires;
- one target wire;
- one borrowed suffix data wire;
- `n-d-2` remaining suffix wires.

The borrowed wire is not assumed clean, idle, separable, or classical. Its
restoration follows from the complete sector table.

The predicate toggle is a negative-control multi-controlled X whose target is
the borrowed system wire. Parallel X wrappers convert all-zero controls to
all-one controls. Yuan–Zhang Lemma 5 supplies the exact zero-ancilla
decomposition.

The half-angle UCG acts only on the prefix, borrowed wire, and target. The
remaining suffix wires are idle during the UCG and are not compiler workspace.

**Audit classification:** no hidden clean or dirty ancillary wire found.

## 5. Exact UCG width

For each prefix `p`, the borrowed-bit UCG blocks are

```math
U_{p,0}=I,
\qquad
U_{p,1}=R_y(\theta_p/2).
```

There are `d+1` controls—`d` prefix bits and the borrowed bit—and one target.
The total UCG width in the Yuan–Zhang convention is therefore

```math
\boxed{q=d+2.}
```

This count is used consistently in the implementation, resource rows, and
asymptotic proof.

**Audit classification:** exact participant count verified.

## 6. Endpoint audit

### `n=1`

No borrowed-suffix layer exists. The complete real frame is one one-qubit
rotation.

### `d=0`

There are no prefix controls. The half-angle UCG is a two-qubit controlled
rotation selected only by the borrowed bit.

### `d=n-2`

The remaining suffix `r` is empty, so `h=1` identically and `T_h=X_b`. The same
sector proof applies.

### `d=n-1`

No lower suffix exists. The final depth is one ordinary `n`-qubit UCG and is not
passed through the echo.

**Audit classification:** all endpoints explicit in code and tests.

## 7. Size audit

Two width-`d+2` UCGs contribute `O(2^d)` size. Four predicate toggles contribute
`O(n-d)` size. Two target echoes contribute constants. Hence

```math
S(L_d)=O(2^d+n-d).
```

The complete real frame satisfies

```math
\begin{aligned}
S(W_{\mathbb R})
&=O\left(
\sum_{d=0}^{n-2}2^d
+\sum_{d=0}^{n-2}(n-d)
+2^n
\right)\\
&=O(2^n+n^2)\\
&=O(2^n).
\end{aligned}
```

The real-state family has dimension `2^n-1`, so parameter counting gives the
matching `Omega(2^n)` lower bound.

**Audit classification:** upper and lower bounds verified.

## 8. Depth audit

The two UCGs contribute

```math
O\left(d+2+\frac{2^d}{d+2}\right)
```

depth up to a constant factor. The predicate toggles contribute `O(n-d)`.
Therefore

```math
D(L_d)
=O\left(n+\frac{2^d}{d+2}\right).
```

The UCG exponential terms satisfy

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq6\frac{2^n}{n}.
```

The linear-width and predicate terms total `O(n^2)`, and

```math
n^2=O(2^n/n).
```

Thus

```math
D(W_{\mathbb R})=O(n+2^n/n).
```

At zero workspace, a depth-`D` circuit on exactly `n` wires contains only
`O(nD)` continuously parameterized one-qubit locations. Covering the
`2^n-1` dimensional real-state family requires

```math
D=\Omega(2^n/n),
```

which supplies the matching lower bound.

The regression suite evaluates the two uniform inequalities with exact rational
or integer arithmetic across broad finite ranges. The proof itself is the
preceding dimension-independent argument.

**Audit classification:** matching asymptotic depth verified.

## 9. Inverse and complex-frame audit

The circuit is unitary and exact, so reversing and adjointing its gates gives
`W_R^dagger` with the same resources.

The phase layer

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\operatorname{diag}(e^{i\phi_{z0}},e^{i\phi_{z1}})
```

is one exact `n`-qubit UCG. At zero workspace it has `O(2^n)` size and
`O(n+2^n/n)` depth. Therefore

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

inherits the same strict-zero frontier.

**Audit classification:** no additional complex obstruction found.

## 10. Prior-art boundary

The audit identifies close antecedents for the component ideas:

- square-root and conjugation constructions for controlled unitaries;
- multiplexed rotations and UCGs;
- borrowed or conditionally clean logical qubits;
- toggle-detection cancellation;
- ancilla-free multi-controlled gates.

The repository does not claim these ingredients as inventions. The claim-safe
Hopf-specific statement is the two-UCG reduction of one addressed depth using a
restored original suffix bit, together with the optimal complete-frame
strict-zero frontier.

See [Related work](RELATED_WORK.md) and
[the broader technical search record](PRIOR_ART_SEARCH_2026_09.md).

## 11. Audit conclusion

The internal reconstruction found no mathematical reason to exclude `m=0`
from the all-workspace theorem. The strict-zero result is consistent with the
operator contract, uses no hidden wire, covers every endpoint, and matches the
real-state lower bound.

The result remains under independent technical review. The executable checks
are supporting evidence, and the prior-art classification remains subject to a
broader specialist assessment.

---

[← Focused construction](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) · [Verification overview](VERIFICATION.md) · [Complete narrative](../REVIEW.md)
