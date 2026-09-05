# Internal proof audit of the all-workspace compiler

## Status

This is the consolidated internal audit of the exact Hopf-frame compiler. It is
not external peer review.

The audit question is:

> Does the all-workspace theorem follow from the Hopf operator identities, the
> explicit constructions in this repository, and the exact Yuan–Zhang circuit
> primitives, without hidden workspace, unsupported executable claims, or a
> weakening of complete frame safety to state-column equality?

**Internal verdict after the peer-review revision:** no remaining operator,
workspace, size, depth, endpoint, inverse, chart-domain, router, or complex-
magnitude obstruction was found. The supported theorem is

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

## 1. Source and version discipline

The active circuit source is Yuan and Zhang, *Quantum* **7**, 956 (2023):

- Theorem 2: optimal QSP frontier;
- Lemma 5: exact ancilla-free multi-controlled X;
- Lemma 6: exact all-workspace UCG synthesis;
- Lemma 9: coherent CNOT-tree copy–uncopy;
- Theorem 1: generic controlled-state-preparation comparison.

The published article is arXiv v2. The imported statements were checked in v3
and retain the forms used here. Sun et al. remain the historical predecessor;
no active schedule selects their earlier regime theorem as a separate compiler.

The current `Hopf-QBP/main` baseline
`faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582` was reconciled explicitly. Raw-
coordinate accuracy, metric conditioning, direct phase-stream, and matched cost
boundaries have been ported into the present narrative.

Classification: **verified and recorded**.

## 2. Geometric target and singular coordinates

For unrestricted angles, the exact differential is

```math
\partial_{\theta_j}|\psi\rangle=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2,
```

where $a_j$ is the oriented incoming amplitude. The principal square root is
$\lvert a_j\rvert$. On the canonical Hopf domains, $a_j\geq0$ and therefore
$a_j=\sqrt{g_{j,j}}$.

At $g_{j,j}=0$, the raw differential vanishes. The unit vector occupying the
marker column remains a canonical orthogonal frame continuation but is not the
normalization of a nonzero derivative. The implementation and tests now encode
this distinction explicitly.

Classification: **proved and tested**.

## 3. Frame-safe logical target

The compiler must satisfy

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input. Unitarity makes the clean subspace reducing and gives
the exact inverse action. State-column equality alone is insufficient: the
closed two-qubit example preserves the state while moving the response between
marker columns and corrupting the decoded gradient.

Classification: **proved and enforced by counterexample**.

## 4. Strict-zero borrowed-suffix echo

For a nonfinal depth, fix prefix $p$, split the suffix into original bit $b$ and
remaining string $r$, and set

```math
h=[r=0],
\qquad
C=R_y(\theta_p/2),
\qquad
J=X.
```

The chronological sequence

```text
controlled_b(J), T_h, controlled_b(C), T_h,
controlled_b(J), T_h, controlled_b(C), T_h
```

uses

```math
C^2=R_y(\theta_p),
\qquad
JCJ=C^{-1},
\qquad
CJCJ=I.
```

The four $(h,b)$ sectors give the addressed rotation only on the original
complete-zero-suffix sector. The borrowed bit is restored and no relative phase
is introduced. Orthogonality of the sectors proves equality on arbitrary
superpositions and entanglement.

The two UCGs have total width $d+2$; the predicate toggles use no ancillary wire.
Thus

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right),
```

and summation gives $\Theta(N)$ size and $\Theta(n+N/n)$ depth at $m=0$.

Classification: **proved relative to Lemmas 5–6 and tested as complete
operators**.

## 5. Tree-cut identities

For a cut after $t$ depths, with $B=2^t$ and $s=n-t$,

```math
F_t^{(n)}
=W_t\otimes|0^s\rangle\!\langle0^s|
+I\otimes(I-|0^s\rangle\!\langle0^s|),
```

```math
R_t^{(n)}=\bigoplus_r W_s^{(r)}.
```

The subtree angle map is exact and the products reconstruct the complete frame.

Classification: **proved and matrix-tested**.

## 6. Binary–one-hot decoder

For $B=2^t$, the explicit decoder uses $B$ one-hot leaves, $B-1$ internal
indicators, and $B-1-t$ shared scratch wires:

```math
3B-2-t
```

clean workspace qubits in total. Its X/CNOT/Toffoli layers are disjoint, have
depth $11t-4=O(t)$, and implement

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle.
```

The one-hot Givens network equals the complete $t$-qubit Hopf frame on the code.

Classification: **explicitly constructed and tested**.

## 7. Explicit coherent router

The earlier evidence gap—resource formulas without an operator-tested
route–operate–unroute implementation—has been closed.

Treat each branch's $s$ data wires and one token as a block of width $s+1$.
At routing level $j$, prefix bit $j$ controls $2^j(s+1)$ disjoint Fredkin gates.
One original prefix control is available, so clean copies at that level number
$2^j(s+1)-1$. Hence

```math
\text{copy wires}=(B-1)(s+1)-t,
```

```math
\text{forward Fredkins}=(B-1)(s+1).
```

Balanced CNOT trees copy all prefix bits. Fredkin levels are applied least-
significant-prefix-bit first. The resulting unitary coherently moves the suffix
and root token to the prefix-selected branch on arbitrary, possibly entangled,
inputs.

Copies are uncomputed before branch operations and reused as local suffix flags.
Token-controlled subtree frames act on disjoint branch registers in parallel.
Every flag is cleared; copies are recomputed; the Fredkin tree is reversed;
copies and the root token are reset.

The implementation in `router.py` supplies the exact layers and a sparse
complex-state simulator. Tests verify basis routing, arbitrary
prefix–suffix-entangled inputs, equality to the ideal tail direct sum, equality
of the complete routed cut to the Hopf frame, and zero leakage from every work
register.

Classification: **explicitly constructed, counted, and operator-tested**.

## 8. Positive-workspace resource envelope

The routed tail uses:

- $(B-1)s$ additional data wires;
- $B$ token wires;
- $(B-1)(s+1)-t$ control-copy wires;
- $B$ branch flags when $s>1$, reusing cleared copy wires.

The tail peak is the data and tokens plus the larger of copies or flags. The
conditioned prefix and routed tail execute sequentially. Both fit inside

```math
2B(s+1).
```

Route and unroute have $O(n)$ depth and $O(B(s+1))$ size. One controlled
subtree has size $O(2^s)$ and depth $O(s^2+2^s/s)$; all branches run in
parallel.

For $m\geq4n$, the largest cut satisfying

```math
2\,2^t(n-t+1)\leq m
```

obeys $\frac{2^s}{s}=O\!\left(\frac{N}{n+m}\right)$. For $1\leq m<4n$, the direct flagged schedule's
$O(n^2)$ term is absorbed. Therefore all positive budgets attain the target
frontier.

Classification: **proved, with explicit schedule-to-ledger regression tests**.

## 9. Lower bounds

The first frame column covers an open $(N-1)$-dimensional real-state family.
Parameter counting gives $\Omega(N)$ size and $\Omega\!\left(\frac{N}{n+m}\right)$ depth. Backward
light cones of the $n$ system outputs give $\Omega(n)$ depth. At $m=0$, the
parameter bound $\Omega(N/n)$ already dominates $n$.

Classification: **proved**.

## 10. Phase-dressed complex magnitude frame

The phase diagonal is one total-width-$n$ UCG with blocks

```math
\mathrm{diag}(e^{i\phi_{z0}},e^{i\phi_{z1}}).
```

It has size $O(N)$ and depth $O\!\left(n+\frac{N}{n+m}\right)$, and reuses the real-frame work
pool sequentially. The result concerns the complex **magnitude** frame. The
leaf-phase derivatives remain a separate direct stream.

Classification: **proved relative to Lemma 6 and tested**.

## 11. Matched QBP consequence

The primary finite-shot target is simultaneous absolute raw-coordinate accuracy.
The fixed-norm magnitude records require

```math
O\left((1+\log(n/\delta))/\varepsilon_\infty^2\right)
```

executions. The scalar and gradient time comparison is defined for matched
programs using the same preparation family and controlled observable:

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E(D_{\mathrm{prep}}+D_O),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}).
```

Because $D_{\mathrm{frame}}$ matches the general QSP order, the inverse frame adds only a
constant per-execution factor. At fixed comparable accuracy and confidence, the
overhead is $O(\log n)=O(\log\log M)$. This excludes output materialization and
instance-specific scalar shortcuts.

Classification: **proved under the stated access and task conventions**.

## 12. Evidence-level boundary

The repository now distinguishes:

- complete dense logical operators for frames and strict-zero identities;
- explicit reversible layers for the decoder and router;
- exact logical block action for controlled subtree UCGs;
- imported elementary UCG/MCT synthesis;
- exact integer/rational resource ledgers.

Toffoli, Fredkin, and controlled one-qubit gates have constant-size exact
decompositions in the declared elementary model. Finite validation supports but
does not replace the analytic theorem.

## 13. Audit conclusion

The revised construction is internally coherent:

```text
strict-zero borrowed-suffix echo
+ direct positive-workspace flagged UCGs
+ self-contained one-hot decoder
+ explicit coherent route–parallel-subframes–unroute
+ Yuan–Zhang UCG/MCT/copy primitives
+ one-UCG phase dressing.
```

Independent human proof and prior-art review remain the next scientific gate.
Hardware routing, approximate fault-tolerant synthesis, noise, and
application-specific controlled-observable costs remain outside the theorem.
