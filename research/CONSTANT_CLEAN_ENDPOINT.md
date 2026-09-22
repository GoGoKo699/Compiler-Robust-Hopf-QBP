# Constant-clean Hopf compilation: resume brief

**Status: active research; endpoint still open.** Repository integration is complete. The [checked-progress report](CONSTANT_CLEAN_PROGRESS.md) records the subsequent dirty-rank compression lemma, restrictions on global program/clock interfaces, and conditional constructive reductions. None changes the unrestricted bounds below. This brief and the linked technical appendices contain the mathematical state needed to continue without the earlier conversation or scratch workspace.

## Target and model

Let $`N=2^n`$. The target is the **prescribed complete real Hopf frame**

```math
W=L_{n-1}\cdots L_0,
\qquad
R_y(\theta)=e^{-i\theta Y}
=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}.
```

For depth $`d`$ and prefix $`p\in\{0,1\}^d`$, $`L_d`$ applies $`R_y(\theta_{d,p})`$ to the pair
$`\{|p,0,0^{n-d-1}\rangle,|p,1,0^{n-d-1}\rangle\}`$, and is identity on the remaining basis states. The angles are supplied classically. Their complete tuple fixes all columns, including at singular chart coordinates. State preparation on $`|0^n\rangle`$ alone does not meet this target. The rotation convention has no factor of $`1/2`$ in its exponent.

There are $`a`$ initially zero clean qubits and $`b`$ arbitrary dirty qubits, with total width $`q=n+a+b`$. A compiler produces a deterministic coherent unitary $`V`$ from the fixed native Clifford and T/T-dagger matrices, with all-to-all connectivity. T and T-dagger each cost one; Clifford cost is tracked separately. There is no measurement, reset, physical postselection, supplied magic state, or uncharged catalyst. Classical compilation work is separate from quantum gate counts.

If $`J_a`$ appends the zero clean register, the contract is

```math
\boxed{\|VJ_a-J_a(W\otimes I_b)\|_{\mathrm{op}}\le\eta.}
```

This bounds the complete output, including work leakage, uniformly over system and dirty inputs and their reference entanglement. It fixes the common scalar phase as well as relative phases. Exact dirty return is available in the retained borrowed compiler; a new approximate-return construction must include its full return error in this same norm. Use

```math
0<\eta\le1/64,\quad
L=\max\{6,\lceil\log_2(1/\eta)\rceil\},\quad
h=1+\lceil\log_2(L+n+2)\rceil.
```

All frontier statements below concern the worst case over prescribed angle tuples, not a lower bound for every individual frame.

## What is settled, and the remaining gap

The general retained lower benchmark is

```math
B(n,a,b,L)=\sqrt{NL}+L+\frac{NL}{q}.
```

| Regime | Established result |
|---|---|
| Sufficient clean reservation $`a\ge C(n+h)`$, every retained precision and dirty budget | $`\tau^*_{F,\mathbb R}=\Theta(B)`$, with $`O(NL)`$ Clifford cost |
| Every clean budget, provided $`h+b\le c\sqrt N`$ for fixed $`c>0`$ | $`\tau^*_{F,\mathbb R}=\Theta_c(B)`$ |
| Arbitrary clean/dirty budgets, retained borrowed-work construction | $`T=O(NL/q+L\sqrt N)`$, $`G=O(NL)`$ |
| **Selected endpoint:** $`a=O(1), b=\Theta(N), L=N`$ | **Lower $`\Omega(N)`$, available upper $`O(N^{3/2})`$** |

At $`L=N`$, $`h=\Theta(n)`$, so the first row gives $`\Theta(N)`$ with a sufficiently large fixed multiple of $`n`$ clean qubits. It does not give the same result with a constant number of clean qubits. The sufficient clean reservation is not proved necessary.

The all-clean-budget corollary has a short splice proof. If the clean reservation fits, use the shifted-source compiler. Otherwise $`q<(C+1)n+Ch+b=O_c(\sqrt N)`$, and the borrowed compiler's $`L\sqrt N`$ term is absorbed by $`NL/q`$. At the selected endpoint $`b=\Theta(N)`$, that hypothesis fails. Rebalancing these same upper bounds alone does not close the gap. The sufficient-clean construction and general lower bounds are proved in the [fault-tolerant compiler theorem](../docs/FAULT_TOLERANT_COMPILER.md). The separate [borrowed-workspace appendix](constant_clean/BORROWED_WORKSPACE_COMPILER.md) proves the arbitrary-budget upper bound and this splice.

## The strongest retained source-interface result

Deliberately grant the processing circuit a freely supplied, independent source density $`\rho`$ on at most $`s`$ qubits. It may depend on the exponent $`k`$ and precision $`L`$, have arbitrary or transcendental amplitudes, and be known classically to the compiler. All other supplied nonstabilizer resources count in this source; other initialized helpers are pure stabilizer states. Mathematical acceptance projects $`f`$ private bits onto zero. It adds no physical postselection to the frame model.

If the accepted source marginal is returned exactly with attenuation $`2^{-k}`$, then, for processing T-count $`\tau`$,

```math
\Phi(\rho)=4^{-k}\rho
\quad\Longrightarrow\quad \boxed{\tau+2f\ge4k.}
```

For every $`k=1,\ldots,L`$, suppose the complete accepted vector is within $`2^{-L}`$ of $`2^{-k}`$ times the intended normalized output with its source returned. Mixed sources use an untouched purifying reference. Each exponent may have a different source and circuit. Then

```math
\boxed{4^s(R+s+6)\ge L-2,\qquad
R=\max_{1\le k\le L}(\tau_k+2f_k).}
```

Thus fixed source size and fixed projected work force some kernel to cost $`\Omega(L)`$. Merely choosing a new high-precision one-qubit source does not evade this contract. Polylogarithmic $`R`$ requires $`s\ge\tfrac12\log_2 L-O(\log\log L)`$; optimality of this source-size dependence is not known.

The [full proof](constant_clean/SOURCE_CHANNEL_PROOF.md) attaches arithmetic to the reduced source channel, not to the source. Its $`D=4^s`$ dimensional Pauli matrix satisfies $`F\in(\sqrt2)^{-(\tau+2f)}\mathrm{Mat}_D(\mathbb Z[\sqrt2])`$, and its Galois conjugate is another physical map. An algebraic-integrality argument gives the exact bound. A determinant-norm and minimum-singular-value estimate gives the uniform robust bound, including nonnormal channels.

This is a **maximum-over-exponents interface bound**, not an additive cost across frame stages. A probability-only promise or a normalized-success promise omitting the correct success weight is insufficient for the robust statement. A source initially correlated with logical/dirty input is outside its independent-source premise. No theorem says that every frame compiler exposes this attenuation interface. In particular, one globally combined $`O(L)=O(N)`$ operation is fully compatible with the desired endpoint.

## Routes already audited

| Route | What survives, and what is missing |
|---|---|
| Relabel arbitrary dirty bits as a prepared precision source | A rank argument forbids exposing more independent pure source wires than the available clean initialization while preserving every input. Conditional system sectors supply work only by reducing the active logical dimension. |
| Shrink the existing nilpotent shift source | If $`S^D=0`$, $`\|Sg-\lambda g\|\ge(1-\lambda)\lambda^D/(1-\lambda^D)`$. The current source is already optimal in exponential order for that shift. This is not a general source-width bound. |
| Replace it by a one-qubit weighted source | $`B=\left(\begin{smallmatrix}0&1\\1/4&0\end{smallmatrix}\right)`$, $`v=(2,1)/\sqrt5`$ obey $`Bv=v/2`$. A constant-size accepted dilation exists, and preparing an approximate $`v`$ costs $`O(L)`$. The identity $`B^2=I/4`$ does not supply cheap variable attenuation; the source-channel theorem covers the returned-column loophole. |
| Conditional-sector transfer of the current compiler | Its source-fit condition gives $`2^mL'\le2^{a-3}N`$ for local precision $`L'=L+n+O(1)`$. At fixed $`a`$, the resulting upper certificate already contains $`\Omega(L'\sqrt N)`$. This is a limitation of that construction, not a general lower bound. |
| Radix regrouping | Quotient and remainder still need $`\log L+O(1)`$ address bits, or a charged streamed replacement. High-radix amplitudes and their normalization are not automatically native-exact. |
| One global XOR-loaded interpreter echo | For $`E_f(z)=D_{z\oplus f}D_z^\dagger`$ with the same returned-source subspace, uniform error $`\eta`$ forces $`\|U_f-U_f^\dagger\|\le2\eta`$, and $`\|[U_f,U_g]\|\le4\eta`$ for two masks. Exact targets are commuting involutions. For the stated $`R_y`$, $`\eta\ge|\sin\theta|`$. Longer or nonunitary constructions are outside this theorem. |
| Independent dyadic factors of a dirty clock | Separately restored factor modules cost $`\Omega(L^2)`$ when clock width is $`\Theta(L)`$. A jointly optimized clock has only the retained $`\Omega(L)`$ lower bound. Sharing a nonstabilizer intermediate invalidates the factorwise summation premise. |
| Turn XOR table insertion into modular addition | The residual $`(z\oplus f)-z=f-2(z\mathbin{\&}f)`$ depends on dirty data. A valid modular echo exists, but cheap carry-aware table insertion is an unproved component. |
| Exact fine phase catalysis | Literal dyadic order $`2^p`$ with exact product return needs at least $`p-3`$ supplied/initialized source wires, independently of dirty width. This does not prove an approximate clean-space bound; arbitrary common phases or normalizations cannot be silently canceled. |

The [appendix index](README.md) supplies the detailed source, XOR, clock, modular, and phase arguments. These results restrict proposed interfaces; none strengthens the selected whole-frame lower bound beyond $`\Omega(N)`$.

### An involution lift does not by itself implement the target

Every unitary $`U`$ has a Hermitian involution lift

```math
\mathcal I_U=\begin{pmatrix}0&U\\U^\dagger&0\end{pmatrix},
\qquad \mathcal I_U^2=I.
```

This removes an algebraic non-involution objection for one abstract target. It supplies no cheaper interpreter. Indeed

```math
\mathcal I_U=\mathrm{diag}(U,I)\,(X\otimes I)\,
\mathrm{diag}(U^\dagger,I),
```

so implementing it by controlled $`U`$ and $`U^\dagger`$ assumes the original hard operation. Conversely, applying $`\mathcal I_U`$ to $`|1\rangle|\psi\rangle`$, followed by an X on the flag, implements $`U`$ and restores the flag. A cheap lift would be useful only after its target-dependent gates are independently synthesized and charged. Multiple loaded masks must still satisfy the common-interpreter consistency conditions; individually lifting each desired program does not make those conditions automatic.

## Constructive proof obligations

The most direct constructive target is **one complete global block**, rather than a new family of cheap tiny-scalar kernels. For every prescribed $`W`$ at $`L=N`$, exhibit an actual native circuit $`U`$ using a fixed constant $`c`$ of clean work and $`b=\Theta(N)`$ arbitrary dirty work, with

```math
2J_c^\dagger UJ_c=M,\qquad
\|M-W\otimes I_b\|\le\eta/4,
\quad T(U)=O(N),\quad G(U)=O(N^2).
```

Here $`M`$ acts on the full system/dirty space. All source preparation, table insertion, addresses, selectors, failures, arithmetic, and inverse operations are part of $`U`$; its off-initialized-subspace action must be a defined unitary. The constant $`c`$ must not hide an $`n`$-bit address, $`\log L`$-bit precision index, or growing history register.

This block interface is sufficient because, with $`R_c=I-2J_cJ_c^\dagger`$, the actual amplification word

```math
F=-UR_cU^\dagger R_cU
```

has accepted block $`3A-4AA^\dagger A`$, where $`A=M/2`$. The retained complete-isometry estimate is
$`\|FJ_c-J_c(W\otimes I_b)\|\le4\|M-W\otimes I_b\|`$ when the latter norm is at most $`1/4`$. The reflection includes every initialized private register; it costs only a constant for fixed $`c`$. This states a sufficient interface, not an existing construction. A direct whole-frame unitary meeting the same budget is equally sufficient.

A second live route is a fully charged dirty Weyl commutator. For an $`m`$-bit word, define $`X|y\rangle=|y+1\bmod2^m\rangle`$, $`Z_m|y\rangle=e^{2\pi i y/2^m}|y\rangle`$. Then

```math
Z_mX^{f(x)}Z_m^\dagger X^{-f(x)}
=e^{2\pi i f(x)/2^m}I.
```

At $`m=\Theta(L)`$, this requires both a constant-clean joint clock costing $`O(m+L)`$ T gates and a carry-aware table translation with a charged ledger, or a direct commutator construction that avoids separate implementations. The hypothetical modular-lookup target is $`O(m+\sqrt{Nm}+Nm/K)`$, where $`K`$ is bank capacity **after** other reservations. At $`m=N`$, the bank-balancing choice is one word; it leaves the original hard modular lookup. Even both primitives need a determinant-one/real-rotation reduction and full prefix/suffix composition with the desired total cost. Their algebra alone is not a frame compiler.

The [current progress report](CONSTANT_CLEAN_PROGRESS.md) adds a direct phase-bank reduction and sharper tests for candidate interfaces. The next construction must specify the complete operator identity and register ledger. Charge where the classical table actually enters. Verify the actual inverse on every work state and the joint dirty/reference action before optimizing its asymptotics.

## Success criteria and stopping claims

A constructive resolution must prove a uniform $`O(N)`$-T family with a specified constant clean allocation, $`\Theta(N)`$ dirty allocation, and the complete error contract. An explicit $`o(N^{3/2})`$ construction would be intermediate progress, with its remaining gap stated. Alternatively, a stronger lower bound must apply to unrestricted admissible frame circuits, not sum costs of a chosen source, clock factorization, or correction architecture.

Finite full-space checks should exercise dirty superpositions/reference entanglement, literal phase, both inverse orders, invalid work encodings, and all private flags. They validate fragile interfaces; the general asymptotic proof remains necessary. No endpoint gate emitter, practical benchmark, optimal growing-source dependence, or exhaustive novelty certification is currently claimed. The arbitrary-source robust tradeoff is a supporting theorem; the exact spectral argument alone should not be presented as a new general theory of catalysis.
