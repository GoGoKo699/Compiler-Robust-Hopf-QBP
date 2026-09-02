# Manuscript workspace

No manuscript is frozen yet. This directory is reserved for the new paper after
the remaining scientific-scope decision.

## Working title

**Compiler-Robust Quantum Backpropagation in Hopf Coordinates**

The title may broaden only after a theorem is proved for a class of charts beyond
the Hopf construction.

## Intended contribution chain

1. Define coherent differential frames and frame-safe compilation.
2. Prove that frame-safe substitution preserves the global Hopf gradient record.
3. Prove by explicit counterexample that state-column equality is insufficient.
4. Distinguish full frame safety from checkpoint active-interface safety.
5. Prove the conditioned-prefix and unary-frame lemmas.
6. Establish the audited all-workspace real-frame theorem.
7. Establish the common-workspace separated complex theorem.
8. Compare both with the optimal QSP frontier of Yuan and Zhang.
9. Include output-sensitive magnitude, phase, and checkpoint decoding.
10. State all circuit-model, phase-convention, observable-access, and accuracy
    assumptions.

## Gates completed internally

- clean frame-safe substitution theorem;
- exact two-qubit global state-column counterexample;
- checkpoint active-interface substitution theorem;
- exact checkpoint state-column sign-flip counterexample;
- explicit proof that active-interface safety preserves means but not complete
  distributions;
- real conditioned-prefix and unary construction audit;
- all-workspace real-frame upper bound;
- clean arbitrary-diagonal all-budget lemma;
- common-workspace separated complex-frame theorem;
- common-phase gauge and singular-leaf checks;
- output-sensitive magnitude and direct-phase decoders.

## Remaining drafting gates

Do not freeze a full paper source until:

- the project decides whether to pursue the optimal all-ancilla theorem or
  publish the audited near-optimal bound with its explicit intermediate gap;
- the intended theorem statements receive an external proof review;
- the controlled-observable and accuracy conventions are frozen.

A provisional section skeleton may now be developed. The abstract and theorem
labels must remain provisional until the optimality-scope decision is made.
