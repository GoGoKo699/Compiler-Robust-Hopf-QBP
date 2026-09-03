# Optimal Compilation of Hopf Differential Frames

### A linear technical narrative from state preparation to compiler-robust quantum backpropagation

[Landing page](README.md) · [Minimal Hopf interface](docs/HOPF_INTERFACE.md) · [Complete compiler proof](docs/COMPILER_THEOREM.md) · [Verification](docs/VERIFICATION.md)

## Orientation

Yuan and Zhang determine the optimal exact circuit size and depth for preparing
one arbitrary `n`-qubit state with any number `m` of clean ancillary qubits. If
`N=2^n`, their frontier is

```math
S_{\mathrm{QSP}}(n,m)=\Theta(N),
```

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

This repository asks a stronger synthesis question.

The Hopf construction is a binary-tree coordinate chart for arbitrary real and
complex pure states. Besides preparing the state, the chart supplies normalized
coordinate tangents. These directions can be placed in designated columns of a
unitary `W`, the **Hopf differential frame**:

```math
W|0^n\rangle=|\psi\rangle,
\qquad
W|\lambda(j)\rangle=|e_j\rangle.
```

The global Hopf quantum-backpropagation protocol applies `W^dagger` to a common
objective response. It therefore depends on the complete frame action, not only
on the prepared state column.

The main result under technical review is that this stronger object reaches the
same size–depth frontier as arbitrary state preparation:

```math
\boxed{
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(N),
}
```

```math
\boxed{
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right),
\qquad m\geq0.
}
```

The result is exact in the all-to-all logical model with arbitrary one-qubit
gates and CNOTs. It has passed internal analytic and executable checks and is
presented here for independent technical review.

This narrative is designed so that the compiler theorem can be checked before
the reader learns the complete QBP protocol. The argument has five conceptual
steps:

1. identify the complete frame operator and show why one state column is
   insufficient;
2. exploit the addressed zero-suffix structure of each Hopf depth;
3. close strict zero workspace by borrowing and exactly restoring one logical
   suffix qubit;
4. trade positive workspace for coherent branch parallelism below a tree cut;
5. transfer the optimal frame compiler to the complex chart and the global QBP
   record.

<p align="center">
  <img src="assets/literature-lineage.svg" width="980" alt="The state-preparation compiler line and the Hopf geometry line meet in the optimal complete-frame compiler." />
</p>

---

## 1. The synthesis problem in familiar terms

### 1.1 State preparation fixes one column

Ordinary exact state preparation asks for a unitary `U_prep` satisfying

```math
U_{\mathrm{prep}}|0^n\rangle=|\psi\rangle.
```

Its action on the orthogonal complement of `|0^n>` is free. That freedom is
useful: the compiler may choose any convenient unitary completion while
optimizing size, depth, or workspace.

The complete Hopf frame removes much of that freedom. Its first column is the
state, but selected nonzero computational columns are normalized coordinate
tangents. These columns are operational because the reverse gradient circuit
applies the inverse frame and reads their computational markers.

<p align="center">
  <img src="assets/state-vs-frame.svg" width="920" alt="State preparation fixes one column, whereas Hopf differential-frame compilation fixes the state and designated tangent columns." />
</p>

### 1.2 Frame-safe compilation

Let `J` append `m` clean workspace qubits:

```math
J|\varphi\rangle
=|\varphi\rangle|0^m\rangle.
```

A compiled circuit `W_tilde` is **frame-safe** when

```math
\boxed{
\widetilde WJ=JW
}
```

for every system input. It must also be unitary on the complete system–workspace
space.

This identity immediately gives the inverse contract. Since `W_tilde` maps the
clean-workspace subspace onto itself, that subspace is invariant under both
`W_tilde` and `W_tilde^dagger`. Hence

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

The global gradient circuit may therefore replace `W` and `W^dagger` by a
frame-safe implementation without changing either coherent branch or the final
measurement distribution.

### 1.3 Why this is not generic unitary synthesis

A generic `n`-qubit unitary has `Theta(4^n)` continuous parameters. The Hopf
frame is a highly structured `N`-by-`N` unitary determined by only `N-1`
magnitude angles, plus `N` leaf phases in the separated complex case. Its
special tree structure is what makes state-preparation-order synthesis
possible.

A generic controlled-state-preparation treatment of all `N` frame columns would
use an `n`-qubit column index and an `n`-qubit target. The resulting scale is
`O(2^(n+n))=O(N^2)`, and the coherent column index remains present. The present
compiler avoids this all-column construction entirely.

> **What should be checked here?**  Confirm that frame safety is an equality on
> all clean-workspace system inputs, not only on `|0^n>`. Check that inverse
> correctness follows from a reducing subspace rather than from simply taking
> the adjoint of a first-column equality.

### Executable counterpart

- [Frame-safe compiler contracts](docs/FRAME_SAFE_COMPILATION.md)
- [Exact counterexamples to weaker contracts](docs/COMPILER_BOUNDARIES.md)
- [Boundary implementation](compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](tests/test_compiler_boundaries.py)

---

## 2. Minimal Hopf interface

### 2.1 Binary-tree coordinates

Fix `n` qubits and `N=2^n`. The real Hopf chart assigns one angle to each
internal node of a complete binary tree. The root angle splits amplitude
between the left and right halves of the computational basis. Each child angle
splits the amplitude arriving in that subtree, and the recursion continues to
sibling leaves.

For internal node `j` at depth `d` and position `r`,

```math
j=2^d+r,
\qquad
0\leq r<2^d.
```

Its computational marker is

```math
\lambda(j)=(2r+1)2^{n-d-1}.
```

The bit string for `lambda(j)` is the node prefix, followed by one at the node's
target location and zeros below it.

### 2.2 Differential directions

Differentiating one tree split replaces its local subtree state by the
orthogonal complement. The derivative of coordinate `theta_j` therefore has
the form

```math
\partial_{\theta_j}|\psi\rangle
=\sqrt{g_{j,j}}\,|e_j\rangle,
```

where `g_(j,j)` is the probability mass entering the node and `|e_j>` is a
normalized direction. The state and all `N-1` normalized magnitude directions
form an orthonormal basis.

The real differential frame is defined by

```math
W_{\mathbb R}|0^n\rangle=|\psi_{\mathbb R}\rangle,
```

```math
W_{\mathbb R}|\lambda(j)\rangle=|e_j^{\mathbb R}\rangle.
```

For the complex chart, leaf phases form a diagonal unitary

```math
D_{\mathrm{ph}}
=\sum_{\ell=0}^{N-1}
e^{i\phi_\ell}|\ell\rangle\!\langle\ell|,
```

and the separated complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

### 2.3 Complete addressed layers

At tree depth `d`, split a basis label as

```math
|p\rangle_P|x\rangle_T|z\rangle_Z,
```

where `p` is the `d`-bit prefix, `x` is the target, and the lower suffix `z` has
length

```math
s=n-d-1.
```

The complete depth operator is

```math
\boxed{
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^s\rangle\!\langle0^s|.
}
```

The convention is

```math
R_y(\alpha)=e^{-i\alpha Y}
=
\begin{pmatrix}
\cos\alpha&-\sin\alpha\\
\sin\alpha&\cos\alpha
\end{pmatrix}.
```

The complete frame is

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_1^{(n)}L_0^{(n)},
```

with `L_0` acting first on state vectors.

The all-zero suffix condition is the central compiler feature. It ensures that
each addressed rotation acts only on its state-and-complement pair and leaves
all other established columns unchanged.

> **What should be checked here?**  Verify the breadth-first node and marker
> conventions, the state-update order, and the identity action on every
> nonzero-suffix sector. These conventions are shared by the proof and code.

### Executable counterpart

- [Minimal Hopf interface with notation table](docs/HOPF_INTERFACE.md)
- [Marker conventions](compiler_robust_hopf/conventions.py)
- [State, tangent, and frame construction](compiler_robust_hopf/frames.py)
- [Frame tests](tests/test_frames.py)

---

## 3. Two qubits: the complete obstruction in one example

For two qubits, the state is

```math
|\psi\rangle
=
\cos\theta_1
\bigl(\cos\theta_2|00\rangle+
      \sin\theta_2|01\rangle\bigr)
+
\sin\theta_1
\bigl(\cos\theta_3|10\rangle+
      \sin\theta_3|11\rangle\bigr).
```

At

```math
\theta_1=\theta_2=\theta_3=\frac{\pi}{4},
```

we have

```math
|\psi\rangle
=\frac{|00\rangle+|01\rangle+|10\rangle+|11\rangle}{2}.
```

The marker assignment is

```math
\lambda(1)=10_2,
\qquad
\lambda(2)=01_2,
\qquad
\lambda(3)=11_2.
```

In computational column order, the canonical frame is

```math
W_{\mathbb R}
=
\begin{pmatrix}
\frac12&-\frac1{\sqrt2}&-\frac12&0\\[3pt]
\frac12& \frac1{\sqrt2}&-\frac12&0\\[3pt]
\frac12&0&\frac12&-\frac1{\sqrt2}\\[3pt]
\frac12&0&\frac12& \frac1{\sqrt2}
\end{pmatrix}
=
\begin{pmatrix}
|&|&|&|\\
\psi&e_2&e_1&e_3\\
|&|&|&|
\end{pmatrix}.
```

Let `Q` swap `|01>` and `|10>` while fixing `|00>` and `|11>`, and set

```math
V=W_{\mathbb R}Q.
```

Then

```math
V|00\rangle=W_{\mathbb R}|00\rangle=|\psi\rangle,
```

so `V` prepares exactly the same state. It nevertheless exchanges the marker
columns for `e_1` and `e_2`.

Choose

```math
O=-Z\otimes I.
```

Direct calculation gives

```math
W_{\mathbb R}^{\dagger}O|\psi\rangle=|10\rangle,
```

but

```math
V^{\dagger}O|\psi\rangle=|01\rangle.
```

The fixed Hopf marker decoder consequently changes the gradient from

```math
(2,0,0)
```

to

```math
(0,\sqrt2,0).
```

<p align="center">
  <img src="assets/two-qubit-obstruction.svg" width="920" alt="Two state-equivalent two-qubit unitaries place the response on different tangent markers." />
</p>

This example establishes the exact boundary:

```math
\boxed{
V|0^n\rangle=W|0^n\rangle
\not\Rightarrow
\text{valid inverse-frame gradient decoding}.
}
```

It does not say that state-preparation compilers are unsuitable in general. It
says that a compiler used inside this reverse protocol must preserve the
columns that the protocol resolves.

> **What should be checked here?**  Confirm first-column equality, the explicit
> swap of marker columns, the observable convention, and the unchanged decoder.
> The example should be reproducible without trusting any asymptotic argument.

### Executable counterpart

- [Counterexample code](compiler_robust_hopf/compiler_boundaries.py)
- [Exact distributions and gradients](tests/test_compiler_boundaries.py)

---

## 4. Circuit framework and literature position

The sole active external compiler framework is Yuan and Zhang, *Quantum* **7**,
956 (2023). The proof imports four statements.

| Result | Use in this repository |
|---|---|
| Theorem 2 | optimal arbitrary-state-preparation frontier for every `m` |
| Lemma 5 | exact ancilla-free multi-controlled X with linear size and depth |
| Lemma 6 | exact total-width-`q` UCG with `O(2^q)` size and `O(q+2^q/(q+w))` depth using `w` clean qubits |
| Lemma 9 | coherent CNOT-tree copy–use–uncopy |

The earlier Sun–Tian–Yang–Yuan–Zhang paper is the historical predecessor. The
Möttönen–Bergholm work supplies the multiplexor/UCG language. These references
are credited without turning the proof into a choice between published
compiler families.

The relationship is best summarized as follows:

> The state-preparation results can be adapted once the complete-operator
> structure of the Hopf frame is exposed. The adaptation is not direct because
> the frame preserves a state and designated tangent columns, whereas ordinary
> state preparation fixes only one initialized column.

The strict-zero circuit also uses familiar ideas from controlled-unitary square
roots and borrowed or conditionally clean workspace. The claim made here is
narrow: the Hopf addressed layer is reduced to two smaller UCGs and linear
predicate toggles, which closes the complete-frame `m=0` frontier. Borrowed
qubits, toggle detection, square-root decompositions, and UCGs themselves are
not claimed as new.

> **What should be checked here?**  Match every imported theorem to the circuit
> model stated above. The present upper bound is conditional on exact versions
> of these primitives and does not imply hardware-native or approximate-gate
> depth.

### Exact dependency map

- [Fact-level source map](docs/SOURCE_MAP.md)
- [Related work and contribution boundary](docs/RELATED_WORK.md)

---

## 5. Main theorem and schedule map

For every integer `m>=0`, the compiler chooses one of three internal schedules.

| Workspace | Schedule | Core operation |
|---:|---|---|
| `m=0` | borrowed-suffix half-angle echo | recognize the zero-suffix sector without an ancillary wire |
| `1<=m<4n` | direct flagged UCG | compute one reusable suffix predicate flag |
| `m>=4n` | routed parallel subframes | exchange workspace for branch parallelism below a tree cut |

The proof of optimality consists of an upper bound for each row and a common
lower bound.

The upper-bound target is

```math
S(n,m)=O(N),
```

```math
D(n,m)=O\left(n+\frac{N}{n+m}\right).
```

The lower-bound target is the same order. The three schedules are not required
to have the same finite constants; they are selected for a uniform asymptotic
theorem.

---

## 6. Strict zero workspace: borrowed-suffix echo

### 6.1 Why a direct sparse multiplexor is not enough

At depth `d`, the logical rotation table is

```math
\alpha(p,z)=\theta_{d,p}\,[z=0].
```

Only `2^d` of its `2^(n-1)` blocks are nontrivial. It is tempting to place zero
angles in all inactive blocks and apply an ancilla-free full-width Möttönen
multiplexor. The standard angle transformation is a signed Walsh transform. For
prefix frequency `u` and suffix frequency `v`,

```math
\widehat\alpha(u,v)
\propto
\sum_{p,z}(-1)^{u\cdot p+v\cdot z}
\theta_{d,p}[z=0]
=
\sum_p(-1)^{u\cdot p}\theta_{d,p}.
```

The result is independent of `v`. For generic prefix angles, the same nonzero
coefficient is repeated across all suffix frequencies. Logical sparsity therefore
does not become sparse physical Möttönen angles.

The strict-zero schedule avoids this dense transform by isolating one suffix
bit and using it as a restored predicate carrier.

### 6.2 Exact echo

Assume `d<n-1`. Write the suffix as one borrowed bit `b` and remaining string
`r`, and define

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Let `T_h` toggle `b` exactly when `h(r)=1`. Apply, from left to right,

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
  <img src="assets/strict-zero-echo.svg" width="1040" alt="Strict-zero borrowed-suffix echo." />
</p>

The rotation convention gives

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
X C_p X=C_p^{-1}.
```

Fixing `p` and `r`, the complete sector table is:

| `h(r)` | original `b` | target word in chronological order | matrix acting on the target | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_p X C_p X=I` | 1 |
| 1 | 0 | `C_p,C_p` | `C_p^2=R_y(theta_(d,p))` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

The desired addressed rotation occurs exactly when the original complete suffix
is zero. Every other sector receives identity. The borrowed logical qubit is
restored and no relative phase is introduced.

Because the sectors are orthogonal and invariant, this basis calculation proves
the complete operator identity on arbitrary superpositions, including inputs in
which `b` is entangled with the prefix, target, or remaining suffix.

### 6.3 No hidden ancillary wire

The predicate toggle `T_h` is a multi-controlled X whose target is the borrowed
system qubit. Its controls are the remaining suffix bits, inverted as needed to
recognize the all-zero string. Yuan–Zhang Lemma 5 implements it without
ancillary qubits.

Each half-angle operation is one UCG with:

- `d` prefix controls;
- the borrowed bit as one control;
- the Hopf target.

Its total width is

```math
q=d+2.
```

The remaining suffix bits are idle during that UCG. They are neither part of
its width nor hidden workspace.

### 6.4 Resource sum

Lemma 6 gives

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^d),
```

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^d}{d+2}\right).
```

Four predicate toggles contribute `O(n-d)` size and depth, and the target echoes
are two CNOTs. Therefore

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)
=O\left(n+\frac{2^d}{d+2}\right).
```

The final depth has no suffix and is one ordinary `n`-qubit UCG. Summing size:

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

For depth,

```math
\sum_{d=0}^{n-2}\frac{2^d}{d+2}
=O(N/n).
```

To see this, split the sum at `n/2`. The early terms total `O(2^(n/2))`. In the
late half, every denominator is `Omega(n)` while the numerators form a geometric
sum of order `N`. The remaining linear-width and predicate terms total
`O(n^2)`, and `n^2=O(N/n)`. Hence

```math
\boxed{
S_{\mathbb R}(n,0)=O(N),
\qquad
D_{\mathbb R}(n,0)=O(n+N/n).
}
```

The `n=1` endpoint is one one-qubit rotation. At `d=n-2`, the remaining suffix
is empty and `T_h=X_b`; the same sector proof applies.

> **What should be checked here?**  This is the most delicate schedule. Check
> the original value of the borrowed bit, the chronological product order, the
> absence of branch phases, the exact UCG width `d+2`, and the no-ancilla
> convention of the imported multi-controlled-X synthesis.

### Executable counterpart

- [Strict-zero construction](compiler_robust_hopf/strict_zero_echo.py)
- [Complete operator tests](tests/test_strict_zero_echo.py)
- [Exact-rational resource checks](compiler_robust_hopf/strict_zero_audit.py)
- [Strict-zero ledger](scripts/strict_zero_echo_ledger.py)

---

## 7. Small positive workspace: direct flagged UCGs

When one clean qubit is available, the common zero-suffix predicate can be
stored directly.

At every nonfinal depth:

1. compute `[z=0]` into one clean flag;
2. apply one UCG selected by the `d` prefix bits and the flag;
3. uncompute the flag.

The flag is reused at the next depth. At nonfinal depths the UCG receives the
remaining `m-1` clean work qubits; at the final depth, where no suffix predicate
is needed, it may use all `m`.

The predicate calculations sum to `O(n^2)` size and depth. The UCG sizes form a
geometric series and total `O(N)`. Lemma 6 and a uniform geometric-tail bound
give

```math
D_{\mathrm{direct}}(n,m)
=O\left(n^2+\frac{N}{n+m}\right).
```

For

```math
1\leq m<4n,
```

we have `n+m<5n`. Since `n^3=O(2^n)`,

```math
n^2
=O\left(\frac{N}{n+m}\right).
```

Thus the direct schedule is already optimal-order throughout this workspace
range:

```math
S_{\mathrm{direct}}(n,m)=O(N),
```

```math
D_{\mathrm{direct}}(n,m)
=O\left(n+\frac{N}{n+m}\right).
```

> **What should be checked here?**  Count the predicate flag inside the
> requested budget and give only `m-1` additional work qubits to the UCG. Verify
> exact uncomputation before the next depth.

### Executable counterpart

- [Direct schedule ledger](compiler_robust_hopf/unified_compiler.py)
- [Low-workspace inequality](compiler_robust_hopf/resource_bounds.py)
- [Endpoint tests](tests/test_unified_compiler.py)

---

## 8. Larger workspace: cut, route, and parallelize

### 8.1 Two complete-operator identities

Cut the Hopf tree after `t` depths and set

```math
B=2^t,
\qquad
s=n-t.
```

Write

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

where `F_t` contains the first `t` depths and `R_t` the remainder.

The prefix obeys

```math
\boxed{
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right).
}
```

Every layer above the cut contains all `s` external suffix qubits in its zero-
suffix predicate. On `|0^s>` those layers form exactly the `t`-qubit Hopf frame;
on the orthogonal complement they are all identity. This proves the prefix
identity.

For each `t`-bit prefix `r`, let `W_s^(r)` be the complete Hopf frame of the
subtree below that prefix. A local subtree node `(ell,u)` receives the global
angle at breadth-first index

```math
2^{t+\ell}+r2^\ell+u.
```

Every layer below the cut preserves the prefix, so each fixed-prefix subspace is
invariant. Within it, the suffix layers are exactly `W_s^(r)`. Hence

```math
\boxed{
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
}
```

<p align="center">
  <img src="assets/tree-cut-routing.svg" width="1040" alt="A tree cut exposes a conditioned prefix and a direct sum of subtree frames that can be routed and run in parallel." />
</p>

### 8.2 Conditioned prefix via a clean one-hot decoder

The prefix frame must run only when the external suffix equals zero. Convert the
`t`-bit prefix to a one-hot register with an explicit reversible decoder `D_t`:

```math
D_t|x\rangle|0\cdots0\rangle
=|0^t\rangle|e_x\rangle|0\cdots0\rangle.
```

For `B=2^t`, the workspace is:

| Register | Qubits |
|---|---:|
| one-hot leaves | `B` |
| internal indicators | `B-1` |
| shared fanout/parity pool | `B-1-t` |
| **total** | `3B-2-t` |

The decoder first propagates one active tree indicator according to the binary
address, then reconstructs each address bit as the parity of the active
right-child indicators and clears the original binary register. The supplied
X/CNOT/Toffoli schedule has disjoint support within every layer, depth
`11t-4=O(t)`, and size `O(B)`. Reversing it gives the exact inverse.

On the one-hot code, all Givens pairs at one Hopf depth are disjoint. Compute the
external suffix-zero predicate, fan it out to the simultaneous Givens controls,
apply the `t` encoded Hopf layers, and uncompute. Internal decoder registers are
clean after encoding and are reused for the live predicate copies.

The conditioned prefix therefore has

```math
S(F_t)=O(B+s),
\qquad
D(F_t)=O(n).
```

### 8.3 Coherent router

Allocate `B` possible suffix-data locations, one-hot activation tokens, and the
control copies needed by a binary-tree controlled-SWAP network. The router
implements

```math
\sum_r c_r|r\rangle_P|\xi_r\rangle_X|0\rangle_{\mathrm{work}}
\longmapsto
\sum_r c_r|r\rangle_P
|\xi_r\rangle_{X_r}|1\rangle_{z_r}|0\rangle_{\mathrm{rest}}.
```

The transformation is coherent; it is valid when the prefix and suffix are
entangled. After the branch operations, inverse routing returns the transformed
suffix to the original system wires and clears every work register.

The routed-tail registers are:

| Register | Clean qubits |
|---|---:|
| additional branch data | `(B-1)s` |
| activation tokens | `B` |
| copied routing controls | `(B-1)(s+1)-t` |
| simultaneous branch flags, when needed | `B` |

Routing copies are uncomputed before the branch frames and their wires are
reused as flags. The complete prefix and tail fit in the common envelope

```math
\boxed{
2B(s+1)
}
```

clean qubits. Prefix and tail are sequential, so their peaks take a maximum,
not a sum.

### 8.4 Parallel subtree frames

Each activation token controls one `s`-qubit subtree frame. A direct controlled
subframe has

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

The `B` branches act on disjoint registers and therefore run in parallel. Their
combined size is

```math
B\,O(2^s)=O(N),
```

while their depth is not multiplied by `B`. Route and unroute have `O(n)` depth
and `O(B(s+1))` size. Since `s+1<=2^s`, routing size is also `O(N)`.

### 8.5 Choosing the cut

For `m>=4n`, choose the largest `t` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If `s=n-t>1`, failure of the next cut gives

```math
m<4\,2^t s.
```

Therefore

```math
\frac{2^s}{s}
=\frac{N}{2^t s}
<4\frac{N}{m}
=O\left(\frac{N}{n+m}\right),
```

because `m>=4n` makes `n+m=Theta(m)`.

Also,

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

For bounded `s`, the term is `O(n)`; for sufficiently large `s`,
`2^s>=s^3` gives `s^2<=2^s/s`.

The routed schedule consequently satisfies

```math
S_{\mathrm{routed}}(n,m)=O(N),
```

```math
D_{\mathrm{routed}}(n,m)
=O\left(n+\frac{N}{n+m}\right).
```

> **What should be checked here?**  Verify the prefix and direct-sum identities
> before auditing resources. Then check the binary-address clearing, router
> action on entangled inputs, simultaneous register peak, branch disjointness,
> and maximal-cut inequality.

### Executable counterpart

- [Tree identities](compiler_robust_hopf/tree_structure.py)
- [Binary–one-hot decoder](compiler_robust_hopf/tree_decoder.py)
- [Router and unified resource selection](compiler_robust_hopf/unified_compiler.py)
- [Resource inequalities](compiler_robust_hopf/resource_bounds.py)
- [Decoder tests](tests/test_tree_decoder.py)
- [All-workspace compiler tests](tests/test_unified_compiler.py)

---

## 9. Matching lower bounds

Every valid frame compiler is also a real-state-preparation circuit when applied
to `|0^n>|0^m>`, because its first column ranges over the complete real unit
sphere.

### 9.1 Size

The real sphere has dimension `N-1`. A circuit with `G` arbitrary one-qubit
gates has only `O(G)` continuous real parameters. A countable collection of
lower-dimensional circuit families cannot cover an open subset of an
`(N-1)`-dimensional manifold. Hence

```math
S_{\mathbb R}(n,m)=\Omega(N).
```

### 9.2 Workspace-dependent depth

A depth-`D` circuit on `n+m` wires has `O(D(n+m))` parameterized one-qubit gate
locations. Parameter counting gives

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

### 9.3 Linear depth

For positive workspace, each of the `n` system outputs has a backward light cone
of at most `2^D` wires. Their union contains at most `O(n2^D)` relevant wires
and `O(Dn2^D)` continuously parameterized locations. Covering the real-state
family requires

```math
Dn2^D=\Omega(2^n),
```

which implies

```math
D=\Omega(n).
```

At `m=0`, the preceding parameter bound already gives `Omega(N/n)`, which
asymptotically dominates `n`.

Thus

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`.

Combining with the three upper-bound schedules yields

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

> **What should be checked here?**  The lower bound uses only the first frame
> column, so it applies to every complete-frame compiler. Check the dimension of
> the real family, parameter count per gate location, and the system-output
> light-cone argument.

### Executable counterpart

- [Integer lower-bound diagnostics](compiler_robust_hopf/resource_bounds.py)
- [Lower-bound tests](tests/test_resource_bounds.py)

---

## 10. Separated complex frame

The complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

Choose the final system qubit as a UCG target and write a basis label as `x=zb`.
Then

```math
D_{\mathrm{ph}}
=
\sum_z|z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
```

This is one exact total-width-`n` UCG. Lemma 6 gives

```math
S_{\mathrm{diag}}(n,m)=O(N),
```

```math
D_{\mathrm{diag}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`.

Both the real frame and phase UCG return their workspace clean. They execute
sequentially and reuse one pool, so workspace takes a maximum rather than a sum.
At `m=0`, both blocks are ancilla-free. The real subfamily supplies the matching
lower bounds.

Therefore

```math
\boxed{
S_{\mathbb C}(n,m)=\Theta(N),
\qquad
D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

> **What should be checked here?**  Verify that arbitrary `U(2)` UCG blocks
> reproduce the complete diagonal, including common phase, and that workspace
> is clean between the real and diagonal blocks.

### Executable counterpart

- [One-UCG phase layer](compiler_robust_hopf/unified_compiler.py)
- [Complex frame and gauge identities](compiler_robust_hopf/complex_analysis.py)
- [Complex composition tests](tests/test_unified_compiler.py)

---

## 11. Quantum-backpropagation consequence

### 11.1 Pulling the objective response into the frame

For

```math
E_O(\boldsymbol\theta)
=\langle\psi|O|\psi\rangle,
```

we have

```math
\partial_{\theta_j}E_O
=
2\sqrt{g_{j,j}}
\operatorname{Re}
\langle\lambda(j)|W^{\dagger}O|\psi\rangle.
```

A phase-calibrated controlled Hermitian-unitary observable creates coherent
reference and response branches. Applying `W^dagger` maps the reference branch
to `|0^n>` and resolves the response branch in the computational frame.

For an all-X outcome `(b,y)`, define

```math
Z_j
=2\sqrt{g_{j,j}}
(-1)^{b+\lambda(j)\cdot y}.
```

Then

```math
\mathbb E[Z_j]=\partial_{\theta_j}E_O.
```

The same `(b,y)` contributes to every `j`. A signed histogram and one fast
Walsh–Hadamard transform evaluate all marker parities together.

### 11.2 Frame-safe substitution preserves the distribution

If

```math
\widetilde WJ=JW,
```

then

```math
\widetilde W^{\dagger}J=JW^{\dagger}.
```

The compiled circuit therefore reproduces the same reference and response
branches on the clean-workspace subspace. The complete measurement distribution,
decoded means, record norms, and concentration premises are unchanged.

### 11.3 Execution and depth scaling

Every complete magnitude-depth record has Euclidean norm two. A fixed-norm
concentration bound gives a sufficient global magnitude count

```math
S_{\mathrm{mag}}
=O\left(
\frac{1+\log(n/\delta)}{\epsilon^2}
\right)
```

for simultaneous coordinatewise accuracy `epsilon` and confidence `1-delta`.
At fixed `epsilon` and `delta`,

```math
S_{\mathrm{mag}}=O(\log n)=O(\log\log M),
```

where `M=Theta(N)` is the number of Hopf coordinates.

The matched scalar program contains the same forward preparation and controlled
observable but omits the reverse frame. Because the compiled frame has the same
asymptotic depth as optimal state preparation for every `m`, adding the reverse
block changes per-execution depth only by a constant asymptotic factor. Under
the declared controlled-observable model,

```math
\boxed{
\frac{\mathrm{TIME}(\nabla E_O)}
     {\mathrm{TIME}(E_O)}
=O(\log n)=O(\log\log M).
}
```

This is an execution-and-logical-depth statement. It does not make the
materialized `M`-entry classical output sublinear, and it does not hide the cost
of implementing the controlled observable.

The complex phase block uses a separate signed one-hot record and no inverse
frame. Checkpoint methods use an active-interface contract rather than the full
global frame and must be analyzed separately.

> **What should be checked here?**  Keep independent executions,
> per-execution depth, classical output size, and controlled-observable cost
> separate. Verify that the fixed decoder sees exactly the same frame columns
> after compilation.

### Executable counterpart

- [Complete QBP consequence](docs/QBP_CONSEQUENCE.md)
- [Magnitude and phase decoders](compiler_robust_hopf/decoders.py)
- [Decoder tests](tests/test_decoders.py)
- [Compiler contracts and checkpoint boundary](docs/COMPILER_BOUNDARIES.md)

---

## 12. Verification and internal audits

The proof is supported by exact finite checks, not inferred from them.

The executable suite compares independently built frame matrices, addressed
layers, strict-zero echoes, tree cuts, one-hot decoder permutations, routed
subframes, phase UCGs, compiler counterexamples, and gradient decoders. Resource
inequalities are checked with integer or exact-rational arithmetic rather than
numerical slope fitting.

The most useful first command is

```bash
python scripts/reviewer_walkthrough.py
```

which prints a short sequence of readable checks. The complete suite is

```bash
python validate.py
```

and the two resource ledgers are

```bash
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

Three detailed internal review records remain visible:

| Record | Purpose |
|---|---|
| [Consolidated proof audit](docs/PROOF_AUDIT.md) | register and all-workspace asymptotic accounting |
| [Strict-zero audit](docs/STRICT_ZERO_ECHO_AUDIT.md) | sector order, restoration, endpoints, and hidden-workspace check |
| [Clean-room reconstruction](docs/CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem re-derived from operator definitions rather than development chronology |

The complete evidence taxonomy and test map are in
[Verification and evidence](docs/VERIFICATION.md).

> **What should be checked here?**  Treat tests as falsification tools for
> finite conventions and implementations. The dimension-independent theorem
> still rests on the operator proofs and imported synthesis bounds.

---

## 13. Source and contribution boundaries

The complete proof depends on three kinds of source.

### Inherited from the Hopf papers

- balanced real and complex Hopf charts;
- diagonal metric weights;
- normalized magnitude tangents;
- marker-column differential frame;
- global, phase, and checkpoint gradient records;
- fixed-norm concentration statement.

### Imported from Yuan–Zhang

- optimal QSP benchmark;
- ancilla-free multi-controlled X;
- all-workspace UCG tradeoff;
- coherent copy–uncopy.

### Proved in this repository

- frame-safe substitution and compiler hierarchy;
- exact state-column obstruction;
- strict-zero borrowed-suffix echo;
- conditioned-prefix and tail direct-sum structure;
- self-contained binary–one-hot decoder;
- routed parallel-subframe compiler;
- optimal all-workspace frame theorem;
- separated complex compiler corollary;
- no-additional-depth-factor QBP consequence.

The exact paper, theorem, local file, and test locations are in
[the source map](docs/SOURCE_MAP.md).

The related-work statement is deliberately narrow. The repository does not
claim the generic echo, UCGs, borrowed workspace, or square-root identities as
new. The Hopf-specific contribution is the complete-frame synthesis and its
resource frontier. A detailed comparison appears in
[Related work and contribution boundary](docs/RELATED_WORK.md).

---

## 14. Scope exclusions

The theorem is an exact logical synthesis result. It does not presently cover:

- restricted device connectivity or SWAP routing;
- native hardware gate sets;
- approximate Clifford+T synthesis and T-depth;
- coherent or stochastic hardware noise;
- readout mitigation;
- approximate block encodings of generic observables;
- a universal cost model for controlled observable access;
- arbitrary non-Hopf charts or generic structured unitaries;
- finite-size constant optimization among the three schedules.

These exclusions are not needed for the exact theorem and should be treated as
separate compiler or hardware layers.

---

## 15. Central technical questions for review

A complete technical assessment can be organized around the following
questions.

1. Does the addressed-layer product realize the claimed Hopf differential frame
   with the stated marker convention?
2. Does the two-qubit example establish that state-column equality is too weak
   for the global decoder?
3. Does the strict-zero echo implement every nonfinal addressed layer as a
   complete operator and restore the borrowed logical qubit without phase?
4. Are the imported MCT and UCG hypotheses used with the correct total-width and
   workspace conventions?
5. Is the binary–one-hot decoder reversible, clean, and correctly counted?
6. Does the router work on arbitrary prefix–suffix entanglement and return every
   auxiliary register to zero?
7. Does the peak workspace fit in `2B(s+1)` and therefore within the chosen
   ancillary budget?
8. Do the low-workspace absorption and maximal-cut inequalities cover every
   `m>=0` endpoint?
9. Do the parameter-count and light-cone arguments give the matching lower
   bound for the real family?
10. Does the one-UCG diagonal establish the complex result with sequential
    workspace reuse?
11. Does frame-safe substitution preserve the complete global QBP distribution
    under the stated observable and accuracy model?
12. Is the contribution boundary relative to state preparation, UCGs, and
    borrowed-workspace techniques stated accurately and generously?

The repository is arranged so that each question can be answered from a nearby
formula, implementation, and finite test rather than by reconstructing the
entire project history.

---

## Reading onward

- [Minimal Hopf interface](docs/HOPF_INTERFACE.md)
- [Complete all-workspace compiler proof](docs/COMPILER_THEOREM.md)
- [Quantum-backpropagation consequence](docs/QBP_CONSEQUENCE.md)
- [Verification and evidence](docs/VERIFICATION.md)
- [Fact-level source map](docs/SOURCE_MAP.md)
- [Related work and contribution boundary](docs/RELATED_WORK.md)

[Back to the landing page](README.md)
