# A compiler from an operator source on dirty qubits

Two initialized qubits and a precision-sized bank of arbitrary dirty
qubits suffice for the following full-frame upper bound. The construction
uses a linear combination of anticommuting Pauli operators to encode
precision coefficients. No precision register is initialized to a
geometric state.

**Theorem.** Let $`N=2^n`$, $`n\geq1`$, $`0<\eta\leq1/64`$,
$`L=\max\{6,\lceil\log_2(1/\eta)\rceil\}`$, and let $`W`$ be the
prescribed complete real Hopf frame, with the rotation convention
$`R_y(\theta)=e^{-i\theta Y}`$. If

```math
a\geq2,\qquad b\geq L+n+7,
\tag{1}
```

then a coherent Clifford+T circuit $`V`$ satisfies

```math
\|VJ_a-J_a(W\otimes I_b)\|\leq\eta,
\qquad
T=O(N+nL),\qquad G=O(NL).
\tag{2}
```

The norm is over all logical and dirty inputs and therefore includes
arbitrary references. It includes all initialized-work leakage and
dirty-work return. Lookup selectors, additional word banks, and the dirty
suffix control return exactly after their completed subroutines. The
operator core may have residual disturbance; its approximate return is
included in the same error bound, together with any reference correlations.
All inverses are actual circuit inverses; there are
no measurements, resets, supplied catalysts, or uncharged quantum oracles.
Angles must be effectively specified so that certified sine and cosine
approximations can be computed. That classical evaluation and table
construction are separate preprocessing costs, excluded from T and G;
the resulting quantum lookup circuits are fully charged below.

At $`L=N`$, choosing $`a=2`$ and $`b=N+n+7`$ gives

```math
T=O(N\log N)=o(N^{3/2}),\qquad G=O(N^2).
\tag{3}
```

This improves the previously retained upper bound at that explicit
workspace allocation. It does not establish $`O(N)`$ T count, nor does
it claim the same result for every constant prefactor in $`b=\Theta(N)`$
or for fewer than two initialized qubits.

## 1. The operator source and its exact native circuit

On $`m\geq2`$ arbitrary dirty qubits define

```math
\Gamma_j=Z_0Z_1\cdots Z_{j-1}X_j,\qquad 0\leq j<m.
\tag{4}
```

Each operator is a Hermitian involution. For $`j<k`$, the X on wire
$`j`$ anticommutes with the Z on that wire in $`\Gamma_k`$, and all
other overlaps commute. Hence

```math
\Gamma_j\Gamma_k+\Gamma_k\Gamma_j=2\delta_{jk}I.
\tag{5}
```

For adjacent generators put

```math
R_j=\exp\!\left(\frac{i\pi}{8}Y_jX_{j+1}\right),
\qquad
U_m=R_{m-2}\cdots R_0,\qquad
M_m=U_mX_0U_m^\dagger.
\tag{6}
```

The sign in (6) matters. Since
$`i\Gamma_j\Gamma_{j+1}=Y_jX_{j+1}`$, direct conjugation gives

```math
R_j\Gamma_jR_j^\dagger
=\frac{\Gamma_j+\Gamma_{j+1}}{\sqrt2}.
\tag{7}
```

The same rotation commutes with every other $`\Gamma_k`$ except
$`\Gamma_j,\Gamma_{j+1}`$. Successively splitting the last remaining
coefficient therefore gives

```math
M_m=\sum_{j=0}^{m-1}a_j\Gamma_j,\qquad
a_j=
\begin{cases}
2^{-(j+1)/2},&j<m-1,\\
2^{-(m-1)/2},&j=m-1.
\end{cases}
\tag{8}
```

The last two squared coefficients are equal and
$`\sum_j a_j^2=1`$. Equations (5) and (8) also directly prove
$`M_m^\dagger=M_m`$ and $`M_m^2=I`$ on the entire dirty Hilbert space.

Every $`R_j`$ is a weight-two Pauli $`\pi/8`$ rotation, implemented
with one T-dagger and a constant number of Clifford gates, up to a
common scalar. That scalar cancels in $`U_mX_0U_m^\dagger`$.
Thus an exact circuit for $`M_m`$ uses $`2(m-1)`$ T gates and
$`O(m)`$ Clifford gates, with no initialized work.

A controlled source costs the same T count. For either control value
$`v\in\{0,1\}`$,

```math
C_{a=v}(M_m)=U_m\,C_{a=v}(X_0)\,U_m^\dagger.
\tag{9}
```

The central controlled X is Clifford, including a negative control.
The two surrounding source circuits are unconditional, so (9) does
not require controlled T gates or introduce a branch-dependent scalar.

The anticommuting-operator representation is established Clifford-algebra
machinery. Kerenidis and Prakash define the same operators and prove
full-Hilbert-space Clifford-loader implementations in
[Sections 4.1–4.3, Definition 4.4, Definition 4.6, and Theorem 4.9](https://arxiv.org/html/2202.00054v2).
The name “Clifford loader” refers to the Clifford algebra, not a claim
that its arbitrary-angle circuit uses only Clifford gates. Here the
fixed geometric coefficients give the explicit native specialization
(6)–(9). The symmetric overlap identity below follows from (5);
the related product decomposition is also recorded in
[Chee et al., Appendix C](https://arxiv.org/pdf/2301.07477).

## 2. Exact signed dyadic coefficients

A bit string $`f\in\{0,1\}^m`$ defines the Pauli mask

```math
P_f=\prod_{j=0}^{m-1}Z_j^{f_j},\qquad
N_f=P_fM_mP_f.
\tag{10}
```

The mask is its own actual inverse. Conjugating by $`Z_j`$ changes
the sign of precisely $`\Gamma_j`$. Therefore

```math
N_f=\sum_j a_j(-1)^{f_j}\Gamma_j,\qquad
\frac{M_mN_f+N_fM_m}{2}=c_fI,
\quad
c_f=\sum_j a_j^2(-1)^{f_j}.
\tag{11}
```

The mixed terms cancel pairwise by anticommutation. This is an operator
identity on every dirty input, including entangled inputs, rather than
an expectation value on a prepared source state.

Here is an encoding covering the endpoints and zero without requiring
an exact comparison against a real rounding tie. Given $`c\in[-1,1]`$,
put $`e=2^{1-m}`$ and compute a certified rational estimate
$`\widehat c`$ with $`|\widehat c-c|\leq e/4`$. Clamp the estimate
to $`[-1,1]`$, which does not increase this error, and choose

```math
k=\mathrm{round}\bigl((1-\widehat c)2^{m-2}\bigr),
\qquad 0\leq k\leq2^{m-1}.
\tag{12}
```

If $`k<2^{m-1}`$, take the first $`m-1`$ bits of $`f`$ to be the
binary fraction representing $`k/2^{m-1}`$, and set the final bit
to zero. If $`k=2^{m-1}`$, set every bit to one. Equation (8) then gives

```math
c_f=1-\frac{k}{2^{m-2}},\qquad
|c_f-\widehat c|\leq e,\qquad |c_f-c|\leq\frac54e.
\tag{13}
```

The rounding in (12) is rational arithmetic with either fixed tie rule.
Known literal entries $`c=1`$, $`c=0`$, and $`c=-1`$ are assigned
their exact encodings; in particular, inactive rows use exact values.
No amplitude is divided out or normalized after selecting the digits.

## 3. Dirty programming and a one-flag scalar block

Let $`y`$ be a k-bit address and let $`f(y)`$ be an arbitrary
classically specified m-bit table. The exact XOR table operation is

```math
Q_f:\ |y,z,w\rangle\longmapsto
|y,z\oplus f(y),w\rangle,
\tag{14}
```

where the m output bits $`z`$ and k selector bits $`w`$ are all
arbitrary dirty inputs. It costs $`O(2^k)`$ Toffolis and
$`O(2^k m+2^k)`$ Clifford gates, with no clean work.

For completeness, this is the whole-word extension of the
[two-pass dirty traversal](BORROWED_WORKSPACE_COMPILER.md#2-exact-dirty-table-and-reflection-interpreter).
Along a depth-first address path, use dirty selectors
$`v_1=w_1\oplus\ell_1`$ and
$`v_i=w_i\oplus v_{i-1}\ell_i`$. The leaf selector equals the row
predicate plus an unwanted term independent of $`\ell_1`$.
At a leaf, CNOT it into every output position whose table bit is one.
Undo selector updates when returning along the path. A second traversal
omitting the first selector updates has exactly the unwanted term;
compose with its inverse. The output XORs cancel those terms, and
every selector returns. There are $`O(2^k)`$ internal updates and
$`O(2^km)`$ leaf CNOTs. The argument holds for arbitrary output words
and is a literal, phase-free permutation. For $`k=0`$, use fixed X gates.

Conjugating (14) by Hadamards on the dirty core implements the required
mask directly:

```math
P_{f(y)}=H^{\otimes m}Q_fH^{\otimes m}.
\tag{15}
```

No separate initialized program word is loaded. The selector work returns
exactly, even while the core contains a state changed by the source.

With one initialized flag a, define

```math
\mathcal S_f
=H_a\,C_{a=0}(M_m)\,N_f\,C_{a=1}(M_m)\,H_a.
\tag{16}
```

Before the final Hadamard, the two branches apply $`M_mN_f`$ and
$`N_fM_m`$. Thus (11) proves the accepted block

```math
(\langle0|_a\otimes I)\mathcal S_f(|0\rangle_a\otimes I)
=c_{f(y)}I_{\rm core,selectors}.
\tag{17}
```

The rejected block is retained coherently. Equation (16) contains three
source uses and two mask queries. Only the source copies are controlled
by a; the masks are not. Its resources are consequently

```math
T(\mathcal S_f)=O(2^k+m),\qquad
G(\mathcal S_f)=O(2^km+m),\qquad
a=1,\quad b=m+k.
\tag{18}
```

This is a charged one-clean block encoding of an arbitrary dyadic real
table, with a scalar accepted action on the entire dirty space.

## 4. Two flags encode a suffix-controlled rotation

At Hopf depth d, let $`x`$ be the d-bit prefix, t the rotation target,
and $`h`$ the Boolean predicate that the lower suffix is all zero.
Here h is a function of unchanged logical wires, not a clean register.
For an empty suffix it is the constant one.

Flag b chooses between the active cosine and sine tables. Let
$`f_{\rm act}(b,x)`$ be their m-bit encodings from (12)–(13).
The inactive coefficients one and zero have the fixed encoding

```math
f_0(b)=b e_0,\qquad
g(b,x)=f_{\rm act}(b,x)\oplus f_0(b),\qquad
f(b,x,h)=f_0(b)\oplus h g(b,x).
\tag{19}
```

Indeed, the all-zero word gives coefficient one, while flipping only
the first sign changes the coefficient by $`2a_0^2=1`$ and gives
zero. The inactive Pauli mask is the Clifford
$`P_0=\mathrm{CZ}_{b,{\rm core}\,0}`$.

The conditional mask requires no clean suffix flag. Allocate one
arbitrary dirty control z, separate from the core and selectors.
Let G toggle z by h, using the exact borrowed-MCX construction and
borrowing the logical target t. It costs $`O(n^2)`$ Toffolis and
returns t on every input. Let $`Q_{zg}`$ be the dirty XOR table query
whose unchanged address is $`(z,b,x)`$ and whose row is
$`z g(b,x)`$. It has $`4S`$ rows, $`S=2^d`$, and uses $`d+2`$
dirty selectors.

The chronological sequence $`G,Q_{zg},G,Q_{zg}`$ adds
$`(z\oplus h)g\oplus zg=hg`$ to the core and returns z, every
selector, and the borrowed target. In rightmost-first notation,
$`\mathcal E=Q_{zg}GQ_{zg}G`$. Therefore

```math
P_{f(b,x,h)}
=P_0 H^{\otimes m}\mathcal E H^{\otimes m}.
\tag{19a}
```

This is an exact full-space identity, including unknown or entangled z
and core inputs. Each use of G restores its borrowed target before the
next query. Its suffix controls are disjoint from that target and the
table address. The complete mask costs $`O(S+n^2)`$ T gates and
$`O(Sm+n^2)`$ Clifford gates. In (10), use this actual mask and its
actual inverse.

Let $`c_{x,h}`$ and $`s_{x,h}`$ be the encoded coefficients.
The literal target operation $`XZ=-iY`$ is Clifford. Its controlled
version is the product of a CNOT and a controlled Z, with the order
chosen to give XZ on the b=1 branch. Define

```math
Q=H_b\,C_b(XZ_t)\,\mathcal S_{f(b,x,h)}\,H_b.
\tag{20}
```

Both the scalar block and the controlled target operation preserve b
and x; the suffix is unchanged by the complete mask circuit. The dirty
control and selectors return exactly after every mask use. With $`J`$
initializing only the flags a and b, the accepted block is

```math
B=J^\dagger QJ
=\frac12\left(c_{x,h}I_t-i s_{x,h}Y_t\right)
 \otimes I_{\rm core,control,selectors}.
\tag{21}
```

For the prescribed Hopf layer $`L_d`$, which applies
$`R_y(\theta_x)`$ when h=1 and identity when h=0,

```math
\|2B-(L_d\otimes I_{\rm dirty})\|
\leq\frac{5\sqrt2}{4}\,2^{1-m}.
\tag{22}
```

The same bound holds across the coherent address direct sum.
Inactive rows are exact: $`c_{x,0}=1`$ and $`s_{x,0}=0`$.
The possibly imperfect length $`c_{x,h}^2+s_{x,h}^2`$ is not
silently normalized.

## 5. Amplification includes rejected-space error

Apply the robust normalization-two lemma from
[the fault-tolerant compiler chapter](../../docs/FAULT_TOLERANT_COMPILER.md).
Robust oblivious amplitude amplification and its cubic accepted-block
identity are established in Berry, Childs, Cleve, Kothari, and Somma,
*Physical Review Letters* **114**, 090502 (2015),
[Eqs. (11)–(15), arXiv:1412.4687](https://arxiv.org/abs/1412.4687).
The local proof below records the full-isometry leakage estimate needed
for the workspace-return contract.
For an actual unitary Q, its initialized embedding J, a unitary W, and
$`\zeta=\|2J^\dagger QJ-W\|\leq1/4`$, put

```math
R=I-2JJ^\dagger,\qquad
\mathcal A=-QRQ^\dagger RQ.
\tag{23}
```

Then $`\|\mathcal A J-JW\|\leq4\zeta`$, including rejected-space
leakage. A short proof is worth retaining here. Put
$`\delta=\zeta/2`$ and use the polar decomposition $`B=VH`$.
Then $`\|H-I/2\|\leq\delta`$ and $`\|V-W\|\leq4\delta`$.
The accepted amplified block is
$`3B-4BB^\dagger B=V(3H-4H^3)`$. Since

```math
3(1/2+e)-4(1/2+e)^3=1-6e^2-4e^3,
```

the complete isometry distance to $`JV`$ is at most
$`\sqrt{12+8\delta}\,\delta`$. Adding the polar-unitary error gives
at most $`8\delta=4\zeta`$. This proof controls the full output,
not only its accepted compression.

In the present construction R tests only the two flags a and b and is
a fixed Clifford reflection. The leading minus sign is a literal
Clifford scalar, implementable by $`XZXZ=-I`$. There are two forward
calls to Q and one actual inverse, so every source and query inverse
has the same charged cost.

The dirty suffix echo is part of each actual Q and its inverse.
It returns its dirty control and borrowed target exactly on all inputs,
even if they are entangled with flags after an earlier call. Thus the
amplified physical stage has two initialized qubits and

```math
\|\widetilde L_dJ_2-J_2(L_d\otimes I_b)\|
\leq5\sqrt2\,2^{1-m}\leq2^{4-m}.
\tag{24}
```

Equation (24) includes all core, control, selector, and flag inputs
in their stated roles. On an inactive suffix, (21) has $`B=I/2`$
exactly. Applying the lemma with $`\zeta=0`$ shows that the actual
amplified stage is exactly identity on the initialized-flag columns,
including dirty-work return. The pre-amplification word Q may have a
rejected component. There is no source-state preparation or fresh
initialization between calls.

## 6. Precision, workspace, and full-frame composition

At depth $`d=0,\ldots,n-1`$, choose

```math
m_d=L+n-d+4.
\tag{25}
```

The source uses $`m_d`$ dirty qubits and the lookup uses $`d+2`$
additional dirty selectors, together with one dirty suffix control.
Their sum is exactly

```math
m_d+(d+2)+1=L+n+7.
\tag{26}
```

The same arbitrary dirty pool is repartitioned between these roles
at each depth. No source-private helper or initialized lookup output
is missing from (26). The two clean qubits are exactly the scalar and
sector flags a and b.

Each source call uses $`2(m_d-1)`$ T gates. Each Q uses three such
calls, of which two are controlled using (9), and two phase-mask
circuits. Each mask contains two whole-word XOR queries and two
predicate toggles. Amplification multiplies these costs by three.
The target-sector Cliffords, two-flag reflections, and predicate
compute/uncompute are also charged. Thus

```math
T_d=O(2^d+m_d+n^2),\qquad
G_d=O(2^dm_d+m_d+n^2).
\tag{27}
```

Equation (24) is at most $`2^{-L}2^{d-n}`$.
A full-isometry hybrid composes the prescribed Hopf layers in their
specified order. Its ideal preceding layers return all work; actual
earlier leakage is propagated unitarily. Consequently

```math
\|VJ_2-J_2(W\otimes I_b)\|
\leq\sum_{d=0}^{n-1}2^{-L}2^{d-n}
<2^{-L}\leq\eta.
\tag{28}
```

Finally,

```math
\sum_dT_d=O(N+nL+n^3)=O(N+nL),
\qquad
\sum_dG_d=O(NL).
\tag{29}
```

Here $`n^3=O(2^n)`$ and
$`\sum_d2^d(n-d)=O(N)`$. This proves (1)–(3), with the complete
prescribed frame, rather than only its first prepared-state column.

An alternative reservation exchanges one dirty wire for one clean wire.
With a third initialized qubit, compute h into it once before OAA, query
the table with address $`(h,b,x)`$ directly, and erase h afterward.
The suffix is preserved throughout and the borrowed-MCX identity
returns its target helper on all inputs. This gives the same basic
bound with $`a=3`$ and $`b\geq L+n+6`$. The bank tradeoff below
also holds for this variant with threshold $`b\geq2(L+n+6)`$.

## 7. Trading additional dirty banks for lookup cost

The unary lookup above can be replaced by a whole-word dirty-bank
SelectSwap query. Consider an S-row, m-bit table, with $`S=2^k`$,
and choose a power of two $`1\leq\lambda\leq S`$. Reserve
$`\lambda`$ additional arbitrary m-bit banks, separate from the
operator core. Split the address into a high part and a low part selecting
one of the banks.

For each high address, the dirty traversal of Section 3 loads the
$`\lambda`$ table words into their respective banks by XOR. This loader
$`\mathcal L`$ costs $`O(S/\lambda)`$ Toffolis and $`O(Sm)`$
Clifford gates. It needs at most k dirty selectors. Let
$`\mathcal R`$ route the low-address-selected bank to position zero,
using $`O(\lambda m)`$ Fredkins, and let C XOR that bank into the
separate operator core. Use the following chronological sequence:

```math
\mathcal L,\ \mathcal R,\ C,\ \mathcal R^\dagger,\
\mathcal L^\dagger,\ \mathcal R,\ C,\ \mathcal R^\dagger.
\tag{30}
```

If the original selected bank word is z, the two contributions to the
core are $`z\oplus f(y)`$ and z. Thus (30) implements (14) on an
arbitrary core input and returns every bank and selector exactly.
This basis identity extends to arbitrary superpositions and references.
The inverse loader is applied only after routing has been reversed;
the core is not among its targets. This is the whole-word version of
the dirty-bank SelectSwap pattern in
[Low, Kliuchnikov, and Schaeffer](https://arxiv.org/abs/1812.00954).

Including both traversals and all routes gives

```math
T_{\rm query}=O(S/\lambda+\lambda m),\qquad
G_{\rm query}=O(Sm),\qquad
b_{\rm query}\leq m+\lambda m+k.
\tag{31}
```

No bank or core output is initialized. Conjugating the core by Hadamards
still gives a phase mask. The dirty suffix echo of Section 4 uses a
constant number of these exact queries, so its cancellation identity
and the OAA error proof are unchanged.

For the real frame put $`B_0=L+n+7`$. This reserves the core, all
selectors, and the separate dirty suffix control at every depth.
Suppose $`b\geq2B_0`$, leaving $`K=b-B_0\geq b/2`$ bank wires.
At each depth $`K\geq m_d`$. Choose $`\lambda`$ by rounding the
following value down to the largest power of two not exceeding it:

```math
\max\!\left\{1,\min\!\left(S,\sqrt{S/m_d},K/m_d\right)\right\},
\qquad S=2^{d+2}.
\tag{32}
```

The $`\lambda m_d`$ word-bank wires then fit. When $`m_d>S`$,
the choice $`\lambda=1`$ is covered by the additive $`m_d`$ term.
Equations (31)–(32), together with the source and suffix-toggle costs,
give

```math
T_d=O\!\left(\sqrt{S m_d}+m_d+\frac{S m_d}{b}+n^2\right),
\qquad G_d=O(Sm_d+m_d+n^2).
\tag{33}
```

The previously proved error and workspace-return contracts still hold.
Using
$`\sum_d\sqrt{2^dm_d}=O(\sqrt{NL})`$,
$`\sum_d2^dm_d=O(NL)`$, and $`n^3=O(2^{n/2})`$ yields

```math
a=2,\quad b\geq2(L+n+7)
\quad\Longrightarrow\quad
T=O\!\left(\sqrt{NL}+nL+\frac{NL}{b}\right),
\qquad G=O(NL).
\tag{34}
```

The two sum bounds follow by writing $`k=n-d`$ and summing
$`2^{-k/2}\sqrt{L+k+4}`$ and $`2^{-k}(L+k+4)`$.
The same pool is reused at all depths; the fixed reservation B_0 is
kept separate from the additional word banks.

For this fixed two-clean budget, $`q=n+2+b=\Theta(b)`$.
Consequently (34) matches the
[existing full-frame lower bound](../../docs/FAULT_TOLERANT_COMPILER.md#10-matching-lower-bounds-and-their-lineage)
whenever the extra $`nL`$ term is absorbed. Two sufficient regimes,
subject to the workspace threshold in (34), are

```math
n^2L\leq N
\quad\text{or}\quad
b\leq N/n.
\tag{35}
```

The first absorbs $`nL`$ into $`\sqrt{NL}`$; the second absorbs it
into $`NL/b`$. This is a statement at the specified constant clean
budget, not at a budget with an unrestricted number of clean qubits.
At $`L=N`$, (34) retains the $`N\log N`$ source cost.

## 8. Literal diagonal unitaries and phase-dressed frames

The scalar block also gives a direct compiler for an arbitrary
classically specified diagonal unitary

```math
D_\phi=\sum_{x=0}^{N-1}e^{i\phi_x}|x\rangle\langle x|.
\tag{36}
```

Use the cosine and sine sign tables for $`\phi_x`$ with address
$`(b,x)`$, and omit both the rotation target and the suffix predicate.
Replace the controlled target XZ in (20) by a phase S on the sector
flag b:

```math
Q_{\rm diag}=H_b S_b\,\mathcal S_{f(b,x)}\,H_b,\qquad
J^\dagger Q_{\rm diag}J
=\frac12\,\mathrm{diag}(c_x+i s_x)\otimes I_{\rm dirty}.
\tag{37}
```

The two flags a and b are the only initialized wires. The literal factor
i on the sine branch fixes the phase in (36); no common or
address-dependent scalar is discarded. The same certified rounding,
actual inverse, normalization-two amplification, and complete
isometry estimate apply.

For desired error $`2^{-\ell}`$, $`\ell\geq6`$, take
$`m=\ell+4`$. There are $`n+1`$ dirty selectors and no dirty suffix
control, so the exact base reservation is
$`B_{\rm diag}=\ell+n+5`$. This proves

```math
a=2,\quad b\geq\ell+n+5
\quad\Longrightarrow\quad
T=O(N+\ell),\qquad G=O(N\ell),
\tag{38}
```

with
$`\|V_{\rm diag}J_2-J_2(D_\phi\otimes I_b)\|\leq2^{-\ell}`$.
Additional dirty banks give

```math
a=2,\quad b\geq2(\ell+n+5)
\quad\Longrightarrow\quad
T=O\!\left(\sqrt{N\ell}+\ell+\frac{N\ell}{b}\right),
\qquad G=O(N\ell).
\tag{39}
```

Since $`q=n+2+b=\Theta(b)`$, (39) matches the diagonal lower bound in
the same model, with every initialized and borrowed wire included.
The GKW diagonal theorem cited in
[Section 10.1 of the main proof](../../docs/FAULT_TOLERANT_COMPILER.md#101-the-real-frame-contains-arbitrary-diagonals)
supplies $`\Omega(\sqrt{N\ell}+\ell)`$.
The [fixed-width circuit count in Section 10.2](../../docs/FAULT_TOLERANT_COMPILER.md#102-fixed-width-coherent-counting),
applied to an $`N`$-phase diagonal grid packing, supplies
$`\Omega(N\ell/q)`$ when $`q^2`$ is a sufficiently small multiple of
$`N\ell`$; otherwise that term is absorbed by $`\sqrt{N\ell}`$.
In particular, the diagonal problem has an $`O(N)`$
construction at $`\ell=N`$ with a sufficiently large linear dirty bank.

There is also an immediate, explicitly scoped complex extension.
For independently supplied real Hopf angles and diagonal phases, consider

```math
U=D_\phi W_{\mathbb R}.
\tag{40}
```

Compile $`W_{\mathbb R}`$ and then $`D_\phi`$, each to error at most
$`\eta/2`$. With $`L`$ as in the theorem, use $`L'=L+1`$.
The real-frame reservation is $`L+n+8`$ and dominates the diagonal
reservation $`L+n+6`$. Both circuits reuse the same two clean flags
and the same dirty pool. A unitary hybrid gives total complete-isometry
error at most $`\eta`$, including any work leakage from the first
circuit.

Thus $`a=2`$ and $`b\geq L+n+8`$ give
$`T=O(N+nL)`$ and $`G=O(NL)`$ for (40). If
$`b\geq2(L+n+8)`$, the improved bound is
$`T=O(\sqrt{NL}+nL+NL/b)`$, with the same Clifford count.
This covers the full phase-dressed frame (40), not an arbitrary complex
unitary and not only a prepared state.

## 9. Verification and scope

The companion [operator-source tests](../../tests/test_operator_source_compiler.py)
check small complete matrices for the anticommuting source, its native
gate word and actual adjoint, all sign masks, dyadic endpoints, and the
dirty-selector phase query. They also check the two-flag rotation block,
amplification on all initialized columns, dirty/reference return, and
negative controls. The dirty suffix echo is checked on every input of
a nine-wire fixture, including arbitrary borrowed control and target
bits; a complete source/OAA fixture checks its coherent composition.
Whole-word SelectSwap tests cover arbitrary core, bank, and selector
inputs. Direct diagonal tests retain literal common phase and
dirty/reference return. The earlier three-clean, two-layer fixture
remains a hybrid-composition baseline. These checks support the signs
and normalization;
the dimension-independent identities and resource proof above establish
the asymptotic statement.

The construction combines established Clifford-loader algebra, exact
dirty XOR lookup, a fixed native geometric specialization, and a
normalization-two block. It implements one address-selected rotation. This is not a simultaneous
tensor product of all the table rotations. In particular, its programmed
mask depends on the address, whereas the earlier batch-extraction converse
requires one common circuit for all selected bank commutators. The proof
therefore does not establish the fast heterogeneous tensor-batch hypothesis
or use it as a subroutine.

The unrestricted $`O(N)`$ endpoint remains open. The established new
upper bound is $`O(N\log N)`$ at the explicit two-clean,
$`N+n+7`$-dirty allocation.
