# Identical phases with one clean overflow bit

This note gives a deterministic constant-clean compiler for identical phase
gates on arbitrary input qubits. It also supplies a small-palette special
case of the [dirty tensor-phase-bank reduction](GLOBAL_BLOCK_FOLLOWUP.md#5-a-constructive-reduction-to-heterogeneous-phase-batching).
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

## 4. A small-palette phase bank and frame corollary

Suppose $`S`$ arbitrary bank inputs have phases drawn from at most
$`p\leq S`$ classically specified angles. Group equal angles, apply
(1) to each group with error $`2^{-\ell}/p`$, and reuse the workspace.
If the group sizes are $`m_1,\ldots,m_p`$, then

```math
T_B,G_B
=O\!\left(\sum_{a=1}^p
 (m_a+\ell+\log p)\log(m_a+1)\right)
\leq O\bigl((S+p(\ell+\log p))\log(S+1)\bigr).
\tag{11}
```

This needs one clean qubit and $`O(\log(S+1))`$ extra dirty qubits,
in addition to the $`S`$ bank inputs, and bounds full output error.
No quantum sorting is needed: the angle groups are known classically.

The [addressed-rotation reduction](GLOBAL_BLOCK_FOLLOWUP.md#5-a-constructive-reduction-to-heterogeneous-phase-batching)
uses four such batch calls, a separate clean readout bit, and
$`O(S+n^2)`$ exact routing/predicate gates. For a Hopf frame with
$`N=2^n`$, banks of size $`S_d=2^d`$, and at most $`p`$ distinct angles
**in each depth table**, take
$`\ell_d=L+n-d+O(1)`$. Summing (11) yields the sufficient bound

```math
T_F,G_F
=O\bigl(Nn+p(L+n+\log p)n^2\bigr).
\tag{12}
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
arithmetic cost. Equation (12) is not a generic frame-frontier improvement.

## 5. Lineage and verification boundary

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
cancellation, and nonzero clean-bit leakage. All seven checks pass.

These finite checks support signs, ordering, native decomposition, counts,
and the output contract. The asymptotic proofs are above; the sharper
increment implementation and arbitrary-precision single-qubit synthesis
are cited primitives, not independently reimplemented by this test suite.
