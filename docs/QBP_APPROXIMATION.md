# Approximate frame compilation in the raw-gradient protocol

[← QBP consequence](QBP_CONSEQUENCE.md) · [Frame-safe interface](FRAME_SAFE_COMPILATION.md)

At a **fixed parameter tuple**, a full initialized-isometry error bound for the
prescribed frame controls the actual gradient measurement. Approximate work may
remain coherent until the final measurement. No derivative of a compiled gate
word is needed. The [two-clean operator-source compilers](OPERATOR_SOURCE_COMPILER.md)
now meet this same contract for both the real frame and its phase-dressed
complex magnitude extension, under their explicit dirty-workspace budgets.
Their different gate counts do not change the bias argument below.

For the shared forward circuit and its actual adjoint, the magnitude stream
satisfies

```math
\boxed{\left|\mathbb E_{\rm actual}Z_j-\partial_{\theta_j}E_O\right|
\leq 4|a_j|(\eta+\eta_O)\leq4(\eta+\eta_O).}
```

Here $`\eta`$ is the full frame-isometry error, $`\eta_O`$ is the error of one
phase-calibrated controlled-observable application, and the raw score is
$`Z_j=2a_j(-1)^{b+\lambda(j)\cdot y}`$. This concerns the specified measurement
protocol; it is not an optimal gradient-query theorem.

## 1. The input and workspace contract

Let $`S`$ be the system, $`C`$ the initialized frame work, and $`D`$ any dirty bank.
The dirty input can be entangled with an arbitrary external reference $`R`$.
Write $`W_D=W\otimes I_D`$, and let $`J`$ append $`|0\rangle_C`$ to an arbitrary
input on $`SD`$. The compiler supplies an actual unitary $`V`$ such that

```math
\|VJ-JW_D\|_{\rm op}\leq\eta.                 \qquad\text{(1)}
```

This is an operator-norm bound on **every** input of $`SD`$, not only the state
column $`|0^n\rangle`$. Tensoring (1) with $`I_R`$ leaves its norm unchanged, so the
same bound holds for dirty inputs entangled with a reference. Mixed inputs
follow by purification or convexity. Any exact dirty-bank restoration promised
by the compiler remains a separate implementation requirement; it is not
inferred from a nonzero tolerance in (1).

Equation (1) includes amplitude outside the clean-work subspace. A bound only
on $`J^\dagger VJ-W_D`$ is insufficient: this projected block may have a
quadratically smaller error than the omitted leakage. Work is neither measured,
postselected nor reset between the forward and reverse circuits.

The observable is a Hermitian unitary $`O`$, with ideal controlled action

```math
\mathcal O=|0\rangle\!\langle0|_B\otimes I+
|1\rangle\!\langle1|_B\otimes O.
```

Its implementation
$`\widetilde{\mathcal O}`$ has full initialized-isometry error at most
$`\eta_O`$ against $`\mathcal O`$. This includes the relative phase of the two
branches and the observable's own work. Its approximate work is disjoint from
$`C`$; exactly returned scratch may be reused where its all-input contract
permits. The oracle bound must hold on arbitrary branch-system inputs and
external references, including the frame's coherent work. An error bound for
an uncontrolled $`O`$ only up to global phase is not this contract.

## 2. The actual adjoint has the same error

The exact identity

```math
V^\dagger J-JW_D^\dagger
=V^\dagger(JW_D-VJ)W_D^\dagger
```

implies

```math
\|V^\dagger J-JW_D^\dagger\|_{\rm op}
=\|VJ-JW_D\|_{\rm op}\leq\eta.              \qquad\text{(2)}
```

Both outer factors are unitary. This proves the inverse guarantee for the
**reversed actual circuit**, including all its work registers. It does not say
that $`V^\dagger`$ approximates $`W_D^\dagger`$ on arbitrary nonzero-work inputs.
That stronger assertion is unnecessary: unitary hybrid estimates propagate
any earlier leakage without assuming it has been reset.

## 3. Full output and the shared-circuit cancellation

Fix a purification $`|\xi\rangle_{DR}`$ of the dirty/reference input. Let
$`|u\rangle=|0^n\rangle_S|\xi\rangle_{DR}`$ and extend all operations by the
identity on unused registers, suppressing $`R`$ in operator subscripts. With the
ideal controlled observable, the actual premeasurement state is

```math
|\chi_V\rangle
=\frac{|0\rangle_BJ|u\rangle
      +|1\rangle_B V^\dagger(O\otimes I_{CDR})VJ|u\rangle}{\sqrt2}.
```

The first branch is exactly $`V^\dagger VJ|u\rangle=J|u\rangle`$.
In the response branch, add and subtract the ideal initialized intermediate:

```math
\begin{aligned}
&V^\dagger(O\otimes I)VJ-JW_D^\dagger O_DW_D\\
&\quad=V^\dagger(O\otimes I)(VJ-JW_D)
 +(V^\dagger J-JW_D^\dagger)O_DW_D,
\end{aligned}
```

where $`O_D=O\otimes I_D`$. Both terms have norm at most $`\eta`$ by (1)–(2).
Consequently the complete response error is at most $`2\eta`$, and

```math
\||\chi_V\rangle-|\chi_W\rangle\|\leq\sqrt2\,\eta.
```

Replacing the controlled observable by its actual implementation adds at most
$`\eta_O`$. The subsequent actual inverse is unitary and cannot increase that
error, even when the oracle's work leaks. Thus the full premeasurement state,
including all retained work and the reference, obeys

```math
\delta_{\rm out}\leq\sqrt2\,\eta+\eta_O.       \qquad\text{(3)}
```

The total-variation distance of the observed $`(b,y)`$ distributions is at most
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

The response error just proved is at most $`2\eta`$, so

```math
|\mathbb E_VZ_j-\partial_{\theta_j}E_O|
\leq4|a_j|\eta.                              \qquad\text{(4)}
```

This use of a projected amplitude is justified by the actual complete branch
state. It does not replace the full-isometry premise.

For normalized states $`|x\rangle,|z\rangle`$ and any bounded observable $`A`$,

```math
|\langle x|A|x\rangle-\langle z|A|z\rangle|
\leq2\|A\|\,\||x\rangle-|z\rangle\|.
```

Apply this to the change caused by the approximate controlled observable.
Its contribution is at most $`4|a_j|\eta_O`$. Adding (4) proves the displayed
$`4|a_j|(\eta+\eta_O)`$ bound. A singular raw coordinate with $`a_j=0`$ remains
exactly zero as a decoded record. No inverse metric weight appears.

The sharper constant in (4) uses the shared $`V,V^\dagger`$ pair and the Walsh
score. Applying only the general bounded-observable estimate to (3) gives the
valid but weaker $`4|a_j|(\sqrt2\eta+\eta_O)`$ bound.

## 5. Precision allocation preserves the sampling order

The classical tuple and oriented weights $`a_j`$ are fixed and known here.
Errors in classical weights, parity decoding or readout labels require their
own budgets. At each tree depth $`d`$,

```math
\sum_{j\text{ at depth }d}a_j^2=1,
\qquad \|Z^{(d)}\|_2=2
```

for every possible outcome. This deterministic norm remains true under the
actual, possibly biased measurement distribution. Independent repetitions
therefore concentrate about the **actual** mean with the same sufficient
sample order as in the exact protocol.

For completeness, if $`\overline Z^{(d)}`$ is a mean of $`S`$ independent depth
records with mean $`\mu^{(d)}`$, then
$`\mathbb E\|\overline Z^{(d)}-\mu^{(d)}\|_2\leq2/\sqrt S`$.
Changing one record changes this norm by at most $`4/S`$. McDiarmid's inequality
and a union bound over the $`n`$ depths give simultaneous depthwise error at
most $`\varepsilon_{\rm stat}`$ when, for example,

```math
S\geq\frac{32[1+\ln(n/\delta)]}{\varepsilon_{\rm stat}^2}.
```

Each coordinate error is at most its depth-vector error. Choose

```math
\eta\leq\varepsilon_\infty/16,\qquad
\eta_O\leq\varepsilon_\infty/16,\qquad
\varepsilon_{\rm stat}=\varepsilon_\infty/2.
```

The bias is at most $`\varepsilon_\infty/2`$, and with probability at least
$`1-\delta`$,

```math
\|\widehat{\nabla E_O}-\nabla E_O\|_\infty\leq\varepsilon_\infty,
\qquad
S=O\!\left(\varepsilon_\infty^{-2}[1+\log(n/\delta)]\right).
```

A sufficient synthesis precision is therefore
$`L=\Theta(1+\log(1/\varepsilon_\infty))`$, independently of the number of
coordinates. If a chosen synthesis theorem assumes error at most $`1/64`$, take
$`L=\max\{6,\lceil\log_2(16/\varepsilon_\infty)\rceil\}`$ for each of the two
allocated errors. This specifies an accuracy requirement; it does not itself
supply an elementary Clifford+T compiler or an optimal T-count theorem.

## 6. Parameter derivatives and complex coordinates

All statements compare a fixed ideal $`W(\theta)`$ and its actual compiled
circuit at that same tuple. They estimate the derivative of the ideal chart's
energy through its known frame identity. They do **not** differentiate the
compiled word. Uniformly close unitary families need not have close parameter
derivatives, and synthesized words can change discontinuously with the tuple.
A parameter update requires its own applicable fixed-tuple guarantee.

For complex magnitude coordinates, use the full phase-dressed frame
$`W_{\mathbb C,\mathrm{mag}}=D_{\rm ph}W_{\mathbb R}`$ in (1). The proof above
then applies unchanged. Leaf-phase coordinates use their separate direct
signed one-hot stream; they are not additional columns of this frame.
Section 9 proves its preparation/oracle guarantee separately, without using
the inverse-frame cancellation.

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

For the real magnitude protocol, let $`t_F`$ be the T-count of the chosen actual
frame circuit $`V`$ at error $`\eta`$, and let $`t_O`$ be that of the calibrated
controlled observable at error $`\eta_O`$. The same $`V`$ prepares the state and
its actual adjoint resolves the response. Clifford interference and readout
add no T gates. Thus

```math
\mathcal T_{\nabla}\leq S(2t_F+t_O).
```

Let $`a_F`$ and $`b_F`$ be the clean and dirty budgets assigned to the frame
compiler. Reserve one additional clean interference qubit and any separately
needed observable work before assigning $`a_F`$. With $`q_F=n+a_F+b_F`$ and the
hypotheses of the [fault-tolerant theorem](FAULT_TOLERANT_COMPILER.md),

```math
\mathcal T_{\nabla}
=O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\left[\sqrt{NL}+L+\frac{NL}{q_F}+t_O\right]
\right).
```

Here $`L`$ is chosen by the precision allocation above, and the sufficient frame
reservation is $`a_F\geq C(n+h)`$. The companion Clifford upper bound is
$`O(S(NL+g_O+n))`$, where $`g_O`$ is the controlled-observable Clifford count.
Classical weight preparation, decoding, and materializing the full gradient
remain separately charged. This is an upper bound for the specified real
inverse-frame protocol. Its frame-synthesis optimality is not a lower bound on
all possible gradient algorithms. The complete complex-gradient cost follows
from adding the direct phase stream below.


## 9. The complete complex gradient

Let $`W=D_\phi W_{\mathbb R}`$ and let $`V`$ approximate this complete
magnitude frame under (1). A phase execution prepares the system with $`V`$,
prepares the branch in $`|+\rangle`$, applies the controlled observable, and
measures the branch in the **Y basis** and the system in the computational
basis. The ideal state before those measurements is

```math
|\zeta\rangle=\frac{|0\rangle|\psi\rangle+
|1\rangle O|\psi\rangle}{\sqrt2}.
```

If $`b`$ labels the Y eigenvalue $`(-1)^b`$ and $`x`$ is the measured leaf, use
the record $`P=2(-1)^b e_x`$. Indeed,

```math
\mathbb E P_x
=2\mathrm{Im}\bigl(\psi_x^*(O\psi)_x\bigr)
=\partial_{\phi_x}E_O,
\qquad \|P\|_2=2.
```

There is no inverse frame in this circuit. Applying the preparation and
oracle bounds in sequence gives complete-state error at most
$`\eta+\eta_O`$, including retained work and reference correlations. For
every real unit vector $`v`$, the observable decoding $`v\cdot P`$ is
$`2Y\otimes\mathrm{diag}(v)`$, of norm at most two. The
bounded-observable estimate followed by Euclidean duality therefore gives

```math
\|\mathbb E_{\rm actual}P-\nabla_\phi E_O\|_2
\leq4(\eta+\eta_O).
```

The same fixed-norm concentration proof as in Section 5 now treats the
whole phase vector as **one** block. A union bound over the $`n`$ magnitude
blocks and this phase block yields simultaneous raw-coordinate accuracy
$`\varepsilon_\infty`$ for the complete complex gradient, with
$`S=O(\varepsilon_\infty^{-2}[1+\log((n+1)/\delta)])`$ executions
of each stream and the same synthesis precision order as before. Taking
the same $`S`$ in both streams gives

```math
\mathcal T_{\nabla,\mathbb C}\leq S(3t_F+2t_O),
```

where $`t_F`$ now counts the chosen complete **complex magnitude** frame.
Its real and diagonal components and all their work must be charged under
the applicable compiler theorem. The two streams run separately and reuse
their workspace. As before, reserve one branch qubit and the controlled
observable's work in addition to the frame reservation. This statement
includes the redundant common-phase coordinate; no inversion of the phase
metric or gauge fixing is needed.

## 10. Reflection sums and finite classical weights

Suppose the desired observable is supplied as a finite real sum

```math
H=\sum_r c_r O_r,\qquad O_r=O_r^\dagger,\quad O_r^2=I,
\qquad \Lambda=\sum_r|c_r|>0.
```

Assume the coefficients and the classical sampling distribution below are
specified exactly. For example, rational coefficients suffice. Independently
in each execution choose $`r`$ with probability $`|c_r|/\Lambda`$, use
phase-calibrated controlled $`O_r`$, and multiply the ordinary record by
$`\Lambda\mathrm{sgn}(c_r)`$. Linearity makes its ideal mean the
corresponding derivative of $`E_H`$. Every magnitude depth record and the
phase record now has norm $`2\Lambda`$. If every sampled oracle obeys the
same error bound $`\eta_O`$, the magnitude-coordinate bias is at most
$`4\Lambda|a_j|(\eta+\eta_O)`$ and the phase-vector bias is at most
$`4\Lambda(\eta+\eta_O)`$.

Classical magnitude weights need not be exact. If
$`|\widetilde a_j-a_j|\leq\tau`$, replacing $`a_j`$ by
$`\widetilde a_j`$ changes **every empirical coordinate average** by at
most $`2\Lambda\tau`$. Analyze concentration with the ideal weights and
then add this deterministic error. This avoids assuming that rounded
weights retain the exact depth-norm identity.

For $`0\lt \varepsilon_\infty\leq\Lambda`$, the explicit allocation

```math
\eta,\eta_O\leq\min\{1/64,\varepsilon_\infty/(32\Lambda)\},
\qquad \tau\leq\varepsilon_\infty/(8\Lambda),
\qquad
S\geq\frac{128\Lambda^2[1+\ln((n+1)/\delta)]}
{\varepsilon_\infty^2}
```

guarantees complete complex raw-gradient error at most
$`\varepsilon_\infty`$ with probability at least $`1-\delta`$.
The bias, weight-rounding and statistical budgets are respectively at most
$`\varepsilon_\infty/4`$, $`\varepsilon_\infty/4`$ and
$`\varepsilon_\infty/2`$. A sufficient frame and oracle precision is

```math
L=\max\{6,\lceil\log_2(32\Lambda/\varepsilon_\infty)\rceil\}.
```

For a real chart omit the phase stream. With
$`\overline t_O=\sum_r |c_r|t_{O_r}/\Lambda`$, the expected quantum
costs are $`S(2t_F+\overline t_O)`$ and
$`S(3t_F+2\overline t_O)`$ for the real and complex protocols,
respectively. Replacing $`\overline t_O`$ by $`\max_r t_{O_r}`$ gives a
deterministic bound. The sufficient-clean complex theorem gives

```math
\mathbb E\mathcal T_{\nabla,\mathbb C}
=O\!\left(\frac{\Lambda^2[1+\log((n+1)/\delta)]}
{\varepsilon_\infty^2}
\left[\sqrt{NL}+L+\frac{NL}{n+a_F+b_F}+\overline t_O\right]\right)
```

when $`a_F\geq C(n+h)`$, with the frame reservation and $`h`$ defined in
[Corollary 7](FAULT_TOLERANT_COMPILER.md#92-literal-diagonals-and-the-complex-magnitude-frame).
The two-clean complex compiler with
$`b_F\geq2(L+n+8)`$ yields

```math
\mathbb E\mathcal T_{\nabla,\mathbb C}
=O\!\left(\frac{\Lambda^2[1+\log((n+1)/\delta)]}
{\varepsilon_\infty^2}
\left[\sqrt{NL}+nL+\frac{NL}{b_F}+\overline t_O\right]\right).
```

The quantum circuit does not coherently load the term label: each shot
uses a classically chosen oracle. Preparing that classical sampler and
reading its term labels are additional classical costs. Approximate
Hamiltonian coefficients or sampling probabilities require their own
error budget; they are not covered by the weight error $`\tau`$ above.

### 10.1 Reusing a dirty bank across executions

Approximate return of an operator-source core does not by itself make
successive measurement outcomes independent. The sampling bounds above
nevertheless hold when that bank is reused, with the **system and all
declared clean inputs initialized for each execution**. The frame and
oracle contracts must continue to hold on every conditional dirty input,
including its external references. This is already their all-input
premise. Clean initialization between completed executions is a protocol
precondition; the compiler itself still uses no intermediate measurement,
reset or postselection.

Fix the parameter tuple throughout these executions. Let $`X_t`$ denote
one magnitude depth record or the complete phase record, with ideal
weights, and let $`\mathcal F_{t-1}`$ contain the preceding outcomes and
classical choices. Term choices are sampled from their declared
distribution independently of this history. Conditional on the history,
the dirty bank can have changed arbitrarily. The earlier bias proof still
applies. For magnitude coordinates, its $`|a_j|`$ factor and
$`\sum_{j\text{ at depth }d}a_j^2=1`$ give depth-block bias at most
$`4\Lambda(\eta+\eta_O)`$. The same bound for the phase block was
proved in Section 9.

The centered increments

```math
D_t=X_t-\mathbb E[X_t\mid\mathcal F_{t-1}]
```

are Hilbert-space martingale differences with $`\|D_t\|_2\leq4\Lambda`$.
[Pinelis, Theorem 3.5](https://arxiv.org/pdf/1208.2200v2), specialized to
Hilbert space, yields

```math
\Pr\!\left(\left\|\frac1S\sum_{t=1}^S D_t\right\|_2
\geq\varepsilon_{\rm stat}\right)
\leq2\exp\!\left(-\frac{S\varepsilon_{\rm stat}^2}{32\Lambda^2}\right).
```

The mean of the conditional biases remains within its same uniform bias
budget. Union over the $`n+1`$ blocks and set
$`\varepsilon_{\rm stat}=\varepsilon_\infty/2`$. It suffices that
$`S\geq128\Lambda^2\ln(2(n+1)/\delta)/\varepsilon_\infty^2`$, which
is already implied by Section 10's displayed choice. Finite weight error
still adds at most $`2\Lambda\tau`$ pathwise. Thus correlations from
reusing the dirty bank do not require an additional synthesis precision
factor proportional to the number of executions. This assertion concerns
the gradient estimate; it does not bound the bank's accumulated
disturbance over the entire experiment by a single-execution error.

The cited result is I. Pinelis, *Optimum bounds for the distributions of
martingales in Banach spaces*, Annals of Probability **22**, 1679–1706
(1994), [DOI: 10.1214/aop/1176988477](https://doi.org/10.1214/aop/1176988477).
Theorem 3.5 requires bounded martingale increments and does not assume
their independence or conditional symmetry.

## 11. Classical preparation and output costs

The weights $`a_j`$ can be computed down the binary tree. Start at one;
multiply by the corresponding ancestor sine or cosine at each edge.
Clamp computed factors and products to $`[-1,1]`$. If each factor error
and each multiplication's rounding error are at most $`\tau/(2n)`$,
induction on the depth gives $`|\widetilde a_j-a_j|\leq\tau`$.
Thus $`O(N)`$ certified trigonometric evaluations and $`O(N)`$ rounded
multiplications at
$`P=O(1+\log(n/\tau))`$ bits suffice. No dense $`N\times N`$ frame
matrix or numerical differentiation is required. For a supplied evaluator
of cost $`E(P)`$ and $`P`$-bit multiplication cost $`M(P)`$, this takes
$`O(N[E(P)+M(P)])`$ classical bit operations, in addition to reading the
angle descriptions. If evaluation costs differ by angle, use their sum.

The [operator-source construction](OPERATOR_SOURCE_COMPILER.md#10-classical-table-construction)
also has an explicit classical table-generation bound for bounded dyadic
angle inputs. These tables and the weights are prepared once per fixed
parameter tuple and reused across shots. A parameter update requires new
applicable tables and weights; compilation cost is not amortized across
unrelated tuples without an additional argument.

For $`S`$ magnitude outcomes, the existing record-wise or histogram decoder
uses $`O(S+N\min\{S,n\})`$ arithmetic operations. The phase decoder adds
$`O(S+N)`$. Classical term signs can be included in the signed histogram,
and its integer counters need $`O(1+\log S)`$ bits. Multiplication by
$`\Lambda`$ and the certified weights, final rounding, and writing the
$`\Theta(N)`$ output coordinates remain classical work. These are
arithmetic-operation counts; arbitrary-precision bit costs are not
silently set to one. The T-counts above quantify the specified protocols,
and do not establish an advantage over all classical or quantum gradient
methods.
