# Synchronization and provenance

This repository is not a mirror of `Hopf-QBP`. It is the authoritative home of
the compiler-robustness paper while retaining explicit provenance for shared
Hopf definitions.

## Source-of-truth rule

| Material | Authoritative repository |
|---|---|
| Established Hopf-chart conventions, gradient protocols, direct-angle ledger, and Möttönen-style robustness | `GoGoKo699/Hopf-QBP` |
| Frame-safe compilation, optimal positive-workspace tradeoffs, compiler boundaries, decoding, and the new manuscript | `GoGoKo699/Compiler-Robust-Hopf-QBP` |

A correction to a shared mathematical foundation must be reviewed in both
repositories. New results are not copied back into `Hopf-QBP` unless they are
needed to interpret or correct an established claim there.

## Recorded upstream states

- `GoGoKo699/Hopf-QBP`, branch `main`, commit
  `9957815767ef3649275960fd5e860fb91725ff26`.
- `GoGoKo699/Hopf-QBP`, historical research branch
  `ancilla-depth-robustness-2026`, commit
  `9cc564f493caff62b847fc362df522a68c6e83bf`.

The historical seed was refactored rather than copied byte for byte. The
self-contained tree decoder, routed compiler, unified resource theorem, and
compiler-boundary results are native to this repository.

## Frozen fallback

The cumulative near-optimal proof package remains preserved on branch

```text
near-optimal-audited-2026-09
```

at manifest commit

```text
24f339b863faa2ac92e1adb3917cbef7dc24d3b8
```

It is a provenance checkpoint, not an active compiler path.

## Synchronization procedure

1. Run:

   ```bash
   python scripts/check_upstream_sync.py
   ```

2. If a tracked upstream branch moved, inspect the diff. Do not update a
   recorded SHA merely to make the audit green.
3. Classify the change as a shared foundational correction, a paper-specific
   change with no effect here, or infrastructure/documentation only.
4. Port only relevant foundational corrections through an ordinary reviewed
   commit.
5. Update `provenance/upstream.json` and append a dated log entry below.
6. When a correction originates here and affects an established result, open a
   separate change in `Hopf-QBP` and record both commit SHAs.

The scheduled workflow reports drift and never overwrites either repository.

## Log

### 2026-09-03

- Consolidated the active compiler around the Yuan--Zhang framework.
- Retained Sun et al. as historical and original-source attribution.
- Removed superseded compiler paths from the active tree.
- Preserved the audited near-optimal fallback branch unchanged.

### 2026-09-02

- Created this repository as the new research source of truth.
- Recorded the established `Hopf-QBP` definitions and the initial research seed.
