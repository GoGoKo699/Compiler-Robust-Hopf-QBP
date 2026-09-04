# Reading guide

[← Repository landing page](../README.md) · [Complete technical note](../REVIEW.md)

The repository is arranged as a small technical website. Its main theorem is a
circuit-synthesis statement, and the quantum-backpropagation consequence comes
only after the compiler has been established.

A reader familiar with exact state preparation, controlled state preparation,
uniformly controlled gates, and clean-workspace tradeoffs can begin without
first reading either Hopf paper. The necessary Hopf structure is introduced as
a compact operator interface.

## Three reading routes

### Seven-minute orientation

Read the [landing page](../README.md). It gives:

- the position of Hopf-frame compilation between QSP and general unitary
  synthesis;
- the all-workspace theorem;
- the zero-workspace, direct, and routed schedules;
- the precise imported circuit results;
- the downstream QBP statement and its scope.

### Complete first reading

Read the [linear technical note](../REVIEW.md). It is organized in the order in
which the proof is most naturally checked from the state-preparation side:

1. define the structured unitary-completion problem;
2. isolate the minimum Hopf interface;
3. show why one correct state column is insufficient;
4. state the exact circuit model and imported primitives;
5. prove the three workspace schedules;
6. prove matching lower bounds;
7. add the complex phase layer;
8. derive the compiler consequence for Hopf QBP.

Every load-bearing operator identity and asymptotic step appears in that note.
Detailed register schedules, audit repetitions, and source records are linked
where they become useful.

### Full technical audit

Use the focused pages in this order:

| Order | Page | Main question |
|---:|---|---|
| 1 | [Minimal Hopf interface](HOPF_INTERFACE.md) | What complete unitary is being compiled? |
| 2 | [Compiler theorem](COMPILER_THEOREM.md) | How do the three schedules attain the all-workspace frontier? |
| 3 | [Verification map](VERIFICATION.md) | Which claims are analytic, explicit-circuit, or finite-test statements? |
| 4 | [Source map](SOURCE_MAP.md) | Which facts are inherited, imported, proved, and tested? |
| 5 | [Related work](RELATED_WORK.md) | How does the result sit within state preparation, UCG synthesis, and borrowed workspace? |
| 6 | [QBP consequence](QBP_CONSEQUENCE.md) | What exactly follows for the inverse-frame gradient protocol? |

The internal audits remain available from the verification page. They record
separate reconstructions of the proof and its likely failure points, but the
canonical mathematical route is the compiler theorem itself.

## Familiar and unfamiliar parts

The following ingredients may be treated in their standard circuit-synthesis
form:

- the optimal all-workspace QSP frontier;
- ancilla-free multi-controlled `X`;
- all-workspace UCG synthesis;
- balanced CNOT copy–uncopy;
- constant-width decompositions of Toffoli, Fredkin, controlled one-qubit, and
  controlled Givens gates.

The Hopf-specific ingredients introduced here are:

- the prescribed state-and-marker frame;
- the addressed all-zero-suffix layers;
- the zero-workspace borrowed-suffix echo;
- the conditioned-prefix and direct-sum tail identities;
- the register allocation that converts workspace into parallel subtree depth.

## Executable orientation

After installing the single NumPy dependency, run:

```bash
python scripts/technical_walkthrough.py
```

The walkthrough checks representative exact identities in the same order as the
technical note. The full deterministic suite and resource ledgers are:

```bash
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
```

These commands are finite falsification tools for signs, indices, phases,
workspace cleanup, and resource formulas. They do not replace the
size-independent proofs.

## The theorem in one line

For `N=2^n` and every clean-workspace budget `m>=0`, the real Hopf differential
frame and the phase-dressed complex magnitude frame have exact frame-safe
circuits with

```math
S=\Theta(N),
\qquad
D=\Theta\left(n+\frac{N}{n+m}\right).
```

The complete leaf-phase gradient uses a separate direct record. The compiler
result is exact and logical; hardware routing, approximate fault-tolerant
synthesis, noise, and application-specific controlled-observable cost remain
outside its scope.

---

[← Repository landing page](../README.md) · [Complete technical note →](../REVIEW.md)
