# Global blocks with a common dirty-program interpreter

This follow-up checks a concrete global route to the constant-clean endpoint:
load a whole classical program into an arbitrary dirty register, run one
interpreter, undo the XOR load, and run an interpreter inverse. The accepted
input and output flags are allowed to differ.

**Result.** Different flags evade the elementary adjoint obstruction, but a
common interpreter still obeys a robust matrix-rank condition. For a full
family of binary-angle programs, it requires growing initialized workspace.
This is an obstruction to the specified two-query architecture, even with
arbitrarily expensive interpreter gates. It is **not** a lower bound on
general Hopf-frame compilation. No improved whole-frame upper bound is
proved here; the selected endpoint remains between $`\Omega(N)`$ and
$`O(N^{3/2})`$ T gates. A separate exact dirty-bank identity in Section 5
reduces the problem to a specified heterogeneous phase-batching primitive.
If that stronger missing primitive were proved, it would give a conditional
$`O(N\log N)`$ endpoint compiler.

The governing model and remaining objective are in the
[endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md). The earlier same-embedding
result is in [Global XOR echo](GLOBAL_XOR_ECHO.md).

## 1. What differing flags change

Let the dirty program label be $`z`$, and let XOR insertion of mask $`f`$
produce the branch operator

```math
E_f(z)=D_{z\oplus f}D_z^\dagger.
\tag{1}
```

Each $`D_z`$ is an actual unitary on the non-program registers. The
interpreter preserves the program label, and the XOR circuit restores it.
Equation (1) uses the actual inverse. It is therefore meaningful for
arbitrary program inputs, including superpositions entangled with a reference.

For one fixed initialized embedding $`J`$,

```math
A_f(z)=J^\dagger E_f(z)J
\quad\Longrightarrow\quad
A_f(z\oplus f)=A_f(z)^\dagger.
\tag{2}
```

No return promise on failed work is needed for (2). If
$`\|A_f(z)-\alpha U_f\|\leq\delta`$ uniformly in $`z`$, with real
$`\alpha>0`$, then

```math
\|U_f-U_f^\dagger\|\leq 2\delta/\alpha.
\tag{3}
```

For $`R_y(\theta)=e^{-i\theta Y}`$, this implies
$`\delta\geq\alpha|\sin\theta|`$. The amplification polynomial
$`p(A)=3A-4AA^\dagger A`$ preserves adjoint pairing:
$`p(A^\dagger)=p(A)^\dagger`$.

However, with distinct embeddings $`J_{\rm in},J_{\rm out}`$, reversal gives

```math
J_{\rm out}^\dagger E_f(z\oplus f)J_{\rm in}
=
\bigl(J_{\rm in}^\dagger E_f(z)J_{\rm out}\bigr)^\dagger.
\tag{4}
```

The right side is the adjoint of the *opposite* cross-block. It does not
force the desired cross-block to be Hermitian.

For example, for any unitary $`W`$, put

```math
\mathcal I_W=
\begin{pmatrix}0&W^\dagger\\W&0\end{pmatrix},
\qquad D_0=I,\qquad D_1=\mathcal I_W.
\tag{5}
```

Then $`\mathcal I_W^2=I`$, and $`E_1(z)=\mathcal I_W`$ for both dirty
values. With
$`J_{\rm in}=|0\rangle\otimes I`$ and
$`J_{\rm out}=|1\rangle\otimes I`$, the cross-block is exactly $`W`$.
An X on the flag restores the initialized flag after that action.

This is an algebraic escape for one target. It supplies no implementation
cost for the target-dependent $`\mathcal I_W`$ or its program-controlled
use. A cheap implementation of the lift would already give a cheap
implementation of $`W`$. In particular, writing the lift with controlled
$`W`$ and $`W^\dagger`$ does not synthesize their gates.

Asymmetric flags can also use amplitude amplification: for
$`B=J_{\rm out}^\dagger UJ_{\rm in}`$, let
$`R_{\rm in}=I-2J_{\rm in}J_{\rm in}^\dagger`$ and
$`R_{\rm out}=I-2J_{\rm out}J_{\rm out}^\dagger`$. The actual word

```math
-U R_{\rm in}U^\dagger R_{\rm out}U
\tag{6}
```

has cross-block $`3B-4BB^\dagger B`$. The complete-isometry estimate
proved for normalization two applies with these two embeddings as well.
Thus different flags are a legitimate interface; their common-interpreter
dimension, rather than (3), is the next issue. Implementing these reflections
requires the actual embedding preparation and inverse; the formula alone
does not make them inexpensive.

## 2. The common-interpreter cross-block rank theorem

Let $`G=\mathbb F_2^m`$ and $`M=2^m`$. Use a dirty program of $`m+1`$
bits, with labels $`z=(z_0,v)\in\mathbb F_2\times G`$. The supplied
program masks are the affine family

```math
f_x=(1,x),\qquad x\in G.
\tag{7}
```

The leading one avoids the zero-mask degeneracy and permits a different
output flag. This is therefore not an argument that assumes a zero-mask
operation implements a nonidentity target.

Let the remaining logical and arbitrary dirty input space have dimension
$`d`$. All other initialized or supplied source work is included in an
ambient interpreter space of dimension

```math
D=2^a d.
\tag{8}
```

Allow arbitrary fixed isometries
$`J_{\rm in},J_{\rm out}:\mathbb C^d\longrightarrow\mathbb C^D`$.
They need not have orthogonal images, need not be product embeddings, and
may include a common actual source preparation. There is one common
family of unitary interpreters $`D_z`$ and one common pair of embeddings
for all $`x`$ below.

**Theorem.** Suppose, for a family of unitaries $`U_x`$ on
$`\mathbb C^d`$ and a real scalar $`\alpha>0`$,

```math
\left\|
J_{\rm out}^\dagger
D_{z\oplus(1,x)}D_z^\dagger J_{\rm in}
-\alpha U_x
\right\|\leq\delta
\quad\text{for every }z,x.
\tag{9}
```

Define normalized Walsh coefficients

```math
\widehat U_\chi
=\frac1M\sum_{x\in G}(-1)^{\chi\cdot x}U_x.
\tag{10}
```

Then

```math
\boxed{
\sum_{\chi\in G}
\#\{j:\sigma_j(\widehat U_\chi)>\delta/\alpha\}
\leq 2^a d.
}
\tag{11}
```

At zero error this gives

```math
\boxed{\sum_\chi \mathrm{rank}(\widehat U_\chi)\leq2^a d.}
\tag{12}
```

The theorem permits arbitrary action on rejected subspaces. There is no
assumption of source return after the interpreter or after acceptance.
There is also no T-count premise.

*Proof.* Consider only the dirty-label slice $`z=(0,v)`$. For
$`u,v\in G`$, put $`x=u\oplus v`$. The actual cross-block matrix is

```math
K_{u,v}
=J_{\rm out}^\dagger D_{(1,u)}D_{(0,v)}^\dagger J_{\rm in}.
\tag{13}
```

Stack its left factors vertically and right factors horizontally:

```math
K=
\begin{pmatrix}
J_{\rm out}^\dagger D_{(1,0)}\\
J_{\rm out}^\dagger D_{(1,1)}\\
\vdots
\end{pmatrix}
\begin{pmatrix}
D_{(0,0)}^\dagger J_{\rm in}&
D_{(0,1)}^\dagger J_{\rm in}&\cdots
\end{pmatrix}.
\tag{14}
```

The middle dimension is $`D`$, so $`\mathrm{rank}(K)\leq D`$.
This factorization does not rely on invariance of either embedded
subspace.

The ideal matrix is the block convolution

```math
H_{u,v}=\alpha U_{u\oplus v}.
\tag{15}
```

Each block of $`K-H`$ has norm at most $`\delta`$. For a block vector
$`\psi=(\psi_v)_v`$, Cauchy–Schwarz gives

```math
\|(K-H)\psi\|^2
\leq
\sum_u\left(\delta\sum_v\|\psi_v\|\right)^2
\leq M^2\delta^2\|\psi\|^2.
```

Hence

```math
\|K-H\|\leq M\delta.
\tag{16}
```

Let $`Q_{\chi,x}=M^{-1/2}(-1)^{\chi\cdot x}`$ be the unitary Walsh
matrix. Direct summation over $`u,v`$ gives

```math
(Q\otimes I_d)H(Q^\dagger\otimes I_d)
=M\alpha\bigoplus_{\chi\in G}\widehat U_\chi.
\tag{17}
```

Thus the number of singular values of $`H`$ strictly exceeding
$`M\delta`$ is exactly the left side of (11). A matrix within
$`M\delta`$ in operator norm of a rank-at-most-$`D`$ matrix can have
at most $`D`$ such singular values: otherwise its
$`(D+1)`$st singular value would exceed the best possible rank-$`D`$
approximation error. Equations (14) and (16) prove (11), and zero error
gives (12). ∎

All non-program dirty spectators occur in both $`d`$ and $`D=2^a d`$.
Their dimension cannot be omitted on one side or counted as initialized
capacity on the other. Their multiplicity cancels in the application
below. The program itself has been fixed to computational-basis labels
only to obtain necessary conditions from the required arbitrary-input
contract; it has not been initialized or measured by the circuit.

## 3. Binary-angle programs require growing clean dimension

Take $`d=2r`$ and the target family

```math
U_x=
R_y\!\left(\sum_{j=1}^m2^{-j}x_j\right)\otimes I_r,
\qquad x\in\mathbb F_2^m.
\tag{18}
```

The angle unit is radians, and the rotation convention has no factor
of one-half in its exponent. The spectator dimension $`r`$ can include
arbitrary logical and dirty inputs.

In the fixed Y-eigenbasis the two eigenvalues are
$`\exp(\pm i\sum_j2^{-j}x_j)`$. Their Walsh coefficients factor as

```math
\frac1M\sum_x(-1)^{\chi\cdot x}
e^{i\sum_j2^{-j}x_j}
=
\prod_{j=1}^m\frac{1+(-1)^{\chi_j}e^{i2^{-j}}}{2}.
\tag{19}
```

The coefficients for the two signs are complex conjugates. Therefore
every singular value of $`\widehat U_\chi`$ equals

```math
c_\chi=
\prod_{\chi_j=0}\cos(2^{-j-1})
\prod_{\chi_j=1}\sin(2^{-j-1})>0,
\tag{20}
```

with multiplicity $`d`$. Equation (11) becomes

```math
\boxed{
\#\{\chi:c_\chi>\delta/\alpha\}\leq2^a.
}
\tag{21}
```

In particular, exact uniform implementation forces $`a\geq m`$.

For a simple robust bound, all arguments in (20) lie in $`(0,1/4]`$.
There, $`\cos t\geq\sin t\geq t/2`$, so

```math
c_\chi
\geq\prod_{j=1}^m2^{-j-2}
=2^{-m(m+5)/2}.
\tag{22}
```

Consequently,

```math
\boxed{
m(m+5)/2\leq L,\quad
\delta\leq\alpha2^{-L-1}
\quad\Longrightarrow\quad a\geq m.
}
\tag{23}
```

If the available program contains at least

```math
k=\left\lfloor\frac{\sqrt{25+8L}-5}{2}\right\rfloor
```

binary-angle bits, restrict to the first $`k`$ and fix the remaining
mask and dirty coordinates in the rank argument. This gives

```math
a\geq k=\sqrt{2L}-O(1)
\tag{24}
```

for this common-interpreter interface. Equivalently, (24) concerns a
family with $`2^k`$ independently specified binary-angle programs; it
does not state that one angle intrinsically requires that many clean
qubits.

A smaller family can already obstruct constant clean work. For
$`M=2^n=N`$ programs, use the first $`n`$ angle bits. At $`L=N`$,
the condition $`n(n+5)/2\leq N`$ holds for $`n\geq5`$, so (23)
forces $`a\geq n`$. This applies to an addressed table only if the
interpreter's action depends on the address through the loaded program,
with the same non-program embeddings and interpreter for every row.
Allowing additional row-dependent logic is a different interface.

The normalization $`\alpha`$ has not been canceled from a physical
success amplitude: it remains in the error threshold. For the desired
normalization-two block $`\alpha=1/2`$, exponentially accurate blocks
satisfy the hypothesis with a constant error-budget margin. Choosing an
exponentially smaller $`\alpha`$ weakens (21) but introduces a separate
normalization/amplification cost; this note grants no free rescaling.

## 4. Consequence for the global construction search

The same-embedding adjoint argument does not justify rejecting all
asymmetric global blocks. Equations (4)–(6) show why that rejection
would be incorrect. The rank theorem supplies a different, precise
stopping rule: a universal binary-angle decoder cannot obtain the
desired constant-clean block from one common two-query XOR interpreter,
even with a high-precision source of fixed dimension and unrestricted
action on failure.

The assumptions that matter are:

- the program register is preserved by the interpreter and modified
  between the two interpreter calls only by the stated XOR mask;
- the same $`D_z`$, input embedding, and output embedding work across
  the full affine family being counted;
- the block error is uniform over every required dirty program value;
- all source and initialized work contributes to $`a`$.

No conclusion follows here for a separately recompiled interpreter or
prepared embedding for each target, an interpreter that also uses
row-dependent target data, a longer query word, or a non-Boolean program
action. A fully synthesized modular Weyl construction, or a directly
compiled complete global block, remains outside the theorem. So does
a construction whose dirty program register is itself changed by the
interpreter rather than used only as a coherent control.

This result does not sum local attenuation costs and does not claim a
new lower bound on the complete Hopf-frame frontier. The remaining
constructive task is to supply and charge one of the interfaces outside
these hypotheses, rather than use a formal Hermitian lift as an
uncharged interpreter.

## 5. A constructive reduction to heterogeneous phase batching

There is a second, positive operator identity that avoids the XOR-program
architecture above. It reduces an addressed rotation to four uses of a
tensor product of heterogeneous phase gates on arbitrary dirty bits.
It needs one additional initialized readout qubit and no modular-addition
table. The identity and its error bound are unconditional; the fast
tensor-product compiler specified below is **not known**.

### 5.1 Exact addressed rotation from a dirty tensor phase

Let $`x\in[S]`$ be an unchanged address, let $`t`$ be the logical target,
and let $`z=(z_0,\ldots,z_{S-1})`$ be an arbitrary dirty bank. The
classically supplied angles define

```math
D=\bigotimes_{j=0}^{S-1}P(\theta_j),
\qquad P(\theta)=\mathrm{diag}(1,e^{i\theta}).
\tag{25}
```

Let $`h`$ be an optional activation predicate on unchanged system bits,
disjoint from $`x,t`$.
Define $`Q_t`$ to flip bank bit $`z_x`$ precisely when the predicate is
true and $`t=1`$. Put
$`Q_{\bar t}=X_tQ_tX_t`$, and define rightmost-first products

```math
E_t=D^\dagger Q_tD Q_t,\qquad
E_{\bar t}=D^\dagger Q_{\bar t}D Q_{\bar t},\qquad
B=E_tE_{\bar t}^\dagger.
\tag{26}
```

On an active computational-basis branch put $`s=1-2z_x`$. The two
commutators return every bank bit and give

```math
E_t=e^{i\theta_x t s},
\qquad E_{\bar t}^\dagger=e^{-i\theta_x(1-t)s},
\qquad B=e^{-i\theta_x sZ_t}.
\tag{27}
```

Inactive branches receive identity.

Initialize a single qubit $`q`$ to zero and let $`R_x`$ XOR the selected
bank bit into it: $`q\leftarrow q\oplus z_x`$. Let $`C_qX_t`$ be a CNOT
from $`q`$ to the target. The complete word

```math
V=R_x(C_qX_t)\,B\,(C_qX_t)R_x
\tag{28}
```

first reads $`q=z_x`$, conjugates the sign in (27), and finally erases
$`q`$. Since $`XZX=-Z`$,

```math
V\bigl(|x,t,z\rangle|0\rangle_q\bigr)
=
\begin{cases}
\bigl(R_z(\theta_x)_t|x,t,z\rangle\bigr)|0\rangle_q,
&\text{active},\\
|x,t,z\rangle|0\rangle_q,&\text{inactive},
\end{cases}
\quad R_z(\theta)=e^{-i\theta Z}.
\tag{29}
```

This is a literal basis identity, so it holds on arbitrary dirty
superpositions and with any reference. Every dirty bank bit is returned
exactly. A fixed Clifford $`K=SH`$, with $`KZK^\dagger=Y`$, turns (29)
into the addressed $`R_y(\theta_x)`$ convention by conjugating the logical
target. No angle-dependent phase is omitted.

The operations in (28) are explicit. A controlled routing network with
$`S-1`$ Fredkins moves the selected bank bit to bank position zero.
Route–CNOT–unroute implements $`R_x`$, and routing around a controlled
bank flip implements $`Q_t`$. With a suffix-zero activation predicate,
the central flip is an at-most-$`n`$-controlled X. The already proved
arbitrary-input borrowed-MCX construction uses $`O(n^2)`$ Toffolis and
may borrow $`q`$: the readout need not be clean while borrowed, and its
entanglement with the bank does not invalidate that complete-space
identity. It returns $`q`$ exactly.

Thus, apart from the four calls to the batch phase operation, (28) uses
$`O(S+n^2)`$ T and Clifford gates and one clean readout qubit. Exact
Fredkin/Toffoli decompositions suffice. The address and suffix are
unchanged; routing is reversed before each batch call. For $`S=1`$,
routing is omitted.

### 5.2 Full-isometry error for an actual batch circuit

The batch circuit need not be exactly diagonal and need not return its
private clean work exactly. Let $`A`$ be an actual unitary on the bank,
its private clean work, and any additional arbitrary dirty helpers.
The bank and those helpers are disjoint from the logical address, target,
suffix, and readout $`q`$. For the embedding $`J_B`$ initializing only that
private clean work, suppose

```math
\|A J_B-e^{i\phi}J_B(D\otimes I_{\rm helpers})\|\leq\delta.
\tag{30}
```

The scalar $`\phi`$ may be arbitrary but must be a common scalar, not
an input-dependent phase. Use $`A`$ and its **actual inverse** in (26).
The inverse has the corresponding complete-isometry error $`\delta`$.
The four appearances contain two forward and two inverse calls, so the
ideal factors $`e^{i\phi}`$ cancel.

All routing, readout, and borrowed-predicate gates are exact and leave
the batch compiler's separate private work untouched. At each term in
the unitary telescoping comparison, its ideal preceding calls have that
work initialized. Consequently the whole word satisfies

```math
\|V_AJ-JU_{\rm addressed}\|\leq4\delta,
\tag{31}
```

where $`J`$ initializes both the readout and batch-private clean work,
and the norm includes every bank/helper input and reference. Earlier
batch leakage is propagated unitarily; no reset or factorization of an
actual intermediate state is assumed. In particular, the final erasure
of $`q`$ is allowed to have leakage in the approximate case: that leakage
is included in (31).

There is a useful exact control check. On an inactive suffix sector,
$`Q_t=Q_{\bar t}=I`$ even for a dense, nondiagonal actual $`A`$ acting
on bank and batch-private work. Therefore each commutator is exactly
$`A^\dagger A=I`$, and the remaining readout/conjugation gates cancel.
Inactive identity does not depend on the batch approximation.

### 5.3 A weaker sufficient batch contract

The full batch approximation (30) is sufficient but stronger than the
echo requires. Let $`X_x`$ flip the selected bank bit and define the
actual unitary

```math
K_x=A^\dagger X_x A X_x.
```

Suppose instead that its complete initialized column satisfies

```math
\|K_xJ_B-J_B U_x\|\leq\epsilon,
\qquad U_x=e^{i\theta_x Z_x}\otimes I_{\rm helpers},
\tag{31a}
```

uniformly in $`x`$. Here $`A`$ acts only on the bank, its private clean
work, and separate dirty helpers, as in Section 5.2. No closeness of
$`A`$ itself to a tensor product is required. All private-work leakage
and all dirty-input dependence are included in (31a).

The actual inverse obeys the same column bound:

```math
\|K_x^\dagger J_B-J_B U_x^\dagger\|
=\|J_B-K_xJ_B U_x^\dagger\|
\leq\epsilon.
\tag{31b}
```

On an active suffix sector the word (26), with $`A`$ in place of
$`D`$, has the exact target-block form

```math
E_tE_{\bar t}^\dagger
=|0\rangle\!\langle0|_t\otimes K_x^\dagger
 +|1\rangle\!\langle1|_t\otimes K_x.
\tag{31c}
```

Thus its complete column error is at most $`\epsilon`$, the maximum
of the two block errors. Conjugating by the exact readout and sign
gates in (28) gives complete addressed-rotation error at most
$`\epsilon`$, including final readout and private-work leakage.
The readout embedding can correlate the target, address, and bank;
the uniform operator bound still applies. The private work remains
disjoint from every readout, routing, and suffix-predicate operation.
On an inactive suffix sector both controlled flips are identity, so
the actual word cancels exactly, with no approximation assumption.

This contract allows additional choices of batch circuit. With no additional work,
its exact version for every bank position is equivalent to
$`A^\dagger X_jA=D^\dagger X_jD`$ for every $`j`$. Writing
$`A=BD`$ shows that all such solutions are precisely those with
$`[B,X_j]=0`$ for every $`j`$: $`B`$ may be any unitary diagonal
in the joint X basis, including an entangling one. This factor cancels
inside each commutator. This characterization is only for the stated
full-space, no-additional-work case.

Equations (31a)–(31c) give a weaker construction target, not a compiler
cost bound. Any proposed implementation must charge $`A`$, its actual
inverse, all initialization, and complete work return. No circuit with
the desired heterogeneous endpoint cost is established here.

### 5.4 The missing primitive and its conditional consequence

A sufficient **unproved** batch hypothesis is the following. For every
$`S`$-fold heterogeneous phase product (25) and precision
$`2^{-\ell}`$, construct an actual Clifford+T circuit satisfying (30)
with

```math
a_{\rm batch}=O(1),\qquad
b_{\rm helpers}=O(S+\ell),\qquad
T_{\rm batch}=O(S+\ell),\qquad
G_{\rm batch}=O(S\ell).
\tag{32}
```

The $`S`$ bank bits themselves are arbitrary logical inputs to this
subroutine. They are additional borrowed bits of the frame compiler;
they are not initialized phase states. All source preparation, arithmetic,
helper return, and actual inverses belong to (32).

Under (32), apply (28) at Hopf depth $`d`$ with
$`S_d=2^d`$ and suffix activation from the prescribed full frame.
Allocate depth error $`2^{-L}2^{d-n}`$ and take

```math
\ell_d=L+n-d+O(1).
\tag{33}
```

The four-call factor in (31) changes only the constant precision margin.
The same constant clean pool and the same dirty bank/helper pools can be
reused across depths using the complete-isometry hybrid. Their largest
required dirty allocation is $`O(N+L)`$.

Summing (32) and the exact overhead gives the conditional full-frame bound

```math
T_F
=O\!\left(\sum_d(2^d+\ell_d+n^2)\right)
=O(N+nL+n^3)
=O(N+nL),
\qquad
G_F=O(NL).
\tag{34}
```

The last simplification uses the uniform elementary bound
$`n^3=O(2^n)`$. At the selected endpoint $`L=N`$, this would give

```math
a=O(1),\quad b=\Theta(N),\quad
T_F=O(N\log N)=o(N^{3/2}),\quad G_F=O(N^2).
\tag{35}
```

Equation (35) is a **conditional implication, not a new compiler upper
bound**. It removes the separate dirty-clock and carry-aware lookup
obligations from this particular reduction, while replacing them with
the full heterogeneous batch-synthesis obligation (32).

One may alternatively posit
$`T_{\rm batch}=O(\sqrt{S\ell}+\ell)`$ only in the range
$`S\leq\ell`$ relevant at $`L=N`$; it yields the same endpoint
implication. That formula is not a valid proposed bound for arbitrary
$`S\gg\ell`$: heterogeneous tensor products have an independent
$`\Omega(S)`$ worst-case requirement, witnessed by T gates on distinct
qubits.

The literature does not currently supply (32). Gosset–Kothari–Wu,
[Section 1.1, Theorem 1.3 and its following discussion](https://arxiv.org/html/2411.04790v3),
prove an $`O(\ell)`$-T and $`O(\ell)`$-ancilla result for
$`O(\log\ell)`$ potentially different one-qubit factors, and explicitly
leave an extension to $`\Omega(\ell)`$ factors open. Their Theorem 1.4
obtains $`O(S+\ell)`$ for **identical** factors, using growing initialized
work; that is a different promise. The constant-clean, arbitrary-input
hypothesis (32) is stronger than the open heterogeneous batching target
at $`S=\Theta(\ell)`$. This reduction does not establish that it is easier.


## 6. Checks and evidence boundary

The proof above is finite-dimensional linear algebra. Independent
checks evaluated 30 exact rational complex instances of the Walsh
product identity (19), for one through four binary factors. Numerical
full block matrices for $`m=1,\ldots,5`$ verified (17), the equal-singular-
value identity underlying (20), and the conservative bound (22).
The largest observed Walsh diagonalization discrepancy was below
$`2.4\times10^{-15}`$.

The independent [structural test suite](../../tests/test_constant_clean_structure.py)
also checks the full program-space echo, differing-flag lift, common-kernel
factorization, and Fourier singular-value count. Its tensor-phase tests use
a complete 64-dimensional circuit and all 32 initialized-readout columns.
They verify the ideal dirty/reference return, literal phase, both required
inverse signs, and exact inactive cancellation. A dense, nondiagonal
approximate batch word with a common scalar phase obeys the full four-call
error bound while exhibiting nonzero readout leakage; an explicit
dirty/reference Bell input is checked as well. All 12 tests in that suite
pass; its additional cyclic and modular tests concern companion notes.

These checks corroborate signs, normalization, and multiplicity. They
do not replace the factorization and singular-value argument, and they
do not certify an endpoint circuit. No existing core theorem or
published repository claim is changed by this follow-up.
