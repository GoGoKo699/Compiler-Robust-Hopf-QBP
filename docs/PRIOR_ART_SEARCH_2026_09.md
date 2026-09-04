# Expanded source search for the strict-zero Hopf compiler

[← Focused prior-art boundary](STRICT_ZERO_PRIOR_ART.md) · [Related work](RELATED_WORK.md) · [Source map](SOURCE_MAP.md)

## Status and limitation

Search date: **2026-09-03**.

This document records a technical source search used to discipline the
repository and manuscript claims. It is not external peer review, it is not an
exhaustive patent or legal search, and it is not a legal novelty opinion.
Failure to find an exact match is not evidence that none exists.

The searched construction is the following Hopf-specific reduction:

> At addressed tree depth `d`, one original lower-suffix data qubit is borrowed
> as a restored predicate carrier. Four predicate toggles and a half-angle echo
> aggregate every prefix-dependent rotation into two total-width-`d+2` UCGs.
> Summing the layers gives `Theta(2^n)` size and `Theta(n+2^n/n)` depth for the
> complete strict-zero Hopf differential frame.

The search distinguishes this aggregate operator reduction from its individual
circuit ingredients.

## 1. Search families

The search used combinations of:

```text
borrowed qubit / dirty ancilla / conditionally clean ancilla
safe uncomputation / restored logical qubit / in-place workspace
controlled-unitary square root / Pauli conjugation / echo cancellation
uniformly controlled gate / quantum multiplexor / multiplexed rotation
sparse UCG / restricted UCG / identity blocks / zero-suffix control
multi-controlled SU(2) / ancilla-free controlled rotation
predicate carrier / borrowed target / borrowed control
```

References cited by the all-workspace state-preparation framework and by the
closest borrowed-workspace papers were also followed.

## 2. State-preparation and UCG line

### Möttönen et al. and Bergholm et al.

M. Möttönen et al., “Transformation of quantum states using uniformly
controlled rotations,” *Quantum Information and Computation* **5**, 467–473
(2005), arXiv:quant-ph/0407010.

V. Bergholm et al., “Quantum circuits with uniformly controlled one-qubit
gates,” *Physical Review A* **71**, 052330 (2005),
doi:10.1103/PhysRevA.71.052330, arXiv:quant-ph/0410066.

**Overlap.** These papers establish the multiplexor and UCG circuit language
used in state preparation, the earlier Möttönen-style Hopf-QBP compiler, and the
present construction.

**Distinction.** The logical Hopf angle table is sparse in the zero-suffix
basis, but its ordinary full-width Möttönen transform is generically dense in
the physical Walsh/Gray-code angles. The present circuit factors the predicate
through one restored logical bit and uses two smaller UCGs.

**Claim consequence.** UCGs and multiplexed rotations are imported. The local
claim is the Hopf-specific factorization and its complete-frame resource
consequence.

### Sun et al.

X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, “Asymptotically Optimal
Circuit Depth for Quantum State Preparation and General Unitary Synthesis,”
*IEEE TCAD* **42**, 3301–3314 (2023),
doi:10.1109/TCAD.2023.3244885.

**Overlap.** This paper establishes the preceding ancilla–depth landscape for
state preparation and general unitary synthesis and is the original source
credited for selected primitives later restated in the uniform framework.

**Claim consequence.** It is the historical predecessor. The present proof uses
the later uniform all-workspace theorem as its active benchmark rather than
selecting separate published regimes.

### Yuan and Zhang

P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
improved unitary synthesis by quantum circuits with any number of ancillary
qubits,” *Quantum* **7**, 956 (2023),
doi:10.22331/q-2023-03-20-956.

**Overlap.** Theorem 2 supplies the optimal QSP frontier. Lemma 5 supplies exact
ancilla-free multi-controlled `X`; Lemma 6 supplies the UCG size–depth tradeoff;
Lemma 9 supplies coherent copy–use–uncopy.

**Relation to the present problem.** The paper solves the state-preparation and
controlled state-preparation tasks in a uniform workspace model. Once the Hopf
frame is exposed as addressed complete-operator layers and routed subtree direct
sums, those primitives can be adapted to the prescribed completion.

**Claim consequence.** Yuan–Zhang is the sole active external compiler
framework. The Hopf-specific contribution is the complete-operator adaptation,
not a new elementary UCG or MCT synthesis.

## 3. Controlled roots and borrowed workspace

### Barenco et al.

A. Barenco et al., “Elementary gates for quantum computation,” *Physical
Review A* **52**, 3457–3467 (1995),
doi:10.1103/PhysRevA.52.3457, arXiv:quant-ph/9503016.

**Overlap.** The paper establishes controlled-unitary constructions using roots
of target unitaries, controlled-NOT gates, and conjugation identities. It is the
appropriate lineage for

```math
C^2=U,
\qquad
JCJ=C^{-1}.
```

**Claim consequence.** The manuscript should not claim invention of
square-root/conjugation control identities.

### Low, Kliuchnikov, and Schaeffer

G. H. Low, V. Kliuchnikov, and L. Schaeffer, “Trading T gates for dirty qubits
in state preparation and unitary synthesis,” *Quantum* **8**, 1375 (2024),
doi:10.22331/q-2024-06-17-1375, arXiv:1812.00954.

**Overlap.** Unknown-state qubits are used to reduce fault-tolerant
state-preparation and unitary-synthesis cost.

**Distinction.** The principal model is approximate Clifford+T and T-count. The
strict-zero Hopf result is an exact logical-depth theorem in the
arbitrary-one-qubit+CNOT model.

### Claudon et al.

B. Claudon et al., “Polylogarithmic-depth controlled-NOT gates without ancilla
qubits,” *Nature Communications* **15**, 5886 (2024),
doi:10.1038/s41467-024-50065-x, arXiv:2312.13206.

**Overlap.** The work develops exact multi-controlled constructions using a
borrowed qubit and controlled target-unitary roots.

**Distinction.** The searched Hopf circuit aggregates a family of prefix-
selected rotations into two UCGs while restoring a logical predicate bit whose
original value is part of the activation condition.

### Khattar and Gidney

T. Khattar and C. Gidney, “Rise of conditionally clean ancillae for efficient
quantum circuit constructions,” *Quantum* **9**, 1752 (2025),
doi:10.22331/q-2025-05-21-1752, arXiv:2407.17966.

**Overlap.** The paper formalizes conditionally clean system qubits and
laddered toggle detection, including restoration requirements when a clean work
bit is replaced by an unknown-state bit.

**Distinction.** Standard toggle detection is most direct for a self-inverse
consumed operation. A generic Hopf rotation is not self-inverse, and the
borrowed suffix bit belongs to the predicate itself. The half-angle root and
Pauli conjugation make the unwanted branch cancel while the desired branch
squares to the full rotation.

**Claim consequence.** Borrowed and conditionally clean workspace and toggle
detection are established ideas.

## 4. Ancilla-free controlled rotations and restricted UCGs

### Zindorf and Bose

B. Zindorf and S. Bose, “Efficient implementation of multi-controlled quantum
gates,” *Physical Review Applied* **24**, 044030 (2025),
arXiv:2404.02279.

**Overlap.** Zindorf and Bose give efficient exact multi-controlled special-
unitary gates without ancillary qubits.

**Distinction.** Implementing one multi-controlled rotation separately for each
of the `2^d` prefixes does not by itself provide the aggregate Hopf depth bound.
The present construction collects all prefix values into two UCGs and pays the
long suffix predicate only a constant number of times per tree depth.

### Xu et al.

C. Xu et al., “A Unified Framework for Optimizing Uniformly Controlled
Structures in Quantum Circuits,” arXiv:2512.08675v2 (2025).

**Overlap.** This work develops restricted UCG models and size–depth bounds that
exploit structural sparsity.

**Distinction.** The addressed Hopf layer has a long all-zero suffix predicate
and a logically sparse block table that is generically dense under the ordinary
Möttönen angle transform. The bounded search did not locate the same restored-
suffix two-UCG reduction within the restricted-UCG framework.

**Claim consequence.** Restricted-UCG work is close context. The absence of an
apparent exact match is not a novelty proof.

## 5. Restoration semantics and compiler automation

### Su et al.

B. Su, L. Zhou, Y. Feng, and M. Ying, “Borrowing Dirty Qubits in Quantum
Programs,” *ASPLOS 2026*, 274–289, arXiv:2508.17190.

**Overlap.** Borrowing Dirty Qubits in Quantum Programs formalizes borrowing and
safe uncomputation, including restoration of unknown states and entanglement.

**Distinction.** It is a programming-language and verification treatment rather
than the exact Hopf synthesis identity. Its semantics reinforce why
computational-basis preparation tests alone are insufficient.

### Bona and related uncomputation work

X. Xu et al., “Bona: Automatic Management of Dirty Ancilla Borrowing in Quantum
Circuits,” arXiv:2608.08765 (2026).

C. Liu, L. Zhou, and B. Meng, “Quantum Uncomputation of Clean and Dirty Ancilla
Qubits,” arXiv:2608.09578 (2026).

**Overlap.** Bona and Quantum Uncomputation of Clean and Dirty Ancilla Qubits
address scheduling, verification, and structured restoration of unknown-state
work qubits.

**Distinction.** The searched sources do not appear to supply the same Hopf-
specific two-UCG layer reduction or its complete-frame size–depth summation.
Their closest role is restoration semantics and possible compiler automation.

## 6. Comparison table

| Prior line | Shared ingredient | Hopf-specific ingredient examined here |
|---|---|---|
| Barenco controlled-unitary decompositions | roots and conjugation | zero-suffix multiplexor aggregation |
| Möttönen/Bergholm UCGs | prefix-selected rotations | in-place elimination of the clean suffix flag |
| Sun et al. | state-preparation ancilla–depth landscape | historical precursor to the active all-workspace framework |
| Yuan–Zhang | exact UCG/MCT/copy primitives and QSP optimum | prescribed complete-frame adaptation |
| Low–Kliuchnikov–Schaeffer | dirty-qubit resource tradeoffs | exact logical-depth Hopf layer |
| Claudon et al. | borrowed qubits and controlled roots | two-UCG family aggregation with original-bit predicate |
| Khattar–Gidney | conditionally clean workspace and toggle detection | non-self-inverse half-angle/Pauli echo |
| Zindorf–Bose | ancilla-free controlled `SU(2)` | aggregate prefix multiplexor depth |
| restricted-UCG work | structured multiplexors | restored-suffix physical width reduction |
| Su et al.; Bona; Liu et al. | safe restoration and uncomputation | exact Hopf synthesis and frontier |

## 7. Negative search result and its meaning

Within the sources and query families above, the search did not identify a
construction with all of the following features at once:

1. the borrowed wire is one of the original logical suffix bits;
2. the desired operation depends on that wire's original value;
3. the unwanted branch is cancelled by a half-angle/Pauli echo;
4. all `2^d` prefix-dependent rotations are aggregated into two total-width-
   `d+2` UCGs;
5. summing the Hopf tree gives an exact complete-frame `Theta(2^n)` size and
   `Theta(n+2^n/n)` depth theorem.

This is a **negative result of a bounded search**, not proof of novelty or
priority. Equivalent circuits may appear under different terminology, and
unindexed theses, patents, software, or unpublished notes may exist.

## 8. Claim-safe wording

Subject to independent assessment, a narrow statement is:

> For one addressed Hopf depth, an original suffix data qubit can serve as a
> restored in-place predicate carrier. A four-toggle half-angle echo reduces all
> prefix-dependent rotations to two total-width-`d+2` UCGs and linear predicate
> toggles. Summing the tree yields an exact ancilla-free complete-frame compiler
> attaining the state-preparation-optimal size–depth frontier.

The manuscript should not claim:

- invention of borrowed or dirty ancillas;
- invention of conditionally clean ancillas or toggle detection;
- the first square-root controlled-unitary echo;
- novelty of the abstract four-toggle identity in all circuit settings;
- absence of equivalent prior circuits;
- a legal determination of novelty.

## 9. Remaining search gate

Before submission, an independent circuit-synthesis specialist should:

1. inspect circuit diagrams and appendices of the closest sources, not only
   abstracts;
2. follow cited and citing literature for borrowed-control multiplexors;
3. search theses, patents, and software for equivalent in-place predicate
   carriers;
4. compare circuits up to reversal, control inversion, relabeling, and
   replacement of `X` by another anticommuting involution;
5. approve or narrow the Hopf-specific contribution statement.

Until then, the repository describes the construction as an internally audited
Hopf-specific synthesis assembled from familiar ingredients.

---

[← Focused prior-art boundary](STRICT_ZERO_PRIOR_ART.md) · [Related work](RELATED_WORK.md) · [Source map](SOURCE_MAP.md)
