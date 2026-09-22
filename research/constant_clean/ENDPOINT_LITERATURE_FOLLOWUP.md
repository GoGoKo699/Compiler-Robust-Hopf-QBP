# Literature follow-up for the constant-clean endpoint

Working research note, 22 September 2026, after integration commit
`b935b34`. This bounded primary-source review changes no established theorem.
The target remains the [endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md):
the prescribed complete real frame, constant initialized workspace,
$`b=\Theta(N)`$ arbitrary dirty work, $`L=N`$, and a literal complete-output
isometry guarantee. At that checkpoint, the lower benchmark was $`\Omega(N)`$
and the available upper benchmark was $`O(N^{3/2})`$. The later
[operator-source compiler](OPERATOR_SOURCE_COMPILER.md) gives $`T=O(N+nL)`$
with $`a=2`$ and $`b\ge L+n+7`$. Thus the current upper bound is
$`O(N\log N)`$ at $`L=N`$ and $`b\ge N+n+7`$, while the lower bound
remains $`\Omega(N)`$.

**No theorem examined below supplies a constant-clean $`O(N)`$ endpoint compiler.**
This is a statement about these inspected results, not an exhaustive novelty
claim. Several recent papers supply useful building blocks, but their clean
instruction registers, prepared catalysts, or accuracy contracts remain
substantive hypotheses.

## 1. The closest instruction-synthesis results

**Tan, _Unitary Synthesis with Fewer T Gates_.**
[Published paper](https://journals.aps.org/prxquantum/pdf/10.1103/pxhd-9s9q),
Theorem I.1, Definition I.2, Lemma IV.1, and Remark IV.2.
With $`\Lambda=n+\log_2(1/\epsilon)`$, the general-unitary bound is

```math
T=O(N^{4/3}\Lambda^{2/3}+N\Lambda),
\qquad a=O(N^{2/3}\Lambda^{1/3}+\Lambda).
```

The definition is a full initialized-isometry bound, so its error contract
is relevant. The ancillas are initialized. Remark IV.2 explicitly prepares
a zero instruction register of length proportional to synthesis precision,
loads the Boolean descriptions, interprets them, and unloads. Lemma IV.1
shares Boolean computation across changing target wires; it does not remove
the initialized instruction output. At our endpoint its generic upper
certificate is $`O(N^2)`$ T gates with $`O(N)`$ clean work.

**Yamazaki–Akibue, _Multi-qubit controlled gate with optimal T-count_.**
[arXiv:2603.14202v1](https://arxiv.org/html/2603.14202v1), Theorems 1 and 4,
Sections 2.1–2.2 and 3.1, Lemma 7.
For S addressed SU(2) blocks, their aligned normal-form construction has
$`3\log_2(1/\epsilon)+O(\sqrt{S\log(1/\epsilon)})+o(\log(1/\epsilon))`$
T gates for the stated typical-target regime. Section 3 still requires
precision-length clean instructions; only the additional lookup work is
dirty. Theorem 4 removes ancillas at a cost of order
$`S\log(1/\epsilon)`$. Its probability qualification and phase-insensitive
diamond metric must also be retained. Lemma 7's arbitrary-input Boolean XOR
oracle and the word alignment are useful inputs, but do not establish the
required worst-case, literal, constant-clean frame result.

The existing GKW optimal diagonal compiler has the same relevant distinction:
its Section 2 proof loads a precision-length description into initialized
work before interpretation. See
[arXiv:2411.04790v3](https://arxiv.org/html/2411.04790v3), Theorem 1.2 and
its proof. Optimal state preparation alone still does not prescribe the frame.

## 2. Global blocks and Hamiltonian synthesis

**Yuan–Zhang–Zi, _Quantum Circuit for General Unitary: Improved T-count via
Block Flattening and Dilation_.**
[arXiv:2608.17846v1](https://arxiv.org/html/2608.17846v1), Definition II.1,
Theorem I.1, Lemma IV.2, Section V, and Appendix B.
The paper flattens block norms with Boolean phase oracles and Walsh transforms,
jointly compiles block dilations, then amplifies their common singular value.
Its complete clean-input isometry metric matches the relevant type of error
guarantee. For $`\Lambda\le N`$, the stated resources are

```math
T=O\!\left(nN^{5/4}\Lambda^{5/8}\right),
\qquad a=O(N\sqrt\Lambda).
```

For larger precision it invokes Tan's $`O(N\Lambda)`$ construction with
$`O(\Lambda)`$ clean work. Lemma IV.2 and the multiplexed extension retain
the clean compiler workspace; preparing and unpreparing block labels is also
part of the circuit. This is an important global-block precedent, but its
resource theorem cannot be specialized into our endpoint. In particular,
the precision-polynomial-in-n headline is not the regime $`L=N`$.

**Fang–Heunen–Wang, _Unitary Synthesis with Near-Optimal T-Count for
Near-Clifford Unitaries_.**
[arXiv:2607.12907v1](https://arxiv.org/html/2607.12907v1), Definition 1.1,
Lemma 3.6, and Theorem 3.7.
The residual-Hamiltonian decomposition controls its normalization by the
Frobenius norm, but the explicit synthesis theorem sets
$`k=\max\{\|H\|_F,1\}`$. When $`k=1`$, its displayed bound is
$`O(N(n+L)^2)`$ T gates and $`O(N(n+L))`$ initialized ancillas, up to the
displayed lower-order logarithmic term. Making a coarse residual smaller
does not reduce this theorem's floor. Moreover, its main contract traces out
an initialized environment and controls diamond distance; literal phase and
complete workspace return need separate treatment. The Hamiltonian
decomposition is a candidate ingredient, not an endpoint compiler.

**Ma–Joven–Liu, _Optimal T-Count for Block Encodings of Fermionic and Spin
Hamiltonians_.**
[arXiv:2609.11153v1](https://arxiv.org/html/2609.11153v1), Definition 2.1,
Theorem 3.1, and Appendix D.
Their compression theorem replaces a block encoding with one satisfying

```math
a'\le\min\{a,n+2t\},\qquad T'\le t,
\qquad \alpha'=2^{-\kappa/2}\alpha,
```

while retaining absolute block error. All retained ancillas remain clean,
and the normalization may change. For $`t=\Theta(N)`$, this offers
$`O(N)`$ clean work, not constant clean work. It neither converts initialized
ancillas into arbitrary borrowed wires nor by itself preserves a specified
complete-output unitary implementation. A stronger structural compression
lemma for the particular frame block would be new work.

## 3. QROM and reusable phase resources

**_Halving the cost of QROM_.**
[arXiv:2605.20334v1](https://arxiv.org/html/2605.20334v1), Section II.1,
Equation (1), and Appendix A Theorem 1.
The theorem loads an m-bit Boolean output by XOR. In addition to
$`\mu(\lambda-1)`$ dirty ancillas, it specifies
$`\max\{\lceil\log_2(N/\lambda)\rceil,\log_2\lambda\}`$ clean selectors
and m clean output wires. Its improvement concerns the existing lookup
structure and constants. It supplies neither a modular translation
$`|x,z\rangle\mapsto|x,z+f(x)\bmod2^m\rangle`$ nor a constant-clean
interpreter for a complete noncommuting gate word. Measurement-based
uncomputation is a separate option in Section II.2.

**Kim, _Catalytic z-rotations in constant T-depth_.**
[arXiv:2506.15147v1](https://arxiv.org/html/2506.15147v1), Equation (1),
Sections 2.2–2.4. Its primitive-polynomial Clifford has high odd period,
and a prepared eigenstate supplies the phase. Fixed-angle catalysts occupy
$`O(p)`$ qubits for p-bit resolution; the variable-angle construction uses
$`3p^2`$ qubits up to its stated index shift. Constant T-depth is not constant
T-count, and offline preparation is a charged nonstabilizer resource here.
The result does not replace the initialized source by arbitrary dirty input.

**Xu–Wang, _Cultivating logical catalysts for fault-tolerant dyadic phase
rotations_.**
[arXiv:2606.27358v1](https://arxiv.org/html/2606.27358v1), Section II.1,
Equation (5), and Section II.3. Exact phase kickback uses a special Clifford
eigenstate; their direct construction for $`Z^{2^{-p}}`$ has
$`2^p+1`$ catalyst qubits. Cultivation uses measurements and postselection.
The online resource claim excludes its preparation and does not match our
coherent, constant-clean model.

**_Multi-Qubit Dyadic Phase Fixing for Fault-Tolerant Quantum Compilation_.**
[arXiv:2606.05397v1](https://arxiv.org/html/2606.05397v1), Sections III.B–D.
Its shared p-bit phase-gradient state and adder use $`2p-2`$ auxiliary
qubits in the analyzed implementation. Preparation is amortized over
rotations, with synthesis error explicitly budgeted. This may help practical
circuits, but the prepared gradient still grows with precision; dirty wires
are not a substitute under its contract.

## 4. Concrete next proof obligations

The following are proposed research inputs, not consequences of the cited
theorems.

1. **A dirty-compatible batch interpreter for aligned words.** Start from
   Tan's shared Boolean factors or Yamazaki–Akibue's aligned normal form.
   Aim to replace the initialized precision-length output by a circuit with
   constant clean work and total cost
   $`O(\sqrt{SL}+L+SL/K)`$. Prove its action on every dirty input before
   optimizing the loader. Completing one involution echo at a time is valid
   but retains the known repeated-precision cost. A new multi-query identity
   could lie outside the retained two-query XOR obstruction.
2. **A jointly compiled full-frame block with a complete workspace ledger.**
   Yuan–Zhang–Zi provides the closest global-block architecture. To help here,
   a specialized frame dilation must charge block-label preparation, selected
   coefficients, instruction work, and the final reflection with only a
   constant initialized register. Generic flattening plus the published
   clean SELECT compiler does not satisfy that obligation.
3. **Structural compression, not the generic compression bound.** Inspect
   the actual Clifford/Pauli representation of a proposed whole-frame block
   for a special constant-dimensional initialized subsystem. The recent
   compression theorem identifies a useful proof framework, but its
   $`n+2t`$ bound alone is insufficient. The literal accepted normalization
   and full-output error must survive any stronger reduction.

The modular-clock route remains a separate possible attack. None of the
QROM or catalyst theorems inspected here supplies its missing coherent,
constant-clean, carry-aware table translation together with a charged joint
clock. A source-interface obstruction should not be extended to these new
architectures without first proving that they expose that interface.
