# Documentation guide

[← Repository landing page](../README.md) · [Start the complete narrative](../REVIEW.md)

The repository is intended to be read in a linear order. The files below are
grouped by purpose so that the mathematical proof, executable evidence, and
internal audit records do not compete for attention.

## Main reading route

| Order | Page | Purpose |
|---:|---|---|
| 1 | [Complete narrative](../REVIEW.md) | the entire argument from the synthesis problem to the QBP consequence |
| 2 | [Minimal Hopf interface](HOPF_INTERFACE.md) | only the chart, tangent, marker, and addressed-layer facts needed here |
| 3 | [Complete compiler theorem](COMPILER_THEOREM.md) | full all-workspace construction and optimality proof |
| 4 | [QBP consequence](QBP_CONSEQUENCE.md) | frame-safe substitution and the final gradient-scaling statement |
| 5 | [Verification and evidence](VERIFICATION.md) | exact finite checks, resource ledgers, and evidence boundaries |
| 6 | [Source map](SOURCE_MAP.md) | fact-level dependencies on the two Hopf papers and Yuan–Zhang |
| 7 | [Related work](RELATED_WORK.md) | compiler lineage and the narrow contribution boundary |

The [technical reading guide](INDEPENDENT_REVIEW_GUIDE.md) gives a shorter
orientation for a first visit.

## Focused construction pages

| Page | Focus |
|---|---|
| [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) | the complete clean-input operator contract and its adjoint consequence |
| [Compiler boundaries](COMPILER_BOUNDARIES.md) | exact global and checkpoint counterexamples and the active-interface theorem |
| [Strict-zero borrowed-suffix echo](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) | the complete `m=0` circuit and four-sector proof |
| [Theorem overview](THEOREM_OVERVIEW.md) | compact theorem chain for reference |
| [Detailed Yuan–Zhang compiler appendix](UNIFIED_YUAN_ZHANG_COMPILER.md) | expanded register and resource derivation retained as a technical appendix |
| [End-to-end QBP appendix](END_TO_END_QBP.md) | expanded execution, decoder, workspace, and access-model accounting |

## Evidence and internal review

| Page | Role |
|---|---|
| [Claim support map](CLAIM_SUPPORT.md) | claim-by-claim proof, code, test, and scope boundary |
| [Research status](RESEARCH_STATUS.md) | concise scientific status without development-history details |
| [Consolidated proof audit](PROOF_AUDIT.md) | internal reconstruction of the complete compiler proof |
| [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | focused internal audit of the borrowed-suffix circuit |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | proof rederived from the operator target and imported primitives |

Internal audits remain visible because they record corrections and likely
failure points. They are evidence about the care of the analysis, not a
substitute for independent technical judgment.

## Literature support

| Page | Role |
|---|---|
| [Related work](RELATED_WORK.md) | readable comparison organized by mathematical role |
| [Strict-zero prior-art boundary](STRICT_ZERO_PRIOR_ART.md) | focused technical comparison around the borrowed-suffix echo |
| [Detailed search record](PRIOR_ART_SEARCH_2026_09.md) | search scope and source-by-source notes kept outside the main proof |

Machine-readable literature and search provenance are stored in
[`../provenance/`](../provenance/).

## Executable route

A compact orientation run is:

```bash
python scripts/reviewer_walkthrough.py
```

The complete reproduction commands are collected in
[Verification and evidence](VERIFICATION.md).

---

[← Repository landing page](../README.md) · [Start the complete narrative →](../REVIEW.md)
