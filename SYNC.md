# Synchronization and provenance

This repository is not a mirror of `Hopf-QBP`. It is the authoritative home of
the new compiler-robustness paper while retaining explicit provenance for the
Hopf definitions it reuses.

## Source-of-truth rule

| Material | Authoritative repository |
|---|---|
| Published-chart conventions, established gradient protocols, direct-angle ledger, and Möttönen robustness | `GoGoKo699/Hopf-QBP` |
| Frame-safe compilation, ancilla--depth tradeoffs, output-sensitive decoding, and the new manuscript | `GoGoKo699/Compiler-Robust-Hopf-QBP` |

A correction to a shared mathematical foundation must be reviewed in both
repositories. New results are not copied back into `Hopf-QBP` unless they become
necessary to interpret or correct an established claim there.

## Recorded seed

The initial migration records two exact upstream states:

- `Hopf-QBP/main` at `9957815767ef3649275960fd5e860fb91725ff26`;
- research branch `ancilla-depth-robustness-2026` at
  `9cc564f493caff62b847fc362df522a68c6e83bf`.

The second commit was refactored rather than copied byte for byte. Package names,
document structure, and tests were changed so this repository is independently
executable. Exact lineage is stored in `provenance/upstream.json`.

## Synchronization procedure

1. Run the scheduled upstream audit or execute:

   ```bash
   python scripts/check_upstream_sync.py
   ```

2. If the tracked upstream commit changed, inspect the upstream diff. Do not
   update the recorded SHA merely to make the audit green.
3. Classify every upstream change as one of:
   - foundational correction relevant here;
   - paper-specific change with no effect here;
   - documentation or infrastructure only.
4. Port only relevant foundational corrections through an ordinary reviewed
   commit in this repository.
5. Update `provenance/upstream.json` and append a dated entry below.
6. When a correction also originates here and affects the established project,
   open a separate change in `Hopf-QBP` and record both commit SHAs.

The scheduled workflow detects upstream drift. It never modifies either
repository automatically.

## Synchronization log

### 2026-09-02

- Created this repository as the new research source of truth.
- Migrated the exact conditioned-prefix bridge, unary-frame construction,
  candidate ancilla--depth ledger, and record-wise decoder from the audited
  research seed.
- Retained `Hopf-QBP/main` as the authority for the established paper.
