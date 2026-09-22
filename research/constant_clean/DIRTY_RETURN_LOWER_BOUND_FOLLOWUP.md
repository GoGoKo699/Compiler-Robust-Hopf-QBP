# Dirty return, symplectic rank, and whole-frame counting

This follow-up resumes the [constant-clean endpoint](../CONSTANT_CLEAN_ENDPOINT.md)
after repository integration. It proves a circuit compression lemma that
preserves the clean allocation and the complete approximation error. It
does **not** improve the unrestricted endpoint bounds
$`\Omega(N)`$ and $`O(N^{3/2})`$ at $`a=O(1)`$, $`b=\Theta(N)`$,
and $`L=N`$.

The useful new restriction is architectural. If the non-Clifford Pauli axes
use only $`O(\sqrt N)`$ noncommuting dirty pairs, then the worst-case
T-count remains $`\Omega(N^{3/2})`$. A compiler attaining $`O(N)`$
T-count for every frame would have to use $`\Omega(N)`$ such pairs on
hard instances. Commuting dirty components can be removed at no T-cost
increase, but removing all dirty workspace can require substantial overhead.

## 1. Model and dirty symplectic rank

Use the literal phase convention and complete initialized-isometry contract
from the [main theorem](../../docs/FAULT_TOLERANT_COMPILER.md). Let a native
Clifford+T circuit $`V`$ act on $`n\ge1`$ data qubits, $`a`$ clean
qubits, and $`b`$ arbitrary dirty qubits. Suppose

```math
\|VJ_a-J_a(W\otimes I_b)\|\le\eta<1/\sqrt2,
\tag{1}
```

where $`W`$ is any data unitary and $`J_a`$ appends the clean zero state.
In particular, the lemma covers the entire main-theorem error range.
No measurement, reset, supplied state, or oracle is allowed.

Moving the Clifford gates to the right gives an exact native-phase form

```math
V=R_{\epsilon_t}(P_t)\cdots R_{\epsilon_1}(P_1)C,
\qquad
R_\epsilon(P)=\frac{I+P}{2}+\zeta_8^\epsilon\frac{I-P}{2},
\qquad \zeta_8=e^{i\pi/4},\quad \epsilon\in\{1,-1\}.
\tag{2}
```

Here $`C`$ is Clifford, each $`P_j`$ is a signed Hermitian Pauli,
and $`t`$ is the original T/T-dagger count. The spectral-projector form
keeps all scalar phases explicit.

Ignore signs and restrict the axes to the dirty register. Write the resulting
binary Pauli labels as $`p_j\in\mathbb F_2^{2b}`$, and put

```math
S_D=\mathrm{span}\{p_1,\ldots,p_t\},\qquad
G_{jk}=\langle p_j,p_k\rangle_{\rm sp},\qquad
r_D=\tfrac12\mathrm{rank}G.
\tag{3}
```

The rank in (3) is also the rank of the symplectic form restricted to
$`S_D`$. Thus $`r_D\le\min\{b,\lfloor t/2\rfloor\}`$.
This quantity belongs to the chosen Pauli-rotation representation. The
lemma applies to every such representation; no minimization or efficient
optimization over representations is assumed. A dirty-only Clifford change
of coordinates preserves it.

## 2. Compression with the same clean allocation

**Lemma.** Under (1), there exists a native Clifford+T circuit
$`V_{\rm eff}`$ on $`n+a+r_D`$ qubits, with T-count at most $`t`$,
such that

```math
\|V_{\rm eff}J_a-J_a(W\otimes I_{r_D})\|\le\eta.
\tag{4}
```

The $`a`$ clean qubits retain their original initialization contract.
The $`r_D`$ surviving dirty qubits have arbitrary inputs, including
entanglement with external references. The conclusion is an existence and
Clifford-synthesis reduction; it does not assert preservation of the
original number of Clifford gates.

**Proof.** A symplectic basis change on the dirty register puts $`S_D`$
on three groups of wires:

- $`r_D`$ pairs with both X and Z directions;
- $`\ell=\dim S_D-2r_D`$ radical wires with only Z directions;
- $`b-r_D-\ell`$ inactive wires with no Pauli support.

Conjugate the full circuit by a dirty-only Clifford realizing this change.
The target in (1) is unchanged, since its dirty action is identity. In the
new coordinates write $`V=RC`$, with $`R`$ the product of rotations.
Every radical Z commutes with $`R`$, as do X and Z on every inactive wire.

For any one of these Hermitian Paulis $`Q`$, the ideal initialized
isometry commutes with $`Q`$. Consequently

```math
\|(CQ-QC)J_a\|
=\|(VQ-QV)J_a\|\le2\eta.
\tag{5}
```

Since $`C`$ is Clifford, $`P=C^\dagger QC`$ is a Hermitian Pauli.
The following discrete gap is the reason approximate return suffices:

```math
\|(P-Q)J_a\|\in\{0,\sqrt2,2\}.
\tag{6}
```

Indeed,

```math
J_a^\dagger(P-Q)^2J_a
=2I-J_a^\dagger(PQ+QP)J_a.
```

If $`P`$ and $`Q`$ anticommute, this is $`2I`$. Otherwise their
product is a signed Hermitian Pauli. Compressing that product to the
clean-zero code gives zero, a signed identity, or a signed nonidentity
Pauli on the arbitrary input wires. The largest eigenvalue of the displayed
positive operator is therefore zero, two, or four. Combining (5), (6),
and $`2\eta<\sqrt2`$ proves the exact intertwining relation

```math
CQJ_a=QCJ_a.
\tag{7}
```

Intertwining both X and Z on every inactive wire makes $`CJ_a`$ factor
as the identity on that entire register: the single-qubit Paulis generate
its full matrix algebra. Intertwining the radical Z operators makes the
remaining isometry block diagonal in every radical computational label.
Fix the radical labels to zero and remove the inactive identity factors.
This leaves an isometry from $`n+r_D`$ input qubits to $`n+a+r_D`$
output qubits. It is a Clifford isometry with exactly $`a`$ initialized
clean qubits available.

Here is an explicit reason that the last isometry has a Clifford extension
without adding work. Initialize the removed wires in zero before applying
$`C`$. Equation (7) ensures their outputs are exactly zero, so this
restriction involves no probabilistic projection or normalization factor.
The remaining output code has $`a`$ independent commuting Pauli
stabilizers. The $`2(n+r_D)`$ logical X and Z images inherited from
$`C`$ commute with those stabilizers and have the standard symplectic
pairings. Extend these labels and the $`a`$ stabilizers to a full
symplectic basis, including one dual label per stabilizer. The resulting
Clifford $`C_{\rm eff}`$ acts as the required isometry on clean-zero
inputs, up to a constant scalar. The scalar is an eighth root of unity:
both maps are normalized native Clifford isometries obtained by deterministic
stabilizer restrictions. It can be calibrated exactly with Clifford gates,
using $`(HS)^3=\zeta_8 I`$ on any retained wire. The assumption
$`n\ge1`$ guarantees such a wire exists.

Now restrict every rotation in (2) to radical label zero and drop its
inactive identities. Each remaining signed nonidentity Pauli rotation uses
one T or T-dagger gate, conjugated by Cliffords. A restricted axis $`I`$
gives identity; an axis $`-I`$ gives the Clifford scalar
$`\zeta_8^\epsilon I`$ and needs no T gate. Their product with
$`C_{\rm eff}`$ is $`V_{\rm eff}`$.

The reduced circuit agrees exactly with the original circuit on the chosen
removed-dirty input sector. Restricting (1) to this sector cannot increase
the operator norm, giving (4). Tensoring with any reference preserves this
norm bound. This proves the lemma.

**Commuting special case.** If all dirty restrictions of the axes commute,
then $`r_D=0`$ and all dirty qubits can be removed without increasing
T-count, clean count, or approximation error. The conclusion does not
declare the surviving noncommuting pairs removable.

## 3. A lower bound for families with bounded dirty rank

Suppose every prescribed real Hopf frame on $`n`$ qubits admits a circuit
with clean budget $`a`$, T-count at most $`T`$, and a representation
(2) satisfying $`r_D\le R`$. The physical dirty budget may be larger
than $`R`$ and may depend on the frame. Apply the lemma to each circuit
and pad its surviving dirty register to $`R`$ wires. All resulting
circuits have common width

```math
q'=n+a+R.
```

The finite word count and real first-column packing in
[Section 10.2 of the main theorem](../../docs/FAULT_TOLERANT_COMPILER.md#102-fixed-width-coherent-counting)
therefore give the necessary inequality

```math
(N-1)(\log_2(1/\eta)-2)
\le 2q'^2+3q'+5+(2q'+1)T.
\tag{8}
```

The representation used for compression need not be unique, and many
original circuits may compress to the same word. That only makes the
counting upper bound more generous. Crucially, (8) concerns a family that
can approximate **every** frame under common resource bounds; it is not a
lower bound on each individual easy frame.

At $`a=O(1)`$ and $`L=N`$, the left side of (8) is $`\Theta(N^2)`$.
Keeping the width-square term explicit yields

```math
T(n+a+R)+O((n+a+R)^2)\ge cN^2
\tag{9}
```

for an absolute positive constant $`c`$. This has two concrete consequences.

1. **Linear T-count needs linear dirty rank on hard instances.** For each
   fixed $`C`$, there is $`c_C>0`$ such that, for sufficiently large
   $`N`$, some frames admit no circuit satisfying both $`T\le CN`$
   and $`r_D\le c_CN`$. To see this, take $`R=c_CN`$ in (8) and
   choose $`c_C`$ small enough that both $`2R^2`$ and $`2CNR`$
   consume less than the packing exponent. In particular, if a compiler
   achieves $`O(N)`$ T-count for every frame, its required dirty rank is
   $`\Omega(N)`$ in the worst case. Equivalently, a putative uniform
   bound $`R=o(N)`$ would make $`Tq'+q'^2=o(N^2)`$ and contradict (8).

2. **Square-root dirty rank has the retained upper-bound order.** If
   $`R=O(\sqrt N)`$, then $`q'^2=O(N)`$ cannot swallow the
   $`\Theta(N^2)`$ packing term. Equation (8) gives worst-case
   $`T=\Omega(N^{3/2})`$. The
   [borrowed-workspace compiler](BORROWED_WORKSPACE_COMPILER.md) can use
   $`O(\sqrt N)`$ active dirty wires at this endpoint and reaches
   $`O(N^{3/2})`$ T-count. Its dirty rank is automatically at most
   that active width. Thus that order is optimal within families whose
   dirty rank stays $`O(\sqrt N)`$.

The universal estimate $`r_D\le t/2`$ alone does not strengthen the
unrestricted endpoint. Substituting it in the word count leaves a
$`2^{O((n+a+t)^2)}`$ description bound and the familiar square-root
packing lower bound. With $`b=\Theta(N)`$, the model permits the
linear dirty rank required by the first consequence.

## 4. Exact dirty return still permits quadratic description entropy

There is a simple obstruction to a substantially smaller count based only
on dirty identity return. Let $`f:\{0,1\}^{m}\to\{0,1\}`$ be an
arbitrary Boolean table with $`M=2^m`$ rows. The exact dirty loader and
router in [the borrowed-workspace proof, Section 2](BORROWED_WORKSPACE_COMPILER.md#2-exact-dirty-table-and-reflection-interpreter)
implement

```math
Q_f|x,z,\mathrm{work}\rangle
=|x,z\oplus f(x),\mathrm{work}\rangle
```

using no initialized clean qubits, $`O(\sqrt M)`$ arbitrary dirty
banks/selectors, $`O(\sqrt M)`$ T gates, and $`O(M)`$ Clifford gates.
Choose a power-of-two bank width within a constant factor of $`\sqrt M`$.
Two routed CNOTs, separated by loading and unloading, cancel the unknown
bank bit and leave only the table bit. Every work wire returns exactly.

The phase echo

```math
Z_zQ_fZ_zQ_f=D_f\otimes I_z\otimes I_{\rm work},
\qquad D_f|x\rangle=(-1)^{f(x)}|x\rangle
\tag{10}
```

is exact on arbitrary inputs. Let $`n=m+1`$ and use $`z`$ as the last
logical qubit. Set all earlier Hopf layers to identity and choose final-layer
angles $`\theta_x=\pi f(x)`$. Under the declared rotation convention,
$`R_y(\pi f(x))=(-1)^{f(x)}I_2`$, so

```math
W_f=D_f\otimes I_2
\tag{11}
```

is exactly the prescribed real frame, including its other columns.

There are $`2^M`$ such frames and any two distinct ones have literal
operator distance two. Restricting to $`f(0)=0`$ still gives
$`2^{M-1}`$ frames with constant separation even after minimizing over
global phase. Thus circuits with zero clean qubits, exact dirty identity
return, and T budget $`T_M=O(\sqrt M)`$ can realize at least
$`2^{\Omega(T_M^2)}`$ distinguishable logical frames along this sequence
of dimensions and budgets.

In particular, dirty identity return alone cannot reduce the universal
logical-circuit count to $`2^{O(nT+n^2)}`$. This example does not show
that $`2^{\Omega(N^2)}`$ generic high-precision frames are realizable
with $`O(N)`$ T gates. It only rules out the stated universal counting
shortcut. Boolean phase synthesis and dirty-bank tradeoffs have prior
literature; the point here is their implication for this exact frame and
workspace contract.

## 5. Removing all dirty wires can require a large T overhead

Fix a constant clean budget $`a_0`$ and a constant error
$`\eta_0<1`$, and set $`q_0=n+a_0`$. The frames (11) are pairwise
distance two. A width-$`q_0`$ circuit can approximate at most one of them
to error $`\eta_0`$. The same finite word count implies that some
$`W_f`$ requires, when no dirty wires are allowed,

```math
T_{\rm narrow}\ge
\frac{M-2q_0^2-3q_0-5}{2q_0+1}
=\Omega(N/n).
\tag{12}
```

Every one of these frames has the exact wide implementation of (10) with
$`O(\sqrt N)`$ T gates and zero clean qubits. Therefore a universal
transformation removing all dirty wires while preserving a constant clean
budget and even constant accuracy must have worst-case multiplicative
T overhead at least $`\Omega(\sqrt N/n)`$. This refutes cost-preserving
removal of arbitrary dirty work, while remaining consistent with the
rank-sensitive removal in Section 2.

## 6. Why counting all frame columns gives no extra parameter factor

A complete Hopf frame has $`N-1`$ angle parameters. Disjoint rotations
within each layer and telescoping between the $`n`$ layers imply

```math
\|W(\theta)-W(\theta')\|
\le\sum_{d=0}^{n-1}\max_p|\theta_{d,p}-\theta'_{d,p}|
\le n\|\theta-\theta'\|_\infty,
\tag{13}
```

using circular angle distances. Since the angles are periodic, a product
grid gives an operator-norm covering with at most

```math
(1+C n/\eta)^{N-1}
```

points, for an absolute constant $`C`$. The lower packing already retained
in the main theorem has logarithmic size $`\Omega(N\log(1/\eta))`$.
At $`L=N`$, both bounds have order $`N^2`$. The other frame columns
are constrained functions of the same angles and do not add independent
continuous parameters. Nor does identity on the dirty register enlarge
their operator distance:

```math
\|(W-W')\otimes I_b\|=\|W-W'\|.
```

A stronger unrestricted lower bound would therefore need a sharper
restriction on attainable circuits, or a different obstruction. Merely
counting all logical or dirty input columns does not multiply the target
packing entropy.

## 7. Scope, prior work, and the next proof obligation

The [source-channel theorem](SOURCE_CHANNEL_PROOF.md) applies to an
explicit returned-source attenuation interface. It does not bound
$`r_D`$ for an arbitrary whole-frame circuit. Its processing costs cannot
be added over independently imagined stages to upgrade (8). In particular,
constant initialized clean width does not imply small dirty symplectic rank.

The present compression proof uses standard Pauli-rotation normal forms,
binary symplectic reduction, and Clifford-code extension. Relevant primary
comparisons are:

- Low, Kliuchnikov, and Schaeffer,
  [*Trading T gates for dirty qubits in state preparation and unitary synthesis*](https://arxiv.org/html/1812.00954v2),
  especially the dirty table lookup and fixed-width counting in Sections 2
  and 5. The zero-clean selector cancellation used in Section 4 above is
  supplied by the local borrowed-workspace proof.
- Gosset, Kothari, and Wu,
  [*Quantum State Preparation with Optimal T-Count*](https://arxiv.org/html/2411.04790v3),
  Section 4 and Appendix A. Their ancillary-qubit-independent canonical
  forms yield quadratic T-count description exponents, with magic-state
  and Pauli-postselection representations. They do not state the
  same-clean, arbitrary-dirty-rank reduction (4).
- Aaronson and Gottesman,
  [*Improved Simulation of Stabilizer Circuits*](https://arxiv.org/abs/quant-ph/0406196),
  for the standard stabilizer and Clifford synthesis framework.
- [*Optimal T-Count for Block Encodings of Fermionic and Spin Hamiltonians*](https://arxiv.org/html/2609.11153v1),
  Theorem 3.1 and its appendices. Its compression also separates Pauli
  rotations from a projected Clifford block, but concerns initialized
  block-encoding ancillas and can change the normalization. That theorem
  does not directly supply complete arbitrary-dirty return with unchanged
  clean allocation and error as in (4).

This comparison establishes the relevant proof lineage, not a priority
claim for the lemma. The new usable conclusion in this repository is (8)
and its dirty-rank consequences under the exact declared model.

For the lower-bound route, the remaining concrete obligation is to bound
the number of high-precision real frames attainable with $`a=O(1)`$,
$`T=O(N)`$, and $`r_D=\Theta(N)`$ more sharply than the generic
$`2^{O(N^2)}`$ word count, or to find another invariant excluding such
circuits. For the construction route, an improvement on the retained
$`O(N^{3/2})`$ order must use asymptotically more than
$`O(\sqrt N)`$ dirty symplectic pairs on some hard frames; merely
allocating more untouched dirty wires cannot help. Reaching $`O(N)`$
would require linear dirty rank in the worst case together with a fully
charged, coherent whole-frame implementation.
