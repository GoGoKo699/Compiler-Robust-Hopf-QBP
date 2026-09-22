# Constant-clean technical appendices

Start with the short [checked-progress report](../CONSTANT_CLEAN_PROGRESS.md), then the [endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md). The full-frame endpoint is now between $`\Omega(N)`$ and $`O(N\log N)`$ with three clean qubits, $`b\ge N+n+6`$ dirty qubits, and $`L=N`$. Smaller allocations retain the earlier bounds.

## Current research

| Note | Result and boundary |
|---|---|
| [Operator-source compiler](OPERATOR_SOURCE_COMPILER.md) | Arbitrary real frames with three clean bits and $`b\ge L+n+6`$: $`T=O(N+nL)`$, $`G=O(NL)`$; leaves a logarithmic endpoint gap. |
| [Phase batching with a dirty accumulator](IDENTICAL_PHASE_BATCHING.md) | One clean qubit handles identical phases and distinct phases built from shared base angles with bounded signed integer coefficients; the fast arbitrary tensor-batch problem remains open. |
| [Dirty symplectic rank](DIRTY_RETURN_LOWER_BOUND_FOLLOWUP.md) | Same-clean/T/error compression; the retained order is optimal for rank $`O(\sqrt N)`$, while linear T count requires linear rank on hard instances. |
| [Global program blocks and phase batching](GLOBAL_BLOCK_FOLLOWUP.md) | Two-call addressed reduction with no extra clean qubit; uniform selected commutators and full batching are equivalent up to a precision margin. The fast batch hypothesis remains unproved. |
| [Joint clock follow-up](JOINT_CLOCK_FOLLOWUP.md) | A single-addition wrapper needs one initialized work qubit per clock bit, even with approximate complete return and arbitrary encoding. |
| [Modular lookup follow-up](MODULAR_LOOKUP_FOLLOWUP.md) | Exact zero-clean modular table addition in $`O((N+m)\log(m+1))`$ T gates using $`O(m+n)`$ dirty work; a cheap joint clock remains missing. |
| [Primary-source follow-up](ENDPOINT_LITERATURE_FOLLOWUP.md) | Precise clean-work, accuracy, and gate-cost hypotheses of the inspected synthesis, lookup, and catalyst results. |

These include the improved arbitrary-angle compiler, exact dirty arithmetic,
restricted batching, structural results, and conditional reductions. Their
small checks run through `python validate.py`; the general proofs and remaining
implementation obligations are stated in the notes.

## Established construction and earlier interface results

| Note | Proven result and scope |
|---|---|
| [Borrowed-workspace compiler](BORROWED_WORKSPACE_COMPILER.md) | The earlier arbitrary-budget real-frame upper bound, with exact dirty return, and the all-clean-budget corollary under its additional precision/dirty-width condition. |
| [Source-channel proof](SOURCE_CHANNEL_PROOF.md) | Arbitrary returned-source attenuation has a processing/width tradeoff, even for precision-dependent sources. Costs are not additive across arbitrary frame stages. |
| [Global XOR echo](GLOBAL_XOR_ECHO.md) | A two-query interpreter with uniform dirty return only supplies near-involutions; targets sharing that interpreter must nearly commute. |
| [Modular lookup](MODULAR_LOOKUP.md) | Historical modular-bank echo and missing-loader target; the follow-up now gives a different charged carry-query construction. |
| [Dirty clock](DIRTY_CLOCK.md) | Separately restored phase factors have quadratic cost; joint clock synthesis remains open. |
| [Exact phase catalysis](EXACT_PHASE_CATALYSIS.md) | Exact literal dyadic phases require growing independent source width. Approximate and projective targets need separate arguments. |
| [Finite-width sources](FINITE_WIDTH_SOURCES.md) | The nilpotent shift has a width obstruction, while another kernel admits a one-qubit source. Variable attenuation and addressing remain charged. |

The first appendix preserves an earlier compiler and its splice with the [main theorem](../../docs/FAULT_TOLERANT_COMPILER.md). The remaining earlier appendices are analytical interface results. Their scoped obstructions remain valid; the new operator-source construction above improves the upper bound without strengthening the unrestricted lower bound. [Provenance](PROVENANCE.md) records the selected source notes and editorial changes.
