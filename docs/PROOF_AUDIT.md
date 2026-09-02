# Proof audit of the unified compiler

## Status

Completed internally for the `yuan-zhang-unified-refactor` branch. This is a
line-by-line mathematical and register audit, not external peer review.

The audit question is:

> Does the active optimal positive-workspace theorem follow using only the Hopf
> frame identities, the construction supplied in this repository, and the exact
> Yuan--Zhang standard-circuit framework, while treating Sun et al. only as a
> historical and original-attribution source?

Outcome: **yes**, subject to the same external-review and strict-zero-workspace
boundaries stated elsewhere in the repository.

## 1. Source discipline

The following Yuan--Zhang results were checked directly in the published
*Quantum* paper:

- Theorem 2 gives the optimal QSP size and depth for every ancillary budget.
- Lemma 5 gives linear-size, linear-depth ancilla-free multi-controlled X.
- Lemma 6 gives exact UCG size `O(2**q)` and depth
  `O(q+2**q/(q+w))`.
- Lemma 9 gives coherent CNOT-tree copying in logarithmic depth.
- Theorem 1 gives the generic CQSP size used in the all-column comparison.

The paper explicitly attributes selected primitives to Sun et al. The active
proof cites Yuan--Zhang as its compiler framework and retains the earlier paper
as historical/original attribution. No active construction invokes the earlier
unary-to-binary lemma.

Classification: **verified**.

## 2. Rejected recursive shortcut

A preliminary cleanup proposal attempted to replace the conditioned prefix by a
naively controlled recursive call to the full frame compiler. That proposal was
rejected before adoption: when the selected cut is close to `n-1`, repeated
recursive prefixes can accumulate `Theta(n**2)` depth.

The active replacement is the explicit binary--one-hot tree decoder below. It
has a nonrecursive `O(t)`-depth schedule.

Classification: **corrected during design**.

## 3. Tree-decoder clean-subspace identity

Let `B=2**t`. The decoder uses:

```math
B
```

one-hot leaf qubits,

```math
B-1
```

internal indicators, and

```math
B-1-t
```

shared scratch qubits. The clean workspace count is therefore

```math
3B-2-t.
```

For each binary input `x`, the top-down indicator tree computes exactly one
active path and one active leaf. At tree depth `d`, the right-child indicators
have parity `x_d`; balanced parity trees therefore clear the original binary
register coherently. CNOTs from both children clear every internal indicator
because the two children are mutually exclusive on the valid path.

Thus

```math
D_t|x\rangle|0\rangle
=|0^t\rangle|e_x\rangle|0\rangle.
```

The circuit is a permutation of the complete computational basis. The identity
therefore extends by linearity to arbitrary superpositions, and reversing the
circuit gives the exact inverse on the complete one-hot code.

Classification: **proved**.

Finite support:

- exhaustive clean-input checks for all labels through `t=7`;
- sampled labels through `t=10`;
- arbitrary full-register basis reversibility through `t=7`.

## 4. Explicit decoder depth schedule

The implementation returns the decoder as disjoint gate layers.

The depth contributions are:

| Stage | Depth |
|---|---:|
| Concurrent address fanout | `t-1` |
| Root initialization | `1` |
| Top-down indicators | `3t` |
| Address uncopy | `t-1` |
| Concurrent parity reductions | `2(t-1)` |
| Clear binary register | `1` |
| Parity uncomputation | `2(t-1)` |
| Clear internal indicators | `2t` |

The total is

```math
11t-4=O(t).
```

Every layer is checked to have pairwise-disjoint gate support. The high-level
gate count is

```math
11B-10-5t=O(B),
```

including `B-1` Toffoli gates. Each Toffoli has constant exact standard-circuit
cost because it is fixed width.

Classification: **proved and explicitly scheduled**.

## 5. One-hot Hopf action

At Hopf tree depth `d`, the one-hot Givens network acts on `2**d` disjoint mode
pairs. The code-space matrix was independently constructed and compared with
the complete addressed `t`-qubit Hopf frame.

Therefore

```math
D_t^\dagger G_tD_t
=W_{\mathbb R}^{(t)}
```

on clean decoder workspace. The Givens network preserves the one-excitation
code exactly.

Classification: **proved**.

Finite support: exact code-space matrix equality through `t=8` and combinatorial
pair-disjointness through `t=11`.

## 6. Conditioned prefix

For external suffix length `s=n-t`, the decoder is followed by:

1. a suffix-zero predicate in one clean decoder-scratch wire;
2. coherent fanout to at most `B/2` controls, counting the original;
3. `t` controlled disjoint Givens layers;
4. exact uncopy and predicate uncomputation;
5. inverse tree decoding.

After the forward decoder, the internal and shared scratch registers are zero.
Their number is

```math
(B-1)+(B-1-t),
```

which is at least the required flag and copied controls for every nontrivial
routed cut. No additional workspace is hidden.

The block therefore implements

```math
W_t\otimes|0^s\rangle\!\langle0^s|
+I\otimes\left(I-|0^s\rangle\!\langle0^s|\right)
```

with depth `O(n)`, size `O(B+s)`, and workspace `3B-2-t`.

Classification: **proved**.

An initial regression test incorrectly compared the full-frame endpoint `t=n`
to the routed-cut envelope, which is only used for `s>=1`. The test was
corrected; no construction or theorem statement changed.

## 7. Low-workspace direct compiler

For `m>=1`, every nonfinal addressed layer uses one suffix flag and one UCG.
The flag is uncomputed before the next layer. The final layer needs no flag.
Yuan--Zhang Lemmas 5 and 6 give

```math
S=O(N),
```

```math
D=O\left(n^2+\frac{N}{n+m}\right).
```

When `1<=m<4n`, the polynomial term is absorbed by the geometric term, so this
schedule has depth `O(N/(n+m))`, which is the optimal order in that range.

At strict `m=0`, representing each addressed layer by one full-width UCG gives
the separately labelled fallback `S=O(nN)`, `D=O(N)`.

Classification: **proved relative to Lemmas 5 and 6**.

## 8. Routed tail and workspace

The exact identity

```math
R_t^{(n)}=\bigoplus_r W_s^{(r)}
```

was rechecked independently of the old module. The coherent router preserves
the prefix, moves the existing suffix and one activation token into the selected
branch, applies all controlled subtree frames on disjoint registers, and routes
the transformed suffix back.

The exact copied-control count is

```math
(B-1)(s+1)-t.
```

After routing these controls are uncomputed and their clean wires are reused as
branch suffix flags. The complete routed-tail peak and the new conditioned
prefix both fit inside

```math
2B(s+1).
```

Route and unroute have depth `O(n)` and size `O(B(s+1))`. One controlled subtree
frame has size `O(2**s)` and depth `O(s**2+2**s/s)`. The `B` frames are physically
disjoint and run in parallel.

Classification: **proved relative to Lemmas 5, 6, and 9**.

Finite support: every tail cut through `n=8`, exact angle partitions, reversible
small routers, arbitrary complex input states, zero leakage, and broad integer
workspace grids.

## 9. Cut choice

For `m>=4n`, choose the largest cut satisfying

```math
2\,2^t(n-t+1)\leq m.
```

For `s=n-t>1`, failure of the next cut gives `m<4Bs`, and therefore

```math
\frac{2^s}{s}<4\frac{N}{m}
=O\left(\frac{N}{n+m}\right).
```

Also `s**2=O(n+2**s/s)`. The complete routed depth is consequently

```math
O\left(n+\frac{N}{n+m}\right).
```

The endpoint `s=1`, the one-qubit case, and arbitrarily large `m` are absorbed
separately. The low-workspace schedule covers every `1<=m<4n`.

Classification: **proved**.

Broad-grid term diagnostics are retained as regression checks only; the theorem
does not rely on numerical slope fitting.

## 10. One-UCG complex diagonal

Writing a basis label as `x=zb` gives

```math
D_{\mathrm{ph}}
=\sum_z|z\rangle\!\langle z|\otimes
\operatorname{diag}(e^{i\phi_{z0}},e^{i\phi_{z1}}).
```

This is exactly one `n`-qubit UCG under the definition preceding Yuan--Zhang
Lemma 6. It therefore has size `O(N)` and depth
`O(n+N/(n+m))` using at most `m` clean ancillas. Arbitrary `U(2)` blocks retain
the common phase exactly.

The earlier phase-polynomial/FWHT compiler is unnecessary. The active block
table is generated directly from the `N` leaf phases in `O(N)` work.

Classification: **proved relative to Lemma 6**.

Finite support: exact complete-matrix and inverse checks through `n=9`, plus
composition with the real frame through `n=7`.

## 11. Lower bounds

Applying the frame to `|0^n>` prepares every real unit vector, a manifold of
dimension `N-1`.

- At most four continuous real parameters occur per arbitrary one-qubit gate,
  giving size `Omega(N)`.
- A depth layer on `n+m` wires has at most `n+m` one-qubit-gate locations,
  giving depth `Omega(N/(n+m))`.
- The backward light cone of the `n` system outputs contains fewer than
  `4n2**D` relevant continuous parameters in depth `D`, giving `D=Omega(n)`.

These combine to

```math
D=\Omega\left(n+\frac{N}{n+m}\right).
```

Classification: **proved**.

## 12. Complex and QBP composition

The real frame and one-UCG phase diagonal are clean sequential blocks and reuse
the same workspace pool. The complex upper bound follows. The real subfamily
supplies the same lower bounds.

Frame-safe substitution preserves the global gradient distribution. The
record-wise magnitude decoder and direct phase decoder remain independent of the
compiler. The phase-block table now requires only `O(N)` direct generation;
old `O(Nn)` phase-polynomial preprocessing is not part of the active theorem.

Classification: **proved**, conditional only on the declared controlled-observable
access model for the final QBP time ratio.

## 13. Audit conclusion

The active positive-workspace theorem is internally supported by one coherent
construction:

```text
self-contained tree decoder
+ Hopf tree direct sum
+ coherent routing
+ Yuan--Zhang UCG/MCT/copy primitives
+ one-UCG complex phase layer.
```

No construction-level step requires selecting the earlier state-preparation
compiler in any ancillary regime.

Remaining boundaries:

- external human proof review;
- simultaneous `O(N)` size and optimal depth at strict `m=0`;
- hardware connectivity and approximate gate-set compilation;
- application-specific controlled-observable cost.
