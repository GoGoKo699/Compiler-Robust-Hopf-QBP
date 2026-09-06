# Related work and contribution boundary

[← Source map](SOURCE_MAP.md) · [Complete narrative](../REVIEW.md) · [Landing page →](../README.md)

The result joins two technical lines:

1. exact state preparation with arbitrary clean workspace;
2. Hopf coordinates and inverse-frame gradient readout.

Borrowed-workspace and controlled-unitary constructions explain the strict-zero
schedule.  This page places the ingredients by mathematical role and keeps the
new claim narrow.

<p align="center">
  <img src="../assets/literature-lineage.svg" width="940" alt="The all-workspace state-preparation line and the Hopf differential-frame line meet in the prescribed-completion compiler." />
</p>

## 1. Exact state preparation and the target frontier

The state-preparation line develops exact circuits whose depth decreases as
clean ancillary workspace increases.  Its uniform all-workspace conclusion is

```math
S_{\mathrm{QSP}}(n,m)=\Theta(2^n),
```

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
```

The active compiler framework in this repository is P. Yuan and S. Zhang,
*Quantum* **7**, 956 (2023).  We use its exact results for:

- ancilla-free multi-controlled X;
- uniformly controlled one-qubit gates at arbitrary workspace;
- coherent CNOT copy–uncopy;
- the optimal state-preparation comparison frontier.

The published article corresponds to `arXiv:2202.11302v2`; the imported
statements were also checked in v3.

The earlier paper by Sun, Tian, Yang, Yuan, and Zhang established the preceding
time–space landscape and is retained as the historical predecessor and original
source of selected primitives.  For the present theorem, the later uniform
framework is sufficient for all workspace regimes.

The connection to the Hopf problem is constructive rather than automatic.  Once
the Hopf completion is written as addressed complete-operator layers, the
state-preparation primitives can be adapted while preserving its designated
columns.

## 2. Uniformly controlled gates and the Möttönen route

Möttönen and coauthors introduced the uniformly controlled rotation language
for state preparation.  Bergholm and coauthors developed the corresponding
general uniformly controlled one-qubit gates.

The earlier Hopf-QBP compiler follows this route: compute the shared lower-
suffix-zero predicate into one clean flag, then apply a smaller multiplexed
rotation selected by the prefix and flag.  This already shows that the complete
Hopf frame can be compiled with linear asymptotic gate count and constant
additional workspace.

At strict zero workspace, inserting identity blocks into one full-width
multiplexor is not enough.  Although the logical block table is sparse, the
standard Walsh/Gray-code angle transform generically repeats nonzero
coefficients across all suffix frequencies.  The physical angle table is not
sparse in the required sense.

The strict-zero schedule instead retains a narrow UCG.  One original suffix data
qubit carries the predicate temporarily, and two half-angle width-$`d+2`$ UCGs
produce the full addressed depth while restoring that qubit exactly.

## 3. Borrowed workspace and controlled-unitary roots

Several established techniques are close to the strict-zero circuit.

- Barenco and coauthors use roots and conjugation identities in controlled-
  unitary decompositions.
- Later borrowed-qubit constructions use unknown-state logical wires while
  restoring them exactly.
- Conditionally clean ancillas and toggle-detection patterns organize
  cancellation across different original values of a borrowed wire.
- Ancilla-free multi-controlled $\mathrm{SU}(2)$ constructions give related individual
  controlled-rotation primitives.

For one Hopf prefix, put

```math
C_p=R_y(\theta_p/2).
```

The identities

```math
C_p^2=R_y(\theta_p),
\qquad
XC_pX=C_p^{-1}
```

make the original zero-suffix sector square to the required rotation and make
the unwanted original value of the borrowed bit cancel.

The borrowed bit is not an extra dirty ancillary wire.  It is part of the
logical input, the desired operation depends on its original value, and the
proof must restore it on arbitrary entangled inputs.

### Narrow strict-zero contribution

The repository does not claim the invention of borrowed qubits, conditional
cleanliness, toggle detection, controlled-unitary roots, Pauli conjugation, or
UCGs.

The Hopf-specific statement is:

> One original suffix data qubit serves as a restored in-place predicate
> carrier, reducing every addressed Hopf depth to two total-width-$`d+2`$ UCGs
> and linear predicate toggles.  Summed over the tree, this gives the optimal
> strict-zero complete-frame frontier.

## 4. Sparse and restricted multiplexors

Recent restricted-UCG work asks when block repetition or limited control
participation can reduce synthesis cost.  The addressed Hopf layer is related,
but its sparsity has a particular form: one long all-zero suffix predicate is
shared by every prefix-selected rotation.

The borrowed-suffix factorization converts this logical predicate into smaller
physical UCG width rather than attempting to prune the full-width Möttönen angle
table.  That is the structural distinction relevant to the strict-zero bound.

## 5. Coherent routing and workspace parallelism

For large workspace, the Hopf tail has the exact direct-sum form

```math
R_t^{(n)}
=\bigoplus_{r=0}^{2^t-1}W_s^{(r)}.
```

The compiler realizes this form by standard reversible ingredients:

- balanced CNOT fanout of the prefix bits;
- Fredkin routing of one suffix-token block;
- disjoint token-controlled subtree frames;
- exact uncomputation and inverse routing.

The state-preparation framework supplies the coherent-copy and UCG primitives.
The Hopf-specific part is the tree-cut identity, the register layout, the
route–operate–unroute schedule, and the shared workspace envelope for prefix and
tail.

The implementation gives the router explicitly and tests arbitrary complex
inputs in which the prefix and suffix are entangled.

## 6. Hopf coordinates and inverse-frame gradients

The first Hopf work develops the balanced binary chart, inverse map, diagonal
metric, and coordinate directions.  The second develops the addressed
state-and-marker frame, global magnitude record, direct phase record, and
checkpoint interface.

The compiler target is

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
\qquad
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

For unrestricted angles,

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical domains, $a_j$ is nonnegative.  At a singular coordinate, the
raw derivative vanishes while the complete parameter tuple still selects an
orthogonal marker-frame continuation.

The phase-dressed complex magnitude frame is

```math
W_{\mathbb C,\mathrm{mag}}
=D_{\mathrm{ph}}W_{\mathbb R}.
```

The leaf-phase coordinates remain a separate direct stream.

The synthesis theorem proves that these prescribed magnitude-frame operators,
not only their first columns, attain the all-workspace state-preparation
frontier.

## 7. Comparison by mathematical role

| Line of work | Object or result | Role used here | Additional Hopf structure |
|---|---|---|---|
| Möttönen; Bergholm | multiplexed rotations and general UCGs | block-diagonal one-qubit-gate language | addressed depths are reduced to narrow UCGs rather than full-width sparse tables |
| exact QSP time–space tradeoffs | arbitrary state preparation with clean workspace | target frontier and compiler primitives | designated frame columns must survive the adaptation |
| controlled-unitary roots and borrowed workspace | exact conditioned operations with limited ancillas | cancellation and restored logical carriers | the predicate includes the borrowed suffix bit's original value |
| restricted UCGs | repeated or sparse block structure | neighboring structural context | one shared zero-suffix predicate is factored through a restored logical bit |
| reversible routing | CNOT fanout, Fredkin networks, uncomputation | coherent branch movement and parallel action | realizes the Hopf tail direct sum within the prefix workspace envelope |
| Hopf chart | state map, inverse, metric, coordinate directions | specifies the structured columns | yields the addressed tree layers |
| Hopf QBP | inverse-frame magnitude record and direct phase record | makes the completion operational | requires frame-safe rather than state-column compilation |

## 8. Contribution at theorem level

The complete contribution is the following chain.

1. Identify complete frame safety as the compiler contract used by the global
   inverse-frame record.
2. Give an exact state-column counterexample.
3. Express the frame as zero-suffix-addressed tree layers.
4. Close the zero-workspace endpoint with the borrowed-suffix echo.
5. Build a clean binary–one-hot prefix decoder and explicit coherent router.
6. Match the state-preparation size–depth frontier for every $m\geq0$.
7. Transfer the result to the phase-dressed complex magnitude frame.
8. State the QBP consequence under matched program and output-task conventions.

The theorem is specific to the structured Hopf completion.  It does not imply
that an arbitrary family of prescribed unitary columns can be implemented at
state-preparation cost.

## 9. Detailed source record

The [source map](SOURCE_MAP.md) gives exact theorem numbers and local consumers.
The broader technical search is retained in
[`PRIOR_ART_SEARCH_2026_09.md`](PRIOR_ART_SEARCH_2026_09.md) and
[`provenance/prior_art_search.json`](../provenance/prior_art_search.json).

A negative result from that bounded search is not treated as proof of novelty or
priority.

## References highlighted here

- A. Barenco et al., “Elementary gates for quantum computation,” *Physical
  Review A* **52**, 3457–3467 (1995).
- M. Möttönen et al., “Transformation of quantum states using uniformly
  controlled rotations,” *Quantum Information and Computation* **5**, 467–473
  (2005).
- V. Bergholm et al., “Quantum circuits with uniformly controlled one-qubit
  gates,” *Physical Review A* **71**, 052330 (2005).
- X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, “Asymptotically Optimal
  Circuit Depth for Quantum State Preparation and General Unitary Synthesis,”
  *IEEE TCAD* **42**, 3301–3314 (2023).
- P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
  improved unitary synthesis by quantum circuits with any number of ancillary
  qubits,” *Quantum* **7**, 956 (2023).
- B. Claudon et al., “Polylogarithmic-depth controlled-NOT gates without
  ancilla qubits,” *Nature Communications* **15**, 5886 (2024).
- T. Khattar and C. Gidney, “Rise of conditionally clean ancillae for efficient
  quantum circuit constructions,” *Quantum* **9**, 1752 (2025).
- B. Zindorf and S. Bose, “Efficient implementation of multi-controlled quantum
  gates,” *Physical Review Applied* **24**, 044030 (2025).

---

[← Source map](SOURCE_MAP.md) · [Complete narrative](../REVIEW.md) · [Landing page →](../README.md)
