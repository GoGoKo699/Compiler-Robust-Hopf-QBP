# Expanded prior-art search for the strict-zero Hopf compiler

## Status and limitation

Search date: **2026-09-03**.

This is a technical literature search intended to discipline the repository and
manuscript claims. It is **not external peer review**, not an exhaustive patent
or legal search, and **not a legal novelty opinion**. Failure to find an exact
match is not evidence that none exists.

The searched construction is the following Hopf-specific reduction:

> At addressed tree depth $d$, borrow one original lower-suffix data qubit as a
> restored predicate carrier, use four predicate toggles and a half-angle echo,
> aggregate every prefix-dependent rotation into two total-width-$d+2$ UCGs,
> and obtain $\Theta\!\left(2^n\right)$ size and $\Theta\!\left(n+\frac{2^n}{n}\right)$ depth for the complete
> strict-zero Hopf differential frame.

The search separates novelty of this aggregate construction from novelty of its
individual ingredients.

## 1. Search families

The review used combinations of the following concepts:

```text
borrowed qubit / dirty ancilla / conditionally clean ancilla
safe uncomputation / restored logical qubit / in-place workspace
controlled-unitary square root / Pauli conjugation / echo cancellation
uniformly controlled gate / quantum multiplexor / multiplexed rotation
sparse UCG / restricted UCG / identity blocks / zero-suffix control
multi-controlled SU(2) / ancilla-free controlled rotation
predicate carrier / borrowed target / borrowed control
```

References cited by the active Yuan--Zhang framework and by the main
borrowed-qubit papers were also inspected.

## 2. Nearest prior work

### Barenco et al.: controlled-unitary square roots

A. Barenco et al., “Elementary gates for quantum computation,” *Physical
Review A* **52**, 3457--3467 (1995),
[doi:10.1103/PhysRevA.52.3457](https://doi.org/10.1103/PhysRevA.52.3457),
[arXiv:quant-ph/9503016](https://arxiv.org/abs/quant-ph/9503016).

**Overlap.** The paper establishes the use of roots of a target unitary,
controlled-NOT gates, and conjugation identities in exact controlled-unitary
decompositions. It is the appropriate lineage for the algebraic pattern
$C^2=U$ together with an involution that maps $C$ to $C^{-1}$.

**Difference.** It does not present the Hopf addressed-layer problem, the
zero-suffix predicate, or the two-UCG aggregation across all prefix values.

**Claim consequence.** Do not claim invention of square-root/conjugation
control identities.

### Möttönen and Bergholm et al.: uniformly controlled rotations and gates

M. Möttönen et al., “Transformation of quantum states using uniformly
controlled rotations,” *Quantum Information and Computation* **5**, 467--473
(2005), [arXiv:quant-ph/0407010](https://arxiv.org/abs/quant-ph/0407010).

V. Bergholm et al., “Quantum circuits with uniformly controlled one-qubit
gates,” *Physical Review A* **71**, 052330 (2005),
[doi:10.1103/PhysRevA.71.052330](https://doi.org/10.1103/PhysRevA.71.052330),
[arXiv:quant-ph/0410066](https://arxiv.org/abs/quant-ph/0410066).

**Overlap.** These papers establish the multiplexor/UCG circuit lineage used in
both the older `Hopf-QBP` compiler and the present construction.

**Difference.** A direct full-width Möttönen transform of the logically sparse
zero-suffix angle table is generically dense in its physical Walsh/Gray-code
angles. The strict-zero construction instead factors the predicate through one
restored system bit and uses two smaller UCGs.

**Claim consequence.** The UCG primitive is imported. The project claim is the
Hopf-specific reduction to a constant number of smaller UCGs per depth.

### Yuan and Zhang: all-ancilla exact UCG and QSP frontier

P. Yuan and S. Zhang, “Optimal (controlled) quantum state preparation and
improved unitary synthesis by quantum circuits with any number of ancillary
qubits,” *Quantum* **7**, 956 (2023),
[doi:10.22331/q-2023-03-20-956](https://doi.org/10.22331/q-2023-03-20-956).

**Overlap.** Lemma 5 supplies exact ancilla-free multi-controlled X; Lemma 6
supplies the exact UCG size--depth tradeoff; Lemma 9 supplies coherent
copy--use--uncopy; Theorem 2 supplies the optimal QSP benchmark.

**Difference.** The paper does not construct the Hopf differential frame or the
borrowed-suffix echo, and state preparation constrains only one input column.

**Claim consequence.** Yuan--Zhang is the sole active external compiler
framework. The frame construction and its frame-safe QBP consequence belong to
this project.

### Low, Kliuchnikov, and Schaeffer: dirty qubits in state preparation

G. H. Low, V. Kliuchnikov, and L. Schaeffer, “Trading T gates for dirty qubits
in state preparation and unitary synthesis,” *Quantum* **8**, 1375 (2024),
[doi:10.22331/q-2024-06-17-1375](https://doi.org/10.22331/q-2024-06-17-1375),
[arXiv:1812.00954](https://arxiv.org/abs/1812.00954).

**Overlap.** The work uses unknown-state qubits to reduce fault-tolerant
state-preparation and unitary-synthesis cost and is relevant to the broad dirty-
qubit lineage.

**Difference.** Its principal resource is approximate Clifford+T/T-count, and
its arbitrary-data oracle construction is not the exact addressed Hopf-layer
echo in the arbitrary-one-qubit-plus-CNOT model.

### Claudon et al.: borrowed qubits and controlled-unitary roots

B. Claudon et al., “Polylogarithmic-depth controlled-NOT gates without ancilla
qubits,” *Nature Communications* **15**, 5886 (2024),
[doi:10.1038/s41467-024-50065-x](https://doi.org/10.1038/s41467-024-50065-x),
[arXiv:2312.13206](https://arxiv.org/abs/2312.13206).

**Overlap.** The paper develops exact multi-controlled constructions using a
borrowed qubit and discusses roots of controlled target unitaries.

**Difference.** It addresses multi-controlled gates rather than a family of
prefix-selected rotations aggregated into two UCGs while one logical predicate
bit is restored.

### Khattar and Gidney: conditionally clean ancillas and toggle detection

T. Khattar and C. Gidney, “Rise of conditionally clean ancillae for efficient
quantum circuit constructions,” *Quantum* **9**, 1752 (2025),
[doi:10.22331/q-2025-05-21-1752](https://doi.org/10.22331/q-2025-05-21-1752),
[arXiv:2407.17966](https://arxiv.org/abs/2407.17966).

**Overlap.** The paper formalizes conditionally clean system qubits and
laddered toggle detection, including the cancellation overhead incurred when a
clean work bit is replaced by an unknown-state bit.

**Difference.** Standard toggle detection is naturally phrased for a
self-inverse consumed operation. A generic Hopf rotation is not self-inverse,
and the borrowed suffix bit is itself part of the predicate. The present circuit
uses a half-angle square root and Pauli conjugation so that the unwanted branch
cancels while the desired branch squares to the full rotation.

**Claim consequence.** Do not claim invention of dirty/conditionally clean
borrowing or toggle detection.

### Zindorf and Bose: ancilla-free multi-controlled SU(2)

B. Zindorf and S. Bose, “Efficient implementation of multi-controlled quantum
gates,” *Physical Review Applied* **24**, 044030 (2025),
[arXiv:2404.02279](https://arxiv.org/abs/2404.02279).

**Overlap.** The paper gives linear-cost exact multi-controlled special-unitary
gates without ancillary qubits and is directly relevant to individual
conditioned rotations.

**Difference.** Applying one multi-controlled rotation separately for each of
the $2^d$ prefixes would not by itself provide the reviewed aggregate depth
bound. The Hopf construction collects all prefix values into two UCGs and pays
the long suffix predicate only a constant number of times per tree depth.

### Xu et al.: restricted and sparse UCGs

C. Xu et al., “A Unified Framework for Optimizing Uniformly Controlled
Structures in Quantum Circuits,” arXiv:2512.08675v2 (2025),
[arXiv:2512.08675](https://arxiv.org/abs/2512.08675).

**Overlap.** This work develops restricted UCG models and size/depth bounds that
exploit sparsity in participating controls.

**Difference.** The reviewed Hopf layer has a long all-zero suffix predicate and
a logically sparse block table that is generically dense under the ordinary
Möttönen angle transform. The present search did not locate the same
borrowed-suffix two-UCG reduction in the rUCG framework.

**Claim consequence.** Restricted-UCG work must be cited and compared, but the
absence of an apparent exact match is not a novelty proof.

### Su et al.: formal semantics of dirty-qubit borrowing

B. Su, L. Zhou, Y. Feng, and M. Ying, “Borrowing Dirty Qubits in Quantum
Programs,” *ASPLOS 2026*, 274--289,
[arXiv:2508.17190](https://arxiv.org/abs/2508.17190).

**Overlap.** The work formalizes borrowing and safe uncomputation, including the
requirement that unknown states and entanglement be restored.

**Difference.** It is a programming-language and verification treatment rather
than this exact synthesis identity. It reinforces why computational-basis tests
alone are insufficient and why the complete operator factorization must restore
the logical suffix qubit.

### Bona and recent uncomputation work

X. Xu et al., “Bona: Automatic Management of Dirty Ancilla Borrowing in Quantum
Circuits,” arXiv:2608.08765 (2026).

C. Liu, L. Zhou, and B. Meng, “Quantum Uncomputation of Clean and Dirty Ancilla
Qubits,” arXiv:2608.09578 (2026).

**Overlap.** These works address scheduling, verification, and structured
uncomputation of unknown-state work qubits.

**Difference.** They do not appear to supply the Hopf-specific two-UCG layer
reduction or its exact size--depth summation. Their relevance is to restoration
semantics and compiler automation.

## 3. Comparison table

| Prior line | Shared ingredient | Missing reviewed ingredient |
|---|---|---|
| Barenco controlled-unitary decompositions | square roots and conjugation | zero-suffix Hopf multiplexor aggregation |
| Möttönen/Bergholm UCGs | prefix-selected rotations | in-place elimination of the clean suffix flag |
| Yuan--Zhang | exact UCG/MCT depth and QSP optimum | complete Hopf-frame construction |
| Low--Kliuchnikov--Schaeffer | dirty-qubit resource tradeoffs | exact logical-depth Hopf layer |
| Claudon et al. | borrowed qubits and controlled roots | two-UCG family aggregation |
| Khattar--Gidney | conditionally clean qubits and toggle detection | non-self-inverse Hopf echo with original-bit predicate |
| Zindorf--Bose | ancilla-free controlled SU(2) | aggregate prefix multiplexor depth |
| Xu et al. rUCG | UCG sparsity framework | identified borrowed-suffix reduction |
| Su et al.; Bona; Liu et al. | safe restoration and uncomputation | exact Hopf synthesis and frontier |

## 4. Negative search result and its meaning

Within the sources and query families above, the search did not identify a
published or preprint construction with all of the following features at once:

1. the borrowed wire is one of the original logical suffix bits;
2. the desired operation depends on that wire's original value;
3. the unwanted unknown-bit branch is cancelled by a half-angle/Pauli echo;
4. all $2^d$ prefix-dependent rotations are aggregated into two total-width-
   $d+2$ UCGs;
5. summing the Hopf tree gives an exact complete-frame $\Theta\!\left(2^n\right)$ size and
   $\Theta\!\left(n+\frac{2^n}{n}\right)$ depth result.

This is a **negative result of a bounded search**, not a proof of novelty or
priority. Equivalent circuits may appear under different terminology, and
unindexed theses, patents, software, or unpublished notes may exist.

## 5. Claim-safe wording

The manuscript may claim the following, subject to independent review:

> For the addressed Hopf differential frame, an original suffix data qubit can
> be used as a restored in-place predicate carrier. A four-toggle half-angle
> echo reduces all prefix-dependent rotations at depth $d$ to two total-width-
> $d+2$ UCGs and linear-size predicate toggles. This yields an exact
> ancilla-free complete-frame compiler attaining the state-preparation-optimal
> size--depth frontier.

The manuscript should not claim:

- invention of borrowed or dirty ancillas;
- invention of conditionally clean ancillas or toggle detection;
- the first square-root controlled-unitary echo;
- novelty of the abstract four-toggle identity in all circuit settings;
- absence of equivalent prior circuits;
- a legal determination of novelty.

## 6. Remaining search gate

Before submission, an independent circuit-synthesis specialist should:

1. inspect circuit diagrams and appendices of the closest references, not only
   abstracts;
2. follow their cited and citing literature for borrowed-control multiplexors;
3. search theses, patents, and software implementations for equivalent in-place
   predicate carriers;
4. compare the reviewed circuit up to gate reversal, control inversion,
   relabeling, and replacement of $X$ by another anticommuting involution;
5. approve or narrow the Hopf-specific novelty statement.

Until then, the repository should describe the construction as an internally
audited Hopf-specific synthesis with familiar ingredients.