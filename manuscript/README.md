# Manuscript workspace

The project now has enough internally audited mathematics to begin a controlled
paper draft. No theorem should be presented as externally verified until an
independent human proof review is complete.

## Working title

**Compiler-Robust Quantum Backpropagation in Hopf Coordinates**

The title should remain Hopf-specific unless a theorem is later proved for a
larger class of coordinate charts.

## Central paper claim

Let `N=2**n`. For every positive clean-workspace budget `m>=1`, the complete
real Hopf differential frame and the separated complex frame admit exact
frame-safe implementations with

```math
S=\Theta(N),
\qquad
D=\Theta\left(n+\frac{N}{n+m}\right),
```

using at most the requested `m` clean ancillary qubits. Thus complete coherent
access to the Hopf state and all normalized magnitude-coordinate directions can
match the optimal state-preparation space--time frontier.

The strict `m=0` endpoint remains separate: one clean qubit gives sharp size
and optimal depth, while the known strict-zero construction has larger size and
depth. The paper must state this boundary explicitly.

## Intended contribution chain

1. Define the Hopf coherent differential frame.
2. State and prove frame-safe substitution for the global gradient protocol.
3. Give the two-qubit state-column obstruction.
4. Prove the conditioned-prefix identity.
5. Prove the tree-cut tail direct sum.
6. Construct the coherent branch router and parallel subtree frames.
7. Prove the optimal positive-workspace size and depth theorem.
8. Prove the matching real-state lower bound.
9. Extend the theorem to the separated complex frame under one clean workspace
   pool.
10. Include output-sensitive magnitude and phase decoding.
11. State the checkpoint active-interface theorem and its counterexamples.
12. Isolate the strict-zero endpoint and broader-chart questions.

## Recommended theorem hierarchy

- **Theorem 1: frame-safe substitution.**
- **Proposition 2: state-column equality is insufficient.**
- **Lemma 3: conditioned-prefix frame identity.**
- **Lemma 4: tree-cut tail direct sum.**
- **Lemma 5: clean coherent branch routing.**
- **Lemma 6: controlled subtree-frame resources.**
- **Theorem 7: optimal positive-workspace real Hopf frame.**
- **Corollary 8: optimal positive-workspace separated complex frame.**
- **Theorem 9: checkpoint active-interface substitution.**
- **Corollary 10: compiler-robust global Hopf backpropagation.**

The numbering is provisional.

## Source discipline

The state-preparation frontier is Theorem 2 of Yuan and Zhang,
*Quantum* **7**, 956 (2023). Their Figure 1 concerns general unitary synthesis.
The older Figure 1 that motivated the original compiler question belongs to the
Sun--Tian--Yang--Yuan--Zhang paper.

The manuscript must distinguish:

- published compiler primitives;
- Hopf-specific identities proved here;
- internally audited deductions;
- finite validation;
- unresolved endpoint questions.

## Completed internal gates

- frame-safe global substitution;
- exact global state-column counterexample;
- checkpoint active-interface theorem and counterexamples;
- first audit of the conditioned-prefix/unary compiler;
- common-workspace separated complex theorem;
- exact tree-cut direct sum;
- routed parallel-subframe construction;
- second audit of the positive-workspace optimal theorem;
- matching real-state size and depth lower bounds;
- parameter-generation and decoder accounting;
- frozen near-optimal fallback branch.

## Remaining drafting and release gates

- external proof review of the router, workspace ledger, and lower bound;
- final decision on whether to pursue the strict `m=0` endpoint before first
  submission or leave it as an explicit open problem;
- freeze the controlled-observable model and statistical-accuracy notation;
- cross-check notation against both earlier Hopf papers;
- decide which construction diagrams and resource plots are necessary;
- compile and audit a complete manuscript package;
- update repository citation metadata only after a manuscript identifier exists.

A full draft may now be started, but the abstract and title page should continue
to describe the theorem as internally checked until the external review gate is
met.
