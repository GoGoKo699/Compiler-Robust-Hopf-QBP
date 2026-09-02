# Related compiler work and citation policy

## Active framework

The active compiler framework and the sole general state-preparation benchmark
used by this project are from:

P. Yuan and S. Zhang, "Optimal (controlled) quantum state preparation and
improved unitary synthesis by quantum circuits with any number of ancillary
qubits," *Quantum* **7**, 956 (2023),
[doi:10.22331/q-2023-03-20-956](https://doi.org/10.22331/q-2023-03-20-956).

The paper proves the uniform optimal state-preparation frontier

```math
S_{\mathrm{QSP}}(n,m)=\Theta(2^n),
```

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every ancillary budget. In the active Hopf proof, its multi-controlled-X,
uniformly controlled-gate, and coherent-copy results supply the standard-circuit
primitives used by the low-workspace compiler, branch router, controlled subtree
frames, and complex phase layer.

The project therefore does not choose between two prior state-preparation
compilers as a function of `m`. Yuan--Zhang supplies one uniform benchmark and
one uniform compiler framework.

## Historical predecessor

The preceding result is:

X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, "Asymptotically Optimal Circuit
Depth for Quantum State Preparation and General Unitary Synthesis," *IEEE
Transactions on Computer-Aided Design of Integrated Circuits and Systems*
**42**, 3301--3314 (2023),
[doi:10.1109/TCAD.2023.3244885](https://doi.org/10.1109/TCAD.2023.3244885).

Sun et al. established the first broad exact ancilla--depth landscape for state
preparation. Their constructions attained optimal order in the low- and
high-workspace regimes and left a logarithmic gap in the intermediate regime.
Yuan and Zhang subsequently closed that gap with a unified result valid for
every ancillary budget.

This earlier paper remains a significant historical citation. It is also the
original source to which Yuan--Zhang attribute selected circuit primitives.
Those original attributions should be retained where technically relevant.
However, the active Hopf compiler no longer imports the earlier paper's
unary-to-binary construction or treats its three regimes as separate active
compiler choices.

## Earlier uniformly controlled constructions

The uniformly controlled-gate and state-transformation lineage also includes:

- M. Möttönen, J. J. Vartiainen, V. Bergholm, and M. M. Salomaa,
  "Transformation of quantum states using uniformly controlled rotations,"
  *Quantum Information and Computation* **5**, 467--473 (2005),
  [arXiv:quant-ph/0407010](https://arxiv.org/abs/quant-ph/0407010).
- V. Bergholm, J. J. Vartiainen, M. Möttönen, and M. M. Salomaa,
  "Quantum circuits with uniformly controlled one-qubit gates,"
  *Physical Review A* **71**, 052330 (2005),
  [arXiv:quant-ph/0410066](https://arxiv.org/abs/quant-ph/0410066).

These works are relevant to the historical development of multiplexed state
preparation and to the established Möttönen-style robustness result in the
`Hopf-QBP` repository. The present optimal compiler uses the later
Yuan--Zhang resource theorem as its active UCG statement.

## Relationship to this project

None of the prior compiler papers constructs the Hopf differential frame or
proves compiler-safe quantum backpropagation. The new ingredients here are:

1. the operator-level frame-safe substitution theorem;
2. exact counterexamples showing that state-column equality is insufficient;
3. the conditioned-prefix and tail direct-sum identities of the Hopf frame;
4. a self-contained reversible binary--one-hot tree decoder;
5. coherent route--parallel-subframes--unroute compilation;
6. optimal frame size and depth for every positive clean-workspace budget;
7. one-UCG synthesis of the complete complex phase layer under the same
   workspace pool; and
8. output-sensitive complete-gradient decoding.

## Citation rule used in the repository and manuscript

| Statement or construction | Primary citation treatment |
|---|---|
| Uniform optimal QSP frontier | Yuan--Zhang Theorem 2 |
| Active exact UCG bound | Yuan--Zhang Lemma 6; retain its original attribution where appropriate |
| Active multi-controlled-X bound | Yuan--Zhang Lemma 5 |
| Active coherent copy--use--uncopy | Yuan--Zhang Lemma 9; retain its original attribution where appropriate |
| Earlier ancilla--depth landscape and intermediate gap | Sun et al. |
| Möttönen-style multiplexed robustness | Möttönen et al., Bergholm et al., and the established `Hopf-QBP` analysis |
| Hopf tree decomposition, tree decoder, router, and frame theorem | This project |

Chronology alone is not the reason for selecting Yuan--Zhang. It is selected
because its theorem strictly strengthens the earlier QSP depth result and gives
the final optimal frontier for every ancillary budget in the common exact
standard-circuit model.
