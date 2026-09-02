# Output-sensitive decoding

## 1. Global magnitude record

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
negates the existing half of the vector. This takes `O(N)` arithmetic. Averaging
all samples costs

```math
O(SN)
```

with one `O(N)` accumulated output array.

### Combined magnitude complexity

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

## 2. Direct complex phase record

One direct phase-stream outcome consists of an ancilla bit `b` and a measured
leaf `ell`. It contributes

```math
Z^{\mathrm{ph}}
=
2(-1)^b e_\ell.
```

The record has deterministic Euclidean norm two. Accumulate the signed samples
in `N` bins and divide by `S_ph`. The total cost is

```math
O(S_{\mathrm{ph}}+N)
```

and the storage is `O(N)`.

No Walsh transform is needed, and the phase stream applies no inverse
differential frame. A projection onto the exact zero-sum phase-gradient
subspace may be performed in an additional `O(N)` pass.

## 3. Diagonal compiler parameter generation

For the complex magnitude frame, the leaf phases must also be converted into the
parity-phase coefficients used by a Gray/Walsh diagonal compiler. After removing
the common phase,

```math
f(x)=\phi_x-\phi_0,
```

and

```math
f(x)
=
\sum_{s\neq0}\alpha_s
\bigl(\langle s,x\rangle\bmod2\bigr),
```

where

```math
\alpha_s
=-\frac{2}{N}
\sum_xf(x)(-1)^{\langle s,x\rangle}
```

for `s!=0`. One fast Walsh--Hadamard transform computes every `alpha_s` in

```math
O(Nn)
```

arithmetic and `O(N)` storage. The inverse diagonal reuses the same parameters
with their signs reversed.

This parameter-generation work is separate from sample decoding and should be
charged once per parameter update, not once per shot.

## 4. Exact implementation

The repository implements the magnitude routines

```text
walsh_character_from_outcome
global_moments_recordwise
decode_balanced_magnitude_samples_recordwise
```

and the phase routines

```text
phase_record
decode_phase_gradient
decode_phase_samples
```

in `compiler_robust_hopf/decoders.py`.

The compiler phase transform

```text
diagonal_parity_angles
reconstruct_relative_phases
```

is in `compiler_robust_hopf/complex_analysis.py`.

The deterministic tests compare direct parity evaluation, histogram plus FWHT,
record-wise accumulation, signed phase-bin accumulation, and exact reconstruction
of arbitrary leaf phases.

## 5. Output lower bound

The complete real gradient contains `N-1` numbers and the complete complex chart
contains `2N-1` coordinates before removal of the common phase gauge. Any
explicit classical output therefore requires `Omega(N)` storage or streaming
work. These decoders are output-sensitive; they are not an exponential
compression of an exponentially long classical vector.

## 6. Boundaries

This accounting does not include:

- controlled-observable implementation cost;
- communication latency from a device;
- sparse or compressed gradient output conventions;
- approximate or sketched Walsh decoding;
- optimizer update cost;
- routed compiler-generation overhead beyond the stated arithmetic transform.

Those resources should be reported separately if they become relevant to the
paper's end-to-end claim.
