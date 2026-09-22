# Constant-clean construction search: dirty phase echo and an exact catalytic obstruction

> Preserved technical appendix. Read the [current endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md) for the governing model, remaining gap, and resume task. [Provenance](PROVENANCE.md) records the source and editorial scope.
> Historical finite-check summaries and scratch reproduction commands are omitted; the complete mathematical argument and its scope are retained.

Research working note for checkpoint 30. The established frontier is unchanged.

## 1. Exact catalyst width cannot be replaced by dirty multiplicity

Let $`K=\mathbb Q(\zeta_8)`$. Every finite circuit built from the project's fixed native Clifford+T matrices has entries in $`K`$. Put $`\zeta=e^{2\pi i/2^p}`$, $`p\ge3`$, and $`d=2^{p-3}`$.

**Exact returned-catalyst lemma.** A $`K`$-valued linear map $`A`$ on one target qubit, $`s`$ source qubits and $`b`$ arbitrary dirty qubits cannot satisfy

```math
A(|j\rangle|g\rangle|\psi\rangle)=\zeta^{2j-1}|j\rangle|g\rangle|\psi\rangle,\qquad j=0,1,
```

for all dirty $`|\psi\rangle`$, with a nonzero fixed source $`|g\rangle`$, unless $`s\ge p-3`$. This applies in particular to an exact Clifford+T unitary implementing the literal determinant-one rotation $`\operatorname{diag}(\zeta^{-1},\zeta)`$ while returning all source and dirty registers. The source may be an ideal arbitrary pure catalyst; no assumption about its preparation complexity is needed for the obstruction. All initialized or supplied registers retained by $`A`$ are included in $`s`$.

Proof. The field extension $`\mathbb Q(\zeta)/K`$ has degree $`d`$. The minimal polynomials over $`K`$ are

```math
m_+(x)=x^d-\zeta_8,\qquad m_-(x)=x^d-\zeta_8^{-1}.
```

They are distinct and irreducible. In particular, the inverse roots are NOT in the same $`K`$-Galois orbit: $`K`$-fixing automorphisms have odd exponents congruent to 1 modulo 8, whereas inversion has exponent 7 modulo 8. For each $`j`$, the promised input subspace has dimension $`D=2^b`$, so $`\zeta`$ and $`\zeta^{-1}`$ each have geometric, hence algebraic, multiplicity at least $`D`$. Because the characteristic polynomial has coefficients in $`K`$, each of $`m_+^D`$ and $`m_-^D`$ divides it. Consequently

```math
2^{s+1+b}\ge2d\,2^b,
```

and $`s\ge\log_2d=p-3`$. Arbitrarily many jointly returned dirty qubits cancel from the inequality. Arbitrary logical spectator qubits cancel by precisely the same argument.

The same lower bound holds for the phase gate $`\operatorname{diag}(1,\zeta)`$: its characteristic polynomial has factors $`(x-1)^D`$ and $`m_+^D`$, giving $`2^{s+1}\ge d+1`$. For integral $`s`$ and $`p\ge3`$ this again gives $`s\ge p-3`$.

This is a dimension lower bound for this exact catalytic interface, independent of T count. It neither proves that $`s=p-3`$ is sufficient for an elementary gate implementation nor addresses approximate frame synthesis.

### Accepted-return extension

One may allow private failure registers initialized and projected on computational zero. Their accepted block $`A`$ is still $`K`$-valued. If that block returns the source and dirty work exactly and implements $`\gamma\operatorname{diag}(\zeta^{-1},\zeta)`$, where $`\gamma`$ is any nonzero element of $`K`$, the same result holds: its distinct irreducible factors are $`x^d-\gamma^d\zeta_8`$ and $`x^d-\gamma^d\zeta_8^{-1}`$. The source dimension $`s`$ counts registers retained in the accepted block, not the computational-zero projection flags. There is no postselection implementation claim here; this is a statement about accepted blocks used in coherent dilations.

The restriction $`\gamma\in K`$ is explicit. Unknown algebraic normalizations cannot silently be canceled in this proof.

### Why this does not contradict small weighted sources

Checkpoint 29's accepted source eigenvalue $`1/2`$ lies in $`K`$ and has degree one. It is unaffected by this obstruction. Small sources can therefore supply dyadic attenuation even though an exact high-order dyadic phase catalyst has a large algebraic degree.

If the source itself is prepared by a finite Clifford+T circuit and returned exactly, there is an even simpler restriction: the resulting effective target entries belong to $`K`$. An exact phase $`\zeta`$ outside $`K`$ is then impossible at any supplied clean width. The statement above instead permits an ideal source containing non-$`K`$ amplitudes, so it directly audits ideal catalytic interfaces before their preparation is approximated and charged.

### Boundaries that matter

* Approximate source or target return is not covered. For example, $`I`$ approximates $`\operatorname{diag}(\zeta^{-1},\zeta)`$ with error $`|1-\zeta|\le2\pi/2^p`$ and uses no source. A robust lower bound at prescribed error requires another argument.
* The exact common phase matters. At $`p=4`$, $`\operatorname{diag}(\zeta^{-1},\zeta)`$ needs at least one ideal source by this lemma, but multiplying by $`\zeta^{-1}`$ yields $`\operatorname{diag}(\zeta_8^{-1},1)`$, an ordinary Clifford+T phase gate up to a Clifford wire flip. Thus the literal theorem cannot simply be relabeled projective.
* The count concerns initialized/supplied independent source work. It does not forbid a circuit using the quantum input itself without exposing such a source, or a globally optimized approximate frame compiler.
* Eigenvalue multiplicity, not merely eigenvalue presence, is essential. Omitting the factor $`2^b`$ would incorrectly turn arbitrary dirty dimensions into a source resource.

## 2. A complete dirty phase-echo identity, but no improved cost

Let $`P=2^\ell`$ and put $`\omega=e^{2\pi i/P}`$. On an arbitrary $`\ell`$-qubit dirty register, define

```math
X|z\rangle=|z+1\bmod P\rangle,\qquad Z|z\rangle=\omega^z|z\rangle.
```

For a classical coefficient function $`f(x)`$, define the controlled addition $`X_f`$ acting as $`X^{f(x)}`$. Then the full operator identity is

```math
ZX_fZ^{-1}X_f^{-1}=\left(\sum_x\omega^{f(x)}|x\rangle\langle x|\right)\otimes I_{\mathrm{dirty}}.
```

It requires no initialized phase-gradient eigenstate and preserves arbitrary dirty/reference states. The order and inverse operations are substantive: the phase is $`\omega^f`$, with the displayed right-to-left operator convention.

This is a valid alternative coefficient interface, not a cheap implementation. Two separate costs remain:

1. The clock $`Z`$ factors into $`\ell`$ one-qubit dyadic phase gates. Independently approximating the determinant-one version of each at error $`\epsilon/O(\ell)`$ gives the clock up to a common scalar; that scalar cancels against its actual inverse in the echo. This costs $`O(\ell\log(\ell/\epsilon))`$ T gates; for $`\ell=\Theta(L)`$ this is $`O(L^2+L\log L)`$, before applying the echo. An exact constant-source catalytic implementation of the finest phases is excluded by Section 1. Approximate joint synthesis of the entire clock with fewer T gates is not excluded.
2. $`X_f`$ is an addition lookup, not the XOR lookup already proved in the repository. The existing dirty-QROM proof uses CNOT table insertion, which supplies $`z\oplus f(x)`$, not $`z+f(x)`$. Replacing table insertions by additions changes their T cost; it cannot be assumed free. Computing angle bits one at a time and adding weighted increments is a valid conservative route but does not improve the available endpoint bound.

The echo's approximation accounting is straightforward: if actual unitaries $`\widetilde Z`$ and $`\widetilde X`$ approximate $`\alpha Z`$ and $`X_f`$ by $`\delta_Z`$ and $`\delta_X`$, for one modulus-one common scalar $`\alpha`$, and their literal inverses are used, the complete operator error is at most $`2\delta_Z+2\delta_X`$. No marginal dirty-state argument or trace average is involved.

The endpoint would require both an $`O(L)`$-T clock on arbitrary dirty data and an $`O(\sqrt{NL}+NL/K)`$-T coherent addition table with constant clean work, plus appropriate control/suffix accounting. Neither primitive has been established here. A scalar phase echo also needs the required determinant-one pairing and complete-frame composition; it cannot immediately substitute for a real Hopf layer without those reductions.

## 3. Primary-source comparison

Isaac H. Kim, [Catalytic z-rotations in constant T-depth](https://arxiv.org/html/2506.15147v1), uses special prepared eigenstates. Its fixed-angle construction has a source of $`O(m)`$ qubits for $`m`$-bit precision, and its variable-angle form uses $`m`$ copies, with a quadratic total-qubit count in the displayed construction (Sections 2.2–2.3). It therefore does not supply constant initialized width merely by allowing dirty work. Our spectral-multiplicity argument above is independent of that paper and carries no novelty claim.
