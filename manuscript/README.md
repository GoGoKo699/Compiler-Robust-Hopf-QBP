# Manuscript guide

[Publication scope](PUBLICATION_SCOPE.md) · [Read the argument](../REVIEW.md) · [Verification](../docs/VERIFICATION.md)

Working title: **Exact and Fault-Tolerant Compilation of Hopf Differential Frames**.

The [publication scope](PUBLICATION_SCOPE.md) fixes the three principal
results and their corollaries. The exact theorem covers every $m\geq0$
clean-workspace budget; the two T-count constructions keep their distinct
clean/dirty reservations and return guarantees.

## Target journal

**First target: Quantum, as an original research article.** This decision
was checked against official journal guidance on 22 September 2026.

Quantum's [editorial criteria](https://quantum-journal.org/instructions/authors/)
value substantial advances within a particular subfield without requiring
broad interdisciplinary appeal. Its absence of format or length limits suits
the unified argument and full technical appendices. This is a fit assessment;
Quantum explicitly places merely incremental work below its acceptance threshold.

The closest venue precedents are Yuan–Zhang's
[exact state-preparation tradeoffs](https://quantum-journal.org/papers/q-2023-03-20-956/)
(Quantum 7, 956), Low–Kliuchnikov–Schaeffer's
[dirty-workspace tradeoffs](https://quantum-journal.org/papers/q-2024-06-17-1375/)
(Quantum 8, 1375), and Gosset–Kothari–Wu's
[optimal T-count](https://quantum-journal.org/papers/q-2026-07-22-2168/)
(Quantum 10, 2168). The manuscript must explain the new complete-operator
guarantees relative to these results, with the attribution in the source map.

| Journal | Role and reason |
|---|---|
| **Quantum** | First target: specialist readership, directly related compiler results, and room for a complete proof. |
| **Physical Review A** | Fallback: its [scope and criteria](https://journals.aps.org/pra/about) include quantum information and substantive, detailed research articles. |
| **PRX Quantum** | Conditional stretch: its [exceptionality criteria](https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.6.020001) need a stronger impact case than the current scope establishes. Its [flexible length policy](https://journals.aps.org/prxquantum/about) accommodates long papers. |

For this target, the opening pages should explain why the prescribed frame
requires more than state preparation, identify the new proof mechanisms,
and state Results A–C with their resource assumptions. QBP provides the
operational motivation and consequence. The exact and fault-tolerant models
remain parts of one operator-compilation story; the open endpoint remains
in the discussion.

At submission preparation, follow Quantum's current author guidance:
post the manuscript on arXiv with a quant-ph listing, include an author
contribution statement, and disclose the scope of AI assistance. The full
draft and external technical feedback come first.

## Paper order

1. Prescribed completion versus one-column state preparation, with the
   two-qubit readout example.
2. Shared Hopf-frame and complete-input compiler contract.
3. Exact all-workspace size/depth theorem and its proof mechanisms.
4. Sufficient-clean matching T theorem, followed by the two-clean construction
   and its bank, diagonal, and complex-magnitude corollaries.
5. Exact and approximate fixed-parameter QBP consequences.
6. The remaining endpoint gap and the limits of the circuit model.

Detailed schedules, source preparation, reversible lookup, error estimates,
and resource sums form the technical appendices. The exact toolkit credits
Yuan and Zhang; the [source map](../docs/SOURCE_MAP.md) gives the complete
attribution. Exploratory research is outside the selected manuscript.

The next publication task is the full LaTeX manuscript with consistent
notation, complete proofs, and bibliography. External technical feedback and
submission follow that draft. Solving the [open endpoint](../docs/OPEN_PROBLEM.md)
is not a prerequisite. Update `CITATION.cff` when a manuscript identifier exists.
