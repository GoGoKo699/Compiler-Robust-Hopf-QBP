# Synchronization and provenance

[Repository landing page](README.md) · [Source map](docs/SOURCE_MAP.md) · [Verification](docs/VERIFICATION.md)

This repository is the authoritative home of the optimal Hopf differential-
frame compiler. It is not a mirror of `Hopf-QBP`. The chart and gradient-record
interfaces are inherited from the earlier Hopf work, while the complete-frame
compiler and its resource theorem are maintained here.

## 1. Source-of-truth rule

| Material | Authoritative location |
|---|---|
| balanced Hopf chart, canonical domains, inverse map, established global and checkpoint protocols, direct phase stream, statistical task boundaries | `GoGoKo699/Hopf-ansatz` and `GoGoKo699/Hopf-QBP` |
| frame-safe compiler contract, state-column obstruction, strict-zero echo, tree decoder, coherent router, all-workspace theorem, compiler-side QBP consequence | `GoGoKo699/Compiler-Robust-Hopf-QBP` |

A correction to a shared mathematical foundation must be reconciled in every
repository that consumes it. New compiler results are not copied back into
`Hopf-QBP` unless they become necessary to interpret or correct an established
claim there.

## 2. Current tracked upstreams

The machine-readable record tracks:

- `GoGoKo699/Hopf-QBP/main` at
  `faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582`;
- the historical research seed
  `GoGoKo699/Hopf-QBP/ancilla-depth-robustness-2026` at
  `9cc564f493caff62b847fc362df522a68c6e83bf`.

Exact file lineage is stored in [`provenance/upstream.json`](provenance/upstream.json).
Updating a tracked branch head records reconciliation with newer upstream work;
it does not imply that old local files were recopied from the newer commit.

## 3. Reconciliation completed on 2026-09-03

The ten commits between the former tracked `Hopf-QBP/main` baseline

```text
9957815767ef3649275960fd5e860fb91725ff26
```

and the current baseline

```text
faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582
```

were inspected individually. The relevant upstream changes sharpened the
following boundaries:

1. simultaneous absolute error of the raw Hopf-coordinate gradient is the
   primary finite-shot target;
2. complete-vector, relative, normalized-frame, and natural-gradient targets
   have different norm and conditioning requirements;
3. a zero metric weight makes the raw differential vanish, while inverse-metric
   outputs become ill-conditioned near small weights;
4. the complex phase metric uses the ambient round-sphere convention unless a
   projective quotient is introduced explicitly;
5. scalar-versus-gradient comparisons must separate executions, per-execution
   logical depth, output materialization, and controlled-observable access.

These clarifications are reflected in the current Hopf interface, QBP
consequence, source map, and executable checks. No upstream implementation was
copied wholesale during the reconciliation.

## 4. Synchronization procedure

When preparing a stable technical snapshot:

1. run the online drift check:

   ```bash
   python scripts/check_upstream_sync.py
   ```

2. if an upstream head moved, inspect the diff rather than replacing the SHA
   automatically;
3. classify each change as:
   - a shared foundational correction;
   - a paper-specific change with no effect here;
   - documentation or infrastructure only;
4. port only relevant foundational corrections through a reviewed commit;
5. update `provenance/upstream.json` and add a dated reconciliation note;
6. retain the ordinary deterministic check:

   ```bash
   python scripts/check_upstream_sync.py --offline
   ```

The audit reports drift. It never modifies either repository automatically.

## 5. Literature versions

The active external compiler framework is P. Yuan and S. Zhang, *Quantum* **7**,
956 (2023). The published article corresponds to `arXiv:2202.11302v2`. Theorem
2 and Lemmas 5, 6, and 9 were also checked in v3 and retain the statements and
model conventions used by this repository.

The earlier state-preparation paper is the historical predecessor and original-
source reference for selected primitives. Exact bibliographic roles and version
policy are stored in [`provenance/literature.json`](provenance/literature.json).

## 6. Historical seed and frozen fallback

The historical branch `ancilla-depth-robustness-2026` was a research seed rather
than a byte-for-byte source tree. Package structure, documentation, proofs, and
tests were replaced as the compiler theorem developed.

The frozen branch `near-optimal-audited-2026-09` preserves the earlier cumulative
proof package for provenance. It is not an active compiler path and is not part
of the reader-facing theorem route.

## 7. Reader-facing versus provenance material

The main technical route is:

```text
README.md
→ REVIEW.md
→ docs/HOPF_INTERFACE.md
→ docs/COMPILER_THEOREM.md
→ docs/VERIFICATION.md
```

Provenance files record exact origins and historical transitions. They should
not be read as additional scientific assumptions or as an alternative proof
route.
