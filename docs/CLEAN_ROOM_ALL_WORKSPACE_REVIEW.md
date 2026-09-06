# Clean-room review of the optimal all-workspace Hopf-frame compiler

[← Verification overview](VERIFICATION.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Complete narrative](../REVIEW.md)

## Status

This document records a third internal reconstruction of the theorem from the
operator definitions and the cited elementary synthesis results. It does not
serve as external peer review or as a legal novelty opinion.

**Verdict after the peer-review revision.** No blocking operator, workspace,
size, depth, endpoint, inverse, chart-domain, router, or complex-magnitude error
was found. Under the declared exact circuit model, the reviewed construction
supports

```math
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(2^n),
```

```math
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every integer $m\geq0$.

Here $W_{\mathbb C,\mathrm{mag}}=D_{\mathrm{ph}}W_{\mathbb R}$ is the phase-dressed complex magnitude frame. The
complex leaf-phase derivatives remain a separate direct measurement stream.

The strongest remaining gate is independent human review, especially of the
strict-zero echo, the coherent router and register peak, the maximal-cut
argument, and the narrow prior-art boundary.

## 1. Review method

The reconstruction was performed in the following order.

1. Start from the complete addressed Hopf-layer operator rather than from the
   prepared state column.
2. Separate unrestricted oriented incoming amplitudes from canonical metric
   square roots and inspect singular coordinates.
3. Derive the strict-zero echo sector by sector, writing chronological and
   matrix multiplication orders separately.
4. Recount every UCG participant and every predicate-control wire.
5. Re-derive the positive-workspace tree cut and conditioned prefix.
6. Reconstruct the explicit CNOT/Fredkin router and compare its schedule with the
   live-register ledger.
7. Re-derive the maximal-cut upper bound and the real-family lower bounds.
8. Check the phase-dressed complex magnitude frame and the matched QBP
   consequence.
9. Compare the strict-zero construction with the nearest circuit-synthesis and
   borrowed-workspace literature.

Finite tests are treated as regression evidence. They are not the logical basis
of the asymptotic theorem.

## 2. Imported circuit results and exact model

The active external framework is P. Yuan and S. Zhang, *Quantum* **7**, 956
(2023), [doi:10.22331/q-2023-03-20-956](https://doi.org/10.22331/q-2023-03-20-956).
The review uses:

- arbitrary one-qubit gates and CNOTs with all-to-all logical connectivity;
- Lemma 5: exact ancilla-free multi-controlled X with linear size and depth;
- Lemma 6: a total-width-$q$ UCG using $w$ clean work qubits has size
  $O(2^q)$ and depth $`O\!\left(q+\frac{2^q}{q+w}\right)`$;
- Lemma 9: coherent CNOT-tree copying and exact uncopying;
- Theorem 2: exact state preparation has size $\Theta(2^n)$ and depth
  $`\Theta\!\left(n+\frac{2^n}{n+m}\right)`$ for every ancillary budget.

The published article corresponds to `arXiv:2202.11302v2`. The imported
statements were also checked in v3 and retain the forms used here.

Toffoli, Fredkin, controlled one-qubit gates, and the fixed-width controlled
Givens rotations used in explicit schedules each admit exact constant-size,
constant-depth decompositions into arbitrary one-qubit gates and CNOTs. Their
use as readable primitives therefore changes only constants.

The earlier Sun--Tian--Yang--Yuan--Zhang paper remains the historical
predecessor and original source credited for selected primitives. It is not a
second active compiler path.

## 3. Geometric target and singular coordinates

For unrestricted magnitude angles, let $a_j$ be the oriented incoming amplitude
to internal node $j$. Then

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

Thus the principal square root is $\sqrt{g_{j,j}}=\lvert a_j\rvert$. On the canonical Hopf
domains, all ancestor factors are nonnegative and $a_j=\sqrt{g_{j,j}}$.

At $g_{j,j}=0$, the raw differential vanishes. The unit vector occupying the
marker column remains a **chart-selected orthogonal continuation determined by
the complete parameter tuple**; it is not the normalization of a nonzero
derivative. This distinction affects interpretation, not the unitary compiler
target.

The executable interface uses a tolerance-aware regular-coordinate mask so a
floating-point representation of a chart boundary, such as $\cos(\pi/2)$, is not
mistaken for a physically regular coordinate.

**Classification:** analytic identity, canonical-domain consequence, and
boundary behavior are documented and tested.

## 4. Complete addressed layer

Let $N=2^n$. At nonfinal tree depth $d$, split a computational-basis label as

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R,
```

where $p$ is the upper prefix, $x$ the Hopf target, and $br$ the lower suffix.
The required complete layer is

```math
L_d
=I+\sum_p |p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_p)-I\bigr)
\otimes |0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

This equality fixes the action on the whole Hilbert space. Agreement only on the
forward preparation input is insufficient for the inverse-frame gradient
protocol.

## 5. Strict-zero borrowed-suffix echo

Set

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_p/2),
```

and let $T_h$ toggle the original system qubit $b$ exactly when $h(r)=1$.
Apply chronologically

```text
controlled_b(X)
T_h
controlled_b(C_p)
T_h
controlled_b(X)
T_h
controlled_b(C_p)
T_h.
```

The Hopf convention gives

```math
C_p^2=R_y(\theta_p),
\qquad
X C_p X=C_p^{-1}.
```

For fixed $p$ and $r$, the sectors are:

| $h(r)$ | original $b$ | chronological target word | resulting matrix | final $b$ |
|---:|---:|---|---|---:|
| 0 | 0 | none | $I$ | 0 |
| 0 | 1 | $X,C_p,X,C_p$ | $C_pXC_pX=I$ | 1 |
| 1 | 0 | $C_p,C_p$ | $C_p^2=R_y(\theta_p)$ | 0 |
| 1 | 1 | $X,X$ | $I$ | 1 |

The desired rotation appears only when the original complete suffix is zero.
The borrowed qubit is restored and no relative phase appears. Orthogonality of
the sectors proves the complete operator identity on arbitrary superpositions
and entangled inputs.

$T_h$ is an ancilla-free negative-control multi-controlled X whose target is the
borrowed logical wire. Each half-angle UCG contains $d$ prefix controls, the
borrowed bit, and the target, so its exact total width is

```math
q=d+2.
```

Two such UCGs and four predicate toggles give

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

The final depth is one ordinary total-width-$n$ UCG. Summation gives

```math
S_{\mathbb R}(n,0)=O(2^n),
```

```math
D_{\mathbb R}(n,0)
=O\left(n+\frac{2^n}{n}\right).
```

The real-state family supplies matching parameter-count lower bounds.

**Classification:** proved relative to Lemmas 5--6 and tested as complete
operators, including inverse and complex-magnitude composition.

## 6. Positive-workspace direct schedule

For $m\geq1$, each nonfinal addressed layer may instead compute the complete
lower-suffix-zero predicate into one clean flag, apply one prefix-and-flag UCG,
and uncompute the flag. The flag is reused between depths.

Yuan--Zhang Lemmas 5 and 6 give

```math
S_{\mathrm{direct}}=O(2^n),
```

```math
D_{\mathrm{direct}}
=O\left(n^2+\frac{2^n}{n+m}\right).
```

When $1\leq m<4n$, $n+m<5n$ and $n^3=O(2^n)$, so the polynomial term is absorbed
by $\frac{2^n}{n+m}$.

## 7. Tree-cut identities and conditioned prefix

For a cut after $t$ depths, let

```math
B=2^t,
\qquad
s=n-t,
```

and write

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)}.
```

The exact operator identities are

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes |0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right),
```

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

A local subtree node $(\ell,u)$ in branch $r$ uses the global breadth-first angle
at index

```math
2^{t+\ell}+r2^\ell+u.
```

The conditioned prefix is implemented with an explicit binary--one-hot decoder
using

```math
3B-2-t
```

clean workspace qubits, depth $O(t)$, and size $O(B)$. On the one-hot code, all
Givens pairs at one Hopf depth are disjoint. The external suffix predicate is
computed, fanned out, used by fixed-width controlled Givens rotations, and
uncomputed. The complete prefix has depth $O(n)$ and size $O(B+s)$.

**Classification:** complete-operator identities are proved; decoder layers and
encoded frame action are explicit and tested.

## 8. Explicit coherent router

The routed tail allocates $(B-1)s$ additional data wires, $B$ activation tokens,
and

```math
C=(B-1)(s+1)-t
```

copied routing controls. Treat each branch's data and token as a block of width
$s+1$.

At routing level $j$, the $j$-th prefix bit controls $2^j(s+1)$ disjoint
Fredkin gates. One original prefix wire is already available, so the number of
clean copies at that level is $2^j(s+1)-1$. Summation yields $C$, while the
forward Fredkin count is

```math
F=(B-1)(s+1).
```

Balanced CNOT trees create and later erase the prefix copies. Fredkin levels are
applied least-significant-prefix-bit first, so an arbitrary state

```math
\sum_r c_r|r\rangle_P|\xi_r\rangle_X
```

is routed coherently to the branch selected by $r$, even when prefix and suffix
are entangled.

After routing, all copies are zero. When $s>1$, the construction needs one local
suffix flag per branch. The cleared copy pool is large enough because

```math
\begin{aligned}
C-B
&=(B-1)(s+1)-t-B\\
&=(B-1)s-t-1\\
&\geq0,
\end{aligned}
```

where $B=2^t$, $t\geq1$, and $s\geq2$. Thus the branch flags reuse existing wires
rather than increasing the peak workspace.

All token-controlled subtree frames act on disjoint branch data, token, and flag
registers and therefore run in parallel. Every flag is uncomputed. Prefix copies
are then recreated, the Fredkin levels reversed, the copies erased, and the root
token reset.

The exact schedule and sparse complex-state simulator are implemented in
[`router.py`](../compiler_robust_hopf/router.py). Tests verify basis routing,
route--inverse identity on arbitrary complex inputs, equality to the ideal tail
direct sum, complete routed-cut equality, and zero leakage from data, tokens,
copies, and flags.

The tail peak is

```math
(B-1)s+B+
\max\{(B-1)(s+1)-t,\,B\},
```

and the sequential prefix/tail construction fits inside $2B(s+1)$ clean qubits.
Route and unroute have $O(n)$ depth and $O(B(s+1))$ size.

**Classification:** explicit reversible construction, exact register count, and
operator-level finite validation.

## 9. Maximal-cut argument, including $s=1$

For $m\geq4n$, choose the largest $t$ satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If $s=n-t>1$, failure of the next cut gives

```math
m<4\,2^t s.
```

Therefore

```math
\frac{2^s}{s}
=\frac{2^n}{2^t s}
<4\frac{2^n}{m}
=O\left(\frac{2^n}{n+m}\right),
```

using $m\geq4n$. Also

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

If $s=1$, every controlled subtree frame has constant depth. The conditioned
prefix and route--unroute stages have $O(n)$ depth. Feasibility of $t=n-1$
requires

```math
m\geq2\,2^{n-1}(1+1)=2^{n+1}=2N,
```

so $N/(n+m)=O(1)$ and the target depth is $\Theta(n)$. The routed schedule again
matches it.

Hence for all large-workspace endpoints,

```math
S_{\mathrm{routed}}(n,m)=O(2^n),
```

```math
D_{\mathrm{routed}}(n,m)
=O\left(n+\frac{2^n}{n+m}\right).
```

Together with the strict-zero and direct schedules, this covers every $m\geq0$.

## 10. Matching lower bounds

Applying the frame to $\lvert0^n\rangle$ prepares an open family of real normalized states
of dimension $2^n-1$.

- A fixed topology with $G$ arbitrary one-qubit gates has $O(G)$ continuous
  parameters, giving $G=\Omega(2^n)$.
- A depth-$D$ circuit on $n+m$ wires has $O(D(n+m))$ parameterized one-qubit
  locations, giving $`D=\Omega\!\left(\frac{2^n}{n+m}\right)`$.
- The union of the backward light cones of the $n$ system outputs gives the
  independent $D=\Omega(n)$ term.
- At $m=0$, $\Omega(2^n/n)$ already dominates the linear term asymptotically.

Thus the real-frame upper and lower bounds match.

## 11. Phase-dressed complex magnitude frame

Writing a basis label as $x=zb$, the full phase layer is

```math
D_{\mathrm{ph}}
=\sum_z |z\rangle\!\langle z|\otimes
\mathrm{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

This is one total-width-$n$ UCG with arbitrary $\mathrm{U}(2)$ blocks. Lemma 6 gives size
$O(2^n)$ and depth $`O\!\left(n+\frac{2^n}{n+m}\right)`$ for every $m\geq0$. Because the real frame
and phase UCG each return the pool clean, they reuse one workspace sequentially.
The real subfamily supplies the lower bounds.

This proves the theorem for $W_{\mathbb C,\mathrm{mag}}$. The direct leaf-phase record is a
separate algorithmic stream, not another set of columns in this unitary.

## 12. Matched QBP consequence

Frame safety on the clean-workspace subspace implies the exact inverse-frame
action and therefore preserves the complete global-gradient measurement
distribution.

The primary finite-shot target is simultaneous absolute accuracy of the raw
Hopf-coordinate gradient. At fixed accuracy and confidence, the magnitude
stream uses $O(\log n)=O(\log\log M)$ executions for $M=\Theta(2^n)$ coordinates.
The displayed runtime ratio compares matched scalar and gradient programs with
the same preparation family and controlled observable. Since the inverse frame
has the same general-family depth order as optimal state preparation, it adds no
extra asymptotic depth factor per execution.

This statement excludes classical output materialization and does not compare
against an instance-specialized scalar shortcut.

## 13. Prior-art boundary

The strict-zero circuit combines familiar ingredients: square-root and
conjugation identities, UCGs, borrowed or conditionally clean logical qubits,
toggle detection, and ancilla-free multi-controlled gates.

The narrow project-specific statement is the use of one original suffix data
qubit as a restored predicate carrier to aggregate one addressed Hopf depth into
two total-width-$d+2$ UCGs and linear predicate toggles, yielding the optimal
strict-zero complete-frame frontier. Absence of an exact match in the bounded
search record is not proof of novelty.

## 14. Final clean-room verdict

The reconstruction found no reason to retain an $m\geq1$ exception or to weaken
the complete-frame theorem. The internally supported result is

```math
\boxed{
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(2^n),
\qquad
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
}
```

for every integer $m\geq0$.

The router and decoder are explicit reversible constructions; frame and
strict-zero identities are checked as complete operators; UCG and
multi-controlled-X elementary synthesis are imported from Yuan--Zhang; and
resource bounds are checked by integer or exact-rational ledgers. Independent
human proof and prior-art review remain the next scientific gate.

---

[← Verification overview](VERIFICATION.md) · [Complete compiler theorem](COMPILER_THEOREM.md) · [Complete narrative](../REVIEW.md)
