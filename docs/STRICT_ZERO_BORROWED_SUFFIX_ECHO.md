# Strict-zero borrowed-suffix echo

[← Complete narrative](../REVIEW.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Verification](VERIFICATION.md)

This page isolates the $m=0$ component of the all-workspace theorem. The
construction uses no ancillary wire. One original suffix data qubit is used as a
temporary predicate carrier and is restored exactly on every input.

Let

```math
N=2^n.
```

The real-frame result is

```math
S_{\mathbb R}(n,0)=\Theta(N),
```

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

The phase-dressed complex magnitude frame has the same asymptotic bounds; the
leaf-phase derivatives use a separate direct measurement stream.

## 1. Addressed Hopf layer

At nonfinal tree depth $d<n-1$, write the system register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R,
```

where:

- $p$ is the $d$-bit Hopf prefix;
- $x$ is the addressed rotation target;
- $b$ is the suffix bit immediately below the target;
- $r$ contains the remaining `n-d-2` suffix bits.

The desired complete layer applies the prefix-selected rotation only when the
original lower suffix `br` is all zero:

```math
L_d
=I+
\sum_p|p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The circuit must equal this operator on the complete Hilbert space. Agreement
only on the forward state-preparation input would be insufficient.

## 2. Echo construction

Define

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Let $T_h$ toggle $b$ iff $h(r)=1$:

```math
T_h:
|b\rangle|r\rangle
\longmapsto
|b\oplus h(r)\rangle|r\rangle.
```

Apply the following sequence from left to right:

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
  <img src="../assets/strict-zero-echo.svg" width="1040" alt="Strict-zero borrowed-suffix echo circuit." />
</p>

The Hopf rotation convention is

```math
R_y(\alpha)=e^{-i\alpha Y}.
```

Hence

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
X C_p X=C_p^{-1}.
```

## 3. Complete four-sector proof

Fix one prefix $p$ and one remaining suffix $r$.

| $h(r)$ | original $b$ | chronological target word | net target action | final $b$ |
|---:|---:|---|---|---:|
| 0 | 0 | none | $I$ | 0 |
| 0 | 1 | $X,C_p,X,C_p$ | $C_pXC_pX=I$ | 1 |
| 1 | 0 | $C_p,C_p$ | $C_p^2=R_y(\theta_{d,p})$ | 0 |
| 1 | 1 | $X,X$ | $I$ | 1 |

The chronological word $X,C_p,X,C_p$ acts on column vectors as
$C_p X C_p X$; this distinction prevents a common order error.

The active sector is $h(r)=1$ and original $b=0$, exactly the condition that the
complete original suffix is zero. Every other sector receives identity. The
borrowed bit is toggled either zero or four times and returns to its original
value. No sector-dependent scalar phase appears.

The prefix and remaining-suffix labels define mutually orthogonal invariant
sectors. The sector calculation therefore proves equality on arbitrary
superpositions and on inputs in which the borrowed bit is entangled with the
rest of the system:

```math
\boxed{
E_d=L_d.
}
```

## 4. No hidden workspace

The predicate operation $T_h$ is a multi-controlled X whose target is the
borrowed logical qubit. Its controls are the bits of $r$, surrounded by X gates
to recognize the all-zero string. Yuan–Zhang Lemma 5 supplies an exact
ancilla-free implementation with linear size and depth.

Each controlled $C_p$ is one UCG. Its participating wires are:

- $d$ prefix controls;
- the borrowed bit as one additional control;
- the Hopf target.

The exact total width is

```math
q=d+2.
```

The remaining suffix bits are idle during the UCG and are not work qubits. Every
wire belongs to the original $n$-qubit logical system.

The published Yuan–Zhang article is arXiv v2. Lemmas 5 and 6 were also checked
in arXiv v3 and retain the exact statements used here.

## 5. Size and depth of one layer

Yuan–Zhang Lemma 6 gives, with no ancillary workspace,

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^d),
```

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^d}{d+2}\right).
```

A nonfinal layer contains two such UCGs, four predicate toggles, and two CNOT
echoes. Thus

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)
=O\left(n+\frac{2^d}{d+2}\right).
```

## 6. Complete real frame

The final depth has no lower suffix and is one ordinary $n$-qubit UCG. Summing
size gives

```math
\begin{aligned}
S(W_{\mathbb R})
&=O\left(
\sum_{d=0}^{n-2}2^d
+\sum_{d=0}^{n-2}(n-d)
+N
\right)\\
&=O(N+n^2)=O(N).
\end{aligned}
```

For the UCG depth terms,

```math
\sum_{d=0}^{n-2}\frac{2^d}{d+2}
=O(N/n).
```

One uniform bound used by the audit is

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq6\frac{2^n}{n}.
```

All predicate and linear-width terms sum to $O(n^2)$, and

```math
n^2=O(N/n).
```

Therefore

```math
S_{\mathbb R}(n,0)=O(N),
```

```math
D_{\mathbb R}(n,0)=O(n+N/n).
```

The real state family has dimension `N-1`. Parameter counting gives
`Omega(N)` size and, on exactly $n$ wires, `Omega(N/n)` depth. These lower
bounds match the construction.

## 7. Endpoint cases

- $n=1$: there is no echo layer; the frame is one one-qubit rotation.
- $d=0$: the half-angle UCG has total width two.
- $d=n-2$: the remaining suffix is empty, so $T_h=X_b$.
- $d=n-1$: there is no borrowed bit; the final layer is the ordinary full-width
  UCG.

The implementation handles each endpoint explicitly.

## 8. Inverse and complex-magnitude corollary

The inverse circuit reverses the gate order and adjoints each gate. It has the
same size, depth, and zero-workspace property.

The phase-dressed complex magnitude frame is

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

The arbitrary leaf-phase diagonal is one exact $n$-qubit UCG, so it also has
$O(N)$ size and $O(n+\frac{N}{n})$ depth with zero ancillary qubits. Sequential
composition therefore gives

```math
S_{\mathbb C,\mathrm{mag}}(n,0)=\Theta(N),
```

```math
D_{\mathbb C,\mathrm{mag}}(n,0)
=\Theta(n+N/n).
```

This unitary contains the phase-dressed magnitude directions. The leaf-phase
derivatives are recovered through the separate direct phase stream and are not
additional columns of the same $N$-dimensional frame.

## 9. Relation to familiar techniques

The circuit combines established ingredients:

- UCGs and multiplexed rotations;
- controlled-unitary square roots;
- Pauli conjugation;
- borrowed or conditionally clean logical qubits;
- toggle-detection cancellation.

The claim is not that these ingredients are new. The Hopf-specific contribution
is the aggregation of every prefix-dependent rotation at depth $d$ into two
total-width-$d+2$ UCGs, using one restored original suffix bit, and the resulting
optimal complete-frame strict-zero bound.

See [Related work](RELATED_WORK.md) for the comparison and
[the strict-zero audit](STRICT_ZERO_ECHO_AUDIT.md) for a separate internal
reconstruction.

## 10. Executable support

- [Circuit and resource implementation](../compiler_robust_hopf/strict_zero_echo.py)
- [Complete sector, layer, frame, inverse, and complex-magnitude tests](../tests/test_strict_zero_echo.py)
- [Exact-rational asymptotic checks](../compiler_robust_hopf/strict_zero_audit.py)
- [Audit tests](../tests/test_strict_zero_audit.py)
- [Human-readable ledger](../scripts/strict_zero_echo_ledger.py)

The tests support the operator proof and resource ledger; they do not replace
the dimension-independent argument.

---

[← Complete narrative](../REVIEW.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Verification](VERIFICATION.md)
