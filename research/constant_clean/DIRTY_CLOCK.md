# Dirty clock synthesis: a factorwise lower bound, with joint synthesis still open

> Preserved technical appendix. Read the [current endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md) for the governing model, remaining gap, and resume task. [Provenance](PROVENANCE.md) records the source and editorial scope.

Working note for checkpoint 31. No improvement to the complete-frame upper bound is claimed.

Let

```math
Z_m|y\rangle=e^{2\pi i y/2^m}|y\rangle,\qquad\eta=2^{-L}.
```

Writing $`y`$ in binary gives a tensor product of dyadic phase gates

```math
Z_m=P_1\otimes\cdots\otimes P_m,
P_j=\operatorname{diag}(1,e^{2\pi i/2^j}),
```

up to the fixed ordering of bits. The first three factors are Clifford+T. Ordinary factorwise synthesis costs $`O(m\log(m/\eta))`$ T gates, and uses no clean work beyond any optional per-factor implementation. Its literal inverse has the same T cost. A common scalar phase may be left uncalibrated only when the actual circuit and its inverse appear in the surrounding Weyl commutator.

The result below proves a quadratic obstruction for this *factorwise representation* at $`m\approx L`$. It is not a general clock lower bound and is not summed across arbitrary correction stages.

## 1. A small nonzero transition costs precision even with dirty helpers

**Probability lemma.** Start a finite coherent Clifford+T circuit with pure stabilizer inputs, including any initialized work and a fixed computational-basis choice for arbitrary dirty inputs. If it uses $`\tau`$ T/T-dagger gates, every nonzero probability $`p`$ of a one-qubit Pauli measurement outcome satisfies

```math
p\ge2^{-(\tau+2)}.
```

Proof. A Clifford channel permutes signed Pauli coefficients. Each T/T-dagger channel introduces at most one denominator $`\sqrt2`$. The projector for one Pauli measurement contributes a denominator 2. Thus

```math
p\in(\sqrt2)^{-(\tau+2)}\mathbb Z[\sqrt2].
```

Under the field automorphism $`\sigma:\sqrt2\mapsto-\sqrt2`$, the Pauli-channel calculation is another physical Clifford+T calculation (the T channel becomes the $`T^5`$ channel, and conversely for the inverse). Therefore $`0\le\sigma(p)\le1`$. Nonzero $`p`$ has a nonzero rational field norm whose numerator is an integer and denominator divides $`2^{\tau+2}`$. Hence $`p\sigma(p)\ge2^{-(\tau+2)}`$, proving the bound. The statement is independent of total dirty width because a uniform dirty-input promise includes the chosen stabilizer input.

This is the same Pauli-denominator method used in checkpoint 30, now with no free nonstabilizer source and only the one-qubit outcome projector; primary precedent is [Beverland, Campbell, Howard and Kliuchnikov, Lower bounds on the non-Clifford resources for quantum computations](https://arxiv.org/html/1904.01124v2), Definition 6.1 and Appendix A.9/A.10. The displayed interface corollary is derived here without a novelty claim. It gives a bound on the *entire circuit being considered*, not an additive accounting rule for arbitrary subcircuits.

**Dyadic-factor corollary.** Suppose such a standalone circuit implements $`P_j`$ to complete-isometry error $`\epsilon\le2^{-j}`$, permitting any common scalar phase. It may use arbitrary dirty helpers with the required uniform return guarantee. Then, for $`j\ge3`$,

```math
\tau\ge2j-6.
```

Indeed, on input $`|+\rangle`$, the ideal norm of the $`|-\rangle`$ component is $`s_j=\sin(\pi/2^j)`$. For $`j\ge1`$,

```math
2^{1-j}\le s_j\le\pi2^{-j}.
```

Projection contracts vector error, so the actual transition norm is nonzero and is at most $`s_j+\epsilon<5\cdot2^{-j}`$. Consequently

```math
0<p<25\cdot4^{-j}<32\cdot4^{-j}.
```

The probability lemma gives $`\tau+2>2j-5`$, or $`\tau>2j-7`$. Integrality yields $`\tau\ge2j-6`$. Literal scalar phases do not affect this measurement.

The same argument gives the **unsegmented whole-clock lower bound** $`\tau\ge2\min\{m,\lfloor L\rfloor\}-6`$: initialize all other clock bits to computational zero and put only the selected bit in $`|+\rangle`$. This is a single-circuit bound and allows arbitrary joint processing. It is linear at $`m\approx L`$ and remains compatible with the sought $`O(m+L)`$ construction.

The standalone circuit can create and consume a precision-dependent catalyst internally; those gates are counted in $`\tau`$. A supplied or retained nonstabilizer source would change the premise, and this corollary does not charge its resources a second time.

## 2. The factorwise clock architecture is quadratic near $`m=L`$

Consider an explicitly factorwise implementation with disjoint charged gate segments $`V_1,\ldots,V_m`$. Each segment starts with pure-stabilizer-initialized private work, targets one clock bit, and restores every arbitrary helper before the next segment. No prepared nonstabilizer state is retained between segments. Assume each $`V_j`$ implements its dyadic factor with error at most $`2^{-L}`$. Put $`k=\min\{m,\lfloor L\rfloor\}`$. Then

```math
T_{\mathrm{total}}\ge\sum_{j=4}^k(2j-6)=(k-2)(k-3),\qquad k\ge3.
```

In particular, $`m=\Theta(L)`$ with $`m`$ bounded below by a positive multiple of $`L`$ gives $`\Omega(L^2)`$. Better per-angle precision allocation inside this architecture cannot supply an $`O(m+L)`$ clock when the allocated per-factor errors sum to $`\eta`$: every allocated error is then at most $`\eta`$.

There is also an exact-work-return version that does not assume independent factor error budgets. Suppose every segment returns clean and dirty work exactly and induces a target-only unitary $`Q_j`$. Its effective clock action is the tensor product of $`Q_j`$. If that tensor product approximates $`Z_m`$ to error $`\eta`$, up to a global phase, then each $`Q_j`$ approximates $`P_j`$ up to its own common phase within $`\eta`$. To see this, put $`W_j=P_j^\dagger Q_j`$, fix one eigenvalue from every $`W_l`$ with $`l\ne j`$, and restrict the tensor-product norm bound to their joint eigenspace. The resulting two eigenvalues show $`\|W_j-c_jI\|\le\eta`$ for a suitable unit-modulus $`c_j`$. The same per-factor probability lower bound therefore applies.

**Scope.** This lower bound applies to the stated decomposition into independently restored factor modules. It does not imply $`T(Z_m)=\Omega(L^2)`$. A joint synthesis may correlate the clock bits, keep a nonstabilizer intermediate source, merge successive words, or directly implement the entire commutator. Such a circuit need not admit the charged segmentation above. Nor may this bound be summed across unrelated frame-correction stages.

## 3. Why the usual catalysis shortcut does not settle joint synthesis

Phase-gradient addition uses a prepared Fourier eigenstate, which has a register whose initialized width grows with precision. Checkpoint 30's exact returned-source theorem also rules out exact dyadic phase catalysis at arbitrarily fine order using a bounded-size source, even with an arbitrary dirty register. Both facts leave approximate joint clock synthesis open.

Checkpoint 31 now covers arbitrary precision-dependent sources for returned-source attenuation. Its interface theorem does not rule out a joint approximate clock: one global $`O(L)`$ operation remains compatible with the bound. In principle a source could be prepared once for $`O(L)`$ T gates on a constant number of clean qubits, influence all $`m`$ dirty target bits, and be returned. No coherent constant-clean construction achieving that interface was found in this search. In particular, the standard two-output rotation-catalysis identity consumes an additional doubled-angle operation; it does not, by itself, produce the complete dyadic ladder from one finest-angle source without additional work.

The primary source [Kim, Catalytic z-rotations in constant T-depth](https://arxiv.org/html/2506.15147v1), Sections 2.2-2.3, uses growing prepared eigenstates and multiple copies for its variable-angle construction. It does not supply the present constant-clean, total-T-count primitive.

## 4. What would be sufficient next

An $`O(m+L)`$-T unitary $`\widetilde Z`$ on $`m`$ arbitrary clock bits with $`O(1)`$ clean work, satisfying

```math
\|\widetilde ZJ-J(e^{i\phi}Z_m\otimes I_{\mathrm{dirty}})\|\le O(\eta),
```

would close the clock side of the proposed Weyl route for $`m=\Theta(L)`$, provided its actual work return is included. If the work return is only approximate, the literal inverse must act on that same work; the clean subspace cannot be assumed restored between calls without a hybrid bound. When full unitary closeness (including dirty helpers) is available, replacing $`Z`$ and $`Z^\dagger`$ by the circuit and its literal inverse incurs at most twice the clock error in the commutator.

An implementation of the entire commutator might require a weaker clock condition: errors invariant under the selected translations cancel. Thus an independent clock compiler is sufficient, not logically necessary. The addressed modular-translation primitive remains a separate cost even if the clock problem is solved. This note used the earlier $`O(N^{3/2})`$ endpoint upper benchmark. The later [operator-source compiler](OPERATOR_SOURCE_COMPILER.md) independently gives $`T=O(N+nL)`$ with $`a=2`$ and $`b\ge L+n+7`$. At $`L=N`$ and $`b\ge N+n+7`$, the current bounds are $`\Omega(N)`$ and $`O(N\log N)`$; the joint-clock question remains open.
