# Research status and release gates

Last updated: 2026-09-02.

## Current conclusion

The evidence supports a precise but still provisional statement:

> The balanced Hopf chart supplies the coherent differential frame, metric
> weights, marker structure, and shared gradient records. A compiler inherits
> global Hopf backpropagation scaling when it implements the complete frame
> cleanly at cost sufficiently close to forward state preparation.

This repository contains an exact structural bridge from the addressed Hopf
frame to the unary--binary compiler architecture of Sun, Tian, Yang, Yuan, and
Zhang. It does not yet contain a proof that the frame reaches the later optimal
all-ancilla frontier of Yuan and Zhang for every workspace budget.

## Claim ledger

| Claim | Status | Evidence | Remaining work |
|---|---|---|---|
| Recursive balanced real Hopf frame equals the addressed layer product | Established here | Independent matrix constructions through `n=7` | None for the finite identity; retain notation audit |
| The first `t` full-system frame layers equal a `t`-qubit frame conditioned on a zero external suffix | Proved and tested | Algebraic proof; every cut through `n=8` | Independent human proof audit |
| The prefix frame acts as disjoint two-mode Givens layers in unary encoding | Proved and tested | Exact code action, unitarity, and zero leakage through `t=3`; combinatorial pair check through `t=8` | Gate-level clean-circuit diagram |
| A frame-safe recompilation preserves the global estimator | Proved algebraically | Clean-interface substitution argument | State as a formal theorem in the manuscript |
| Current unary-prefix/UCG construction has size `O(2**n)` | Theorem candidate | Geometric size ledger plus cited synthesis results | Check every reused workspace register against the source compiler |
| Current construction has depth `O(n(n-t+1)+2**n/(n+m))` using at most `m+1` clean ancillas | Theorem candidate | Exact bridge, term ledger, cited UCG/unary/MCT synthesis | Independent derivation and endpoint audit |
| The construction reproduces all three Figure 1 upper profiles of Sun et al. | Theorem candidate | Regime reductions in the companion | Verify notation against the journal version |
| The separated complex frame has the same profiles | Theorem candidate | `W_C=D_ph W_R` plus diagonal-synthesis bounds | Complete common-workspace audit |
| Record-wise Walsh decoding costs `O(S 2**n)` and matches FWHT decoding | Established here | Exact deterministic tests for `n=1,...,6` | Benchmark constants only if useful |
| The complete frame reaches `Theta(n+2**n/(n+m))` depth for every `m` | Open target | Optimal QSP benchmark known | New compiler construction or obstruction |
| Compiler robustness extends automatically to checkpoints | Not claimed | State-equivalent compilation can erase intermediate interfaces | Separate sufficient conditions or counterexample |
| The framework applies to arbitrary state charts | Not claimed | Hopf orthogonality and marker structure are special | Identify a genuinely broader class before renaming scope |

## Paper threshold

The project is ready for a standalone paper only after the following minimum
conditions are met:

1. A formal frame-safe substitution theorem with exact register contracts.
2. A line-by-line proof audit of the conditioned-prefix and unary clean-circuit
   construction.
3. A theorem valid for every ancillary budget, even if it is only within an
   explicitly bounded factor of the optimal QSP frontier.
4. Complete accounting of quantum executions, circuit size, circuit depth,
   clean workspace, parameter-generation work, and classical decoding.
5. A precise complex-chart statement.
6. A negative result explaining why arbitrary state-column compilation and
   arbitrary checkpoint recompilation do not follow.
7. Independent tests and a claim-support map that separate finite verification
   from asymptotic deduction.

## Preferred theorem hierarchy

The paper should aim for the following hierarchy rather than a single oversized
claim.

### Theorem A: frame-safe invariance

A clean implementation of the same differential-frame unitary preserves the
exact global protocol distribution and all record-level concentration premises.

### Theorem B: current all-workspace upper bound

For every `m>=0`, the real global Hopf frame has an exact implementation with
`O(2**n)` size, at most `m+1` clean ancillary qubits, and the candidate depth
bound recorded in `ANCILLA_DEPTH_ROBUSTNESS.md`.

### Corollary: compiler-robust Hopf backpropagation

Combine Theorem B with the global gradient record and output-sensitive decoder.
State the accuracy model explicitly.

### Target Theorem C: optimal frame compilation

Either prove

```math
D_{\mathrm{frame}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every `m`, or prove a separation/obstruction showing why a complete clean
differential frame is intrinsically harder than preparing one state column.

## Present release decision

- Suitable for private research development: **yes**.
- Suitable for a public theorem claim: **not yet**.
- Suitable for merging back into the established `Hopf-QBP` repository: **no**.
- Suitable as a seed for the new manuscript: **yes, after the first independent
  proof audit**.
