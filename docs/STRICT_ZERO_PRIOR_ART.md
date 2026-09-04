# Prior-art boundary for the strict-zero Hopf layer

[← Strict-zero construction](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) · [Related work](RELATED_WORK.md) · [Expanded source search →](PRIOR_ART_SEARCH_2026_09.md)

This page separates the project-specific strict-zero result from the familiar
circuit ideas used to obtain it. It is a technical prior-art analysis, not a
legal novelty opinion.

## 1. Construction being classified

At a nonfinal Hopf depth `d`, split the logical register as

```math
|p\rangle|x\rangle|b\rangle|r\rangle,
```

where `p` is the `d`-bit prefix, `x` the target, `b` one original suffix bit,
and `r` the remaining suffix.

Let

```math
h(r)=[r=0],
\qquad
C_p=R_y(\theta_p/2).
```

A four-toggle echo uses `b` as a restored in-place predicate carrier. The active
original-zero-suffix branch receives `C_p^2=R_y(theta_p)`, while the unwanted
original value of `b` receives the cancelling word `C_pXC_pX=I`.

Aggregating all prefix values into two total-width-`d+2` UCGs gives

```math
S(L_d)=O(2^d+n-d),
```

```math
D(L_d)=O\left(n+\frac{2^d}{d+2}\right),
```

and hence the optimal strict-zero complete-frame frontier after summing the
Hopf tree.

The classification question is whether this complete Hopf-specific feature
bundle appears in earlier work, not whether its individual ingredients have
precedents.

## 2. Established ingredients

### Controlled-unitary roots and conjugation

Exact controlled-unitary constructions have long used roots of target
unitaries together with Pauli conjugation. Barenco and coauthors are the natural
reference for this lineage.

The identities

```math
C^2=U,
\qquad
JCJ=C^{-1}
```

are therefore not treated as new.

### Multiplexed rotations and UCGs

Möttönen and coauthors introduced the uniformly controlled rotation form used in
state preparation. Bergholm and coauthors developed general uniformly
controlled one-qubit gates.

The present circuit uses those UCG primitives. It does not claim a new
multiplexor synthesis theorem.

### Borrowed and conditionally clean logical qubits

Borrowing a qubit in an unknown state, using it coherently, and restoring it has
an established history. Recent work by Claudon and coauthors and by Khattar and
Gidney gives particularly close context for borrowed and conditionally clean
workspace.

The present suffix bit is logical data rather than an allocated ancilla. Its
restoration requirement is still part of this broader lineage.

### Toggle-detection cancellation

Toggle-detection methods replace a clean control with an unknown-state bit by
applying and unapplying a predicate so that unwanted branches cancel. That
pattern is also established.

The Hopf target rotation is generally not self-inverse, so a half-angle root and
Pauli conjugation are used to create the required cancellation. This is a
specialization of familiar ingredients rather than a claim to have invented
toggle detection.

### Ancilla-free multi-controlled rotations

Efficient exact multi-controlled `SU(2)` gates without ancillas are also known.
Such constructions could implement one prefix-conditioned rotation at a time.
The present size–depth result instead depends on aggregating all `2^d` prefix
values into two UCGs and paying the long suffix predicate only a constant number
of times per depth.

### Restricted and sparse UCGs

Recent restricted-UCG work studies repeated blocks and partial control
participation. The addressed Hopf layer belongs to the same broad structural
setting.

A direct full-width Möttönen transform of the logical zero-suffix table is
generically dense in the physical angle domain. The borrowed-suffix factorization
avoids that transform by reducing the physical UCG width to `d+2`.

## 3. State-preparation compiler line

The all-workspace framework of P. Yuan and S. Zhang supplies:

- exact ancilla-free multi-controlled `X`;
- the UCG size–depth tradeoff;
- coherent copy–use–uncopy;
- the optimal QSP comparison frontier.

The earlier state-preparation paper remains the historical predecessor and
original-source reference for selected primitives. The two papers are treated
as one coherent compiler line.

The present proof adapts those primitives after the complete Hopf layer is
exposed. It does not infer complete-frame correctness from first-column state
preparation.

## 4. Feature comparison

| Feature | Established in prior work? | Role here |
|---|---:|---|
| roots of target unitaries | yes | split `R_y(theta_p)` into two half-angle factors |
| Pauli conjugation to invert a root | yes | make the unwanted branch cancel |
| borrowed or conditionally clean logical qubits | yes | allow one suffix bit to carry the predicate temporarily |
| toggle-detection cancellation | yes | erase the effect of the unknown original bit |
| uniformly controlled one-qubit gates | yes | aggregate every prefix-dependent half-angle rotation |
| ancilla-free multi-controlled `X` | yes | implement the remaining all-zero suffix toggle |
| Hopf addressed zero-suffix layer | project-specific target | fixes the complete state-and-marker frame |
| two width-`d+2` UCGs for all prefix values | project-specific reduction | keeps cost at `O(2^d)` rather than full width |
| optimal strict-zero complete-frame theorem | project-specific consequence | gives `Theta(2^n)` size and `Theta(n+2^n/n)` depth |

## 5. Claim-safe contribution

A precise positive statement is:

> For one addressed Hopf depth, an original suffix data qubit can serve as a
> restored in-place predicate carrier. A four-toggle half-angle echo reduces all
> prefix-dependent rotations to two total-width-`d+2` UCGs and linear predicate
> toggles. Summing the addressed layers yields an exact ancilla-free complete-
> frame compiler at the optimal state-preparation frontier.

This wording identifies:

- the operator being compiled;
- the local reduction;
- the aggregate resource consequence;
- the complete-frame rather than state-column contract.

## 6. Claims that should not be used

The following claims should not be used:

- first use of borrowed or dirty qubits;
- first use of conditionally clean ancillas;
- first toggle-detection construction;
- first controlled-unitary square-root echo;
- first UCG or multiplexed rotation synthesis;
- first ancilla-free multi-controlled `SU(2)` circuit;
- proof that no equivalent circuit exists in earlier literature;
- legal determination of novelty or priority.

The mathematical theorem does not depend on any of those broader claims.

## 7. Bounded search result

The expanded search record did not locate the same complete feature bundle:

1. one original suffix data bit whose original value belongs to the predicate;
2. half-angle/Pauli cancellation of the unwanted branch;
3. two UCGs aggregating every prefix value at one Hopf depth;
4. exact restoration on the complete Hilbert space;
5. the resulting optimal strict-zero complete-frame frontier.

That is a negative result of a bounded technical search, not proof of novelty.
Equivalent constructions may use different terminology or appear in theses,
patents, software, or unpublished notes.

The detailed record is in
[Expanded prior-art search](PRIOR_ART_SEARCH_2026_09.md) and
[`provenance/prior_art_search.json`](../provenance/prior_art_search.json).

## 8. Assessment boundary

The appropriate final assessment is narrow:

- the component techniques are established;
- the Hopf-specific aggregation and resource theorem are the project-specific
  contribution under review;
- broader novelty or priority remains open to independent specialist checking.

---

[← Strict-zero construction](STRICT_ZERO_BORROWED_SUFFIX_ECHO.md) · [Related work](RELATED_WORK.md) · [Expanded source search →](PRIOR_ART_SEARCH_2026_09.md)
