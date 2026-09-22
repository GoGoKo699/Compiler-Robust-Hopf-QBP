# Technical appendix provenance

These seven notes preserve the mathematical dependencies needed to resume the constant-clean endpoint. The integration source was the frozen research package through checkpoint 31; the current [resume brief](../CONSTANT_CLEAN_ENDPOINT.md) consolidates its conclusions and the later scope audit without extending the frontier.

The source identities below refer to the original package, not additional repository dependencies. Each appendix received a navigation/scope notice and GitHub-compatible mathematical typography. Where marked, only the final historical verification section was omitted, avoiding reproduction commands that depend on the earlier scratch layout. The source-channel proof is retained in full. The borrowed-workspace appendix condenses and independently checks the earlier proof rather than importing its full historical narrative. No mathematical claim was strengthened during import or formatting.

| Repository appendix | Original package path | Additional editorial change beyond navigation and math typography |
|---|---|---|
| [BORROWED_WORKSPACE_COMPILER.md](BORROWED_WORKSPACE_COMPILER.md) | `Hopf_Fault_Tolerant_Research.md`, Sections 4.5–4.6, 4.8 and 5.19; `Hopf_Small_Clean_Workspace.md` | Condensed self-contained proof of the real-frame borrowed upper bound and all-clean-budget splice; omitted complex variants and historical verification narrative; independently checked exact echoes and resource sums |
| [SOURCE_CHANNEL_PROOF.md](SOURCE_CHANNEL_PROOF.md) | `analysis/source_channel_review.md` | None |
| [GLOBAL_XOR_ECHO.md](GLOBAL_XOR_ECHO.md) | `analysis/global_construction.md` | Omitted final historical finite-check section |
| [MODULAR_LOOKUP.md](MODULAR_LOOKUP.md) | `analysis/modular_lookup.md` | Omitted final historical finite-check section |
| [DIRTY_CLOCK.md](DIRTY_CLOCK.md) | `analysis/clock_construction.md` | None |
| [EXACT_PHASE_CATALYSIS.md](EXACT_PHASE_CATALYSIS.md) | `analysis/exact_phase_catalysis.md` | Omitted final historical finite-check section |
| [FINITE_WIDTH_SOURCES.md](FINITE_WIDTH_SOURCES.md) | `analysis/finite_width_precision.md` | None |

## Original source SHA-256

- `Hopf_Fault_Tolerant_Research.md`: `3c8c421f8a55067c56d48efcb6acb1e03eba71538d6f11d96cba9b61842f24ba`
- `Hopf_Small_Clean_Workspace.md`: `e3ae27f40e7e65249aa7cd1227d7a91d1330e021cb80bbcef65375260ae8a618`
- `analysis/source_channel_review.md`: `c39a2748ecaf73f4160804d30d672f9a2001d179a7abe5c75218592215c94f0e`
- `analysis/global_construction.md`: `7011ec8d83d67b379bea199016e22da8665f7f01a8d80ea7bd009baa53c720c2`
- `analysis/modular_lookup.md`: `15d9eccc506c3dfbfb608c401e0712449c23ab88d1d0c4c96ddabdf402e00879`
- `analysis/clock_construction.md`: `d2c8e13d1ddd995b3a664465b5ed3fe1f074c1b9fdbfefcdf38a1f9b26dcb6cb`
- `analysis/exact_phase_catalysis.md`: `6a0e8765264d165cc7b981713cb3ec3ccdf9ed7910e7f5d99da235c12bafe87b`
- `analysis/finite_width_precision.md`: `ffcf613361bb6e303528d44dcb97bc8bca80172ba3313c4c710a184f7f7b7938`

The main theorem narrative lives in [the fault-tolerant compiler documentation](../../docs/FAULT_TOLERANT_COMPILER.md). These selected research appendices are not an archive of all earlier checkpoints or a substitute for the repository verification entrypoint.

## Research resumed after integration

The [checked-progress report](../CONSTANT_CLEAN_PROGRESS.md) and the five
`FOLLOWUP.md` notes were developed after integration revision `b935b34`.
They are new derivations and primary-source comparisons, not verbatim imports
from the frozen package above. The original source hashes remain unchanged.

Their proofs distinguish universal compression, restrictions on specified
interfaces, and reductions whose synthesis hypotheses remain unproved.
Primary papers are linked at the claims they support. Internal proof review
and small checks do not certify publication novelty or external peer review.
The executable regression record is
[test_constant_clean_structure.py](../../tests/test_constant_clean_structure.py).
The unrestricted endpoint bounds are unchanged.

The subsequent constructive continuation adds
[identical-phase batching](IDENTICAL_PHASE_BATCHING.md) and the weaker
selected-commutator contract in the global-block note. The batching proof
combines a masked accumulator with existing phase-commutator and coherent
dirty-increment techniques; the note cites their primary sources and makes
no priority claim. Its full-input identity, phase cancellation and resource
ledger received a separate internal proof check. Small regression checks are
in [test_identical_phase_batching.py](../../tests/test_identical_phase_batching.py).
The result concerns identical phases, so the unrestricted endpoint remains open.

The next continuation extends that same note to signed integer combinations
of shared base angles. Independent checks confirm the centering identity,
coherent constant-offset costs, and reuse of the initialized bit under the
complete-output error contract. A separate covering argument limits this
angle-table representation; it is not a frame T-count lower bound. Four
additional finite tests check signed sums, a missing-centering failure,
nondiagonal approximation, and sequential reuse with intermediate leakage.
The offset costs are cited arithmetic primitives, not inferred from the
permutation macros in those four tests. The unrestricted endpoint bounds
are unchanged.
