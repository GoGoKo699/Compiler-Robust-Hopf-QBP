# Constant-clean technical appendices

Start with the short [checked-progress report](../CONSTANT_CLEAN_PROGRESS.md), then the [endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md). The full-frame endpoint remains between $`\Omega(N)`$ and $`O(N^{3/2})`$ at constant clean width, $`\Theta(N)`$ dirty width, and $`L=N`$.

## Current research

| Note | Result and boundary |
|---|---|
| [Phase batching with a dirty accumulator](IDENTICAL_PHASE_BATCHING.md) | One clean qubit handles identical phases and distinct phases built from shared base angles with bounded signed integer coefficients; the general angle-table problem remains open. |
| [Dirty symplectic rank](DIRTY_RETURN_LOWER_BOUND_FOLLOWUP.md) | Same-clean/T/error compression; the retained order is optimal for rank $`O(\sqrt N)`$, while linear T count requires linear rank on hard instances. |
| [Global program blocks and phase batching](GLOBAL_BLOCK_FOLLOWUP.md) | Two-call addressed reduction with no extra clean qubit; uniform selected commutators and full batching are equivalent up to a precision margin. The fast batch hypothesis remains unproved. |
| [Joint clock follow-up](JOINT_CLOCK_FOLLOWUP.md) | A single-addition wrapper needs one initialized work qubit per clock bit, even with approximate complete return and arbitrary encoding. |
| [Modular lookup follow-up](MODULAR_LOOKUP_FOLLOWUP.md) | Exact carry-query decomposition and sign-corrected dirty-bank echo; the jointly compiled arithmetic remains missing. |
| [Primary-source follow-up](ENDPOINT_LITERATURE_FOLLOWUP.md) | Precise clean-work, accuracy, and gate-cost hypotheses of the inspected synthesis, lookup, and catalyst results. |

These include a restricted constructive theorem, structural results, and
conditional reductions. Their small checks run through
`python -m unittest tests.test_constant_clean_structure tests.test_identical_phase_batching`;
the general proofs and unresolved implementation costs are stated in the notes.

## Established construction and earlier interface results

| Note | Proven result and scope |
|---|---|
| [Borrowed-workspace compiler](BORROWED_WORKSPACE_COMPILER.md) | The earlier arbitrary-budget real-frame upper bound, with exact dirty return, and the all-clean-budget corollary under its additional precision/dirty-width condition. |
| [Source-channel proof](SOURCE_CHANNEL_PROOF.md) | Arbitrary returned-source attenuation has a processing/width tradeoff, even for precision-dependent sources. Costs are not additive across arbitrary frame stages. |
| [Global XOR echo](GLOBAL_XOR_ECHO.md) | A two-query interpreter with uniform dirty return only supplies near-involutions; targets sharing that interpreter must nearly commute. |
| [Modular lookup](MODULAR_LOOKUP.md) | A modular-bank echo is valid, but its carry-aware loader is still a missing charged construction. |
| [Dirty clock](DIRTY_CLOCK.md) | Separately restored phase factors have quadratic cost; joint clock synthesis remains open. |
| [Exact phase catalysis](EXACT_PHASE_CATALYSIS.md) | Exact literal dyadic phases require growing independent source width. Approximate and projective targets need separate arguments. |
| [Finite-width sources](FINITE_WIDTH_SOURCES.md) | The nilpotent shift has a width obstruction, while another kernel admits a one-qubit source. Variable attenuation and addressing remain charged. |

The first appendix preserves an earlier compiler and its splice with the [main theorem](../../docs/FAULT_TOLERANT_COMPILER.md). The remaining appendices are analytical interface results. None improves the selected constant-clean endpoint or strengthens its unrestricted frame lower bound. [Provenance](PROVENANCE.md) records the selected source notes and editorial changes.
