# Documentation map

[← Repository landing page](../README.md) · [Complete technical narrative](../REVIEW.md)

The documentation is arranged in three passes.  The first pass states the
problem and two resource models. The second contains the proofs.  The third exposes the
implementation, evidence, and provenance.

## Pass I: orient the synthesis question

| Page | Purpose |
|---|---|
| [Landing page](../README.md) | one prepared column versus a prescribed unitary completion; theorem and schedule map |
| [Technical reading map](INDEPENDENT_REVIEW_GUIDE.md) | a compact route through the proof and executable checks |
| [Complete narrative](../REVIEW.md) | the full argument in one continuous reading |

## Pass II: inspect the proof by component

| Page | Purpose |
|---|---|
| [Hopf interface](HOPF_INTERFACE.md) | the four geometric facts consumed by synthesis, plus the addressed-layer operator |
| [Exact compiler theorem](COMPILER_THEOREM.md) | strict-zero, direct, and routed schedules with matching size/depth bounds |
| [Fault-tolerant compiler theorem](FAULT_TOLERANT_COMPILER.md) | precision, shared source, clean/dirty workspace, and matching T-count regime |
| [Approximate QBP](QBP_APPROXIMATION.md) | complete-input circuit error, actual adjoints, and bounded raw-gradient bias |
| [QBP consequence](QBP_CONSEQUENCE.md) | exact frame-safe substitution, shared records, and the matched-program cost statement |
| [Frame-safe compilation](FRAME_SAFE_COMPILATION.md) | clean-subspace operator contract and adjoint consequence |
| [Compiler boundaries](COMPILER_BOUNDARIES.md) | state-column and checkpoint-interface counterexamples |
| [Strict-zero echo](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) | focused four-sector construction and zero-workspace resource proof |

The [theorem overview](THEOREM_OVERVIEW.md),
[compiler architecture summary](UNIFIED_YUAN_ZHANG_COMPILER.md), and
[end-to-end accounting](END_TO_END_QBP.md) provide shorter reference views of
the same result.

## Pass III: inspect evidence and provenance

| Page | Purpose |
|---|---|
| [Fault-tolerant reproduction](../verification/fault_tolerant/README.md) | exact source/kernel fixtures, rational budgets, and their limits |
| [Proof and executable correspondence](VERIFICATION.md) | what is represented locally, what is imported, and what every test checks |
| [Source and dependency map](SOURCE_MAP.md) | exact state-preparation, Hopf, and QBP premises with local consumers |
| [Related work](RELATED_WORK.md) | mathematical lineage and the narrow contribution boundary |
| [Claim support map](CLAIM_SUPPORT.md) | claim-by-claim proof, implementation, test, and scope ledger |

The internal reconstructions remain visible:

| Record | Distinct role |
|---|---|
| [Consolidated proof audit](PROOF_AUDIT.md) | complete operator and resource reconstruction |
| [Strict-zero audit](STRICT_ZERO_ECHO_AUDIT.md) | order, phase, borrowed-bit restoration, endpoints, and sums |
| [Clean-room reconstruction](CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md) | theorem re-derived from the target operator and imported compiler results |

Detailed search and provenance records are kept separately from the proof:

- [strict-zero prior-art boundary](STRICT_ZERO_PRIOR_ART.md);
- [technical search record](PRIOR_ART_SEARCH_2026_09.md);
- [provenance directory map](../provenance/README.md);
- [`SYNC.md`](../SYNC.md) upstream synchronization policy.

## Browse the repository by purpose

Every principal directory contains its own short map.

| Directory | Contents |
|---|---|
| [implementation](../compiler_robust_hopf/README.md) | modules arranged in proof order, public entry points, and interpretation of resource rows |
| [tests](../tests/README.md) | validation groups organized by operator and theorem interface |
| [scripts](../scripts/README.md) | walkthrough, ledgers, and synchronization commands |
| [diagrams](../assets/README.md) | the five reviewer-facing SVGs and the exact statements they illustrate |
| [provenance](../provenance/README.md) | compiler versions, Hopf upstreams, and prior-art claim boundaries |
| [Research continuation](../research/README.md) | constant-clean endpoint, retained bounds, and the next proof obligation |
| [manuscript workspace](../manuscript/README.md) | paper question chain, theorem hierarchy, and scope discipline |

## Executable route

```bash
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/verify_fault_tolerant.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

The short walkthrough is an orientation.  The complete suite additionally
tests the explicit coherent router on arbitrary complex prefix–suffix-entangled
inputs and verifies exact workspace cleanup.

---

[← Repository landing page](../README.md) · [Complete technical narrative →](../REVIEW.md)
