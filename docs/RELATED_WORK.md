# Related work and contribution boundary

[← Source map](SOURCE_MAP.md) · [Complete narrative](../REVIEW.md) · [Landing page →](../README.md)

The paper joins three technical lines around the same prescribed frame:

1. exact state preparation with arbitrary clean workspace;
2. Hopf coordinates and inverse-frame gradient readout;
3. precision-aware Clifford+T synthesis with clean and dirty workspace.

Borrowed-workspace and controlled-unitary constructions explain the strict-zero
schedule.  This page places the ingredients by mathematical role and keeps the
contribution narrow. The exact size–depth and approximate T-count results use
different circuit models; they do not assert simultaneous optimality of one
circuit. The [fault-tolerant theorem](FAULT_TOLERANT_COMPILER.md) states the
second model and its workspace conditions separately.

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

[Xu et al., “A Unified Framework for Optimizing Uniformly Controlled
Structures in Quantum Circuits”](https://arxiv.org/abs/2512.08675) study
restricted UCGs and synthesis savings from limited control participation.
The addressed Hopf layer is related, but its sparsity has a particular form:
one long all-zero suffix predicate is shared by every prefix-selected rotation.

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

The exact compiler contribution is the following chain.

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

## 9. Fault-tolerant lineage and the precision register

Let $N=2^n$ and let $L$ denote the requested number of accuracy bits. Three
established results are particularly close to the fault-tolerant construction.

**Gosset–Kothari–Wu (GKW).** Their Theorems 1.1–1.2 give the optimal unrestricted
T-count $\Theta(\sqrt{NL}+L)$ for state preparation and diagonal synthesis.
Their Appendix B already treats complete single-qubit multiplexors and allocates
error geometrically across state-preparation layers, obtaining
$O(\sqrt{NL}+nL)$. These are imported benchmarks and methods. A state-preparation
theorem alone does not specify the remaining columns of the Hopf frame, and an
unrestricted-ancilla theorem does not supply a prescribed clean/dirty budget.
Their Theorem 4.2 supplies the ancilla-independent lower bound used through the
frame's diagonal subfamily.

**Low–Kliuchnikov–Schaeffer (LKS).** Section 2, Table 2, Figure 1(d), and Eq. (8)
provide dirty-assisted SelectSwap lookup with exact bank restoration. For an
$m$-bit table with $D$ entries, its T count is $O(D/\lambda+m\lambda)$ with
$m\lambda$ dirty bank qubits and $O(\log D+m)$ clean wires. Appendix C also
gives exact Boolean XOR constructions using dirty auxiliaries. The basis-state
identity in Eq. (8) extends to reference-entangled inputs by linearity. We do
not claim dirty lookup or its cancellation identity as a contribution. Its
dirty bank does not replace the clean output word needed by an instruction-word
interpreter. Section 5 supplies the finite-width counting method.

**Bausch.** Equations (4) and (6) of *Fast Black-Box Quantum State Preparation*
already use a geometric precision register and a bit oracle addressed by the
data index and precision position. Section 2.3.3 includes a capped geometric
source. Its explicit exact preparation uses a linear-size unary temporary,
then binary conversion and routing cleanup. Consequently, logarithmic output
width there does not by itself establish logarithmic peak clean workspace.
The compact Gray construction used here supplies the specific simultaneous
resource guarantee: exact $O(L)$ T count, $O(\log L)$ peak clean workspace,
ordinary binary labels, and restored temporary work. The geometric weighting
and bit-oracle idea are credited to Bausch; no strict gate-count improvement
over his routing variants is asserted.

The addressed SU(2) compiler combines this source with a constant-size Pauli
linear combination and oblivious amplitude amplification. It is a
space-efficient application of these ingredients, with all preparations,
adjoints, reflections, and one-bit tables charged. It is not a new general
principle of dyadic sampling or amplitude amplification.

## 10. What the full-frame T theorem adds

The main additional construction is the uniform-in-precision composition of
complete frame corrections. A shared geometric source supplies approximate
shift amplitudes on accepted branches; the source is retained between stages.
The residual decomposition, failure tracking, and one final amplification
control the full initialized isometry while returning dirty workspace exactly.
Under the conditions in the [theorem](FAULT_TOLERANT_COMPILER.md), this gives

```math
T=\Theta\!\left(\sqrt{NL}+L+\frac{NL}{n+a+b}\right),
```

where $a$ and $b$ count clean and dirty ancillary qubits. The theorem retains
its sufficient clean-workspace reservation. A separate retained corollary for
all clean budgets, under an additional restriction on precision and dirty
width, is proved in the [borrowed-workspace appendix](BORROWED_WORKSPACE_COMPILER.md).
The lower bounds follow from GKW and LKS with the stated reductions; the
contribution is the upper construction and the resulting match in those
regimes. The all-clean-budget extension also uses the earlier borrowed-work
compiler; it is a compiler splice, not an independent lower-bound technique.

The simpler direct sampler already costs
$O(\sqrt{NL}+nL+NL/(n+a+b))$ with logarithmic precision workspace. For example,
at $L=n^2$, $a=\Theta(n)$ with sufficient headroom, and
$b=\Theta(n\sqrt N)$, it already attains $\Theta(n\sqrt N)$ T gates.
This illustrates the small-clean sampler; it is not an additional improvement
due to shared-source composition. Eliminating repeated precision charges is
the reason for the stronger uniform-precision construction.

Tan's published Theorem I.1 and Lemma IV.1 treat general unitary synthesis and
batched controlled gates. Remark IV.2 uses zeroed precision-length instruction
registers; it does not directly give the clean/dirty contract above. The
Yuan–Zhang depth theorem uses arbitrary continuous one-qubit gates, so it is not
a T-count comparison. Recent sparse-QROM and sparse-state bounds address
different input families. These distinctions delimit the use of each result;
they do not establish priority by absence of a matching theorem.

At a fixed parameter value, a full-isometry error can bound the bias of the
[bounded-score QBP estimator](QBP_APPROXIMATION.md).
This does not differentiate the compiled Clifford+T word as a function of the
parameters and does not prove optimal gradient-query complexity.

## 11. What the two-clean construction adds

The [operator-source compiler](OPERATOR_SOURCE_COMPILER.md)
uses two initialized flags and an arbitrary dirty bank. Full-space
anticommuting loaders are established by
[Kerenidis–Prakash](https://arxiv.org/html/2202.00054v2), Definitions 4.4/4.6
and Theorem 4.9; their scalar-overlap product algebra also appears in
[Chee et al.](https://arxiv.org/pdf/2301.07477), Appendix C. Dirty SelectSwap
is credited to LKS, and normalization-two amplification to
[Berry et al.](https://arxiv.org/pdf/1412.4687), Eqs. (11)–(15).

The local construction specializes the loader to native geometric weights,
programs its signs through whole-word dirty queries, and combines a scalar
block, suffix echo, and full-output amplification into the prescribed Hopf
frame. With $`b\ge L+n+7`$ it gives $`T=O(N+nL)`$; with
$`b\ge2(L+n+7)`$ its banked form gives
$`T=O(\sqrt{NL}+nL+NL/b)`$. Both use $`O(NL)`$ Clifford gates.
The operator core returns approximately within the full-isometry bound;
lookup banks and selectors return exactly. Literal diagonal compilation
also gives the phase-dressed magnitude-frame corollary with its own error
allocation and dirty-width threshold.

The remaining $`nL`$ term matters: at $`L=N`$ the two-clean result is an
$`O(N\log N)`$ upper bound, not a matched linear bound. The claimed
contribution is this explicitly charged construction and its stated resource
regimes, not the invention of loaders, dirty lookup, overlap algebra, or
amplification.

The [source map](SOURCE_MAP.md) gives exact theorem numbers and local consumers.
The comparisons identify dependencies and specific additional constructions;
they do not certify priority.

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
- C. Xu et al., [“A Unified Framework for Optimizing Uniformly Controlled
  Structures in Quantum Circuits”](https://arxiv.org/abs/2512.08675),
  arXiv:2512.08675 (2025).
- J. Bausch, [“Fast Black-Box Quantum State Preparation”](https://arxiv.org/pdf/2009.10709v4),
  arXiv:2009.10709v4 (2022), Eqs. (4), (6), and Section 2.3.3.
- G. H. Low, V. Kliuchnikov, and L. Schaeffer,
  [“Trading T gates for dirty qubits in state preparation and unitary synthesis”](https://arxiv.org/html/1812.00954v2),
  *Quantum* **8**, 1375 (2024).
- D. W. Berry, A. M. Childs, R. Cleve, R. Kothari, and R. D. Somma,
  [“Simulating Hamiltonian dynamics with a truncated Taylor series”](https://arxiv.org/pdf/1412.4687),
  *Physical Review Letters* **114**, 090502 (2015), Eqs. (11)–(15).
- D. Gosset, R. Kothari, and K. Wu,
  [“Quantum state preparation with optimal T-count”](https://quantum-journal.org/papers/q-2026-07-22-2168/pdf/),
  *Quantum* **10**, 2168 (2026).
- X. Tan, [“Unitary Synthesis with Fewer T Gates”](https://journals.aps.org/prxquantum/pdf/10.1103/pxhd-9s9q),
  *PRX Quantum* **7**, 033058 (2026).
- T. Li, F. Ou, X. Wang, P. Yao, P. Yuan, and S. Zhang,
  [“Optimal T Counts under Sparsity: from QROM to State Preparation and Block Encoding”](https://arxiv.org/html/2607.28260v1),
  arXiv:2607.28260v1 (2026).

---

[← Source map](SOURCE_MAP.md) · [Complete narrative](../REVIEW.md) · [Landing page →](../README.md)
