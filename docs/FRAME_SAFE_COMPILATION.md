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
outside $\lvert0^m\rangle$.

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

The relation $\widetilde WJ_m=J_mW$ maps the range of $P_0$ unitarily onto itself.
Because $\widetilde W$ is unitary, that subspace is reducing.  Hence both
$\widetilde W$ and $\widetilde W^{\dagger}$ preserve it, and the restriction of the adjoint is
the adjoint of the restriction.  ∎

This argument is stronger than taking the adjoint of a first-column equality.

## 4. Substitution in the global gradient circuit

### Theorem 3: global frame-safe substitution

Replace a logical frame $W$ or inverse frame $W^{\dagger}$ by a frame-safe compiled
implementation or its adjoint.  Initialize its work register in $\lvert0^m\rangle$ and do
not couple unrelated operations to that register while the compiled block is
active.  Then the output on all original protocol registers is unchanged, and
the compiler workspace returns to $\lvert0^m\rangle$.

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
to a tensor factor $\lvert0^m\rangle$.  ∎

### Necessity for all observable-dependent gradient means

The complete-frame contract can also be recovered from the designated gradient
means themselves. Fix a Hopf parameter tuple, write
$|\psi\rangle=W|0^n\rangle$ and $|e_j\rangle=W|\lambda(j)\rangle$, and let
$a_j$ be the real oriented incoming amplitude. Allow a unitary compiler
$\widetilde V$ with clean-input embedding $J=J_m$ whose prepared state is exact:

```math
\widetilde VJ|0^n\rangle=e^{i\chi}J|\psi\rangle.
```

The same compiler and its adjoint are used in the forward and reverse blocks.
Define its phase-aligned projected marker and marker error by

```math
|v_j\rangle=e^{-i\chi}J^\dagger\widetilde VJ|\lambda(j)\rangle,
\qquad
|d_j\rangle=|v_j\rangle-|e_j\rangle.
```

No clean return is assumed for the other input columns. Orthogonality of the
compiled state and marker columns gives $\langle\psi|v_j\rangle=0$, and
projection gives $`\|v_j\|\leq1`$. The fixed marker decoder has mean

```math
\mu_j(\widetilde V,O)
=2a_j\mathrm{Re}\langle v_j|O|\psi\rangle
```

for a Hermitian-unitary system observable $O$. This follows by taking the
interference between the reference branch $J|0^n\rangle$ and the reverse
branch $e^{i\chi}\widetilde V^\dagger JO|\psi\rangle$; workspace components
orthogonal to the clean reference do not contribute to this correlation.

**Proposition: exact worst-observable sensitivity.**

```math
\sup_{O=O^\dagger,\ O^2=I}
|\mu_j(\widetilde V,O)-\mu_j(W,O)|
=2|a_j|\,\|d_j\|.
```

The upper bound is Cauchy–Schwarz. If $d_j\neq0$, put
$`|z\rangle=|d_j\rangle/\|d_j\|`$. Since $z$ is orthogonal to $\psi$, the operator

```math
O_z=|z\rangle\!\langle\psi|+|\psi\rangle\!\langle z|
    +I-|\psi\rangle\!\langle\psi|-|z\rangle\!\langle z|
```

is Hermitian and unitary and sends $\psi$ to $z$. It attains the stated bound.
When $d_j=0$, the equality is immediate.

At a regular point, where every $a_j\neq0$, equality of every designated
gradient mean for every allowed observable forces $v_j=e_j$ for all markers.
Each projected marker then has unit norm, so the corresponding compiled
column has no workspace leakage. Together with the prepared-state column,
this proves

```math
\widetilde VJ=e^{i\chi}JW.
```

Thus complete frame safety, up to one common phase, is necessary and sufficient
for universal preservation of the designated means under the exact
prepared-state assumption. Under the literal phase convention $\chi=0$, this
is Definition 1. Consistent forward–inverse use cannot identify a common
phase, so the mean condition alone does not enforce that phase convention.
For exact equality it suffices to consider all Hermitian Pauli words: they
span the Hermitian operators, and the mean difference is linear in $O$.

The converse has two important boundaries. At a singular coordinate $a_j=0$,
the raw mean is zero for every observable and does not identify that marker
column. For one fixed observable, equality of the means likewise need not
determine the frame.

The quantitative statement also distinguishes projected marker error from
workspace leakage. If the left side of the sensitivity formula is at most
$\varepsilon$ and $a_j\neq0$, then

```math
\|d_j\|\leq\frac{\varepsilon}{2|a_j|},
\qquad
\left\|e^{-i\chi}\widetilde VJ|\lambda(j)\rangle-J|e_j\rangle\right\|
\leq\sqrt{\frac{\varepsilon}{|a_j|}}.
```

For the second bound, the squared column distance is
$`2-2\mathrm{Re}\langle e_j|v_j\rangle\leq2\|d_j\|`$.
Without workspace leakage, the column distance equals $`\|d_j\|`$ instead.
The factors involving $a_j$ explain why accurate raw means near a singular
coordinate do not certify a comparably accurate complete frame. Finite checks
in [`test_compiler_boundaries.py`](../tests/test_compiler_boundaries.py)
exercise complex marker phases, common-phase cancellation, and workspace
leakage through the actual probability decoder.

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
state $A_d\lvert0^n\rangle$.

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
