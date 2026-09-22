# A compiler from an operator source on dirty qubits

Three initialized qubits and a precision-sized bank of arbitrary dirty
qubits suffice for the following full-frame upper bound. The construction
uses a linear combination of anticommuting Pauli operators to encode
precision coefficients. No precision register is initialized to a
geometric state.

**Theorem.** Let $`N=2^n`$, $`n\geq1`$, $`0<\eta\leq1/64`$,
$`L=\max\{6,\lceil\log_2(1/\eta)\rceil\}`$, and let $`W`$ be the
prescribed complete real Hopf frame, with the rotation convention
$`R_y(\theta)=e^{-i\theta Y}`$. If

```math
a\geq3,\qquad b\geq L+n+6,
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
dirty-work return. All inverses are actual circuit inverses; there are
no measurements, resets, supplied catalysts, or uncharged quantum oracles.
Angles must be effectively specified so that certified sine and cosine
approximations can be computed. That classical evaluation and table
construction are separate preprocessing costs, excluded from T and G;
the resulting quantum lookup circuits are fully charged below.

At $`L=N`$, choosing $`a=3`$ and $`b=N+n+6`$ gives

```math
T=O(N\log N)=o(N^{3/2}),\qquad G=O(N^2).
\tag{3}
```

This improves the previously retained upper bound at that explicit
workspace allocation. It does not establish $`O(N)`$ T count, nor does
it claim the same result for every constant prefactor in $`b=\Theta(N)`$
or for fewer than three initialized qubits.

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

## 4. Two flags encode an addressed rotation with normalization two

At Hopf depth d, let $`x`$ be the d-bit prefix and t the rotation
target. Compute the predicate h that the lower suffix is all zero
into a third initialized qubit. A borrowed-MCX construction uses
$`O(n^2)`$ Toffolis and may borrow t in its arbitrary state. For an
empty suffix, flip h to one.

The following block treats h as an unchanged address bit. Flag b chooses
between the cosine and sine tables:

```math
g_0(x,h)=
\begin{cases}\cos\theta_x,&h=1,\\1,&h=0,\end{cases}
\qquad
g_1(x,h)=
\begin{cases}\sin\theta_x,&h=1,\\0,&h=0.\end{cases}
\tag{19}
```

Use (12)–(13) to encode each entry by $`f(b,h,x)`$. The table has
$`2^{d+2}=4S`$ rows, where $`S=2^d`$, and uses $`d+2`$ dirty
selectors. Let $`c_{x,h}`$ and $`s_{x,h}`$ be its encoded coefficients.

The literal target operation $`XZ=-iY`$ is Clifford. Its controlled
version is the product of a CNOT and a controlled Z, with the order
chosen to give XZ on the b=1 branch. Define

```math
Q=H_b\,C_b(XZ_t)\,\mathcal S_{f(b,h,x)}\,H_b.
\tag{20}
```

Both the scalar block circuit and the controlled target operation
preserve b, h, and x. They act coherently when b is in superposition.
With $`J`$ initializing only the flags a and b, the accepted block is

```math
B=J^\dagger QJ
=\frac12\left(c_{x,h}I_t-i s_{x,h}Y_t\right)
 \otimes I_{\rm core,selectors}.
\tag{21}
```

For the unitary $`D_d`$ that applies $`R_y(\theta_x)`$ when h=1
and identity when h=0,

```math
\|2B-D_d\|\leq\frac{5\sqrt2}{4}\,2^{1-m}.
\tag{22}
```

The same bound holds across the coherent address direct sum. Inactive
rows are exact: $`c_{x,0}=1`$ and $`s_{x,0}=0`$.
The possibly imperfect length $`c_{x,h}^2+s_{x,h}^2`$ is not
silently normalized.

## 5. Amplification includes rejected-space error

Apply the robust normalization-two lemma from
[the fault-tolerant compiler chapter](../../docs/FAULT_TOLERANT_COMPILER.md).
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

The predicate h and the suffix are unchanged throughout Q and (23).
Compute h once before amplification and uncompute it afterward.
The borrowed MCX may again use t even if it is entangled after the
amplified word: its full-unitary identity returns the borrowed wire.
The predicate is erased exactly because its suffix controls were
unchanged. The full stage therefore has three initialized qubits and

```math
\|\widetilde L_dJ_3-J_3(L_d\otimes I_b)\|
\leq5\sqrt2\,2^{1-m}\leq2^{4-m}.
\tag{24}
```

Here $`L_d`$ is the prescribed Hopf layer on the original logical
register, obtained by substituting the suffix predicate for h in
$`D_d`$, and $`\widetilde L_d`$ includes its predicate computation
and erasure. The uniform bound for $`D_d`$ remains valid on that
correlated subspace. Equation (24) includes all core, selector, and flag
inputs in their stated roles.

On an inactive suffix, (21) has $`B=I/2`$ exactly. Applying the lemma
with $`\zeta=0`$ shows that the actual amplified stage is exactly
identity on the initialized-flag columns, including dirty-work return.
The pre-amplification word Q may have a rejected component.
There is no source-state preparation or fresh initialization between calls.

## 6. Precision, workspace, and full-frame composition

At depth $`d=0,\ldots,n-1`$, choose

```math
m_d=L+n-d+4.
\tag{25}
```

The source uses $`m_d`$ dirty qubits and the lookup uses $`d+2`$
additional dirty selectors. Their sum is exactly

```math
m_d+(d+2)=L+n+6.
\tag{26}
```

The same arbitrary dirty pool is repartitioned between these two roles
at each depth. No source-private helper or initialized lookup output
is missing from (26). The three clean qubits are exactly a, b, and h.

Each source call uses $`2(m_d-1)`$ T gates. Each Q uses three such
calls, of which two are controlled using (9), and two whole-word
dirty-mask queries. Amplification multiplies these costs by three.
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
\|VJ_3-J_3(W\otimes I_b)\|
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

## 7. Verification and scope

The companion [operator-source tests](../../tests/test_operator_source_compiler.py)
check small complete matrices for the anticommuting source, its native
gate word and actual adjoint, all sign masks, dyadic endpoints, and the
dirty-selector phase query. They also check the two-flag rotation block,
amplification on all initialized columns, dirty/reference return, and
negative controls. A two-layer full-frame fixture also checks suffix erasure,
exact inactive action, and reuse after intermediate flag leakage. These checks
support the signs and normalization;
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
upper bound is $`O(N\log N)`$ at the explicit three-clean,
$`N+n+6`$-dirty allocation.
