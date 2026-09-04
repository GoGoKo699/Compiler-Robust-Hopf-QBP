# Strict zero workspace: the borrowed-suffix echo

[← Complete compiler theorem](COMPILER_THEOREM.md) · [Complete technical note](../REVIEW.md) · [Strict-zero audit →](STRICT_ZERO_ECHO_AUDIT.md)

The small-positive-workspace compiler stores the common lower-suffix predicate
in one clean bit. At `m=0`, that bit is unavailable. This page isolates the
in-place replacement that closes the strict-zero endpoint without widening the
prefix-selected UCG to the full system register.

Let

```math
N=2^n.
```

The result is

```math
S_{\mathbb R}(n,0)=\Theta(N),
```

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

The phase-dressed complex magnitude frame has the same frontier. The leaf-phase
derivatives use a separate direct measurement stream.

## 1. Addressed layer

At a nonfinal tree depth `d<n-1`, write the logical register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R,
```

where:

- `p` is the `d`-bit Hopf prefix;
- `x` is the rotation target;
- `b` is the first bit of the lower suffix;
- `r` contains the remaining `n-d-2` suffix bits.

The required complete operator is

```math
L_d
=I+
\sum_p|p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

Thus `R_y(theta_(d,p))` must be applied exactly when the original suffix `br`
is zero. Every other suffix sector must be fixed.

A direct full-width Möttönen multiplexor represents this same block table, but
the standard angle transform is generically dense across the suffix controls.
The construction below instead keeps the UCG width tied to the prefix.

## 2. Borrow one logical suffix bit

Define

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Let `T_h` toggle `b` iff `h(r)=1`:

```math
T_h:
|b\rangle|r\rangle
\longmapsto
|b\oplus h(r)\rangle|r\rangle.
```

`T_h` is a negative-control multi-controlled `X` whose target is the original
logical bit `b`. It uses no additional wire.

Apply the following gates chronologically:

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
  <img src="../assets/strict-zero-echo.svg" width="1040" alt="Ancilla-free borrowed-suffix echo for one addressed Hopf depth." />
</p>

The Hopf rotation convention is

```math
R_y(\alpha)=e^{-i\alpha Y}.
```

Hence

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
XC_pX=C_p^{-1}.
```

## 3. Complete four-sector proof

Fix a prefix `p` and a remaining suffix `r`.

| `h(r)` | original `b` | chronological target word | resulting target matrix | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_pXC_pX=I` | 1 |
| 1 | 0 | `C_p,C_p` | `C_p^2=R_y(theta_(d,p))` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

The chronological word `X,C_p,X,C_p` acts on column vectors as
`C_pXC_pX`. The unwanted original-`b=1` branch therefore cancels exactly.

The active sector is `h(r)=1` with original `b=0`, precisely the condition that
the complete original suffix `br` is zero. Every other sector receives identity.
The borrowed bit is toggled either zero or four times and returns to its original
value. No sector-dependent scalar phase remains.

The prefix and remaining-suffix labels define orthogonal invariant sectors.
The sector table therefore proves the complete operator identity on arbitrary
superpositions and on inputs in which the borrowed bit is entangled with the
rest of the system:

```math
\boxed{E_d=L_d.}
```

> **Technical checkpoint.** The borrowed wire is logical data whose original
> value is part of the predicate. Correctness must include every initial value
> of that wire and exact restoration, not only the zero-suffix preparation
> branch.

## 4. UCG width and elementary primitives

Each controlled `C_p` is one UCG with:

- `d` prefix controls;
- the borrowed bit as one additional control;
- one target.

Its exact total width in the Yuan–Zhang convention is

```math
\boxed{q=d+2.}
```

The remaining suffix bits participate only in `T_h` and are not workspace.
Yuan–Zhang Lemma 5 supplies an exact ancilla-free implementation of `T_h`, and
Lemma 6 supplies the exact zero-workspace UCG size–depth tradeoff.

The published article corresponds to `arXiv:2202.11302v2`; the imported
statements were also checked in v3.

## 5. One-layer resources

Lemma 6 gives

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^d),
```

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^d}{d+2}\right).
```

A nonfinal layer contains two such UCGs, four predicate toggles, and two CNOT
echoes. Therefore

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)
=O\left(n+\frac{2^d}{d+2}\right).
```

The long suffix predicate is paid only a constant number of times per depth.
The `2^d` prefix-dependent rotations remain aggregated inside two UCGs.

## 6. Complete real frame

The final depth has no lower suffix and is one ordinary total-width-`n` UCG.
Summing size gives

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

For the depth-dependent UCG terms,

```math
\sum_{d=0}^{n-2}\frac{2^d}{d+2}
=O(N/n).
```

A uniform inequality used by the exact-rational audit is

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq6\frac{2^n}{n}.
```

The linear-width and predicate terms total `O(n^2)`, and

```math
n^2=O(N/n).
```

Hence

```math
S_{\mathbb R}(n,0)=O(N),
```

```math
D_{\mathbb R}(n,0)=O(n+N/n).
```

The real-state family has dimension `N-1`. Parameter counting gives the matching
`Omega(N)` size bound and `Omega(N/n)` depth bound on exactly `n` wires.

## 7. Endpoints

- `n=1`: there is no echo layer; the frame is one one-qubit rotation.
- `d=0`: each half-angle UCG has total width two.
- `d=n-2`: `r` is empty, so `h=1` and `T_h=X_b`.
- `d=n-1`: there is no lower suffix and no borrowed bit.

The implementation and tests cover each endpoint explicitly.

## 8. Inverse and complex magnitude frame

The inverse circuit reverses the gate order and adjoints each gate. It has the
same size, depth, and zero-workspace property.

The phase-dressed complex magnitude frame is

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

The arbitrary leaf-phase diagonal is one exact total-width-`n` UCG, so it has
`O(N)` size and `O(n+N/n)` depth at zero workspace. Sequential composition gives

```math
S_{\mathbb C,\mathrm{mag}}(n,0)=\Theta(N),
```

```math
D_{\mathbb C,\mathrm{mag}}(n,0)
=\Theta(n+N/n).
```

The direct leaf-phase derivatives remain a separate algorithmic stream.

## 9. Relation to familiar circuit techniques

The construction combines established ingredients:

- UCGs and multiplexed rotations;
- controlled-unitary square roots;
- Pauli conjugation;
- borrowed or conditionally clean logical qubits;
- toggle-detection cancellation;
- ancilla-free multi-controlled gates.

The claim is not that these ingredients are new. The Hopf-specific contribution
is the two-UCG aggregation of one addressed tree depth using a restored original
suffix bit, together with the optimal complete-frame strict-zero frontier.

See [Related work](RELATED_WORK.md) and
[the focused prior-art boundary](STRICT_ZERO_PRIOR_ART.md).

## 10. Executable support

- [Construction and resource rows](../compiler_robust_hopf/strict_zero_echo.py)
- [Complete sector, layer, frame, inverse, and complex tests](../tests/test_strict_zero_echo.py)
- [Exact-rational audit helpers](../compiler_robust_hopf/strict_zero_audit.py)
- [Audit tests](../tests/test_strict_zero_audit.py)
- [Human-readable ledger](../scripts/strict_zero_echo_ledger.py)

The tests support the operator proof and resource ledger. They do not replace
the dimension-independent argument.

---

[← Complete compiler theorem](COMPILER_THEOREM.md) · [Complete technical note](../REVIEW.md) · [Strict-zero audit →](STRICT_ZERO_ECHO_AUDIT.md)
