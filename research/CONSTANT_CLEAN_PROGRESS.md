# Constant-clean research: checked progress

This is the reading entry for the research resumed on 22 September 2026.
The [endpoint brief](CONSTANT_CLEAN_ENDPOINT.md) supplies the complete model.
**No improvement to the unrestricted endpoint bounds has been proved:**

```math
a=O(1),\qquad b=\Theta(N),\qquad L=N,
\qquad \Omega(N)\le\tau^*_{F,\mathbb R}\le O(N^{3/2}).
```

The latest refinement removes the extra clean readout qubit from the
phase-bank-to-frame reduction and cuts its batch calls from four to two.
A converse theorem also shows that a common circuit implementing every
selected commutator already supplies a full phase bank, with a logarithmic
precision margin. This consolidates the two proposed batching routes into
one synthesis problem. The unrestricted endpoint and main sufficient-clean
theorem are unchanged.

## Proved construction: distinct angles from shared base angles

The [masked-accumulator construction](constant_clean/IDENTICAL_PHASE_BATCHING.md)
now covers phase tables of the form

```math
\theta_j=\sum_{a=1}^d k_{ja}\phi_a\pmod{2\pi},
\qquad k_{ja}\in\mathbb Z.
```

For a fixed number of base angles and polynomially bounded integer
coefficients, one clean qubit and logarithmic dirty work still suffice.
Every table entry can be different: $`\theta_j=j\phi`$ is a simple example.
The note gives the complete gate bound in terms of the coefficient sums,
including signed coefficients and an approximation budget for the table.

The circuit adds a weighted sum into a dirty accumulator. A fixed offset
centers the accumulator so negative terms do not wrap around; the clean
high bit supplies the remaining range. A phase followed by the actual inverse
arithmetic and phase removes the unknown starting value. The weighted sum
is never extracted into an initialized register.

The proof includes the literal scalar phase, clean leakage, arbitrary dirty
inputs and their reference entanglement. The same clean bit can be reused
across base angles without a reset, with errors added in the full-output norm.

For Hopf frames whose table at every depth has a fixed number of such base
angles and coefficients bounded by a fixed power of $`N`$, the addressed
improved reduction gives $`O(N\log^2 N)`$ T gates at $`L=N`$, using
**one clean qubit** and $`N/2+O(\log N)`$ dirty qubits. This is a sufficient bound for
a restricted family, not a claim of its optimal compilation cost.

**Different angles are now supported, but arbitrary angle tables remain
unresolved.** A covering argument shows that a fixed number of bases with
polynomial coefficients cannot represent all tables at the required
precision. Allowing enormous coefficients makes the accumulator and its
precision clock expensive again. This is a limitation of the representation,
not a new unrestricted frame lower bound.

The earlier identical-phase result remains a useful special case:
$`m`$ identical phases need one clean qubit, $`O(\log(m+1))`$ dirty
work, and $`O((m+L)\log(m+1))`$ T gates.

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
into an addressed determinant-one rotation. Temporarily swap the logical
target into the selected bank position, apply the selected phase commutator,
and swap back. The old dirty value is held on the logical target during the
batch calls, where the batch circuit does not act.

This uses **two batch calls and no additional clean qubit**. Complete batch
error $`\delta`$ contributes at most $`2\delta`$ to the addressed rotation,
including all work leakage and reference entanglement. A common scalar
cancels with the actual inverse. Inactive suffix sectors remain exactly
identity even for a dense, nondiagonal approximate batch circuit.

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

The apparently weaker selected-commutator contract is now understood more
fully. If the **same** circuit $`A`$ satisfies the contract at every bank
position, write $`F=\prod_jX_j`$. The two-call circuit
$`FA^\dagger FA`$ produces the full rotation bank, with error at most
the sum of the selected errors and no extra workspace. Compiling half
angles gives the phase product up to the permitted common scalar.
Thus full batching and uniform selected-commutator synthesis reduce to
each other with $`O(\log S)`$ extra precision bits. The latter is a useful
design interface, but it does not bypass the unresolved batching problem.
The proof permits substantial clean-work leakage inside $`A`$ itself.

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

The next constructive task is a charged arbitrary-angle compiler under
either of these equivalent batch contracts, or a direct full-frame
construction. The compact shared-generator representation is insufficient
for general tables. Reoptimizing the retained compiler's existing resource
ledger did not lower its dominant endpoint term. An improved construction must
use the available dirty space beyond the rank-limited architecture above,
while avoiding the two restricted global interfaces. A proved smaller T
upper bound would update the frontier; an algebraic reduction with an
unimplemented subroutine does not.
