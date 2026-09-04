# Prior-art boundary for the strict-zero borrowed-suffix echo

## Purpose

This note records the current technical prior-art assessment for the exact
$m=0$ Hopf-frame compiler. It is deliberately conservative. It does not claim
that the abstract echo is a newly invented universal identity. This note is not
a legal novelty opinion.

## 1. The project construction

At nonfinal Hopf depth $d$, the desired layer applies a prefix-selected
$R_y(\theta_p)$ exactly when the complete lower suffix is zero. One original
suffix data qubit $b$ is borrowed, while $r$ denotes the remaining suffix and

```math
h(r)=[r=0].
```

Set

```math
C_p=R_y(\theta_p/2).
```

The chronological sequence

```text
controlled_b(X)
T_h
controlled_b(C_p)
T_h
controlled_b(X)
T_h
controlled_b(C_p)
T_h
```

uses $T_h$ to toggle $b$ iff $h(r)=1$. It relies on

```math
C_p^2=R_y(\theta_p),
\qquad
X C_p X=C_p^{-1}.
```

The unwanted original-$b=1$ sector receives a cancelling word, the desired
original-full-suffix-zero sector receives $R_y(\theta_p)$, and $b$ is restored.
All prefix-dependent half-angle rotations are aggregated into two UCGs of total
width $d+2$.

## 2. Controlled-unitary square roots

Barenco et al., "Elementary gates for quantum computation" (1995), use square
roots of unitaries together with controlled-NOT and conjugation identities in
multi-controlled-unitary decompositions. The broad algebraic pattern

```math
V^2=U
```

combined with conjugation to reverse $V$ is therefore established circuit
technology rather than a new theme introduced here.

Claudon et al., "Polylogarithmic-depth controlled-NOT gates without ancilla
qubits" (2024), also discuss controlled-unitary reductions using roots of the
target unitary and distinguish borrowed from zeroed ancillary qubits.

**Implication for claims:** do not call the square-root/conjugation mechanism
itself new.

## 3. Borrowed and dirty ancillas

Borrowed qubits are unknown-state wires temporarily modified and restored by
the end of a circuit. Claudon et al. use borrowed ancillas in exact
multi-controlled-NOT constructions.

Khattar and Gidney, "Rise of conditionally clean ancillae for efficient quantum
circuit constructions" (2025), describe laddered toggle detection: a
self-inverse controlled operation can be repeated so that an unknown dirty-
control branch cancels while the desired branch survives. They also develop
conditionally clean system qubits as temporary workspace.

**Difference here:**

- the borrowed wire is part of the logical suffix predicate;
- the desired operation is a generic angle-dependent rotation and is not
  self-inverse;
- the circuit must distinguish the borrowed bit's original value;
- half-angle factorization and Pauli conjugation produce cancellation without
  assuming the borrowed bit is clean.

**Implication for claims:** the use of a restored unknown system wire is related
to borrowed/dirty-ancilla techniques and should be cited accordingly.

## 4. Uniformly controlled rotations

Möttönen et al. and Bergholm et al. established the standard uniformly
controlled-rotation and one-qubit multiplexor constructions. Yuan and Zhang
later give the all-ancilla exact UCG size--depth theorem used in the present
resource proof.

The older `Hopf-QBP` robustness compiler uses one clean flag to compress the
lower-suffix-zero predicate and then applies one prefix-and-flag UCG. The new
strict-zero construction removes that clean flag by borrowing one suffix data
qubit and replacing the one flagged UCG by two half-angle UCGs plus an echo.

**Implication for claims:** the UCG primitive is imported; the project claim is
about how the Hopf layer is reduced to a constant number of smaller UCGs.

## 5. Sparse and restricted UCGs

Xu et al., "A Unified Framework for Optimizing Uniformly Controlled Structures
in Quantum Circuits" (2025), introduce restricted UCG models and analyze
control-support sparsity. Other multiplexer-optimization work exploits repeated
or identity blocks.

The addressed Hopf layer has a sparse logical block table, but its all-zero
suffix condition becomes generically dense under the standard Möttönen
Walsh/Gray-code angle transform. The strict-zero echo avoids this transform by
factoring the condition through one borrowed suffix bit.

The current search did not locate the same two-UCG borrowed-suffix reduction in
restricted-UCG work. This absence is not a proof of novelty.

## 6. Multi-controlled rotations

There is substantial literature on ancilla-free multi-controlled $SU(2)$ gates
and multi-controlled-NOT gates. Such results can implement one conditioned
rotation efficiently in the number of controls, but applying them independently
for all $2^d$ prefix values may introduce an extra factor in size or depth.

The Hopf compiler instead aggregates all prefix values into two total-width-
$d+2$ UCGs, preserving the geometric $O\!\left(2^d\right)$ contribution of one tree depth.

## 7. Claim-safe novelty statement

The strongest currently defensible statement is:

> For the addressed Hopf frame, one original suffix data qubit can serve as a
> restored predicate carrier. A four-toggle half-angle echo reduces all
> prefix-dependent rotations at depth $d$ to two total-width-$d+2$ UCGs and
> linear-size predicate toggles. Summing the tree depths yields an exact
> ancilla-free complete-frame compiler with $\Theta\!\left(2^n\right)$ size and
> $\Theta\!\left(n+\frac{2^n}{n}\right)$ depth.

The following statements should not be used:

- “We invent borrowed ancillas.”
- “We invent toggle detection.”
- “We give the first square-root controlled-unitary echo.”
- “No prior circuit uses this identity.”
- “The generic echo is novel.”

## 8. Search record

The current search covers:

- controlled-unitary decompositions and roots of unitaries;
- Möttönen/Bergholm multiplexors;
- exact and approximate multi-controlled gates;
- borrowed and dirty ancillas;
- conditionally clean ancillas and toggle detection;
- restricted and sparse UCGs.

Primary references currently retained are:

1. A. Barenco et al., *Physical Review A* **52**, 3457--3467 (1995),
   [arXiv:quant-ph/9503016](https://arxiv.org/abs/quant-ph/9503016).
2. M. Möttönen et al., *Quantum Information and Computation* **5**, 467--473
   (2005), [arXiv:quant-ph/0407010](https://arxiv.org/abs/quant-ph/0407010).
3. V. Bergholm et al., *Physical Review A* **71**, 052330 (2005),
   [arXiv:quant-ph/0410066](https://arxiv.org/abs/quant-ph/0410066).
4. P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023),
   [doi:10.22331/q-2023-03-20-956](https://doi.org/10.22331/q-2023-03-20-956).
5. B. Claudon et al., *Nature Communications* **15**, 5886 (2024),
   [doi:10.1038/s41467-024-50065-x](https://doi.org/10.1038/s41467-024-50065-x).
6. T. Khattar and C. Gidney, *Quantum* **9**, 1752 (2025),
   [doi:10.22331/q-2025-05-21-1752](https://doi.org/10.22331/q-2025-05-21-1752).
7. C. Xu et al., arXiv:2512.08675,
   [arXiv:2512.08675](https://arxiv.org/abs/2512.08675).

## 9. Remaining prior-art gate

Before manuscript submission:

1. search references cited by Barenco, Claudon, Khattar--Gidney, and restricted-
   UCG papers;
2. search controlled multiplexors with borrowed targets or dirty controls;
3. search reversible predicate-carrier and quantum Shannon decomposition
   literature;
4. compare exact circuit diagrams, not only abstracts and asymptotic statements;
5. ask an independent circuit-synthesis specialist to review the novelty wording.

Until then, repository and manuscript language should describe the strict-zero
result as a Hopf-specific construction with familiar ingredients.
