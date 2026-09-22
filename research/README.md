# Research continuation

**Resume after repository integration.** The active open problem is the constant-clean, large-dirty, high-precision endpoint for coherent Clifford+T compilation of the prescribed real Hopf frame. Integration preserves the research state; it does not start another construction attempt.

Read [the endpoint brief](CONSTANT_CLEAN_ENDPOINT.md) first. It defines the target and resource model, separates the solved neighboring regime from the open endpoint, records the useful obstructions, and states the next concrete proof obligation. The supported endpoint remains

```math
a=O(1),\quad b=\Theta(N),\quad L=N,
\qquad \Omega(N)\le \tau^*_{F,\mathbb R}\le O(N^{3/2}).
```

The [fault-tolerant compiler theorem](../docs/FAULT_TOLERANT_COMPILER.md) is the repository's main account of the established compiler frontier. These research notes preserve the unresolved continuation, rather than extending that theorem.

| Technical appendix | What it preserves |
|---|---|
| [Arbitrary returned-source attenuation](constant_clean/SOURCE_CHANNEL_PROOF.md) | Full Pauli-channel, integrality, determinant and singular-value proof; arbitrary precision-dependent sources; uniform family tradeoff |
| [Global XOR-program echo](constant_clean/GLOBAL_XOR_ECHO.md) | Complete-output inverse and commutator obstructions; precise two-query scope |
| [Modular table lookup](constant_clean/MODULAR_LOOKUP.md) | Valid modular-bank echo, carry/selector/bank ledger, and the missing loader hypothesis |
| [Joint dirty clock](constant_clean/DIRTY_CLOCK.md) | Linear whole-clock bound versus quadratic separately restored factor cost; remaining joint interface |
| [Exact catalytic phases](constant_clean/EXACT_PHASE_CATALYSIS.md) | Spectral multiplicity bound, accepted-block extension, and literal-phase caveats |
| [Finite-width precision sources](constant_clean/FINITE_WIDTH_SOURCES.md) | Nilpotent-shift bound, one-qubit counterexample, and radix/address accounting |
| [Appendix provenance](constant_clean/PROVENANCE.md) | Source identities and the limited editorial changes made during integration |

The mathematical proofs are the evidence for the asymptotic claims. Historical finite checks test particular algebraic interfaces; they do not establish the universal quantifiers, emit a constant-clean endpoint compiler, or certify novelty. The endpoint brief governs current scope where an older appendix records an earlier proposed route.
