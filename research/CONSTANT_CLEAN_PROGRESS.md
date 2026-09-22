# Constant-clean research: checked progress

This is the reading entry for the research resumed on 22 September 2026.
The [endpoint brief](CONSTANT_CLEAN_ENDPOINT.md) supplies the complete model.
**No improvement to the unrestricted endpoint bounds has been proved:**

```math
a=O(1),\qquad b=\Theta(N),\qquad L=N,
\qquad \Omega(N)\le\tau^*_{F,\mathbb R}\le O(N^{3/2}).
```

The latest constructive result batches identical phases with one clean qubit
and logarithmic dirty work. Earlier results characterize useful dirty workspace,
restrict two proposed global shortcuts, and identify missing synthesis tasks.
These results support continued research; they do not change the main
sufficient-clean theorem.

## Latest construction: identical phases with one clean qubit

For an arbitrary angle, a product of $`m`$ identical phase gates can be
approximated to complete-output error $`2^{-L}`$ using

```math
a=1,\qquad b=O(\log(m+1)),\qquad
T,G=O((m+L)\log(m+1)).
```

The [construction and proof](constant_clean/IDENTICAL_PHASE_BATCHING.md)
use a dirty binary accumulator with one initialized high bit. Add the input's
Hamming weight, apply a phase proportional to the accumulator value, and
reverse the addition. A matching inverse phase removes the accumulator's
unknown starting value. The high bit gives enough room to prevent wraparound;
the Hamming weight is never extracted into an initialized count register.
Only logarithmically many one-qubit phases need synthesis. Existing coherent
dirty-work arithmetic supplies the increment operations.

The proof includes the literal scalar phase, clean leakage, arbitrary dirty
inputs and their reference entanglement. The approximate circuit uses the
actual inverse of its synthesized phase operator. The note also gives a
simple explicit arithmetic implementation and finite regression checks.

This is a proved restricted primitive. The phase bank needed for an arbitrary
Hopf layer contains **different** angles. Decomposing all of those angles
into dyadic layers introduces a precision-dependent number of batches, so
the construction does not establish a smaller unrestricted frame bound.

## 1. The relevant dirty workspace can be characterized

Write the whole native circuit as Pauli rotations followed by a Clifford. Restrict
the Pauli labels to the dirty wires, and let $`r_D`$ be half the rank of their
binary symplectic pairing matrix. It counts independent noncommuting Pauli
pairs in this description; it is not the total number of allocated wires.

The [dirty-rank compression lemma](constant_clean/DIRTY_RETURN_LOWER_BOUND_FOLLOWUP.md)
shows that a circuit satisfying the complete return contract with error below
$`1/\sqrt2`$ can be replaced using at most $`r_D`$ dirty qubits, with no
increase in T count, clean count, or error. Commuting dirty directions and
unused spectators can be removed. Arbitrary borrowed workspace cannot all be
removed at the same T cost.

Combining this compression with the existing counting lower bound gives two
useful worst-case consequences at $`L=N`$ and constant clean width:

- If a compiler family has $`r_D=O(\sqrt N)`$, it needs
  $`\Omega(N^{3/2})`$ T gates on some frames. The retained borrowed compiler
  attains this order using $`O(\sqrt N)`$ active dirty wires.
- Any family attaining $`O(N)`$ T gates for all frames must use
  $`r_D=\Omega(N)`$ on hard instances.

Thus merely allocating a larger bank does not close the gap. An improved
construction must change how its non-Clifford operations use that bank.
These statements concern worst-case families, not every angle tuple or every
individual frame.

## 2. Two proposed global shortcuts have stronger restrictions

| Interface | Checked restriction | What remains outside it |
|---|---|---|
| One common XOR-loaded interpreter | The adjoint obstruction persists for same-embedding accepted blocks. Allowing different input/output flags still leaves a Fourier-rank bound when one interpreter serves the stated whole program family. | An interpreter recompiled for the target, more queries, and other bank transformations. |
| One-addition phase kickback | An $`m`$-bit cyclic clock needs at least $`m`$ initialized work qubits for uniform complete-output error below one, even with arbitrary work encoding and arbitrarily much dirty work. | Multiple interleaved additions, input-dependent encoding, direct clock synthesis, and a directly implemented Weyl commutator. |

The proofs are in [global program blocks](constant_clean/GLOBAL_BLOCK_FOLLOWUP.md)
and [joint dirty clocks](constant_clean/JOINT_CLOCK_FOLLOWUP.md). Their quantifiers
matter: neither is an unrestricted clean-space or T-count lower bound for
the Hopf frame. The Fourier averages used in the proofs are mathematical
operations, not measurements inserted into the compiler.

## 3. A precise conditional route through batched phases

A product of different one-qubit phase gates on a dirty bank can be converted
into an addressed determinant-one rotation. A clean bit temporarily records
the selected dirty bit; two echoes and a sign correction remove its unknown
value. The actual phase-bank circuit is used twice forward and twice backward.
Its complete approximation error contributes at most four times its own
error, including work leakage. A common phase cancels with the actual inverse.

This is an exact reduction, not a fast implementation of the phase bank.
If an arbitrary $`S`$-gate phase product admitted full-input synthesis with
$`O(S+\ell)`$ T gates, $`O(S\ell)`$ Clifford gates, constant clean work,
and $`O(S+\ell)`$ dirty work at precision $`2^{-\ell}`$, the reduction would
give the full frame $`O(N\log N)`$ T count at the selected endpoint.
That would be intermediate progress, rather than the desired $`O(N)`$ result.

**The batch-synthesis hypothesis remains unproved.** It is stronger than the
available heterogeneous batching theorem discussed in
[the literature follow-up](constant_clean/ENDPOINT_LITERATURE_FOLLOWUP.md).
It should not be mistaken for an existing compiler primitive. The precise
circuit, workspace and error ledger are recorded with the global-block work.

The separate [modular-lookup follow-up](constant_clean/MODULAR_LOOKUP_FOLLOWUP.md)
also gives a valid sign-corrected echo using a weighted subset-sum interpreter.
Its arithmetic cost is still unresolved. These reductions escape the earlier
restricted XOR echo because they introduce and charge additional operations.

## 4. Evidence and the next task

The general statements rest on their proofs. Small full-space and exact
finite checks exercise Pauli restrictions, dirty/reference return, Fourier
signs, cross-flag blocks, and the new echo identities. Run them with

```bash
python -m unittest tests.test_constant_clean_structure tests.test_identical_phase_batching
```

The source review records the precise hypotheses of the inspected synthesis,
lookup and catalytic results. It is not an exhaustive novelty certification
or external peer review.

The next constructive task is to extend the identical-phase primitive to
heterogeneous phases, or implement the weaker selected-commutator contract in
the [phase-bank reduction](constant_clean/GLOBAL_BLOCK_FOLLOWUP.md), and
charge all operations. An improved arbitrary-frame construction must
use the available dirty space beyond the rank-limited architecture above,
while avoiding the two restricted global interfaces. A proved smaller T
upper bound would update the frontier; an algebraic reduction with an
unimplemented subroutine does not.
