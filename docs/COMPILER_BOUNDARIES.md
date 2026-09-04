# Compiler boundaries: state columns, active interfaces, and complete frames

[← Frame-safe compilation](FRAME_SAFE_COMPILATION.md) · [Complete technical note](../REVIEW.md) · [QBP consequence →](QBP_CONSEQUENCE.md)

This page collects four exact finite-dimensional statements. Their purpose is
to identify the operator promise required by each reverse circuit before any
asymptotic resource theorem is invoked.

1. one correct state column need not preserve the global Hopf gradient;
2. one correct checkpoint state need not preserve a selected derivative;
3. equality on the complete active checkpoint interface is sufficient for the
   designated checkpoint means;
4. active-interface equality may preserve those means without preserving the
   complete output distribution.

## 1. Global frame: the first-column obstruction

### 1.1 Canonical two-qubit frame

Take

```math
\theta_1=\theta_2=\theta_3=\frac{\pi}{4}.
```

The real Hopf state is

```math
|\psi\rangle
=\frac{|00\rangle+|01\rangle+|10\rangle+|11\rangle}{2}.
```

The computational markers are

```math
\lambda(1)=10_2,
\qquad
\lambda(2)=01_2,
\qquad
\lambda(3)=11_2.
```

The complete frame in computational column order is

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

### 1.2 A preparation-equivalent completion

Let `Q` exchange the computational inputs `|01>` and `|10>` while fixing
`|00>` and `|11>`, and define

```math
V=W_{\mathbb R}Q.
```

Since `Q|00>=|00>`,

```math
V|00\rangle=W_{\mathbb R}|00\rangle=|\psi\rangle.
```

Thus `V` and `W_R` are exact state-preparation completions for the same target
state. They differ only by exchanging the marker columns associated with
`e_1` and `e_2`.

Choose

```math
O=-Z\otimes I.
```

Then

```math
W_{\mathbb R}^{\dagger}O|\psi\rangle=|10\rangle,
```

while

```math
V^{\dagger}O|\psi\rangle=|01\rangle.
```

The unchanged marker decoder returns

```math
(2,0,0)
```

for the Hopf frame and

```math
(0,\sqrt2,0)
```

for the preparation-equivalent completion.

<p align="center">
  <img src="../assets/two-qubit-obstruction.svg" width="900" alt="Two exact preparation completions share the same state column but place the response on different Hopf marker columns." />
</p>

Therefore

```math
\boxed{
V|0^n\rangle=W|0^n\rangle
\not\Rightarrow
\text{valid global inverse-frame decoding}.
}
```

The failure is exact and appears before any approximation, hardware routing, or
noise is introduced.

## 2. Checkpoint suffix: one correct state is still insufficient

A checkpoint circuit reverses only a suffix below one selected tree depth. The
same first-column issue reappears on the suffix interface.

Consider the one-qubit Hopf rotation

```math
R_y(\theta)
=
\begin{pmatrix}
\cos\theta&-\sin\theta\\
\sin\theta& \cos\theta
\end{pmatrix}.
```

The prepared state is

```math
|\psi(\theta)\rangle
=R_y(\theta)|0\rangle.
```

Let

```math
Z_\psi
=2|\psi\rangle\!\langle\psi|-I
```

be the reflection that fixes the prepared state and negates its orthogonal
complement. Define the alternative suffix

```math
\widetilde R_y(\theta)
=R_y(\theta)Z.
```

Both suffixes prepare the same state from `|0>`:

```math
\widetilde R_y(\theta)|0\rangle
=R_y(\theta)|0\rangle.
```

Their action on the derivative input differs by a sign:

```math
\widetilde R_y(\theta)|1\rangle
=-R_y(\theta)|1\rangle.
```

A checkpoint estimator whose interference term resolves that derivative can
therefore change sign even though the checkpoint state itself is exact.

```math
\boxed{
\text{one prepared checkpoint state}
\not\Rightarrow
\text{correct checkpoint derivative}.
}
```

## 3. Active-interface equality is sufficient for checkpoint means

Factor a logical preparation as

```math
U=B_dA_d,
```

where `A_d` prepares the prefix and `B_d` is the suffix reversed by the
checkpoint experiment. Let `P_d` project onto the complete subspace that can
enter `B_d` in the forward and response branches of that experiment.

Let `J` append clean compiler workspace. A sufficient compiled-suffix condition
is

```math
\boxed{
\widetilde B_dJP_d
=e^{i\chi}JB_dP_d,
}
```

where `chi` is independent of the vector in the active interface.

If the compiled suffix is used consistently in the forward and reverse
branches, the common phase cancels from the designated interference mean. All
logical vectors entering the suffix remain within the subspace on which the two
operators agree. The checkpoint mean is therefore unchanged.

This is the natural middle contract:

- stronger than preserving one state;
- weaker than implementing the complete global frame;
- tailored to the actual active subspace of the checkpoint experiment.

## 4. Mean preservation does not imply distribution preservation

The active-interface theorem fixes the interference quantity used by the
checkpoint decoder. It need not fix every output amplitude outside the measured
observable.

The repository includes a two-qubit example in which an alternative suffix
agrees with the logical suffix on the complete active interface up to one common
phase. The decoded checkpoint mean is unchanged, but the alternative completion
acts differently on an orthogonal sector. A measurement resolving that sector
can distinguish the full output distributions.

Thus

```math
\boxed{
\text{active-interface equality preserves the designated mean,}
}
```

```math
\boxed{
\text{but not necessarily the complete distribution.}
}
```

The global frame-safe contract is stronger precisely because the global record
uses the complete frame action and its full output distribution.

## 5. Contract hierarchy

| Compiler promise | Exact state preparation | Checkpoint means | Global Hopf distribution |
|---|---:|---:|---:|
| one prepared column | yes | no in general | no |
| complete active checkpoint interface | yes | yes for the designated interface | no in general |
| complete frame-safe action | yes | yes where applicable | yes |

The relevant promise is determined by the operator actually consumed by the
algorithm, not by the name of the elementary compiler.

## 6. Clean workspace

All three promises can be stated with clean work qubits. For complete frame
safety,

```math
\widetilde WJ=JW
```

implies

```math
\widetilde W^{\dagger}J=JW^{\dagger}
```

because the clean-workspace subspace is reducing. For checkpoint interfaces,
the same reasoning applies after restriction to the active subspace, provided
the forward and reverse uses are consistent and the interface phase is common.

Residual workspace entanglement would invalidate these conclusions even if the
logical system state looked correct after tracing out the work register.

## 7. Executable support

- [Boundary constructions](../compiler_robust_hopf/compiler_boundaries.py)
- [Exact tests](../tests/test_compiler_boundaries.py)
- [Frame-safe substitution theorem](FRAME_SAFE_COMPILATION.md)
- [QBP consequence](QBP_CONSEQUENCE.md)

The tests verify the state columns, complete unitaries, response states, decoded
gradients, checkpoint signs, active-interface means, and distinguishable output
distributions. The general operator implications are the subspace arguments
above.

---

[← Frame-safe compilation](FRAME_SAFE_COMPILATION.md) · [Complete technical note](../REVIEW.md) · [QBP consequence →](QBP_CONSEQUENCE.md)
