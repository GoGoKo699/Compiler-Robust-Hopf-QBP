# Optimal all-ancilla target: current resolution and remaining endpoint

## 1. Benchmark

Let

```math
N=2^n.
```

Yuan and Zhang proved that arbitrary `n`-qubit state preparation with `m`
clean ancillary qubits has optimal size and depth

```math
S_{\mathrm{QSP}}(n,m)=\Theta(N),
```

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every `m>=0`. The relevant statement is Theorem 2 of their 2023
*Quantum* paper. Figure 1 of that paper concerns general unitary synthesis.

## 2. Positive-workspace problem: internally resolved

For every `m>=1`, the complete real Hopf differential frame now has an
internally audited exact frame-safe implementation using at most `m` clean
ancillary qubits, with

```math
\boxed{
S_{\mathbb R}(n,m)=\Theta(N),
\qquad
D_{\mathbb R}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The separated complex frame inherits the same size and depth profile under the
same clean workspace budget.

The construction and independent audit are in:

```text
docs/OPTIMALITY_CHECKPOINT_1.md
docs/OPTIMALITY_AUDIT_ISSUE_9.md
compiler_robust_hopf/optimal_parallel.py
compiler_robust_hopf/optimal_audit.py
```

This remains an internal theorem status pending external proof review.

## 3. Structural decomposition

Cut the addressed frame after `t` prefix qubits. Put

```math
B=2^t,
\qquad
s=n-t.
```

The remaining tail is exactly

```math
R_t^{(n)}
=
\bigoplus_{r=0}^{B-1}W_s^{(r)}.
```

Each block is the complete Hopf frame belonging to one depth-`t` subtree. This
full-operator direct sum is the key structure absent from a generic list of
unrelated target columns.

## 4. Routed parallel-subframe compiler

The construction allocates `B` branch-data registers and `B` one-hot token
qubits. A coherent binary-tree router moves the existing suffix data and token
into the branch selected by the prefix. All token-controlled subtree frames act
on disjoint registers and therefore run in parallel. The inverse router returns
the transformed suffix to the original system register and cleans all auxiliary
registers.

The exact copied-control count is

```math
(B-1)(s+1)-t.
```

The complete routed construction fits in the conservative envelope

```math
2B(s+1)\leq m.
```

One controlled subtree frame has

```math
S_{\mathrm{csub}}(s)=O(2^s),
```

```math
D_{\mathrm{csub}}(s)
=O\left(s^2+\frac{2^s}{s}\right).
```

All `B` branches together have total size `O(B2**s)=O(N)` and the depth of one
branch.

## 5. Cut choice

For `m>=4n`, choose the largest `t<n` satisfying

```math
2\,2^t(n-t+1)\leq m.
```

If `s=n-t>1`, maximality gives

```math
m<4Bs.
```

Consequently,

```math
\frac{2^s}{s}
=\frac{N}{Bs}
<4\frac{N}{m}
=O\left(\frac{N}{n+m}\right).
```

Also,

```math
s^2=O\left(n+\frac{2^s}{s}\right).
```

The route and conditioned prefix each have `O(n)` depth, so the complete depth
is optimal.

For `1<=m<4n`, the frozen audited compiler has

```math
O\left(n^2+\frac{N}{n+m}\right)
```

depth. Since `n+m<5n` and `n**3<=4*2**n`, the `n**2` term is already absorbed
by `N/(n+m)`.

## 6. Matching lower bound

Applying the frame to `|0^n>` prepares an arbitrary real unit vector. The real
unit sphere has dimension `N-1`.

Parameter counting therefore gives

```math
S=\Omega(N)
```

and, on `n+m` total wires,

```math
D=\Omega\left(\frac{N}{n+m}\right).
```

For the independent linear term, the backward light cone of the `n` system
outputs contains fewer than `4n2**D` relevant continuous parameters in a
depth-`D` circuit. Covering an `(N-1)`-dimensional real state family requires

```math
4n2^D\geq N-1,
```

which gives `D=Omega(n)`. Combining the two bounds matches the routed upper
bound.

## 7. Why generic CQSP is not the solution

Yuan--Zhang controlled state preparation implements

```math
|j\rangle|0^n\rangle
\longmapsto
|j\rangle|\psi_j\rangle.
```

Treating all `N` frame columns as unrelated targets requires `n` index qubits
and has generic size

```math
O(2^{n+n})=O(N^2).
```

It also leaves the coherent input column label present. The routed compiler
avoids both problems by exploiting the Hopf tail direct sum and moving the
existing suffix register instead of generating a second indexed output.

## 8. Remaining strict-zero endpoint

The positive-workspace theorem does not settle `m=0` with simultaneous sharp
size and optimal depth.

Known exact constructions are:

| Clean ancillary qubits | Size | Depth |
|---:|---:|---:|
| `1` | `O(N)` | `O(n+N/n)` |
| `0` | `O(nN)` | `O(N)` |

The remaining question is:

```math
\boxed{
S_{\mathrm{frame}}(n,0)=O(N),
\qquad
D_{\mathrm{frame}}(n,0)=O\left(n+\frac{N}{n}\right)
\;?
}
```

Two outcomes remain scientifically useful:

1. an ancilla-free global synthesis of the Hopf tree frame attaining both
   bounds; or
2. a rigorous separation showing that one clean flag changes the achievable
   size--depth tradeoff for complete frame access.

## 9. Current stop conditions

Do not claim the strict-zero theorem from:

- the one-ancilla construction;
- a zero-ancilla circuit with `O(nN)` size;
- state-column equality;
- finite scaling fits;
- generic unitary synthesis;
- a CQSP routine that leaves its index register entangled.

The positive-workspace theorem may be used as the main manuscript result after
external proof review, with the `m=0` point stated as an explicit endpoint
problem rather than hidden inside an all-`m` claim.
