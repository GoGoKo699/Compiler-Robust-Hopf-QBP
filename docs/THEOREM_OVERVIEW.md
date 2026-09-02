# Theorem overview

This page gives the shortest complete route through the mathematical claims. It
separates chart geometry, compiler correctness, all-workspace resource
optimality, and quantum-backpropagation consequences.

## Notation and circuit model

Let

```math
N=2^n
```

be the Hilbert-space dimension and let `m>=0` be the number of available clean
ancillary qubits. The exact logical circuit model consists of arbitrary
one-qubit gates and CNOTs with all-to-all connectivity. Clean workspace begins
and ends in `|0>`.

The sole active external compiler framework is Yuan--Zhang, *Quantum* **7**,
956 (2023). Sun et al., *IEEE TCAD* **42**, 3301--3314 (2023), are cited as the
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

This statement is geometric and independent of an elementary compiler.

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

State-column equality alone is insufficient. An exact two-qubit compiler
preserves the Hopf state but changes the decoded gradient from `(2,0,0)` to
`(0,sqrt(2),0)`.

## Lemma C: strict-zero borrowed-suffix echo

Fix a nonfinal addressed depth `d<n-1`. Split the lower suffix into one original
system qubit `b` and the remaining suffix `r`. Let

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_p/2),
```

where `p` is the `d`-bit tree prefix. Let `T_h` toggle `b` exactly when
`h(r)=1`. The chronological sequence

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

implements the addressed Hopf layer exactly and restores `b` on every input.
The proof is the four-sector identity

```math
C_p^2=R_y(\theta_p),
\qquad
X C_p X=C_p^{-1},
\qquad
C_pXC_pX=I.
```

The construction uses no ancillary wire. Each nonfinal layer contains two
zero-ancilla UCGs of total width `d+2`, four zero-ancilla predicate toggles, and
two CNOT echoes.

## Theorem D: optimal strict-zero frame

Summing the echo layers and compiling the final depth as one ordinary
`n`-qubit UCG gives

```math
S_{\mathbb R}(n,0)=\Theta(N),
```

```math
D_{\mathbb R}(n,0)
=\Theta\left(n+\frac{N}{n}\right).
```

The upper bound uses Yuan--Zhang Lemmas 5 and 6:

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right).
```

The sums satisfy

```math
\sum_{d=0}^{n-2}2^d=O(N),
```

```math
\sum_{d=0}^{n-2}\frac{2^d}{d+2}=O(N/n),
```

and `n**2=O(N/n)`. The matching size and depth lower bounds follow from the
`N-1` dimensional real-state family and parameter counting on exactly `n`
wires.

## Lemma E: tree-cut identities

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

## Lemma F: clean binary--one-hot tree decoder

There is an explicit reversible circuit `D_t` satisfying

```math
D_t
\bigl(|x\rangle|0\rangle\bigr)
=|0^t\rangle|e_x\rangle|0\rangle,
```

using

```math
3\,2^t-2-t
```

clean ancillary qubits, depth `O(t)`, and size `O(2**t)`. It is built from X,
CNOT, and Toffoli gates arranged in explicit disjoint layers.

Using `D_t`, one suffix-zero predicate, coherent predicate fanout, and `t`
layers of controlled disjoint Givens rotations realizes the conditioned prefix
with depth `O(n)` and size `O(2**t+n-t)`.

## Lemma G: routed parallel tail

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

## Theorem H: optimal positive-workspace frame

For every `m>=1`, use the direct flagged-UCG schedule when no useful routed cut
fits. Otherwise choose the largest nontrivial cut satisfying

```math
2\,2^t(n-t+1)\leq m.
```

The resulting exact frame-safe real compiler satisfies

```math
S_{\mathbb R}(n,m)=\Theta(N)
```

and

```math
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
```

For `1<=m<4n`, the direct schedule's `O(n**2)` term is absorbed by the
state-preparation scale. For larger `m`, maximality of the routed cut gives the
required bound on `2**s/s`.

The lower bound follows because the frame prepares every real state: parameter
counting gives `Omega(N)` size and `Omega(N/(n+m))` depth, while the backward
light cone of the `n` system outputs gives `Omega(n)` depth.

## Theorem I: optimal all-workspace real frame

Combining Theorems D and H gives, for every integer `m>=0`,

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

The schedule is selected internally:

- `m=0`: borrowed-suffix echo;
- small positive `m`: direct flagged UCGs;
- larger `m`: tree-decoder routed subframes.

## Corollary J: optimal all-workspace complex frame

The phase layer is exactly one `n`-qubit UCG:

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\operatorname{diag}\left(e^{i\phi_{z0}},e^{i\phi_{z1}}\right).
```

Yuan--Zhang Lemma 6 gives size `O(N)` and depth

```math
O\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`. It reuses the real-frame workspace pool sequentially.
Therefore

```math
\boxed{
S_{\mathbb C}(n,m)=\Theta(N),
\qquad
D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
}
```

for every integer `m>=0`.

## Corollary K: compiler-robust global Hopf backpropagation

The global magnitude estimator uses the same output distribution under every
frame-safe compiler. At fixed simultaneous coordinatewise accuracy and
confidence, its execution count is

```math
O(\log n)=O(\log\log M),
```

where `M=Theta(N)` is the number of Hopf coordinates. Because one compiled
forward or inverse frame matches the optimal state-preparation depth for every
ancillary budget, compilation adds no asymptotic factor to this execution
overhead.

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

## Theorem L: checkpoint active-interface substitution

For checkpoint factorization `U=B_dA_d`, let `P_d` be the active-interface
projector and `J` append clean workspace. The sufficient compiler contract is

```math
\widetilde B_dJP_d=e^{i\chi}JB_dP_d.
```

Consistent forward and reverse use preserves every designated checkpoint
estimator mean. Equality on only the prepared prefix state is insufficient, and
active-interface equality need not preserve the complete output distribution.

## Evidence classes

- **Algebraic proof:** dimension-independent operator or resource argument.
- **Explicit construction:** gate/register schedule supplied here.
- **Imported theorem:** exact standard-circuit result from Yuan--Zhang.
- **Finite validation:** deterministic checks supplementing, not replacing, the
  proof.
- **Internal audit:** independent re-derivation within this project, not external
  peer review.
- **Prior-art boundary:** the abstract echo ingredients have antecedents; the
  Hopf-specific aggregation and optimal complete-frame consequence are the
  claimed project contribution.
