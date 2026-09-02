# Strict-zero workspace through the Möttönen completion

## Status

This is a focused research branch, not part of the positive-workspace theorem in
PR #14. The exact operator identities and finite tests are complete. The new
strict-zero **size** conclusion is proved relative to standard exact
no-workspace decompositions of multi-controlled one-qubit gates. The optimal
strict-zero **depth** remains open.

Let

```math
N=2^n.
```

The main conclusion of this exploration is

```math
\boxed{
S_{\mathbb R}(n,0)=\Theta(N)
}
```

with a constructive upper bound, while the best depth established here is still

```math
D_{\mathbb R}(n,0)=O(N).
```

The unresolved target is

```math
D_{\mathbb R}(n,0)
=O\left(n+\frac{N}{n}\right).
```

Thus the clean flag is no longer needed for asymptotically sharp gate count; it
is still the missing resource in the known optimal-depth schedule.

## 1. Two frame layers

For depth `d`, let

```math
s=n-d-1.
```

Write `p` for the `d`-bit upper prefix, `b` for the target bit, and `z` for the
`s`-bit lower suffix.

The ordinary Möttönen preparation layer is

```math
P_d
=\sum_{p,z}|p,z\rangle\!\langle p,z|
\otimes R_y(\theta_{d,p}),
```

with tensor factors reordered so that the rotation acts on `b`. The selected
angle depends on `p` but not on `z`.

The addressed Hopf-frame layer is

```math
A_d
=I+
\sum_p |p\rangle\!\langle p|
\otimes\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes|0^s\rangle\!\langle0^s|.
```

Equivalently, let `V_d` be the complete `(d+1)`-qubit Möttönen UCR on the prefix
and target. Then

```math
\boxed{
A_d
=V_d\otimes|0^s\rangle\!\langle0^s|
+I_{2^{d+1}}\otimes
 \left(I-|0^s\rangle\!\langle0^s|\right).
}
```

This is a full-operator identity, not only a state-column identity. The branch
constructs both matrices independently and tests every depth through `n=8`.

## 2. Ancilla-free linear-size construction

A standard Möttönen/Gray-code decomposition of `V_d` contains `O(2**d)`
elementary `R_y` and CNOT gates.

To implement `A_d` without an ancillary qubit:

1. conjugate the `s` suffix controls by `X`, so the zero-suffix condition becomes
   an all-positive condition;
2. attach those same `s` controls to every elementary gate in the circuit for
   `V_d`;
3. undo the `X` conjugations.

This is exact because controlling a product gate by gate gives

```math
\Lambda(V_d)
=\Lambda(G_L)\cdots\Lambda(G_1)
```

whenever `V_d=G_L\cdots G_1` and every factor uses the same external control
projector.

The controlled local rotations are exact multi-controlled `SU(2)` gates. The
controlled CNOTs are multi-controlled `X` gates. Exact ancilla-free
constructions have polynomial overhead in the number of external controls; the
classical Barenco construction already gives a conservative quadratic overhead.
Therefore

```math
S(A_d)
=O\left(2^d(s+1)^2+s\right).
```

Summing over all depths gives

```math
\begin{aligned}
S(W_{\mathbb R})
&=O\left(
 \sum_{d=0}^{n-1}2^d(n-d)^2+n^2
 \right)\\
&=O\left(
 N\sum_{r=1}^{n}\frac{r^2}{2^r}+n^2
 \right)\\
&=O(N),
\end{aligned}
```

because

```math
\sum_{r=1}^{\infty}\frac{r^2}{2^r}=6.
```

The repository also records the available linear-control-overhead proxy, for
which

```math
\sum_{d=0}^{n-1}2^d(n-d)
=2N-n-2.
```

The quadratic argument is retained because it is already sufficient for the
asymptotic theorem.

Since applying the frame to `|0^n>` prepares an arbitrary real normalized state,
the existing parameter-count lower bound gives `S_R(n,0)=Omega(N)`. Hence the
strict-zero size is asymptotically optimal.

## 3. Exact completion-correction identity

The Möttönen compiler also reveals the exact difference between state
preparation and the complete Hopf frame.

Define

```math
U_n=P_{n-1}\cdots P_0,
\qquad
W_n=A_{n-1}\cdots A_0.
```

For `0<=k<n`, define the rightmost-one stratum

```math
\mathcal H_k
=\operatorname{span}
\left\{
 |p\rangle_{0,\ldots,k-1}
 |1\rangle_k
 |0^{n-k-1}\rangle:
 p\in\{0,1\}^k
\right\}.
```

Also let `H_empty=span{|0^n>}`. These mutually orthogonal spaces partition the
computational basis.

Let `U_k` denote the `k`-qubit Möttönen completion formed from the first
`2**k-1` Hopf angles, with `U_0=I`. Define `C_n` by

```math
C_n|_{\mathcal H_\emptyset}=I,
\qquad
C_n|_{\mathcal H_k}=U_k^\dagger.
```

Then

```math
\boxed{
W_n=U_nC_n,
}
```

or, after grouping the one-dimensional initial sectors,

```math
\boxed{
C_n\cong
I_2\oplus U_1^\dagger\oplus U_2^\dagger
\oplus\cdots\oplus U_{n-1}^\dagger.
}
```

### Proof

Take a basis state in `H_k`. The layers `A_d` with `d<k` are inactive because
their lower suffix contains the delimiter bit `1`. Starting at depth `k`, all
bits below the current target are zero, so each addressed layer agrees with the
corresponding full preparation layer on the evolving state. Hence

```math
W_n|_{\mathcal H_k}
=P_{n-1}\cdots P_k|_{\mathcal H_k}.
```

On the other hand,

```math
U_nU_k^\dagger
=P_{n-1}\cdots P_k
```

on this stratum, because the first `k` preparation layers cancel their inverse
prefix completion. The all-zero state is prepared identically by `U_n` and
`W_n`. Linear extension over the orthogonal strata proves the identity.

The implementation checks the identity through `n=8` with random angles. It
also verifies the equivalent correction-layer product

```math
C_n=B_0B_1\cdots B_{n-1},
\qquad
B_d=P_d^\dagger A_d.
```

Here `B_d` is the identity on a zero lower suffix and applies `P_d^dagger` on a
nonzero lower suffix.

## 4. A second linear-size proof

The direct-sum correction gives an independent strict-zero size construction.
On `H_k`, implement `U_k^dagger` by controlling every elementary gate of its
`O(2**k)` Möttönen circuit on the pattern

```text
bit k = 1, bits k+1,...,n-1 = 0.
```

There are `n-k` external controls. With conservative quadratic
no-workspace control overhead,

```math
S(C_n)
=O\left(
 \sum_{k=1}^{n-1}2^k(n-k+1)^2
 \right)
=O(N).
```

The strata are mutually orthogonal, so these controlled blocks implement the
direct sum exactly. Since `S(U_n)=O(N)`, the identity `W_n=U_nC_n` again gives
`S(W_n)=O(N)`.

This factorization is less direct than Section 2 but exposes the correction that
a state-column compiler omits.

## 5. Why ordinary zero-padding does not exploit the sparsity

One could instead regard `A_d` as a full-width `R_y` UCR with identity blocks on
all nonzero suffixes. This is exact but gives `O(N)` size per depth.

The logical angle function is

```math
\alpha(p,z)=\theta_p\,\delta_{z,0^s}.
```

Its Walsh transform factorizes as

```math
\widehat\alpha(u,v)
=\sum_p(-1)^{u\cdot p}\theta_p,
```

which is independent of the suffix frequency `v`. For generic Hopf angles it is
therefore nonzero for every `v`. The sparse logical block table becomes dense in
the standard Möttönen frequency-angle representation.

Thus simply inserting zero angles into the inactive logical blocks and pruning
the standard Gray-code circuit does not produce the linear-size result. The
construction in Section 2 groups the repeated suffix condition before applying
an exact no-workspace controlled-gate decomposition.

## 6. Remaining depth bottleneck

The gate-by-gate controlled construction has the sequential upper bound

```math
D(W_{\mathbb R})=O(N).
```

It does not preserve the `O(2**d/d)` parallel depth of an unconstrained UCR,
because all controlled elementary gates at depth `d` repeatedly depend on the
same `s` suffix qubits. With one clean flag, this nonlinear predicate is computed
once and its value can be used by the Yuan--Zhang UCG schedule. At strict zero
workspace, the known construction re-evaluates or propagates the condition
through the controlled gates.

The precise missing lemma is therefore:

> Compile a suffix-zero-conditioned `d`-control `R_y` UCR with no ancillary
> qubits, size `O(2**d poly(n-d))`, and depth low enough that the sum over all
> Hopf depths is `O(n+N/n)`.

The parameter count does not rule this out. The existing lower bound is only

```math
\Omega\left(n+\frac{N}{n}\right),
```

which matches the desired target rather than the current `O(N)` schedule.

## 7. Routes worth pursuing

### Shared-control parallelization

A depth-optimal UCR distributes its phase/rotation work across the register.
The open problem is to retain that parallelism while imposing the common
suffix-zero condition without a stored flag.

### Conditionally clean system qubits

On the active branch, the trailing suffix qubits are known zeros. Techniques
based on conditionally clean or dirty workspace may permit temporary predicate
storage while restoring every system qubit. A valid construction must still act
correctly on arbitrary superpositions and return every borrowed qubit exactly.

### Completion-correction fusion

The direct sum

```math
I_2\oplus U_1^\dagger\oplus\cdots\oplus U_{n-1}^\dagger
```

may admit a global synthesis that shares Gray-code traversals across strata or
absorbs the correction into the preparation completion. Implementing the blocks
separately proves optimal size but not optimal depth.

### Restricted-UCG methods

Recent restricted-UCG work gives ancilla-free linear-size decompositions and
optimal depth for commuting rotation/diagonal families. Its `k`-sparsity notion
concerns the weight of frequency-domain control states. The suffix projector
above has generic support on all suffix frequencies, so those theorems do not
directly close this endpoint. They may nevertheless supply components for a
custom shared-control construction.

## 8. Executable support

```text
compiler_robust_hopf/strict_zero_mottonen.py
tests/test_strict_zero_mottonen.py
scripts/strict_zero_mottonen_ledger.py
```

Run

```bash
python -m unittest -v tests.test_strict_zero_mottonen
python scripts/strict_zero_mottonen_ledger.py --nmax 24
```

The tests verify:

- the complete conditioned-layer identity;
- equality of the Möttönen and Hopf state columns;
- the rightmost-one partition;
- `W_n=U_nC_n` through `n=8`;
- the explicit correction blocks;
- the correction-layer product; and
- exact integer bounds for the weighted resource sums through `n=256`.

## 9. References

- M. Möttönen, J. J. Vartiainen, V. Bergholm, and M. M. Salomaa,
  [Transformation of quantum states using uniformly controlled rotations](https://arxiv.org/abs/quant-ph/0407010),
  *Quantum Information and Computation* **5**, 467--473 (2005).
- V. Bergholm, J. J. Vartiainen, M. Möttönen, and M. M. Salomaa,
  [Quantum circuits with uniformly controlled one-qubit gates](https://arxiv.org/abs/quant-ph/0410066),
  *Physical Review A* **71**, 052330 (2005).
- A. Barenco et al.,
  [Elementary gates for quantum computation](https://arxiv.org/abs/quant-ph/9503016),
  *Physical Review A* **52**, 3457--3467 (1995).
- R. Vale et al.,
  [Decomposition of multi-controlled special-unitary single-qubit gates](https://arxiv.org/abs/2302.06377),
  *IEEE Transactions on Computer-Aided Design of Integrated Circuits and
  Systems* **43**, 1528--1539 (2024).
- T. Khattar and C. Gidney,
  [Rise of conditionally clean ancillae for efficient quantum circuit constructions](https://arxiv.org/abs/2407.17966),
  *Quantum* **9**, 1752 (2025).
- C. Xu, X. Chen, X. Li, Z. Liu, and Z. Li,
  [A unified framework for optimizing uniformly controlled structures in quantum circuits](https://arxiv.org/abs/2512.08675),
  arXiv:2512.08675 (2025).
