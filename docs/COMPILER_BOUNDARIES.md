# Compiler boundaries: state columns, global frames, and checkpoint interfaces

[← Complete narrative](../REVIEW.md) · [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) · [QBP consequence](QBP_CONSEQUENCE.md)

This page isolates four exact finite-dimensional statements:

1. a compiler may prepare the correct Hopf state while returning the wrong
   global coordinate gradient;
2. equality on a complete active checkpoint interface is sufficient for the
   designated checkpoint estimator means;
3. equality on only the prepared checkpoint state can still flip a derivative;
4. active-interface equality may preserve the decoded mean without preserving
   the complete output distribution.

These boundaries do not depend on asymptotic resource estimates. Their purpose
is to identify the operator contract that each reverse-mode protocol actually
uses.

## 1. Three different compiler contracts

Let $J$ append clean workspace:

```math
J|\varphi\rangle
=|\varphi\rangle|0^w\rangle.
```

Three contracts must not be conflated.

### State-column equality

For one prepared input state $\lvert \alpha\rangle$,

```math
\widetilde UJ|\alpha\rangle
=e^{i\chi}JU|\alpha\rangle.
```

This certifies one output state, up to a common phase. It places no useful
restriction on the orthogonal complement of $\lvert \alpha\rangle$.

### Checkpoint active-interface equality

For an active-interface projector $P$,

```math
\widetilde UJP
=e^{i\chi}JUP.
```

This certifies the complete isometry on every state that can appear at the
chosen checkpoint interface. The compiler remains arbitrary on the orthogonal
input sector.

### Full frame safety

For a complete differential-frame unitary $W$,

```math
\widetilde WJ=JW.
```

This certifies the complete system action on every clean-workspace input. It is
the natural substitution contract for the global-frame protocol.

The implications are strict:

```math
\text{full frame safety}
\Longrightarrow
\text{active-interface safety}
\Longrightarrow
\text{state-column equality},
```

while neither converse holds in general.

## 2. Two-qubit global state-column counterexample

This is the smallest Hopf example that can mix two distinct marker labels. A
one-qubit example can change the phase or sign of its only nonzero marker
column, but cannot display marker-to-marker reassignment.

Choose the regular real Hopf point

```math
\theta_1=\theta_2=\theta_3=\frac{\pi}{4}.
```

The state is

```math
|\psi\rangle
=\frac{|00\rangle+|01\rangle+|10\rangle+|11\rangle}{2}.
```

In computational-column order $0,1,2,3$, the canonical real Hopf frame is

```math
W=
\begin{pmatrix}
\tfrac12 & -\tfrac{1}{\sqrt2} & -\tfrac12 & 0\\
\tfrac12 &  \tfrac{1}{\sqrt2} & -\tfrac12 & 0\\
\tfrac12 & 0 & \tfrac12 & -\tfrac{1}{\sqrt2}\\
\tfrac12 & 0 & \tfrac12 &  \tfrac{1}{\sqrt2}
\end{pmatrix}.
```

The marker map is

```math
\lambda(1)=2,
\qquad
\lambda(2)=1,
\qquad
\lambda(3)=3,
```

and the metric square roots at this regular point are

```math
\bigl(1,2^{-1/2},2^{-1/2}\bigr).
```

Let $Q$ be the two-qubit SWAP matrix,

```math
Q|00\rangle=|00\rangle,
\qquad
Q|01\rangle=|10\rangle,
\qquad
Q|10\rangle=|01\rangle,
\qquad
Q|11\rangle=|11\rangle,
```

and define

```math
V=WQ.
```

Because $Q\lvert 00\rangle=\lvert 00\rangle$,

```math
V|00\rangle=W|00\rangle=|\psi\rangle.
```

Thus $V$ is an exact state-preparation replacement for this point, but not a
valid replacement for the Hopf differential frame.

Choose

```math
O=-Z\otimes I
=\mathrm{diag}(-1,-1,1,1).
```

At this point,

```math
O|\psi\rangle=W|10\rangle.
```

Consequently,

```math
W^\dagger O|\psi\rangle=|10\rangle,
```

whereas

```math
V^\dagger O|\psi\rangle
=Q^\dagger|10\rangle
=|01\rangle.
```

The response amplitude has moved from the root marker to the left-child marker.
The exact coordinate gradient is

```math
\nabla_{\boldsymbol\theta}E=(2,0,0).
```

The fixed Walsh-marker decoder returns this value with $W$, but with $V$ it
returns

```math
\widetilde\nabla_{\boldsymbol\theta}E
=(0,\sqrt2,0).
```

### Complete output distributions

Write one measured outcome as $(b,y)$, where $b$ is the ancilla X-basis bit and
$y$ the two-bit system X-basis label. The correct frame has probability $1/4$
on

```text
(0,00), (0,01), (1,10), (1,11),
```

and zero elsewhere. The state-equivalent compiler has probability $1/4$ on

```text
(0,00), (0,10), (1,01), (1,11),
```

and zero elsewhere. Their total-variation distance is $1/2$.

> **State-column equality is insufficient for global Hopf backpropagation.**
> There exist exact unitaries $V$ and $W$ with $V\lvert 0\rangle=W\lvert 0\rangle$ and a
> Hermitian-unitary observable $O$ for which the designated global marker
> decoder gives different gradients. An exact state-preparation compiler cannot
> therefore be inverted as a Hopf reverse frame without an additional
> operator-level contract.

## 3. Checkpoint notation

At depth $d$, write the designated preparation as

```math
U=B_dA_d,
```

where $A_d$ contains depths `0,...,d` and $B_d$ contains the later depths. Let

```math
|\alpha_d\rangle=A_d|0^n\rangle,
\qquad
|\psi\rangle=B_d|\alpha_d\rangle.
```

The active-interface projector is

```math
P_d
=I_{2^{d+1}}
\otimes
|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The prefix state satisfies

```math
P_d|\alpha_d\rangle=|\alpha_d\rangle.
```

For prefix label $r$, the checkpoint score uses an operator of the form

```math
K_{d,r}
=|r\rangle\!\langle r|
\otimes Y_{q_d}
\otimes I_{\mathrm{suffix}}.
```

It preserves the active-interface sectors:

```math
[K_{d,r},P_d]=0.
```

The physical score is the corresponding ancilla-system correlation, with the
repository convention $-2 Y_{\mathrm{ancilla}} \otimes K_{d,r}$.

## 4. Active-interface substitution theorem

Let $\widetilde B_d$ be a unitary compiler acting on system and clean workspace.
Assume that, for one phase $\chi$ independent of the active-interface input,

```math
\widetilde B_dJP_d
=e^{i\chi}JB_dP_d.
```

Use $\widetilde B_d$ consistently in the forward suffix and
$\widetilde B_d^{\dagger}$ after the controlled observable.

> **Checkpoint active-interface substitution.** Under the condition above,
> every designated checkpoint gradient estimator at depth $d$ has exactly the
> same expectation as under $B_d$, for every allowed controlled observable. The
> complete measurement distribution need not be the same.

### Proof

Taking the adjoint of the interface condition gives

```math
P_dJ^\dagger\widetilde B_d^\dagger
=e^{-i\chi}P_dB_d^\dagger J^\dagger.
```

The consistent compiled forward branch is

```math
\widetilde B_dJ|\alpha_d\rangle
=e^{i\chi}J|\psi\rangle.
```

After the controlled observable and compiled inverse, the two system-work
branches are

```math
|\beta_0\rangle=J|\alpha_d\rangle
```

and

```math
|\beta_1\rangle
=e^{i\chi}\widetilde B_d^\dagger JO|\psi\rangle.
```

Their active clean component obeys

```math
P_dJ^\dagger|\beta_1\rangle
=P_dB_d^\dagger O|\psi\rangle.
```

Every checkpoint score is an ancilla-off-diagonal correlation between
`beta_0` and `beta_1`. Since `beta_0` has clean workspace and lies in the range
of $P_d$, while each $K_{d,r}$ preserves that range, the score depends only on
this active clean component. It is therefore identical to the score produced by
$B_d$.

Components of `beta_1` outside the active clean sector are orthogonal to the
reference branch in the score correlation. They may nevertheless change
suffix-resolved probabilities and other observables. Equality of means does not
therefore imply equality of complete distributions.

### On minimality

For a fixed state, score family, and observable class, the condition can be
weakened to equality of only the relevant score matrix elements. Such a
condition depends on the particular checkpoint state and decoder and is not a
compositional compiler contract. Active-interface equality is the natural
objective-independent sufficient condition: it certifies the complete isometry
that the checkpoint can probe.

## 5. State-column-only checkpoint failure

Use two qubits, checkpoint depth $d=0$, and again set all three Hopf angles to
$\pi/4$. The checkpoint factors are

```math
A=R_y(\pi/4)\otimes I,
\qquad
B=I\otimes R_y(\pi/4).
```

The prefix and final states are

```math
|\alpha\rangle=A|00\rangle=|+0\rangle,
\qquad
|\psi\rangle=B|\alpha\rangle=|++\rangle.
```

The active interface is

```math
P=I\otimes|0\rangle\!\langle0|.
```

Let

```math
Q_{\mathrm{bad}}=X\otimes I,
\qquad
C_{\mathrm{bad}}=BQ_{\mathrm{bad}}.
```

Because $X\lvert +\rangle=\lvert +\rangle$,

```math
C_{\mathrm{bad}}|\alpha\rangle
=B|\alpha\rangle
=|\psi\rangle.
```

The complete prepared state is correct, but

```math
C_{\mathrm{bad}}P\neq BP.
```

The compiler fixes only the actual prefix state, not the complete checkpoint
interface.

Choose

```math
O=-Z\otimes I.
```

The exact root derivative is $2$. Under the designated inverse suffix, the two
checkpoint branches before Y-basis readout are the prefix state and its root
coordinate direction. The nonzero measured outcomes are

```text
correct B:      (ancilla,target,suffix) = (0,1,0), (1,0,0), each 1/2;
compiled C_bad: (ancilla,target,suffix) = (0,0,0), (1,1,0), each 1/2.
```

The checkpoint decoder therefore returns $2$ with $B$, but $-2$ with
$C_{\mathrm{bad}}$.

> **Checkpoint state-column equality is insufficient.** A recompiled suffix may
> preserve the exact final prepared state while changing a checkpoint
> derivative, even when the same suffix is used in the forward and reverse
> directions. The missing condition is preservation of the complete active
> interface, not merely its one prepared vector.

## 6. Interface safety preserves means, not full distributions

Keep the same $A$, $B$, and $P$, but define

```math
Q_\perp=\mathrm{diag}(1,1,1,i),
\qquad
C_{\mathrm{safe}}=BQ_\perp.
```

Since $Q_{\perp} P=P$,

```math
C_{\mathrm{safe}}P=BP.
```

Thus the complete active-interface contract holds exactly. The two suffix
unitaries still differ outside the interface.

Choose

```math
O=I\otimes Z.
```

The depth-zero checkpoint derivative is zero. Both suffixes decode exactly zero,
as required. Their complete distributions differ:

- the reference distribution is uniform over all eight ancilla-system outcomes;
- the compiled distribution, in ancilla-major order, is

```math
\left(
\tfrac18,0,\tfrac18,\tfrac14,
\tfrac18,0,\tfrac18,\tfrac14
\right).
```

The total-variation distance is $1/4$.

This establishes the precise boundary:

```math
\text{active-interface equality}
\Longrightarrow
\text{checkpoint mean equality},
```

but not

```math
\text{active-interface equality}
\Longrightarrow
\text{complete distribution equality}.
```

## 7. Consequences

| Protocol | Natural sufficient contract | What state-column equality misses |
|---|---|---|
| Global differential frame | complete frame-safe operator action | marker columns can be permuted, phased, or mixed |
| Checkpoint reverse sweep | suffix isometry on the active checkpoint interface | one prepared prefix vector does not determine the remaining interface directions |
| Scalar objective | one initialized state column | no derivative interface is required |

The global method is chart-native but frame-implementation conditional. The
checkpoint method is factorization- and interface-dependent. It can tolerate
more freedom than the global frame because behavior outside $P_d$ is irrelevant
to its means, but it cannot be inferred from final-state preparation alone.

## 8. Executable support

- [Boundary constructions](../compiler_robust_hopf/compiler_boundaries.py)
- [Magnitude decoders](../compiler_robust_hopf/decoders.py)
- [Exact boundary tests](../tests/test_compiler_boundaries.py)

Run the complete suite with

```bash
python validate.py
```

The deterministic tests verify the operator identities, exact distributions,
analytic gradients, decoded gradients, interface residuals, and total-variation
distances stated above.

---

[← Complete narrative](../REVIEW.md) · [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) · [QBP consequence](QBP_CONSEQUENCE.md)
