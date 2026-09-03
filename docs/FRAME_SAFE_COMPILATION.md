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

This obstruction is realized explicitly, with exact distributions and decoded
gradients, in [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md).

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
Because `W_tilde` is unitary, the equality implies that the clean workspace
subspace is reducing, not merely invariant:

```math
\widetilde W_{\boldsymbol\theta}P_0
=P_0\widetilde W_{\boldsymbol\theta},
\qquad
\widetilde W_{\boldsymbol\theta}^{\dagger}P_0
=P_0\widetilde W_{\boldsymbol\theta}^{\dagger}.
```

In particular, the inverse obeys

```math
\widetilde W_{\boldsymbol\theta}^{\dagger}P_0
=(W_{\boldsymbol\theta}^{\dagger}\otimes I)P_0.
```

Thus the forward and inverse compiled frames both return the workspace to zero
for every system input. The contract need not specify the compiler's action when
the workspace starts in an arbitrary nonzero state.

## 3. Global frame-safe substitution

> **Theorem (frame-safe substitution).** Replace `W_theta` or
> `W_theta^dagger` in the global Hopf protocol by a frame-safe compiled
> implementation or its inverse. Initialize its workspace in `|0^w>` and apply
> no unrelated operation to that workspace while the compiled block is active.
> Then the joint output is the original protocol output tensored with `|0^w>`.
> Consequently, the complete distribution on the original measured registers,
> decoded gradient mean, record norm, and finite-shot concentration premises are
> unchanged.

For a forward occurrence, the defining clean-frame identity gives the claim on
every system input, including inputs entangled with untouched external
registers. For an inverse occurrence, Section 2 gives the corresponding inverse
identity. Every original protocol register is therefore unchanged and the
workspace factors as `|0^w>`.

## 4. Clean sequential composition

Suppose clean compilers `U_tilde` and `V_tilde` implement system unitaries `U`
and `V` using at most `a` and `b` workspace qubits. Embed both in a common pool
of

```math
w=\max\{a,b\}
```

clean qubits, leaving unused wires untouched. Because the first block returns
the pool to zero, the second begins with a clean input. Therefore

```math
\widetilde V\widetilde U
\bigl(|\varphi\rangle|0^w\rangle\bigr)
=
(VU|\varphi\rangle)|0^w\rangle.
```

Workspace costs take a maximum rather than a sum, while circuit sizes and depths
add for a sequential schedule. The inverse clean composition is obtained by
reversing the two blocks and taking their adjoints.

This is the register-level reason that the clean real Hopf frame and the clean
diagonal phase layer can share one ancillary pool in the separated complex
construction.

## 5. What full frame-safe compilation may change

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

One Hopf coordinate need not remain one physical gate angle. The Möttönen-style
compiler in the established `Hopf-QBP` repository already provides an example:
compiler-generated multiplexor angles replace the coordinate angles while the
complete frame action remains intact.

## 6. Resource inheritance criterion

Logical correctness does not by itself imply backpropagation scaling. Let

```math
C_{\mathrm{prep}}(n,m)
```

be the matched scalar state-preparation cost and

```math
C_{\mathrm{frame}}(n,m)
```

be the clean frame cost in the same circuit model. A compiler-robust result
needs a bound of the form

```math
C_{\mathrm{frame}}(n,m)
\leq
\rho(n,m)C_{\mathrm{prep}}(n,m),
```

where `rho` remains within the permitted backpropagation overhead. Size, depth,
and workspace must be compared separately. End-to-end accounting must also
report executions, controlled-observable cost, classical decoding, and output
size.

## 7. Checkpoint active-interface contract

Checkpoint methods require a different, factorization-specific contract. Write
one preparation as

```math
U=B_dA_d,
```

and let `P_d` project onto the zero-lower-suffix subspace present after `A_d`.
A compiled suffix `B_tilde_d` is **active-interface safe** when, for a single
phase `chi` independent of the interface input,

```math
\widetilde B_dJP_d
=
e^{i\chi}JB_dP_d.
```

This is weaker than full-unitary equality because no action is prescribed on
the orthogonal input sector. It is stronger than preserving only the one prefix
state `A_d|0>`.

> **Theorem (checkpoint active-interface substitution).** Use an
> active-interface-safe suffix consistently in the forward and reverse
> checkpoint circuit. Then every designated checkpoint gradient estimator at
> depth `d` has exactly the same expectation as under the original suffix for
> every allowed controlled observable. The complete measurement distribution
> need not be preserved.

The proof uses two facts: the reference branch lies in `P_d`, and every
checkpoint score operator preserves `P_d`. Hence its ancilla-off-diagonal
correlation sees only the active clean component of the observed branch. The
adjoint of the interface identity makes that component exactly equal to the
original `P_d B_d^dagger O|psi>` component. Details and explicit examples are
in [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md).

## 8. Strict hierarchy of promises

The compiler promises form a strict hierarchy:

| Promise | Sufficient for scalar state | Sufficient for checkpoint means | Sufficient for global distribution |
|---|---:|---:|---:|
| One prepared state column | yes | no | no |
| Complete checkpoint active interface | yes | yes | no |
| Complete frame-safe operator | yes | yes when it contains the relevant suffix interface | yes |

The exact two-qubit constructions in `COMPILER_BOUNDARIES.md` establish both
failed converses:

- a SWAP of two marker columns preserves the prepared Hopf state but moves the
  global response to the wrong coordinate;
- a checkpoint suffix can preserve its prepared state while flipping a decoded
  derivative from `2` to `-2`;
- a compiler equal on the full checkpoint interface can still change the full
  output distribution by total-variation distance `1/4` while preserving the
  decoded checkpoint mean.

## 9. Chart-native versus compiler-native ingredients

| Ingredient | Mathematical source |
|---|---|
| State and coordinate tangents | Hopf chart |
| Orthogonality and diagonal pullback metric | Hopf chart |
| Marker assignment | Chosen coherent frame completion |
| Shared Walsh record | Frame plus measurement design |
| Clean physical implementation | Compiler |
| Ancilla--depth tradeoff | Compiler theorem |
| Checkpoint interfaces | Particular circuit factorization |

The global method is chart-native but requires an efficient complete frame
implementation. The checkpoint method can tolerate arbitrary behavior outside
its active interface, but its valid interface is determined by a chosen circuit
factorization rather than by the final state chart alone.
