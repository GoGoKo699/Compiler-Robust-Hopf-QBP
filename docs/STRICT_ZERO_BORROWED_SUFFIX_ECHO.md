# Strict-zero borrowed-suffix echo

## Status

This document records a **theorem candidate** for the strict zero-workspace
endpoint. It is developed on the branch

```text
strict-zero-borrowed-suffix-echo
```

and is not yet part of the active theorem in PR #14.

The exact operator construction, full-frame matrix checks, and integer resource
ledgers are implemented in:

```text
compiler_robust_hopf/strict_zero_echo.py
tests/test_strict_zero_echo.py
scripts/strict_zero_echo_ledger.py
```

Independent proof and prior-art review are tracked in Issue #17.

## 1. Candidate result

Let

```math
N=2^n.
```

In the exact all-to-all standard circuit model of arbitrary one-qubit gates and
CNOTs, the construction below appears to give the complete real Hopf
differential frame at strict zero additional workspace with

```math
S_{\mathbb R}(n,0)=\Theta(N)
```

and

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

The separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

would have the same strict-zero size and depth. Combined with the audited
positive-workspace compiler, this would match the Yuan--Zhang optimal
state-preparation frontier for every integer `m>=0`.

No clean or dirty ancillary qubit is introduced. One existing suffix qubit is
temporarily borrowed and restored exactly on every input.

## 2. One addressed Hopf layer

At nonfinal tree depth `d<n-1`, write the computational register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R,
```

where:

- `p` is the `d`-bit Hopf prefix;
- `x` is the addressed rotation target;
- `b` is the suffix bit immediately below the target;
- `r` contains the remaining
  ```math
  n-d-2
  ```
  suffix bits.

Put

```math
h(r)=[r=0].
```

The addressed layer must apply the prefix-selected rotation

```math
R_y(\theta_p)
```

exactly when

```math
h(r)=1,
\qquad
b=0.
```

That is precisely the condition that the entire original suffix is zero.

Define

```math
C_p=R_y(\theta_p/2)
```

and let `X_T` be Pauli `X` on the target. In the Hopf convention

```math
R_y(\alpha)=
\begin{pmatrix}
\cos\alpha&-\sin\alpha\\
\sin\alpha&\cos\alpha
\end{pmatrix},
```

we have

```math
C_p^2=R_y(\theta_p)
```

and

```math
X_T C_p X_T=C_p^{-1}.
```

## 3. In-place predicate toggle

Let `T_h` be the zero-ancilla reversible operation

```math
T_h:
|b\rangle|r\rangle
\longmapsto
|b\oplus h(r)\rangle|r\rangle.
```

Thus `T_h` toggles the borrowed bit exactly when all remaining suffix bits are
zero.

When `r` is nonempty, `T_h` is a multi-controlled `X` on `b` with zero-valued
controls. The zero controls are obtained by parallel `X` wrappers around an
ordinary multi-controlled `X`. Yuan--Zhang Lemma 5 supplies an exact
ancilla-free linear-size, linear-depth implementation of the controlled `X`
core.

At the endpoint `d=n-2`, `r` is empty and `h=1` identically, so

```math
T_h=X_B.
```

## 4. Four-toggle echo

Let `Lambda_B(X_T)` denote the CNOT from the borrowed bit to the target, and let
`Lambda_B(C_p)` denote the UCG that applies the prefix-selected half rotation
`C_p` when `b=1`.

Use the following **chronological** sequence:

```text
Lambda_B(X_T)
T_h
Lambda_B(C_p)
T_h
Lambda_B(X_T)
T_h
Lambda_B(C_p)
T_h
```

The target word in each sector is:

| `h(r)` | original `b` | chronological target gates | net operator |
|---:|---:|---|---|
| 0 | 0 | none | `I` |
| 0 | 1 | `X, C_p, X, C_p` | `C_p X C_p X=I` |
| 1 | 0 | `C_p, C_p` | `C_p^2=R_y(theta_p)` |
| 1 | 1 | `X, X` | `I` |

The matrix product in the second row is written in reverse chronological order,
as usual for operators acting on column vectors.

The borrowed bit is restored:

- when `h=0`, it is never toggled;
- when `h=1`, it is toggled four times.

Therefore, in every prefix and remaining-suffix sector, the echo applies
`R_y(theta_p)` exactly when the original full suffix is zero and otherwise
applies the identity. It follows that

```math
\boxed{E_d=L_d}
```

as complete operators on the entire `n`-qubit Hilbert space.

This is stronger than equality on the state-preparation input. It remains valid
for arbitrary superpositions and entanglement among the prefix, target,
borrowed bit, and remaining suffix.

## 5. UCG width

The half-angle operation `Lambda_B(C_p)` has:

- `d` prefix controls;
- the borrowed bit as one additional control;
- the Hopf target.

It is therefore a UCG on

```math
q=d+2
```

qubits. Its block table contains identity blocks for `b=0` and
`R_y(theta_p/2)` blocks for `b=1`.

Yuan--Zhang Lemma 6 gives, with no ancillary qubits,

```math
S_{\mathrm{UCG}}(q,0)=O(2^q)
```

and

```math
D_{\mathrm{UCG}}(q,0)
=O\left(q+\frac{2^q}{q}\right).
```

Each nonfinal Hopf layer uses two such half-angle UCGs, four predicate toggles,
and two CNOT echoes. With

```math
s=n-d-1,
```

the resulting layer bounds are

```math
S(L_d)=O(2^d+s)
```

and

```math
D(L_d)
=O\left(n+\frac{2^d}{d+1}\right).
```

No ancillary wire is present in this count.

## 6. Complete real-frame upper bound

The final Hopf depth has no lower suffix and is compiled as one ordinary
`n`-qubit UCG.

Summing size over the nonfinal depths gives

```math
\begin{aligned}
S(W_{\mathbb R})
&=O\left(
\sum_{d=0}^{n-2}2^d
+\sum_{d=0}^{n-2}(n-d-1)
+N
\right)\\
&=O(N+n^2)\\
&=O(N).
\end{aligned}
```

For depth,

```math
D(W_{\mathbb R})
=O\left(
n^2+
\sum_{d=0}^{n-2}\frac{2^d}{d+1}
+n+\frac{N}{n}
\right).
```

Split the dyadic sum at `d=floor(n/2)`:

- the early part is `O(2**(n/2))`;
- every denominator in the late part is `Omega(n)`, so the late part is
  `O(N/n)`.

Also `n**3=O(2**n)`, hence

```math
n^2=O(N/n).
```

Therefore

```math
\boxed{
S(W_{\mathbb R})=O(N),
\qquad
D(W_{\mathbb R})=O\left(n+\frac{N}{n}\right).
}
```

Taking the adjoint of the exact circuit implements `W_R^dagger` with identical
resources.

## 7. Lower bound

Applying the frame to `|0^n>` prepares an arbitrary real normalized `n`-qubit
state. The family has `N-1` real degrees of freedom. The parameter-count and
backward-light-cone arguments already used by the unified compiler therefore
give

```math
S(W_{\mathbb R})=\Omega(N)
```

and

```math
D(W_{\mathbb R})
=\Omega\left(n+\frac{N}{n}\right).
```

If the upper-bound audit survives, the strict-zero real-frame result is

```math
\boxed{
S_{\mathbb R}(n,0)=\Theta(N),
\qquad
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
}
```

## 8. Separated complex frame

The phase diagonal is already one exact `n`-qubit UCG:

```math
D_{\mathrm{ph}}
=\sum_z |z\rangle\!\langle z|
\otimes
\operatorname{diag}
\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

At zero workspace it has `O(N)` size and `O(n+N/n)` depth by Yuan--Zhang
Lemma 6. Sequential composition with the strict-zero real frame therefore gives
the same candidate bounds for

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

## 9. Why direct sparse Möttönen pruning is insufficient

For one addressed depth, the logical angle table is

```math
\alpha(p,z)=\theta_p\,\delta_{z,0}.
```

The standard Möttönen/Gray-code physical angles are obtained from a signed
Walsh transform. For prefix frequency `u` and suffix frequency `v`,

```math
\widehat\alpha(u,v)
\propto
\sum_{p,z}
(-1)^{u\cdot p+v\cdot z}
\theta_p\delta_{z,0}
=
\sum_p(-1)^{u\cdot p}\theta_p.
```

The result is independent of `v`. For generic Hopf angles, each nonzero prefix
coefficient is replicated across every suffix frequency. Thus a sparse logical
block table becomes generically dense in the standard full-width Möttönen
parameterization.

The echo avoids that dense transform. It uses a smaller
prefix-plus-borrowed-bit UCG and handles the remaining suffix condition through
in-place toggles.

## 10. Executable evidence

The deterministic suite checks:

- the two one-qubit echo identities;
- all four `(h,b)` sectors;
- exact restoration of the borrowed bit;
- self-inverse predicate and target-echo permutations;
- every nonfinal depth through `n=8`;
- complete real frames through `n=8`;
- inverse-frame equality;
- separated complex frames through `n=7`;
- strict zero-workspace resource ledgers through `n=256`;
- the zero-control endpoint `d=n-2`.

The matrix tests compare independently constructed complete operators. They do
not merely test the initialized state column.

Run:

```bash
python validate.py
python scripts/strict_zero_echo_ledger.py --n 12 --layers
```

## 11. Evidence and novelty boundary

This branch should not yet replace the `m>=1` theorem in PR #14.

The following remain required:

1. an independent line-by-line proof audit;
2. verification of every imported Yuan--Zhang hypothesis and width convention;
3. a prior-art review covering dirty or borrowed controls, toggle detection,
   sparse UCGs, and multi-controlled rotations;
4. final integration into the unified resource theorem only after those gates
   pass.

The repository makes no novelty claim for the abstract echo before that review.

## Primary compiler source

P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
improved unitary synthesis by quantum circuits with any number of ancillary
qubits,” *Quantum* **7**, 956 (2023),
[PDF](https://quantum-journal.org/papers/q-2023-03-20-956/pdf/).

The historical Möttönen-style compilation remains relevant as the source of the
multiplexor viewpoint, but the active asymptotic primitive is Yuan--Zhang
Lemma 6.
