# Research continuation

The [publication scope](../manuscript/PUBLICATION_SCOPE.md) includes the
positive two-clean compiler below. The other investigations remain available
as supporting research; their inclusion in this directory does not make them
required sections of the current paper.

The constant-clean research now has an improved arbitrary-angle compiler.
Start with the [checked-progress report](CONSTANT_CLEAN_PROGRESS.md), then
read the [operator-source proof](constant_clean/OPERATOR_SOURCE_COMPILER.md).
With two clean qubits and $`b\ge L+n+7`$ dirty qubits it gives
$`T=O(N+nL)`$ and $`G=O(NL)`$ for the complete real Hopf frame.

At $`L=N`$, the sufficient allocation is $`b=N+O(\log N)`$ and the frontier is

```math
\Omega(N)\le\tau^*_{F,\mathbb R}\le O(N\log N).
```

The earlier arbitrary-budget compiler remains available for smaller clean or
dirty allocations. The [endpoint brief](CONSTANT_CLEAN_ENDPOINT.md) states the
full contract, sufficient allocations, and remaining logarithmic gap. The
[sufficient-clean matching theorem](../docs/FAULT_TOLERANT_COMPILER.md) and
all general lower bounds are unchanged.

The same source proof adds a sharper dirty-bank tradeoff, matching lower
bounds in the stated lower-precision regimes, and a two-clean literal diagonal
compiler. It consequently covers the phase-dressed complex magnitude frame
with $`b\ge L+n+8`$.

The [technical reading map](constant_clean/README.md) also covers the new
[graph-source reuse restriction](constant_clean/OPERATOR_SOURCE_REUSE.md), the
zero-clean modular table adder, one-clean shared-generator phase batching,
dirty-rank compression, and the scoped program/clock obstructions. The
operator-source compiler does not depend on the unresolved arbitrary phase
batch or joint clock.

| Earlier appendix | What it preserves |
|---|---|
| [Arbitrary returned-source attenuation](constant_clean/SOURCE_CHANNEL_PROOF.md) | Full Pauli-channel and algebraic proof for a supplied source; uniform family tradeoff |
| [Global XOR-program echo](constant_clean/GLOBAL_XOR_ECHO.md) | Complete-output inverse and commutator obstructions; precise two-query scope |
| [Modular table lookup](constant_clean/MODULAR_LOOKUP.md) | Historical modular-bank proposal and its then-missing loader; the follow-up now supplies a different charged adder |
| [Joint dirty clock](constant_clean/DIRTY_CLOCK.md) | Linear whole-clock bound versus quadratic separately restored factor cost |
| [Exact catalytic phases](constant_clean/EXACT_PHASE_CATALYSIS.md) | Spectral multiplicity bound, accepted-block extension, and literal-phase caveats |
| [Finite-width precision sources](constant_clean/FINITE_WIDTH_SOURCES.md) | Nilpotent-shift bound, one-qubit alternative, and radix/address accounting |
| [Appendix provenance](constant_clean/PROVENANCE.md) | Source identities, integration history, and subsequent mathematical changes |

The proofs establish the general claims. Finite executable checks test fragile
identities and conventions, not universal quantifiers or publication novelty.
The endpoint brief governs current scope where an older appendix records an
earlier stage of the investigation.
