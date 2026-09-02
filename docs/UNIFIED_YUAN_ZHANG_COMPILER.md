# Unified Yuan--Zhang compiler for Hopf differential frames

## Status

This document gives the active compiler architecture of the project. It replaces
the earlier regime-by-regime presentation and removes the construction-level
dependency on the previous unary-to-binary compiler.

The sole external compiler framework and state-preparation benchmark used in the
active proof is:

P. Yuan and S. Zhang, "Optimal (controlled) quantum state preparation and
improved unitary synthesis by quantum circuits with any number of ancillary
qubits," *Quantum* **7**, 956 (2023),
[PDF](https://quantum-journal.org/papers/q-2023-03-20-956/pdf/).

The earlier work of Sun, Tian, Yang, Yuan, and Zhang remains cited as the
historical predecessor and as the original source credited by Yuan--Zhang for
selected primitives. It is not a second active compiler path.

The construction below is exact in the all-to-all standard circuit model of
arbitrary one-qubit gates and CNOTs. Every workspace statement refers to clean
ancillary qubits that are returned to zero.

## 1. Result

Let

```math
N=2^n.
```

For every integer `m>=1`, the complete real Hopf differential frame has an exact
frame-safe implementation using at most `m` clean ancillary qubits with

```math
S_{\mathbb R}(n,m)=\Theta(N)
```

and

```math
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

The separated complex frame

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}
```

has the same positive-workspace size and depth profile. This matches the
optimal arbitrary-state-preparation frontier in Yuan--Zhang Theorem 2.

The strict `m=0` endpoint remains separate. The current exact fallback has size
`O(nN)` and depth `O(N)`. One clean ancillary qubit is sufficient for size
`O(N)` and depth `O(n+N/n)`.

## 2. Yuan--Zhang results used

The active proof uses the following statements from the 2023 paper.

| Result | Role in this project |
|---|---|
| Standard circuit model in Section 2 | Arbitrary one-qubit gates, CNOTs, clean ancillary qubits, all-to-all logical connectivity |
| Lemma 5 | Exact ancilla-free multi-controlled X with linear size and depth |
| Lemma 6 | Exact `q`-qubit uniformly controlled gate with size `O(2**q)` and depth `O(q+2**q/(q+w))` using `w` ancillary qubits |
| Lemma 9 | Coherent CNOT-tree copy--use--uncopy in logarithmic depth |
| Theorem 1 | Generic controlled-state-preparation size, used to explain why treating all frame columns independently costs `O(N**2)` |
| Theorem 2 | Optimal state-preparation size and depth for every ancillary budget |

Figure 1 in that paper concerns general unitary synthesis. The state-preparation
frontier used here is Theorem 2.

## 3. Exact Hopf tree factorization

Write the addressed real frame as

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_0^{(n)}.
```

For a cut after the first `t` tree depths, define

```math
F_t^{(n)}=L_{t-1}^{(n)}\cdots L_0^{(n)},
```

```math
R_t^{(n)}=L_{n-1}^{(n)}\cdots L_t^{(n)}.
```

Put

```math
B=2^t,
\qquad
s=n-t.
```

The prefix and tail obey two complete-operator identities.

### Conditioned prefix

Let

```math
P_s=|0^s\rangle\!\langle0^s|.
```

Then

```math
\boxed{
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes P_s
+I_{2^t}\otimes(I-P_s).
}
```

Thus the first `t` Hopf depths form a `t`-qubit frame conditioned on the
external suffix being zero.

### Tail direct sum

For each prefix `r` of length `t`, define the local `s`-qubit subtree frame
`W_s^(r)` by assigning local node `(ell,u)` the global breadth-first angle at
node

```math
2^{t+\ell}+r2^\ell+u.
```

Then

```math
\boxed{
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
}
```

The repository constructs both sides independently and checks every cut through
`n=8`. The algebraic proof follows because every addressed rotation below the
cut preserves the first `t` computational bits and reduces inside each prefix
block to the corresponding local addressed rotation.

## 4. Self-contained binary--one-hot tree decoder

The active prefix compiler uses a new reversible tree decoder rather than an
imported unary-to-binary routine.

### Registers

For `B=2**t`, allocate:

- the existing `t`-qubit binary prefix register `A`;
- a clean `B`-qubit one-hot leaf register `U`;
- `B-1` clean internal-tree indicator qubits `I`;
- `B-1-t` clean scratch qubits `R`.

The clean workspace is therefore

```math
\boxed{
B+(B-1)+(B-1-t)=3B-2-t.
}
```

### Decoder identity

The reversible circuit `D_t` satisfies

```math
\boxed{
D_t
\bigl(|x\rangle_A|0\rangle_{UIR}\bigr)
=|0^t\rangle_A|e_x\rangle_U|0\rangle_{IR}
}
```

for every `t`-bit string `x`. Here `|e_x>` is the one-hot basis state with the
single excitation at leaf `x`.

### Construction

1. **Copy the address controls.** At tree depth `d`, copy binary bit `x_d` to
   `2**d` coherent controls, counting the original. All address bits use
   disjoint scratch pools and are copied concurrently by CNOT trees.
2. **Build path indicators.** Set the root indicator to one. For every active
   parent `p` and copied address bit `a`, compute

   ```math
   \mathrm{left}=p(1-a),
   \qquad
   \mathrm{right}=pa
   ```

   using one CNOT, one Toffoli, and one CNOT. All nodes at one depth are
   disjoint. The leaves become the one-hot register.
3. **Uncopy the address controls.** The copied controls were never targets of
   the path gates, so inverse CNOT trees return them to zero.
4. **Erase the original binary address.** At depth `d`, the bit `x_d` equals the
   parity of all right-child indicators at that depth. Compute these parities by
   balanced CNOT trees in the shared scratch pool, XOR them into `A`, and
   uncompute the parity trees.
5. **Erase internal indicators.** Working from the leaves upward, clear every
   parent with CNOTs from its two children. Exactly one child of an active parent
   is one, so their XOR equals the parent indicator.

All gates are fixed-width reversible gates. A Toffoli is the two-control case of
Yuan--Zhang Lemma 5 and has constant exact cost in the declared gate model.
The decoder has depth `O(t)` and size `O(B)`. Reversing it gives the exact
one-hot-to-binary decoder.

The tests verify the clean-subspace identity, inverse recovery, and full basis
permutation reversibility. The one-hot Givens network is independently checked
against the complete `t`-qubit Hopf frame.

## 5. Conditioned prefix compiler

Apply the following clean sequence.

1. Run `D_t` on the prefix register.
2. If `s>0`, compute the predicate `[suffix=0]` into one clean internal/scratch
   wire using Lemma 5.
3. Copy that predicate to enough controls for the widest Givens layer using
   Lemma 9.
4. Apply the `t` Hopf tree depths as controlled disjoint two-mode Givens gates
   on the one-hot register.
5. Uncopy and uncompute the suffix predicate.
6. Apply `D_t^dagger`.

When the suffix is zero, the one-hot code undergoes the complete frame
`W_R^(t)`. Otherwise the Givens network is inactive and the decoder round trip
is the identity. This realizes the conditioned-prefix operator in Section 3 on
every system input.

The decoder's internal and shared scratch registers are clean after step 1 and
are reused for the predicate and its copied controls. No extra register is added
to the peak count. The complete prefix has

```math
S_{\mathrm{prefix}}=O(B+s),
```

```math
D_{\mathrm{prefix}}=O(n),
```

and uses at most `3B-2-t` clean ancillary qubits.

## 6. Direct low-workspace compiler

When no useful routed cut fits, compile each addressed depth directly.

For a nonfinal depth `d`:

1. compute the lower-suffix-zero predicate into one reusable clean flag;
2. apply one UCG with the `d` upper-prefix bits and the flag as controls;
3. uncompute the flag.

The UCG has width `d+2`; it receives the remaining `m-1` work qubits. The final
depth has no suffix predicate and uses one `n`-qubit UCG with all `m` work
qubits.

Lemmas 5 and 6 give

```math
S_{\mathrm{direct}}=O(N),
```

```math
D_{\mathrm{direct}}
=O\left(n^2+\frac{N}{n+m}\right).
```

For `1<=m<4n`, the sequence `n**3/2**n` is uniformly bounded and
`n+m<5n`, so

```math
n^2=O\left(\frac{N}{n+m}\right).
```

The direct compiler therefore already has optimal-order depth throughout the
small-positive-workspace range.

At strict `m=0`, synthesize every addressed layer as one full-width UCG with
zero blocks on inactive suffix sectors. This exact fallback has size `O(nN)`
and depth `O(N)`.

## 7. Routed parallel-subframe compiler

For larger workspace, coherently route the existing suffix register into one of
`B` disjoint branch registers selected by the prefix.

Allocate:

```math
(B-1)s
```

additional data qubits,

```math
B
```

activation-token qubits, and

```math
(B-1)(s+1)-t
```

copied routing controls. The copies are uncomputed before the subtree frames and
are reused as one simultaneous suffix flag per branch when `s>1`.

The exact routed-tail peak is

```math
(B-1)s+B+
\max\left\{(B-1)(s+1)-t,\,B\mathbf1_{s>1}\right\}.
```

Both the routed tail and the conditioned prefix fit inside the convenient
common envelope

```math
\boxed{
2B(s+1).
}
```

The router consists of `t` levels of controlled swaps. Coherent copies of all
prefix controls are made concurrently, the Fredkin gates at one level use
disjoint targets, and all copies are uncomputed. Route and unroute have depth
`O(n)` and size `O(B(s+1))`.

After routing, all `B` controlled subtree frames act on disjoint registers. One
controlled `s`-qubit subtree frame is compiled directly with one branch flag,
zero UCG workspace, and the activation token as an additional UCG control. It
has

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

All branches run in parallel, giving total branch size

```math
B\,O(2^s)=O(N)
```

without multiplying the branch depth. Inverse routing returns the transformed
suffix to the original system register and resets every auxiliary data, token,
copy, and flag qubit.

## 8. Cut selection and optimal upper bound

For `m>=4n`, choose the largest `t` with `1<=t<n` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

With `B=2**t` and `s=n-t`, if `s>1`, maximality gives

```math
m<4Bs.
```

Therefore

```math
\frac{2^s}{s}
=\frac{N}{Bs}
<4\frac{N}{m}
=O\left(\frac{N}{n+m}\right).
```

Also

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

The conditioned prefix and routing contribute only `O(n)` depth. Hence

```math
D_{\mathrm{routed}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

and

```math
S_{\mathrm{routed}}(n,m)=O(N).
```

Combining this with the direct low-workspace schedule proves the upper bound for
every `m>=1`.

## 9. Matching lower bounds

Applying the frame to `|0^n>` prepares every real normalized `n`-qubit state.
That family has dimension `N-1`.

A circuit with `G` arbitrary one-qubit gates has at most `4G` continuous real
parameters, while CNOTs carry no continuous parameters. Therefore

```math
S_{\mathbb R}(n,m)=\Omega(N).
```

A depth-`D` circuit on `n+m` wires has at most `D(n+m)` one-qubit-gate locations,
which gives

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

For the independent linear term, trace the backward light cone of the `n`
system outputs. At distance `j` it contains at most `n2**j` wires. The total
number of relevant continuous parameters in depth `D` is therefore less than

```math
4n2^D.
```

Covering an `(N-1)`-dimensional real family requires

```math
4n2^D\geq N-1,
```

and hence `D=Omega(n)`. Together these bounds give

```math
D_{\mathbb R}(n,m)
=\Omega\left(n+\frac{N}{n+m}\right).
```

The upper and lower bounds match for every `m>=1`.

## 10. Complex frame as one additional UCG

For leaf phases `phi_x`, choose the last system qubit as a UCG target and write
`x=zb`, with `z` the `n-1` control bits and `b` the target bit. Then

```math
\boxed{
D_{\mathrm{ph}}
=\sum_z |z\rangle\!\langle z|
\otimes
\begin{pmatrix}
e^{i\phi_{z0}}&0\\
0&e^{i\phi_{z1}}
\end{pmatrix}.
}
```

This is exactly one `n`-qubit UCG in the sense of Yuan--Zhang Lemma 6. It has

```math
S_{\mathrm{diag}}(n,m)=O(N),
```

```math
D_{\mathrm{diag}}(n,m)
=O\left(n+\frac{N}{n+m}\right)
```

using at most `m` clean ancillary qubits. The blocks are arbitrary `U(2)`
matrices, so the complete diagonal, including its common phase, is represented
without a separate correction gate or phase-polynomial transform.

The real frame and diagonal are sequential clean operators. They reuse the same
workspace pool, so the separated complex frame has the same asymptotic size,
depth, and workspace profile.

## 11. Compiler boundary

The theorem concerns a frame-safe implementation:

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input. It is not enough to compile only

```math
\widetilde W|0^n\rangle=W|0^n\rangle.
```

The repository contains exact two-qubit counterexamples showing that state-column
equality can corrupt both global and checkpoint gradient decoders.

## 12. Evidence boundary

The active implementation contains:

- independent exact matrices for every Hopf tree factor;
- an explicit reversible gate list for the binary--one-hot decoder;
- exact basis-state and inverse checks of that decoder;
- exact one-hot-code action checks;
- exact one-UCG phase-diagonal checks;
- routed workspace and resource ledgers;
- deterministic broad-grid integer diagnostics.

Finite tests support the construction but do not replace the dimension-independent
proof. The UCG, multi-controlled-X, and coherent-copy resource statements are
imported from Yuan--Zhang under their stated circuit model.

The result does not currently cover:

- simultaneous sharp size and optimal depth at strict `m=0`;
- routed hardware connectivity;
- approximate Clifford+T synthesis;
- noise robustness;
- arbitrary coordinate charts; or
- external peer review.
