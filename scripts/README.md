# Executable entry points

[← Repository landing page](../README.md) · [Verification map](../docs/VERIFICATION.md)

The scripts provide one readable orientation, two resource ledgers, and one
source-synchronization check.  They do not replace the analytic proof.

## Technical walkthrough

```bash
python scripts/reviewer_walkthrough.py
```

This runs ten representative checks in the same order as the narrative:

1. recursive and addressed two-qubit frames agree;
2. canonical domains and singular coordinates are interpreted consistently;
3. one prepared column is insufficient;
4. the strict-zero four-sector identity holds;
5. the borrowed suffix bit is restored;
6. the explicit coherent router matches the tail direct sum;
7. the phase diagonal is one UCG;
8. the correct workspace schedule is selected;
9. the simultaneous workspace peak respects the supplied budget;
10. the low-workspace and maximal-cut inequalities hold.

## All-workspace ledger

```bash
python scripts/unified_resource_ledger.py --n 12
```

This displays the selected schedule and transparent integer resource terms over
representative clean-workspace budgets.  Use `--format json` for a
machine-readable record.

## Strict-zero ledger

```bash
python scripts/strict_zero_echo_ledger.py --n 12
```

This displays the per-depth borrowed-suffix UCG widths, predicate terms, and the
complete strict-zero size/depth proxies.

## Upstream synchronization

```bash
python scripts/check_upstream_sync.py --offline
```

The offline mode validates the recorded source schema and local lineage without
network access.  The tracked upstream commits and scientific reconciliation are
listed in [`SYNC.md`](../SYNC.md) and
[`provenance/upstream.json`](../provenance/upstream.json).

## Complete deterministic suite

```bash
python validate.py
```

The complete test map is in [`tests/README.md`](../tests/README.md).

## Fault-tolerant checks

Run `python scripts/verify_fault_tolerant.py` to reproduce four focused exact
source/kernel and rational-resource suites. See the
[scope and receipt guide](../verification/fault_tolerant/README.md). Temporary
outputs are used by default, leaving the expected evidence files unchanged.
