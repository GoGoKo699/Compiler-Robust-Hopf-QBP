# Joint dirty clocks: a robust rank bound for one-addition kickback

Research follow-up to [DIRTY_CLOCK.md](DIRTY_CLOCK.md), after repository revision
`b935b34`. The [endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md) governs the model.
No improved unrestricted joint-clock or complete-frame compiler is claimed.

The new result is an architecture bound: a standard joint phase-kickback clock
with **one controlled modular addition** requires at least as many initialized
work qubits as clock bits, even with arbitrary work encoding and uniform error
below one. Arbitrarily many dirty work qubits do not replace this initialization.
The proof does not sum separate rotation costs or assume a supplied source is
exactly returned. It permits approximate complete work return.

## 1. The complete one-addition interface

Let $`q=2^m`$, $`\zeta=e^{2\pi i/q}`$, and

```math
Z_m|y\rangle=\zeta^y|y\rangle,
\qquad X_m|z\rangle=|z+1\bmod q\rangle.
```

The work register has $`s`$ initialized qubits and $`b`$ arbitrary dirty qubits.
Write $`d=s+b\ge m`$ and $`D=2^b`$. The initialization isometry
$`J_{\mathrm{in}}:\mathbb C^D\to\mathbb C^{2^d}`$ appends the initialized work.
Let $`J_{\mathrm{out}}`$ be the desired returned-work isometry. Ordinary clean
and dirty return sets $`J_{\mathrm{out}}=J_{\mathrm{in}}`$.

Allow **arbitrary work-only unitaries** $`E,F`$, independent of the clock input
$`y`$. They need not be inverses, need not be Clifford+T, and may depend on the
desired precision. Granting this freedom strengthens the obstruction. Put

```math
U=X_m\otimes I_{2^{d-m}},\qquad
V=(I\otimes F)
   \left(\sum_{y=0}^{q-1}|y\rangle\!\langle y|\otimes U^y\right)
   (I\otimes E).
```

All source preparation, encoding, decoding and their workspace must fit in the
stated work register. The approximation promise is the full isometry bound

```math
\left\|V(I\otimes J_{\mathrm{in}})
 -c\,(Z_m\otimes J_{\mathrm{out}})\right\|_{\mathrm{op}}
 \le\eta,\qquad |c|=1.
```

This permits a common scalar phase, and therefore also covers the stricter
literal-phase promise. It is uniform over every clock and dirty input. Tensoring
an untouched reference leaves the norm unchanged; no maximally mixed marginal
or traced-work condition substitutes for this promise.

**Theorem.** In this architecture, $`\eta<1`$ implies

```math
\boxed{s\ge m.}
```

The bound is independent of T count and precision. In particular, for
$`m=\Theta(L)`$ it excludes a constant-clean implementation by this route even
before charging gates.

## 2. Proof by a Fourier coefficient of full rank

Restricting to each computational clock input gives

```math
\|F U^y E J_{\mathrm{in}}
    -c\zeta^yJ_{\mathrm{out}}\|\le\eta
\qquad(0\le y<q).
```

The character average

```math
\Pi=\frac1q\sum_{y=0}^{q-1}\zeta^{-y}U^y
```

is the orthogonal projector onto the $`\zeta`$ eigenspace of $`U`$. One cyclic
increment has each $`q`$th root as a simple eigenvalue. Its spectator factor gives

```math
\mathrm{rank}\Pi=2^{d-m}.
```

Average the branch errors with the same character. The triangle inequality
gives

```math
\|F\Pi E J_{\mathrm{in}}-cJ_{\mathrm{out}}\|\le\eta.
```

If $`s<m`$, then $`2^{d-m}<2^b=D`$, so $`F\Pi E J_{\mathrm{in}}`$ has a nonzero
kernel. For a unit vector $`v`$ in that kernel,

```math
\|(F\Pi E J_{\mathrm{in}}-cJ_{\mathrm{out}})v\|
=\|cJ_{\mathrm{out}}v\|=1,
```

contradicting $`\eta<1`$. Therefore $`s\ge m`$. This is a dimension argument
about the complete dirty-input space: the factor $`2^b`$ is essential and cancels
from the final inequality.

The Fourier average is a mathematical proof device, not an additional physical
operation. The argument works for distinct input and output isometries and
distinct encoder and decoder. No arithmetic-field assumption on their entries,
or on an encoded independent source, is used.

More generally, for any unitary representation $`R(y)`$ of the cyclic group and
one-dimensional character $`\chi(y)`$, define

```math
\Pi_\chi=\frac1q\sum_y\overline{\chi(y)}R(y).
```

A single-use wrapper $`F R(y)E`$ that approximates
$`c\chi(y)J_{\mathrm{out}}`$ uniformly within $`\eta<1`$ must satisfy
$`\mathrm{rank}\Pi_\chi\ge D`$. The clock result is the character-multiplicity
specialization for the regular cyclic shift.

## 3. What this does and does not rule out

The theorem covers preparing one Fourier source, using one addition to impart
the joint clock phase, and then undoing or otherwise decoding the source. It
also covers arbitrary target-independent attempts to encode that source into
the available clean and dirty work. Even unlimited processing gates in the
encoder and decoder cannot fix the missing character multiplicity.

Reusing one such encoded source across several ordinary additions does not
remove the width requirement: fix every other clock input to zero and retain
one variable input. With no extra operations interleaved with those additions,
the same single-use interface remains.

The theorem does **not** apply to a general circuit for $`Z_m`$. In particular it
does not cover multiple additions interleaved with other work operations,
encoding that depends on the clock input, or synthesis that processes the
logical clock register without this separated work interface. It also does
not bound a direct Weyl commutator implementation. No stronger unrestricted
T lower bound follows from the rank calculation.

The established unrestricted joint-clock lower benchmark is still linear in
$`\min\{m,L\}`$; the separately restored factor architecture has its stronger
quadratic bound for $`m=\Theta(L)`$. The present result is a different,
initialization-width obstruction for a joint architecture, not a proof that
all joint synthesis has quadratic T count.

## 4. Fully charged amortization when growing clean work is allowed

There is a useful distinction between the unresolved constant-clean target and
the standard growing-source baseline. Define the ideal Fourier source

```math
|\gamma_m\rangle=\frac1{\sqrt q}\sum_{z=0}^{q-1}\zeta^{-z}|z\rangle,
\qquad X_m^y|\gamma_m\rangle=\zeta^y|\gamma_m\rangle.
```

Suppose a native unitary preparation $`B`$ satisfies
$`\|B|0^m\rangle-|\gamma_m\rangle\|\le\delta`$, after choosing an irrelevant
common phase for the ideal source. That source phase cancels with the literal
inverse and does not relax the logical output-phase contract. Use exact reversible additions
for an entire sequence, retaining the same source, and apply the literal
$`B^\dagger`$ only at the end. If $`A`$ is the sequence of additions and $`Q`$ its
ideal logical phase operation, then

```math
A(|\psi\rangle|\gamma_m\rangle)
=(Q|\psi\rangle)|\gamma_m\rangle,
```

and the resulting complete-isometry error is at most $`2\delta`$. To see this,
replace the prepared source by the ideal source before $`A`$ and replace it
back after $`A`$; each replacement costs at most $`\delta`$ because $`A`$ is unitary.
This estimate is uniform in logical/reference input and **does not grow with
the number of exact additions**. It does not assert that the approximate
source is independently reset after each use.

A conservative deterministic preparation synthesizes the product of $`m`$
one-qubit phases to total state error $`\delta`$, costing
$`O(m\log(m/\delta))`$ T gates. The modular variant of the
[Cuccaro–Draper–Kutin–Moulton ripple-carry adder](https://arxiv.org/pdf/quant-ph/0410184),
Section 4.1, uses one further initialized bit and $`O(m)`$ Toffoli and Clifford
gates. Exact coherent Clifford+T decomposition gives $`O(m)`$ T gates. Taking
$`\delta=2^{-L-1}`$, $`r`$ clock uses, including source preparation and its literal
inverse, have the sufficient ledger

```math
T=O\bigl(m(L+\log m)+rm\bigr),\qquad
\text{initialized work}=m+O(1),\qquad \eta=2^{-L}.
```

The Clifford cost obeys the same conservative order. No measurements, resets,
or supplied magic states are needed for this baseline. Once
$`r\ge L+\log m`$, its average T cost per use is $`O(m)`$, but its initialized
width still grows with $`m`$. It therefore supplies no constant-clean endpoint
improvement.

## 5. Primary-source audit

- [Jones et al., *Simulating chemistry efficiently on fault-tolerant quantum
  computers*, arXiv:1204.0567](https://arxiv.org/pdf/1204.0567), Sections 2.1 and
  4.1, gives Fourier-state phase kickback and joint quantum-variable rotation.
  The linear online arithmetic acts on a prepared Fourier register. Its
  eigenstate/addition interface is the baseline above; it does not supply
  constant initialized width. The full-norm rank theorem here is a separate
  derivation about that interface, with no claim of novelty certification.
- [Gosset, Kothari and Wu, *Quantum State Preparation with Optimal T-Count*,
  arXiv:2411.04790v3](https://arxiv.org/html/2411.04790v3), Theorems 1.3 and 1.4,
  gives batching of $`O(\log L)`$ different one-qubit unitaries with $`O(L)`$ T
  gates and ancillas, and $`O(m+L)`$ T gates and ancillas for identical-unitary mass
  production. The dyadic clock has different rotations, and the cited
  constructions permit growing initialized workspace. These theorems do not
  resolve the present constant-clean clock.
- [Jones, *Distillation protocols for Fourier states in quantum computing*,
  arXiv:1303.3066](https://arxiv.org/pdf/1303.3066), gives a more efficient
  Fourier-source preparation route using growing width and postselected
  measurement/retry. It cannot be inserted unchanged into the deterministic
  coherent model.
- [Gidney and Fowler, arXiv:1812.01238v2](https://arxiv.org/html/1812.01238v2),
  Section 4, produces two angle-$`\theta`$ rotations using a catalyst, a Toffoli,
  **and a doubled-angle operation**. It does not provide an uncharged dyadic
  ladder from one small source.
- [Kalloor et al., *Multi-Qubit Dyadic Phase Fixing*, arXiv:2606.05397v1](https://arxiv.org/html/2606.05397v1),
  Section III-C, allocates a growing gradient register and adder scratch and
  includes gradient-state preparation rotations. Its resource improvements
  do not remove the clean-source reservation.

The search found no verified constant-clean $`O(m+L)`$ or $`o(mL)`$ joint-clock
construction, and no new unrestricted superlinear lower bound. The
one-addition route is now ruled out with a precise approximate-return contract;
other joint synthesis and direct-commutator routes remain open.

## 6. Finite exact check

Independent small checks used standard-library Fraction arithmetic in
$`\mathbb Q[x]/(x^{2^{m-1}}+1)`$ for $`m=1,\ldots,5`$. They verified the Fourier
sign, projector identities, rank-one minors, and an explicit deficient-rank
kernel witness with different encoding and decoding permutations. These
finite calculations check fragile conventions; the all-size theorem is proved
above. No large simulation or empirical extrapolation enters the result.

The repository's [structural regression suite](../../tests/test_constant_clean_structure.py)
also checks small full matrices for the cyclic projector, a deficient-work
kernel witness, and exact dirty return at the sufficient-width boundary:

```bash
python -m unittest tests.test_constant_clean_structure
```
