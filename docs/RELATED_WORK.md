# Related work and contribution boundary

[← Source map](SOURCE_MAP.md) · [Read the complete narrative](../REVIEW.md) · [Back to the landing page →](../README.md)

The compiler result sits at the meeting point of two lines of work:

1. exact quantum state preparation and uniformly controlled gates;
2. Hopf-coordinate geometry and quantum backpropagation.

A third line—borrowed, dirty, and conditionally clean workspace—helps explain
the strict-zero circuit. The purpose of this page is to show how these ideas fit
together without attributing familiar circuit ingredients to the present work.

<p align="center">
  <img src="../assets/literature-lineage.svg" width="940" alt="The state-preparation and Hopf-geometry lines meet in the optimal complete-frame compiler." />
</p>

## 1. Optimal state preparation and the active compiler framework

Yuan and Zhang give a unified exact construction for arbitrary controlled state
preparation and determine the optimal size and depth of arbitrary state
preparation for every clean-ancillary budget. In the notation of this
repository, their state-preparation frontier is

```math
S_{\mathrm{QSP}}(n,m)=\Theta(2^n),
```

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right).
```

Their paper is the sole active external compiler framework and comparison
benchmark here. The present proof also uses their exact statements for:

- ancilla-free multi-controlled X;
- uniformly controlled one-qubit gates with arbitrary workspace;
- coherent copy–use–uncopy by CNOT trees.

These results can be adapted after the special structure of the Hopf
differential frame is exposed. The adaptation is not direct: ordinary state
preparation constrains one initialized column, while the Hopf global-gradient
protocol uses the inverse of a complete unitary with designated tangent-marker
columns.

The earlier paper of Sun, Tian, Yang, Yuan, and Zhang established the preceding
broad ancilla–depth landscape and remains an important historical reference. It
is cited briefly rather than treated as a second active compiler, because the
later Yuan–Zhang theorem supplies the uniform all-workspace frontier used in the
comparison.

## 2. Uniformly controlled gates and the Möttönen connection

The state-preparation constructions of Möttönen and coauthors, and the general
uniformly controlled one-qubit gates developed by Bergholm and coauthors,
provide the multiplexor language underlying both the older optimized Hopf-QBP
compiler and the present work.

At one Hopf depth, the logical block table is sparse: only the blocks whose lower
suffix is zero contain a nontrivial rotation. A direct full-width Möttönen
transformation does not automatically preserve that sparsity. The corresponding
Walsh/Gray-code physical angles are generically repeated across all suffix
frequencies, so compiling each depth as a full `n`-qubit multiplexor pays for a
dense table.

The strict-zero construction keeps the multiplexor narrow instead. It uses one
original suffix data qubit as a restored predicate carrier and replaces one
addressed layer by two total-width-`d+2` UCGs plus linear-size predicate
toggles. Thus the Möttönen/Bergholm line is both a technical precursor and the
natural language in which the new reduction is stated.

## 3. Borrowed and conditionally clean workspace

The strict-zero echo is close in spirit to several established techniques.

Barenco and coauthors use roots of target unitaries and conjugation identities
in exact controlled-unitary decompositions. Claudon and coauthors develop exact
multi-controlled constructions using borrowed qubits and controlled roots.
Khattar and Gidney formalize conditionally clean qubits and toggle-detection
patterns that replace clean workspace by unknown-state logical qubits. Work by
Zindorf and Bose gives efficient ancilla-free multi-controlled `SU(2)` gates.

The present Hopf layer combines these familiar ingredients in a specific way.
Let

```math
C_p=R_y(\theta_p/2).
```

The relations

```math
C_p^2=R_y(\theta_p),
\qquad
X C_p X=C_p^{-1}
```

make the desired original-suffix-zero branch square to the full rotation while
the unwanted value of the borrowed suffix bit cancels. The borrowed qubit is
not an extra dirty ancillary wire: it remains part of the logical input, the
desired operation depends on its original value, and the complete operator
proof restores it exactly.

### Claim boundary beside the strict-zero result

The repository does **not** claim invention of:

- borrowed or dirty qubits;
- conditionally clean ancillas;
- toggle detection;
- square-root controlled-unitary decompositions;
- Pauli-conjugation echoes;
- uniformly controlled gates.

The narrow project-specific contribution is:

> For an addressed Hopf depth, one original suffix data qubit serves as a
> restored in-place predicate carrier, reducing all prefix-dependent rotations
> to two total-width-`d+2` UCGs and linear predicate toggles. Summing these
> layers gives the optimal strict-zero complete-frame frontier.

This wording attributes the familiar ingredients while identifying the exact
operator reduction and resource consequence established here.

## 4. Restricted and sparse UCG synthesis

Recent work on restricted or sparse uniformly controlled structures asks when a
UCG can exploit limited participation of controls or repeated block patterns.
That perspective is closely related to the addressed Hopf layer.

The difficulty here is that the long all-zero suffix predicate is logically
sparse but generically dense under the ordinary Möttönen angle transform. The
borrowed-suffix echo avoids compiling that full table. It first factors the
predicate through a restored logical bit, then applies two smaller UCGs whose
block count depends on the prefix width.

The repository therefore cites restricted-UCG work as the closest structural
context while making the Hopf-specific factorization explicit.

## 5. Hopf coordinates and the differential frame

The first Hopf paper develops the balanced binary coordinate chart for arbitrary
real and complex pure states. It supplies:

- the forward state map;
- an explicit inverse coordinate map;
- a diagonal pullback metric;
- normalized coordinate tangents;
- exact tangent-state preparation;
- the original indexed gradient interface.

The second Hopf paper turns the normalized magnitude directions into a complete
addressed differential frame and uses controlled observable interference to
recover shared gradient records. One global magnitude outcome contributes to
every magnitude coordinate, while complex leaf phases use a direct one-hot
record. A checkpoint method provides selected-depth locality.

The compiler question begins only after those interfaces are fixed:

```math
W_{\mathbb R}|0^n\rangle=|\psi\rangle,
\qquad
W_{\mathbb R}|\lambda(j)\rangle=|e_j\rangle.
```

The new synthesis result proves that this complete frame—not only its prepared
state column—can attain the optimal state-preparation size–depth frontier.

## 6. Comparison by mathematical role

| Work or line | Object compiled or analyzed | Resource or structural result used | Hopf-specific adaptation in this repository |
|---|---|---|---|
| Möttönen et al.; Bergholm et al. | multiplexed rotations and general UCGs | exact block-diagonal one-qubit-gate language | addressed depths are factored into smaller UCGs rather than full-width sparse tables |
| Sun et al. | exact state preparation and general unitary synthesis | historical broad ancilla–depth landscape | cited as the predecessor to the uniform frontier |
| Yuan–Zhang | controlled state preparation, UCGs, MCTs, coherent copying | optimal QSP frontier for every `m`; active circuit primitives | complete Hopf frame is decomposed so those primitives can act without losing tangent columns |
| Barenco et al.; Claudon et al. | controlled unitaries, roots, borrowed-qubit constructions | square-root and conjugation lineage | one logical suffix bit carries and then releases the zero-suffix predicate |
| Khattar–Gidney | conditionally clean workspace and toggle detection | cancellation and safe restoration of unknown-state qubits | a non-self-inverse Hopf rotation is handled by a half-angle/Pauli echo |
| Zindorf–Bose | ancilla-free multi-controlled `SU(2)` | context for individual conditioned rotations | all prefix values are aggregated into two UCGs, avoiding one rotation family per prefix |
| restricted-UCG work | sparsity and limited control participation | structured multiplexor context | logical suffix sparsity is converted into a smaller physical UCG width |
| first Hopf paper | state chart, inverse, metric, normalized tangents | differential geometry and coordinate interface | supplies the structured columns that must be preserved |
| Hopf-QBP paper | global, phase, and checkpoint gradient records | inverse-frame backpropagation interface | frame-safe compilation is separated from state-column equality and made optimal |

## 7. What is new at the level of the full theorem

The full contribution is not one isolated circuit identity. It is the theorem
chain:

1. identify complete frame safety as the compiler contract relevant to the
   global Hopf record;
2. show by exact counterexample that state-column equality is weaker;
3. exploit the addressed Hopf layers and tree-cut direct sum;
4. close strict zero workspace with the borrowed-suffix echo;
5. use clean decoding and coherent routing for positive workspace;
6. match the optimal state-preparation size–depth frontier for every `m>=0`;
7. transport the result to the separated complex frame and the global QBP
   protocol.

The result is specific to the structured Hopf differential frame. It does not
assert that a generic family of `2^n` orthonormal columns can be compiled at
state-preparation cost.

## 8. Technical search record

The broader source-by-source search, including recent borrowed-workspace,
uncomputation, and restricted-UCG references, is preserved in
[`PRIOR_ART_SEARCH_2026_09.md`](PRIOR_ART_SEARCH_2026_09.md) and
[`provenance/prior_art_search.json`](../provenance/prior_art_search.json).

Those files document search scope and citation discipline. They are not part of
the mathematical proof, and an absence of an exact match in a bounded search is
not treated as proof of novelty or priority.

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

Exact identifiers and local dependency locations are listed in
[the source map](SOURCE_MAP.md).

---

[← Source map](SOURCE_MAP.md) · [Read the complete narrative](../REVIEW.md) · [Back to the landing page →](../README.md)
