# CP31: modular table lookup on arbitrary borrowed words

> Preserved technical appendix. Read the [current endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md) for the governing model, remaining gap, and resume task. [Provenance](PROVENANCE.md) records the source and editorial scope.
> Historical finite-check summaries and scratch reproduction commands are omitted; the complete mathematical argument and its scope are retained.

Investigation outcome: no claimed $`O(N)`$-T implementation at $`m=N`$ with constant clean workspace. There is an exact modular-bank echo, but its loader is not the existing XOR loader. A broad natural XOR-echo substitution is impossible. The uniform resource target also needs an additive $`m`$ term outside the endpoint regime.

## 1. Desired primitive and unavoidable linear word cost

For a known classical table $`f:\{0,1\}^n\to\mathbb Z_{2^m}`$, with $`N=2^n`$, the desired full-space unitary is

```math
U_f|x,y,z\rangle=|x,y+f(x)\bmod2^m,z\rangle.
```

Here $`y`$ is arbitrary logical/borrowed input, $`z`$ denotes additional arbitrary borrowed work, and every helper returns jointly with an external reference. The table is encoded by a finite classical description, not a free oracle.

A uniform target should be

```math
T=O\!\left(m+\sqrt{Nm}+\frac{Nm}{K}\right),\tag{1}
```

plus any separately unresolved selector reservation. Dropping $`m`$ is not valid for all $`m,N`$. For $`f\equiv1`$, the operation is the exact $`m`$-bit incrementer. Supply its low $`m-1`$ input bits in $`|+\rangle`$ and its most significant bit in $`|0\rangle`$; fix address and dirty inputs to any stabilizer states. Its output most-significant-bit Pauli expectation is

```math
\langle Z_{m-1}\rangle=1-2^{2-m}.
```

For $`m\ge3`$, this rational has $`\sqrt2`$-adic denominator exponent $`2m-4`$. A Clifford+T circuit with $`\tau`$ T/T-dagger gates and pure stabilizer inputs has all Pauli expectations in $`(\sqrt2)^{-\tau}\mathbb Z[\sqrt2]`$. Hence

```math
\boxed{\tau\ge2m-4.}\tag{2}
```

No acceptance projection or supplied nonstabilizer source is present here. Extra initialized stabilizer helpers and arbitrary dirty helpers do not evade the bound, since a stabilizer dirty specialization is permitted and tracing restored work adds no denominator. The $`+m`$ term is absorbed by $`\sqrt{Nm}`$ when $`m\le N`$, including the desired $`m=N`$ endpoint. This is a worst-case exact modular-lookup lower bound, not an approximate-frame result.

## 2. Why the XOR dirty-bank echo cannot simply become an addition echo

The retained loader performs

```math
Q_f:|x,z\rangle\mapsto|x,z\oplus f(x)\rangle.
```

If one copies a loaded word into the target by **modular addition**, uncomputes the XOR load and subtracts the original dirty word, the resulting target displacement is

```math
(z\oplus f)-z=f-2(z\mathbin{\&}f)\pmod{2^m}.\tag{3}
```

For example, at $`m=2,f=1`$, the displacement is $`+1`$ when $`z=0`$ and $`-1=3`$ when $`z=1`$. The bank itself can be perfectly restored while the target remains correlated with its unknown value. This violates the complete dirty/reference contract.

There is a useful wider obstruction. Fix an arbitrary word $`c`$. Suppose a proposed conversion uses a single dirty word $`z`$, repeatedly applies $`z\mapsto z\oplus c`$, and otherwise only applies commuting translations to $`y`$ whose amounts are fixed functions of the *current* dirty word. The functions may also depend on an unchanged address $`x`$, but may not directly contain the unknown table value $`c`$; all $`c`$-dependence is through that XOR access. Assume it restores $`z`$ for all $`c`$, and is identity on $`y`$ for $`c=0`$.

The bank alternates between $`z`$ and $`z\oplus c`$. All target translations commute, so the net displacement is

```math
G_0(z)+G_1(z\oplus c).
```

The $`c=0`$ promise says $`G_0(z)=-G_1(z)`$. Thus for one fixed function $`H`$ the displacement is

```math
H(z\oplus c)-H(z).
```

If this were independent of $`z`$, equal to $`d(c)`$, substituting $`z\oplus c`$ for $`z`$ changes its sign. Consequently

```math
\boxed{2d(c)=0\pmod{2^m}.}\tag{4}
```

Only zero or half-period translations can result. In particular, no number of such restored XOR-load/add/subtract alternations implements arbitrary $`d(c)=c`$ when $`m>1`$. This encompasses replacing the CNOT copies in the existing same-bank echo by arithmetic copies, and allowing any fixed reinterpretation $`H`$ of the dirty word.

Equation (4) is an interface obstruction. It does not cover circuits that nonlinearly change dirty banks between oracle calls, use several interacting banks, alter the address, apply noncommuting target operations, or insert target-dependent arithmetic in another form. It is not a lower bound for unrestricted modular lookup. Accessing the table value directly inside the fixed functions would simply assume another implementation of the missing primitive.

## 3. A valid modular-bank echo and its conditional resource lemma

Split $`x=(u,r)`$, where $`r`$ chooses one of $`\lambda`$ words in a chunk. Let $`F_j(u)=f(u,j)`$. Suppose a **modular** chunk loader has been implemented:

```math
L_f^+:|u,z_0,\ldots,z_{\lambda-1}\rangle
\mapsto|u,z_0+F_0(u),\ldots,z_{\lambda-1}+F_{\lambda-1}(u)\rangle.
```

Let $`R`$ route word $`z_r`$ to slot zero, and $`A`$ add slot zero modulo $`2^m`$ into $`y`$. In chronological order apply

```math
L_f^+,\ R,\ A,\ R^\dagger,\ (L_f^+)^\dagger,\ R,\ A^\dagger,\ R^\dagger.\tag{5}
```

The first addition supplies $`z_r+f(x)`$, the second subtracts $`z_r`$, and all banks and routing are restored. Thus (5) implements $`U_f\otimes I_z`$ exactly, including every reference-entangled input. The modular loader and its actual inverse are each used once; the word adder and inverse are each used once; routing appears four times.

With one clean carry qubit, a coherent ripple adder on **two arbitrary quantum words** has $`O(m)`$ Toffoli and Clifford cost and restores the carry. Routing costs $`O(\lambda m)`$ phase-correct Fredkins. Therefore a modular chunk loader with costs $`(T_L,G_L)`$ gives

```math
T_{U_f}=O(T_L+\lambda m+m),\qquad
G_{U_f}=O(G_L+\lambda m+m),\tag{6}
```

using $`\lambda m`$ dirty bank wires, the adder's constant clean carry allocation, and the loader's separately charged selectors/helpers. Define $`K`$ to be the usable dirty **bank capacity after reserving those other selectors/helpers**. Thus the physical allocation satisfies $`\lambda m\le K`$; selectors are never spent a second time from the same bank budget. Sufficient constant-factor dirty headroom preserves the desired endpoint order. The literal reversed word has the same cost. Exact dirty-bank return permits reuse without multiplying the peak bank width.

If a loader satisfying $`T_L=O(N/\lambda+\lambda m)`$, $`G_L=O(Nm)`$, and **constant clean work** were independently established, with its dirty selectors/helpers reserved as just stated, choosing

```math
\lambda\asymp\max\{1,\min\{\sqrt{N/m},K/m\}\},
```

when $`K\ge m`$, would give (1), up to integer rounding and the loader's explicit selector cost. This is a conditional statement. At $`m=N`$, the balancing choice is $`\lambda=1`$, so the required loader is already the difficult single-word modular table primitive; (5) does not solve it by itself.

The $`\lambda m`$ term in the uniform loader target has an independent exact witness. Set every table value to one, and give every bank its own pure stabilizer increment input from Section 1. Measure the **single product Pauli** consisting of the most-significant-bit Z in each bank. The promised complete loader output has expectation

```math
\left(1-2^{2-m}\right)^\lambda
=\frac{(2^{m-2}-1)^\lambda}{2^{\lambda(m-2)}}.
```

For $`m\ge3`$, its numerator is odd. Thus its denominator exponent gives

```math
\boxed{T_L\ge2\lambda(m-2).}\tag{7}
```

This lower bound applies to an arbitrary jointly optimized simultaneous loader circuit, including arbitrary restored dirty helpers. It follows from one Pauli expectation; it is **not** a sum of independent per-bank lower bounds. The balanced endpoint $`m=N,\lambda=1`$ remains compatible with $`O(N)`$ T gates.

## 4. Why the retained loader does not supply the hypothesis

For XOR loading, the selection predicate for one table row is computed once. Its arbitrary $`\lambda m`$-bit row string is then inserted into banks by CNOTs, so the row's data size contributes Clifford gates but no additional T gates. This is the source of the $`N/\lambda`$ selection term.

For modular loading, the corresponding row action is a selected modular addition of arbitrary constants into $`\lambda`$ dirty words. It contains carry logic. Replacing each CNOT insertion by such a constant addition changes the T ledger and is not an invocation of the existing theorem. Even **granting** an $`O(m)`$-T selected constant adder per word, the direct row-by-row loader has the available bound $`O((N/\lambda)\lambda m)=O(Nm)`$, before selector overhead. This is a charge for that implementation, not an $`\Omega(Nm)`$ lower bound on arbitrary loaders. Some restricted-work constant adders have larger conservative bounds and must be charged at their actual cost.

The retained canonical report Section 4.6 already supplies an exact XOR loader with **dirty selectors**. Its two depth-first traversals cancel the selector-dependent unwanted XORs, use $`k=n-\log_2\lambda`$ arbitrary selector wires, cost $`O(N/\lambda)`$ Toffolis, and restore all selectors. The proof extends from one-bit banks to $`m`$-bit words because the inserted table data still uses CNOTs. Dirty selection itself is therefore not a newly open clean-workspace gap.

The modular construction must specify and charge its use of selector capacity, reserved before defining $`K`$, and must implement the carry-dependent row action with complete restoration. The retained cancellation is XOR-linear and does not prove that replacing its row CNOTs by modular constant additions preserves the same T ledger or cancellation. This is part of the missing modular data-insertion construction, not a reason to reintroduce an $`O(n)`$-clean selector premise.

## 5. Primary-source audit and next constructive interface

The existing XOR SelectSwap result is Low, Kliuchnikov and Schaeffer, [*Trading T-gates for dirty qubits in state preparation and unitary synthesis*](https://arxiv.org/html/1812.00954v2). The distinction between XOR and integer addition is algebraic, independent of constant-factor improvements.

A recent primary update, Motlagh and Pocrnic, [*Halving the cost of QROM*](https://arxiv.org/html/2605.20334v1), improves dirty **XOR** QROM constants using SelectCopy and batched queries. Its stated primitive loads classical bitstrings; it does not establish the modular loader in Section 3 or remove the selector obligation. This paper should be included in a future broad lookup prior-art audit; no new asymptotic frame conclusion is inferred here.

For the genuine two-input word adder used in (5), a standard coherent reference is Cuccaro et al., [*A new quantum ripple-carry addition circuit*](https://arxiv.org/abs/quant-ph/0410184). No measurement-based temporary-AND cleanup is imported. For the distinction between general word addition and restricted-work classical-constant addition, see Häner, Roetteler and Svore, [*Factoring using 2n+2 qubits with Toffoli based modular multiplication*](https://arxiv.org/abs/1611.07995), whose dirty-work constant-adder construction has $`O(m\log m)`$ size. This is a conservative available construction, not an optimality statement.

The useful next constructive object is therefore a complete constant-clean modular chunk loader with cheap data insertion, or a different whole-table arithmetic factorization. The simple XOR-mask echo cannot provide it. The constant-clean $`b=\Theta(N),L=N`$ full-frame frontier remains unchanged by this investigation.
