# The fault-tolerant compiler for the complete real frame

[← Exact compiler](COMPILER_THEOREM.md) · [QBP consequence](QBP_CONSEQUENCE.md) · [Remaining constant-clean endpoint](../research/CONSTANT_CLEAN_ENDPOINT.md)

The exact compiler counts arbitrary one-qubit gates and CNOTs. This chapter
keeps the same prescribed Hopf frame and changes the gate set to Clifford+T.
Precision and the distinction between initialized and borrowed workspace now
matter. With a sufficient logarithmic clean reservation, the worst-case
T-count is

```math
\Theta\!\left(\sqrt{NL}+L+\frac{NL}{n+a+b}\right).
```

The upper bound implements the whole frame, including its marker columns.
Its high-precision construction prepares one geometric source, passes it
through all residual corrections, and reverses its actual preparation once.
A retained failure counter makes this reuse coherent. The proof below
accounts for the source, rejected branches, actual inverses, and reflection
work as circuit resources.

## 1. Target, resources, and theorem

Use the rotation convention

```math
R_y(\theta)=e^{-i\theta Y}
=\begin{pmatrix}\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta\end{pmatrix}.
```

For a supplied angle tuple, let

```math
W=L_{n-1}\cdots L_0,\qquad N=2^n,
```

```math
L_d=I+\sum_{p=0}^{2^d-1}|p\rangle\langle p|
\otimes(R_y(\theta_{d,p})-I)
\otimes|0^{n-d-1}\rangle\langle0^{n-d-1}|.
\tag{1}
```

The rightmost layer acts first. The complete angle tuple specifies the
continuation at singular charts; the compiler may not replace this frame
by another unitary with the same first column.

There are $`n`$ system qubits, $`a`$ clean qubits initialized to zero, and
$`b`$ borrowed qubits in an arbitrary joint state. Write

```math
q=n+a+b,\qquad
L=\max\{6,\lceil\log_2(1/\eta)\rceil\},\qquad
h=1+\lceil\log_2(L+n+2)\rceil,
\quad 0<\eta\leq1/64.
```

Let $`J_a`$ append the clean zero state to the system and borrowed registers.
A valid circuit $`V`$ satisfies the complete-isometry contract

```math
\left\|VJ_a-J_a(W\otimes I_b)\right\|\leq\eta.
\tag{2}
```

The norm is the operator norm on the entire system-and-borrowed input
space. Tensoring an arbitrary reference preserves this bound. Thus (2)
controls the logical action and joint clean-work return, including coherent
garbage. Literal phases are fixed; no input-dependent or common phase is
discarded in the upper-bound contract. In fact, the construction returns
the borrowed registers **exactly**, jointly with their reference, after
every table query. Only the designated initialized approximation work has
the return error in (2).

The model is a fixed coherent circuit over $`H,S,\mathrm{CNOT},T,T^\dagger`$,
with all-to-all logical connectivity. A T or T-dagger counts as one
non-Clifford gate. Clifford count means elementary one- and two-qubit
Clifford gates. There are no measurements, resets, supplied magic states,
or parameter-dependent catalyst states. Classical coefficient evaluation,
word synthesis, and table generation are separate preprocessing tasks.

**Theorem 1 — matching T-count with a logarithmic clean reservation.**
There is an absolute constant $`C`$ such that, for every $`n\geq1`$, every
specified real frame (1), and every budget

```math
a\geq C(n+h),\qquad b\geq0,
```

there is a circuit satisfying (2), using at most those budgets, with

```math
T=O\!\left(\sqrt{NL}+L+\frac{NL}{q}\right),
\qquad G_{\rm Clifford}=O(NL).
\tag{3}
```

The worst-case minimum T-count over this frame family is

```math
\tau_F(n,a,b,\eta)
=\Theta\!\left(\sqrt{NL}+L+\frac{NL}{q}\right)
\quad\text{when }a\geq C(n+h).
\tag{4}
```

The upper bound holds for every supplied tuple; the lower bound is
worst-case, so it need not be attained by each individual frame. No optimal
T-depth or optimal Clifford-count statement is part of the theorem.
The reservation on $`a`$ is sufficient, not a clean-space lower bound.
For example, at $`L=N`$, sufficiently many $`O(n)`$ clean qubits and
$`\Theta(N)`$ borrowed qubits give $`T=\Theta(N)`$. The case of only
$`O(1)`$ clean qubits is treated separately in the
[remaining-endpoint note](../research/CONSTANT_CLEAN_ENDPOINT.md).

We first establish three reusable primitives, then give the low- and
high-precision constructions and the matching lower bound.

## 2. Exact tables and the workspace split

Reserve $`A_0=C_0(n+h)`$ clean wires for logical source registers, selectors,
output words, failure flags, and arithmetic. Choose the theorem's $`C`$
large enough that the remaining clean bank capacity $`c=a-A_0`$ is a fixed
fraction of $`a`$. Put

```math
K=c+b=\Theta(q).
\tag{5}
```

A live source or output word is never simultaneously counted as a bank.
Surplus capacity may be left unused.

For a classical $`v`$-bit table $`f`$ on $`S`$ addresses, an exact XOR
query has action

```math
|x\rangle|y\rangle|z\rangle
\longmapsto |x\rangle|y\oplus f(x)\rangle|z\rangle.
\tag{6}
```

Here $`y`$ is arbitrary and $`z`$ is the entire borrowed bank. To see the
joint-return property directly, split an address into a chunk and a
within-chunk position. Let $`A_f`$ XOR the chunk's $`\lambda`$ words into
the banks, $`P`$ route the selected bank to position zero, and $`C_y`$
copy that bank into $`y`$. The chronological sequence

```math
A_f,\ P,\ C_y,\ P^\dagger,\ A_f^\dagger,
\ P,\ C_y,\ P^\dagger
\tag{7}
```

copies $`z_r\oplus f(x)`$ and then $`z_r`$, restoring the banks and leaving
exactly (6). This basis identity has no phase and therefore holds for
every superposition and reference. Phase-correct Toffoli and Fredkin
decompositions suffice.

A reversible traversal of the chunk-address tree costs $`O(S/\lambda)`$
Toffolis with $`O(\log S)`$ live selector bits; routing costs
$`O(\lambda v)`$. Table data contributes $`O(Sv)`$ CNOTs. This is the
SelectSwap mechanism of Low–Kliuchnikov–Schaeffer [1]. Choosing a power of
two $`\lambda`$ near $`\max\{1,\min(S,\sqrt{S/v},K/v)\}`$
gives, when a full $`v`$-bit output word and the required bank fit,

```math
T_{\rm table}=O\!\left(\sqrt{Sv}+\frac{Sv}{K}+v\right),
\qquad G_{\rm table}=O(Sv+\log S).
\tag{8}
```

If necessary, use the larger of the clean or borrowed pools; its size is
at least $`K/2`$. Our reserved constants ensure that the coarse word fits
both the output reservation and a usable bank allocation. For one-bit
tables, (8) reduces to

```math
T_{\rm bit}=O(\sqrt S+S/K),\qquad G_{\rm bit}=O(S).
\tag{9}
```

The bounds include the actual lookup inverse when a computed word must
be erased. Exact selector scratch returns to zero on every logical input.
These strong invariants allow table helpers to be reused inside circuits
whose other clean work has acquired coherent leakage.

## 3. An exact geometric source of logarithmic width

**Lemma 2 — capped geometric source.** For a power of two $`M=2^t\geq2`$,
there is an exact Clifford+T unitary $`P_M`$ whose initialized column is

```math
g=P_M|0^t\rangle
=\sum_{j=0}^{M-2}2^{-(j+1)/2}|j\rangle
 +2^{-(M-1)/2}|M-1\rangle.
\tag{10}
```

It uses $`O(M)`$ T and Clifford gates and $`O(\log M)`$ total initialized
width, including the source and exactly restored scratch. Its actual
inverse has the same resources.

*Proof.* Let $`G_t=(g_0,\ldots,g_{M-1})`$ be the reflected binary Gray
path. Apply an ordered two-level Hadamard successively on the edges
$`(g_0,g_1),(g_1,g_2),\ldots,(g_{M-2},g_{M-1})`$. Starting at $`g_0=0`$,
each edge finalizes a positive amplitude and halves the remaining
probability. The resulting amplitudes are those in (10), in Gray order.
An $`O(t)`$-CNOT decoder changes Gray order to binary order.

The edge chain has a compact recursive implementation, not $`M`$
independently synthesized $`t`$-controlled gates. Split
$`G_t=0G_{t-1}\Vert1\mathrm{rev}(G_{t-1})`$. Run the first child
under an enable $`e\wedge\neg z`$, bridge the halves with a Hadamard on
$`z`$ conditioned on $`e`$ and the lower register's last Gray vertex,
then run the reversed child under $`e\wedge z`$. Reversal is conjugation
by X on the child's highest bit. Child enables are erased before the
bridge; the bridge predicate excludes its target. A downward physical
edge uses $`XHX`$, preserving the required ordered-Hadamard signs.
All predicates are therefore uncomputed from unchanged control values.

Controlled-H costs two T gates exactly: with $`V=SHTHS^\dagger`$,
$`VZV^\dagger=H`$, so
$`\mathrm{CH}=(I\otimes V)\mathrm{CZ}(I\otimes V^\dagger)`$.
Using seven-T Toffolis, a conservative recurrence is

```math
T_1=2,\qquad T_t=2T_{t-1}+14t+16
=30\,2^t-14t-44.
```

Clifford work obeys the same $`2G_{t-1}+O(t)`$ recurrence. Scratch can be
reused between children and bridge, with
$`W_1=0, W_t=\max\{1+W_{t-1},t-1\}=t-1`$. One additional root enable
is prepared and restored by X. The induction proves a full unitary with
exact scratch return on arbitrary logical inputs, so reversing the
actual word is legitimate. ∎

There are two uses of this source. First, if
$`p=\sum_{k\geq1}b_k2^{-k}<1`$, output digit $`b_{j+1}`$ at label
$`j<M-1`$ and zero at the last label. The output-one probability obeys

```math
0\leq p-p_M\leq2^{-M+1}.
\tag{11}
```

The endpoint $`p=1`$ uses a literal constant-one function. Thus a
classical digit table and (10) realize an approximate Bernoulli decision
with no approximate source preparation. A fixed number of independent
decisions costs $`O(L)`$ gates and $`O(\log L)`$ initialized width at
error $`O(2^{-L})`$.

Geometric indexing and the binary-digit oracle have prior precedent in
Bausch [3], including a capped source. Lemma 2 supplies the simultaneous
exact linear-T and logarithmic-clean-width guarantee used here, with
explicit scratch return. No gate-speedup claim over Bausch's optimized
routing is needed for this theorem.

Second, (10) is approximately preserved by a contractive shift. This
property, proved in Section 7, permits one source to serve all
high-precision corrections.

## 4. From a half-unitary block to the complete output

We use the normalization-two oblivious amplification of
[Berry–Childs–Cleve–Kothari–Somma](https://arxiv.org/pdf/1412.4687),
Eqs. (11)–(15). The following lemma, used twice in the proof, supplies the
complete initialized-isometry estimate, including the rejected-subspace
error required when work is retained coherently.

**Lemma 3 — robust normalization-two amplification.** Let $`U`$ be an
actual unitary, let $`J`$ initialize its logical clean work, and set
$`B=J^\dagger UJ`$. If $`W`$ is unitary and

```math
\zeta=\|2B-W\|\leq1/4,
\quad R=I-2JJ^\dagger,
\quad F=-URU^\dagger RU,
```

then

```math
\|FJ-JW\|\leq4\zeta.
\tag{12}
```

*Proof.* Multiplying the reflections gives
$`J^\dagger FJ=3B-4BB^\dagger B`$. Put
$`\delta=\|B-W/2\|=\zeta/2`$ and write the polar decomposition
$`B=VH`$. Its singular values satisfy
$`\|H-I/2\|\leq\delta`$; hence $`B`$ is nonsingular and $`V`$ is
unitary. The triangle estimate
$`\|V-W\|\leq\|V-2B\|+\|2B-W\|\leq4\delta`$
is enough here.

For $`f(s)=3s-4s^3`$, writing $`s=1/2+e`$ gives
$`f(s)=1-6e^2-4e^3`$. Since $`FJ`$ and $`JV`$ are isometries,

```math
\|FJ-JV\|^2
=2\|I-f(H)\|
\leq(12+8\delta)\delta^2.
```

The equality follows by expanding the squared difference and using
$`V^\dagger J^\dagger FJ=f(H)`$; the latter is Hermitian. Therefore
$`\|FJ-JW\|\leq(4+\sqrt{12+8\delta})\delta\leq8\delta`$.
This is (12), including all leakage. ∎

The word uses two forward calls and one **actual inverse**, and two
zero-work reflections. Its leading minus sign is a literal Clifford
scalar, realizable by $`XZXZ=-I`$. A reflection tests every retained
approximation register; it does not test arbitrary system or borrowed
inputs. Exact scratch may be omitted only after its invariant-zero
boundary property is established. Computing a conjunction, applying Z,
and reversing the conjunction gives an $`O(r)`$-gate reflection with
$`O(r)`$ reusable exact scratch for $`r`$ tested wires.

## 5. The direct construction at low precision

We need a small-space addressed one-qubit compiler before constructing
the high-precision frame.

**Lemma 4 — addressed SU(2) compiler.** For $`S`$ specified gates $`U_x`$
in SU(2), precision $`\epsilon=2^{-\ell}`$, and free bank capacity $`K`$,
the addressed unitary $`\sum_x|x\rangle\langle x|\otimes U_x`$ has a
complete-isometry implementation with

```math
T=O\!\left(\sqrt{S\ell}+\ell+\frac{S\ell}{K}\right),
\quad G=O(S\ell+\ell),
\quad a_{\rm reserved}=O(\log S+\log\ell).
\tag{13}
```

Its actual circuit preserves the address exactly, and every table query
returns borrowed work exactly.

*Proof.* Write
$`U_x=a_{0,x}I+i\sum_{j=1}^3a_{j,x}\sigma_j`$, with real coefficients
and $`\sum_j a_{j,x}^2=1`$. Their absolute sum is at most two. Split
signs into fixed phase-Pauli categories, and add equal weights on $`+I`$
and $`-I`$ so that the total weight is exactly two. At most ten categories
are needed. Their weighted operator sum is $`U_x`$.

For finite classical data, obtain narrow rational enclosures and round
each component toward zero. An enclosure containing zero is rounded to
zero. Otherwise round the endpoint nearer zero to a dyadic grid toward
zero. With grid and enclosure width $`d_0`$, component error is at most
$`2d_0`$; the absolute-weight sum stays at most two. Consequently the
padding remains nonnegative and operator error is at most $`8d_0`$.
No exact sign or exact-zero oracle is required.

A depth-four binary decision tree samples the resulting normalized
rational weights. Use four independently prepared sources (10), one
per decision, and read its conditional probability digit through an
exact XOR table. Unreachable prefixes receive a fixed specified action.
Each table has $`O(S\ell)`$ bits, since the prefix alphabet is constant
and $`M=O(\ell)`$. The total-variation error of the category distribution
is at most four times the tail in (11).

Let $`P`$ be this actual preparation, retaining all source and category
history. SELECT applies the literal fixed phase-Pauli on the target.
Then $`U=P^\dagger\mathrm{SELECT}P`$ has zero-work block equal to the
actual average selected Pauli. Rounding and tail bounds make
$`\|2J^\dagger UJ-W\|\leq\epsilon/8`$ by constant precision margins.
Lemma 3 supplies the full output contract. All address blocks use the
same normalization; all operations preserve the address exactly.
Equations (9), (10), and the constant amplification multiplicity give
(13). The source construction is independent of this compiler. ∎

At frame depth $`d`$, compute one exact suffix flag
$`f=[s=0^{n-d-1}]`$, and use Lemma 4 with address $`(p,f)`$ and
$`S_d=2^{d+1}`$: select $`R_y(\theta_{d,p})`$ if $`f=1`$, and $`I`$
otherwise. The sampler preserves $`p,f`$ exactly and never changes the
suffix. The flag therefore uncomputes exactly even when sampler work
has leakage. The empty suffix uses a constant flag.

Choose layer errors
$`\epsilon_d=2^{-L}2^{d-n}`$, so
$`\ell_d=L+n-d+O(1)`$ and $`\sum_d\epsilon_d<\eta`$. All layers may
use one private clean pool. If $`H_d`$ is an actual layer circuit and
$`\|H_dJ-JL_d\|\leq\epsilon_d`$, unitary telescoping gives

```math
\|H_{n-1}\cdots H_0J-JW\|
\leq\sum_d\epsilon_d.
\tag{14}
```

Each comparison uses the ideal preceding layers with work zero; the
actual earlier leakage is propagated unitarily. No reset or assumed
factorization of the actual intermediate state is involved.

The geometric sums

```math
\sum_d2^d\ell_d=O(NL),\qquad
\sum_d\sqrt{2^d\ell_d}=O(\sqrt{NL}),\qquad
\sum_d\ell_d=O(nL+n^2)
```

give

```math
T_{\rm direct}=O(\sqrt{NL}+nL+NL/K),\qquad
G_{\rm direct}=O(NL),\qquad a_{\rm reserved}=O(n+h).
\tag{15}
```

For $`L<n^3`$, $`nL/\sqrt{NL}\leq n^{5/2}/2^{n/2}`$, whose supremum
over positive integer $`n`$ is finite. Thus (15) proves the desired
upper bound throughout this low-precision branch.

The direct sampler has approximate clean return. The coarse circuit
needed next has a stronger, exact return property and is built separately.

## 6. Grouped dictionaries and an exactly clean coarse frame

Assume now $`L\geq n^3`$. Partition the depth interval into consecutive
groups. To discover the partition, start with $`r=0`$ deepest layers
covered, choose

```math
s=\min\{n-r,2^{\lfloor r/2\rfloor}\},\qquad e=n-r,
```

form the group $`[e-s,e)`$, and replace $`r`$ by $`r+s`$. Execute the
resulting groups in the original shallow-to-deep order. Denote their
number by $`R\leq n`$, heights by $`s_i`$, and ending depths by $`e_i`$.

**Lemma 5 — sparse grouped residuals.** Suppose $`C_i`$ is a product of
actual one-qubit program words in the same addressed order as group
$`W_i`$, with exact identity on inactive suffix sectors. Then
$`E_i=C_i^\dagger W_i-I`$ has a fixed permitted support of size

```math
S_i=2^{e_i-s_i}\bigl[(2s_i-1)2^{s_i}+2\bigr]
\leq2s_i2^{e_i}.
\tag{16}
```

After splitting each entry into its nonnegative real and imaginary
parts with phases $`1,-1,i,-i`$, pad its dictionary to a power of two
$`Q_i=O(s_i2^{e_i})`$. These actual padded dictionaries satisfy

```math
\sum_i Q_i=O(N),\qquad
\sum_i\sqrt{Q_i}=O(\sqrt N),\qquad \log Q_i=O(n).
\tag{17}
```

*Proof.* A group preserves its initial prefix of length $`e_i-s_i`$.
It is identity unless its final $`n-e_i`$ suffix bits are all zero.
Within this active sector it is a direct sum of $`2^{e_i-s_i}`$
complete $`s_i`$-level frames, each of dimension $`2^{s_i}`$.

In an $`s`$-level frame, a nonzero marker $`y`$ has a column supported
inside its aligned dyadic subtree of size $`2^{1+\nu_2(y)}`$. Shallower
layers fix it because its suffix is nonzero; its own layer and all later
layers preserve that subtree. This reasoning also holds for the complex
coarse words. Column zero has full support. Two such subtrees overlap
only when their nodes coincide or are comparable by ancestry. Therefore
the permitted ordered column pairs for $`C^\dagger W-I`$ number

```math
(2^s-1)+2\sum_{j=0}^{s-1}j2^j+2(2^s-1)+1
=(2s-1)2^s+2.
```

This proves (16); accidental zero coefficients need not be recognized.
The chosen partition gives
$`s_i2^{e_i}\leq N2^{-r_i/2}`$. The distinct $`r_i`$ are nonnegative
integers, so summing the geometric series in $`2^{-r_i/2}`$ and
$`2^{-r_i/4}`$ proves (17), including fixed phase and padding factors. ∎

The dictionary atoms are
$`A_{i\ell}=\omega_{i\ell}|u_{i\ell}\rangle\langle v_{i\ell}|`$,
$`\omega_{i\ell}\in\{1,-1,i,-i\}`$. Their full-system endpoints are

```math
(\text{prefix}\,\Vert\,\text{local endpoint})\,\Vert\,0^{n-e_i}.
```

This embedding preserves every inactive sector. A matrix unit has a
one-flag unitary dilation: XOR $`[z\ne v]`$ into a failure flag and then
XOR $`u\oplus v`$ into the system. Its flag-zero block is exactly
$`|u\rangle\langle v|`$. Equality scratch is erased **before** changing
the system. Coherently loaded endpoints and their label are unchanged;
the actual inverse applies the mask first and reverses the predicate.
On an active selected branch, literal phases are applied using S and Z
on exactly computed phase-control bits and then erasing those bits;
computing the activity conjunction costs only a constant number of
Toffolis. Inactive branches receive no phase. Full endpoint words cost $`O(n)`$ Boolean-table bits per entry.

Choose

```math
p=2^{-\lceil\log_2(8R)\rceil},\qquad
J=2^{\lceil\log_2(L+8)\rceil},\qquad M=4J,
\qquad \gamma=(1-p)^R\geq1-Rp\geq7/8.
\tag{18}
```

Here $`p`$ is the exact probability of an all-zero outcome on
$`\log_2(1/p)`$ Hadamard bits. Let $`Q_{\max}=\max_iQ_i`$, and compile
each original depth with error at most

```math
\delta_c=\frac{p}{4nQ_{\max}J}.
\tag{19}
```

The phase-calibrated one-qubit synthesis primitive supplies words of
length $`w=O(\log(1/\delta_c))=O(n+h)`$; this is the single-qubit
primitive recorded as GKW Lemma 2.3 [2]. A common constant-alphabet
schedule, controlled by a loaded $`w`$-bit word, implements the selected
actual word exactly. Controlled-H is exact as above; controlled-T can
be implemented by computing the conjunction of control and target,
applying T there, and uncomputing it. Inactive rows contain the empty
program. All prefix, suffix, and word controls are preserved, so lookup
and selector work erase exactly.

Thus $`C_i`$ is an actual unitary with exactly clean work and the support
used in Lemma 5, although its active words only approximate their real
targets. It obeys

```math
\|E_i\|=\|C_i-W_i\|\leq s_i\delta_c
\leq\frac{p}{4Q_{\max}J}.
\tag{20}
```

Define the classical scale

```math
\varepsilon_i=\frac{p}{(1-p)Q_iJ}.
```

Every nonnegative split coefficient $`a_{i\ell}`$ of $`E_i`$ is at most
$`\varepsilon_i/4`$. Obtain a nonnegative rational lower enclosure with
error below $`\Delta_i=\varepsilon_i2^{1-J}`$, then round it down to
that grid. This produces Boolean digits satisfying

```math
\widehat a_{i\ell}
=\varepsilon_i\sum_{k=0}^{J-1}f_{i\ell k}2^{-k},\qquad
0\leq a_{i\ell}-\widehat a_{i\ell}
<2\varepsilon_i2^{1-J}.
\tag{21}
```

Positive and negative parts can be enclosed by clipping rational
intervals at zero. No undecidable exact sign test is used. Structural
zeros and padding have zero digits. The scale $`\varepsilon_i`$ is
classical data only; the quantum circuit never prepares an amplitude
equal to its square root. Nor does the definition
$`E_i=C_i^\dagger W_i-I`$ call $`W_i`$ as a quantum oracle: it specifies
the classical coefficient calculation relative to the actual coarse
words.

## 7. A reusable source and the local correction kernel

Prepare (10) once with the $`M`$ in (18). For $`0\leq d<M`$, define

```math
S_d=\sum_{j=d}^{M-1}|j-d\rangle\langle j|.
```

These are contractions. For $`d=0`$, $`S_0=I`$; for every $`1\leq d<M`$,

```math
\|S_dg-2^{-d/2}g\|^2=(4-2\sqrt2)2^{-M}.
\tag{22}
```

Indeed all coordinates before $`M-d-1`$ agree. At that coordinate the
difference is $`(\sqrt2-1)2^{-M/2}`$, while the omitted tail has squared
norm $`2^{-M}`$. Adding gives (22), uniformly in $`d`$.

The dilation of $`S_d`$ first XORs $`[j<d]`$ into a retained source-failure
bit, then subtracts $`d`$ modulo $`M`$. Initialized and projected flag
zero gives exactly $`S_d`$. Both operations are reversible on every
source/flag input; the inverse reverses subtraction and then the
predicate. Ordinary ripple arithmetic costs $`O(\log M)`$ Toffolis
and $`O(\log M)`$ exact temporary work. The digit label supplies the
unchanged displacement $`d=2k<M`$.

Use one shared private register $`F`$ for each local kernel. It includes
the rare-mode bits, a uniform entry label $`\ell\in[Q_i]`$, a uniform
digit label $`k\in[J]`$, their loaded digit and metadata, and three
independent dilation flags. Prepare the uniform labels by Hadamards,
compute $`f_{i\ell k}`$, and load the endpoints exactly. Let this
source-independent preparation be $`B_i`$.

The actual SELECT has the following flag-zero blocks:

| Sector | Accepted block on source and system |
|---|---|
| Common mode, probability $`1-p`$ | $`I`$ |
| Rare mode and digit one | $`S_{2k}\otimes A_{i\ell}`$ |
| Rare mode and digit zero, or invalid padding | (0) |

Source underflow and matrix-unit rejection have distinct flags, so
their accepted block is the product of the two contractions. The zero
case flips a separate failure flag. All SELECT cases have specified
unitary actions on the complete space. Source and system changes leave
the entry and digit labels unchanged, so every lookup and predicate can
be reversed on failure branches as well.

Set $`K_i=B_i^\dagger\mathrm{SELECT}_i B_i`$. Projecting **only** $`F`$
to zero gives the exact contraction

```math
T_i=(1-p)I+\frac{p}{Q_iJ}
\sum_{\ell,k}f_{i\ell k}S_{2k}\otimes A_{i\ell}.
\tag{23}
```

No source projector is inserted. Let $`E_g=|g\rangle\otimes I`$,
$`e_M=\sqrt{4-2\sqrt2}\,2^{-M/2}`$, and

```math
D_i=(1-p)C_i^\dagger W_i=(1-p)(I+E_i).
```

Using (22) for every digit and (21) for every coefficient yields

```math
\|T_iE_g-E_gD_i\|
\leq p e_M+\frac{2p}{J}2^{1-J}.
\tag{24}
```

For clarity, the shift error is bounded by
$`p(Q_iJ)^{-1}\sum_{\ell,k}f_{i\ell k}e_M\leq pe_M`$.
The coefficient error is at most
$`2Q_i\varepsilon_i2^{1-J}`$, multiplied by $`1-p`$.
Both $`T_i`$ and $`D_i`$ are contractions, with
$`\|D_i\|=1-p`$. The rounded approximation need not be a contraction;
it is used only to derive the error estimate. Equation (24) controls
every system input and reference on the specified source column. Earlier
source disturbance is propagated contractively in the following hybrid.

## 8. Shared private work, history, and the final normalization

Sharing $`F`$ without a record would allow a failed component to return
to $`F=0`$ at a later stage. A small counter supplies the required
record. Initialize a counter $`H`$ of
$`\lceil\log_2R\rceil`$ bits; omit it when $`R=1`$. Run each actual
$`K_i`$ unconditionally, then its system coarse circuit $`C_i`$. Between
successive stages increment $`H`$ if and only if $`F\ne0`$. There are
at most $`R-1`$ increments, so a counter initialized at zero never wraps
back to zero. The modulo counter action on other inputs is still a
defined unitary, and its actual reverse is used below.

Consequently the final $`H=0,F=0`$ block has exactly the intermediate
$`F=0`$ projectors inserted between every stage. This statement follows
by expanding in the counter and private-work computational bases: each
path with any recorded nonzero $`F`$ has a positive final counter; the
only surviving paths have every intermediate $`F=0`$. Later kernels
do not act on the counter. Coarse words act only on the system and their
separate exactly restored scratch, so their execution is valid on every
failed source/private branch.

The accepted block on source and system is thus

```math
V_{\rm acc}=(I\otimes C_R)T_R\cdots(I\otimes C_1)T_1.
```

Contractive telescoping of (24) proves

```math
\|V_{\rm acc}E_g-E_g\gamma W\|\leq\xi,
\qquad
\xi\leq Rp\left(e_M+\frac2J2^{1-J}\right)
\leq\frac{2^{-L}}{128}.
\tag{25}
```

This is the accepted-block estimate; no claim of full output correctness
has yet been made. Apply the actual inverse $`P_M^\dagger`$ after the
stream. Projecting the source to zero at this final boundary gives a
block $`V_0`$ with
$`\|V_0-\gamma W\|\leq\xi`$. Approximate source return is already
charged in (25).

To obtain normalization two, use an independent global mode with target
probability

```math
w_0=\frac1{2\gamma}\in[1/2,4/7].
```

One further source (10) and its binary-digit sampler (11) realize an
actual probability $`\widetilde w`$ with
$`|\widetilde w-w_0|\leq\epsilon_0=2^{-L}/128`$, at cost $`O(L)`$
and width $`O(\log L)`$. Run the stream unconditionally; flip a separate
zero-padding flag on the mode-zero sector, and reverse the actual mode
preparation. The mode registers never enter the intermediate $`F\ne0`$
test. Its accepted block is exactly

```math
B=\widetilde w V_0,\qquad
\|2B-W\|\leq2\xi+2\epsilon_0.
\tag{26}
```

Let $`U`$ denote this entire actual unitary, including both source
preparations, their inverses, history, zero padding, and all coarse
words. Apply Lemma 3 to $`-URU^\dagger RU`$. The reflection tests every
retained logical clean register: source, shared private work, history,
mode, and failure flags. The borrowed bank is never tested. Exact
scratch is separately restored and may be excluded from the test.
The final complete-isometry error is less than

```math
8\xi+8\epsilon_0\leq2^{-L}/8<\eta.
\tag{27}
```

There are three complete stream appearances, one reversed. Each
individual coarse group therefore appears exactly three times as its
word or actual inverse. The stream is not controlled by the global
mode, and the complete coarse frame is not repeated once per group.

## 9. Resource ledger and completion of the upper bound

The following bounds are for the high-precision branch $`L\geq n^3`$.
All forward/inverse calls and the constant amplification multiplicity
are included in the $`O(\cdot)`$ constants. The full coarse output word
has $`w=O(n+h)`$ bits.

| Component | T-count | Clifford count | Simultaneous initialized reservation |
|---|---:|---:|---:|
| Residual digit tables | $`O(\sqrt{NL}+NL/K)`$ | $`O(NL)`$ | $`O(n+h)`$ labels/selectors, plus banks |
| Endpoint and phase tables | $`O(n\sqrt N+nN/K)`$ | $`O(nN)`$ | $`O(n)`$ output and selectors |
| All coarse group words together | $`O(\sqrt{Nw}+Nw/K+nw+n^2)`$ | $`O(Nw+n^2)`$ | $`O(n+h)`$ output/selectors |
| Common shift source and global-mode source | $`O(L)`$ | $`O(L)`$ | $`O(h)`$ source and exact scratch |
| Shift arithmetic, equality, history, and reflections | $`O(n(n+h)+(n+h)^2)`$ conservatively | Same order | $`O(n+h)`$ reusable exact scratch |

The first row follows from (9) with table sizes $`Q_iJ`$, followed by
(17). For endpoints, perform $`O(n)`$ one-bit queries per group and
again use (17). The coarse row follows from (8) at each original depth,
with $`S_d=O(2^d)`$, one complete output program of length $`w`$, and an
$`O(w)`$-cost interpreter. Thus
$`\sum_d\sqrt{2^dw}=O(\sqrt{Nw})`$ and
$`\sum_d2^dw=O(Nw)`$. Groups partition the original depths, so there is
no additional factor $`R`$.

For the last row, each source shift, full-system equality, private-zero
test, and controlled counter increment uses linear-size reversible
arithmetic on $`O(n+h)`$ bits. There are $`O(R)\leq O(n)`$ such
operations. Select activity controls cost only a constant factor when
implemented by exact bounded-control gates. Predicates and arithmetic
scratch are erased before reuse. The stated quadratic allowance also
covers straightforward selector and reflection implementations.

All logical retained fields and all temporary fields have only a fixed
number of $`O(n+h)`$-bit components. In particular, there is one common
source, one reused $`F`$, one logarithmic counter, and one separate mode;
there are not $`R`$ live precision sources or failure registers. A
constant multiple of $`n+h`$ clean wires therefore suffices before the
bank pool in (5) is allocated.

Since $`J=\Theta(L)`$ and $`w=O(n+h)=O(L)`$, the coarse square-root and
table terms are absorbed by $`\sqrt{NL}+NL/K`$. Also $`n\leq\sqrt L`$
in this branch, so $`n\sqrt N\leq\sqrt{NL}`$ and $`nN/K\leq NL/K`$.
The polynomial terms are absorbed uniformly: if $`n^3\leq L\leq N`$,
then $`h=O(n)`$ and the overhead is $`O(n^2)=O(\sqrt{NL})`$; if
$`L\geq N`$, then $`n,h=O(\log L)`$ and it is $`O((\log L)^2)=O(L)`$.
Bounded small dimensions are covered by the same absolute constants.
All Clifford rows are $`O(NL)`$.

Combining this ledger with the low-precision branch (15) proves (3),
using $`K=\Theta(q)`$. Applying the actual inverse of any completed
compiler has the same isometry error: from (2),

```math
\|V^\dagger J_a-J_a(W^\dagger\otimes I_b)\|
=\|V^\dagger[J_a(W\otimes I_b)-VJ_a]
 (W^\dagger\otimes I_b)\|\leq\eta.
\tag{28}
```

This is the inverse interface used by downstream differential-frame
algorithms. It requires the complete contract, rather than merely an
approximation to $`W|0^n\rangle`$.

## 10. Matching lower bounds and their lineage

Two different bounds are required: one for precision at arbitrary
width, and one for width at fixed coherent gate count.

### 10.1 The real frame contains arbitrary diagonals

Set all layers except the final one to identity. Then

```math
W=\bigoplus_{p=0}^{2^{n-1}-1}R_y(\theta_p),\qquad
R_y(\theta_p)|y_+\rangle=e^{-i\theta_p}|y_+\rangle,
\quad |y_+\rangle=(|0\rangle+i|1\rangle)/\sqrt2.
```

A Clifford encoding of this last stabilizer qubit therefore turns the
real-frame compiler into a compiler for an arbitrary diagonal on
$`n-1`$ logical qubits. Initialize the borrowed register to zero, a
permitted special case of its required arbitrary input. The complete
isometry error implies channel diamond-norm error at most $`2\eta`$,
including ancillary return. GKW Theorem 4.2 [2] gives

```math
\tau_F=\Omega(\sqrt{NL}+L).
\tag{29}
```

For $`n=1`$, a fixed Clifford conjugates the one-qubit $`R_y`$ family
to determinant-one diagonals. These realize every one-qubit diagonal
channel up to its irrelevant channel phase, so the same theorem gives
the needed $`\Omega(L)`$ bound. This reduction is from the actual real
frame family. It does not infer real-family hardness from a packing of
unrelated complex states.

The published GKW lower bound allows a stronger adaptive circuit model;
using it for the coherent model here is therefore valid. Their
ancilla-independent lower-bound machinery builds on the Clifford/Pauli
postselection framework of Beverland, Campbell, Howard, and Kliuchnikov;
we use GKW's proved diagonal theorem, not a new unrestricted counting
claim.

### 10.2 Fixed-width coherent counting

Commuting Cliffords through a word makes each T or T-dagger a rotation
about a signed $`q`$-qubit Pauli, leaving a terminal Clifford. There are
at most $`2\cdot4^q`$ choices per such rotation and fewer than
$`2^{2q^2+3q}`$ projective Cliffords. Including a finite scalar allowance
and all shorter lengths gives the conservative bound

```math
\#\{\text{width-}q\text{ words of T-count at most }t\}
\leq2^{2q^2+3q+5+(2q+1)t}.
\tag{30}
```

This is the LKS fixed-width counting route [1], specialized here to the
real frame and its declared workspace contract.

For an explicit real packing, map the radius-$`1/2`$ Euclidean ball in
$`\mathbb R^{N-1}`$ into the real unit sphere by

```math
x\longmapsto\psi(x)=(\sqrt{1-\|x\|_2^2},x).
```

Distances do not shrink. A maximal set with pairwise distances greater
than $`2\eta`$ has at least $`(1/(4\eta))^{N-1}`$ elements, by comparing
the ball's volume with the radius-$`2\eta`$ covering balls. Its states
have positive real inner products, so optimizing their relative global
phase does not reduce these distances. The real Hopf chart contains
all these first columns. One circuit cannot approximate two of them.
Using the all-zero borrowed input in (2) and comparing with (30) yields

```math
t\geq
\left[
\frac{(N-1)(\log_2(1/\eta)-2)-2q^2-3q-5}{2q+1}
\right]_+.
\tag{31}
```

The exact logarithm in (31) avoids a rounding ambiguity: with the
ceiling definition of $`L`$, $`L-3`$ is a valid integer substitute for
$`\log_2(1/\eta)-2`$. If $`q^2\leq c_0NL`$ for a sufficiently small
absolute constant $`c_0`$, (31) gives $`\Omega(NL/q)`$. Outside this
range, $`NL/q=O(\sqrt{NL})`$, already supplied by (29). Combining
(29) and (31) proves

```math
\tau_F=\Omega\!\left(\sqrt{NL}+L+\frac{NL}{q}\right)
```

at every width, and (4) follows from the construction. No local
precision costs have been added to obtain this lower bound.

## 11. What is proved, and what remains to implement

The result is an analytic circuit construction with an explicit
complete-input contract, exact source and table primitives, a finite
classical coefficient prescription, and a charged resource ledger.
It is not a report that a general elementary-gate emitter for the entire
high-precision construction has already been implemented. Finite matrix
and circuit fixtures can check individual identities and conventions;
they do not establish the asymptotic theorem by sampling.

Classical preprocessing produces $`O(NL)`$ digit-table bits, coarse
programs, and endpoint data. The time for evaluating the supplied
coefficients, computing residual entries relative to actual coarse
words, and obtaining certified rational enclosures is additional.
The theorem does not assume unit-cost exact real arithmetic or assert
an $`O(NL)`$ classical running time. As usual for constructive synthesis,
the angle descriptions must permit the required certified evaluation.

The $`O(L)`$ precision charge comes from a constant number of geometric
source preparations and their actual inverses. Its reuse across the
whole frame is justified by (22)–(27). Geometric indices and digit
oracles themselves have earlier precedent; the relevant resource step
here is their exact logarithmic-width implementation and the shared
source's complete-frame composition. SelectSwap and the lower-bound
machinery retain their original attribution. The sufficient reservation
$`a\geq C(n+h)`$ remains part of Theorem 1; the
[constant-clean endpoint](../research/CONSTANT_CLEAN_ENDPOINT.md) is not
settled by removing that hypothesis from the displayed formula. A separate
[operator-source construction](../research/constant_clean/OPERATOR_SOURCE_COMPILER.md)
now gives $`T=O(N+nL)`$ and $`G=O(NL)`$ with $`a=2`$ and
$`b\ge L+n+7`$. At $`L=N`$ its upper bound is $`O(N\log N)`$;
Theorem 1 and its matching lower bounds are unchanged. The separate note
also sharpens this bound to $`O(\sqrt{NL}+nL+NL/b)`$ when
$`b\ge2(L+n+7)`$, and adds a literal diagonal/complex magnitude corollary.
Its stated matching subregimes use the existing lower bounds; they do not
remove Theorem 1's sufficient-clean hypothesis by substitution.

### Primary references

1. Guang Hao Low, Vadym Kliuchnikov, and Luke Schaeffer,
   *Trading T gates for dirty qubits in state preparation and unitary
   synthesis*, Quantum **8**, 1375 (2024),
   [arXiv:1812.00954v2](https://arxiv.org/html/1812.00954v2).
   Section 2, Figure 1(d), and equation (8) supply the table mechanism
   and dirty cancellation; Section 5 gives the fixed-width counting
   lineage. The specialized joint-return and resource derivation used
   here is in Section 2 above.
2. David Gosset, Robin Kothari, and Kewen Wu,
   *Quantum State Preparation with Optimal T-Count*, Quantum **10**,
   2168 (2026),
   [arXiv:2411.04790v3](https://arxiv.org/html/2411.04790v3).
   Lemma 2.3 supplies phase-calibrated one-qubit approximation;
   Theorem 4.2 supplies the diagonal lower bound used in Section 10.1.
   The original single-qubit synthesis references are identified there.
3. Johannes Bausch, *Fast Black-Box Quantum State Preparation*,
   [arXiv:2009.10709v4](https://arxiv.org/pdf/2009.10709v4).
   Equations (4) and (6) give geometric-index and bit-oracle sampling;
   Section 2.3.3 discusses exact unary preparation and conversion to
   a binary index. The source and complete-frame resource proof in
   this chapter is given independently in Sections 3 and 6–9.
4. Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, and
   Rolando D. Somma, *Simulating Hamiltonian dynamics with a truncated Taylor
   series*, Physical Review Letters **114**, 090502 (2015),
   [arXiv:1412.4687](https://arxiv.org/pdf/1412.4687).
   Equations (11)–(15) give normalization-two oblivious amplification and
   its accepted-block polynomial. Section 4 above proves the full-output
   estimate used here without discarding retained work.
