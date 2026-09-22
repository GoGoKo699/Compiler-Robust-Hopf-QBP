# Provenance and source records

[← Source map](../docs/SOURCE_MAP.md) · [Related work](../docs/RELATED_WORK.md) · [Repository landing page](../README.md)

This directory records exactly which external results and upstream files are
used.  It is a source-discipline layer, not an additional scientific premise.

## Files

| Record | Contents |
|---|---|
| [`literature.json`](literature.json) | active compiler framework, published and checked source versions, theorem/lemma roles, historical predecessor, and strict-zero claim policy |
| [`upstream.json`](upstream.json) | tracked Hopf repository commits, adapted file lineage, project-native paths, scientific reconciliation notes, and frozen fallback branch |
| [`prior_art_search.json`](prior_art_search.json) | bounded technical search for borrowed-workspace, UCG, and uncomputation antecedents, with explicit limits on negative-search evidence |

The human-readable synchronization policy and current upstream baselines are in
[`SYNC.md`](../SYNC.md).

## Active compiler source

The normative compiler citation is P. Yuan and S. Zhang, *Quantum* **7**, 956
(2023).  The published article corresponds to `arXiv:2202.11302v2`; the imported
statements were also checked in v3.

The exact roles are:

- Theorem 2: optimal state-preparation frontier;
- Lemma 5: ancilla-free multi-controlled X;
- Lemma 6: all-workspace UCG synthesis;
- Lemma 9: coherent copy–uncopy;
- Theorem 1: generic controlled-state-preparation comparison.

The preceding state-preparation paper is recorded as the historical predecessor
and original source of selected primitives.  It is not a second active compiler
path in the theorem.

## Hopf upstreams

The repository tracks the established Hopf chart and QBP conventions rather
than duplicating their full scientific scope.  The current baseline, adapted
file lineage, and reconciliation of the latest `Hopf-QBP` scientific boundaries
are recorded in `upstream.json` and summarized in `SYNC.md`.

The compiler construction, strict-zero echo, tree decoder, coherent router, and
all-workspace proof are project-native paths.

## Prior-art boundary

The search record covers controlled-unitary roots, Möttönen/Bergholm
multiplexors, borrowed and conditionally clean qubits, toggle detection,
ancilla-free multi-controlled gates, restricted UCGs, and uncomputation.

The record does not claim that failure to locate an exact match proves novelty
or priority.  The project-specific claim remains the Hopf addressed-layer
factorization and its optimal complete-frame resource consequence.

## Validation

```bash
python scripts/check_upstream_sync.py --offline
python -m unittest -v tests.test_provenance tests.test_literature_policy
```

## Fault-tolerant integration

The [source map](../docs/SOURCE_MAP.md) records the imported synthesis and lookup
results. The [finite-check provenance](../verification/fault_tolerant/README.md)
identifies the selected research files and their adaptations. The
[endpoint archive](../research/constant_clean/README.md) preserves a small
collection of supporting proofs for the next research question.
