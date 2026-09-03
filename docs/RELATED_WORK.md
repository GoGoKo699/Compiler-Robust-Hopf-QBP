# Related compiler work and citation policy

## Active framework

The sole active external compiler framework and general state-preparation
benchmark used by this project are from:

P. Yuan and S. Zhang, "Optimal (controlled) quantum state preparation and
improved unitary synthesis by quantum circuits with any number of ancillary
qubits," *Quantum* **7**, 956 (2023),
[doi:10.22331/q-2023-03-20-956](https://doi.org/10.22331/q-2023-03-20-956).

They prove the uniform optimal state-preparation frontier

```math
S_{\mathrm{QSP}}(n,m)=\Theta(2^n),
```

```math
D_{\mathrm{QSP}}(n,m)
=\Theta\left(n+\frac{2^n}{n+m}\right)
```

for every ancillary budget. Their exact multi-controlled-X, uniformly
controlled-gate, and coherent-copy results provide the standard-circuit
primitives used by all three internal Hopf schedules and by the complex phase
layer.

The project does not choose between two prior state-preparation compilers as a
function of `m`.

## Historical predecessor

The preceding state-preparation result is:

X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang, "Asymptotically Optimal Circuit
Depth for Quantum State Preparation and General Unitary Synthesis," *IEEE
Transactions on Computer-Aided Design of Integrated Circuits and Systems*
**42**, 3301--3314 (2023),
[doi:10.1109/TCAD.2023.3244885](https://doi.org/10.1109/TCAD.2023.3244885).

Sun et al. established the first broad exact ancilla--depth landscape for state
preparation, attained optimal order in the low- and high-workspace regimes, and
left an intermediate logarithmic gap later closed by Yuan and Zhang.

This paper remains a significant historical citation and the original source to
which Yuan--Zhang attribute selected primitives. It is not an alternative active
compiler path in this repository.

## Uniformly controlled gates

The UCG and multiplexed-state-preparation lineage includes:

- M. Möttönen, J. J. Vartiainen, V. Bergholm, and M. M. Salomaa,
  "Transformation of quantum states using uniformly controlled rotations,"
  *Quantum Information and Computation* **5**, 467--473 (2005),
  [arXiv:quant-ph/0407010](https://arxiv.org/abs/quant-ph/0407010).
- V. Bergholm, J. J. Vartiainen, M. Möttönen, and M. M. Salomaa,
  "Quantum circuits with uniformly controlled one-qubit gates,"
  *Physical Review A* **71**, 052330 (2005),
  [arXiv:quant-ph/0410066](https://arxiv.org/abs/quant-ph/0410066).

These works explain the older Möttönen-style robustness result in `Hopf-QBP`.
The present resource theorem uses the stronger all-ancilla UCG bound restated
and optimized in Yuan--Zhang.

## Square-root controlled-unitary decompositions

Square roots and Pauli conjugations are classical ingredients in controlled-
unitary synthesis. A standard source is:

A. Barenco et al., "Elementary gates for quantum computation," *Physical
Review A* **52**, 3457--3467 (1995),
[arXiv:quant-ph/9503016](https://arxiv.org/abs/quant-ph/9503016).

Related modern controlled-gate work includes:

B. Claudon, J. Zylberman, C. Feniou, F. Debbasch, A. Peruzzo, and J.-P. Piquemal,
"Polylogarithmic-depth controlled-NOT gates without ancilla qubits," *Nature
Communications* **15**, 5886 (2024),
[doi:10.1038/s41467-024-50065-x](https://doi.org/10.1038/s41467-024-50065-x).

That work distinguishes zeroed and borrowed ancillas and recalls square-root
controlled-unitary reductions. These precedents mean that the abstract identity
underlying the strict-zero echo should not be presented as wholly new.

## Dirty and conditionally clean ancillas

T. Khattar and C. Gidney, "Rise of conditionally clean ancillae for efficient
quantum circuit constructions," *Quantum* **9**, 1752 (2025),
[doi:10.22331/q-2025-05-21-1752](https://doi.org/10.22331/q-2025-05-21-1752),
develop conditionally clean ancillas and laddered toggle detection. In
particular, they describe the well-known replacement of a clean control bit by a
dirty bit for self-inverse controlled operations, at the cost of repeating the
controlled operation.

The Hopf strict-zero construction is related but not identical:

- the borrowed bit is one of the original suffix data qubits;
- the desired rotation is not self-inverse;
- the desired predicate includes the borrowed bit's **original** value;
- the half-angle relation and Pauli conjugation make the unwanted borrowed-bit
  sector cancel exactly.

## Restricted and sparse UCG synthesis

Recent work on restricted UCGs includes:

C. Xu, X. Chen, X. Li, Z. Liu, and Z. Li, "A Unified Framework for Optimizing
Uniformly Controlled Structures in Quantum Circuits," arXiv:2512.08675,
[arXiv:2512.08675](https://arxiv.org/abs/2512.08675).

That paper studies algebraic and control-support restrictions in UCG-like
structures. It is relevant to the broader sparse-multiplexor context, but the
current project has not identified in it the same zero-suffix Hopf-layer echo or
the resulting complete-frame all-workspace theorem.

## What this project claims

None of the sources above is currently known to construct the complete Hopf
differential frame or prove compiler-safe Hopf backpropagation. The project
contributions are:

1. the operator-level frame-safe substitution theorem;
2. exact counterexamples showing state-column equality is insufficient;
3. conditioned-prefix and tail direct-sum identities for the Hopf frame;
4. a self-contained reversible binary--one-hot decoder;
5. coherent route--parallel-subframes--unroute compilation;
6. the borrowed-suffix echo for strict zero workspace;
7. optimal frame size and depth for every clean ancillary budget;
8. one-UCG synthesis of the complete complex phase layer under the same budget;
9. output-sensitive complete-gradient decoding.

The strict-zero novelty wording is intentionally narrow:

> One original suffix data qubit is used as a restored predicate carrier so
> that all prefix-dependent Hopf rotations at depth `d` are aggregated into two
> total-width-`d+2` UCGs, closing the optimal complete-frame frontier at strict
> zero ancillary workspace.

The repository does **not** claim that the generic square-root/conjugation echo,
borrowed-bit controls, or toggle detection were invented here.

## Citation rule

| Statement or construction | Primary citation treatment |
|---|---|
| Uniform optimal QSP frontier | Yuan--Zhang Theorem 2 |
| Active exact UCG bound | Yuan--Zhang Lemma 6; retain original attribution where appropriate |
| Active multi-controlled-X bound | Yuan--Zhang Lemma 5 |
| Active coherent copying | Yuan--Zhang Lemma 9; retain original attribution where appropriate |
| Earlier ancilla--depth landscape | Sun et al. |
| Möttönen-style multiplexing | Möttönen et al. and Bergholm et al. |
| Square-root controlled-unitary lineage | Barenco et al.; Claudon et al. |
| Dirty/conditionally clean controls and toggle detection | Khattar--Gidney and cited predecessors |
| Hopf tree decomposition, decoder, router, echo aggregation, and frame theorem | This project |

## Evidence boundary

The prior-art search recorded here is a technical literature survey, not a legal
novelty opinion and not evidence that no equivalent construction exists. The
search should be repeated and broadened before manuscript submission.
