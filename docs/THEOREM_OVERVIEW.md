# Theorem overview

This page gives the shortest complete route through the mathematical claims. It
separates chart geometry, compiler correctness, resource optimality, and
protocol consequences.

## Notation and circuit model

Let

```math
N=2^n
```

be the Hilbert-space dimension and let `m` be the number of available clean
ancillary qubits. The exact logical circuit model consists of arbitrary
one-qubit gates and CNOTs with all-to-all connectivity. Workspace qubits begin
and end in `|0>`.

The active external compiler framework is Yuan--Zhang, *Quantum* **7**, 956
(2023). Sun et al., *IEEE TCAD* **42**, 3301--3314 (2023), is cited as the
historical predecessor and original source credited for selected primitives.

## Theorem A: Hopf differential frame

For the balanced real Hopf chart,

```math
\partial_{\theta_j}|\psi(\boldsymbol\theta)\rangle
=\sqrt{g_{j,j}}\,|e_j(\boldsymbol\theta)\rangle,
```

where the state and normalized coordinate tangents form an orthonormal basis.
The canonical frame unitary satisfies

```math
W_{\mathbb R}|0\rangle=|\psi\rangle,
```

```math
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

For the separated complex chart,

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

This theorem is geometric. It does not depend on an elementary circuit
compiler.

## Theorem B: frame-safe substitution

A clean implementation `W_tilde` is frame-safe when

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=(W|\varphi\rangle)|0^m\rangle
```

for every system input `|varphi>`. Replacing `W` or `W^dagger` in the global
Hopf gradient protocol by a frame-safe implementation preserves the complete
measurement distribution, decoded mean, record norm, and concentration
premises.

State-column equality alone is insufficient. An explicit two-qubit compiler
preserves the prepared Hopf state but changes the decoded gradient from
`(2,0,0)` to `(0,sqrt(2),0)`.

## Lemma C: tree-cut identities

For a cut after `t` Hopf depths, write

```math
W_{\mathbb R}^{(n)}=R_t^{(n)}F_t^{(n)},
```

```math
B=2^t,
\qquad
s=n-t.
```

The prefix is

```math
F_t^{(n)}
=W_{\mathbb R}^{(t)}\otimes|0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right),
```

and the tail is

```math
R_t^{(n)}
=\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

Both are complete-operator identities.

## Lemma D: clean binary--one-hot tree decoder

There is an explicit reversible circuit `D_t` with

```math
D_t
\bigl(|x\rangle|0\rangle\bigr)
=|0^t\rangle|e_x\rangle|0\rangle,
```

using

```math
3\,2^t-2-t
```

clean ancillary qubits, depth `O(t)`, and size `O(2**t)`. It is built from
X, CNOT, and Toffoli gates arranged in explicit disjoint layers.

Using `D_t`, one suffix-zero predicate, coherent fanout of that predicate, and
`t` layers of controlled disjoint Givens rotations realizes the conditioned
prefix with depth `O(n)` and size `O(2**t+n-t)`.

## Lemma E: routed parallel tail

A coherent binary-tree router moves the existing `s`-qubit suffix and one
activation token into the branch selected by the `t`-qubit prefix. All `B`
controlled subtree frames then run on disjoint registers in parallel. Inverse
routing returns every auxiliary data, token, control-copy, and flag register to
zero.

The complete prefix and routed tail fit inside

```math
2B(s+1)
```

clean ancillary qubits. The routed construction has size `O(N)` and depth

```math
O\left(n+s^2+\frac{2^s}{s}\right).
```

## Theorem F: optimal positive-workspace real frame

For every `n>=1` and every `m>=1`, select the largest nontrivial cut satisfying

```math
2\,2^t(n-t+1)\leq m
```

when such a cut exists. Otherwise use the direct flagged-UCG schedule.

The resulting exact frame-safe compiler satisfies

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The upper bound matches Yuan--Zhang's optimal QSP frontier. The lower bound
follows because applying the frame to `|0^n>` prepares an arbitrary real state:
parameter counting gives `Omega(N)` size and `Omega(N/(n+m))` depth, while the
backward light cone of the `n` system outputs gives `Omega(n)` depth.

## Corollary G: optimal positive-workspace complex frame

The phase layer is exactly one `n`-qubit UCG:

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\operatorname{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

Yuan--Zhang's UCG theorem gives size `O(N)` and depth

```math
O\left(n+\frac{N}{n+m}\right)
```

using at most `m` clean ancillary qubits. The phase layer and real frame reuse
one workspace pool sequentially. Therefore

```math
\boxed{
S_{\mathbb C}(n,m)=\Theta(N),
\qquad
D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
}
```

for every `m>=1`.

## Corollary H: compiler-robust global Hopf backpropagation

The global magnitude estimator uses the same output distribution under every
frame-safe compiler. At fixed simultaneous coordinatewise accuracy and
confidence, its execution count is

```math
O(\log n)=O(\log\log M),
```

where `M=Theta(N)` is the number of Hopf coordinates. Because one compiled
forward or inverse frame has the same asymptotic depth as optimal state
preparation, compilation adds no asymptotic factor to this execution overhead.

The direct complex phase stream needs no inverse frame. Output-sensitive
classical decoders cost

```math
O(S_{\mathrm{mag}}N)
```

for magnitude outcomes and

```math
O(S_{\mathrm{ph}}+N)
```

for phase outcomes.

## Theorem I: checkpoint active-interface substitution

For checkpoint factorization `U=B_dA_d`, let `P_d` be the active-interface
projector and `J` append clean workspace. The sufficient compiler contract is

```math
\widetilde B_dJP_d=e^{i\chi}JB_dP_d.
```

Consistent forward and reverse use preserves every designated checkpoint
estimator mean. Equality on only the prepared prefix state is insufficient, and
active-interface equality need not preserve the complete output distribution.

## Strict zero-workspace boundary

The optimal theorem currently begins at `m=1`. At strict `m=0`, the known exact
frame compiler has

```math
S(n,0)=O(nN),
\qquad
D(n,0)=O(N).
```

With one clean ancillary qubit, the sharp positive-workspace bounds already give

```math
S(n,1)=O(N),
\qquad
D(n,1)=O(n+N/n).
```

Whether strict zero workspace can attain both sharp size and optimal depth is
open. The repository does not identify one clean qubit with zero workspace.

## Evidence classes

- **Algebraic proof:** dimension-independent operator or resource argument.
- **Imported theorem:** exact standard-circuit result from Yuan--Zhang.
- **Explicit construction:** gate/register schedule supplied in this repository.
- **Finite validation:** deterministic exact checks supplementing, not replacing,
  the proof.
- **Open boundary:** no claim of proof.
