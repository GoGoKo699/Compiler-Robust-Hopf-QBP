# Independent review guide

## Purpose

This guide is the shortest reviewer-facing route through the proposed optimal
all-workspace Hopf-frame theorem. It is written for an independent quantum
circuit-synthesis or quantum-algorithms specialist who has not participated in
the construction.

The active review target is:

```text
PR #20: Consolidate the optimal all-workspace Hopf-frame compiler
branch: all-workspace-unified-final
```

The repository's internal audits and deterministic tests are supporting
material only. They do not count as independent review.

## The statement under review

Let

```math
N=2^n
```

and let `m>=0` be the number of clean ancillary qubits available to the
compiler. The proposed theorem is that the complete real Hopf differential
frame and the separated complex frame admit exact frame-safe implementations
using at most `m` clean ancillary qubits, with

```math
S_{\mathbb R}(n,m)=S_{\mathbb C}(n,m)=\Theta(N),
```

```math
D_{\mathbb R}(n,m)=D_{\mathbb C}(n,m)
=\Theta\left(n+\frac{N}{n+m}\right)
```

for every integer `m>=0` in the exact all-to-all circuit model with arbitrary
one-qubit gates and CNOTs.

The result is stronger than state preparation: the compiled circuit must act as
the full differential-frame unitary on every clean-workspace system input and
must return all compiler workspace to zero.

## Imported results

The sole active external compiler framework and state-preparation benchmark is
P. Yuan and S. Zhang, *Quantum* **7**, 956 (2023). The proof uses:

- Theorem 2: the optimal arbitrary-state-preparation size--depth frontier;
- Lemma 5: exact ancilla-free multi-controlled X with linear size and depth;
- Lemma 6: exact total-width-`q` uniformly controlled gates with
  `O(2**q)` size and `O(q+2**q/(q+w))` depth using `w` clean work qubits;
- Lemma 9: coherent copy--use--uncopy by CNOT trees.

Sun, Tian, Yang, Yuan, and Zhang are retained as the historical predecessor and
original source credited for selected primitives. The active proof does not
select between the two papers by workspace regime.

## Recommended review order

### 1. Compiler contract and obstruction

Read:

```text
docs/FRAME_SAFE_COMPILATION.md
docs/COMPILER_BOUNDARIES.md
```

Check that the global protocol genuinely requires the complete clean-input
operator action, and that the state-column counterexample invalidates a weaker
compiler promise.

### 2. Exact Hopf tree structure

Read:

```text
docs/THEOREM_OVERVIEW.md
compiler_robust_hopf/frames.py
compiler_robust_hopf/tree_structure.py
```

Reconstruct the addressed layers and verify the conditioned-prefix and tail
direct-sum identities as complete operators.

### 3. Strict zero workspace

Read:

```text
docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md
docs/STRICT_ZERO_ECHO_AUDIT.md
compiler_robust_hopf/strict_zero_echo.py
```

The key independent checks are:

1. derive the four `(h,b)` sectors without using the implementation;
2. distinguish chronological gate order from matrix multiplication order;
3. verify `C_p^2=R_y(theta_p)` and `X C_p X=C_p^{-1}` in the stated convention;
4. verify that the borrowed suffix qubit is restored with no branch-dependent
   phase on arbitrary, possibly entangled input;
5. verify that each half-angle UCG has total width exactly `d+2`;
6. verify that the predicate toggle uses no ancillary wire under the imported
   multi-controlled-X result;
7. check `n=1`, `d=0`, `d=n-2`, and final-depth endpoints;
8. rederive the `O(N)` size and `O(n+N/n)` depth sums;
9. rederive the matching strict-zero parameter-count lower bounds.

### 4. Positive workspace

Read:

```text
docs/UNIFIED_YUAN_ZHANG_COMPILER.md
compiler_robust_hopf/tree_decoder.py
compiler_robust_hopf/unified_compiler.py
compiler_robust_hopf/resource_bounds.py
```

Check separately:

- the explicit reversible binary--one-hot decoder and exact clean return;
- its register count and disjoint depth schedule;
- coherent routing on arbitrary prefix--suffix entanglement;
- branch data, activation tokens, copied controls, reusable flags, and peak
  workspace;
- controlled subtree-frame widths and resource sums;
- the low-workspace absorption argument;
- the largest-feasible-cut inequality and all endpoint regimes;
- the `Omega(n)` and `Omega(N/(n+m))` depth lower bounds.

### 5. Complex frame and QBP consequence

Read:

```text
docs/END_TO_END_QBP.md
compiler_robust_hopf/complex_analysis.py
compiler_robust_hopf/decoders.py
```

Verify that the arbitrary leaf-phase diagonal is one exact UCG, that the real
and diagonal blocks reuse one clean workspace pool sequentially for every
`m>=0`, and that frame-safe substitution preserves the global-gradient
measurement distribution. Check the controlled-observable and accuracy model
whenever the final QBP time ratio is quoted.

### 6. Prior-art boundary

Read:

```text
docs/STRICT_ZERO_PRIOR_ART.md
docs/PRIOR_ART_SEARCH_2026_09.md
provenance/literature.json
provenance/prior_art_search.json
```

The repository does not claim invention of borrowed or dirty ancillas,
conditionally clean ancillas, toggle detection, controlled-unitary square-root
identities, or generic UCGs. The proposed project-specific contribution is the
Hopf-layer aggregation into two total-width-`d+2` UCGs and linear predicate
toggles, together with the resulting optimal strict-zero complete-frame
frontier.

A bounded negative search is not proof of novelty or priority. The reviewer
should inspect the closest circuit diagrams, appendices, cited and citing work,
theses, patents, and software before accepting or narrowing that wording.

## Reproduction

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python validate.py
python scripts/unified_resource_ledger.py --n 12
python scripts/strict_zero_echo_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```

The deterministic suite checks complete operators at finite sizes, exact
workspace bookkeeping, resource inequalities, compiler counterexamples, and
decoders. None of these tests replaces the dimension-independent arguments.

## Requested review report

A useful independent report should state explicitly:

1. which imported theorem statements and circuit-model assumptions were
   checked;
2. whether the strict-zero four-sector operator proof is accepted;
3. whether the borrowed logical qubit and all clean workspace are restored;
4. whether every width, size, depth, and peak-workspace count is accepted;
5. whether the upper and lower bounds cover all `m>=0` endpoints;
6. whether the separated complex corollary and QBP consequence follow;
7. any correction required in notation, proof order, or scope;
8. whether the Hopf-specific novelty wording is acceptable or should be
   narrowed;
9. a clear verdict: accept, accept after listed corrections, or reject with a
   concrete obstruction.

The review should be recorded in Issues #12 and #17 or as a review on PR #20.
PR #20 must remain unmerged until those independent decisions are documented.
