# Reusing the geometric operator source for scalar attenuation

The [operator-source compiler](OPERATOR_SOURCE_COMPILER.md) prepares a
geometric Majorana operator with linear T cost. A possible amortization
route is to prepare its graph encoding once, then obtain many scalar
attenuations from cheap kernels while returning that encoding. This note
checks that particular interface. It proves that constant additional clean
workspace cannot support sublinear T cost for large attenuation exponents
on this encoding, even when its initial preparation is charged only once.
It does not give an additive lower bound for a frame compiler or change the
current full-frame upper bound.

## 1. Encoding and the required returned operator

Use the source convention of the compiler: on an arbitrary dirty bank of
$`m\ge2`$ qubits,

```math
\Gamma_j=Z_0\cdots Z_{j-1}X_j,\qquad
M=\sum_{j=0}^{m-1}a_j\Gamma_j,
\qquad
a_j^2=\begin{cases}
2^{-(j+1)},&j<m-1,\\
2^{-(m-1)},&j=m-1.
\end{cases}
```

The coefficients are positive, the generators anticommute, and
$`M^2=I`$. One retained graph flag encodes an arbitrary bank input by

```math
E\psi=\frac{|0\rangle\psi+|1\rangle M\psi}{\sqrt2},\qquad
EE^\dagger=\frac{I+\sum_j a_jP_j}{2},\qquad
P_j=X_{\rm graph}\otimes\Gamma_j.
\tag{1}
```

Any extra dirty helpers are included in the input of $`E`$, with identity
factors in (1). They may be entangled with the bank and an external
reference. The initial preparation of $`E`$ is outside the kernel cost
below and may use the known $`O(m)`$ source circuit.

Let $`U`$ be a fixed coherent Clifford+T circuit on the retained graph,
bank, dirty helpers, and $`r`$ additional private qubits initialized to
zero. It has $`\tau`$ T or T-dagger gates. Its unnormalized accepted block is

```math
K=\langle0^r|U|0^r\rangle.
```

Count **all** additional initialized scratch in $`r`$, even if its circuit
returns it deterministically. The graph flag belongs to the retained
encoding, not these private flags. The desired contract is

```math
\|KE-\lambda E\|\le\delta,\qquad
\lambda=2^{-k},\qquad 0\le\delta\le\theta\lambda,
\quad 0\le\theta<1.
\tag{2}
```

Here $`k\ge0`$ is an integer. This is an operator-norm promise on every
bank/helper input, so it also
holds with arbitrary references. It includes return of the encoding and
all dirty work on the accepted branch. It is not a normalized postselected
state promise, a scalar expectation, or a marginal obtained by discarding
work. Averaging inputs in the proof below is only a mathematical test of
this full operator contract.

## 2. Bound for one returned attenuation block

The field-conjugation argument below is the arithmetic tool retained in
the [returned-source theorem](SOURCE_CHANNEL_PROOF.md); the graph-specific
ingredients here are the Pauli-support dimension and geometric tail bound.

If $`K\ne0`$ and $`\tau+r<m`$, then

```math
\frac{\|KE\|_F^2}{\dim(\mathrm{domain}(E))}
\ge 2^{-(2\tau+3r+1)}.
\tag{3}
```

Consequently, (2) requires either $`\tau+r\ge m`$ or

```math
\boxed{\displaystyle
\tau\ge k-\frac{3r+1}{2}-\log_2(1+\theta).}
\tag{4}
```

For constant $`r`$, this rules out a uniformly polylogarithmic T cost for
returned attenuations with $`k=\Theta(m)`$ and fixed relative accuracy.
It also applies to an absolute budget $`\delta=2^{-L}`$ whenever the chosen
$`k`$ leaves $`\delta/2^{-k}<1`$; for example, $`m=\Theta(L)`$ and
$`k\approx L/2`$ remain within this regime. The constants in (3) and (4)
are sufficient bounds, without a sharpness claim.

If a kernel also receives and returns a coherent $`\ell`$-bit index,
fix one index basis input and project onto that same output. Free X gates
identify this restricted block with $`r+\ell`$ initialized/projected
flags, even if the circuit changes the index temporarily. Equations
(3) and (4) then apply with $`r\mapsto r+\ell`$; projection cannot increase
the promised error. This is a proof restriction, not an additional clean
allocation in the implementation. With constant $`r`$, an index of width
$`O(\log L)`$ therefore does not remove the linear bound for
$`k=\Theta(L)`$ and $`m=\Theta(L)`$.

**Pauli support.** Write $`A=K^\dagger K`$, and let $`D`$ be the dimension
of the retained graph, bank, and helpers. Before compressing the input
private flags, $`A`$ comes from conjugating their output projector
$`2^{-r}\prod_{t=1}^r(I+Z_t)`$ by $`U`$. Its initial binary Pauli-label
span has dimension $`r`$. A Clifford transports this span linearly. One T
or T-dagger conjugation sends each Pauli to itself or to a linear
combination of itself and its product with that gate's Z Pauli. It can
therefore add at most one label to the span.

Compression against the initialized private flags discards terms with
X or Y on those flags and removes the remaining I/Z labels. This filters
the support and applies a linear projection, so the Pauli support of
$`A`$ lies in a binary subspace of dimension at most $`r+\tau`$.
The labels of the $`P_j`$ in (1) are linearly independent: each has an X
component on its own bank coordinate and none on any other bank
coordinate. Hence at most $`h\le r+\tau`$ of them can occur in $`A`$.

**Positivity and the geometric tail.** Set
$`q=\mathrm{Tr}(A)/D>0`$ and $`\rho=A/\mathrm{Tr}(A)`$.
Let $`b_j=\mathrm{Tr}(\rho P_j)`$. Anticommutation and positivity give
$`\sum_j b_j^2\le1`$: the Hermitian operator $`B=\sum_j b_jP_j`$ has
norm $`\sqrt{\sum_j b_j^2}`$, while
$`\mathrm{Tr}(\rho B)=\sum_j b_j^2\le\|B\|`$.
Pauli orthogonality gives $`b_j=0`$ outside the support of $`A`$.
For $`h<m`$, the sum of the largest $`h`$ squared source coefficients is
exactly $`1-2^{-h}`$. Thus (1) gives

```math
p:=\frac{\mathrm{Tr}(E^\dagger AE)}{D/2}
=q\left(1+\sum_j a_jb_j\right)
\ge q\left(1-\sqrt{1-2^{-h}}\right)
\ge q\,2^{-h-1}.
\tag{5}
```

**Nonzero maximally mixed acceptance.** The quantity $`q`$ is the
acceptance probability for maximally mixed retained data and zero private
flags. Clifford Pauli-transfer matrices are integral; each T/T-dagger
matrix has entries in $`(\sqrt2)^{-1}\mathbb Z[\sqrt2]`$.
Normalized Pauli traces cancel the input stabilizer expansion and data
dimension; the output private-flag projector contributes the remaining
factor $`2^{-r}`$. Therefore

```math
q\in\frac{1}{2^r(\sqrt2)^\tau}\mathbb Z[\sqrt2].
\tag{6}
```

Under the field conjugation $`\sqrt2\mapsto-\sqrt2`$, its conjugate
$`q^\sigma`$ is another physical acceptance probability: replace every
T by ZT and every T-dagger by ZT-dagger in the Pauli-transfer circuit.
Thus $`0<q^\sigma\le1`$ when $`q\ne0`$. The nonzero algebraic norm of
the numerator in (6) is an integer, so

```math
q\,q^\sigma\ge2^{-(\tau+2r)},\qquad
q\ge2^{-(\tau+2r)}.
\tag{7}
```

Combining (5), (7), and $`h\le r+\tau<m`$ proves (3).
Since $`E`$ is an isometry, (2) implies $`p\le(\lambda+\delta)^2`$;
substitution proves (4). If $`K=0`$, (2) instead requires
$`\delta\ge\lambda`$, excluded by $`\theta<1`$.
The same argument applies to a target $`\lambda EW`$ for any unitary
$`W`$ on the domain of $`E`$ (bank and helpers): a known shift of the
arbitrary input does not evade the
bound, because the proof only uses the target's norm.

## 3. Exact checks of the interface boundaries

A cheap scalar compression exists and explains the attraction of this
encoding. The Clifford Pauli $`J_j=X_{\rm graph}\otimes\Gamma_j`$
satisfies

```math
E^\dagger J_jE=a_jI.
```

For $`j=2k-1<m-1`$, this scalar is $`2^{-k}`$ with zero T gates.
But the complementary isometry
$`E_-\psi=(|0\rangle\psi-|1\rangle M\psi)/\sqrt2`$ obeys

```math
E_-^\dagger J_jE=\frac{\Gamma_jM-M\Gamma_j}{2},\qquad
\|E_-^\dagger J_jE\|=\sqrt{1-a_j^2}.
\tag{8}
```

The last equality follows from $`\{\Gamma_j,M\}=2a_jI`$ and
$`\Gamma_j^2=M^2=I`$. Hence
$`\|J_jE-a_jE\|=\sqrt{1-a_j^2}`$: the small scalar compression has
order-one leakage out of the code. A final code projection would give
$`EE^\dagger J_jE=a_jE`$, but its reflection is
$`2EE^\dagger-I=X_{\rm graph}\otimes M`$, reintroducing the source
operation whose repeated cost was to be avoided.

The flag count also matters. Apply Hadamards to $`2k`$ initially-zero
private flags and accept all zeros. This gives $`K=2^{-k}I`$ with zero
T gates and exact code return, using $`r=2k`$; it satisfies the theorem.
Sequential measurement, reset, and postselection may reuse a physical
flag, but such a procedure is not the single coherent block defined
above. Its total projection events cannot be replaced by its peak live
flag count in (6). Finally, a zero accepted block has error exactly
$`\lambda`$, so the strict relative-error requirement is necessary.

These are exact operator checks, not numerical evidence for the theorem.
The [four focused circuit tests](../../tests/test_operator_source_reuse.py)
check a native T gate that expands accepted Pauli-support rank, irrational
acceptance and its physical field conjugate, the graph leakage identity,
and the difference between fresh projected flags and coherent flag reuse.
They use exact arithmetic; these finite fixtures exercise the interfaces
and do not replace the general proof.
The proof permits arbitrary Clifford routing and arbitrary dirty helpers;
it does not assume a particular attempted shift circuit. It excludes this
returned graph-source attenuation route with constant private flags,
while leaving different encodings, joint blocks without intermediate
source return, and the unrestricted full-frame endpoint open.
