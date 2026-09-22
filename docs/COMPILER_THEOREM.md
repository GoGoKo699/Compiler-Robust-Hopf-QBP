# Complete all-workspace compiler theorem

This page concerns the **exact logical model**. The integrated paper also has
a [fault-tolerant compiler theorem](FAULT_TOLERANT_COMPILER.md) and an
[approximate-QBP bridge](QBP_APPROXIMATION.md); their hypotheses and evidence
are stated separately.

[← Hopf interface](HOPF_INTERFACE.md) · [Complete narrative](../REVIEW.md) · [QBP consequence →](QBP_CONSEQUENCE.md)

This page gives the formal operator and resource proof.  The construction uses
one exact circuit framework and three Hopf-specific schedules covering every
clean-workspace budget.

## 1. Circuit model and imported results

Let

```math
N=2^n
```

and let $m\geq0$ be the number of clean ancillary qubits.  The circuit model is:

- arbitrary one-qubit gates;
- CNOTs;
- all-to-all logical connectivity;
- exact unitary implementation;
- clean ancillary qubits initialized in $\lvert0\rangle$ and returned exactly to $\lvert0\rangle$.

Toffoli, Fredkin, controlled one-qubit gates, and the fixed-width controlled
Givens rotations used as readable primitives have exact constant-size,
constant-depth decompositions in this model.

The proof imports the following results from P. Yuan and S. Zhang, *Quantum*
**7**, 956 (2023).

| Imported result | Form used here |
|---|---|
| Yuan–Zhang Theorem 2 | exact $q$-qubit state preparation has $\Theta(2^q)$ size and $`\Theta\!\left(q+\frac{2^q}{q+w}\right)`$ depth with $w$ clean ancillary qubits |
| Yuan–Zhang Lemma 5 | an $r$-controlled X has $O(r)$ size and depth with no ancillary qubit |
| Yuan–Zhang Lemma 6 | a total-width-$`q`$ UCG has $O(2^q)$ size and $`O\!\left(q+\frac{2^q}{q+w}\right)`$ depth with $w$ clean ancillary qubits |
| Yuan–Zhang Lemma 9 | coherent CNOT-tree copying and exact uncopying have logarithmic depth and linear size |

The published article corresponds to `arXiv:2202.11302v2`.  The imported
statements were also checked in v3 and retain the forms and model conventions
used here.

The earlier state-preparation paper is the historical predecessor and original
source of selected primitives.  It is not used as a second regime-dependent
compiler.

## 2. Compiler target

Let

```math
J_m|\varphi\rangle
=|\varphi\rangle|0^m\rangle.
```

### Definition: frame-safe implementation

A unitary $\widetilde W$ on the system and $m$ clean work qubits is frame-safe for
$W$ when

```math
\widetilde WJ_m=J_mW.
```

This complete clean-input equality implies

```math
\widetilde W^{\dagger}J_m
=J_mW^{\dagger}
```

because the clean subspace is reducing for $\widetilde W$.

The real Hopf frame is

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_0^{(n)},
```

where, at depth $d$,

```math
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The phase-dressed complex magnitude frame is

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

## 3. Main theorem

### Main theorem: optimal exact Hopf-frame compilation

For every integer $n\geq1$ and $m\geq0$, the real Hopf differential frame has an
exact frame-safe implementation using at most $m$ clean ancillary qubits with

```math
S_{\mathbb R}(n,m)=\Theta(2^n)
```

and

```math
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
```

The phase-dressed complex magnitude frame has the same frontier:

```math
S_{\mathbb C,\mathrm{mag}}(n,m)=\Theta(2^n),
```

```math
D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
```

The upper bounds hold for every parameter tuple. The matching lower bounds
hold in the worst case over the Hopf-frame family, uniformly in the
clean-workspace budget. They do not impose the same cost on every individual
frame.

For $n\geq2$, the worst-case **CNOT count alone** is also $\Theta(N)$,
even when arbitrary one-qubit gates are free. The one-qubit case $n=1$
requires zero CNOTs. Section 9 gives the additional argument needed to
separate this statement from the total-size bound. These are asymptotic
counts; no optimal leading CNOT constant is asserted.

The proof is assembled from the three schedules below and the matching lower
bounds in Section 9.

## 4. Strict zero workspace

Assume $m=0$ and fix a nonfinal depth $d\lt n-1$.  Write the system register as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R,
```

where $p$ contains the $d$ prefix bits, $x$ is the Hopf target, $b$ is the first
lower-suffix bit, and $r$ contains the remaining $n-d-2$ suffix bits.

Set

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2),
```

and let $T_h$ toggle $b$ when $h(r)=1$.

### Lemma Z: borrowed-suffix echo

The chronological sequence

```text
controlled_b(X)
T_h
controlled_b(C_p)
T_h
controlled_b(X)
T_h
controlled_b(C_p)
T_h
```

implements $L_d^{(n)}$ exactly, with the borrowed suffix bit restored
and no additional sector-dependent phase.

#### Proof

The Hopf rotation convention gives

```math
C_p^2=R_y(\theta_{d,p}),
\qquad
XC_pX=C_p^{-1}.
```

For fixed $p$ and $r$, the four invariant sectors are:

| $h(r)$ | original $b$ | chronological target word | net action | final $b$ |
|---:|---:|---|---|---:|
| 0 | 0 | none | $I$ | 0 |
| 0 | 1 | $X,C_p,X,C_p$ | $C_pXC_pX=I$ | 1 |
| 1 | 0 | $C_p,C_p$ | $R_y(\theta_{d,p})$ | 0 |
| 1 | 1 | $X,X$ | $I$ | 1 |

The active sector is exactly the sector in which the original complete suffix
$br$ is zero.  Every other sector receives identity.  The borrowed bit is
restored and no sector-dependent phase appears.  Orthogonality of the $p,r$
sectors gives the complete operator identity on arbitrary superpositions and
entangled inputs.  ∎

### Proposition Z: strict-zero resources

Each controlled $C_p$ is one UCG with:

- $d$ prefix controls;
- the borrowed bit as one additional control;
- one target.

Its total width is

```math
q=d+2.
```

The remaining suffix bits participate only in $T_h$.  Yuan–Zhang Lemma 5
implements $T_h$ without an ancillary qubit.  Therefore

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)
=O\left(n+\frac{2^d}{d+2}\right).
```

The final depth has no suffix and is one total-width-$`n`$ UCG.  Consequently,

```math
S(W_{\mathbb R})
=O\left(\sum_{d=0}^{n-2}2^d+n^2+2^n\right)
=O(2^n).
```

Furthermore,

```math
\sum_{q=2}^{n}\frac{2^q}{q}
=O(2^n/n)
```

and $n^2=O(2^n/n)$, so

```math
D(W_{\mathbb R})
=O\left(n+\frac{2^n}{n}\right).
```

For $n=1$, only the final one-qubit rotation remains.  For $d=n-2$, $r$ is
empty and $T_h=X_b$; Lemma Z is unchanged.

## 5. Small positive workspace

Assume $m\geq1$.  At each nonfinal depth, compute the complete lower-suffix-zero
predicate into one reusable clean flag, apply one UCG selected by the prefix and
flag, and uncompute the flag.

### Proposition D: direct flagged schedule

The direct schedule has

```math
S_{\mathrm{direct}}(n,m)=O(2^n)
```

and

```math
D_{\mathrm{direct}}(n,m)
=O\left(n^2+\frac{2^n}{n+m}\right).
```

#### Proof

The nonfinal depth-$`d`$ UCG has total width $d+2$ and may use $m-1$ additional
clean qubits.  The final depth has no predicate flag and may use all $m$ clean
qubits.  Yuan–Zhang Lemma 6 gives a geometric $O(2^n)$ total size and the
displayed UCG depth term.  The compute–uncompute predicates contribute
$O(n^2)$ total size and depth.  ∎

If

```math
1\leq m\lt 4n,
```

then $n+m\lt 5n$.  Since $n^3=O(2^n)$,

```math
n^2=O\left(\frac{2^n}{n+m}\right),
```

so Proposition D already attains the target depth throughout this regime.

## 6. Exact tree cut

For a cut after the first $t$ depths, define

```math
B=2^t,
\qquad
s=n-t,
```

and write

```math
W_{\mathbb R}^{(n)}
=R_t^{(n)}F_t^{(n)}.
```

### Lemma T1: conditioned prefix identity

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I_{2^t}\otimes\left(I-|0^s\rangle\!\langle0^s|\right).
```

#### Proof

Every layer above the cut contains the complete external suffix in its
zero-suffix predicate.  On the sector $\lvert0^s\rangle$, these layers form the $t$-qubit
Hopf frame.  On the orthogonal complement, every layer is identity.  ∎

### Lemma T2: tail direct sum

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A local node $(\ell,u)$ in branch $r$ uses global breadth-first node

```math
2^{t+\ell}+r2^\ell+u.
```

#### Proof

Every layer below the cut preserves the $t$-bit prefix.  Each fixed-prefix
subspace is invariant, and the restricted action is exactly the Hopf frame of
that subtree with the displayed angle map.  ∎

## 7. Conditioned prefix construction

### Lemma P: clean binary–one-hot decoder

For an integer $t\geq1$ and $B=2^t$, there is an explicit reversible
X/CNOT/Toffoli circuit satisfying

```math
D_t|x\rangle|0\cdots0\rangle
=|0^t\rangle|e_x\rangle|0\cdots0\rangle.
```

It uses

```math
3B-2-t
```

clean ancillary qubits and has $11t-4$ disjoint X/CNOT/Toffoli layers.
Decomposing these fixed-width primitives into arbitrary one-qubit gates and
CNOTs gives elementary depth $O(t)$ and size $O(B)$.

#### Register count

| Register | Qubits |
|---|---:|
| one-hot leaves | $B$ |
| internal indicators | $B-1$ |
| shared scratch and fanout pool | $B-1-t$ |
| **total** | $3B-2-t$ |

The explicit schedule propagates one active tree indicator according to the
binary address, reconstructs each address bit as a parity of active right-child
indicators, and clears the original address.  Reversing the layers gives the
exact inverse.

On the one-hot code, the Givens pairs at each Hopf depth are disjoint.  Computing
and copying the external suffix-zero predicate, applying the fixed-width
controlled Givens rotations, and reversing the decoder implements $F_t^{(n)}$ in

```math
S(F_t)=O(B+s),
\qquad
D(F_t)=O(n).
```

## 8. Routed parallel tail

### Lemma R: explicit coherent router

There is an exact route–operate–unroute circuit for $R_t^{(n)}$ using:

```math
(B-1)s
```

additional branch-data qubits,

```math
B
```

one-hot activation-token qubits, and

```math
C=(B-1)(s+1)-t
```

copied routing controls.

Treat each branch's $s$ data qubits and one token as a block of width $s+1$.
At routing level $j$, prefix bit $j$ controls $2^j(s+1)$ disjoint Fredkin gates.
One original prefix wire is available, so $2^j(s+1)-1$ clean copies are needed.
Summing over $j=0,\ldots,t-1$ gives $C$.  The forward Fredkin count is

```math
F=(B-1)(s+1).
```

Balanced CNOT trees create and erase the prefix copies.  Processing the prefix
bits from least to most significant sends the suffix-token block coherently to
the branch selected by the prefix, including on prefix–suffix-entangled inputs.

After routing, the copies are uncomputed.  Their cleared wires are reused as
one local suffix flag per branch.  For $s\geq2$, this is possible because

```math
\begin{aligned}
C-B
&=(B-1)(s+1)-t-B\\
&=(B-1)s-t-1\\
&\geq0.
\end{aligned}
```

All token-controlled subtree frames have disjoint data, token, and flag
registers and run in parallel.  Every flag is cleared; the copies are recreated;
the Fredkin levels are reversed; the copies and root token are reset.

The tail peak is

```math
(B-1)s+B+
\max\left\{(B-1)(s+1)-t,\,B\right\}.
```

The prefix and tail execute sequentially and both fit within

```math
2B(s+1)
```

clean ancillary qubits.

Route and unroute have $O(n)$ depth and $O(B(s+1))$ size.  Each controlled
subtree frame has $O(2^s)$ size and

```math
O\left(s^2+\frac{2^s}{s}\right)
```

depth.  Parallel execution multiplies the size by $B$ but not the depth.  Since
$B2^s=2^n$, the routed tail has $O(2^n)$ total size.

### Proposition R: maximal-cut depth

Assume $n\geq2$ and $m\geq4n$. Choose the largest integer
$1\leq t\leq n-1$ satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If $s=n-t>1$, failure of the next cut gives

```math
m\lt 4\,2^t s,
```

hence

```math
\frac{2^s}{s}
=\frac{2^n}{2^t s}
\lt 4\frac{2^n}{m}
=O\left(\frac{2^n}{n+m}\right).
```

Also,

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

If $s=1$, each subtree frame has constant depth.  Feasibility of $t=n-1$
requires $m\geq2^{n+1}=2N$, so $N/(n+m)=O(1)$ and the target depth is
$\Theta(n)$, matching the prefix and route–unroute stages.

Thus the subtree term obeys the uniform bound
$`2^s/s=O(1+N/(n+m))`$, including arbitrarily large workspace budgets.
For $n=1$, the frame is a single one-qubit rotation and needs no routed cut,
regardless of the available workspace.

Therefore

```math
S_{\mathrm{routed}}(n,m)=O(2^n),
```

```math
D_{\mathrm{routed}}(n,m)
=O\left(n+\frac{2^n}{n+m}\right).
```

## 9. Matching lower bounds

Applying the frame to $\lvert0^n\rangle$ covers an open family of real normalized states
of dimension $N-1$.

### Size

A fixed topology with $G$ arbitrary one-qubit gates has only $O(G)$ continuous
real parameters.  A countable union of lower-dimensional families cannot cover
an open subset of the real-state manifold.  Hence

```math
S_{\mathbb R}(n,m)=\Omega(N).
```

### CNOT count with unrestricted clean workspace

Let $K$ be the CNOT count of an exact implementation. Its one-qubit gates may
be arbitrarily numerous and are free for this count. Only ancillary wires
participating in a CNOT can affect the system, and there are at most $2K$ such
wires. An untouched ancillary wire undergoes a one-qubit circuit that must
return its initialized state to itself, up to phase. Removing all such wires
therefore changes only a common phase, which can be absorbed into a system
one-qubit gate.

On the remaining at most $n+2K$ wires, fuse every sequence of one-qubit gates
between successive incident CNOTs. Each wire contributes one initial slot,
and each CNOT contributes at most two further slots. Thus the normalized
circuit has at most

```math
(n+2K)+2K=n+4K
```

one-qubit slots. Parameterizing each by $U(2)$ gives the deliberately loose,
workspace-independent parameter bound $4n+16K$. For a fixed CNOT topology,
the circuit output is a smooth function of these parameters. Its image cannot
cover a positive-measure subset of the $(N-1)$-dimensional real-state family
when $4n+16K\lt N-1$. The possible finite topologies form a countable set, so
allowing the topology to depend on the desired frame does not evade this
measure-zero argument. Restricting to gates that return the workspace clean
cannot increase the image dimension. Consequently the worst-case count obeys

```math
K\geq\frac{N-1-4n}{16}=\Omega(N),
```

uniformly in $m$. The existing $O(N)$ total-size construction supplies an
$O(N)$ CNOT upper bound. For the finitely many $n\geq2$ below the asymptotic
range of the displayed lower bound, a nonproduct real state requires at least
one CNOT, so the constants can be chosen uniformly for all $n\geq2$.
At $n=1$, both the real and phase-dressed frames are single-qubit unitaries
and their CNOT count is zero.

This is an application of the standard circuit-parameter method, not a new
lower-bound technique. See Iten et al., *Quantum circuits for isometries*,
[Section III and its ancillary-qubit footnote](https://arxiv.org/html/1501.06911v4#S3).
The explicit normalization above records why a large supply of initialized
wires does not supply uncharged continuous parameters to the system. The
real subfamily gives the same CNOT lower bound for the phase-dressed frame.

### Workspace-dependent depth

A depth-$`D`$ circuit on $n+m$ wires contains at most $O(D(n+m))$ parameterized
one-qubit locations, so

```math
D_{\mathbb R}(n,m)
=\Omega\left(\frac{N}{n+m}\right).
```

### Linear depth

For positive workspace, the union of the backward light cones of the $n$ system
outputs contains at most $O(n2^D)$ continuously parameterized locations.
Covering an $N-1$ dimensional output family requires

```math
D=\Omega(n).
```

At $m=0$, the parameter bound $\Omega(N/n)$ already dominates $n$
asymptotically.  Therefore

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right)
```

for every $m\geq0$.

Proposition Z, Proposition D, and Proposition R match these lower bounds and
prove the real part of the main theorem.

## 10. Phase-dressed complex magnitude frame

Write a computational label as $x=zb$, with the final bit as target.  The leaf
phase layer is

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
```

This is one total-width-$`n`$ UCG with arbitrary one-qubit unitary blocks.
Yuan–Zhang Lemma 6 gives

```math
S(D_{\mathrm{ph}})=O(N),
```

```math
D(D_{\mathrm{ph}})
=O\left(n+\frac{N}{n+m}\right).
```

Both $W_{\mathbb R}$ and $D_{\mathrm{ph}}$ return the workspace clean, so they reuse one pool
sequentially.  The real subfamily supplies the matching lower bounds.  This
proves the complex-magnitude part of the main theorem.

The leaf-phase derivatives remain a separate direct measurement stream and are
not additional columns of $W_{\mathbb C,\mathrm{mag}}$.

## 11. Exact support

| Statement | Implementation and tests |
|---|---|
| addressed frame layers | [`frames.py`](../compiler_robust_hopf/frames.py), [`test_frames.py`](../tests/test_frames.py) |
| strict-zero echo | [`strict_zero_echo.py`](../compiler_robust_hopf/strict_zero_echo.py), [`test_strict_zero_echo.py`](../tests/test_strict_zero_echo.py) |
| binary–one-hot decoder | [`tree_decoder.py`](../compiler_robust_hopf/tree_decoder.py), [`test_tree_decoder.py`](../tests/test_tree_decoder.py) |
| explicit coherent router | [`router.py`](../compiler_robust_hopf/router.py), [`test_router.py`](../tests/test_router.py) |
| resource selection and phase UCG | [`unified_compiler.py`](../compiler_robust_hopf/unified_compiler.py), [`test_unified_compiler.py`](../tests/test_unified_compiler.py) |
| exact inequalities | [`resource_bounds.py`](../compiler_robust_hopf/resource_bounds.py), [`strict_zero_audit.py`](../compiler_robust_hopf/strict_zero_audit.py) |

The elementary UCG and MCT decompositions are imported rather than regenerated
locally.  The finite tests support the operator, register, and indexing claims;
the asymptotic conclusion follows from the proof above.

---

[← Hopf interface](HOPF_INTERFACE.md) · [Complete narrative](../REVIEW.md) · [QBP consequence →](QBP_CONSEQUENCE.md)
