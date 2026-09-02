# Output-sensitive decoding

## 1. Two exact decoding strategies

Let `N=2**n`, and let `S` global-frame outcomes be

```math
(b_s,y_s),
\qquad
b_s\in\{0,1\},
\quad
y_s\in\{0,1\}^n.
```

The Walsh moment indexed by `k` is estimated by

```math
\widehat\mu_k
=\frac{1}{S}\sum_{s=1}^{S}
(-1)^{b_s+k\cdot y_s}.
```

The magnitude gradient reads selected marker moments and multiplies them by the
known metric factors.

### Histogram plus FWHT

Construct the signed histogram

```math
h(y)=\frac{\#(0,y)-\#(1,y)}{S}
```

in `O(S)` time and apply a length-`N` fast Walsh--Hadamard transform. The cost is

```math
O(S+Nn)
```

with `O(N)` storage.

### Record-wise characters

For one measured `y`, generate the complete character vector

```math
\chi_y(k)=(-1)^{k\cdot y},
\qquad 0\leq k<N,
```

recursively. Starting from `chi_y(0)=1`, each binary bit of `y` either copies or
negates the existing half of the vector. This takes `O(N)` arithmetic and
`O(N)` storage per accumulated output array. Averaging all samples costs

```math
O(SN).
```

## 2. Combined complexity

Choose the smaller strategy:

```math
O\bigl(S+N\min(S,n)\bigr)
```

time and `O(N)` storage.

This distinction matters after circuit recompilation. A direct-angle Hopf
circuit may already cost `Theta(Nn)`, making the FWHT term harmless. An optimized
logical compiler can have `O(N)` size, in which case automatically charging
`O(Nn)` classical work would hide an avoidable factor.

At fixed simultaneous coordinatewise accuracy and confidence, the global Hopf
record requires

```math
S=O(\log n)=O(\log\log M)
```

executions for `M=Theta(N)` coordinates. The record-wise decoder then costs

```math
O(N\log n),
```

which is linear in the output length up to the statistical repetition factor.

## 3. Exact implementation

The repository implements:

```text
walsh_character_from_outcome
global_moments_recordwise
decode_balanced_magnitude_samples_recordwise
```

in `compiler_robust_hopf/decoders.py`.

The tests compare:

1. direct parity evaluation;
2. histogram plus FWHT;
3. record-wise accumulation;
4. the final metric-weighted gradient decoder.

The comparisons cover deterministic random samples for `n=1,...,6` at tolerance
`1e-12`.

## 4. Output lower bound

The complete real gradient contains `N-1` numbers and the complete complex chart
contains `2N-1` coordinates before removal of the common phase gauge. Any
explicit classical output therefore requires `Omega(N)` storage or streaming
work. The record-wise decoder is output-sensitive; it is not an exponential
compression of an exponentially long classical vector.

## 5. Boundaries

This accounting does not include:

- parameter-generation time for the quantum compiler;
- communication latency from a device;
- sparse or compressed gradient output conventions;
- approximate/sketched Walsh decoding;
- optimizer update cost.

Those resources should be reported separately if they become relevant to the
paper's end-to-end claim.
