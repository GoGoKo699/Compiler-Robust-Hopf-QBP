# Synchronization and provenance

This repository is not a mirror of `Hopf-QBP`. It is the authoritative home of
the optimal Hopf differential-frame compiler while retaining explicit
provenance for the chart and QBP interfaces it reuses.

## Source-of-truth rule

| Material | Authoritative repository |
|---|---|
| Published-chart conventions, established gradient protocols, direct-angle ledger, Möttönen robustness, and statistical task boundaries | `GoGoKo699/Hopf-QBP` |
| Frame-safe compilation, strict-zero echo, routed all-workspace compiler, output-sensitive decoding, and the new compiler theorem | `GoGoKo699/Compiler-Robust-Hopf-QBP` |

A correction to a shared mathematical foundation must be reviewed in both
repositories. New compiler results are not copied back into `Hopf-QBP` unless
they become necessary to interpret or correct an established claim there.

## Current tracked upstreams

The provenance record tracks:

- `GoGoKo699/Hopf-QBP/main` at
  `a9885317cf998a7df87ca07ba86e3bd4f0f419ef`;
- the historical research seed
  `GoGoKo699/Hopf-QBP/ancilla-depth-robustness-2026` at
  `9cc564f493caff62b847fc362df522a68c6e83bf`.

The compiler repository was originally seeded from earlier commits. Exact file
lineage is preserved in `provenance/upstream.json`; updating the tracked branch
head does not pretend that old files were recopied from the newer commit.

## Reconciliation completed on 2026-09-03

The ten commits between the former tracked `Hopf-QBP/main` baseline

```text
9957815767ef3649275960fd5e860fb91725ff26
```

and the baseline adopted at that time

```text
faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582
```

were inspected rather than accepted by SHA replacement alone. The relevant
upstream changes sharpened the following boundaries:

1. simultaneous absolute error of the raw Hopf-coordinate gradient is the
   primary finite-shot target;
2. complete-vector, relative, normalized-frame, and natural-gradient targets
   have different conditioning and sample requirements;
3. a zero magnitude metric weight makes the raw magnitude differential and
   estimator vanish, while inverse-metric outputs become ill-conditioned near
   small weights;
4. the complex phase metric uses the ambient round-sphere convention unless a
   projective quotient is explicitly introduced;
5. scalar-versus-gradient comparisons must separate independent executions,
   per-execution logical depth, output materialization, and controlled-observable
   access.

These clarifications are now reflected in the compiler repository's Hopf
interface, QBP consequence, source map, and peer-review tests. No upstream
implementation was copied wholesale during this reconciliation.

## Reconciliation completed on 2026-09-07

The five commits from the September 3 baseline

```text
faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582
```

to the newly tracked baseline

```text
a9885317cf998a7df87ca07ba86e3bd4f0f419ef
```

were reviewed in full. The changes synchronize manuscript terminology for
raw-coordinate and geometric outputs, the ambient-sphere phase metric, and
reflection-sum sampling with matched controlled-observable costs. They also
repair the upstream claim map and add documentation-integrity tests. No circuit
builder, decoder, or headline sampling theorem changes in this interval.

One clarification is relevant locally: zero-weight magnitude records vanish,
whereas zero-amplitude phase derivatives have zero mean records but need not
have zero individual signed one-hot records. The zero-record statement in the
QBP consequence and the zero-weight statement above now explicitly concern
magnitude coordinates. The existing frame, sampling, and cost arguments are
unchanged.

The current-baseline references and provenance tests are updated together. The
September 3 reconciliation is retained in
`upstream_reconciliation_history`, and original file lineage, the historical
seed, and the frozen fallback remain unchanged. No upstream implementation was
copied and no approved layout was altered.

## Synchronization procedure

1. Run the online drift check when preparing a review snapshot:

   ```bash
   python scripts/check_upstream_sync.py
   ```

2. If an upstream head moved, inspect the diff. Do not update a recorded SHA
   merely to make the audit green.
3. Classify each change as:
   - a foundational correction relevant here;
   - a paper-specific change with no effect here;
   - documentation or infrastructure only.
4. Port only relevant foundational corrections through a reviewed commit.
5. Update `provenance/upstream.json` and append a dated reconciliation note.
6. Keep the ordinary continuous-integration check offline and deterministic:

   ```bash
   python scripts/check_upstream_sync.py --offline
   ```

The online audit also runs when the provenance record or audit machinery
changes, before and after merge, as well as on its existing schedule and manual
trigger. Ordinary numerical validation remains offline. The audit never
modifies either repository automatically.

## Historical seed

The branch `ancilla-depth-robustness-2026` was refactored rather than copied
byte for byte. Package names, documentation, proofs, and tests were replaced as
the compiler theorem developed. The frozen branch
`near-optimal-audited-2026-09` preserves the earlier cumulative proof package
for provenance but is not an active compiler path.
