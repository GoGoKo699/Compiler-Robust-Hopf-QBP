# Claim support map

This page separates exact finite checks, algebraic proofs, imported synthesis
theorems, internally audited deductions, explicit counterexamples, and open
problems. Finite tests supplement but do not replace the analytic arguments.

## Evidence classes

| Class | Meaning |
|---|---|
| Exact matrix check | Independently constructed finite-dimensional operators are compared numerically |
| Algebraic proof | Dimension-independent identity proved in the documentation or manuscript |
| Explicit counterexample | Closed-form finite instance disproving a stronger statement |
| Imported synthesis theorem | Resource deduction uses a published compiler theorem under its hypotheses |
| Internally audited deduction | Logical, register, and asymptotic steps were re-derived in a separate audit |
| Term ledger | Code exposes every contribution but does not infer an asymptotic proof from fitting |
| Open problem | No proof claim |

## Source map for the optimal theorem

The positive-workspace optimal theorem uses two primary compiler sources.

| Source | Results used |
|---|---|
| Yuan and Zhang, *Quantum* 7, 956 (2023) | Standard circuit model; ancilla-free MCT; UCG tradeoff; coherent copying; CQSP size benchmark; optimal QSP frontier; lower-bound architecture |
| Sun, Tian, Yang, Yuan, and Zhang, IEEE TCAD 42, 3301--3314 (2023) | Unary-to-binary unitary used in the conditioned-prefix compiler and the earlier near-optimal construction |

The optimal QSP frontier is Theorem 2 of Yuan--Zhang. Figure 1 in that paper is
a general unitary-synthesis figure. The older Figure 1 discussed in the original
compiler question is from the Sun et al. paper.

## Compiler contracts and boundaries

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Frame-safe recompilation preserves the complete global protocol distribution | Algebraic reducing-subspace substitution theorem | `FRAME_SAFE_COMPILATION.md` | Requires complete system action on every clean-workspace input |
| State-column equality is insufficient for global Hopf QBP | Explicit two-qubit counterexample | `compiler_boundaries.py`, boundary tests | Marker SWAP preserves state but corrupts decoder |
| Correct and corrupted gradients are `(2,0,0)` and `(0,sqrt(2),0)` | Exact Hopf derivative and output distributions | same | Observable `-Z tensor I`, all angles `pi/4` |
| Checkpoint active-interface equality preserves all designated estimator means | Algebraic adjoint/interface theorem | `COMPILER_BOUNDARIES.md`, exact positive example | Full distribution need not agree |
| Checkpoint state-column equality is insufficient | Explicit two-qubit counterexample | boundary tests | Final state remains `|++>` while derivative flips `2` to `-2` |
| Active-interface equality need not preserve checkpoint distributions | Explicit positive example | boundary tests | Same mean, total-variation distance `1/4` |

## Hopf-frame identities

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Recursive and addressed real Hopf frames coincide | Algebraic construction plus exact checks | `frames.py`, `test_frames.py` | Checked through `n=7`; formula general |
| Real frame is orthogonal and separated complex frame unitary | Algebraic construction plus exact checks | frame tests | Numerical checks supplement proof |
| Conditioned-prefix identity | Proved and first-audit verified | `ancilla_depth.py`, `PROOF_AUDIT_ISSUE_1.md` | Every cut through `n=8` checked |
| Prefix frame is a unary network of disjoint Givens layers | Proved and tested | `ancilla_depth.py`, tests | Dense unary checks through `t=3` |
| Tail below cut `t` is `direct_sum_r W_(n-t)^(r)` | Proved and second-audit verified | `optimal_parallel.py`, `OPTIMALITY_AUDIT_ISSUE_9.md` | Every cut through `n=8` checked |
| Global-to-local subtree angle map is exact | Algebraic breadth-first index map | subtree partition tests | Checked through `n=12` |

## Routed optimal positive-workspace compiler

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Router is a coherent basis permutation on arbitrary prefix--suffix entanglement | Proved and internally audited | dense route tests | Small Hilbert spaces checked exhaustively |
| Forward and inverse routing clean every auxiliary register | Proved and tested | route--subframe--unroute leakage tests | Exact logical model |
| Fredkin count per level is `2**ell*(s+1)` | Exact combinatorial count | `optimal_audit.py`, tests | One count includes data and token lanes |
| Exact copied-control count is `(B-1)(s+1)-t` | Proved and tested | independent audit ledger | Candidate's looser upper bound remains valid |
| Concurrent fanout depth is `O(t+log(s+1))` | CNOT-tree proof using coherent copy/use/uncopy | audit document and tests | Prefix bits use disjoint copy pools |
| Copy pool can be reused for all branch flags | Exact inequality and clean uncopy proof | audit ledger | Flags required only for `s>1` |
| Complete routed cut fits in `2B(s+1)` clean ancillas | Internally audited register ledger | `router_audit_row`, tests | Conservative envelope, not exact minimum |
| One controlled subtree frame has size `O(2**s)` | UCG geometric size sum | `optimal_parallel.py`, audit | Imported exact UCG/MCT synthesis |
| One controlled subtree frame has depth `O(s**2+2**s/s)` | Width-by-width summation | audit document | All width shifts included |
| All `B` controlled subtree frames run in parallel | Disjoint data/token/flag registers | routed construction | All-to-all logical circuit |
| Routed construction has total size `O(N)` | Prefix, routing, and `B*O(2**s)` summation | size ledger and audit | Constants not optimized |
| For `m>=4n`, maximal feasible cut yields optimal depth | Proved with `m<4Bs` and polynomial-term absorption | audit inequalities and tests | `s=1` handled separately |
| For `1<=m<4n`, frozen compiler is already optimal order | Proved with `n**3<=4*2**n` | explicit constant-20 audit test | Small `n` included |
| Real frame has upper bound `O(n+N/(n+m))` for every `m>=1` | Internally audited theorem | PR #8 construction plus PR #10 audit | External review pending |
| Real frame has size `O(N)` for every `m>=1` | Internally audited theorem | same | External review pending |

## Lower bounds and optimality

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Real Hopf state family has dimension `N-1` | Standard real-sphere dimension | audit helper | Includes an open chart subset |
| Any exact universal real-state preparation family needs `Omega(N)` parameterized gates | Parameter-count argument | audit document | Standard finite-layout circuit model |
| Depth is `Omega(N/(n+m))` | Gate-slot count on `n+m` wires | integer audit helper | Constant parameter dimension per gate |
| Backward system-output light cone contains fewer than `4n2**D` continuous parameters | Internally audited light-cone count | audit helper and tests | Arbitrary one-qubit plus CNOT model |
| Depth is `Omega(n)` | `4n2**D >= N-1` | audit proof | Asymptotic statement; small cases absorbed |
| Positive-workspace real frame has `Theta(N)` size and `Theta(n+N/(n+m))` depth | Upper and lower bounds combined | `OPTIMALITY_AUDIT_ISSUE_9.md` | `m>=1`; external review pending |
| Generic all-column CQSP would have `O(N**2)` size | Theorem 1 with `k=n`, inferred | `generic_all_column_cqsp_size_proxy` | Does not exploit Hopf tree structure |

## Complex frame and diagonal compilation

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| Separated frame is `W_C=D_ph W_R` and contains phase-dressed magnitude tangents | Algebraic derivative identity | complex analysis tests | Exact separated construction |
| Exact arbitrary diagonal has size `O(N)` and depth `O(n+N/(n+m))` | Audited piecewise use of exact synthesis results | `complex_resources.py`, complex ledger | Clean all-budget logical model |
| Diagonal and real frame reuse one workspace pool | Clean sequential-composition theorem | common-workspace document | Both blocks return workspace to zero |
| Positive-workspace complex frame has `O(N)` size and optimal depth | Internally audited corollary | optimal audit plus diagonal audit | `m>=1`; lower bound inherited from real subfamily |
| Common phase is a gauge and exact phase gradient is zero-sum | Algebraic proof and exact checks | `complex_analysis.py` | Hermitian expectation objectives |
| Zero-amplitude leaves have zero phase derivative and gradient | Direct formula and singular tests | complex analysis tests | No amplitude division |
| Strict zero-ancilla complex fallback has depth `O(N)` and size `O(nN)` | Full-width zero-angle UCG construction | complex resource tests | Sharp `O(N)` size unresolved |

## End-to-end work

| Statement | Status and evidence | Implementation/tests | Boundary |
|---|---|---|---|
| UCG/subtree parameter generation costs `O(Nn)` | Summed layer transforms | optimality audit | Arithmetic model |
| Diagonal phase parameters cost `O(Nn)` | One length-`N` FWHT | exact reconstruction tests | Arithmetic model |
| Record-wise magnitude decoder costs `O(SN)` | Direct character accumulation | decoder tests | Explicit full gradient output |
| Direct phase decoder costs `O(S+N)` | Signed-bin accumulation | decoder tests | Output array length `N` |
| Magnitude stream uses one inverse complex frame | Protocol factorization | common-workspace document | Controlled-observable cost separate |
| Direct phase stream uses no inverse frame | Protocol factorization | same | Forward preparation still required |

## Open problems and nonclaims

| Statement | Status | Current evidence |
|---|---|---|
| Strict `m=0` achieves both `O(N)` size and `O(n+N/n)` depth | Open | One-ancilla sharp compiler and zero-ancilla larger compiler known |
| One clean flag is provably necessary for the sharp endpoint | Open | No separation proof |
| General coherent-differential-frame theorem for arbitrary charts | Not claimed | Present geometry, marker map, and direct sum are Hopf-specific |
| Routed-device or noisy implementation is optimal | Not claimed | Logical all-to-all theorem only |
| Approximate Clifford+T version has the same bias/error profile | Not claimed | Requires a separate approximation analysis |
| Active-interface compilation preserves full checkpoint distributions | False in general | Explicit TV-distance counterexample |

## Reproduction

```bash
python -m pip install -r requirements.txt
python validate.py
python scripts/ancilla_depth_ledger.py --n 10
python scripts/complex_workspace_ledger.py --n 10
python scripts/optimality_ledger.py --n 12
python scripts/check_upstream_sync.py --offline
```

GitHub Actions runs the deterministic suite on Python 3.11 and 3.13.
