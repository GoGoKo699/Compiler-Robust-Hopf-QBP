# Provenance and source records

[Source map](../docs/SOURCE_MAP.md) · [Related work](../docs/RELATED_WORK.md)

| Record | Purpose |
|---|---|
| [`literature.json`](literature.json) | Imported compiler versions, theorem roles, historical predecessor, and attribution policy |
| [`upstream.json`](upstream.json) | Tracked Hopf commits, adapted-file lineage, active native paths, and reconciliation history |
| [`SYNC.md`](../SYNC.md) | Recorded upstream baselines and synchronization policy |
| [Fault-tolerant provenance](../verification/fault_tolerant/README.md) | Original finite-check files, their adaptations, and exact receipt verification |

The normative exact compiler source is P. Yuan and S. Zhang, *Quantum* **7**,
956 (2023): Theorem 2 supplies the state-preparation benchmark; Lemmas 5, 6,
and 9 supply multi-controlled X, UCG synthesis, and coherent copy–uncopy.
The published article corresponds to arXiv:2202.11302v2; the imported
statements were also checked in v3. The preceding state-preparation paper is
the historical predecessor, not a second active compiler path.

The [source map](../docs/SOURCE_MAP.md) separately identifies the Hopf/QBP
premises and the fault-tolerant ingredients. The local contribution is the
prescribed-frame construction and its resource guarantees. Source searches
and internal checks do not certify priority or substitute for external review.

## Earlier research snapshot

The complete pre-pruning research and internal audit material remains in
[commit da91e34](https://github.com/GoGoKo699/Compiler-Robust-Hopf-QBP/tree/da91e34edd97d6d0f90af58ab556412c04929cb4).
It includes the exploratory constant-clean routes and their tests. Those
materials are outside the active publication tree; the retained proof chapters
contain all dependencies of the selected results.

## Check recorded provenance

```bash
python scripts/check_upstream_sync.py --offline
python -m unittest tests.test_provenance tests.test_literature_policy
```

The offline check validates recorded baselines, not current remote freshness.
