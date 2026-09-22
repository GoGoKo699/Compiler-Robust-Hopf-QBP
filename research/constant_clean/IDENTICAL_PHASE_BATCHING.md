# Phase batching with one clean overflow bit

This note gives deterministic constant-clean compilers for identical phases
and for heterogeneous phases with bounded integer coefficients in a shared
set of base angles. It also supplies a small-palette special case of the
[dirty tensor-phase-bank reduction](GLOBAL_BLOCK_FOLLOWUP.md#5-a-constructive-reduction-to-heterogeneous-phase-batching).
The construction does not require a prepared phase catalyst or an initialized
Hamming-weight register. It does not resolve arbitrary heterogeneous batching.

## 1. Complete-input theorem

Let $`m\geq1`$, $`L\geq1`$, $`\varepsilon=2^{-L}`$, and let the angle
$`\theta`$ be classically specified to sufficient precision. Write

```math
P(\theta)=\mathrm{diag}(1,e^{i\theta}),\qquad
t=\lceil\log_2(m+1)\rceil,\qquad r=t+1.
```

There is a deterministic Clifford+T circuit $`V`$ with **one clean qubit**
and $`t+1`$ arbitrary dirty qubits such that

```math
\left\|VJ-J\bigl(P(\theta)^{\otimes m}\otimes I_{\rm dirty}\bigr)\right\|
\leq\varepsilon,
\qquad
T(V),G(V)=O\bigl((m+L)\log(m+1)\bigr).
\tag{1}
```

Here $`J`$ initializes the one clean qubit to zero, $`G`$ counts Clifford
gates, and the norm includes the **entire output**. The data and every dirty
qubit may be jointly entangled with an untouched reference. Tensoring (1)
with its identity preserves the bound. There are no measurements, resets,
postselections, or free resource states. Return of the accumulator and clean
qubit is approximate in this complete-output sense; return of the separate
arithmetic helper is exact.

The sharp arithmetic bound uses the exact borrowed-bit controlled increment
in [Gidney, §2.10, Fig. 20](https://arxiv.org/html/1706.07884v2#S2.SS10).
Section 3 also gives an independently emitted and checked, slightly slower
implementation using $`2t-1`$ dirty qubits and

```math
T(V),G(V)=O\bigl(m\log^2(m+1)+L\log(m+1)\bigr).
\tag{2}
```

## 2. Masked accumulation and its phase word

Set $`Q=2^t>m`$. The accumulator consists of $`t`$ arbitrary low bits
$`y\in[0,Q)`$ and the clean top bit. Its integer value $`w`$ is taken
modulo $`2Q`$. Define an exact reversible circuit

```math
A|x,w,z\rangle
  =|x,w+h(x)\bmod 2Q,z\rangle,
\qquad h(x)=\sum_{j=1}^m x_j,
\tag{3}
```

where $`z`$ denotes the borrowed arithmetic helper(s). Equation (3) must
hold for **every** $`w,z`$, including top-bit-one inputs. Apply one
controlled increment per input bit to obtain this circuit.

Define a diagonal operator on the whole accumulator,

```math
D_\theta|w\rangle=e^{i\theta w}|w\rangle,
\qquad
D_\theta=\bigotimes_{k=0}^{r-1}P(2^k\theta).
\tag{4}
```

Products act rightmost first. The ideal word is

```math
V_0=A^\dagger D_\theta A D_\theta^\dagger.
\tag{5}
```

On the initialized top-bit-zero subspace, $`w=y`$ and
$`y+h(x)\leq Q-1+m<2Q`$. Thus addition does not wrap, and (5) gives

```math
|x,y,0,z\rangle
\longmapsto
e^{i\theta((y+h(x))-y)}|x,y,0,z\rangle
=e^{i\theta h(x)}|x,y,0,z\rangle.
\tag{6}
```

This literal basis identity proves exact return in the ideal circuit,
including arbitrary dirty/reference coherence. The clean top bit is a
range guarantee: the count remains masked as $`y+h(x)`$ and is never
extracted into a register containing $`h(x)`$ independently of the dirty
input. Consequently a lower bound for producing an unmasked population
count does not apply to (3). Omitting the clean bit generally introduces
an unwanted wrap phase $`e^{-i\theta Q}`$.

### Native phase synthesis and the actual inverse

Choose an ancilla-free Clifford+T word $`C`$ and a scalar $`e^{i\alpha}`$
with

```math
\|C-e^{i\alpha}D_\theta\|\leq\delta,
\qquad \delta=\varepsilon/2.
```

For example, synthesize each factor in (4), up to its own scalar, to
error $`\delta/r`$. Ancilla-free single-qubit synthesis gives
$`O(\log(r/\delta))`$ T and Clifford gates per factor; see
[Ross–Selinger](https://arxiv.org/abs/1403.2975). This uses no additional
quantum workspace. Classical angle accuracy is charged in preprocessing:
sufficiently accurate values of $`2^k\theta`$ require, conservatively,
$`L+O(\log(m+1)+\log r)`$ bits of $`\theta`$.

The native implementation uses the **literal reversed and adjointed gate
word**, not a separately synthesized negative angle:

```math
V=A^\dagger C A C^\dagger,
\qquad
\|V-V_0\|\leq2\delta=\varepsilon.
\tag{7}
```

The common scalar cancels. The two-term unitary telescoping bound in (7)
holds on the full workspace even when $`C`$ is nondiagonal and
$`C^\dagger`$ temporarily leaks outside the initialized subspace. It
therefore bounds all final accumulator/top-bit leakage. The arithmetic
helpers are untouched by $`C`$ and are returned by $`A`$ on all inputs,
so their return remains exact. This full-input contract also permits
reusing the same clean qubit in a sequence of batches: the usual isometry
hybrid adds their errors without resets.

## 3. Native arithmetic ledger

The cited Gidney circuit implements a controlled increment on $`r`$ bits
with $`O(r)`$ Clifford/Toffoli gates and one arbitrary dirty helper. Its
even-width extension separates the low bit; no initialized intermediate
register is needed. Use Fig. 20, not the separate phase-gradient circuit
of Fig. 21. Applying it $`m`$ times, and reversing the actual word,
costs $`O(mr)`$. Exact seven-T Toffoli decomposition and the two phase
words give

```math
T(V),G(V)=O\bigl(mr+r(L+\log r)\bigr)
        =O\bigl((m+L)\log(m+1)\bigr).
\tag{8}
```

The dirty ledger is $`t`$ low accumulator bits plus one increment helper.
Both remain arbitrary; the one clean top bit is counted separately.

For an explicit alternative requiring no imported arithmetic emitter,
increment from the highest target bit to the lowest. Target bit $`w_k`$
is toggled controlled on $`x_j,w_0,\ldots,w_{k-1}`$. This order tests
the original lower bits. A NOT with $`c\geq3`$ controls uses $`c-2`$
arbitrary borrowed bits and $`4c-8`$ Toffolis, as follows.

Let $`F`$ be the first Toffoli of a borrowed conjunction ladder, $`G`$
the remaining ladder, and $`B`$ its final Toffoli into the target. The
**chronological** word

```math
F,\ G,\ B,\ G^\dagger,\ F,\ G,\ B,\ G^\dagger
\tag{9}
```

cancels the dirty contribution while retaining the product of all controls;
each borrowed bit returns exactly. For three controls the middle ladder
$`G`$ is empty. One and two controls use a CNOT and Toffoli respectively.
The $`r`$-bit controlled increment therefore uses

```math
c_r=1+\sum_{k=2}^{r-1}(4k-4)
   =2(r-2)(r-1)+1
\tag{10}
```

Toffolis, one CNOT, and at most $`r-2`$ dirty helpers. The complete
arithmetic pair costs **exactly** $`2mc_r`$ Toffolis, hence
$`14mc_r`$ T gates with the checked literal seven-T decomposition.
Including the $`t`$ low accumulator bits gives $`2t-1`$ dirty qubits.
The phase-word cost is unchanged, proving (2).

## 4. Distinct angles from shared generators

### One signed generator

Let the desired phases be $`P(k_j\phi)`$ on $`S`$ arbitrary input bits,
where the integers $`k_j`$ may have either sign. Define

```math
h(x)=\sum_j k_jx_j,\qquad
H_- =\sum_j\max\{-k_j,0\},\qquad H=\sum_j|k_j|,
\qquad q=\#\{j:k_j\ne0\}.
```

If $`H=0`$, the operation is identity. Otherwise set
$`t=\lceil\log_2(H+1)\rceil`$, $`Q=2^t>H`$, and $`r=t+1`$.
Use $`t`$ arbitrary low accumulator bits, one clean top bit, and two
separately reserved dirty arithmetic helpers. On the full accumulator,
let $`R`$ add the constant $`H_-`$, let $`A`$ add $`h(x)`$, both modulo
$`2Q`$, and let $`D_\phi|w\rangle=e^{i\phi w}|w\rangle`$. Then

```math
V_0=R^\dagger A^\dagger D_\phi A D_\phi^\dagger R
\quad\Longrightarrow\quad
V_0|x,y,0,z\rangle
=e^{i\phi h(x)}|x,y,0,z\rangle,
\qquad 0\le y<Q.
\tag{11}
```

Indeed, $`-H_-\le h(x)\le H-H_-`$, so both accumulator values
$`y+H_-`$ and $`y+H_-+h(x)`$ lie between zero and $`Q-1+H<2Q`$.
The phase difference is exactly $`\phi h(x)`$. Centering by $`R`$
therefore handles signed coefficients with only one initialized bit.
No input-independent phase is discarded. The proof includes all dirty
inputs and their references. A negative offset uses the actual inverse
of its positive-offset circuit.

The coherent constant-offset construction in
[Gidney, §2.9, Figs. 16 and 18](https://arxiv.org/html/1706.07884v2#S2.SS9)
costs $`O(r\log r)`$ gates with one dirty helper when uncontrolled,
or two dirty helpers when controlled by one input bit. Compile $`A`$
as $`q`$ such controlled offsets, and charge $`R,R^\dagger`$ as well.
These are complete-input reversible circuits; they use neither
measurements nor initialized carry words. With a phase approximation
$`\|C-e^{i\alpha}D_\phi\|\le\varepsilon/2`$, use
$`R^\dagger A^\dagger C A C^\dagger R`$. The same full-unitary
hybrid as (7) bounds the error by $`\varepsilon`$. The resulting ledger is

```math
T,G=O\bigl((q+1)r\log r+r(L+\log r)\bigr),\qquad
\text{clean}=1,\qquad \text{dirty}=r+1.
\tag{12}
```

The dirty count is $`r-1`$ low accumulator bits plus two arithmetic
helpers. Their work is reused between the centered additions and the
offsets. Accumulator return is within the full-output error; the separate
helpers return exactly. For coefficients of magnitude one, the sharper
increment/decrement construction in Section 3 removes the arithmetic
$`\log r`$ factor.

### Several generators and inexpensive parity controls

Suppose, modulo $`2\pi`$, that
$`\theta_j=\sum_{a=1}^d k_{aj}\phi_a`$. Omit generators whose coefficients
are all zero; if none remain, the operation is identity.
As a classical simplification, divide a generator's integer coefficients
by their common divisor and multiply its base angle by that divisor before
computing its width. This avoids paying for redundant coefficient scaling.
For each remaining generator define $`q_a,H_a,r_a`$ as above. Apply
its signed-generator circuit with error $`\varepsilon/d`$, reusing the
same clean bit and dirty workspace. The complete-isometry hybrid gives
the tensor phase bank with total error at most $`\varepsilon`$ and

```math
T,G=O\!\left(\sum_{a=1}^d
 \left[(q_a+1)r_a\log r_a
 +r_a(L+\log d+\log r_a)\right]\right),
\quad \text{clean}=1,\quad
\text{dirty}=1+\max_a r_a.
\tag{13}
```

The actual inverses remain part of every call. Reuse does not assume that
the actual intermediate accumulator has returned perfectly. Classical
base-angle errors $`\Delta\phi_a`$ contribute at most
$`\sum_a H_a|\Delta\phi_a|`$ to the phase-bank operator error. Likewise,
an approximate angle representation with residuals $`e_j`$ contributes
at most $`\sum_j|e_j|`$; either error must receive its own share of the
budget in addition to native synthesis.

The same argument applies to a specified parity-phase polynomial by
replacing each $`x_j`$ with a parity of input bits. Compute that parity
into one participating input wire using CNOTs, apply the controlled
offset, and reverse the CNOTs. This requires no initialized parity bit
and leaves the T bound unchanged, while adding the sum of the parity
support sizes to the Clifford ledger, up to constant factors. This
extension does not itself find a smaller generator representation for
an arbitrary tensor phase bank.

### A family with all distinct angles

For $`\theta_j=j\phi`$, $`0\le j<S`$, one has
$`H=S(S-1)/2`$ and $`r=O(\log(S+1))`$. The phases can all be distinct,
and (12) gives

```math
T,G=O\bigl(S\log(S+1)\log\log(S+2)+L\log(S+1)\bigr).
\tag{14}
```

More generally, a constant number of generators with polynomially bounded
integer coefficients has the same order. This includes fixed-degree
integer polynomial multiples $`\theta_j=p(j)\phi`$. In the addressed
frame reduction, if each depth table has such a representation with a
uniform constant number of generators and coefficients bounded by a
fixed power of $`N`$, the sum over depths is
$`O(Nn\log(n+1)+(L+n)n^2)`$. At $`L=N`$ this is
$`O(N\log^2 N)`$ with two clean qubits and $`N/2+O(n)`$ dirty qubits.
This is a sufficient bound for the stated structured family, without an
optimality or best-known-bound claim.

Arbitrary $`L`$-bit angles can be put on a common dyadic grid, but their
integer coefficients may require $`\Theta(L)`$ bits. The worst-case
accumulator width is then $`\Theta(L+\log S)`$, and (12) no longer gives the structured
bound (14). Classical preprocessing and Clifford changes of basis are
not a justification for treating those large coefficients as small.

Applying the same construction recursively to an $`r`$-bit phase gradient
uses weights $`2^k`$, whose sum is $`2^r-1`$, and therefore requires a
new accumulator of width $`r+1`$: the recursion does not shrink. For the
primitive $`2^r`$-th-root clock, the extra top phase is identity, but the
remaining factors are exactly the original clock that still needs synthesis.

### A limit on compressing arbitrary angle tables

Normalize angles by $`2\pi`$ and use circular $`\ell_\infty`$ distance
on $`\mathbb T^S`$, where $`\mathbb T=\mathbb R/\mathbb Z`$.
For integers $`d,B\ge1`$, let $`E_{S,d,B}(\epsilon)`$ contain all tables
within distance $`\epsilon`$ of $`K\varphi\pmod1`$, allowing every
$`K\in\mathbb Z^{S\times d}`$ with $`|K_{ja}|\le B`$ and every
$`\varphi\in\mathbb T^d`$. Thus the integer labels and the real base
angles may both depend on the table. For $`0<\epsilon\le1/8`$, normalized
Haar measure obeys

```math
\mu(E_{S,d,B}(\epsilon))
\le\min\!\left\{1,
(4\epsilon)^S(2B+1)^{Sd}
\left(\frac{2dB}{\epsilon}\right)^d\right\}.
```

There are at most $`(2B+1)^{Sd}`$ coefficient matrices. For each matrix,
a base-angle grid with spacing at most $`\epsilon/(dB)`$ has at most
$`(2dB/\epsilon)^d`$ points and its image is an $`\epsilon`$-net.
The $`\epsilon`$-neighborhood of the image is therefore covered by that
many circular cubes of radius $`2\epsilon`$, each of measure
$`(4\epsilon)^S`$. Multiplying proves the bound; only the $`d`$ base
angles are continuous parameters.

With $`\epsilon=2^{-\ell}`$, covering a fraction $`\alpha>0`$ of all
tables consequently requires

```math
S\ell\le Sd\log_2(2B+1)
+d\bigl(\ell+1+\log_2(dB)\bigr)
+2S+\log_2(1/\alpha).
```

At $`\ell=S`$, polynomially bounded $`B`$ and fixed positive
$`\alpha`$ force $`d=\Omega(S/\log S)`$. In particular, a constant
number of bases with polynomial integer labels cannot approximate a
positive fraction of arbitrary high-precision tables. This is an angle
representation bound, not a T-count lower bound. Coordinate angle error
$`\epsilon`$ suffices for phase-bank error $`2\pi S\epsilon`$; using
$`\ell=L+\log_2 S+O(1)`$ for a bank error $`2^{-L}`$ leaves the stated
conclusion unchanged when $`L=S`$.

## 5. A small-palette phase bank and frame corollary

Suppose $`S`$ arbitrary bank inputs have phases drawn from at most
$`p\leq S`$ classically specified angles. Group equal angles, apply
(1) to each group with error $`2^{-\ell}/p`$, and reuse the workspace.
If the group sizes are $`m_1,\ldots,m_p`$, then

```math
T_B,G_B
=O\!\left(\sum_{a=1}^p
 (m_a+\ell+\log p)\log(m_a+1)\right)
\leq O\bigl((S+p(\ell+\log p))\log(S+1)\bigr).
\tag{15}
```

This needs one clean qubit and $`O(\log(S+1))`$ extra dirty qubits,
in addition to the $`S`$ bank inputs, and bounds full output error.
No quantum sorting is needed: the angle groups are known classically.

The [addressed-rotation reduction](GLOBAL_BLOCK_FOLLOWUP.md#5-a-constructive-reduction-to-heterogeneous-phase-batching)
uses four such batch calls, a separate clean readout bit, and
$`O(S+n^2)`$ exact routing/predicate gates. For a Hopf frame with
$`N=2^n`$, banks of size $`S_d=2^d`$, and at most $`p`$ distinct angles
**in each depth table**, take
$`\ell_d=L+n-d+O(1)`$. Summing (15) yields the sufficient bound

```math
T_F,G_F
=O\bigl(Nn+p(L+n+\log p)n^2\bigr).
\tag{16}
```

The auxiliary budget is two clean qubits and
$`N/2+O(n)`$ dirty qubits. In particular, for $`p=O(1)`$ and $`L=N`$,
this construction gives $`T_F,G_F=O(N\log^2 N)`$, below the retained
general-purpose upper bound for that special family and within an
$`O(N^2)`$ Clifford budget. This corollary is not an optimality or
best-known-bound claim for restricted angle tables. The explicitly
checked slower arithmetic in (2) also suffices
for this endpoint bound. The table entries may vary in arbitrary order;
the restriction concerns their number of distinct values.

For unrestricted angle tables, replacing them by a small palette at the
required precision is not justified. Applying this construction separately
to every binary precision layer also reintroduces the layer count into the
arithmetic cost. Equation (16) is not a generic frame-frontier improvement.

## 6. Lineage and verification boundary

The dirty commutator algebra is established prior art:
[Chi–Kim–Lee, Theorem 2 and Eq. (7)](https://arxiv.org/pdf/quant-ph/0006039)
extract modular character phases using addition and its inverse while
returning an arbitrary, reference-entangled register. The specialization
here uses a single initialized overflow bit to avoid wrapping for an
arbitrary real angle, then charges the complete native phase and arithmetic
circuits. No novelty claim is made for the commutator identity.

[Gosset–Kothari–Wu, Theorem 1.4 and §2.2](https://arxiv.org/html/2411.04790v3#S2.SS2)
give mass production with $`O(m+L)`$ T gates and growing initialized
workspace. Their Hamming-weight route computes an unmasked count. The
tradeoff proved here gives up a logarithmic gate factor to use one clean
bit and logarithmically many arbitrary dirty bits.

The focused [finite checks](../../tests/test_identical_phase_batching.py)
run with:

```sh
python -m unittest tests.test_identical_phase_batching -v
```

They exhaust borrowed-MCX inputs through six controls, accumulator/helper
inputs through six accumulator bits, and complete permitted batch inputs
through six data bits. They verify the arithmetic counts, an overflow
negative control, the literal seven-T Toffoli over exact algebraic
arithmetic, and an exact native two-input batch with a reference purifying
every permitted input. A separate 64-dimensional numerical test checks
the full-output bound for a nondiagonal phase approximant, common-scalar
cancellation, and nonzero clean-bit leakage. Four further signed-generator
checks cover centered additions with positive, negative, mixed, and zero
coefficients, nondiagonal phase error, and reuse of the clean bit across
two generators despite intermediate leakage. All eleven checks pass.

These finite checks support signs, ordering, native decomposition, counts,
and the output contract. The asymptotic proofs are above; the sharper
increment implementation, general controlled constant offsets, and
arbitrary-precision single-qubit synthesis are cited primitives, not
independently reimplemented by this test suite. The signed-generator
fixtures use exact offset permutations; they do not emit those offsets
into native gates.
