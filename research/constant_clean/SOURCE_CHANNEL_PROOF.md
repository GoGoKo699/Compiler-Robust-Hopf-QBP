# CP31 independent review: arbitrary returned-source attenuation

> Preserved technical appendix. Read the [current endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md) for the governing model, remaining gap, and resume task. [Provenance](PROVENANCE.md) records the source and editorial scope.

**Verdict: PASS, under the explicit returned-source contract below.** The proposed channel argument removes CP30's source-arithmetic restriction. It gives a quantitative obstruction for a source of fixed width even if its amplitudes are transcendental or depend on the requested precision. It does not give a general Hopf-frame lower bound or an additive lower bound over independently specified kernels.

This note derives the channel lattice and constants independently. A second auditor, `lower_frontier_audit`, independently reported the same determinant and singular-value bounds.

## 1. Exact circuit and source premises

There are $`s`$ retained source qubits in an arbitrary density matrix $`\rho`$, initially in product with all other registers. Set

```math
d=2^s,\qquad D=d^2=4^s.
```

Every additional supplied nonstabilizer quantum resource must be included in this source register. There is no requirement that $`\rho`$ be exactly preparable, algebraic, fixed as precision changes, or efficiently specified. The processing word can be compiled with full classical knowledge of $`\rho`$; the proof is independent of that choice.

The processing operation is a finite coherent Clifford+T word with $`\tau`$ T/T-dagger gates. Mathematical acceptance projects $`f`$ specified private qubits onto computational zero. All such projected qubits must be counted, even if omitted from a chosen output description. Other initialized helpers are pure stabilizer states; arbitrary biased stabilizer mixtures are not supplied for free. Any additional logical/address registers may be specialized to a stabilizer input; in a controlled attenuation family, specialize the exponent address to its classical value $`k`$. Dirty helpers have a uniform arbitrary-input promise and may therefore be specialized to maximally mixed states. No assumption that arbitrary unknown dirty bits are actually initialized is used.

After acceptance, trace every register except the source. This defines a completely positive, trace-nonincreasing map

```math
\Phi:\mathcal L(\mathbb C^d)\longrightarrow\mathcal L(\mathbb C^d).
```

Output helpers and data need not be restored for this lower bound. The source-return contract, however, is substantive: in the exact case its subnormalized marginal must equal $`4^{-k}\rho`$. A probability-only promise without returned source is not enough for the new eigenvalue argument.

## 2. Logical Pauli coefficients have no hidden helper denominator

Choose Hermitian source Paulis $`P_i`$ and define the real Pauli transfer matrix

```math
F_{ij}=d^{-1}\operatorname{Tr}[P_i\Phi(P_j)].
```

Let the environment have $`h`$ qubits and input

```math
\omega=2^{-h}\sum_Q c_Q Q,
\qquad c_Q\in\{0,1,-1\},
```

as holds for the selected stabilizer inputs and maximally mixed dirty factors. Let $`R_{\mathrm{full}}`$ be the normalized Pauli transfer matrix of the full processing unitary. Expanding the $`f`$-bit acceptance projector gives

```math
F_{ij}=2^{-f}\sum_{Q,R}c_Q
(R_{\mathrm{full}})_{(P_i,Z_R),(P_j,Q)}.
```

Here $`R`$ runs over the selected products of acceptance $`Z`$ operators, with identity on the other traced outputs. The $`2^{-h}`$ environmental expansion factor cancels the full trace normalization exactly. Thus neither the dirty width nor the number of ordinary stabilizer helpers introduces an extra denominator.

Every full transfer coefficient belongs to $`(\sqrt2)^{-\tau}\mathbb Z[\sqrt2]`$: Cliffords permute signed Pauli coordinates, while each T/T-dagger introduces at most one division by $`\sqrt2`$. Consequently, with

```math
r=\tau+2f,
\qquad F\in(\sqrt2)^{-r}\operatorname{Mat}_D(\mathbb Z[\sqrt2]).
```

Coefficientwise conjugation $`\sigma:\sqrt2\mapsto-\sqrt2`$ turns this transfer calculation into another physical CPTNI map. Replace each T by ZT and each T-dagger by ZT-dagger; Clifford channels, the selected environment and the acceptance projector are fixed. The source density is **not** conjugated or assumed algebraic in this statement. It is the map that has the conjugated physical implementation.

## 3. Exact returned-source bound

Suppose

```math
\Phi(\rho)=q\rho,
\qquad q=4^{-k}=2^{-2k},
\qquad \operatorname{Tr}\rho=1.
```

Then $`q`$ is an eigenvalue of $`F`$, regardless of the arithmetic of its nonzero eigenvector $`\rho`$. The matrix $`(\sqrt2)^rF`$ has entries in the algebraic integer ring $`\mathbb Z[\sqrt2]`$; every eigenvalue of that matrix is an algebraic integer. Therefore

```math
(\sqrt2)^r q=(\sqrt2)^{r-4k}
```

is an algebraic integer. Its field norm is $`\pm2^{r-4k}`$, which cannot be an integer when $`r<4k`$. Hence

```math
\boxed{\tau+2f\ge4k.}
```

This needs only equality of the accepted source marginal. It does not need an exact product-return promise, although the stronger circuit contract implies it. In contrast with CP30's probability-only theorem for its particular rational source, this theorem needs returned source but permits **any** source state.

## 4. Quantitative spectral separation when $`r<4k`$

Assume $`r<4k`$, and set

```math
M=F-qI_D,\qquad H=\sqrt d+1.
```

The preceding integrality argument shows $`M`$ is invertible. Its entries lie in $`2^{-2k}\mathbb Z[\sqrt2]`$, so

```math
2^{2kD}\det M\in\mathbb Z[\sqrt2].
```

The nonzero algebraic integer norm is at least one in absolute value. Since $`q`$ is rational, $`\sigma(M)=\sigma(F)-qI`$, and

```math
\left|\det M\det\sigma(M)\right|\ge2^{-4kD}.
```

For a Hermitian matrix $`X`$, complete positivity and trace nonincrease imply

```math
\|\Phi(X)\|_2\le\|\Phi(X)\|_1
\le\|X\|_1\le\sqrt d\,\|X\|_2.
```

The middle inequality follows by applying the map to the positive and negative parts of $`X`$. Because the Pauli matrix is real, its largest singular value is attained on a real vector, corresponding to a Hermitian $`X`$. Thus its Euclidean operator norm is at most $`\sqrt d`$. The same holds for the conjugated CPTNI map. Both $`M`$ and $`\sigma(M)`$ therefore have operator norm at most $`H`$ for $`k\ge 0`$.

Bounding the conjugate determinant by $`H^D`$ and the largest $`D-1`$ singular values of $`M`$ by $`H`$ gives

```math
\boxed{\sigma_{\min}(M)\ge
\frac{2^{-4kD}}{H^{2D-1}}.}
```

The normalization of the Pauli basis introduces no extra factor: the same $`F`$ acts in the orthonormal basis $`P_i/\sqrt d`$. Every normalized source density satisfies $`\|\rho\|_2\ge1/\sqrt d`$, so

```math
\boxed{\|\Phi(\rho)-4^{-k}\rho\|_2
\ge\frac{2^{-4kD}}{\sqrt d\,H^{2D-1}}.}
```

This is uniform over all density matrices, including precision-dependent and transcendental choices. Nonnormality of the channel matrix is fully accounted for by the singular-value estimate; an eigenvalue-distance argument alone would have been insufficient.

## 5. From accepted-vector error to the source residual

Put $`\lambda=2^{-k}`$. Suppose the complete accepted output is within vector error $`\epsilon`$ of $`\lambda`$ times an intended normalized output that returns the source. For a mixed source, impose this contract on a normalized purification, with the processing word acting trivially on the purifying reference. The desired target/data action may otherwise be arbitrary.

For actual and ideal accepted vectors $`a,b`$,

```math
\||a\rangle\langle a|-|b\rangle\langle b|\|_1
\le(\|a\|+\|b\|)\|a-b\|
\le(2\lambda+\epsilon)\epsilon.
```

Partial trace and the inequality between Hilbert-Schmidt and trace norms then give

```math
\|\Phi(\rho)-\lambda^2\rho\|_2
\le2\lambda\epsilon+\epsilon^2.
```

A uniformly valid promise on pure dirty inputs can alternatively be averaged to reach the same bound on the chosen maximally mixed dirty input. A bound on the normalized successful source alone would not supply this estimate, because its success probability could be wrong.

Take $`\epsilon=2^{-L}`$ and $`1\le k\le L`$. The upper bound is at most $`3\cdot2^{-k-L}`$. Therefore $`r<4k`$ would require

```math
L\le(4D-1)k+c_s,
\qquad c_s=\log_2\!\left[3\sqrt d(\sqrt d+1)^{2D-1}\right].
```

Equivalently,

```math
\boxed{L>(4D-1)k+c_s
\quad\Longrightarrow\quad\tau+2f\ge4k.}
```

All strict inequalities and the assumption $`k\le L`$ are explicit.

For an integer-only conservative threshold, use

```math
c_s< C_s:=2+(s+2)D.
```

Indeed $`\sqrt d+1\le2^{s/2+1}`$ gives $`c_s<1+(s+2)D`$, so the stated $`C_s`$ has extra headroom. If

```math
L\ge16D(s+3),\qquad k=\left\lfloor\frac{L}{8D}\right\rfloor,
```

then $`1\le k\le L`$ and $`(4D-1)k+C_s<L`$. Hence

```math
\boxed{\tau+2f\ge4\left\lfloor\frac{L}{8D}\right\rfloor
\ge\frac{L}{2D}-4.}
```

For fixed source width and fixed projected work this yields a worst-case $`\Omega(L/4^s)`$ T cost for a family that must supply all those attenuations with absolute accepted-vector error $`2^{-L}`$. The dependence on $`4^s`$ is a proved sufficient bound from this determinant argument, not an optimality assertion.

## 6. Uniform-family corollary without a large-precision threshold

Suppose a family supplies the preceding accepted-vector attenuation contract at absolute error $`2^{-L}`$ for every integer exponent $`k=1,\ldots,L`$. Each circuit may have its own source state, even depending on $`k`$ and $`L`$, but all sources use at most $`s`$ qubits. Source registers smaller than $`s`$ can be padded by untouched initialized zero qubits, so the same $`D=4^s`$ applies. Let

```math
R=\max_{1\le k\le L}(\tau_k+2f_k).
```

If $`R<4L`$, choose $`k=\lfloor R/4\rfloor+1`$. Then $`1\le k\le L`$ and $`\tau_k+2f_k\le R<4k`$, so the preceding determinant argument implies

```math
\begin{aligned}
L&\le(4D-1)k+c_s\\
&\le(4D-1)(R/4+1)+2+(s+2)D\\
&=D(R+s+6)-R/4+1\\
&\le D(R+s+6)+1.
\end{aligned}
```

If instead $`R\ge 4L`$, the final lower bound below is immediate. Thus the safe uniform statement, valid without a separate large-$`L`$ threshold, is

```math
\boxed{4^s(R+s+6)\ge L-2,}
\qquad
\boxed{R\ge\frac{L-2}{4^s}-s-6.}
```

The derivation actually permits $`L-1`$ with these constants; retaining $`L-2`$ is harmless extra slack. The statement makes no claim that the dimension dependence is optimal.

In particular, if $`R=\operatorname{polylog}(L)`$, then

```math
\boxed{s\ge\tfrac12\log_2L-O(\log\log L).}
```

For completeness, if $`s\ge\tfrac12\log_2L`$ this follows immediately. Otherwise $`s=O(\log L)`$, so taking logarithms of the boxed product bound gives $`2s\ge\log_2(L-2)-\log_2(R+s+6)`$, and the last term is $`O(\log\log L)`$. The required initialized source width therefore cannot remain constant for a family with polylogarithmic processing/projected-work cost under this returned-source contract.

This is a maximum-over-exponents bound. It does not sum processing costs, assume a single source state must work for all exponents, or apply to a family specified only at a few exponents that omit the chosen witness.

## 7. Consequences and limits

The new source-channel argument closes the arithmetic-source escape left explicit in CP30, **for this returned-source attenuation interface**. Supplying a precision-dependent one-qubit state with very large denominator or conjugate norm no longer evades it. Changing the source with the exponent also does not evade the individual-k bound, since the residual estimate is uniform over all normalized densities.

It remains compatible with one globally combined $`O(L)`$-T coefficient operation. The lower bound cannot be summed over calls in an unrestricted synthesized circuit, and it does not show that every full-frame implementation must expose a source-returning scalar attenuation channel. At $`L=N`$, an $`\Omega(N)`$ primitive cost is itself compatible with the desired global $`O(N)`$ endpoint. A complete constructive compiler or a general small-clean-space lower bound requires additional work.

No finite check substitutes for the channel-lattice and determinant arguments. Focused exact tests can verify the PTM convention, projection factor, physical conjugate and finite determinant certificates; they do not establish the universal quantifier over sources by sampling them.
