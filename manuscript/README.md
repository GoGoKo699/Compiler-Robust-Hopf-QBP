# Manuscript guide

[Publication scope](PUBLICATION_SCOPE.md) · [Read the argument](../REVIEW.md) · [Verification](../docs/VERIFICATION.md)

Working title: **Exact and Fault-Tolerant Compilation of Hopf Differential Frames**.

The [publication scope](PUBLICATION_SCOPE.md) fixes the three principal
results and their corollaries. The exact theorem covers every $m\geq0$
clean-workspace budget; the two T-count constructions keep their distinct
clean/dirty reservations and return guarantees.

## Target journal

**Target: PRX Quantum, as a full-length research article.** The author selected
this goal on 22 September 2026. Scientific development and verification come
before final manuscript writing.

The journal's [editorial criteria](https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.6.020001)
require an exceptional advance, connection, capability, or insight. The
scientific case pursued here is a compiler capability: preserving an entire
operationally required frame while controlling exact entangling cost,
fault-tolerant precision cost, and initialized versus borrowed workspace.
The two-clean diagonal and general one-target multiplexor results also cover
standard operator families beyond Hopf frames. This is the intended significance argument, not a prediction of
an editorial decision.

The closest venue precedents are Yuan–Zhang's
[exact state-preparation tradeoffs](https://quantum-journal.org/papers/q-2023-03-20-956/)
(Quantum 7, 956), Low–Kliuchnikov–Schaeffer's
[dirty-workspace tradeoffs](https://quantum-journal.org/papers/q-2024-06-17-1375/)
(Quantum 8, 1375), and Gosset–Kothari–Wu's
[optimal T-count](https://quantum-journal.org/papers/q-2026-07-22-2168/)
(Quantum 10, 2168). The manuscript must explain the new complete-operator
guarantees relative to these results, with the attribution in the source map.

The [related-work comparison](../docs/RELATED_WORK.md) includes newer synthesis
results and distinguishes their input contracts and workspace assumptions.
The opening pages should explain why the prescribed frame
requires more than state preparation, identify the new proof mechanisms,
and state Results A–C with their resource assumptions. QBP provides the
operational motivation and consequence. The exact and fault-tolerant models
remain parts of one operator-compilation story; the open endpoint remains
in the discussion.

At submission preparation, follow the current
[PRX Quantum author guidance](https://journals.aps.org/prxquantum/authors),
including a cover letter explaining significance, a popular summary, data
availability, and disclosure of substantive AI assistance. These presentation
tasks follow the scientific package and the complete draft.

## Paper order

1. Prescribed completion versus one-column state preparation, with the
   two-qubit readout example.
2. Shared Hopf-frame and complete-input compiler contract.
3. Exact all-workspace size/depth theorem and its proof mechanisms.
4. Sufficient-clean matching T theorem, followed by the two-clean construction
   and its bank, diagonal, general multiplexor, and complex-magnitude corollaries.
5. Exact and approximate fixed-parameter QBP consequences, including complete
   complex gradients and the costs of classical preprocessing and output.
6. The remaining endpoint gap and the limits of the circuit model.

Detailed schedules, source preparation, reversible lookup, error estimates,
and resource sums form the technical appendices. The exact toolkit credits
Yuan and Zhang; the [source map](../docs/SOURCE_MAP.md) gives the complete
attribution. Exploratory research is outside the selected manuscript.

The current task is to finish and integrate the scientific ingredients listed
in the [publication scope](PUBLICATION_SCOPE.md): analytic proofs, explicit
resource and error contracts, current comparisons, operational consequences,
and reproducible checks. Final LaTeX writing follows that consolidation;
external technical feedback and submission follow the complete draft.
The [open endpoint](../docs/OPEN_PROBLEM.md) is investigated separately and
must retain its actual status. Update `CITATION.cff` when a manuscript
identifier exists.
