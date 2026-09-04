# The theorem chain in one page

[← Landing page](../README.md) · [Complete narrative](../REVIEW.md) · [Formal proof →](COMPILER_THEOREM.md)

This page compresses the proof to its load-bearing statements.  The complete
operator, register, and resource arguments are in
[`COMPILER_THEOREM.md`](COMPILER_THEOREM.md).

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits.  The exact logical
model uses arbitrary one-qubit gates and CNOTs with all-to-all connectivity.

## 1. A prescribed completion

The real Hopf frame is the unitary satisfying

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
\qquad
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

For unrestricted magnitude angles,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical Hopf domains, `a_j>=0` and equals the principal metric square
root.  At zero metric weight, the raw differential vanishes while the complete
parameter tuple still selects a unit orthogonal marker-frame continuation.

The global gradient circuit applies `W_R^dagger`.  A compiler must therefore
preserve the complete clean-input action,

```math
\widetilde WJ=JW,
```

not only the state column.  Unitarity makes the clean subspace reducing and
gives

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

An exact two-qubit example preserves `W|0^n>` while moving two marker columns
and changing the decoded gradient.

## 2. Addressed Hopf layers

At depth `d`, split a basis label into prefix `p`, target `x`, and lower suffix
`z`, where `|z|=n-d-1`.  The complete layer is

```math
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The full frame is

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_0^{(n)}.
```

The prefix selects the rotation; the complete lower suffix supplies one shared
all-zero predicate.  This structure is the input to every compiler schedule.

## 3. Strict zero workspace

For `d<n-1`, split the suffix into one original bit `b` and the remaining
string `r`.  Put

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Four predicate toggles of `b`, two controlled half-angle UCGs, and two target
CNOT echoes use

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
XC_pX=C_p^{-1}.
```

The original complete-zero-suffix sector receives the desired rotation.  The
other three sectors receive identity, and `b` is restored exactly.  Each
half-angle UCG has total width `d+2`, so

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

Summing over the tree gives

```math
S_{\mathbb R}(n,0)=\Theta(N),
```

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

## 4. Positive workspace

With one clean qubit, each nonfinal layer may compute the zero-suffix predicate
into one reusable flag, apply one prefix-plus-flag UCG, and uncompute the flag.
For

```math
1\leq m<4n,
```

the resulting `O(n^2)` sequential predicate term is absorbed by
`N/(n+m)`, giving the target frontier directly.

For larger workspace, cut the tree after `t` depths and set

```math
B=2^t,
\qquad
s=n-t.
```

The exact factorization is

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right),
```

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A clean binary–one-hot decoder implements the conditioned prefix with
`3B-2-t` work qubits, `O(t)` decoder depth, and `O(B)` size.

An explicit CNOT/Fredkin router moves the original suffix and one activation
token to the prefix-selected branch.  Its exact principal counts are

```math
\text{copy wires}=(B-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(B-1)(s+1).
```

After the copies are uncomputed, their wires are reused as branch-local suffix
flags.  The subtree frames run on disjoint branch registers in parallel, after
which all flags, copies, tokens, and additional data registers return clean.
The prefix and tail both fit within

```math
2B(s+1)
```

clean ancillary qubits.

Choosing the largest feasible cut for `m>=4n` yields

```math
\frac{2^s}{s}
=O\left(\frac{N}{n+m}\right),
```

including the separate `s=1` endpoint.  Hence the routed schedule also has
`O(N)` size and `O(n+N/(n+m))` depth.

## 5. Matching lower bounds

The first frame column covers an open real-state family of dimension `N-1`.
Parameter capacity gives

```math
S_{\mathbb R}(n,m)=\Omega(N),
```

```math
D_{\mathbb R}(n,m)
=\Omega\left(\frac{N}{n+m}\right).
```

The backward light cones of the `n` system outputs give the independent
`Omega(n)` term.  At `m=0`, `Omega(N/n)` already dominates `n`.

Therefore, for every `m>=0`,

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

## 6. Complex magnitude frame

Writing the final system bit as the UCG target,

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}
```

is one exact total-width-`n` UCG.  It reuses the real-frame work pool
sequentially.  Thus

```math
\boxed{
S_{\mathbb C,\mathrm{mag}}(n,m)=\Theta(N),
\qquad
D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The leaf-phase derivatives remain a separate direct record.

## 7. QBP consequence

Frame-safe substitution preserves the complete global inverse-frame measurement
distribution.  The primary finite-shot target is simultaneous absolute accuracy
of the raw Hopf-coordinate gradient.  At fixed accuracy and confidence, the
magnitude stream uses

```math
O(\log n)=O(\log\log M)
```

independent executions for `M=Theta(N)` coordinates.

The scalar and gradient costs are compared as matched general-family programs
with the same forward preparation and controlled observable.  Because the
inverse frame has the same asymptotic depth as optimal state preparation, it
adds only a constant per-execution depth factor.  Classical output
materialization and differently conditioned gradient targets are separate
resources.

## Imported compiler toolkit

The proof uses the optimal QSP theorem, ancilla-free multi-controlled-X lemma,
all-workspace UCG lemma, and coherent-copy lemma from P. Yuan and S. Zhang,
*Quantum* **7**, 956 (2023).  Exact source versions and local consumers are
listed in the [source map](SOURCE_MAP.md).

---

[← Landing page](../README.md) · [Complete narrative](../REVIEW.md) · [Formal proof →](COMPILER_THEOREM.md)
