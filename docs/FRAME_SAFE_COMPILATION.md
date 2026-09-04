# Frame-safe compilation

[← Hopf interface](HOPF_INTERFACE.md) · [Complete narrative](../REVIEW.md) · [Compiler boundaries →](COMPILER_BOUNDARIES.md)

This page isolates the operator contract connecting the compiler theorem to the
inverse-frame gradient circuit.

## 1. Three different promises

A state-preparation circuit fixes one initialized input:

```math
U_{\mathrm{prep}}|0^n\rangle=|\psi\rangle.
```

The Hopf differential frame fixes additional columns:

```math
W|0^n\rangle=|\psi\rangle,
\qquad
W|\lambda(j)\rangle=|e_j\rangle.
```

A checkpoint protocol lies between these two extremes: it needs a compiled
suffix to agree on the complete interface actually reached by the retained
prefix circuit.

| Promise | Prescribed input space |
|---|---|
| state-column equality | one initialized vector |
| checkpoint active-interface equality | one factorization-dependent subspace |
| frame safety | the complete system space with clean workspace |

The three promises support different reverse protocols and should not be
interchanged.

## 2. State-column equality leaves a free completion

Suppose

```math
V|0^n\rangle=W|0^n\rangle=|\psi\rangle.
```

Then one may write

```math
V=WQ,
\qquad
Q|0^n\rangle=|0^n\rangle,
```

with no corresponding restriction on $Q$ over the orthogonal complement.  The
response resolved by the inverse becomes

```math
V^{\dagger}O|\psi\rangle
=Q^{\dagger}W^{\dagger}O|\psi\rangle.
```

Thus the free completion can mix the marker amplitudes read by the gradient
decoder.  The exact two-qubit construction in
[`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md) exhibits this effect without
an asymptotic argument.

## 3. Complete clean-input contract

Let

```math
J_m|\varphi\rangle
=|\varphi\rangle|0^m\rangle
```

append $m$ clean workspace qubits.

### Definition 1: frame-safe implementation

A unitary $\widetilde W$ is frame-safe for $W$ when

```math
\boxed{
\widetilde WJ_m=J_mW.
}
```

Equivalently, for every system state,

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle.
```

The contract does not prescribe the action when the compiler workspace begins
outside $\lvert 0^m\rangle$.

### Lemma 2: inverse frame safety

If $\widetilde W$ is unitary and frame-safe, then

```math
\boxed{
\widetilde W^{\dagger}J_m
=J_mW^{\dagger}.
}
```

#### Proof

Let

```math
P_0=J_mJ_m^{\dagger}
=I\otimes|0^m\rangle\!\langle0^m|.
```

The relation $\widetilde W J_m=J_m W$ maps the range of $P_0$ unitarily onto itself.
Because $\widetilde W$ is unitary, that subspace is reducing.  Hence both
$\widetilde W$ and $\widetilde W^{\dagger}$ preserve it, and the restriction of the adjoint is
the adjoint of the restriction.  ∎

This argument is stronger than taking the adjoint of a first-column equality.

## 4. Substitution in the global gradient circuit

### Theorem 3: global frame-safe substitution

Replace a logical frame $W$ or inverse frame $W^{\dagger}$ by a frame-safe compiled
implementation or its adjoint.  Initialize its work register in $\lvert 0^m\rangle$ and do
not couple unrelated operations to that register while the compiled block is
active.  Then the output on all original protocol registers is unchanged, and
the compiler workspace returns to $\lvert 0^m\rangle$.

Consequently, compilation preserves:

- the complete measurement distribution;
- every decoded raw-coordinate mean;
- the almost-sure record-norm bounds;
- the finite-shot concentration statement;
- the classical decoding routes.

#### Proof

The forward statement is Definition 1, including when the system is entangled
with untouched registers.  The inverse statement is Lemma 2.  Applying these
identities to each frame block leaves the complete protocol state unchanged up
to a tensor factor $\lvert 0^m\rangle$.  ∎

## 5. Sequential reuse of one workspace pool

Suppose $\widetilde U$ and $\widetilde V$ frame-safely implement $U$ and $V$ using at most
$a$ and $b$ clean qubits.  Embed them in one pool of

```math
m=\max\{a,b\}
```

qubits.  Since the first block returns the pool clean,

```math
\widetilde V\widetilde U
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(VU|\varphi\rangle)|0^m\rangle.
```

Workspace therefore takes a maximum across sequential blocks, while size and
depth add.  This is the register-level reason that $W_{\mathbb R}$ and $D_{\mathrm{ph}}$ reuse one
pool in

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

## 6. What a frame-safe compiler may change

The compiler may change:

- elementary angles and their classical preprocessing;
- gate ordering and intermediate encodings;
- the number and layout of clean work qubits;
- size and depth constants;
- a later hardware-routing realization.

It may not change:

- the complete logical system action on clean workspace input;
- the designated marker columns;
- the relative phase convention used by the interference circuit;
- the declared controlled-observable interface.

One Hopf coordinate need not remain one physical gate angle.  The Möttönen-style
compiler already demonstrates this: compiler-generated multiplexor angles
replace the coordinate angles while the complete frame is preserved.

## 7. Resource inheritance

Logical equivalence alone does not establish backpropagation scaling.  Let

```math
C_{\mathrm{prep}}(n,m)
```

be the matched state-preparation cost and

```math
C_{\mathrm{frame}}(n,m)
```

the frame-safe cost in the same model.  The compiler result must compare size,
depth, and workspace separately.

The all-workspace theorem proves the sharp relations

```math
S_{\mathrm{frame}}(n,m)=\Theta(S_{\mathrm{prep}}(n,m))
```

and

```math
D_{\mathrm{frame}}(n,m)=\Theta(D_{\mathrm{prep}}(n,m))
```

for the general state family.  Executions, controlled-observable depth,
classical decoding, and output materialization remain separate end-to-end
resources.

## 8. Checkpoint active-interface contract

Write one preparation as

```math
U=B_dA_d,
```

and let $P_d$ project onto the active interface reached by $A_d$.

### Definition 4: active-interface-safe suffix

A compiled suffix $\widetilde B_d$ is active-interface safe when

```math
\widetilde B_dJ_mP_d
=e^{i\chi}J_mB_dP_d,
```

where $\chi$ is independent of the interface input.

This is weaker than complete frame safety because no action is prescribed on
the orthogonal input sector.  It is stronger than preserving only the single
state $A_d\lvert 0^n\rangle$.

### Theorem 5: checkpoint substitution

Use an active-interface-safe suffix consistently in the forward and reverse
checkpoint circuit.  Then every designated checkpoint estimator at depth $d$
has the same expectation as under the original suffix for every allowed
controlled observable.  The complete output distribution need not be the same.

The reference branch lies in $P_d$, and the checkpoint score operators preserve
$P_d$.  The adjoint of the interface identity therefore preserves exactly the
component entering the estimator mean.  The complete proof and separating
examples are given in [`COMPILER_BOUNDARIES.md`](COMPILER_BOUNDARIES.md).

## 9. Strict hierarchy

| Promise | Scalar state | Checkpoint means | Global-frame distribution |
|---|---:|---:|---:|
| one state column | sufficient | insufficient | insufficient |
| complete active checkpoint interface | sufficient | sufficient | generally insufficient |
| complete frame-safe action | sufficient | sufficient where applicable | sufficient |

This hierarchy identifies the contract before any resource comparison is made.
The all-workspace theorem addresses the strongest row.

---

[← Hopf interface](HOPF_INTERFACE.md) · [Complete narrative](../REVIEW.md) · [Compiler boundaries →](COMPILER_BOUNDARIES.md)
