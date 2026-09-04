# Manuscript workspace

The repository contains one internally coherent all-workspace compiler theorem.
The reader-facing route begins with the structured unitary-completion problem in
[`../README.md`](../README.md) and continues through the complete technical note
[`../REVIEW.md`](../REVIEW.md).

## Working title

**Optimal Compilation of Hopf Differential Frames for Quantum Backpropagation**

The title should remain Hopf-specific unless a broader coordinate-frame theorem
is established.

## Intended intellectual order

The paper should begin from exact state preparation rather than from quantum
backpropagation.

1. QSP fixes one column of a unitary.
2. The Hopf differential frame fixes one structured complete unitary.
3. The complete frame is required because the inverse circuit resolves marker
   columns.
4. The state-preparation primitives can be adapted after the addressed-layer and
   tree-cut structure is exposed.
5. The adapted compiler matches the optimal QSP frontier for every workspace
   budget.
6. Compiler-robust QBP follows as the downstream corollary.

This order lets a circuit-synthesis reader check the central theorem without
first learning the complete Hopf optimization program.

## Central theorem

Let

```math
N=2^n.
```

For every clean-workspace budget `m>=0`, the complete real Hopf differential
frame and the phase-dressed complex magnitude frame have exact frame-safe
implementations with

```math
\boxed{
S_{\mathbb R}(n,m)
=S_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta(N)
}
```

and

```math
\boxed{
D_{\mathbb R}(n,m)
=D_{\mathbb C,\mathrm{mag}}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right).
}
```

The complex leaf-phase derivatives use a separate direct measurement stream.
The theorem does not place all `2N-1` real complex-chart coordinate directions
inside one `N`-dimensional unitary.

## Problem statement in compiler language

The logical frame satisfies

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
```

```math
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

A valid clean compiler must satisfy

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=
\bigl(W|\varphi\rangle\bigr)|0^m\rangle
```

for every system input. The state-column obstruction should appear before the
all-workspace construction, using the explicit two-qubit gradient change

```math
(2,0,0)\longmapsto(0,\sqrt2,0).
```

The point should be phrased positively: the state-preparation framework can be
adapted once the stronger operator specification is made explicit.

## Minimal Hopf interface

For unrestricted magnitude angles, use the oriented incoming amplitude `a_j`:

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical domains, `a_j>=0`, so `a_j=sqrt(g_(j,j))`. At a singular
coordinate, the raw differential vanishes and the marker column remains a
chart-selected orthogonal frame direction determined by the complete parameter
tuple.

Canonical domains:

- real depths `0,...,n-2`: `[0,pi/2]`;
- final real magnitude depth: `[0,2pi)`;
- complex magnitude depths: `[0,pi/2]`.

The compiler proof consumes the marker formula and addressed layer

```math
L_d^{(n)}
=I+
\sum_p|p\rangle\!\langle p|
\otimes
\bigl(R_y(\theta_{d,p})-I\bigr)
\otimes
|0^{n-d-1}\rangle\!\langle0^{n-d-1}|.
```

The full inverse coordinate map and optimization architecture need not enter the
compiler sections.

## External circuit framework

The active framework and QSP benchmark are P. Yuan and S. Zhang, *Quantum*
**7**, 956 (2023):

- Theorem 2 for the optimal all-workspace QSP frontier;
- Lemma 5 for exact ancilla-free multi-controlled `X`;
- Lemma 6 for UCG synthesis;
- Lemma 9 for coherent copy–use–uncopy.

The published article corresponds to `arXiv:2202.11302v2`; the imported
statements were checked in v3. The earlier state-preparation paper is the
historical predecessor and original-source reference for selected primitives.
The two papers should be presented as one coherent compiler line, not as
competing constructions selected by workspace regime.

## Compiler contribution chain

1. Define the complete real frame and phase-dressed complex magnitude frame.
2. State the canonical domains, oriented incoming amplitudes, and singular
   boundary.
3. Prove complete frame-safe substitution.
4. Give the two-qubit state-column obstruction.
5. Prove the strict-zero borrowed-suffix echo.
6. Derive optimal strict-zero resources.
7. Prove the conditioned-prefix and tail direct-sum identities.
8. Construct the clean binary–one-hot decoder.
9. Construct the explicit coherent CNOT/Fredkin router.
10. Prove route–controlled-subframes–unroute equality and cleanup.
11. Establish the simultaneous peak-workspace envelope.
12. Prove the direct and routed positive-workspace upper bounds.
13. Prove matching size and depth lower bounds.
14. Combine the schedules into one all-workspace theorem.
15. Add the one-UCG phase dressing.
16. Derive the matched compiler consequence for global Hopf QBP.
17. State the separate checkpoint active-interface boundary.

## Provisional theorem hierarchy

- **Definition 1:** real Hopf differential frame and complex magnitude frame.
- **Definition 2:** frame-safe compiler.
- **Proposition 3:** one state column is insufficient.
- **Lemma 4:** strict-zero borrowed-suffix echo.
- **Theorem 5:** optimal strict-zero real frame.
- **Lemma 6:** conditioned-prefix identity.
- **Lemma 7:** tail direct-sum identity.
- **Lemma 8:** clean binary–one-hot decoder.
- **Lemma 9:** explicit coherent routed tail.
- **Theorem 10:** optimal all-workspace real Hopf frame.
- **Corollary 11:** optimal all-workspace phase-dressed complex magnitude frame.
- **Corollary 12:** matched compiler-robust global Hopf backpropagation.
- **Theorem 13:** checkpoint active-interface substitution.

Numbering remains provisional.

## Preferred paper structure

1. Introduction: structured completion between QSP and general unitary synthesis
2. Minimal Hopf frame interface
3. Compiler contracts and the state-column obstruction
4. Exact circuit model and imported state-preparation primitives
5. Ancilla-free borrowed-suffix echo
6. Exact tree cut and conditioned prefix
7. Clean prefix decoder and coherent branch router
8. All-workspace upper and lower bounds
9. Phase-dressed complex magnitude frame
10. Matched quantum-backpropagation consequence
11. Checkpoint interfaces and limitations
12. Related work and broader applicability

The strict-zero echo should appear before the routed construction because it
closes the endpoint that workspace parallelism cannot address. The four-sector
proof, explicit router action, simultaneous register peak, and maximal-cut
inequality belong in the main text. Constant-bearing gate ledgers may be placed
in appendices.

## Runtime and statistical wording

The primary finite-shot target is simultaneous absolute accuracy of the raw
Hopf-coordinate gradient. Complete-vector, relative, normalized-frame, and
natural-gradient targets have different norm and conditioning costs.

The scalar-versus-gradient statement should be written for matched programs:

```math
T_{\mathrm{scalar}}^{\mathrm{matched}}
=S_E(D_{\mathrm{prep}}+D_O),
```

```math
T_{\mathrm{grad}}^{\mathrm{matched}}
=S_{\nabla}(D_{\mathrm{prep}}+D_O+D_{\mathrm{frame}}).
```

At fixed comparable scalar and raw-coordinate absolute accuracy and confidence,
the inverse frame adds only a constant per-execution depth factor and the total
logical-depth overhead is `O(log n)=O(log log M)`. This is a general-family
comparison, not a claim against an instance-specific scalar shortcut, and it
excludes classical output materialization.

## Novelty discipline

The manuscript should not claim invention of:

- UCGs or multiplexed rotations;
- controlled-unitary square-root identities;
- borrowed or dirty qubits;
- conditionally clean workspace;
- toggle detection;
- ancilla-free multi-controlled gates.

The narrow strict-zero contribution is:

> One original suffix data qubit is used as a restored in-place predicate
> carrier, allowing every prefix-dependent Hopf rotation at depth `d` to be
> implemented by two total-width-`d+2` UCGs and linear predicate toggles. The
> resulting complete frame attains the optimal ancilla-free frontier.

The broader theorem-level contribution is the complete frame-safe all-workspace
compiler and its QBP consequence.

## Completed support

- complete frame and addressed-layer operator checks;
- canonical-domain, oriented-amplitude, and singular-coordinate tests;
- exact global and checkpoint compiler-boundary examples;
- strict-zero layer, frame, inverse, and complex-magnitude tests;
- exact-rational strict-zero resource diagnostics;
- conditioned-prefix and direct-sum identities;
- explicit reversible tree decoder;
- explicit coherent router on arbitrary entangled inputs;
- exact token, copy, flag, and data cleanup;
- all-workspace upper and lower bounds;
- one-UCG phase diagonal;
- output-sensitive magnitude and direct-phase decoders;
- source-version and upstream-repository reconciliation;
- consolidated proof, source, verification, and claim-support maps.

## Remaining work

- independent technical assessment of the strict-zero echo, router, register
  peak, maximal-cut argument, lower bounds, and matched QBP statement;
- specialist prior-art assessment of the narrow strict-zero claim;
- manuscript drafting and notation cross-check against both Hopf papers;
- selection of the minimum useful resource figures;
- complete manuscript compilation and referee-style audit;
- update of citation metadata after a manuscript identifier exists.

The repository already presents the theorem in the intended manuscript order.
The next writing phase should compress that route rather than reconstructing the
argument from the development history.
