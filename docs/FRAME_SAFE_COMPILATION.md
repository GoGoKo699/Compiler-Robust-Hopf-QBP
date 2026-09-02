# Frame-safe compilation

## 1. Why state preparation is not enough

Let

```math
W_{\boldsymbol\theta}|0\rangle
=|\psi(\boldsymbol\theta)\rangle
```

be the canonical Hopf differential frame. Its designated nonzero columns contain
the normalized coordinate tangents:

```math
W_{\boldsymbol\theta}|\lambda(j)\rangle
=|e_j(\boldsymbol\theta)\rangle.
```

A generic state-preparation compiler only promises

```math
V_{\boldsymbol\theta}|0\rangle
=|\psi(\boldsymbol\theta)\rangle.
```

Since the first columns agree, one may write

```math
V_{\boldsymbol\theta}=W_{\boldsymbol\theta}Q_{\boldsymbol\theta},
\qquad
Q_{\boldsymbol\theta}|0\rangle=|0\rangle.
```

There is no corresponding restriction on `Q_theta` over the orthogonal
complement of `|0>`. After the observable branch,

```math
V_{\boldsymbol\theta}^{\dagger}O|\psi\rangle
=
Q_{\boldsymbol\theta}^{\dagger}
W_{\boldsymbol\theta}^{\dagger}O|\psi\rangle.
```

The uncontrolled factor can mix all tangent-marker amplitudes. Therefore
initialized-state-column equality does not license replacing
`W_theta^dagger` by `V_theta^dagger`.

This is the central obstruction that any compiler-robust statement must respect.

## 2. Clean frame contract

A compiled frame with `w` workspace qubits is **frame-safe** when

```math
\widetilde W_{\boldsymbol\theta}
\bigl(|\varphi\rangle|0^w\rangle\bigr)
=
\bigl(W_{\boldsymbol\theta}|\varphi\rangle\bigr)|0^w\rangle
```

for every system state `|varphi>`. If

```math
P_0=I\otimes|0^w\rangle\!\langle0^w|,
```

this is equivalently

```math
\widetilde W_{\boldsymbol\theta}P_0
=(W_{\boldsymbol\theta}\otimes I)P_0.
```

The right-hand side maps the range of `P_0` unitarily onto the same subspace.
Because `W_tilde` is unitary, the equality therefore implies that the clean
workspace subspace is reducing, not merely invariant:

```math
\widetilde W_{\boldsymbol\theta}P_0
=P_0\widetilde W_{\boldsymbol\theta},
\qquad
\widetilde W_{\boldsymbol\theta}^{\dagger}P_0
=P_0\widetilde W_{\boldsymbol\theta}^{\dagger}.
```

In particular, the inverse obeys the required clean-input identity

```math
\widetilde W_{\boldsymbol\theta}^{\dagger}P_0
=(W_{\boldsymbol\theta}^{\dagger}\otimes I)P_0.
```

Thus the forward and inverse compiled frames both return the workspace to zero
for every system input. The contract need not specify the compiler's action when
the workspace starts in an arbitrary nonzero state.

## 3. Substitution theorem

> **Frame-safe substitution.** Replace `W_theta` or `W_theta^dagger` in the
> global Hopf protocol by a frame-safe compiled implementation or its inverse.
> Initialize its workspace in `|0^w>` and apply no unrelated operation to that
> workspace while the compiled block is active. Then the joint output is the
> original protocol output tensored with `|0^w>`. Consequently, the complete
> distribution on the original measured registers, decoded gradient mean,
> record norm, and finite-shot concentration premises are unchanged.

### Proof

For a forward occurrence, the defining clean-frame identity gives the claim
directly on every system input, including states entangled with untouched
external registers by linear extension.

For an inverse occurrence, Section 2 establishes

```math
\widetilde W_{\boldsymbol\theta}^{\dagger}P_0
=(W_{\boldsymbol\theta}^{\dagger}\otimes I)P_0.
```

Hence a clean workspace input undergoes exactly the original inverse frame and
returns to the clean subspace. Replacing either block therefore leaves the state
of all original protocol registers unchanged and factors the workspace as
`|0^w>`. Measuring only the original registers gives exactly the same
probability distribution. Every estimator statement that is a function of that
distribution is consequently preserved.

## 4. What compilation may change

Frame-safe compilation may change:

- elementary physical rotation angles;
- gate ordering;
- ancillary workspace;
- circuit size and depth constants;
- parameter preprocessing;
- device routing after logical synthesis.

It may not change:

- the complete system action on clean workspace input;
- the tangent-marker columns;
- the relative phase convention used by the interference protocol;
- the declared observable-access interface.

In particular, one Hopf coordinate need not remain one physical gate angle. The
Möttönen-style compiler in the established `Hopf-QBP` repository already
provides an example: compiler-generated multiplexor angles replace the original
coordinate angles while the complete frame action remains intact.

## 5. Resource inheritance criterion

Logical correctness does not by itself imply backpropagation scaling. Let

```math
C_{\mathrm{prep}}(n,m)
```

be the matched scalar state-preparation cost and

```math
C_{\mathrm{frame}}(n,m)
```

be the clean frame cost in the same circuit model. A useful compiler-robust
result needs a bound of the form

```math
C_{\mathrm{frame}}(n,m)
\leq
\rho(n,m)C_{\mathrm{prep}}(n,m),
```

where `rho` remains within the overhead permitted by the chosen quantum
backpropagation definition. Size, depth, and workspace should be compared
separately.

For end-to-end work, the following must also be reported:

```math
\text{executions},\quad
\text{controlled-observable cost},\quad
\text{classical decoding},\quad
\text{output size}.
```

## 6. Chart-native versus compiler-native ingredients

| Ingredient | Mathematical source |
|---|---|
| State and coordinate tangents | Hopf chart |
| Orthogonality and diagonal pullback metric | Hopf chart |
| Marker assignment | Chosen coherent frame completion |
| Shared Walsh record | Frame plus measurement design |
| Clean physical implementation | Compiler |
| Ancilla--depth tradeoff | Compiler theorem |
| Checkpoint interfaces | Particular circuit factorization |

This is why the global method is the natural object for compiler robustness.
Checkpoint methods may remain efficient under structure-preserving compilers,
but their intermediate interfaces are not determined by the final state chart
alone.

## 7. Counterexample template for state-column claims

Choose any nontrivial unitary `Q` satisfying `Q|0>=|0>` and mixing two marker
basis states. Define `V=WQ`. Then `V|0>=W|0>`, but `V^dagger O|psi>` contains the
marker amplitudes after the additional mixing `Q^dagger`. Unless the decoder is
changed with full knowledge of `Q`, the original coordinate estimates are
incorrect.

A manuscript version should include the smallest explicit finite-dimensional
example, preferably on two system qubits, as a negative proposition rather than
only a verbal warning.
