# Documentation

[← Repository landing page](../README.md) · [Complete technical note](../REVIEW.md) · [Short reading guide](READING_GUIDE.md)

The documentation is organized by mathematical purpose rather than by
repository history. The main route begins with the synthesis problem, introduces
only the Hopf structure needed by the compiler, proves the all-workspace
frontier, and then derives the quantum-backpropagation consequence.

## Main route

| Order | Page | Purpose |
|---:|---|---|
| 1 | [Complete technical note](../REVIEW.md) | the full argument in one continuous reading |
| 2 | [Minimal Hopf interface](HOPF_INTERFACE.md) | the structured unitary target, marker columns, coordinate weights, and addressed layers |
| 3 | [Complete compiler theorem](COMPILER_THEOREM.md) | strict-zero, direct, and routed constructions with matching lower bounds |
| 4 | [Verification and evidence](VERIFICATION.md) | implementation levels, finite checks, resource ledgers, and audit boundaries |
| 5 | [Source and dependency map](SOURCE_MAP.md) | exact theorem, version, repository, implementation, and test dependencies |
| 6 | [Related work](RELATED_WORK.md) | state-preparation lineage, UCG structure, borrowed workspace, and contribution boundary |
| 7 | [QBP consequence](QBP_CONSEQUENCE.md) | frame-safe substitution, shared records, accuracy targets, and matched logical depth |

The [reading guide](READING_GUIDE.md) gives shorter routes for orientation and
focused checking.

## Focused mathematical pages

| Page | Question answered |
|---|---|
| [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) | What operator equality is sufficient for substituting a compiled frame and its inverse? |
| [Compiler boundaries](COMPILER_BOUNDARIES.md) | Why is one prepared state column insufficient, and what changes for checkpoint interfaces? |
| [Strict-zero borrowed-suffix echo](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) | How is one addressed Hopf depth compiled without any additional wire? |
| [Theorem overview](THEOREM_OVERVIEW.md) | What is the compact theorem and lemma hierarchy? |
| [Unified compiler architecture](UNIFIED_YUAN_ZHANG_COMPILER.md) | How do the three workspace schedules fit into one compiler? |
| [End-to-end QBP accounting](END_TO_END_QBP.md) | How are executions, per-execution depth, classical decoding, and access costs separated? |

## Evidence and independent reconstructions

| Page | Distinct role |
|---|---|
| [Claim support map](CLAIM_SUPPORT.md) | claim-by-claim proof, implementation, test, and scope boundary |
| [Research status](RESEARCH_STATUS.md) | concise current scientific state |
| [Consolidated proof audit](PROOF_AUDIT.md) | register accounting and all-workspace upper and lower bounds rechecked together |
| [Strict-zero echo audit](STRICT_ZERO_ECHO_AUDIT.md) | independent reconstruction of the four-sector circuit and zero-workspace resources |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem rederived from the operator target and imported primitives |

These records remain visible because they document which parts were rebuilt and
which failure modes were examined. They are supporting evidence, not substitutes
for the proof in [the compiler theorem](COMPILER_THEOREM.md).

## Literature and provenance

| Page or record | Role |
|---|---|
| [Related work](RELATED_WORK.md) | readable comparison organized by mathematical role |
| [Strict-zero prior-art boundary](STRICT_ZERO_PRIOR_ART.md) | focused comparison around the in-place echo |
| [Detailed search record](PRIOR_ART_SEARCH_2026_09.md) | bounded source-by-source search kept outside the proof route |
| [`provenance/literature.json`](../provenance/literature.json) | machine-readable source versions and roles |
| [`provenance/upstream.json`](../provenance/upstream.json) | exact Hopf-repository baselines and local lineage |
| [`SYNC.md`](../SYNC.md) | human-readable source-of-truth policy |

The two state-preparation papers are presented in the main narrative as one
coherent compiler line. Formal citations and the source map retain complete
authorship and exact theorem attribution.

## Executable route

A compact orientation follows the proof order:

```bash
python scripts/technical_walkthrough.py
```

The complete deterministic checks are:

```bash
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

The [verification page](VERIFICATION.md) states what is represented as a dense
operator, an explicit reversible schedule, an imported elementary compiler, or
an asymptotic ledger.

---

[← Repository landing page](../README.md) · [Complete technical note →](../REVIEW.md)
