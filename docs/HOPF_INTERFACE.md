# Minimal Hopf interface for the compiler theorem

[← Landing page](../README.md) · [Read the complete narrative](../REVIEW.md) · [Next: compiler theorem →](COMPILER_THEOREM.md)

This page isolates the Hopf facts used by the compiler result. It is not a
replacement for the full Hopf-ansatz or Hopf-QBP papers. The purpose is narrower:
a circuit-synthesis reader should be able to identify the exact unitary being
compiled, the columns that matter, and the addressed-layer structure without
first learning the full optimization framework.

## 1. The object is a coordinate frame, not only a state loader

Fix `n` system qubits and write

```math
N=2^n.
```

The real Hopf chart uses one angle for each internal node of a complete binary
tree, hence `N-1` real coordinates. The root angle splits amplitude between the
left and right halves of the computational basis. The next two angles split
those halves, and so on until the final layer splits sibling basis states.

For one internal node `j`, differentiating its local split replaces the local
subtree state by its orthogonal complement. Repeating this fact through the tree
gives a normalized direction `|e_j>` and a known scalar weight
`sqrt(g_(j,j))` such that

```math
\partial_{\theta_j}|\psi(\boldsymbol\theta)\rangle
=\sqrt{g_{j,j}}\,|e_j(\boldsymbol\theta)\rangle.
```

The normalized directions are mutually orthogonal and orthogonal to the state.
They therefore complete the state to an orthonormal basis.

The **real Hopf differential frame** is the unitary `W_R` whose designated
columns satisfy

```math
W_{\mathbb R}|0^n\rangle
=|\psi(\boldsymbol\theta)\rangle,
```

```math
W_{\mathbb R}|\lambda(j)\rangle
=|e_j(\boldsymbol\theta)\rangle,
\qquad 1\leq j<N.
```

The marker `lambda(j)` is a nonzero computational-basis label assigned to node
`j`. Thus the frame converts a known computational basis into the state and its
normalized coordinate directions.

This is the only geometric interface required by the global compiler theorem.
The inverse coordinate map, optimizer construction, and numerical optimization
studies remain important parts of the first Hopf paper, but they are not used in
the synthesis proof here.

## 2. Tree and marker conventions

Internal nodes are indexed breadth first, beginning at one. If node `j` lies at
depth `d` and position `r`, then

```math
j=2^d+r,
\qquad
0\leq r<2^d.
```

The computational marker for this node is

```math
\lambda(j)
=(2r+1)2^{n-d-1}.
```

Equivalently, the marker bit string consists of:

- the `d`-bit prefix describing the node position;
- a one in the node's target position;
- zeros in every lower suffix position.

The corresponding left-subtree anchor has label

```math
\ell_0(j)=r2^{n-d}.
```

The addressed rotation at node `j` mixes exactly the two basis states

```math
|\ell_0(j)\rangle
\quad\text{and}\quad
|\lambda(j)\rangle.
```

### Notation used throughout this repository

| Symbol | Meaning |
|---|---|
| `n` | number of system qubits |
| `N=2^n` | Hilbert-space dimension |
| `j` | breadth-first internal-node index, `1<=j<N` |
| `d` | depth of an internal node, `0<=d<n` |
| `r` or `p` | node position or prefix at depth `d` |
| `theta_(d,p)` | Hopf angle attached to that node |
| `|psi>` | current real or complex Hopf state |
| `|e_j>` | normalized magnitude-coordinate tangent |
| `g_(j,j)` | diagonal coordinate-metric weight |
| `lambda(j)` | computational marker assigned to `|e_j>` |
| `W_R` | real Hopf differential frame |
| `D_ph` | diagonal complex leaf-phase layer |
| `W_C=D_ph W_R` | separated complex magnitude frame |
| `m` | number of clean ancillary qubits supplied to the compiler |

Basis labels are ordered from the most significant tree decision to the least
significant one. In code, computational labels are ordinary nonnegative
integers in this bit order.

## 3. The complete addressed layer

At depth `d`, split the system label as

```math
|p\rangle_P|x\rangle_T|z\rangle_Z,
```

where:

- `p` is the `d`-bit upper prefix;
- `x` is the next qubit and is the rotation target;
- `z` is the lower suffix of length
  ```math
  s=n-d-1.
  ```

The depth-`d` addressed layer is

```math
\boxed{
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^s\rangle\!\langle0^s|
}
```

with the Hopf convention

```math
R_y(\alpha)=e^{-i\alpha Y}
=
\begin{pmatrix}
\cos\alpha&-\sin\alpha\\
\sin\alpha&\cos\alpha
\end{pmatrix}.
```

This equation is the compiler's local target. It says:

1. the prefix selects one of `2^d` angles;
2. the target is rotated only when every lower suffix bit is zero;
3. every other computational sector is fixed.

The complete real frame is the ordered product

```math
\boxed{
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_1^{(n)}L_0^{(n)},
}
```

where the root layer `L_0` acts first on state vectors.

The zero-suffix restriction is not incidental. It is what preserves the
state-and-complement columns already established higher in the tree. It is also
the source of the strict-zero compilation problem: a clean implementation must
recognize this long shared predicate without disturbing arbitrary input
columns.

> **What should be checked here?**  Verify the basis ordering, the marker
> formula, the state-update order of the layers, and the fact that the operator
> is identity on every nonzero-suffix sector. A state-preparation-only formula
> is not sufficient.

### Executable counterpart

- [Marker and anchor conventions](../compiler_robust_hopf/conventions.py)
- [Recursive state, tangent, and frame construction](../compiler_robust_hopf/frames.py)
- [Independent addressed-layer construction](../compiler_robust_hopf/frames.py)
- [Frame parity tests](../tests/test_frames.py)

## 4. A complete two-qubit example

For two qubits, the real chart has three angles:

- `theta_1` at the root;
- `theta_2` in the left subtree;
- `theta_3` in the right subtree.

The state is

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

The normalized directions are

```math
|e_1\rangle
=-\sin\theta_1
 \bigl(\cos\theta_2|00\rangle+
       \sin\theta_2|01\rangle\bigr)
+\cos\theta_1
 \bigl(\cos\theta_3|10\rangle+
       \sin\theta_3|11\rangle\bigr),
```

```math
|e_2\rangle
=-\sin\theta_2|00\rangle+
 \cos\theta_2|01\rangle,
```

```math
|e_3\rangle
=-\sin\theta_3|10\rangle+
 \cos\theta_3|11\rangle.
```

Their metric weights are

```math
\partial_{\theta_1}|\psi\rangle=|e_1\rangle,
```

```math
\partial_{\theta_2}|\psi\rangle
=\cos\theta_1|e_2\rangle,
\qquad
\partial_{\theta_3}|\psi\rangle
=\sin\theta_1|e_3\rangle.
```

The markers are

```math
\lambda(1)=10_2,
\qquad
\lambda(2)=01_2,
\qquad
\lambda(3)=11_2.
```

Hence, in the computational column order
`|00>,|01>,|10>,|11>`, the frame is

```math
W_{\mathbb R}
=
\begin{pmatrix}
|&|&|&|\\
\psi&e_2&e_1&e_3\\
|&|&|&|
\end{pmatrix}.
```

At the symmetric point

```math
\theta_1=\theta_2=\theta_3=\frac{\pi}{4},
```

this becomes

```math
W_{\mathbb R}
=
\begin{pmatrix}
\frac12&-\frac1{\sqrt2}&-\frac12&0\\[3pt]
\frac12& \frac1{\sqrt2}&-\frac12&0\\[3pt]
\frac12&0&\frac12&-\frac1{\sqrt2}\\[3pt]
\frac12&0&\frac12& \frac1{\sqrt2}
\end{pmatrix}.
```

The first column is the uniform state. The other three columns are fixed by the
differential geometry and are not arbitrary choices of unitary completion.

## 5. Why one correct state column is not enough

Let `Q` swap the computational basis states `|01>` and `|10>` while fixing
`|00>` and `|11>`, and define

```math
V=W_{\mathbb R}Q.
```

Because `Q|00>=|00>`,

```math
V|00\rangle=W_{\mathbb R}|00\rangle=|\psi\rangle.
```

Thus `V` is an exact state-preparation completion for the same target state.
But it exchanges the marker columns for `e_1` and `e_2`.

Choose

```math
O=-Z\otimes I.
```

At the symmetric point,

```math
W_{\mathbb R}^{\dagger}O|\psi\rangle=|10\rangle,
```

whereas

```math
V^{\dagger}O|\psi\rangle=|01\rangle.
```

The canonical marker decoder returns the exact coordinate gradient

```math
(2,0,0),
```

but the state-equivalent completion returns

```math
(0,\sqrt2,0).
```

<p align="center">
  <img src="../assets/two-qubit-obstruction.svg" width="900" alt="Two unitaries prepare the same two-qubit state, but one swaps tangent-marker columns and changes the decoded gradient." />
</p>

```math
\boxed{
\text{State-column equality is sufficient for loading }|\psi\rangle,
\text{ but insufficient for inverse-frame gradient readout.}
}
```

> **What should be checked here?**  Confirm that `Q` fixes `|00>`, that both
> circuits prepare the same state, that the response marker moves from `|10>`
> to `|01>`, and that the decoder is intentionally unchanged. The example is a
> compiler-contract obstruction, not a claim that every state-preparation
> completion fails.

### Executable counterpart

- [Exact counterexample construction](../compiler_robust_hopf/compiler_boundaries.py)
- [Distribution and decoded-gradient tests](../tests/test_compiler_boundaries.py)

## 6. Complex magnitudes require only a diagonal dressing

For the complex chart, attach one phase `phi_l` to each computational leaf and
define

```math
D_{\mathrm{ph}}
=\sum_{\ell=0}^{N-1}
e^{i\phi_\ell}|\ell\rangle\!\langle\ell|.
```

The separated complex magnitude frame is

```math
\boxed{
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
}
```

It satisfies

```math
W_{\mathbb C}|0^n\rangle=|\psi_{\mathbb C}\rangle,
```

```math
W_{\mathbb C}|\lambda(j)\rangle
=|e_j^{\mathbb C}\rangle.
```

The magnitude compiler therefore consists of the real frame followed by one
diagonal unitary. The leaf-phase derivatives themselves are already localized
in the computational basis and are read by a separate direct record in the QBP
protocol.

The diagonal is also one `n`-qubit uniformly controlled one-qubit gate. Writing
a basis label as `x=zb`, with the final bit chosen as target,

```math
D_{\mathrm{ph}}
=
\sum_z |z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
```

This observation makes the complex compiler a short corollary once the real
frame is compiled.

> **What should be checked here?**  Verify complete operator equality, including
> the common phase, and distinguish the complex magnitude frame from the direct
> phase-gradient record.

### Executable counterpart

- [Separated complex frame](../compiler_robust_hopf/frames.py)
- [Complex chart identities](../compiler_robust_hopf/complex_analysis.py)
- [One-UCG phase diagonal](../compiler_robust_hopf/unified_compiler.py)
- [Complex composition tests](../tests/test_unified_compiler.py)

## 7. What is inherited and what is proved here

The first Hopf paper supplies the balanced coordinate chart, inverse map,
diagonal metric, and normalized tangent-state construction. The Hopf-QBP paper
assembles the normalized magnitude directions into the addressed frame and uses
its inverse in shared gradient records.

This repository takes that complete frame as the synthesis target. It proves:

- the operator-level compiler contract required by the global record;
- explicit failure of the weaker state-column contract;
- exact all-workspace constructions of the complete frame;
- matching size and depth bounds;
- preservation of the QBP distribution under frame-safe substitution.

For exact theorem, equation, repository, implementation, and test locations, see
[the source map](SOURCE_MAP.md).

---

[← Landing page](../README.md) · [Read the complete narrative](../REVIEW.md) · [Next: compiler theorem →](COMPILER_THEOREM.md)
