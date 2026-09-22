# CP29: finite precision sources, shift width, and the missing cost in radix shortcuts

> Preserved technical appendix. Read the [current endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md) for the governing model, remaining gap, and resume task. [Provenance](PROVENANCE.md) records the source and editorial scope.
> The standalone-power result here is supplemented by the later [arbitrary returned-source theorem](SOURCE_CHANNEL_PROOF.md), which also permits precision-dependent source states.

This note audits whether the precision register of checkpoint 28 can be made substantially smaller. It proves a tight bound for that construction's unweighted nilpotent shift and gives an explicit constant-width counterexample to any unrestricted source-width claim. It does not improve the full-frame compiler frontier below its stated clean reservation.

Let the requested error be $`\eta=2^{-L}`$, with harmless constant error-budget factors suppressed only where stated. Source-register width is distinct from the entry label, precision-digit label, clean coarse-program buffer, private failure work, and exact lookup selectors. Reducing one register alone does not reduce the complete reservation.

## 1. A tight finite-dimensional bound for the unweighted shift

On an $`m`$-dimensional space define

```math
S_m=\sum_{j=1}^{m-1}|j-1\rangle\langle j|.
```

For every $`0<\lambda<1`$ and normalized vector $`v`$,

```math
\boxed{\|(S_m-\lambda I)v\|\geq\frac{(1-\lambda)\lambda^m}{1-\lambda^m}.}\tag{1}
```

Indeed $`S_m^m=0`$, so

```math
(S_m-\lambda I)^{-1}=-\sum_{r=0}^{m-1}\lambda^{-r-1}S_m^r,\qquad
\|(S_m-\lambda I)^{-1}\|\leq\sum_{r=0}^{m-1}\lambda^{-r-1}=\frac{\lambda^{-m}-1}{1-\lambda}.
```

Applying the inverse to $`(S_m-\lambda I)v`$ proves (1). This holds for complex vectors as well as real nonnegative vectors; cancellations do not evade it.

For comparison, the normalized geometric vector

```math
v_j=\sqrt{\frac{1-\lambda^2}{1-\lambda^{2m}}}\,\lambda^j\quad(0\leq j<m)
```

satisfies

```math
\|(S_m-\lambda I)v\|=\sqrt{\frac{1-\lambda^2}{1-\lambda^{2m}}}\,\lambda^m.\tag{2}
```

Only its last coordinate contributes to the residual. Thus the best possible error is $`\Theta(\lambda^m)`$ for every fixed $`\lambda`$ strictly between zero and one. No assertion about the Clifford+T preparation cost of this exactly normalized vector is needed for this matching mathematical upper bound.

More generally, the displacement-$`d`$ partial shift $`S_d`$ on $`M`$ coordinates decomposes into $`d`$ chains. The longest has $`m=\lceil M/d\rceil`$ coordinates, and the shortest differs by at most one. Applying (1) on every chain and using the longest-chain bound gives

```math
\|(S_d-\lambda I)v\|\geq\frac{(1-\lambda)\lambda^{\lceil M/d\rceil}}{1-\lambda^{\lceil M/d\rceil}}\tag{3}
```

for every normalized $`v`$. A geometric vector supported on a longest chain supplies the matching order.

For checkpoint 28, $`d=2`$, $`\lambda=1/2`$, and $`M`$ is even. Hence

```math
\boxed{\|(S_2-\tfrac12 I)v\|\geq\frac{2^{-M/2-1}}{1-2^{-M/2}}>2^{-M/2-1}.}\tag{4}
```

The retained capped source has error $`\sqrt{4-2\sqrt2}\,2^{-M/2}`$, within a constant factor of this optimum. If the interface requires source-return error at most $`2^{-L}`$, (4) forces $`M>2(L-1)`$ and therefore $`\log_2M\ge\log_2L-O(1)`$ source qubits.

This is a bound on the unweighted shift interface. If the shift is multiplied by a small physical coefficient $`w`$, the conclusion from a requirement $`w\|(S_2-I/2)v\|\le2^{-L}`$ is only

```math
M/2>L+\log_2 w-1.
```

For weights bounded below by an inverse polynomial in $`N,L`$, this still needs $`M=\Omega(L)`$ when $`L`$ dominates the logarithm of that polynomial. An upper bound obtained by summing absolute coefficients is not automatically a necessary error for every target. In particular, cancellations between an entire target's selected atoms could matter. No global frame lower bound or additive cost over stages follows from (4).

## 2. Constant-width source return is possible for a different kernel

The following example rules out an overbroad inference that all high-precision reusable sources must have logarithmic precision width. On one source qubit put

```math
v=\frac{2|0\rangle+|1\rangle}{\sqrt5},\qquad
B=|0\rangle\langle1|+\tfrac14|1\rangle\langle0|
=\begin{pmatrix}0&1\\1/4&0\end{pmatrix}.
```

Then $`\|B\|=1`$ and

```math
Bv=\tfrac12v,\qquad B^2=\tfrac14I.\tag{5}
```

There is a constant-size, exact Clifford+T dilation of $`B`$. Initialize four private failure bits in $`|0000\rangle`$. Conditional on the **input** source bit being zero, apply a Hadamard to each of those four bits. Then apply $`X`$ to the source bit. Projection of the failure bits onto $`|0000\rangle`$ gives amplitude $`1/4`$ on input source zero and amplitude one on input source one, followed by the source flip. This is exactly $`B`$. Each controlled Hadamard has an exact constant Clifford+T implementation; the whole operation and its literal reverse are unitaries on every input, including nonzero failure registers. No failure bit is overwritten or measured.

The ideal vector $`v`$ is not an exactly Clifford+T-preparable state: its $`Z`$ expectation is $`3/5`$, which is outside the dyadic ring $`\mathbb Z[1/\sqrt2]`$. A single-qubit preparation can, however, approximate it in vector norm to $`\epsilon`$ using $`O(\log(1/\epsilon))`$ T gates under the retained one-qubit synthesis interface. The physical source is then the actual vector $`\widetilde v`$ prepared by that word, and

```math
\|B\widetilde v-\tfrac12\widetilde v\|\leq(\|B\|+\tfrac12)\|\widetilde v-v\|\leq\tfrac32\epsilon.
```

For any exponent $`k\ge 1`$, the sharper direct estimate is

```math
\|B^k\widetilde v-2^{-k}\widetilde v\|\leq(\|B^k\|+2^{-k})\epsilon\leq2\epsilon.
```

Thus preparing one qubit to precision $`2^{-L}`$ once can supply an approximately returned eigenvector for an entire family of ideal contractions. This example does not provide efficient variable powers of those contractions.

The exact-return valuation obstruction of checkpoint 28 is respected. The physical source is exactly Clifford+T-prepared but is only approximately returned; the exactly returned ideal source is not exactly Clifford+T-preparable.

## 3. Variable powers transfer the cost to scalar attenuation

For the preceding example,

```math
B^k=\begin{cases}2^{-k}I,&k\text{ even},\\2^{-(k-1)}B,&k\text{ odd}.\end{cases}\tag{6}
```

Computing the integer $`k`$ or its parity does not implement the scalar factors in (6). Their deterministic accepted-block implementation has a useful separate lower bound.

Suppose a Clifford+T circuit with $`\tau`$ T gates and stabilizer-initialized ancillary work realizes **exactly the standalone accepted block** $`B^k`$, with a designated projection of $`f`$ initialized private qubits onto zero. Ordinary additional initialized or dirty helpers may be traced out only consistently with that exact accepted map. There is no supplied nonstabilizer catalyst in this statement. On the stabilizer input source $`|0\rangle`$, the accepted source amplitude has magnitude

```math
2^{-k}\quad(k\text{ even}),\qquad 2^{-(k+1)}\quad(k\text{ odd}).
```

Consequently its success probability is respectively $`2^{-2k}`$ or $`2^{-2k-2}`$. The dyadic Pauli valuation argument retained in checkpoint 28 applies directly: initial valuation is zero, each T gate increases it by at most one, projection of $`f`$ qubits increases it by at most $`2f`$, and tracing helpers cannot increase it. The identity Pauli coefficient of the subnormalized output is already the stated success probability. Therefore

```math
\boxed{\tau+2f\geq4k+4(k\bmod2).}\tag{7}
```

With a constant number of projected private bits this forces $`\Omega(k)`$ T gates. With $`\Theta(k)`$ projected bits, a large probability attenuation can instead be encoded in their Hadamard overlap; that allocation is not tiny clean workspace. This is a lower bound on exact standalone $`B^k`$ dilation, not on an arbitrary circuit that only has to work on its particular approximate source, and not on a jointly optimized full frame. Approximate logical powers require a separate analysis and are not covered by (7).

Thus the one-qubit example removes a spurious generic width obstruction but does not yet provide the cheap $`k`$-dependent contractions required by checkpoint 28's $`O(QL)`$ digit tables.

## 4. Why radix regrouping alone does not remove the live precision label

Write a binary position as $`k=Dq+r`$, with $`0\le r<D`$. Then

```math
2^{-k}=(2^{-D})^q2^{-r}.
```

A faster-decaying source could reduce its quotient-index width from $`\log L`$ to approximately $`\log(L/D)`$. But the exact Boolean table remains indexed by the arbitrary binary digit $`f_{\ell,Dq+r}`$. A coherent quotient-and-remainder address occupies

```math
\lceil\log_2(L/D)\rceil+\lceil\log_2D\rceil=\log_2L+O(1)
```

bits in the balanced range. The factor $`2^{-r}`$ also needs a physical implementation. Loading the full radix digit uses a $`D`$-bit output word; streaming that word changes the charged program/combination circuit. Treating either a high-precision scalar attenuation or a complete $`D`$-bit digit as a constant-cost classical label would omit the operation that actually introduces its amplitude.

A base-$`2^D`$ capped geometric source is also not an automatic exact version of the special binary source. Its ordinary geometric amplitudes contain $`\sqrt{1-2^{-D}}`$. For general $`D`$ these do not lie in the Clifford+T ring. Additional dilation coordinates, approximate preparation, or a separate normalization construction must be specified and charged. The exceptional binary source cannot simply be relabelled with a larger radix while retaining its exact preparation proof.

## 5. Coarse compensation does not give a free small-width branch

One can formally reduce the number $`J`$ of retained digit positions by making the rare correction probability much smaller. The checkpoint-28 local error contains terms of the form

```math
Rp\left(2^{-M/2}+J^{-1}2^{1-J}\right),\qquad M=4J.
```

Choosing $`p`$ of order $`2^{-(L-J)}`$ can compensate for a shorter digit cutoff. But the exactly clean coarse word must then achieve per-depth error at most $`p/(4nQ_{\max}J)`$, so its program precision becomes

```math
w=O(n+L-J+\log J+\log R).
```

In the regime $`J\ll L`$, the requested coarse accuracy has $`\Theta(L)`$ precision bits, and the retained synthesis guarantee is an $`O(L)`$-length word rather than an $`O(n+h)`$-length word. A particular simple target may compile shorter; no lower bound on every target word is being asserted. The old full-word buffer guarantee no longer applies merely because the source register has shrunk. The retained mixed loader must charge its streamed output-buffer penalty, and each original depth still interprets its actual synthesized word. Moreover, preparing a rare probability of order $`2^{-L}`$ on $`O(1)`$ wires invokes a separately charged synthesis; implementing that probability with $`L`$ Hadamards instead uses $`L`$ initialized wires. These are alternative charged circuits, not free replacement constants.

This observation yields no better full-frame T bound than the applicable earlier compilers. In particular, none of the foregoing arguments closes the constant-clean, large-dirty endpoint.

## 6. Result and next concrete interface

The capped unweighted shift used in checkpoint 28 is already optimal to constant factors in its source dimension at fixed eigenvalue. A lower-dimensional source is possible when the contraction itself changes, as (5) demonstrates. The remaining constructive target is therefore a family of cheap, controlled contractions that acts on one common small prepared state and supplies the entire sequence of binary weights, while charging the coefficient address, private failures and actual inverse. An improvement must specify that complete family; a small source alone is insufficient.

No numerical experiment is needed for (1)–(7): these are finite algebraic statements. They delimit particular proposed interfaces and do not establish a new full-frame asymptotic frontier, a generic lower bound on all reusable precision states, or an additive per-stage lower bound.
