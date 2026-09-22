# Borrowed-workspace compiler and the all-clean-budget corollary

This publication appendix proves the arbitrary-budget borrowed-workspace
upper bound and its restricted matching splice with the
[sufficient-clean compiler](FAULT_TOLERANT_COMPILER.md). Its dirty lookup
and predicate-toggle primitives also support the
[two-clean construction](OPERATOR_SOURCE_COMPILER.md). It concerns the
prescribed complete **real** Hopf frame; no complex-frame or common-phase
extension is asserted here.

## 1. Contract and statements

Use the rotation convention, frame order, and complete initialized-isometry
contract of the main theorem. In particular, set

```math
\begin{gathered}
N=2^n,\qquad q=n+a+b,\qquad 0<\eta\le1/64,\\
L=\max\{6,\lceil\log_2(1/\eta)\rceil\},\qquad
h=1+\lceil\log_2(L+n+2)\rceil.
\end{gathered}
```

For every $`n\ge1`$ and every $`a,b\ge0`$, a coherent Clifford+T circuit
implements the specified real frame with

```math
T=O\!\left(\frac{NL}{q}+L\sqrt N\right),
\qquad G=O(NL).
\tag{1}
```

All extra wires are treated as arbitrary borrowed inputs. The construction
in fact implements $`\widetilde W\otimes I_{a+b}`$ exactly, where
$`\|\widetilde W-W\|\le\eta`$. It therefore returns every borrowed wire
exactly, jointly with arbitrary references, and meets the initialized-clean
contract when any designated clean wires are supplied in zero. Native scalar
phases are retained. There are no measurements, resets, supplied magic states,
or uncharged oracles. Angle evaluation and classical single-qubit synthesis
are additional classical work.

Combining (1) with the main theorem gives, for each fixed $`c>0`$,

```math
h+b\le c\sqrt N
\quad\Longrightarrow\quad
\tau^*_{F,\mathbb R}(n,a,b,\eta)
=\Theta_c\!\left(\sqrt{NL}+L+\frac{NL}{q}\right)
\quad\text{for every }a\ge0.
\tag{2}
```

Here the optimum and lower bound are worst-case over prescribed angle tuples.
Section 6 gives the splice proof. Neither statement resolves the constant-clean,
large-dirty endpoint outside the hypothesis of (2).

## 2. Exact dirty table and reflection interpreter

Consider a Boolean table with $`S=2^r`$ rows and a power-of-two number
$`\lambda\le S`$ of one-bit banks. The low address selects a bank; the
high address has $`k=r-\log_2\lambda`$ bits. Use $`k`$ arbitrary dirty
selectors. During a depth-first traversal of the high-address rows, update
the selectors along a path with address literals $`\ell_i`$ by

```math
v_1=z_1\oplus\ell_1,\qquad
v_i=z_i\oplus v_{i-1}\ell_i.
```

At each leaf, CNOT the last selector into the banks whose table bits are one;
undo selector updates on returning from the subtree. Expanding the recurrence
gives

```math
v_k=\prod_{i=1}^k\ell_i\ \oplus\ H_z(\ell_2,\ldots,\ell_k).
```

Repeat the same traversal and data insertions with the first selector updates
omitted. Its leaf value is exactly the unwanted term $`H_z`$. Composing the
first traversal with the inverse of the second cancels those terms and
restores every selector. This is a phase-free permutation on all inputs.
For $`k=0`$, insert the constant bank contents by X gates. The resulting
loader costs $`O(S/\lambda)`$ Toffolis and $`O(S)`$ Clifford gates.

The interpreter uses only the fixed reflection alphabet

```math
\mathcal R=\{T^jHT^{-j}:0\le j<8\}\cup\{Z\}.
```

Each member squares to identity. Every one-qubit native word of determinant
$`\pm1`$ has an exact $`O(w)`$-length rewrite in this alphabet: expand it
in H and T powers, move the accumulated T power past each H, and retain the
conjugated H. The residual T exponent is zero or four modulo eight, by the
determinant promise, so the remaining gate is I or Z. These are exact matrix
equalities, including scalar phase. The words used below have determinant one.

One- and two-controlled reflections have constant-size exact circuits without
scratch. For example, $`V=SHTHS^\dagger`$ obeys $`VZV^\dagger=H`$.
Conjugating controlled-Z or twice-controlled-Z by V gives the corresponding
controlled-H; twice-controlled-Z is an H-conjugated exact Toffoli. Conjugating
on the target by T powers covers the remaining reflections.

Let $`L_f`$ be a dirty loader, $`R`$ a Fredkin bank router, and $`\beta`$
an arbitrary additional control. For one reflection G, use the following
chronological sequence:

```math
L_f,\ R,\ C_{\beta,\mathrm{bank}\,0}G,\ R^\dagger,\ L_f^\dagger,
\ R,\ C_{\beta,\mathrm{bank}\,0}G,\ R^\dagger.
\tag{3}
```

On an original selected bank value z, the two target exponents are
$`\beta(z\oplus f)`$ and $`\beta z`$. Since G is an involution, their
product is $`G^{\beta f}`$. Banks, selectors, and addresses return exactly.
The identity on basis inputs extends to arbitrary reference-entangled inputs.
Complete both uses of a reflection before advancing to the next one;
different reflections need not commute.

Rewrite each table word and pad it into a common schedule: at each word
position, use nine Boolean tables that indicate which reflection is present.
This changes only a constant factor. Routing costs $`O(\lambda)`$ Fredkins.
The controlled multiplexor consequently costs

```math
T_{\rm mux}=O\!\left(w(S/\lambda+\lambda+1)\right),
\qquad G_{\rm mux}=O(Sw),
\tag{4}
```

with at most r dirty selectors and $`\lambda`$ dirty banks. For $`S=1`$,
apply the known controlled word directly, using no selectors or banks.

## 3. An exact echo selects a logical sector

A predicate toggle with k controls can be implemented with one arbitrary
borrowed bit and $`O(k^2)`$ exact Toffolis. Split the controls into A and B.
Let F toggle the borrowed bit z by $`\bigwedge A`$, and G toggle the target
by $`z\wedge\bigwedge B`$. The chronological word
$`F,G,F^{-1},G^{-1}`$ toggles the target by $`\bigwedge(A\cup B)`$ and
restores z. Recursively implement F borrowing the target and G borrowing a
bit of A. For more than two controls the recurrence is

```math
m(k)=2m(\lceil k/2\rceil)+2m(\lfloor k/2\rfloor+1)=O(k^2),
```

with X, CNOT, and the exact seven-T Toffoli as base cases. Negative controls
use paired X gates. This recursion is a full-unitary identity.

At Hopf depth d, let t be the rotation target. When a suffix exists, take its
first bit as a borrowed control $`\beta`$ whose selected value is zero.
At the final depth, take one prefix bit as $`\beta`$ and process its two
values in separate sectors. Leave $`r_d`$ other prefix bits as a free table
address. The remaining $`n-2-r_d`$ system bits form F. Let $`P`$ indicate
that F equals the specified outer prefix and zero suffix. The predicate
toggle M acts as $`\beta\mapsto\beta\oplus P`$, borrowing t, and costs
$`O(n^2)`$ Toffolis.

For each free-address row x, synthesize a word $`Q_x`$ that approximates
$`R_y(\theta_x/4)`$ up to scalar phase. Define the actual word

```math
C_x=XQ_x^\dagger XQ_x.
```

The scalar phase cancels. Exactly, regardless of approximation error,

```math
\det C_x=1,\qquad XC_xX=C_x^\dagger.
\tag{5}
```

It approximates $`R_y(\theta_x/2)`$. Implement its controlled table using
(3)–(4), borrowing selectors and banks from F and the external workspace.
All these bits return before each predicate toggle. Now apply, chronologically,

```math
C_\beta X,\ M,\ C_\beta C,\ M^\dagger,
\ C_\beta X,\ M,\ C_\beta C,\ M^\dagger.
\tag{6}
```

| Original borrowed control | Predicate | Target action |
|---:|---:|---|
| 0 | 1 | $`C_x^2`$ |
| 0 | 0 | I |
| 1 | 0 | $`(C_xX)^2=I`$ |
| 1 | 1 | I |

Equation (5) makes the inactive cancellation exact, even though the actual
word need not be a real rotation. Surround (6) by X on $`\beta`$ to select
its original value one. Every system control and external borrowed wire is
restored. None is assumed zero during the multiplexor.

If Q has phase-optimized error at most $`\epsilon_d/4`$, then C has error
at most $`\epsilon_d/2`$ and $`C^2`$ has error at most $`\epsilon_d`$.
Distinct sectors have orthogonal invariant supports, so their errors take
a maximum rather than adding. Set

```math
\epsilon_d=\eta\,2^{d-n},\qquad
w_d=O(L+n-d).
\tag{7}
```

Standard one-qubit synthesis supplies these word lengths, including Clifford
gates. Summing (7) over depths gives total operator error less than $`\eta`$.
This establishes the full-frame contract, rather than just a first-column
state-preparation guarantee.

## 4. Capacity and the arbitrary-width resource sum

Write $`B=a+b`$ and $`K=n+B=q`$. Extra clean wires can be treated as arbitrary
borrowed wires because the preceding identities hold on their full spaces.
For $`n\ge2`$, choose

```math
r=\min\left\{
\left\lceil\log_2(n^2K+K^2)\right\rceil,\ n-2,
\max\left(0,\left\lfloor\frac{K-3}{2}\right\rfloor\right)
\right\},\qquad A=2^r.
\tag{8}
```

At depth d use $`r_d=\min(d,r)`$, except that the final depth permits at
most $`d-1`$ free prefix bits. The restriction $`r\le n-2`$ already ensures
this. After reserving $`r_d`$ dirty selectors, the combined fixed-system and
external bank capacity is

```math
K-2-2r_d.
\tag{9}
```

There are $`2^{d-r_d}`$ sectors, including both borrowed-control values at
the final depth. Whenever the capacity in (9) is $`\Omega(K)`$, choose a
power-of-two bank count within a factor two of
$`\min\{S,\sqrt S,\text{capacity}\}`$, with $`S=2^{r_d}`$. Equation (4)
and the predicate toggles give per sector

```math
O\!\left(n^2+\frac{Sw_d}{K}+w_d\sqrt S+w_d\right).
\tag{10}
```

First suppose $`B<4n`$. For all sufficiently large n, (8) has
$`r=O(\log n)`$, $`A=\Theta(n^2K+K^2)=O(n^3)`$, and (9) is
$`\Omega(n)=\Omega(K)`$. Deep layers, $`d\ge r`$, contribute

```math
O\!\left(\frac{Nn^2}{A}+\frac{NL}{K}
+\frac{NL}{\sqrt A}+\frac{NL}{A}\right)
=O(NL/K),
\tag{11}
```

because $`A\ge n^2K,K^2`$. Shallow layers contribute at most

```math
O\!\left(rn^2+\frac{A(L+n)}K+(L+n)\sqrt A+r(L+n)\right).
```

Here $`K=\Theta(n)`$ and $`A=O(n^3)`$, so dividing by $`NL/K`$ leaves
polynomials in n divided by $`2^n`$, uniformly bounded for $`L\ge6`$.
For the finitely many remaining n in this case, use no free address bits
and synthesize one sector at a time. The cost
$`O(N(n^2+L+n))`$ obeys (1) with a larger absolute constant. No bank is
needed in this fallback.

Now suppose $`B\ge4n`$. The capacity cutoff in (8) cannot bind before
$`r=n-2`$, and

```math
K-2-2r_d\ge B-n+2=\Omega(K).
```

If the address cap does not bind, $`A\ge n^2K,K^2`$; if it binds,
$`A=N/4`$. Thus the expression on the left of (11) is
$`O(NL/K+L\sqrt N+n^2)`$. For shallow layers put $`u=n-r`$ and retain
the decreasing precision in (7). Geometric sums give

```math
\sum_{d<r}2^{d/2}(L+n-d)=O\!\left(\sqrt A(L+u+1)\right),
\qquad
\sum_{d<r}\frac{2^d(L+n-d)}K
=O\!\left(\frac{A(L+u+1)}K\right).
```

Since $`A/N=2^{-u}`$, these are respectively $`O(L\sqrt N)`$ and
$`O(NL/K)`$. The remaining predicate and word costs are
$`O(n^3+nL+n^2)=O(L\sqrt N)`$. This proves (1) for $`n\ge2`$.
For $`n=1`$, apply $`C^2`$ directly at cost $`O(L)`$, ignoring workspace.

Table insertion across sectors has cost

```math
O\!\left(\sum_{d=0}^{n-1}2^dw_d\right)=O(NL).
```

All other elementary gates obey the preceding sums and hence also fit
$`O(NL)`$. These statements bound gate count; they do not claim an optimal
depth or classical compilation time.

## 5. Scope of the underlying ingredients

The dirty-bank cancellation follows the SelectSwap lineage in Low,
Kliuchnikov, and Schaeffer, [Figure 1(d) and equation (8)](https://arxiv.org/html/1812.00954v2).
Borrowed-bit predicate toggles and dirty-selector cancellation have established
precedents; see also Khattar and Gidney,
[Sections 4 and 7.4](https://arxiv.org/pdf/2407.17966v2).
The proof above supplies the particular exact identities and conservative
counts needed here; it imports neither measurement-based uncomputation nor
optimized relative-phase gate constants. One-qubit approximation is the
same synthesis input used in the
[main theorem](FAULT_TOLERANT_COMPILER.md#primary-references).

In particular, (3) is not a valid dirty interpreter for arbitrary rotations:
it uses $`G^2=I`$. Equation (6) also requires the exact symmetry (5).
A merely approximate symmetry would introduce inactive-sector errors that
could accumulate over sectors. These exact properties explain why borrowed
program memory is valid without an initialized precision register.

## 6. The all-clean-budget splice

Let C be the absolute sufficient-clean constant in the main theorem, increased
to at least one. If $`a\ge C(n+h)`$, use that theorem. Otherwise, under
$`h+b\le c\sqrt N`$ and using $`n\le2\sqrt N`$,

```math
q<(C+1)n+Ch+b\le D\sqrt N,
\qquad D=2(C+1)+Cc.
```

The borrowed compiler then gives

```math
T=O\!\left(NL/q+L\sqrt N\right)=O_c(NL/q),
```

because $`L\sqrt N\le DNL/q`$. Both branches satisfy the same literal
initialized-isometry and dirty/reference-return contract, with $`O_c(NL)`$
Clifford work. The real-diagonal and fixed-width lower bounds proved in the
main theorem give the opposite order and establish (2).

At $`a=O(1), b=\Theta(N), L=N`$, the hypothesis of (2) fails. Equation (1)
still gives $`O(N^{3/2})`$, against the retained $`\Omega(N)`$ lower bound.
The [two-clean construction](OPERATOR_SOURCE_COMPILER.md) improves this upper
bound at its stated allocation; the remaining gap is recorded in the
[open problem](OPEN_PROBLEM.md).
