# Modular lookup followup: exact carry queries and a corrected dirty echo

This note continues [modular lookup](MODULAR_LOOKUP.md) and the [global XOR echo analysis](GLOBAL_XOR_ECHO.md) under the [constant-clean endpoint contract](../CONSTANT_CLEAN_ENDPOINT.md). It establishes two exact reductions, with their unresolved costs exposed. Neither reduction improves the current whole-frame upper bound. A recent linear-size constant adder also needs a model qualification: its carry cleanup uses measurements.

Throughout, $`N=2^n`$, the classical table is $`f:\{0,1\}^n\to\mathbb Z_{2^m}`$, and the desired operator is

```math
U_f|x,y,z\rangle=|x,y+f(x)\bmod2^m,z\rangle.
```

Every borrowed register is arbitrary, including entanglement with an external reference. Circuit equalities below are literal equalities, without input-dependent phases. Clean flags start and finish at zero. The endpoint of interest is $`m=L=N`$, constant clean width, and $`b=\Theta(N)`$ borrowed wires with sufficient constant-factor headroom for the explicitly listed allocations.

## 1. An exact carry-query decomposition without initialized carry storage

Write $`f_i(x)`$ and $`y_i`$ for the bits at position $`i`$, with position zero least significant. Define

```math
c_0(x,y)=0,\qquad
c_i(x,y)=
\mathbf 1\!\left[
 (y\bmod2^i)+(f(x)\bmod2^i)\ge2^i
\right]\quad(i>0).
```

Thus $`c_i`$ depends on the address and the lower $`i`$ input bits, but not on $`y_i`$ or higher bits. Define an involution $`G_i`$ that performs

```math
y_i\longmapsto y_i\oplus f_i(x)\oplus c_i(x,y),
```

and fixes the remaining registers. Apply these gates in **descending** order, from $`i=m-1`$ to $`i=0`$. When $`G_i`$ acts, every lower bit still has its original input value. The binary addition rule therefore sets $`y_i`$ to the corresponding sum bit. Later gates do not change it. Consequently

```math
U_f=G_0G_1\cdots G_{m-1},
```

where the rightmost factor acts first. The reversed word is the actual inverse. This proves correctness on every computational basis input and hence on arbitrary superpositions and reference-entangled inputs.

The carry has the Boolean expansion

```math
c_i(x,y)=
\bigoplus_{j=0}^{i-1}
\left[
 y_j f_j(x)
 \prod_{k=j+1}^{i-1}\bigl(y_k\oplus f_k(x)\bigr)
\right].
```

To prove it, set $`g_j=y_j f_j(x)`$ and $`p_j=y_j\oplus f_j(x)`$. The carry recurrence is $`c_{j+1}=g_j\oplus p_jc_j`$: generation and propagation cannot occur simultaneously because $`g_jp_j=0`$. Expanding the recurrence from $`c_0=0`$ gives the formula. Equivalently, a carry generated at position $`j`$ reaches position $`i`$ precisely when every intervening position propagates it. Two such generating terms cannot both be one, so XOR agrees with their logical union.

This identity does not provide a cheap circuit for those functions. In particular, the carry query is a function of both $`x`$ and the arbitrary lower target bits. Treating it as an ordinary unrestricted truth table gives $`N2^i`$ rows, not $`N`$. Its arithmetic structure must be used to obtain a better bound.

There is no need to *assume* a zero carry bit when reducing a query to an output flip. Suppose a circuit $`A_i`$ has already been implemented with the exact contract

```math
A_i:
|x,y_{<i},h,w\rangle\longmapsto
|x,y_{<i},h\oplus f_i(x)\oplus c_i(x,y),w\rangle,
```

where $`h`$ and $`w`$ may be dirty. In chronological order, apply

```math
A_i,\quad \mathrm{CNOT}_{h\to y_i},\quad
A_i,\quad \mathrm{CNOT}_{h\to y_i}.
```

The two CNOTs cancel the original unknown value of $`h`$ and leave exactly the desired flip. The second query has the same inputs because the lower target bits were not changed. Thus it also restores $`h,w`$. The semantic query is its own inverse; literal inversion may be used for its second implementation.

If the query costs are $`t_i`$ T gates and $`g_i`$ total gates, this reduction costs

```math
T=2\sum_{i=0}^{m-1}t_i,\qquad
G=2\sum_{i=0}^{m-1}g_i+2m.
```

It needs one reusable dirty query bit in addition to the queries' peak work allocations. The unresolved problem is to bound the *sum* of the complete query costs, including actual table insertion and coherent cleanup. A simultaneous XOR of all carries into a dirty bank does not establish these bounds: changing the lower target bits can change the inputs needed to erase that bank.

## 2. A valid sign-corrected echo on a one-hot dirty bank

The preceding XOR-echo obstruction applies to an uncorrected common interpreter. An address-dependent sign correction gives a useful exact reduction outside that premise.

Allocate $`N`$ dirty bits $`z_0,\ldots,z_{N-1}`$. Define the one-hot XOR query and a weighted subset sum by

```math
Q_x:z\longmapsto z\oplus e_x,\qquad
S_f(z)=\sum_{j=0}^{N-1}z_j f(j)\pmod{2^m}.
```

Suppose the following arithmetic interpreter has been compiled:

```math
D_f:|z,y,w\rangle\longmapsto
|z,y+S_f(z)\bmod2^m,w\rangle.
```

This is an operation on arbitrary $`z,y,w`$, with complete restoration of its work $`w`$. It is not a free oracle and it contains the entire classical table.

With rightmost factors acting first, let

```math
E_x=D_f^\dagger Q_xD_fQ_x.
```

After the rightmost query, the interpreter adds $`S_f(z\oplus e_x)`$. The second query restores the bank, and the inverse interpreter subtracts $`S_f(z)`$. Therefore

```math
E_x|x,z,y\rangle
=|x,z,y+(1-2z_x)f(x)\bmod2^m\rangle.
```

The unknown bank bit changes only the sign. To remove it, first read $`z_x`$ coherently into one clean bit $`q`$. Let $`B_q`$ complement every target bit when $`q=1`$ and otherwise do nothing. On an integer target, the complement is $`y\mapsto-1-y\pmod{2^m}`$, so

```math
B_q\mathrm{ADD}_d B_q
=\mathrm{ADD}_{(-1)^q d}.
```

When $`q=z_x`$, conjugating $`E_x`$ by $`B_q`$ therefore gives $`\mathrm{ADD}_{f(x)}`$. The operation $`B_q`$ consists of exactly $`m`$ CNOTs, with no T gates. Because the bank and address are restored by the echo, repeating the selected-bit read erases $`q`$.

The complement sign reversal is the standard arithmetic identity used in [offset commutator constructions, Section 2.9](https://arxiv.org/html/1706.07884v2). The point here is to expose the resulting dirty-table interface and its costs, without a priority claim for the underlying identity.

In chronological order, the complete construction is

```math
\mathrm{READ}(z_x\to q),\ B_q,\ Q_x,\ D_f,\ Q_x,
\ D_f^\dagger,\ B_q,\ \mathrm{READ}(z_x\to q).
```

For each basis input its output is exactly $`|x,z,y+f(x),0\rangle`$, including restored interpreter work. This proves the full dirty/reference contract by linearity. The proof does not measure $`z_x`$ or replace the dirty bank by a classical random variable.

Without the sign correction, $`m=2`$, $`z_x=1`$, $`f(x)=1`$, and $`y=0`$ give output three instead of one. With the correction, they give one. There is no contradiction with the earlier obstruction: the read and the controlled complement introduce address-dependent, noncommuting target operations outside its specified translation-only/common-interpreter interface.

## 3. Resource ledger and the remaining subset-sum problem

The two bank operations needed above have independent complete implementations:

- The retained dirty-selector XOR loader implements $`Q_x`$ with $`O(N)`$ Toffolis and $`O(n)`$ reserved dirty selector wires. Its table is the one-hot table, so each selected row flips one bank bit. The loader's own dirty-selector cancellation and inverse are included in this cost. We use the conservative $`O(N(1+n))`$ total-gate allowance for address and selector bookkeeping.
- A selected-bit read routes bank bit $`z_x`$ to a fixed slot, CNOTs it into $`q`$, then reverses the routing. A binary selection network needs at most $`N-1`$ controlled swaps in each routing direction. Hence one read costs $`O(N)`$ phase-correct Toffolis and gates, without an initialized copy of the bank.

For a compiled interpreter with costs $`T_D,G_D`$, the resulting modular lookup has

```math
T_{U_f}=2T_D+O(N),\qquad
G_{U_f}=2G_D+O(N(1+n)+m).
```

Peak space consists of the $`m`$-bit target, the $`N`$ dirty bank bits, one clean read flag, the separately reserved $`O(n)`$ dirty selectors, and the interpreter's additional work. If the interpreter requires $`c_D`$ clean work bits, the construction requires $`c_D+1`$: the read flag remains live throughout both interpreter calls and cannot also serve as an initialized adder carry. Selector and interpreter dirty work can be reused between calls if their contracts restore it; no wire may simultaneously be counted as a live bank bit and a separately reserved helper. Thus an interpreter using constant clean work and $`O(N)`$ additional dirty work still fits the endpoint's order of space, with an explicit sufficiently large constant in $`b=\Theta(N)`$.

A direct implementation of $`D_f`$ performs, for every $`j`$, the constant addition $`y\mapsto y+z_jf(j)`$. Coherent restricted-work controlled offsets have an available $`O(m\log m)`$ gate/Toffoli upper bound; see Gidney's [reversible dirty-arithmetic constructions, Section 2.9](https://arxiv.org/html/1706.07884v2), building on Häner, Roetteler and Svore. Consequently this route currently supplies only the conservative bound $`T_D,G_D=O(Nm\log m)`$. Even granting an $`O(m)`$ coherent controlled offset per row leaves the direct implementation at $`O(Nm)`$. Neither statement is a lower bound for jointly compiled weighted subset sums.

The missing primitive can now be stated precisely: compile the entire fixed weighted subset sum $`S_f(z)`$ into an arbitrary word with constant clean work, $`O(N)`$ additional dirty space, and $`T_D=O(N)`$, $`G_D=O(N^2)`$ when $`m=N`$. Such a result would imply an $`O(N)`$-T modular table query through this reduction. It would still need integration with a charged clock and a complete frame construction; it is not by itself a frame compiler.

Viewing the table as a Boolean matrix does not yet provide that interpreter. If $`a_{ij}=f_i(j)`$, its columnwise arithmetic obeys

```math
w_i=\kappa_i+\sum_j a_{ij}z_j,\qquad
(S_f(z))_i=w_i\bmod2,\qquad
\kappa_{i+1}=\lfloor w_i/2\rfloor,\qquad \kappa_0=0.
```

Clifford XOR operations supply the parity part of a column. They do not supply its integer carry $`\kappa_{i+1}`$ or a restored storage arrangement for that carry. Moreover, $`z`$ ranges over *all* bitstrings: an implementation valid only when it is one-hot is insufficient, because the one-hot query is applied to an arbitrary dirty bank. This is the precise carry and workspace obligation left by the reduction.

## 4. Why the recent linear constant adder is not a coherent subroutine here

Gidney's [*A Classical-Quantum Adder with Constant Workspace and Linear Gates*](https://arxiv.org/html/2507.23079v1) reports a $`4m\pm O(1)`$-Toffoli adder with three clean qubits, and a $`3m\pm O(1)`$ variant with two clean and $`m-2`$ dirty qubits. Sections 2.2–2.4 explicitly erase carries by X-basis measurements and later correct the resulting phases using the measurement outcomes. These results therefore do not directly give deterministic coherent circuits in the present no-measurement model.

Straightforward deferred measurement retains the carry records coherently instead of freeing their qubits; the streaming construction has linearly many such events. Obtaining constant clean width would require an additional coherent storage/erasure construction. This observation does not rule out a different coherent linear adder. Even such an adder, applied separately to every row, would not establish the desired whole-table bound.

## 5. Checks and scope of the result

Exact finite checks evaluated the carry expansion and descending decomposition for every pair $`(f,y)`$ at widths one through seven: 21,844 cases. Separate checks evaluated the complete sign-corrected echo for every table and every $`x,z,y`$ at $`(N,m)=(2,3)`$ and $`(4,2)`$: 69,632 cases, including return of the clean read flag. Negative controls detected both the omitted sign correction and the wrong ascending carry schedule; at $`m=2,f=1,y=1`$ the ascending schedule yields zero instead of two. These are checks of the displayed integer identities, not a gate synthesis or evidence for an unproved asymptotic cost. The universal justification is the algebra above.

The useful progress is an exact carry-query interface and a sign-corrected one-hot reduction whose overhead fits the endpoint resources. Their remaining costs are explicit. No unrestricted modular-lookup lower bound, new optimality claim, or improvement of the existing $`O(N^{3/2})`$ whole-frame upper bound follows from this note.
