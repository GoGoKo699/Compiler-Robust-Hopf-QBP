# Internal audit: strict-zero borrowed-suffix echo

[← Focused construction](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Verification](VERIFICATION.md)

## Status and question

This document records an internal reconstruction of the strict-zero schedule. It
is not external peer review.

The audit asks whether the `m=0` circuit:

1. implements the complete addressed Hopf layer on every logical input;
2. restores the borrowed logical suffix bit exactly;
3. uses no hidden ancillary wire;
4. has the stated UCG width and predicate cost;
5. sums to the state-preparation-optimal strict-zero frontier.

No operator, workspace, size, depth, endpoint, inverse, or complex-magnitude
obstruction was found. Relative to the exact no-ancilla multi-controlled-`X` and
UCG statements imported from P. Yuan and S. Zhang, the construction supports

```math
S_{\mathbb R}(n,0)
=S_{\mathbb C,\mathrm{mag}}(n,0)
=\Theta(2^n),
```

```math
D_{\mathbb R}(n,0)
=D_{\mathbb C,\mathrm{mag}}(n,0)
=\Theta\left(n+\frac{2^n}{n}\right).
```

The complex leaf-phase derivatives remain a separate direct measurement stream.
The audit distinguishes the Hopf-specific two-UCG reduction from its familiar
component ideas.

## 1. Operator target

At a nonfinal depth `d<n-1`, split the system register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R.
```

The required layer is

```math
L_d
=I+
\sum_p|p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_p)-I\bigr)
\otimes|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

This is a complete operator specification. Correctness only on the preparation
input is not sufficient.

**Audit classification:** target fixed independently of the proposed circuit.

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

| `h` | original `b` | chronological target word | resulting matrix | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `J,C,J,C` | `CJCJ=I` | 1 |
| 1 | 0 | `C,C` | `C^2=R_y(theta_p)` | 0 |
| 1 | 1 | `J,J` | `I` | 1 |

The desired rotation appears only when the original complete suffix is zero.
Every other sector receives identity. The borrowed bit returns to its original
value and no sector-dependent phase remains.

The labels `p` and `r` define orthogonal invariant sectors. The calculation
therefore proves equality on arbitrary superpositions and on states in which
`b` is entangled with the rest of the system.

**Audit classification:** algebraically proved.

## 3. Chronological and matrix order

The unwanted sector receives the chronological target word

```text
J, C, J, C.
```

For column vectors, the corresponding matrix is

```math
CJCJ=C(JCJ)=CC^{-1}=I.
```

The implementation composes chronological gates by left multiplication. Both
the sector helper and the complete layer matrix therefore use the same order as
the proof.

**Audit classification:** checked independently in algebra and code.

## 4. Restoration and hidden workspace

The circuit uses only:

- `d` prefix wires;
- one target wire;
- one borrowed suffix data wire;
- `n-d-2` remaining suffix wires.

The borrowed wire is not assumed clean, idle, classical, or separable. Its
restoration follows from the complete sector table.

The predicate toggle is a negative-control multi-controlled `X` whose target is
the borrowed system wire. Parallel `X` wrappers convert the all-zero controls to
all-one controls. Yuan–Zhang Lemma 5 supplies an exact zero-ancilla
decomposition.

The half-angle UCG acts only on the prefix, borrowed bit, and target. The
remaining suffix bits are idle during that UCG and are not compiler workspace.

**Audit classification:** no hidden clean or dirty ancillary wire found.

## 5. Exact UCG width

For each prefix `p`, the UCG blocks are

```math
U_{p,0}=I,
\qquad
U_{p,1}=R_y(\theta_p/2).
```

There are `d+1` controls, namely the `d` prefix bits and the borrowed bit, plus
one target. The exact total width is

```math
\boxed{q=d+2.}
```

This convention matches Yuan–Zhang Lemma 6 and is used consistently in the
implementation and resource rows.

**Audit classification:** participant count verified.

## 6. Endpoint audit

- `n=1`: no borrowed-suffix layer exists; the frame is one one-qubit rotation.
- `d=0`: the half-angle UCG has total width two.
- `d=n-2`: the remaining suffix is empty, so `h=1` and `T_h=X_b`.
- `d=n-1`: the final depth has no suffix and uses one ordinary `n`-qubit UCG.

**Audit classification:** all endpoints explicit in code and tests.

## 7. Size audit

Two width-`d+2` UCGs contribute `O(2^d)` size. Four predicate toggles contribute
`O(n-d)`, and the target echoes contribute constants. Hence

```math
S(L_d)=O(2^d+n-d).
```

Summing gives

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

The real-state family has dimension `2^n-1`, yielding the matching
`Omega(2^n)` parameter-count lower bound.

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

The exact-rational audit checks the uniform bound

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

On exactly `n` wires, a depth-`D` circuit contains only `O(nD)` continuously
parameterized one-qubit locations. Covering the `2^n-1` dimensional real-state
family requires

```math
D=\Omega(2^n/n).
```

**Audit classification:** matching asymptotic depth verified.

## 9. Inverse and complex magnitude frame

Reversing the exact circuit and adjointing each gate gives `W_R^dagger` with the
same resources.

The phase layer

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\mathrm{diag}(e^{i\phi_{z0}},e^{i\phi_{z1}})
```

is one total-width-`n` UCG. At zero workspace it has `O(2^n)` size and
`O(n+2^n/n)` depth. Therefore

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}
```

inherits the same strict-zero frontier.

The direct leaf-phase derivatives are not additional columns of this frame.

**Audit classification:** no additional complex-magnitude obstruction found.

## 10. Contribution boundary

The component ideas have established precedents:

- controlled-unitary roots and conjugation;
- multiplexed rotations and UCGs;
- borrowed or conditionally clean logical qubits;
- toggle-detection cancellation;
- ancilla-free multi-controlled gates.

The Hopf-specific statement is the reduction of one addressed depth to two
width-`d+2` UCGs using a restored original suffix bit, together with the optimal
complete-frame strict-zero resource consequence.

See [Related work](RELATED_WORK.md) and
[the strict-zero prior-art boundary](STRICT_ZERO_PRIOR_ART.md).

## 11. Audit conclusion

The internal reconstruction found no mathematical reason to exclude `m=0` from
the all-workspace theorem. The construction satisfies the complete operator
contract, uses no hidden wire, covers all endpoints, restores the borrowed
logical bit, and matches the state-preparation lower bounds.

Independent technical and prior-art assessment remains the final scientific
check. Executable tests are supporting evidence, not the basis of the
size-independent proof.

---

[← Focused construction](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Verification](VERIFICATION.md)
