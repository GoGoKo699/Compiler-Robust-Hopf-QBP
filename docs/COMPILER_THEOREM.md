# Complete all-workspace compiler theorem

[← Minimal Hopf interface](HOPF_INTERFACE.md) · [Read the complete narrative](../REVIEW.md) · [Next: QBP consequence →](QBP_CONSEQUENCE.md)

This page gives the complete operator and resource proof for the real and
separated complex Hopf differential frames. The proof uses one external circuit
framework—Yuan and Zhang, *Quantum* **7**, 956 (2023)—and three Hopf-specific
internal schedules covering every clean-workspace budget.

## 1. Circuit model and imported primitives

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits available to the
compiler. The circuit model is exact and logical:

- arbitrary one-qubit gates;
- CNOTs;
- all-to-all logical connectivity;
- clean ancillary qubits initialized in `|0>` and returned to `|0>`.

The proof uses the following results from Yuan and Zhang.

| Imported result | Role in this proof |
|---|---|
| Theorem 2 | optimal arbitrary-state-preparation benchmark `Theta(N)` size and `Theta(n+N/(n+m))` depth |
| Lemma 5 | exact ancilla-free multi-controlled X with linear size and depth |
| Lemma 6 | exact total-width-`q` UCG with `O(2^q)` size and `O(q+2^q/(q+w))` depth using `w` clean work qubits |
| Lemma 9 | coherent CNOT-tree copy–use–uncopy in logarithmic depth |

The earlier work of Sun, Tian, Yang, Yuan, and Zhang is the historical
predecessor and original source credited for selected primitives. The active
proof does not switch between the two state-preparation papers according to the
workspace regime.

The published results can be adapted once the complete-operator structure of
the Hopf frame is exposed. The adaptation is not direct: state preparation
fixes one initialized column, whereas the present circuit must implement a
specified unitary on every system input.

## 2. The theorem

### Theorem: optimal exact compilation of the Hopf differential frame

For every integer `n>=1` and every integer `m>=0`, the complete real Hopf
differential frame has an exact frame-safe implementation using at most `m`
clean ancillary qubits with

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(2^n)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
}
```

The separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

has the same asymptotic size, depth, and clean-workspace frontier.

The real compiler uses three internal schedules.

| Workspace regime | Schedule | Mechanism |
|---:|---|---|
| `m=0` | strict-zero echo | borrow one logical suffix bit and restore it exactly |
| small positive `m` | direct flagged UCG | store the shared suffix-zero predicate in one reusable clean flag |
| larger `m` | routed parallel subframes | cut the tree, route the suffix, and execute disjoint subtree frames in parallel |

The threshold used below is `4n`. It is chosen for a simple uniform proof; it is
not asserted to be the best finite-size crossover.

> **What should be checked here?**  The upper bound must use no more than the
> requested workspace in every regime, and every schedule must implement the
> complete frame rather than only its first column. The lower bound must apply
> to the real family being compiled, not only to generic complex states.

## 3. Local target: one addressed Hopf depth

At tree depth `d`, write a computational basis label as

```math
|p\rangle_P|x\rangle_T|z\rangle_Z,
```

where `p` is the `d`-bit prefix, `x` is the target, and `z` is the suffix of
length

```math
s=n-d-1.
```

The exact addressed layer is

```math
L_d^{(n)}
=I+
\sum_{p=0}^{2^d-1}
|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^s\rangle\!\langle0^s|.
```

The complete frame is

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_0^{(n)}.
```

All three schedules below implement these same operators. They differ only in
how the common zero-suffix condition and the parallel tree structure are
realized.

## 4. Schedule Z: strict zero workspace

### 4.1 Intuition

A direct Möttönen decomposition of the full `n`-qubit layer treats every suffix
string as a separate logical block. Although only the zero-suffix blocks are
nontrivial, the standard Walsh/Gray-code angle transformation is generically
dense. Repeating that full-width construction at every Hopf depth therefore
loses a factor of `n`.

The alternative is to keep the multiplexor small. One original suffix qubit is
used temporarily as an in-place predicate carrier. A half-angle echo cancels the
unwanted value of that qubit and restores it exactly.

<p align="center">
  <img src="../assets/strict-zero-echo.svg" width="1000" alt="Strict-zero borrowed-suffix echo circuit." />
</p>

### 4.2 Exact operator identity

Assume `d<n-1`. Split the lower suffix into one borrowed system bit `b` and the
remaining suffix `r`:

```math
|p\rangle_P|x\rangle_T|b\rangle_B|r\rangle_R.
```

Define

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_{d,p}/2).
```

Let `T_h` toggle the borrowed bit exactly when the remaining suffix is zero:

```math
T_h:
|b\rangle|r\rangle
\longmapsto
|b\oplus h(r)\rangle|r\rangle.
```

Use the chronological sequence

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

The Hopf convention is

```math
R_y(\alpha)=e^{-i\alpha Y}.
```

Therefore

```math
C_p^2=R_y(\theta_{d,p}),
```

and, because `XYX=-Y`,

```math
X C_p X=C_p^{-1}.
```

Fix `p` and `r`. The four sectors are invariant and give:

| `h(r)` | original `b` | chronological target word | resulting target matrix | final `b` |
|---:|---:|---|---|---:|
| 0 | 0 | none | `I` | 0 |
| 0 | 1 | `X,C_p,X,C_p` | `C_p X C_p X=I` | 1 |
| 1 | 0 | `C_p,C_p` | `C_p^2=R_y(theta_(d,p))` | 0 |
| 1 | 1 | `X,X` | `I` | 1 |

The chronological word `X,C_p,X,C_p` acts on column vectors as
`C_p X C_p X`, so the order in the cancellation identity is correct.

The desired rotation is applied exactly when the **original** complete suffix
is zero: `h(r)=1` and `b=0`. Every other sector receives identity. The borrowed
bit is toggled either zero or four times and is returned to its original value.
There is no sector-dependent scalar phase.

Since the prefix and remaining-suffix labels define mutually orthogonal
invariant sectors, the basis-sector calculation proves equality on arbitrary
superpositions and on inputs entangled across all system qubits. Thus the echo
is exactly `L_d^(n)` as a complete operator.

The endpoint `d=n-2` has empty `r`, so `h=1` and `T_h=X_b`. The same four-sector
proof applies. For `n=1` there is no nonfinal layer.

> **What should be checked here?**  The borrowed bit is logical data, not a
> clean ancillary target. Verify its original value is included in the desired
> predicate, that chronological and matrix order are not reversed, and that no
> branch acquires a minus sign or global phase relative to another branch.

### Executable counterpart

- [Strict-zero layer and complete frame](../compiler_robust_hopf/strict_zero_echo.py)
- [Full-sector and complete-operator tests](../tests/test_strict_zero_echo.py)
- [Exact-rational resource checks](../tests/test_strict_zero_audit.py)
- [Strict-zero resource ledger](../scripts/strict_zero_echo_ledger.py)

### 4.3 No hidden workspace

Each nonfinal layer contains:

- two controlled half-angle UCGs;
- four applications of `T_h`;
- two CNOT target echoes.

The half-angle UCG acts on:

- `d` prefix controls;
- the borrowed bit as one additional control;
- the Hopf target.

Its total width is therefore

```math
q=d+2.
```

The remaining suffix bits are not work qubits; they are controls of `T_h`.
Yuan–Zhang Lemma 5 implements this multi-controlled X without an ancillary wire.
Zero-valued controls are converted to ordinary controls by parallel X wrappers.

No wire outside the original `n`-qubit system is used.

### 4.4 Strict-zero size and depth

Yuan–Zhang Lemma 6 gives, at zero clean workspace,

```math
S_{\mathrm{UCG}}(d+2,0)=O(2^d),
```

```math
D_{\mathrm{UCG}}(d+2,0)
=O\left(d+2+\frac{2^d}{d+2}\right).
```

The four predicate toggles contribute `O(n-d)` size and depth, while the two
CNOT echoes contribute constants. Hence

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)
=O\left(n+\frac{2^d}{d+2}\right).
```

The final depth has no suffix condition and is one ordinary total-width-`n`
UCG. Summing size gives

```math
\begin{aligned}
S(W_{\mathbb R})
&=O\left(
\sum_{d=0}^{n-2}2^d
+\sum_{d=0}^{n-2}(n-d)
+2^n
\right)\\
&=O(2^n+n^2)\\
&=O(2^n).
\end{aligned}
```

For depth, put `q=d+2`. A uniform dyadic-harmonic estimate gives

```math
\sum_{q=2}^{n}\frac{2^q}{q}
\leq 6\frac{2^n}{n}.
```

One proof splits the sum at `n/2`: the early part is `O(2^(n/2))`, while every
denominator in the late part is `Omega(n)` and its numerators form a geometric
tail of total `O(2^n)`. The linear UCG-width and predicate terms sum to
`O(n^2)`, and

```math
n^2=O(2^n/n).
```

Therefore

```math
\boxed{
D(W_{\mathbb R})
=O\left(n+\frac{2^n}{n}\right).
}
```

This proves the desired upper bound at `m=0`.

## 5. Schedule P1: small positive workspace

### 5.1 Construction

Assume `m>=1`. For every nonfinal depth:

1. compute the lower-suffix-zero predicate into one clean flag;
2. apply one UCG controlled by the `d` prefix bits and the flag;
3. uncompute the flag.

The flag is returned to zero before the next depth and is reused. The final
depth has no lower suffix and is one ordinary UCG.

At a nonfinal depth, the UCG has total width `d+2`. The remaining `m-1` clean
qubits are available to the UCG compiler. At the final depth, all `m` clean
qubits are available.

The construction is frame-safe because the flag is computed from the actual
system suffix for every input, the UCG applies the exact addressed block table,
and the flag is uncomputed coherently.

### 5.2 Resources

Predicate computation and uncomputation contribute

```math
O\left(\sum_{d=0}^{n-2}(n-d-1)\right)=O(n^2)
```

size and depth.

The UCG sizes form a geometric sum and give `O(N)` total size. Their depth terms
satisfy a uniform bound of the form

```math
\sum_{d=0}^{n-2}
\frac{2^d}{d+m+1}
+
\frac{N}{n+m}
=O\left(\frac{N}{n+m}\right).
```

Thus

```math
S_{\mathrm{direct}}(n,m)=O(N),
```

```math
D_{\mathrm{direct}}(n,m)
=O\left(n^2+\frac{N}{n+m}\right).
```

For

```math
1\leq m<4n,
```

we have `n+m<5n`. Since `n^3=O(2^n)`,

```math
n^2
=O\left(\frac{2^n}{n+m}\right).
```

The direct schedule therefore already attains

```math
D_{\mathrm{direct}}(n,m)
=O\left(\frac{N}{n+m}\right)
```

throughout the small-positive-workspace regime. The linear `n` term is also
absorbed there.

> **What should be checked here?**  Confirm that one flag is included inside
> the requested budget, that the UCG receives only the remaining `m-1` work
> qubits at nonfinal depths, and that all workspace is clean again before the
> next layer.

### Executable counterpart

- [Direct schedule resource ledger](../compiler_robust_hopf/unified_compiler.py)
- [Small-workspace absorption checks](../compiler_robust_hopf/resource_bounds.py)
- [Workspace endpoint tests](../tests/test_unified_compiler.py)

## 6. Exact tree cut for larger workspace

### 6.1 Operator factorization

For a cut after the first `t` depths, define

```math
F_t^{(n)}=L_{t-1}^{(n)}\cdots L_0^{(n)},
```

```math
R_t^{(n)}=L_{n-1}^{(n)}\cdots L_t^{(n)},
```

and write

```math
B=2^t,
\qquad
s=n-t.
```

Then

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)}.
```

The prefix identity is

```math
\boxed{
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I_{2^t}\otimes\left(I-|0^s\rangle\!\langle0^s|\right).
}
```

**Proof.** Every layer above the cut has all `s` lower qubits inside its
zero-suffix predicate. On the sector `|0^s>`, those layers act exactly as the
`t`-qubit Hopf frame on the prefix. On its orthogonal complement, every such
layer is identity. Multiplying the layers preserves this direct-sum form. ∎

For each prefix `r`, let `W_s^(r)` be the complete `s`-qubit Hopf frame of the
subtree rooted at that prefix. A local node at depth `ell` and position `u`
uses the global breadth-first angle at

```math
2^{t+\ell}+r2^\ell+u.
```

The tail identity is

```math
\boxed{
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
}
```

**Proof.** Every layer below the cut preserves the first `t` qubits. Fixing one
prefix therefore selects an invariant subspace. Within that subspace, the
remaining layers have exactly the addressed form of an `s`-qubit Hopf frame,
with the angle map displayed above. The prefix sectors are orthogonal and cover
the complete Hilbert space, so the tail is their direct sum. ∎

These are complete-operator identities, not state-column decompositions.

<p align="center">
  <img src="../assets/tree-cut-routing.svg" width="1000" alt="The Hopf tree is cut into a conditioned prefix and a direct sum of subtree frames, which are coherently routed and run in parallel." />
</p>

> **What should be checked here?**  Verify the multiplication order, the exact
> global-to-local angle map, and that fixing the prefix really leaves an
> invariant suffix space. The direct sum is the structural reason parallel
> synthesis is possible.

### Executable counterpart

- [Independent prefix and tail constructions](../compiler_robust_hopf/tree_structure.py)
- [Every-cut full-frame tests](../tests/test_unified_compiler.py)

## 7. Clean binary–one-hot decoder for the conditioned prefix

The prefix operator is active only when the external suffix is zero. To execute
all `B=2^t` prefix Givens rotations in parallel, the binary prefix is converted
coherently into a one-hot code.

### 7.1 Decoder statement

There is an explicit reversible circuit `D_t` such that

```math
D_t
\bigl(|x\rangle|0\cdots0\rangle\bigr)
=
|0^t\rangle|e_x\rangle|0\cdots0\rangle
```

for every `t`-bit address `x`. It uses

```math
3B-2-t
```

clean ancillary qubits, size `O(B)`, and depth `O(t)`.

### 7.2 Construction and proof

The workspace consists of:

| Register | Qubits |
|---|---:|
| one-hot leaf register | `B` |
| internal tree indicators | `B-1` |
| shared fanout/parity pool | `B-1-t` |
| **total** | `3B-2-t` |

The reversible schedule proceeds as follows.

1. Each binary address bit is copied coherently to the number of tree nodes that
   need it, using disjoint CNOT fanout trees.
2. A root indicator is set to one.
3. At each tree depth, a parent indicator and the corresponding copied address
   bit compute the right-child indicator with a Toffoli. The parent is copied to
   the left child and the right child is subtracted from it. Exactly one child
   remains active for each input address.
4. The temporary address copies are uncomputed.
5. For each original binary bit, the parity of the active right-child indicators
   at that depth equals that bit. Parallel parity trees compute these values and
   XOR them back into the original address register, clearing it.
6. Internal indicators are cleared from their two children, leaving only the
   one-hot leaf.

Every gate is X, CNOT, or Toffoli. The supplied layer schedule has disjoint
support inside each layer. Its forward depth is `11t-4`, and its size is linear
in `B`; reversing the gate order gives the exact inverse.

On the one-hot code, one Hopf tree depth is a collection of disjoint two-mode
Givens rotations. All `2^ell` pairs at local depth `ell` can therefore run in
parallel. The resulting `t` Givens layers implement the complete `t`-qubit Hopf
frame on the code.

To obtain the conditioned prefix:

1. run the decoder;
2. compute the external `s`-qubit zero predicate;
3. fan that predicate out coherently to the simultaneous Givens controls;
4. apply the controlled Givens layers;
5. undo the fanout and predicate;
6. run the inverse decoder.

The decoder's internal and shared registers are clean after encoding and can be
reused for the live predicate copies. The complete conditioned prefix has

```math
S(F_t)=O(B+s),
```

```math
D(F_t)=O(t+s)=O(n).
```

> **What should be checked here?**  Verify the clean-input mapping and inverse
> on superpositions, the clearing of the original binary address, disjointness
> of every reported layer, the exact `3B-2-t` workspace count, and the reuse of
> decoder workspace for predicate fanout.

### Executable counterpart

- [Explicit reversible decoder and layer schedule](../compiler_robust_hopf/tree_decoder.py)
- [Decoder reversibility, disjointness, and one-hot Hopf tests](../tests/test_tree_decoder.py)

## 8. Coherent routing and parallel subtree frames

### 8.1 Router action

Allocate `B` suffix-data locations `X_r`, with the original suffix serving as
one of them, and `B` one-hot activation-token locations. A binary-tree network
of controlled swaps implements

```math
\sum_r c_r|r\rangle_P|\xi_r\rangle_X|0\rangle_{\mathrm{work}}
\longmapsto
\sum_r c_r|r\rangle_P
|\xi_r\rangle_{X_r}|1\rangle_{z_r}|0\rangle_{\mathrm{rest}}.
```

Prefix controls are copied coherently so all controlled swaps at one routing
level have disjoint support. No measurement or classical branching occurs.
After the subtree operations, the inverse router returns the transformed suffix
to the original system register and clears every branch-data, token, and copied-
control register.

### 8.2 Exact workspace ledger

With `s=n-t` and `B=2^t`, the routed tail allocates:

| Register | Clean qubits |
|---|---:|
| additional branch data | `(B-1)s` |
| activation tokens | `B` |
| copied routing controls | `(B-1)(s+1)-t` |
| simultaneous branch flags, when `s>1` | `B` |

The routing-control copies are uncomputed before the branch frames and their
clean wires are reused as branch flags. Hence the tail peak is

```math
(B-1)s+B+
\max\left\{(B-1)(s+1)-t,\;B\right\}.
```

The conditioned-prefix peak and routed-tail peak both fit inside the simple
common envelope

```math
\boxed{
2B(s+1).
}
```

Because prefix and tail are sequential, they reuse one workspace pool rather
than adding their peaks.

### 8.3 Branch compilation

Each branch applies one activation-controlled `s`-qubit Hopf frame. A direct
flagged-UCG implementation gives one controlled subtree frame with

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

All `B` branches occupy disjoint physical registers and execute in parallel.
Their total size is

```math
B\,O(2^s)=O(B2^s)=O(N),
```

while their depth is the depth of one branch.

Route and unroute have depth `O(n)` and size `O(B(s+1))`. Since

```math
s+1\leq2^s
```

for `s>=1`,

```math
B(s+1)\leq B2^s=N,
```

so routing also has `O(N)` size.

> **What should be checked here?**  Audit the action on a prefix–suffix
> entangled input, not only basis addresses. Count data, tokens, copied
> controls, and branch flags at the same physical time. Confirm that branch
> depth does not multiply by `B` because the supports are disjoint.

### Executable counterpart

- [Router and workspace ledger](../compiler_robust_hopf/unified_compiler.py)
- [Workspace and cut inequalities](../compiler_robust_hopf/resource_bounds.py)
- [Broad-grid workspace tests](../tests/test_unified_compiler.py)

## 9. Selecting the routed cut

For

```math
m\geq4n,
```

choose the largest nontrivial cut `t` satisfying

```math
\boxed{
2\,2^t(n-t+1)\leq m.
}
```

This is exactly the simple workspace envelope with `B=2^t` and `s=n-t`.
The condition `m>=4n` ensures the cut `t=1` is feasible.

If `s>1`, maximality means that the next cut is infeasible:

```math
4\,2^t s>m.
```

Therefore

```math
\frac{2^s}{s}
=
\frac{N}{2^t s}
<4\frac{N}{m}.
```

Since `m>=4n`, `n+m=Theta(m)`, so

```math
\frac{2^s}{s}
=O\left(\frac{N}{n+m}\right).
```

The remaining polynomial branch term obeys

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

For bounded `s` this is absorbed by `O(n)`; for sufficiently large `s`, the
inequality `2^s>=s^3` gives `s^2<=2^s/s`.

Combining conditioned prefix, routing, and one parallel branch layer gives

```math
D_{\mathrm{routed}}(n,m)
=O\left(n+s^2+\frac{2^s}{s}\right)
=O\left(n+\frac{N}{n+m}\right).
```

Every size contribution is `O(N)`. The `s=1` and very-large-workspace endpoints
are absorbed by the linear `n` term.

Together with Schedule P1, this proves the positive-workspace upper bound for
every `m>=1`.

## 10. Matching lower bounds

The frame's first column covers the complete real unit sphere. Applying any
valid frame compiler to `|0^n>|0^m>` therefore prepares an arbitrary real
`n`-qubit state while returning the workspace to zero.

### 10.1 Size

The real sphere has dimension `N-1`. A fixed circuit topology with `G`
arbitrary one-qubit gates has only `O(G)` continuous real parameters. Countably
many circuit families of dimension smaller than `N-1` cannot cover an open
subset of that sphere. Hence

```math
S_{\mathbb R}(n,m)=\Omega(N).
```

### 10.2 Workspace-dependent depth

A depth-`D` circuit on `n+m` wires contains at most `O(D(n+m))` one-qubit gate
locations. Parameter counting therefore gives

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

### 10.3 Linear depth

For positive workspace, consider the union of the backward light cones of the
`n` system outputs. After depth `D`, each output depends on at most `2^D` wires,
so the union contains at most `O(n2^D)` relevant wires and
`O(Dn2^D)` continuously parameterized locations. Covering an `(N-1)`-
dimensional family requires

```math
Dn2^D=\Omega(2^n),
```

which implies

```math
D=\Omega(n).
```

At strict zero workspace, the parameter bound already gives

```math
D=\Omega(N/n),
```

which asymptotically dominates `n`.

Thus, for every `m>=0`,

```math
\boxed{
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right).
}
```

Combining upper and lower bounds proves the real-frame theorem.

> **What should be checked here?**  The reduction uses only the first frame
> column, so every valid frame compiler is also a real-state-preparation
> compiler. Verify the parameter dimension, the number of available gate
> locations per depth layer, and the light-cone count for the system outputs.

### Executable counterpart

- [Integer lower-bound diagnostics](../compiler_robust_hopf/resource_bounds.py)
- [Lower-bound regression tests](../tests/test_resource_bounds.py)

## 11. Separated complex frame

For leaf phases `phi_x`, choose the final system qubit as a UCG target and write
`x=zb`. Then

```math
D_{\mathrm{ph}}
=
\sum_z |z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
```

This is one exact total-width-`n` UCG with arbitrary `U(2)` blocks. Yuan–Zhang
Lemma 6 gives

```math
S_{\mathrm{diag}}(n,m)=O(N),
```

```math
D_{\mathrm{diag}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`.

The real frame returns its workspace clean. The diagonal UCG also returns its
workspace clean. They therefore reuse the same `m`-qubit pool sequentially:

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

Size and depth add only constant asymptotic factors, while workspace takes the
maximum rather than the sum. At `m=0`, both blocks are ancilla-free. The real
subfamily supplies the matching lower bounds.

Hence

```math
\boxed{
S_{\mathbb C}(n,m)=\Theta(N),
\qquad
D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
}
```

for every integer `m>=0`.

> **What should be checked here?**  Confirm that the UCG blocks reproduce the
> complete diagonal, including common phase, and that the two blocks return the
> same workspace pool clean before it is reused.

### Executable counterpart

- [Phase UCG block construction](../compiler_robust_hopf/unified_compiler.py)
- [Complex geometry and gauge checks](../compiler_robust_hopf/complex_analysis.py)
- [One-UCG and complex-frame tests](../tests/test_unified_compiler.py)

## 12. Final conclusion

The complete real and separated complex Hopf differential frames are
asymptotically no more expensive in size or depth than preparing one arbitrary
state in the same exact circuit model:

```math
\boxed{
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(2^n),
}
```

```math
\boxed{
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right),
\qquad m\geq0.
}
```

The result depends on special Hopf structure:

- addressed zero-suffix layers;
- the borrowed-suffix echo at strict zero workspace;
- conditioned-prefix and direct-sum tree identities;
- coherent routing of complete subtree frames.

It is not a generic claim that every state-preparation circuit can be promoted
to an equally efficient complete unitary.

---

[← Minimal Hopf interface](HOPF_INTERFACE.md) · [Read the complete narrative](../REVIEW.md) · [Next: QBP consequence →](QBP_CONSEQUENCE.md)
