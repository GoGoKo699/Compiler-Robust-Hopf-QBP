# Modular lookup through dirty carry queries

This note continues [modular lookup](MODULAR_LOOKUP.md) and the [global XOR echo analysis](GLOBAL_XOR_ECHO.md) under the [constant-clean endpoint contract](../CONSTANT_CLEAN_ENDPOINT.md). Section 2 gives an exact modular table adder with $`O((N+m)\log(m+1))`$ T gates, $`O(m+\log N)`$ additional dirty work, and no initialized work. It batches the table-dependent carry computation across divide-and-conquer levels. The later weighted-subset-sum reduction remains an alternative interface with its own unresolved cost. Modular lookup alone does not supply a joint phase-clock compiler.

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

It needs one reusable dirty query bit in addition to the queries' peak work allocations. This particular per-output-bit decomposition still needs a bound on the *sum* of its query costs. Section 2 instead uses simultaneous carry queries while keeping their lower input bits unchanged through each complete correction. This permits exact erasure of the dirty carry masks.

## 2. An exact modular table adder with no clean work

### Statement and charged interfaces

For an arbitrary $`N=2^n`$-row table of $`m\ge1`$-bit constants, there is
a deterministic coherent Clifford+T implementation of $`U_f`$ with

```math
T=O\bigl((N+m)\log(m+1)\bigr),\qquad
G=O\bigl(Nm\log(m+1)\bigr),\qquad
a=0,
```

using $`2m+n`$ additional dirty wires beyond the address and target.
Here $`G`$ counts Clifford gates after exact Toffoli decomposition.
Every additional workspace wire is returned exactly, including its joint
state with an external reference; the designated target undergoes $`U_f`$.
If a caller supplies that target from its dirty budget, include its
$`m`$ wires as well: the complete dirty allocation is $`3m+n`$.

The [retained dirty-selector loader](BORROWED_WORKSPACE_COMPILER.md#2-exact-dirty-table-and-reflection-interpreter)
supplies the exact whole-word query

```math
Q_f:|x,v,z\rangle\longmapsto|x,v\oplus f(x),z\rangle
```

for arbitrary $`v,z`$, using $`n`$ dirty selectors, $`O(N)`$ Toffolis,
and $`O(Nm)`$ Clifford gates. The two selector traversals cancel their
unknown initial values; inserting an entire table row uses CNOTs into
each selected output bit. No initialized copy of $`f(x)`$ is supplied.
We charge every invocation below. The other cited primitive is the
exact [controlled increment, Gidney §2.10, Fig. 20](https://arxiv.org/html/1706.07884v2#S2.SS10):
it uses $`O(w)`$ gates on a $`w`$-bit word with one arbitrary dirty helper.
Its even-width extension has the same order and needs no initialized carry.

### Four queries compute all carries into an arbitrary mask

Borrow two $`m`$-bit words $`g,a`$. Fix any collection of disjoint
contiguous chunks of the target word. The desired query XORs the carry
out of every bit of each chunk into the corresponding bit of $`g`$,
with carry-in zero at the start of each chunk. Other bits of $`g`$ are
unchanged. Address $`x`$ and words $`y,a`$ must all return exactly.

First apply $`Q_f`$ to $`y`$, temporarily making $`p=y\oplus f(x)`$.
For a chunk starting at position $`b`$, define a reversible binary-linear
map $`P_p`$ by the ascending sweep

```math
g_i\longleftarrow g_i\oplus p_i g_{i-1},
\qquad i=b+1,\ldots,\text{last bit of the chunk}.
```

There is no connection between different chunks. The inverse sweep runs
in descending order. Put $`u_i=f_i(x)(1-p_i)`$ on chunk positions and
zero elsewhere. On those positions $`u_i=y_i^{\rm original}f_i(x)`$.
The carry recurrence is precisely

```math
c_i=u_i\oplus p_i c_{i-1},\qquad c_{b-1}=0,
\quad\text{so}\quad c=P_pu.
```

An XOR of $`u`$ into arbitrary $`g`$ needs two more whole-word queries:
apply $`Q_f`$ to $`a`$, apply the transversal Toffolis
$`g_i\mathrel{\oplus}=a_i(1-p_i)`$ on chunk positions, apply $`Q_f`$
to $`a`$ again, and repeat those Toffolis. Their difference is exactly
$`f_i(x)(1-p_i)`$; the original unknown $`a_i`$ cancels. Negative controls
use ordinary X gates, without initialized work.

The complete chronological carry-query word $`C`$ is

```math
Q_f(y),\quad P_p^{-1},\quad
Q_f(a),\quad \mathrm{AND}_{a,\neg p\to g},\quad
Q_f(a),\quad \mathrm{AND}_{a,\neg p\to g},\quad
P_p,\quad Q_f(y).
```

In its middle it performs
$`P_p(P_p^{-1}g\oplus u)=g\oplus c`$. Hence $`C`$ returns $`y,a`$
and implements the required carry XOR on all $`g`$ inputs. It uses four
queries and $`O(m)`$ other Toffolis and Clifford gates. A contiguous
$`s`$-bit chunk contributes exactly $`4s-2`$ carry-circuit Toffolis:
two propagation sweeps and two transversal AND passes. The semantic
operation $`C`$ is an involution.

### Dirty carry correction and divide-and-conquer order

At one level, split each current $`w`$-bit non-singleton block into a
lower chunk of width $`\lfloor w/2\rfloor`$ and an upper chunk of width
$`\lceil w/2\rceil`$. Use $`C`$ only on the lower chunks. For each block let
$`z`$ be the corresponding final lower-chunk bit of $`g`$, and let
$`c`$ be the true carry from adding that lower chunk of $`f(x)`$.
Let $`B`$ complement the entire upper chunk controlled by $`z`$, and
let $`I`$ increment it controlled by $`z`$. Both operations are applied
to every block at this level. Use the chronological word

```math
B,\quad C,\quad I,\quad C,\quad I^\dagger,\quad B.
```

The lower target chunks do not change during this word. Thus the two
calls to $`C`$ use identical inputs and restore *every* bit of $`g`$,
including carry-mask bits that are not used as controls. Between the
two complements, the upper-chunk translation is
$`(z\oplus c)-z=(1-2z)c`$. When $`z=1`$, bitwise complement
$`v\mapsto-1-v`$ reverses the sign of a translation. The two outer
complements therefore make the net translation exactly $`+c`$ for
both original values of the dirty control. No flag is assumed zero.

This level costs eight whole-word queries and $`O(m)`$ additional
arithmetic gates. The upper chunks are disjoint, and their widths sum
to at most $`m`$. The incrementer may borrow one bit of $`a`$: that
word has already been restored and is idle between carry queries.
Each increment returns this helper before another query uses $`a`$.

Process these levels from the whole word down to singleton blocks.
A parent's carry is added to its upper chunk before either child is
processed. This is the usual addition identity: the final upper chunk
is its original value plus its table constant plus the carry from the
original lower chunk. At the leaves, apply one final $`Q_f(y)`$ to
perform every one-bit addition. The same induction applies to unequal
chunk sizes, so no zero padding or initialized padding wires are needed.

There are at most $`\lceil\log_2 m\rceil`$ nontrivial levels. The
total query count is at most $`8\lceil\log_2m\rceil+1`$, and other
arithmetic costs $`O(m\log(m+1))`$. Substituting the charged XOR-loader
cost proves the stated T and Clifford bounds. The two borrowed words
and selectors are disjoint; all work is reused only after its exact
return. These basis identities use phase-correct native Toffolis, so
linearity proves the complete dirty/reference contract.

At $`m=N`$, this gives $`O(N\log N)`$ T gates for addressed modular
translation with $`O(N)`$ dirty work and no clean work. It improves this
arithmetic primitive without providing an $`O(N)`$-cost joint phase
clock or, by itself, a complete frame compiler. The theorem is a
construction and resource bound, without a novelty or optimality claim.

## 3. A valid sign-corrected echo on a one-hot dirty bank

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

## 4. Resource ledger and the remaining subset-sum problem

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

## 5. Why the recent linear constant adder is not a coherent subroutine here

Gidney's [*A Classical-Quantum Adder with Constant Workspace and Linear Gates*](https://arxiv.org/html/2507.23079v1) reports a $`4m\pm O(1)`$-Toffoli adder with three clean qubits, and a $`3m\pm O(1)`$ variant with two clean and $`m-2`$ dirty qubits. Sections 2.2–2.4 explicitly erase carries by X-basis measurements and later correct the resulting phases using the measurement outcomes. These results therefore do not directly give deterministic coherent circuits in the present no-measurement model.

Straightforward deferred measurement retains the carry records coherently instead of freeing their qubits; the streaming construction has linearly many such events. Obtaining constant clean width would require an additional coherent storage/erasure construction. This observation does not rule out a different coherent linear adder. Even such an adder, applied separately to every row, would not establish the desired whole-table bound.

## 6. Checks and scope of the result

Exact finite checks evaluated the carry expansion and descending decomposition for every pair $`(f,y)`$ at widths one through seven: 21,844 cases. Separate checks evaluated the complete sign-corrected echo for every table and every $`x,z,y`$ at $`(N,m)=(2,3)`$ and $`(4,2)`$: 69,632 cases, including return of the clean read flag. Negative controls detected both the omitted sign correction and the wrong ascending carry schedule; at $`m=2,f=1,y=1`$ the ascending schedule yields zero instead of two. These are checks of the displayed integer identities, not a gate synthesis or evidence for an unproved asymptotic cost. The universal justification is the algebra above.

The [modular compiler checks](../../tests/test_modular_lookup_compiler.py)
add finite all-input checks of the carry-query circuit and complete
divide-and-conquer addition, including odd word widths, query counts,
dirty-register return, and incorrect-sign/propagation-order negative
controls. An exact native small-instance check purifies all permitted
address, target, and dirty-work inputs. Its finite increment emitter is
quadratic in word width; the sharp asymptotic increment cost is the cited
linear primitive, not an inference from that emitter. The test module
states this boundary explicitly.

The modular arithmetic theorem is the constructive gain in this note.
The alternative weighted-subset-sum interpreter and the joint phase-clock
task have separate costs. No unrestricted lower bound or optimality
statement follows from these constructions.
