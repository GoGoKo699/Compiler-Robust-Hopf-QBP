# Checkpoint 31: global constant-clean construction search

> Preserved technical appendix. Read the [current endpoint brief](../CONSTANT_CLEAN_ENDPOINT.md) for the governing model, remaining gap, and resume task. [Provenance](PROVENANCE.md) records the source and editorial scope.
> Historical finite-check summaries and scratch reproduction commands are omitted; the complete mathematical argument and its scope are retained.

This independent search has not produced an improved complete frame compiler. It did identify a general obstruction to batching the dirty involution interpreter into one global XOR echo, and independently verified the new arbitrary-source attenuation-channel argument. Both are scoped interface results, not global frame lower bounds.

## 1. Why a global XOR-loaded program echo does not implement arbitrary rotations

The earlier borrowed compiler loads and consumes one involution instruction at a time. A natural attempt to save its factor of the program length is to load the entire program into a wide dirty bank, run one interpreter, undo the lookup, and apply the interpreter inverse. The lookup could be cheap because its classical data insertion is Clifford; the issue is its algebraic action on an unknown program.

Let the dirty bank label be $`z\in\mathbb F_2^m`$, and let the data word to be inserted be $`f`$. Let $`D_z`$ be an arbitrary unitary interpreter on a logical register and any source/private registers. The two-query XOR echo has branch operator

```math
E_f(z)=D_{z\oplus f}D_z^\dagger.
```

The opposite chronological convention gives $`D_z^\dagger D_{z\oplus f}`$ and the same argument. This description applies to an addressed multiplexor after fixing an address preserved by the interpreter. It does not assume that a lookup can be uncomputed across an operation that changes its address.

**Exact obstruction.** Suppose $`E_f(z)`$ implements the same logical unitary $`U_f`$ for every dirty $`z`$, with every supplied source returned exactly. Then $`U_f`$ is an involution. Any two masks whose promises use the same interpreter and returned-source subspace must also induce commuting logical unitaries:

```math
U_f^2=I,\qquad U_fU_g=U_gU_f.
```

Indeed,

```math
E_f(z\oplus f)=E_f(z)^\dagger,
```

and the source-return promise permits passing this inverse relation to the logical action. The branch operators also obey

```math
E_f(z\oplus g)E_g(z)=D_{z\oplus f\oplus g}D_z^\dagger
=E_g(z\oplus f)E_f(z),
```

which induces commutation. No promise for the additional mask $`f\oplus g`$ is needed. Neither the source dimension nor its precision changes these exact relations.

**Robust obstruction.** Let $`J`$ embed the logical input with the actual fixed prepared source and other initialized work. Suppose uniformly in $`z`$,

```math
\|E_f(z)J-JU_f\|\le\eta.
```

Unitarity also gives $`\|E_f(z)^\dagger J-JU_f^\dagger\|\le\eta`$. Applying the promise at $`z\oplus f`$ therefore proves

```math
\boxed{\|U_f-U_f^\dagger\|\le2\eta.}
```

In the project's convention,

```math
R_y(\theta)=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix},
```

this requires

```math
\boxed{\eta\ge |\sin\theta|.}
```

A nontrivial accurate generic rotation cannot be supplied by this single global echo. For example, the exact rational rotation with cosine $`3/5`$ and sine $`4/5`$ requires error at least $`4/5`$ under this interface. By contrast, choosing $`D_z=R^z`$ for one Hermitian involution $`R`$ gives $`E_f(z)=R^f`$ exactly, recovering the valid old instruction-level mechanism.

For two masks satisfying their promises on the same embedded subspace $`J`$, each side of the displayed branch-product identity approximates its logical product with error at most $`2\eta`$. Hence

```math
\boxed{\|U_fU_g-U_gU_f\|\le4\eta.}
```

Again, no promise for $`f\oplus g`$ is required. These estimates concern complete output, including return of the same actual source, rather than an averaged dirty state.

This rules out one concrete way to amortize all program-bit interpretations. It does not rule out longer echo sequences, a data-dependent non-Boolean group action, a global nonunitary block followed by amplification, or the dirty Weyl route. In particular the cyclic addition in the Weyl identity is not interchangeable with a Boolean XOR table loader.

## 2. Independently checked source-channel obstruction

The root agent proposed an attenuation proof that removes the checkpoint-30 arithmetic restriction on the prepared source. The independent source reviewer and I obtained the same constants and argument.

Let a source have $`s`$ qubits, Hilbert dimension $`d=2^s`$, and Pauli-space dimension $`D=d^2=4^s`$. Form the accepted, trace-nonincreasing completely positive source map $`\Phi`$, after fixing ordinary pure-stabilizer initialized inputs, taking dirty inputs maximally mixed, and tracing non-source outputs. Set

```math
r=\tau+2f,
```

where $`\tau`$ counts processing T gates and $`f`$ counts all computationally projected private flags. In normalized Pauli coordinates, $`\Phi`$ has entries in $`(\sqrt2)^{-r}\mathbb Z[\sqrt2]`$. The Galois conjugate map is also physical under the native gate conventions. Its source state need not be conjugated: $`\Phi`$ is defined independently of that input state.

If an arbitrary density $`\rho`$ is returned with attenuation $`2^{-k}`$, its accepted source density satisfies

```math
\Phi(\rho)=4^{-k}\rho.
```

Thus $`(\sqrt2)^{r-4k}`$ is an eigenvalue of the algebraic-integer matrix $`(\sqrt2)^r\Phi`$. If $`r<4k`$, that eigenvalue is not an algebraic integer, a contradiction. Consequently exact attenuation-return requires $`r\ge4k`$, with **no arithmetic premise on $`\rho`$** and even if the source changes with precision.

For the approximate statement assume $`r<4k`$, and write $`B=\Phi-4^{-k}I`$, $`H=\sqrt d+1`$. The preceding integrality argument makes $`B`$ invertible. Its determinant has a nonzero algebraic norm, while both $`\Phi`$ and its conjugate have Hilbert–Schmidt induced norm at most $`\sqrt d`$. Hence

```math
\sigma_{\min}(B)\ge
\frac{2^{-4kD}}{H^{2D-1}},\qquad
\|B\rho\|_2\ge
\frac{2^{-4kD}}{\sqrt d\,H^{2D-1}}.
```

If the complete accepted vector on a purification has error $`\epsilon`$ from its target vector of norm $`\lambda=2^{-k}`$, tracing it gives the upper estimate

```math
\|B\rho\|_2\le(2\lambda+\epsilon)\epsilon.
```

For $`\epsilon=2^{-L}`$ and $`k\le L`$, a necessary condition under $`r<4k`$ is therefore

```math
L\le(4D-1)k+c_D,\qquad
c_D=\log_2\!\left(3\sqrt d\,H^{2D-1}\right).
```

Choosing $`k=\lfloor L/(8D)\rfloor`$, with $`L\ge8D`$ and $`L>2c_D`$, forces $`r\ge4k`$. A fixed-width source and a fixed number of projected flags therefore cannot furnish every required dyadic attenuation using sublinear-in-$`L`$ processing cost, even when the source is precision-dependent or transcendental.

The factor $`4^s`$ is an explicit bound from the source superoperator dimension. No optimal dependence on growing $`s`$ is asserted. This is also not additive across stages: one whole $`O(L)`$-T operation remains compatible with the desired endpoint.

## 3. What remains constructively plausible

The failed routes above narrow, but do not settle, the global construction problem. A candidate that applies only one global coefficient operation at cost $`O(L)`$ need not implement cheap standalone attenuation for every exponent. Nor must it reduce to a two-query XOR echo.

The most concrete distinction from the old compiler is now algebraic: its Boolean program insertion supports involution differences, while arbitrary rotation coefficients require a different action or a genuinely global block. A cyclic-group action would support nontrivial characters, but its clock and addition lookup have the separately identified missing costs. A nonunitary global block could also avoid the exact involution argument, but it must retain the full accepted-source error and prove how a constant amount of initialized work suffices for its final amplification.

I did not establish either of those missing implementations. The available $`O(N^{3/2})`$ upper bound at fixed clean width and $`L=N,b=\Theta(N)`$ must therefore remain unchanged on the basis of this note. The two interface obstructions above are the supported research output, rather than an uncharged proposed compiler.
