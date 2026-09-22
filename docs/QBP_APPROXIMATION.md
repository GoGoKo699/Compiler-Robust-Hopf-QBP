# Approximate frame compilation in the raw-gradient protocol

[← QBP consequence](QBP_CONSEQUENCE.md) · [Frame-safe interface](FRAME_SAFE_COMPILATION.md)

At a **fixed parameter tuple**, a full initialized-isometry error bound for the
prescribed frame controls the actual gradient measurement. Approximate work may
remain coherent until the final measurement. No derivative of a compiled gate
word is needed.

For the shared forward circuit and its actual adjoint, the magnitude stream
satisfies

```math
\boxed{\left|\mathbb E_{\rm actual}Z_j-\partial_{\theta_j}E_O\right|
\leq 4|a_j|(\eta+\eta_O)\leq4(\eta+\eta_O).}
```

Here $\eta$ is the full frame-isometry error, $\eta_O$ is the error of one
phase-calibrated controlled-observable application, and the raw score is
$Z_j=2a_j(-1)^{b+\lambda(j)\cdot y}$. This concerns the specified measurement
protocol; it is not an optimal gradient-query theorem.

## 1. The input and workspace contract

Let $S$ be the system, $C$ the initialized frame work, and $D$ any dirty bank.
The dirty input can be entangled with an arbitrary external reference $R$.
Write $W_D=W\otimes I_D$, and let $J$ append $|0\rangle_C$ to an arbitrary
input on $SD$. The compiler supplies an actual unitary $V$ such that

```math
\|VJ-JW_D\|_{\rm op}\leq\eta.                 \tag{1}
```

This is an operator-norm bound on **every** input of $SD$, not only the state
column $|0^n\rangle$. Tensoring (1) with $I_R$ leaves its norm unchanged, so the
same bound holds for dirty inputs entangled with a reference. Mixed inputs
follow by purification or convexity. Any exact dirty-bank restoration promised
by the compiler remains a separate implementation requirement; it is not
inferred from a nonzero tolerance in (1).

Equation (1) includes amplitude outside the clean-work subspace. A bound only
on $J^\dagger VJ-W_D$ is insufficient: this projected block may have a
quadratically smaller error than the omitted leakage. Work is neither measured,
postselected nor reset between the forward and reverse circuits.

The observable is a Hermitian unitary $O$, with ideal controlled action

```math
\mathcal O=|0\rangle\!\langle0|_B\otimes I+
|1\rangle\!\langle1|_B\otimes O.
```

Its implementation
$\widetilde{\mathcal O}$ has full initialized-isometry error at most
$\eta_O$ against $\mathcal O$. This includes the relative phase of the two
branches and the observable's own work. Its approximate work is disjoint from
$C$; exactly returned scratch may be reused where its all-input contract
permits. The oracle bound must hold on arbitrary branch-system inputs and
external references, including the frame's coherent work. An error bound for
an uncontrolled $O$ only up to global phase is not this contract.

## 2. The actual adjoint has the same error

The exact identity

```math
V^\dagger J-JW_D^\dagger
=V^\dagger(JW_D-VJ)W_D^\dagger
```

implies

```math
\|V^\dagger J-JW_D^\dagger\|_{\rm op}
=\|VJ-JW_D\|_{\rm op}\leq\eta.              \tag{2}
```

Both outer factors are unitary. This proves the inverse guarantee for the
**reversed actual circuit**, including all its work registers. It does not say
that $V^\dagger$ approximates $W_D^\dagger$ on arbitrary nonzero-work inputs.
That stronger assertion is unnecessary: unitary hybrid estimates propagate
any earlier leakage without assuming it has been reset.

## 3. Full output and the shared-circuit cancellation

Fix a purification $|\xi\rangle_{DR}$ of the dirty/reference input. Let
$|u\rangle=|0^n\rangle_S|\xi\rangle_{DR}$ and extend all operations by the
identity on unused registers, suppressing $R$ in operator subscripts. With the
ideal controlled observable, the actual premeasurement state is

```math
|\chi_V\rangle
=\frac{|0\rangle_BJ|u\rangle
      +|1\rangle_B V^\dagger(O\otimes I_{CDR})VJ|u\rangle}{\sqrt2}.
```

The first branch is exactly $V^\dagger VJ|u\rangle=J|u\rangle$.
In the response branch, add and subtract the ideal initialized intermediate:

```math
\begin{aligned}
&V^\dagger(O\otimes I)VJ-JW_D^\dagger O_DW_D\\
&\quad=V^\dagger(O\otimes I)(VJ-JW_D)
 +(V^\dagger J-JW_D^\dagger)O_DW_D,
\end{aligned}
```

where $O_D=O\otimes I_D$. Both terms have norm at most $\eta$ by (1)–(2).
Consequently the complete response error is at most $2\eta$, and

```math
\||\chi_V\rangle-|\chi_W\rangle\|\leq\sqrt2\,\eta.
```

Replacing the controlled observable by its actual implementation adds at most
$\eta_O$. The subsequent actual inverse is unitary and cannot increase that
error, even when the oracle's work leaks. Thus the full premeasurement state,
including all retained work and the reference, obeys

```math
\delta_{\rm out}\leq\sqrt2\,\eta+\eta_O.       \tag{3}
```

The total-variation distance of the observed $(b,y)$ distributions is at most
$`\min\{1,\delta_{\rm out}\}`$. Tracing work and measuring cannot increase
trace distance. Equation (3) is a complete-output guarantee, not a comparison
of projected response amplitudes alone.

## 4. Raw-coordinate bias

Measuring the branch and system in the X basis makes the score observable

```math
A_j=2a_jX_B\otimes X_S^{\lambda(j)}\otimes I_{CDR},
\qquad \|A_j\|=2|a_j|\leq2.
```

For the ideal controlled observable, the exact reference branch gives

```math
\mathbb E_V Z_j
=2a_j\,\mathrm{Re}
\langle J(\lambda(j),\xi)|
 V^\dagger(O\otimes I)VJ|0,\xi\rangle.
```

The response error just proved is at most $2\eta$, so

```math
|\mathbb E_VZ_j-\partial_{\theta_j}E_O|
\leq4|a_j|\eta.                              \tag{4}
```

This use of a projected amplitude is justified by the actual complete branch
state. It does not replace the full-isometry premise.

For normalized states $|x\rangle,|z\rangle$ and any bounded observable $A$,

```math
|\langle x|A|x\rangle-\langle z|A|z\rangle|
\leq2\|A\|\,\||x\rangle-|z\rangle\|.
```

Apply this to the change caused by the approximate controlled observable.
Its contribution is at most $4|a_j|\eta_O$. Adding (4) proves the displayed
$4|a_j|(\eta+\eta_O)$ bound. A singular raw coordinate with $a_j=0$ remains
exactly zero as a decoded record. No inverse metric weight appears.

The sharper constant in (4) uses the shared $V,V^\dagger$ pair and the Walsh
score. Applying only the general bounded-observable estimate to (3) gives the
valid but weaker $4|a_j|(\sqrt2\eta+\eta_O)$ bound.

## 5. Precision allocation preserves the sampling order

The classical tuple and oriented weights $a_j$ are fixed and known here.
Errors in classical weights, parity decoding or readout labels require their
own budgets. At each tree depth $d$,

```math
\sum_{j\text{ at depth }d}a_j^2=1,
\qquad \|Z^{(d)}\|_2=2
```

for every possible outcome. This deterministic norm remains true under the
actual, possibly biased measurement distribution. Independent repetitions
therefore concentrate about the **actual** mean with the same sufficient
sample order as in the exact protocol.

For completeness, if $\overline Z^{(d)}$ is a mean of $S$ independent depth
records with mean $\mu^{(d)}$, then
$`\mathbb E\|\overline Z^{(d)}-\mu^{(d)}\|_2\leq2/\sqrt S`$.
Changing one record changes this norm by at most $4/S$. McDiarmid's inequality
and a union bound over the $n$ depths give simultaneous depthwise error at
most $\varepsilon_{\rm stat}$ when, for example,

```math
S\geq\frac{32[1+\ln(n/\delta)]}{\varepsilon_{\rm stat}^2}.
```

Each coordinate error is at most its depth-vector error. Choose

```math
\eta\leq\varepsilon_\infty/16,\qquad
\eta_O\leq\varepsilon_\infty/16,\qquad
\varepsilon_{\rm stat}=\varepsilon_\infty/2.
```

The bias is at most $\varepsilon_\infty/2$, and with probability at least
$1-\delta$,

```math
\|\widehat{\nabla E_O}-\nabla E_O\|_\infty\leq\varepsilon_\infty,
\qquad
S=O\!\left(\varepsilon_\infty^{-2}[1+\log(n/\delta)]\right).
```

A sufficient synthesis precision is therefore
$L=\Theta(1+\log(1/\varepsilon_\infty))$, independently of the number of
coordinates. If a chosen synthesis theorem assumes error at most $1/64$, take
$`L=\max\{6,\lceil\log_2(16/\varepsilon_\infty)\rceil\}`$ for each of the two
allocated errors. This specifies an accuracy requirement; it does not itself
supply an elementary Clifford+T compiler or an optimal T-count theorem.

## 6. Parameter derivatives and complex coordinates

All statements compare a fixed ideal $W(\theta)$ and its actual compiled
circuit at that same tuple. They estimate the derivative of the ideal chart's
energy through its known frame identity. They do **not** differentiate the
compiled word. Uniformly close unitary families need not have close parameter
derivatives, and synthesized words can change discontinuously with the tuple.
A parameter update requires its own applicable fixed-tuple guarantee.

For complex magnitude coordinates, use the full phase-dressed frame
$W_{\mathbb C,\mathrm{mag}}=D_{\rm ph}W_{\mathbb R}$ in (1). The proof above
then applies unchanged. Leaf-phase coordinates use their separate direct
signed one-hot stream; they are not additional columns of this frame. This
page does not transfer the frame-specific cancellation to that different
circuit without a separate preparation/oracle analysis. Its bounded-record
method can be applied once those actual circuit contracts are specified.

The result preserves the raw-gradient sampling guarantee of this protocol.
It does not establish optimal gradient-query complexity, the best gradient
algorithm, a natural-gradient guarantee, a hardware noise threshold, or an
end-to-end advantage over state-only shadow methods or classical differentiation.

## 7. Executable evidence

[Approximation-contract tests](../tests/test_approximation_contract.py) use the
repository's two-qubit frames and decoders. They check the actual adjoint,
coherent work leakage, a dirty bank entangled with a reference, a controlled
observable phase error, and complete output distributions. Adversarial controls
show that exact state-column agreement is insufficient and that projected
clean-block error can underestimate the full-isometry error. These finite
floating-point tests support the interface identities; the inequalities above
are analytic proofs.


## 8. Per-execution and complete-gradient T costs

For the real magnitude protocol, let $t_F$ be the T-count of the chosen actual
frame circuit $V$ at error $\eta$, and let $t_O$ be that of the calibrated
controlled observable at error $\eta_O$. The same $V$ prepares the state and
its actual adjoint resolves the response. Clifford interference and readout
add no T gates. Thus

```math
\mathcal T_{\nabla}\leq S(2t_F+t_O).
```

Let $a_F$ and $b_F$ be the clean and dirty budgets assigned to the frame
compiler. Reserve one additional clean interference qubit and any separately
needed observable work before assigning $a_F$. With $q_F=n+a_F+b_F$ and the
hypotheses of the [fault-tolerant theorem](FAULT_TOLERANT_COMPILER.md),

```math
\mathcal T_{\nabla}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\left[\sqrt{NL}+L+\frac{NL}{q_F}+t_O\right]
\right).
```

Here $L$ is chosen by the precision allocation above, and the sufficient frame
reservation is $a_F\geq C(n+h)$. The companion Clifford upper bound is
$O(S(NL+g_O+n))$, where $g_O$ is the controlled-observable Clifford count.
Classical weight preparation, decoding, and materializing the full gradient
remain separately charged. This is an upper bound for the specified real
inverse-frame protocol. Its frame-synthesis optimality is not a lower bound on
all possible gradient algorithms, and the complex leaf-phase stream has not
been folded into this formula.
