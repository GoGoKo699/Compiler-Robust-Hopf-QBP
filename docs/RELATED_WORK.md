# Related work and contribution boundary

[← Source map](SOURCE_MAP.md) · [Complete technical note](../REVIEW.md) · [Back to the landing page →](../README.md)

The theorem joins two lines of work:

1. exact state preparation and uniformly controlled gates;
2. Hopf-coordinate geometry and inverse-frame gradient records.

Borrowed and conditionally clean workspace provides a third, local connection
for the zero-workspace construction.

<p align="center">
  <img src="../assets/literature-lineage.svg" width="980" alt="The state-preparation compiler line and the Hopf differential-frame line meet in the optimal structured unitary-completion theorem." />
</p>

## 1. State-preparation compiler line

### Uniform all-workspace frontier

Yuan and Zhang give a unified exact framework for controlled state preparation
and determine the optimal arbitrary-QSP size and depth for every clean-ancillary
budget:

```math
S_{\mathrm{QSP}}(n,m)=\Theta(2^n),
```

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
```

Their paper is the active external compiler framework and comparison benchmark
throughout this repository. The Hopf proof uses its exact multi-controlled-`X`,
UCG, and coherent copy–uncopy primitives.

The published *Quantum* article corresponds to `arXiv:2202.11302v2`. Theorem 2
and Lemmas 5, 6, and 9 were also checked in v3 and retain the statements and
circuit-model conventions used here.

The earlier state-preparation paper of Sun, Tian, Yang, Yuan, and Zhang
established the preceding ancilla–depth landscape and is retained as the
historical predecessor and original-source reference for selected primitives.
For the present theorem, the two papers form one coherent compiler line. The
later result supplies the uniform all-workspace frontier, so there is no need to
select a different published construction in different workspace regimes.

### Relation to the Hopf problem

The state-preparation results and the Hopf theorem specify different operators.
QSP fixes one initialized state column. The Hopf gradient protocol uses a
particular unitary completion with prescribed marker columns.

The external primitives can nevertheless be adapted once the complete Hopf
frame is written as addressed zero-suffix layers and tree-cut direct sums. The
adaptation is the local content of the three schedules in this repository.

This formulation keeps the relationship precise without treating the different
operator task as a limitation of the state-preparation results.

## 2. UCG and multiplexor structure

Möttönen and coauthors introduced the uniformly controlled rotation form used in
state preparation. Bergholm and coauthors developed the corresponding general
uniformly controlled one-qubit gates. This language underlies both the earlier
Möttönen-style Hopf-QBP compiler and the present theorem.

At one Hopf depth, the logical block table is sparse: only the blocks whose lower
suffix is zero contain a nontrivial rotation. A direct full-width Möttönen
transform does not preserve that sparsity in its physical angle list. The
Walsh/Gray-code coefficients are generically repeated across all suffix
frequencies, so a full `n`-qubit multiplexor pays for a dense table at each
depth.

The present constructions keep the UCG width tied to the prefix rather than the
complete suffix:

- at zero workspace, one original suffix bit carries the predicate through an
  echo, leaving two total-width-`d+2` UCGs;
- with one clean bit, the suffix predicate is stored explicitly and one
  total-width-`d+2` UCG is used;
- with larger workspace, the tail is split into disjoint `s`-qubit subtree
  UCGs that run in parallel.

The Möttönen/Bergholm line is therefore both a technical precursor and the
natural language for the Hopf-specific factorization.

## 3. Borrowed and conditionally clean workspace

The strict-zero circuit combines several familiar ingredients.

Barenco and coauthors use roots of target unitaries and conjugation identities
in controlled-unitary decompositions. Claudon and coauthors develop exact
controlled constructions with borrowed qubits. Khattar and Gidney formalize
conditionally clean qubits and toggle-detection patterns. Zindorf and Bose give
efficient ancilla-free multi-controlled `SU(2)` constructions.

For one addressed Hopf layer, put

```math
C_p=R_y(\theta_p/2).
```

The identities

```math
C_p^2=R_y(\theta_p),
\qquad
XC_pX=C_p^{-1}
```

allow one original suffix data qubit to carry the all-zero predicate temporarily.
The desired original-suffix-zero branch receives `C_p^2`, while the unwanted
original value of the borrowed bit receives the cancelling word `C_pXC_pX`.
The logical qubit is restored exactly on the complete Hilbert space.

### Contribution boundary beside the construction

The repository does not claim invention of:

- borrowed or dirty qubits;
- conditionally clean ancillas;
- toggle detection;
- controlled-unitary square roots;
- Pauli-conjugation echoes;
- uniformly controlled gates.

The narrow Hopf-specific contribution is:

> One original suffix data qubit is used as a restored in-place predicate
> carrier, reducing all prefix-dependent rotations at depth `d` to two
> total-width-`d+2` UCGs and linear predicate toggles. Summing those addressed
> layers gives the optimal strict-zero complete-frame frontier.

This statement identifies the operator reduction and resource consequence while
crediting the familiar component ideas.

## 4. Restricted and sparse UCG synthesis

Recent work on restricted or sparse UCG structures asks when repeated blocks or
limited control participation can reduce synthesis cost. The addressed Hopf
layer belongs to the same broad structural setting, but its long all-zero
suffix predicate is generically dense under the ordinary Möttönen angle
transform.

The borrowed-suffix echo avoids that transform. It factors the logical
predicate through one restored system bit and then applies two smaller UCGs.
The restricted-UCG literature is therefore close context, while the exact
Hopf-layer factorization remains explicit in the present proof.

## 5. Coherent routing and workspace parallelism

The positive-workspace construction uses standard reversible ingredients:
coherent CNOT fanout, Fredkin routing, clean uncomputation, and parallel action
on disjoint registers.

The project-specific content is how those primitives realize the Hopf tail
identity

```math
R_t^{(n)}=\bigoplus_r W_s^{(r)}
```

inside the same workspace envelope as the conditioned prefix.

The explicit router:

1. copies each prefix control with a balanced CNOT tree;
2. routes the suffix and one activation token through disjoint Fredkin layers;
3. erases the prefix copies;
4. reuses the clean copy pool as local suffix flags;
5. applies all token-controlled subtree frames in parallel;
6. clears the flags, recreates the copies, reverses the route, and resets every
   work register.

Yuan–Zhang Lemma 9 supplies the coherent-copy primitive. The Hopf tree cut,
register allocation, router, and live-workspace proof are developed here.

## 6. Hopf geometry and gradient records

The first Hopf paper develops the balanced binary chart for arbitrary real and
complex pure states. It supplies the forward map, explicit inverse, canonical
domains, diagonal pullback metric, coordinate directions, and original
optimization interface.

For unrestricted angles, the precise differential relation is

```math
\partial_{\theta_j}|\psi\rangle
=a_j|e_j\rangle,
\qquad
g_{j,j}=a_j^2.
```

On the canonical domains, `a_j>=0` and equals the principal metric square root.
At a singular coordinate, the raw differential vanishes while the unit marker
column remains a chart-selected frame direction.

The second Hopf paper arranges the magnitude directions as an addressed unitary
frame and applies its inverse to a shared objective response. One global
magnitude outcome contributes to every magnitude coordinate. Complex leaf
phases use a separate direct one-hot record, and a checkpoint method gives
selected-depth locality.

The compiler question starts after these interfaces are fixed:

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
\qquad
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

The present theorem shows that these complete magnitude-frame operators, not
only their first columns, attain the optimal state-preparation frontier.

## 7. Comparison by mathematical role

| Work or line | Object compiled or analyzed | Result used | Adaptation in this repository |
|---|---|---|---|
| Möttönen et al.; Bergholm et al. | multiplexed rotations and UCGs | exact block-diagonal one-qubit-gate language | addressed depths are factored into narrow UCGs rather than full-width sparse tables |
| Sun et al. | state preparation and general unitary synthesis | historical ancilla–depth landscape | predecessor and original-source attribution |
| Yuan–Zhang | controlled state preparation, UCGs, MCTs, coherent copying | uniform optimal QSP frontier and active primitives | complete Hopf layers are exposed so the primitives preserve every marker column |
| Barenco et al.; Claudon et al. | controlled roots and borrowed-qubit constructions | square-root, conjugation, and borrowed-wire lineage | one logical suffix bit carries and releases the zero-suffix predicate |
| Khattar–Gidney | conditionally clean workspace and toggle detection | safe restoration of unknown-state wires | a non-self-inverse Hopf rotation is handled by a half-angle/Pauli echo |
| Zindorf–Bose | ancilla-free multi-controlled `SU(2)` | context for exact individual controlled rotations | all prefix values are aggregated into two UCGs |
| restricted-UCG work | structured multiplexors | sparse-control context | logical suffix sparsity is converted into smaller physical UCG width |
| reversible routing | CNOT fanout, Fredkin networks, uncomputation | coherent movement and branch parallelism | explicit tree router realizes the Hopf tail direct sum and reuses cleared copies as flags |
| first Hopf paper | state chart, metric, and coordinate directions | geometric interface | supplies the structured columns to be preserved |
| Hopf-QBP paper | global, phase, and checkpoint records | inverse-frame protocol and statistical task boundaries | frame safety is separated from state-column equality and made optimal |

## 8. Full theorem-level contribution

The contribution is the complete chain rather than one isolated circuit
identity:

1. identify complete frame safety as the compiler contract used by the global
   inverse-frame record;
2. show by exact example that a preparation-equivalent completion can fail;
3. expose the addressed layers and exact tree-cut direct sum;
4. close strict zero workspace with the in-place suffix echo;
5. construct the clean binary–one-hot decoder and coherent router;
6. match the QSP size–depth frontier for every `m>=0`;
7. transport the result to the phase-dressed complex magnitude frame;
8. state the QBP consequence as a matched logical-program comparison.

The theorem is specific to the Hopf differential frame. It does not assert that
a generic family of `N` orthonormal columns can be compiled at state-preparation
cost.

## 9. Detailed search record

The broader source-by-source search, including recent borrowed-workspace,
uncomputation, and restricted-UCG references, is stored in
[`PRIOR_ART_SEARCH_2026_09.md`](PRIOR_ART_SEARCH_2026_09.md) and
[`provenance/prior_art_search.json`](../provenance/prior_art_search.json).

Those records document the search scope. An absence of an exact match in a
bounded search is not treated as proof of novelty or priority.

## References highlighted on this page

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

Exact identifiers, versions, and local dependency locations are listed in the
[source map](SOURCE_MAP.md).

---

[← Source map](SOURCE_MAP.md) · [Complete technical note](../REVIEW.md) · [Back to the landing page →](../README.md)
