# Frame-safe compilation

[← Complete technical note](../REVIEW.md) · [Minimal Hopf interface](HOPF_INTERFACE.md) · [Compiler boundaries →](COMPILER_BOUNDARIES.md)

The state-preparation problem and the Hopf inverse-frame problem ask for
different operator promises. This page states the exact promise that allows a
compiled frame and its inverse to replace the logical Hopf frame without
changing the gradient record.

## 1. Three levels of compiler promise

Let `U` be a logical unitary on the system register and let `J` append `m` clean
work qubits:

```math
J|\varphi\rangle
=|\varphi\rangle|0^m\rangle.
```

Three promises should be kept separate.

| Promise | Equality | What it fixes |
|---|---|---|
| state-column correctness | `U_tilde J|alpha> = JU|alpha>` | one prepared input column |
| active-interface correctness | `U_tilde J P = e^(i chi) J U P` | a specified input subspace `P` |
| **complete frame safety** | `U_tilde J = J U` | every logical input column and exact workspace return |

Ordinary state preparation needs the first promise. A checkpoint protocol may
need the second. The global Hopf inverse-frame record uses the third.

## 2. Frame-safe definition

### Definition

A unitary `W_tilde` is a clean frame-safe implementation of `W` when

```math
\boxed{
\widetilde WJ=JW.
}
```

Equivalently, for every system state,

```math
\widetilde W
\bigl(|\varphi\rangle|0^m\rangle\bigr)
=
\bigl(W|\varphi\rangle\bigr)|0^m\rangle.
```

The definition includes two requirements:

1. the logical action agrees with the complete frame;
2. all clean workspace is returned exactly to zero.

A circuit may use arbitrary coherent intermediate work. Only the final action
on the clean-input subspace is constrained.

## 3. Why the inverse is automatically safe

Let

```math
\mathcal K
=\mathcal H_{\mathrm{sys}}\otimes|0^m\rangle
```

be the clean-workspace subspace. If `W_tilde J=JW`, then `W_tilde` maps
`mathcal K` onto itself. Since `W_tilde` is unitary, `mathcal K` is a reducing
subspace. The restriction of `W_tilde` to `mathcal K` is unitarily equivalent to
`W`.

Taking the adjoint on the restricted block gives

```math
\boxed{
\widetilde W^{\dagger}J
=JW^{\dagger}.
}
```

No separate inverse-compiler theorem is required. Reversing the compiled circuit
also returns the workspace clean and implements the logical inverse frame.

### Consequence for any surrounding circuit

Suppose a larger circuit prepares a system state `|eta>` and clean workspace,
then applies `W_tilde^dagger`. The output is

```math
\widetilde W^{\dagger}
\bigl(|\eta\rangle|0^m\rangle\bigr)
=
\bigl(W^{\dagger}|\eta\rangle\bigr)|0^m\rangle.
```

All subsequent system measurements therefore have the same distribution as in
the logical circuit.

## 4. Why one state column is weaker

First-column equality only states

```math
\widetilde WJ|0^n\rangle
=JW|0^n\rangle.
```

It places no condition on the marker inputs `|lambda(j)>` whose images are the
frame directions. The inverse circuit resolves the response on precisely those
columns.

The exact two-qubit construction in
[Compiler boundaries](COMPILER_BOUNDARIES.md) gives two unitaries `W` and `V`
with

```math
V|00\rangle=W|00\rangle=|\psi\rangle,
```

but with two marker columns exchanged. For

```math
O=-Z\otimes I,
```

the decoded gradient changes from

```math
(2,0,0)
```

to

```math
(0,\sqrt2,0).
```

The obstruction is not approximation error. Both circuits prepare the same
state exactly. The difference lies entirely in the unitary completion.

<p align="center">
  <img src="../assets/state-vs-frame.svg" width="900" alt="State preparation fixes one column, while frame-safe compilation fixes the complete state-and-marker unitary." />
</p>

## 5. Application to the global Hopf record

The global magnitude circuit prepares coherent reference and objective-response
branches and then applies `W^dagger`. If `W_tilde` is frame-safe, the reducing-
subspace identity gives exactly the same premeasurement state with an appended
zero workspace register.

Therefore frame-safe substitution preserves:

- every branch amplitude;
- the complete X-basis output distribution;
- all marker parities;
- every raw-coordinate estimator;
- the fixed record-norm bound;
- the concentration and decoder arguments.

The compiler theorem supplies such a frame-safe implementation for every clean
workspace budget `m>=0`.

## 6. Checkpoint interfaces

A checkpoint circuit factors the preparation as

```math
U=B_dA_d
```

and reverses only the suffix `B_d`. Let `P_d` project onto the complete interface
subspace that may enter `B_d` during the checkpoint experiment.

A sufficient compiled-suffix condition is

```math
\boxed{
\widetilde B_dJP_d
=e^{i\chi}JB_dP_d,
}
```

where the phase `chi` is independent of the input vector in the interface.
Consistent forward and inverse use then preserves the designated checkpoint
means.

This condition is weaker than global frame safety because it constrains only the
active interface. It is stronger than preserving one prepared prefix state.

The exact examples in [Compiler boundaries](COMPILER_BOUNDARIES.md) show both
sides:

- one correct checkpoint state can still give the wrong derivative;
- active-interface equality can preserve the decoded mean without preserving
  the complete output distribution.

## 7. Practical substitution rule

A compiler can be inserted safely according to the operator actually consumed
by the algorithm.

| Algorithmic use | Sufficient compiler statement |
|---|---|
| prepare one state and measure it directly | first-column equality |
| reverse a factor on a known subspace | complete active-interface equality |
| apply the inverse Hopf frame and decode all markers | complete frame safety |

This is an interface statement, not a restriction to one elementary
implementation. Any compiler satisfying the relevant equality is admissible.

## 8. Executable support

- [Exact global and checkpoint boundary constructions](../compiler_robust_hopf/compiler_boundaries.py)
- [Boundary tests](../tests/test_compiler_boundaries.py)
- [Complete compiler theorem](COMPILER_THEOREM.md)
- [QBP consequence](QBP_CONSEQUENCE.md)

The finite examples prove the strict separation between the promises in the
smallest useful setting. The general substitution theorem is the reducing-
subspace argument above.

---

[← Complete technical note](../REVIEW.md) · [Minimal Hopf interface](HOPF_INTERFACE.md) · [Compiler boundaries →](COMPILER_BOUNDARIES.md)
