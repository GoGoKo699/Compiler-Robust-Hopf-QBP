# Constant-clean research: checked progress

The arbitrary-angle upper bound has improved. The new
[operator-source compiler](constant_clean/OPERATOR_SOURCE_COMPILER.md) implements
every prescribed **complete real Hopf frame** with

```math
a=3,\qquad b\ge L+n+6,
\qquad T=O(N+nL),\qquad G=O(NL),\qquad N=2^n.
```

At the high-precision endpoint this gives

```math
L=N,\qquad a=3,\qquad b=N+O(\log N),
\qquad \Omega(N)\le\tau^*_{F,\mathbb R}\le O(N\log N).
```

The earlier upper bound was $`O(N^{3/2})`$. The lower bound is unchanged:
**a logarithmic gap remains**. The displayed clean and dirty allocations are
sufficient, not necessary. This result does not assert the same bound with
zero, one, or two clean qubits, or with every smaller constant multiple of
$`N`$ dirty qubits. The [endpoint brief](CONSTANT_CLEAN_ENDPOINT.md) gives the
complete model and other workspace regimes.

## How the construction works

The precision information is stored in a **charged operator on dirty work**.
It does not require that work to start in a special state.

1. A chain of fixed Clifford+T gates constructs a Hermitian unitary
   $`M=\sum_j a_j\Gamma_j`$. The Pauli operators $`\Gamma_j`$ anticommute,
   and their squared coefficients are binary weights.
2. An exact dirty XOR table, conjugated by Hadamards, flips selected signs:
   $`N_x=P_xMP_x^\dagger`$. The address chooses the signs encoding a sine
   or cosine coefficient. The lookup costs $`O(S)`$ T gates for $`S`$ rows,
   even though each row contains $`O(L)`$ bits; its Clifford cost includes
   every inserted bit.
3. Anticommutation gives
   $`(MN_x+N_xM)/2=c_xI`$ on the **entire dirty space**. A clean flag
   coherently selects the two orders. This produces the scalar coefficient
   without learning or erasing the unknown dirty input.
4. A second flag combines cosine and sine into half of the desired real
   rotation. Coherent amplitude amplification converts that block into a
   complete-output approximation. The third clean bit holds the suffix
   predicate needed by the Hopf layer.
5. Compose the tree layers with a summable error budget. The same work is
   reused without a reset; the full norm bound includes clean leakage,
   dirty return, literal phase, and arbitrary external references.

The Clifford-loader operator and its overlap algebra have earlier literature
precedents, credited in the proof. The contribution assessed here is the
native binary-weight specialization, dirty sign-table use, complete-output
rotation construction, and charged full-frame composition. No priority or
external-review claim is made.

## Why this changes the frontier

This is an implemented analytic construction for arbitrary angle tables,
with each quantum primitive charged. It does not assume the open fast
heterogeneous phase-batching conjecture. The operation is address dependent;
it is outside the earlier equivalence that required one common circuit to
implement every selected bank commutator.

At depth $`d`$, the T count is $`O(2^d+L+n-d+n^2)`$. Summing the table costs
is linear in $`N`$. The precision operator costs $`O(L+n-d)`$ at **each**
depth, leaving the $`nL`$ term. The predicate overhead sums to $`O(n^3)`$,
which is absorbed by $`O(N)`$. Clifford table insertion sums to $`O(NL)`$.
The proof records the simultaneous allocation $`b\ge L+n+6`$ explicitly.

The sufficient-clean matching theorem remains
$`\Theta(\sqrt{NL}+L+NL/q)`$ under its stated reservation. Its lower bound
and the exact CNOT theorem have not changed.

## A separate arithmetic advance

The [modular-lookup construction](constant_clean/MODULAR_LOOKUP_FOLLOWUP.md)
now gives an exact coherent table addition with zero clean work,
$`O(m+n)`$ dirty work, and

```math
T=O((N+m)\log(m+1)),\qquad
G=O(Nm\log(m+1)).
```

It batches carry extraction through whole-word XOR queries and uses a
sign-corrected dirty echo at each divide-and-conquer level. All dirty words
are restored exactly. This removes one missing arithmetic component of the
clock route, but a cheap joint precision clock remains unproved. The
operator-source frame compiler above does not use that clock or this adder.

## Earlier results that remain useful

| Result | What it establishes |
|---|---|
| [Shared-generator phase batching](constant_clean/IDENTICAL_PHASE_BATCHING.md) | One clean bit handles identical phases and bounded signed integer combinations of a few base angles. Its restricted-frame corollary still uses only one clean bit. |
| [Dirty-rank compression](constant_clean/DIRTY_RETURN_LOWER_BOUND_FOLLOWUP.md) | Rank $`O(\sqrt N)`$ forces worst-case $`\Omega(N^{3/2})`$ T count at the endpoint. Any linear-T family must use linear dirty symplectic rank on hard instances. |
| [Phase-bank reduction and converse](constant_clean/GLOBAL_BLOCK_FOLLOWUP.md) | Two batch calls and no extra clean bit produce an addressed rotation. Uniform selected commutators from one common circuit conversely supply the full bank, with a logarithmic precision margin. Fast arbitrary batching is still unproved. |
| [Restricted program and clock interfaces](constant_clean/JOINT_CLOCK_FOLLOWUP.md) | A one-addition clock needs growing initialized work; the common XOR-program interpreter has separate adjoint and rank restrictions. Their hypotheses do not cover the new operator-source construction. |

## Evidence and the next question

The [technical proof](constant_clean/OPERATOR_SOURCE_COMPILER.md) supplies the
uniform operator identities, native gate accounting, and error composition.
The [operator-source tests](../tests/test_operator_source_compiler.py) exercise
small native sources, sign tables, full-space accepted blocks, amplification,
and dirty/reference return. The [modular tests](../tests/test_modular_lookup_compiler.py)
check exact reversible arithmetic. Run all repository checks with

```bash
python validate.py
```

Finite checks support the algebra and conventions; they do not prove the
asymptotic theorem by enumeration. A general production gate emitter and
finite-size performance benchmark are not claimed.

The next main question is **whether the precision cost can be shared across
tree depths with constant clean work**, reducing $`O(N+nL)`$ to $`O(N+L)`$
at the endpoint. Cancellation between displayed subcircuits alone is not a
proof: every address-dependent sign lookup changes the intervening operator.
A complete global construction or a stronger unrestricted lower bound is
still needed to settle the remaining gap.
