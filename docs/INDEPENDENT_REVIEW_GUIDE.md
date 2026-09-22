# A reading route through the compiler paper

[Landing page](../README.md) · [Continuous narrative](../REVIEW.md) · [Evidence](VERIFICATION.md)

The paper asks one question: how expensive is it to implement the prescribed
Hopf differential frame while preserving its gradient-readout function?
It answers that question in an exact logical model and an approximate
Clifford+T model. A reader can assess the story before inspecting the circuits.

## First pass: understand the claim

Allow about 30 minutes for these selected sections.

1. Read the opening of [the narrative](../REVIEW.md) and its two-qubit
   completion example. Explain why keeping the prepared state alone changes
   the inverse-frame readout.
2. Read the [minimal interface](HOPF_INTERFACE.md): the state column, marker
   columns, incoming weights, and addressed tree layers. These are the geometry
   facts consumed by the compilers.
3. Compare the two theorem statements in the narrative. The exact theorem
   optimizes size/depth at every clean budget. The T theorem optimizes
   non-Clifford count at finite precision under its stated clean reservation.
4. Read narrative Sections 9–10 for the shared-source idea and the fixed-parameter
   QBP consequence. The finer compiler proofs can wait until the second pass.

By this point, the reader should be able to state the target operator, the
workspace promises, the accuracy target, and the remaining endpoint without
knowing the research history.

## Second pass: inspect the two compiler proofs

| Question | Where to inspect it |
|---|---|
| Are all columns preserved, including singular chart continuations? | [Hopf interface](HOPF_INTERFACE.md) and [compiler contract](FRAME_SAFE_COMPILATION.md) |
| How is a suffix borrowed and restored on arbitrary inputs? | [Strict-zero construction](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) |
| Why does more clean workspace reduce exact depth? | [Exact theorem](COMPILER_THEOREM.md), tree cut and route–operate–unroute |
| Where does the single precision charge come from? | [T-count theorem](FAULT_TOLERANT_COMPILER.md), source return and streamed correction |
| Which work registers must be included in the final reflection? | T-count theorem, full-output and workspace ledger |
| How does approximate implementation affect gradient estimates? | [Approximation proof](QBP_APPROXIMATION.md) |
| Which ingredients and lower bounds are inherited? | [Source map](SOURCE_MAP.md) and [related work](RELATED_WORK.md) |

The constructions need not be the same circuit, and their optima concern
different cost functions. In particular, the T theorem's conservative Clifford
budget must not be read as simultaneous CNOT optimality.

## Third pass: inspect the evidence

Start with [the evidence map](VERIFICATION.md), then run:

```bash
python scripts/reviewer_walkthrough.py
python validate.py
python scripts/verify_fault_tolerant.py
```

The first command is a short exact-model orientation. The second checks the
logical interfaces, circuits, decoders, provenance, and documentation. The
third reproduces focused finite-precision receipts. Each guide distinguishes
analytic proofs, finite exact identities, floating-point examples, and resource
proxies. The asymptotic shared-source compiler does not yet have a general
local elementary-gate emitter.

## The question deliberately left open

At $a=2$, $b\ge N+n+7$, and $L=N$, the known bounds here are $\Omega(N)$
and $O(N\log N)$. The new
[operator-source proof](../research/constant_clean/OPERATOR_SOURCE_COMPILER.md)
should be checked at the full-dirty-space anticommutator, controlled source,
dirty suffix echo, normalization-two amplification, and simultaneous workspace
ledger. Its banked lookup and literal diagonal corollaries extend the same
contract to additional workspace regimes and the complex magnitude frame. Its finite
checks do not replace these arguments. The
[continuation brief](../research/CONSTANT_CLEAN_ENDPOINT.md) records the remaining
gap and the smaller budgets not covered by this sufficient allocation.

The complete frame is the compiler target. Its lower bounds do not rule out
other gradient algorithms using different measurements or classical processing.
The observable-access cost and full classical gradient output remain explicit
parts of any end-to-end comparison.
