# Minimal Hopf interface for the compiler theorem

[← Landing page](../README.md) · [Read the complete narrative](../REVIEW.md) · [Next: compiler theorem →](COMPILER_THEOREM.md)

This page isolates the Hopf facts consumed by the compiler theorem. It is not a
replacement for the full Hopf-ansatz or Hopf-QBP papers. Its purpose is
narrower: a circuit-synthesis reader should be able to identify the exact
unitary being compiled, the columns that matter, the coordinate domain, and the
addressed-layer structure without first learning the full optimization
framework.

The final all-workspace result uses the Yuan–Zhang exact circuit framework and
covers every clean-workspace budget `m>=0`.

## 1. The object is a coordinate frame, not only a state loader

Fix `n` system qubits and write

```math
N=2^n.
```

The real Hopf chart assigns one angle to each internal node of a complete binary
tree, hence `N-1` magnitude coordinates. The root angle splits amplitude
between the left and right halves of the computational basis. Each descendant
angle splits the amplitude entering its subtree, and the recursion continues to
sibling leaves.

For internal node `j`, let `a_j(theta)` be the **oriented incoming amplitude**:
the product of the sine or cosine factors selected along the path from the root
to that node. Differentiating the split at `j` replaces the local subtree state
by a unit orthogonal complement `|e_j>`. The exact differential is

```math
\boxed{
\partial_{\theta_j}|\psi(\boldsymbol\theta)\rangle
=a_j(\boldsymbol\theta)|e_j(\boldsymbol\theta)\rangle,
\qquad
g_{j,j}=a_j(\boldsymbol\theta)^2.
}
```

This formulation is valid for unrestricted real angles. The principal metric
square root is

```math
\sqrt{g_{j,j}}=|a_j|.
```

On the canonical Hopf domains described below, every ancestor factor entering
`a_j` is nonnegative, so

```math
a_j=\sqrt{g_{j,j}}.
```

At a regular point, `g_(j,j)>0`, the vector `|e_j>` is the normalized coordinate
derivative up to the canonical positive metric weight. At a singular point,
`g_(j,j)=0`, the raw differential vanishes. The unit vector `|e_j>` remains a
**chart-selected orthogonal continuation determined by the complete parameter
tuple** and occupies the same marker column, but it is not the normalization of
a nonzero derivative.

The state and the `N-1` chart-selected continuation vectors form an orthonormal
basis for every choice of angles. The **real Hopf differential frame** is the
unitary `W_R` satisfying

```math
W_{\mathbb R}|0^n\rangle
=|\psi_{\mathbb R}(\boldsymbol\theta)\rangle,
```

```math
W_{\mathbb R}|\lambda(j)\rangle
=|e_j^{\mathbb R}(\boldsymbol\theta)\rangle,
\qquad 1\leq j<N.
```

The marker `lambda(j)` is a nonzero computational-basis label assigned to node
`j`. The frame converts a known computational basis into the state and its
marker-frame directions.

This is the geometric interface required by the compiler theorem. The inverse
coordinate map, optimization architecture, and numerical studies remain in the
first Hopf paper and repository.

## 2. Canonical coordinate domains

The compiler identities are algebraic and remain valid for unrestricted real
angles. The geometric notation `a_j=sqrt(g_(j,j))`, however, uses the canonical
chart domains.

For the **real chart**:

- every magnitude angle at depths `0,...,n-2` lies in
  ```math
  [0,\pi/2];
  ```
- every angle at the final magnitude depth lies in
  ```math
  [0,2\pi),
  ```
  so the last sibling split can encode signs without a separate phase layer.

For the **complex chart**, every magnitude angle lies in

```math
[0,\pi/2],
```

and one phase `phi_l` is attached to each leaf.

Only ancestor angles enter an internal node's incoming amplitude. In the real
chart, the final-depth angles therefore do not affect the sign of any internal
`a_j`. Hence every `a_j` is nonnegative on the canonical real and complex
magnitude domains.

The implementation exposes both views:

- `incoming_amplitude` stores the oriented value valid for unrestricted angles;
- `sqrt_metric` is the principal nonnegative square root;
- `regular_mask` uses a documented numerical tolerance for nonzero metric
  weight;
- `regular_coordinate_mask(atol=...)` permits a caller-selected tolerance;
- `in_canonical_magnitude_domain` checks the declared domains.

This separation prevents unrestricted algebraic tests from silently changing
the meaning of `sqrt(g_(j,j))` and prevents floating-point chart boundaries from
being mislabeled as regular coordinates.

## 3. Tree and marker conventions

Internal nodes are indexed breadth first, beginning at one. If node `j` lies at
depth `d` and position `r`, then

```math
j=2^d+r,
\qquad
0\leq r<2^d.
```

Its computational marker is

```math
\lambda(j)
=(2r+1)2^{n-d-1}.
```

Equivalently, the marker bit string consists of:

- the `d`-bit prefix describing the node position;
- a one at the node's target position;
- zeros in every lower suffix position.

The corresponding left-subtree anchor is

```math
\ell_0(j)=r2^{n-d}.
```

The addressed rotation at node `j` mixes exactly

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
| `m` | clean ancillary qubits supplied to the compiler, `m>=0` |
| `j` | breadth-first internal-node index, `1<=j<N` |
| `d` | depth of an internal node, `0<=d<n` |
| `r` or `p` | node position or prefix at depth `d` |
| `theta_(d,p)` | Hopf magnitude angle at that node |
| `a_j` | oriented incoming amplitude multiplying coordinate `j` |
| `g_(j,j)=a_j^2` | diagonal metric weight |
| `|e_j>` | unit marker-frame direction; a normalized derivative direction when `g_(j,j)>0`, otherwise a chart-selected continuation |
| `lambda(j)` | computational marker assigned to `|e_j>` |
| `W_R` | real Hopf differential frame |
| `D_ph` | diagonal complex leaf-phase layer |
| `W_(C,mag)=D_ph W_R` | phase-dressed complex magnitude frame |

Basis labels are ordered from the most significant tree decision to the least
significant one. In code they are ordinary nonnegative integers in this order.

## 4. The complete addressed layer

At depth `d`, split a basis label as

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

The rotation convention is

```math
R_y(\alpha)=e^{-i\alpha Y}
=
\begin{pmatrix}
\cos\alpha&-\sin\alpha\\
\sin\alpha&\cos\alpha
\end{pmatrix}.
```

Thus:

1. the prefix selects one of `2^d` angles;
2. the target rotates only when every lower suffix bit is zero;
3. every nonzero-suffix sector is fixed.

The complete real frame is

```math
\boxed{
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_1^{(n)}L_0^{(n)},
}
```

with `L_0` acting first on state vectors.

The zero-suffix restriction is essential. It preserves the state-and-complement
columns established at earlier depths. It is also the compiler's central
structural feature: the long shared predicate must be recognized without
corrupting arbitrary frame columns.

> **What should be checked here?** Verify the basis ordering, marker formula,
> layer order, and identity action on every nonzero-suffix sector. A formula
> valid only on the state-preparation input is not enough.

### Executable counterpart

- [Marker and anchor conventions](../compiler_robust_hopf/conventions.py)
- [Recursive state, oriented differentials, and frame](../compiler_robust_hopf/frames.py)
- [Independent addressed-layer construction](../compiler_robust_hopf/frames.py)
- [Frame and chart-domain tests](../tests/test_frames.py)

## 5. A complete two-qubit example

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

The unit frame continuations are

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

The oriented differential factors are

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

On the canonical domain `theta_1 in [0,pi/2]`, these factors are the principal
metric square roots. At `theta_1=0`, the third derivative vanishes while
`|e_3>` remains the chart-selected unit continuation fixed by the complete
parameter tuple.

The markers are

```math
\lambda(1)=10_2,
\qquad
\lambda(2)=01_2,
\qquad
\lambda(3)=11_2.
```

Hence in computational column order the frame is

```math
W_{\mathbb R}
=
\begin{pmatrix}
|&|&|&|\\
\psi&e_2&e_1&e_3\\
|&|&|&|
\end{pmatrix}.
```

At

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

## 6. Why one correct state column is not enough

Let `Q` swap `|01>` and `|10>` while fixing `|00>` and `|11>`, and define

```math
V=W_{\mathbb R}Q.
```

Because `Q|00>=|00>`,

```math
V|00\rangle=W_{\mathbb R}|00\rangle=|\psi\rangle.
```

Thus `V` is an exact state-preparation completion for the same target state,
but it exchanges the marker columns for `e_1` and `e_2`.

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

The unchanged marker decoder returns

```math
(2,0,0)
```

for the Hopf frame but

```math
(0,\sqrt2,0)
```

for the state-equivalent completion.

<p align="center">
  <img src="../assets/two-qubit-obstruction.svg" width="900" alt="Two unitaries prepare the same two-qubit state, but one swaps tangent-marker columns and changes the decoded gradient." />
</p>

```math
\boxed{
\text{State-column equality loads }|\psi\rangle,
\text{ but does not guarantee inverse-frame gradient readout.}
}
```

### Executable counterpart

- [Exact counterexample construction](../compiler_robust_hopf/compiler_boundaries.py)
- [Distribution and decoded-gradient tests](../tests/test_compiler_boundaries.py)

## 7. The phase-dressed complex magnitude frame

For the complex chart, attach one phase `phi_l` to each computational leaf and
define

```math
D_{\mathrm{ph}}
=\sum_{\ell=0}^{N-1}
e^{i\phi_\ell}|\ell\rangle\!\langle\ell|.
```

The unitary compiled by the inverse-frame magnitude protocol is

```math
\boxed{
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
}
```

It satisfies

```math
W_{\mathbb C,\mathrm{mag}}|0^n\rangle
=|\psi_{\mathbb C}\rangle,
```

```math
W_{\mathbb C,\mathrm{mag}}|\lambda(j)\rangle
=|e_j^{\mathbb C}\rangle.
```

This is a frame for the `N-1` complex-chart **magnitude** directions. The `N`
leaf-phase differentials cannot all be additional columns of the same
`N`-dimensional unitary. They are localized in the computational basis and use
a separate direct signed one-hot record in the QBP protocol.

Writing a basis label as `x=zb`, with the final bit as target,

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

Thus the phase dressing is one exact `n`-qubit UCG, and the complex magnitude
compiler is a short corollary of the real-frame compiler.

> **What should be checked here?** Verify complete operator equality, including
> common phase, and keep the magnitude-frame stream distinct from the direct
> leaf-phase stream.

### Executable counterpart

- [Phase-dressed magnitude frame](../compiler_robust_hopf/frames.py)
- [Complex magnitude and phase derivatives](../compiler_robust_hopf/complex_analysis.py)
- [One-UCG phase diagonal](../compiler_robust_hopf/unified_compiler.py)
- [Complex composition tests](../tests/test_unified_compiler.py)

## 8. What is inherited and what is proved here

The first Hopf paper supplies the balanced chart, inverse map, diagonal metric,
and normalized tangent construction on regular coordinates. `Hopf-QBP` supplies
the addressed frame, global and direct-phase records, checkpoint interface, and
statistical task boundaries.

This repository takes the complete real frame and phase-dressed complex
magnitude frame as synthesis targets. It proves:

- the operator-level frame-safe compiler contract;
- explicit failure of the weaker state-column contract;
- exact all-workspace constructions, including an explicit coherent router;
- matching size and depth bounds;
- preservation of the global QBP distribution under frame-safe substitution.

For exact theorem, repository, implementation, and test locations, see
[the source map](SOURCE_MAP.md).

---

[← Landing page](../README.md) · [Read the complete narrative](../REVIEW.md) · [Next: compiler theorem →](COMPILER_THEOREM.md)
