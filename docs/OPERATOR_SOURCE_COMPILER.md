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

### Exact source costs, including returned helpers

The displayed source word is convenient, but its uncontrolled version can
save two T gates. In fact, for $`m\ge2`$,

```math
T_{\mathrm{exact}}(M_m)=2m-4,\qquad
T_{\mathrm{exact}}(C_{a=v}(M_m))=2m-2.
```

These exact minima allow arbitrarily many initialized stabilizer ancillas
and arbitrary dirty helpers returned under the complete-input contract.
No nonstabilizer resource states, measurements, or postselection are supplied.

For the upper bound, the two-generator base is Clifford:

```math
M_2=\frac{X_0+Z_0X_1}{\sqrt2}=C H_0 C^\dagger,
\qquad C=H_1\mathrm{CNOT}_{1\to0}.
```

Conjugating this base by $`R_{m-2}\cdots R_1`$ produces $`M_m`$ with
$`2(m-2)`$ T gates. The product is empty when $`m=2`$. Equation (9)
already attains $`2(m-1)`$ for either value of the control.

For the lower bound, use the standard Pauli-transfer denominator method
of [Gosset–Kliuchnikov–Mosca–Russo, Sections 2.3 and 4](https://arxiv.org/html/1308.4134v1).
Every Pauli-transfer coefficient of a Clifford+T circuit with $`t`$ T or
T-dagger gates lies in $`(\sqrt2)^{-t}\mathbb Z[\sqrt2]`$: Clifford
conjugations permute signed Paulis, and each T conjugation introduces at
most one factor $`1/\sqrt2`$.

Initializing returned clean helpers does not supply an extra denominator.
If a circuit $`V`$ implements $`U\otimes I_r`$ on $`d`$ data qubits,
$`r`$ dirty helpers and $`a`$ clean helpers, define
$`R_V(A,B)=2^{-(d+r+a)}\mathrm{Tr}(AVBV^\dagger)`$. For a data Pauli
$`P`$, its effective transfer coefficient is

```math
\begin{aligned}
c&=2^{-(d+r)}\mathrm{Tr}\!\left[
(P\otimes I_r\otimes I_a)V
(P\otimes I_r\otimes|0^a\rangle\langle0^a|)V^\dagger\right]\\
&=\sum_{s\in\{0,1\}^a}
R_V(P\otimes I_r\otimes I_a,\,P\otimes I_r\otimes Z^s).
\end{aligned}
```

The stabilizer projector's factor $`2^{-a}`$ cancels the change in trace
normalization. The sum therefore has the same denominator bound. Any
returned pure stabilizer initialization reduces to this case by Cliffords.

Take $`P=Z_{m-1}`$. It commutes with every generator except the last, so
Pauli orthogonality gives

```math
2^{-m}\mathrm{Tr}(P M_m P M_m)=1-2a_{m-1}^2=1-2^{2-m}.
```

For $`m\ge3`$ this rational has odd numerator and denominator
$`2^{m-2}`$, hence least square-root-of-two denominator exponent
$`2m-4`$. For the controlled source, the transfer coefficient of
$`I_a\otimes P`$ averages its two control sectors and equals
$`1-2^{1-m}`$, whose exponent is $`2m-2`$. The uncontrolled $`m=2`$
lower bound is zero. These witnesses prove both minima.

This is optimality of the exact source primitive. It does not make source
costs additive across a larger circuit, nor lower-bound the unrestricted
approximate frame problem. The [native-word tests](../tests/test_operator_source_compiler.py)
check both source words and transfer witnesses for $`m=2,3,4,5`$.

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
Let G toggle z by h, using the exact
[borrowed-MCX construction](BORROWED_WORKSPACE_COMPILER.md#3-an-exact-echo-selects-a-logical-sector) and
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
[the fault-tolerant compiler chapter](FAULT_TOLERANT_COMPILER.md).
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
[existing full-frame lower bound](FAULT_TOLERANT_COMPILER.md#10-matching-lower-bounds-and-their-lineage)
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
[Section 10.1 of the main proof](FAULT_TOLERANT_COMPILER.md#101-the-real-frame-contains-arbitrary-diagonals)
supplies $`\Omega(\sqrt{N\ell}+\ell)`$.
The [fixed-width circuit count in Section 10.2](FAULT_TOLERANT_COMPILER.md#102-fixed-width-coherent-counting),
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

### 8.1 General one-qubit multiplexors with two clean qubits

The same operator source compiles a family beyond the Hopf frame. A
one-qubit multiplexor is a prescribed unitary

```math
U=\sum_{x=0}^{N-1}|x\rangle\langle x|\otimes U_x,
\qquad U_x\in\mathrm U(2),\qquad N=2^n,
```

on an $`n`$-qubit address and one target qubit. Every block is supplied;
the task concerns the complete operator, including relative phases
between addresses.

**Corollary — optimal two-clean multiplexor synthesis.** Let $`n\geq1`$,
$`0<\eta\leq1/64`$, and
$`L=\max\{6,\lceil\log_2(1/\eta)\rceil\}`$. Assume certified
approximations to the entries of each promised unitary $`U_x`$ can be
computed to any requested accuracy. Two clean qubits and
$`b\geq B_0=L+n+7`$ arbitrary dirty qubits suffice for a coherent
Clifford+T circuit satisfying

```math
\|VJ_2-J_2(U\otimes I_b)\|\leq\eta,
\qquad T=O(N+L),\qquad G=O(NL).
```

If $`b\geq2B_0`$, the bound improves to

```math
T=O\!\left(\sqrt{NL}+L+\frac{NL}{b}\right),
\qquad G=O(NL).
```

For every $`b\geq2B_0`$, the worst-case optimum for this two-clean
model therefore obeys

```math
\tau_{\mathrm{mux}}(n,b,\eta)
=\Theta\!\left(\sqrt{NL}+L+\frac{NL}{n+3+b}\right).
```

The total physical width is $`q=n+3+b`$: address, target, two clean
flags, and dirty work. Literal block phases are retained. The contract
holds on every address-target-dirty input and every external reference.
The operator core has approximate return charged in the displayed norm;
lookup selectors and additional word banks return exactly. No quantum
oracle, measurement, reset, or supplied source state is used.
Classical entry evaluation, Euler approximation, and sign-table generation
are additional preprocessing; the result places no universal time bound on
the supplied entry evaluators.

*Proof.* Four factors suffice. With the convention
$`R_P(\theta)=e^{-i\theta P}`$, every block has an Euler representation

```math
U_x=e^{i\alpha_x}R_z(\beta_x)R_y(\gamma_x)R_z(\delta_x).
```

All four angles can be chosen in $`[-\pi,\pi]`$, with
$`\gamma_x\in[0,\pi/2]`$. This algebraic representation is not an
assumption of a computable, continuous inverse chart. Instead, put
$`\rho=2^{-L}/16`$ and obtain a dyadic tuple for each block whose
displayed product $`\widehat U_x`$ satisfies
$`\|\widehat U_x-U_x\|\leq\rho`$ as a literal matrix.

A finite certified construction of these tuples is available even at
singular Euler charts. Enumerate a dyadic grid in $`[-4,4]^4`$ with
mesh at most $`\rho/16`$. Changing the four angles changes the operator
by at most the sum of their absolute changes, by unitary telescoping.
Consequently a grid tuple approximates an exact Euler tuple to operator
error at most $`\rho/8`$. Evaluate candidate matrices and the supplied
entries with rational enclosures, and select a candidate whose Frobenius
distance has a certified upper bound below $`\rho`$. Such a candidate
exists since $`\|A\|_F\leq\sqrt2\|A\|`$ for a two-by-two matrix.
Refining the enclosures for all candidates until one passes terminates
without requiring an
exact determinant phase, an exact zero test, or division by a vanishing
matrix entry. This finite search can be expensive; it is not included
in the quantum gate counts. If certified Euler angles are already the
input representation, this search is unnecessary.

Let $`\widehat U=\bigoplus_x\widehat U_x`$. Orthogonality of the
address sectors gives $`\|\widehat U-U\|\leq\rho`$, with no factor
of $`N`$. Compile the four addressed factors independently using the
same two flags and dirty pool.

For an addressed y rotation, take the two-flag rotation construction
with the suffix predicate identically one. Query the cosine/sine word
directly on address $`(\mathrm{sector},x)`$, using $`n+1`$ dirty
selectors and no suffix-control qubit. For a z rotation, conjugate this
entire circuit on its target by the fixed Clifford
$`K=HS^\dagger`$, which obeys $`KYK^\dagger=Z`$.
For the scalar factor $`e^{i\alpha_x}`$, use the literal diagonal
construction on the address, leaving the target untouched. Its S phase
on the sine branch retains the desired literal phase.

In all four factors take the same core size

```math
m=L+6,\qquad m+(n+1)=B_0=L+n+7.
```

The explicit error bound (24), before its final conservative rounding,
also holds for the diagonal factor: its complex scalar error is bounded
by the Euclidean norm of the sine and cosine errors. Thus every amplified
factor has complete initialized-isometry error at most

```math
\epsilon_{\mathrm{stage}}
=5\sqrt2\,2^{1-m}
=\frac{5\sqrt2}{32}\,2^{-L}.
```

The Clifford conjugations do not change this norm. If $`A_j`$ are the
four actual circuits and $`F_j`$ their ideal factors, unitary telescoping
on the common initialized embedding gives

```math
\|A_4A_3A_2A_1J_2-J_2(F_4F_3F_2F_1\otimes I_b)\|
\leq4\epsilon_{\mathrm{stage}}.
```

This identity propagates earlier flag leakage and core disturbance by
actual unitaries. It does not assume either clean flags or dirty inputs
have been reset between stages. Combining the factor errors with the
classical Euler approximation gives

```math
\|VJ_2-J_2(U\otimes I_b)\|
\leq\left(\frac1{16}+\frac{5\sqrt2}{8}\right)2^{-L}
<2^{-L}\leq\eta.
```

Each factor has $`2N`$ cosine/sine rows. The unbanked source and dirty
lookup therefore cost $`O(N+m)=O(N+L)`$ T gates and $`O(Nm)=O(NL)`$
Clifford gates. There are only four factors. When $`b\geq2B_0`$,
reserve $`B_0`$ base wires and optimize the additional word-bank count
as in (31)–(32). This gives
$`O(\sqrt{NL}+L+NL/b)`$ T gates per factor and the same Clifford
bound. All forward calls, actual inverses, and amplification are included
in these constant-factor costs.

For the lower bound, restrict to $`U_x=e^{i\phi_x}I_2`$. Fixing the
target input to zero gives an arbitrary $`n`$-qubit diagonal, so GKW's
diagonal theorem supplies $`\Omega(\sqrt{NL}+L)`$. The diagonal phase
grid packing and width-$`q`$ Clifford+T word count used in the preceding
diagonal corollary supply $`\Omega(NL/q)`$ when
$`q^2\leq cNL`$ for a sufficiently small absolute constant $`c`$.
Otherwise $`NL/q=O(\sqrt{NL})`$. Combining the bounds gives the
displayed worst-case lower bound.

The banked upper bound matches it for $`b\geq2B_0`$ because
$`q=\Theta(b)`$. The unbanked upper bound is also matching when
$`B_0\leq b<2B_0`$ and $`L\geq n`$: then
$`q=\Theta(L)`$, and $`NL/q=\Theta(N)`$. No matching assertion
for the remaining unbanked regimes is needed here. ∎

## 9. Verification and scope

The companion [operator-source tests](../tests/test_operator_source_compiler.py)
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
remains a hybrid-composition baseline. A separate nine-wire native
Clifford+T fixture now composes two approximate Hopf layers with exactly
two initialized flags, all logical/dirty input columns, actual gate-word
inverses, and no intermediate projection. The general U(2) fixture checks
literal block phases and four-factor composition at exact and coarse
precision. These checks support the signs and normalization;
the dimension-independent identities and resource proof above establish
the asymptotic statement.

The construction combines established Clifford-loader algebra, exact
dirty XOR lookup, a fixed native geometric specialization, and a
normalization-two block. Its programmed mask depends on the address and
implements one address-selected rotation.

The unrestricted $`O(N)`$ endpoint remains open. The established new
upper bound is $`O(N\log N)`$ at the explicit two-clean,
$`N+n+7`$-dirty allocation.

## 10. Classical table construction

The sign tables are ordinary classical data, generated once for a supplied
parameter tuple. At depth $`d`$ the construction uses
$`m_d=L+n-d+O(1)`$ bits per sine or cosine entry. Equations (12)–(13)
therefore need $`O(2^d)`$ certified trigonometric evaluations at precision
$`m_d+O(1)`$, followed by rational rounding. The total table length is

```math
\sum_{d=0}^{n-1}O(2^d m_d)=O(NL).
```

For an evaluator whose cost for an angle $`\theta`$ at $`P`$ bits is
$`E_\theta(P)`$, table construction takes the sum of these evaluation
costs plus $`O(NL)`$ bit operations for encoding and writing the tables.
The diagonal extension adds $`O(N)`$ evaluations at $`L+O(1)`$ bits.
This is a computational input contract: effective specifications alone
put no universal time bound on their evaluation routines.

An explicit elementary bound is available for **bounded dyadic inputs**.
Suppose every angle, including any leaf phase, is supplied as a dyadic
rational in $`[-8,8]`$ with at most $`B`$ bits. Then the real and complex
two-clean tables can be produced deterministically in

```math
O(NB+NL^4)
```

classical bit operations using schoolbook integer arithmetic. This is a
conservative preprocessing bound, separate from the quantum gate counts.
The input restriction already contains a full angle period; reducing
arbitrarily large angle descriptions modulo a transcendental period is
not included for free.

To see the bound, truncate an input toward zero to $`P+2`$ fractional bits
and evaluate the degree $`K=16(P+2)`$ Taylor polynomial of
$`e^{i\theta}`$, for $`P\geq6`$. The input perturbation has magnitude at
most $`2^{-(P+2)}`$. The absolute Taylor tail is at most
$`e^8 8^{K+1}/(K+1)!<2^{-(P+2)}`$, using
$`k!\geq(k/e)^k`$. If the truncated angle is $`q/2^b`$, compute the
polynomial exactly with common denominator $`2^{bK}K!`$. At step $`k`$,
the numerator obeys

```math
A_0=1,\qquad A_k=k2^b A_{k-1}+(iq)^k,
\qquad D_k=2^{bk}k!,
```

so $`A_k/D_k`$ is the degree-$`k`$ partial sum. The integers have
$`O(P^2)`$ bits; each of the $`O(P)`$ steps multiplies a long integer by
an $`O(P)`$-bit integer. Schoolbook arithmetic and a final rational
rounding thus cost $`O(P^4)`$ bit operations and provide certified
sine and cosine errors below $`2^{-P}`$ after a fixed guard margin.
Choose $`P=m_d+O(1)`$ in (12). Finally,

```math
\sum_{d=0}^{n-1}2^d(L+n-d+O(1))^4=O(NL^4)
```

by the convergent weighted fourth-moment geometric sum. Reading the
inputs costs $`O(NB)`$. Working storage can be bounded by
$`O(NL+(L+n)^2)`$ bits, including all output tables; individual entries
can be evaluated sequentially. This construction does not supply a
classical running-time bound for the separate sufficient-clean
compiler's coarse Clifford+T word-synthesis primitive.
