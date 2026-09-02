"""Independent bookkeeping checks for the routed optimal-frame candidate.

This module does not synthesize circuits.  It exposes the exact combinatorial
counts and elementary inequalities used by the second internal proof audit of
the positive-workspace theorem.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math

from .optimal_parallel import choose_routed_cut


@dataclass(frozen=True)
class RouterAuditRow:
    """Exact register and routing counts for one nontrivial tree cut."""

    n: int
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    forward_fredkin_gates: int
    round_trip_fredkin_gates: int
    exact_control_copy_ancillas: int
    maximum_fanout_depth: int
    branch_data_ancillas: int
    token_ancillas: int
    branch_flag_ancillas: int
    copy_pool_covers_flags: bool
    exact_tail_peak_ancillas: int
    prefix_compiler_ancillas: int
    exact_complete_peak_ancillas: int
    simple_workspace_envelope: int

    def as_dict(self) -> dict[str, int | bool]:
        return asdict(self)


def _validate_cut(n: int, t: int) -> None:
    if n < 2:
        raise ValueError("n must be at least two for a routed cut.")
    if not 1 <= t < n:
        raise ValueError("A routed cut requires 1 <= t < n.")


def ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive.")
    return (value - 1).bit_length()


def routing_level_fredkin_count(n: int, t: int, level: int) -> int:
    """Return the number of Fredkin gates at one forward routing level."""

    _validate_cut(n, t)
    if not 0 <= level < t:
        raise ValueError("level must lie in 0, ..., t-1.")
    s = n - t
    return (1 << level) * (s + 1)


def exact_control_copy_count(n: int, t: int) -> int:
    """Return the exact number of extra coherent routing controls.

    At level ``ell`` there are ``2**ell * (s+1)`` Fredkin gates.  The original
    prefix qubit can control one of them, so that level needs one fewer copied
    control.  Different prefix bits use disjoint copy pools and are fanned out
    concurrently.
    """

    _validate_cut(n, t)
    return sum(
        routing_level_fredkin_count(n, t, level) - 1
        for level in range(t)
    )


def maximum_routing_fanout_depth(n: int, t: int) -> int:
    """Return the maximum binary CNOT-tree depth for one routing pass."""

    _validate_cut(n, t)
    return max(
        ceil_log2(routing_level_fredkin_count(n, t, level))
        for level in range(t)
    )


def router_audit_row(n: int, t: int) -> RouterAuditRow:
    """Return exact counts and the conservative ``2 B(s+1)`` envelope."""

    _validate_cut(n, t)
    B = 1 << t
    s = n - t
    forward_fredkins = sum(
        routing_level_fredkin_count(n, t, level) for level in range(t)
    )
    copies = exact_control_copy_count(n, t)
    flags = B if s > 1 else 0
    data = (B - 1) * s
    tokens = B
    tail_peak = data + tokens + max(copies, flags)
    prefix_workspace = 3 * B - t
    complete_peak = max(tail_peak, prefix_workspace)
    envelope = 2 * B * (s + 1)
    return RouterAuditRow(
        n=n,
        prefix_qubits=t,
        suffix_qubits=s,
        branches=B,
        forward_fredkin_gates=forward_fredkins,
        round_trip_fredkin_gates=2 * forward_fredkins,
        exact_control_copy_ancillas=copies,
        maximum_fanout_depth=maximum_routing_fanout_depth(n, t),
        branch_data_ancillas=data,
        token_ancillas=tokens,
        branch_flag_ancillas=flags,
        copy_pool_covers_flags=copies >= flags,
        exact_tail_peak_ancillas=tail_peak,
        prefix_compiler_ancillas=prefix_workspace,
        exact_complete_peak_ancillas=complete_peak,
        simple_workspace_envelope=envelope,
    )


def low_workspace_absorption_holds(n: int, m: int) -> bool:
    """Check the explicit inequality ``n**2 <= 20*2**n/(n+m)``.

    The hypothesis is ``n>=1`` and ``1<=m<4n``.  It follows from the uniform
    elementary bound ``n**3 <= 4*2**n``.
    """

    if n < 1:
        raise ValueError("n must be positive.")
    if not 1 <= m < 4 * n:
        raise ValueError("The low-workspace audit requires 1 <= m < 4n.")
    return n * n * (n + m) <= 20 * (1 << n)


def routed_geometric_inequality_holds(n: int, m: int) -> bool:
    """Check the maximal-cut inequality used for ``m>=4n``.

    If the selected cut is not the last possible cut, maximality must imply
    ``2**s/s < 4*2**n/m``.  At the last cut, ``s=1`` and no geometric estimate
    is needed.
    """

    if n < 2:
        raise ValueError("n must be at least two.")
    if m < 4 * n:
        raise ValueError("The routed audit requires m >= 4n.")
    t = choose_routed_cut(n, m)
    if t is None:
        return False
    s = n - t
    if s == 1:
        return True
    N = 1 << n
    return m * (1 << s) < 4 * N * s


def real_state_parameter_dimension(n: int) -> int:
    """Return the dimension of the real unit sphere ``S^(2**n-1)``."""

    if n < 1:
        raise ValueError("n must be positive.")
    return (1 << n) - 1


def parameter_count_depth_lower_bound(n: int, m: int) -> int:
    """A conservative integer lower bound from gate-parameter counting.

    A one-qubit U(2) gate carries at most four real parameters and a depth layer
    on ``n+m`` wires contains at most ``n+m`` such gates.  Covering the real
    state sphere therefore requires at least this many layers.
    """

    if n < 1 or m < 0:
        raise ValueError("Require n>=1 and m>=0.")
    dimension = real_state_parameter_dimension(n)
    return math.ceil(dimension / (4 * (n + m)))


def lightcone_parameter_slots(n: int, depth: int) -> int:
    """Bound continuous gate parameters in the system-output light cone.

    Tracing backward from ``n`` system outputs, the number of wires at distance
    ``j`` is at most ``n*2**j``.  Summing over ``depth`` layers and charging four
    real parameters per one-qubit gate gives ``4*n*(2**depth-1)``.
    """

    if n < 1 or depth < 0:
        raise ValueError("Require n>=1 and depth>=0.")
    return 4 * n * ((1 << depth) - 1)


def lightcone_depth_lower_bound(n: int) -> int:
    """Return the first depth whose light-cone parameter bound can cover S^(N-1)."""

    if n < 1:
        raise ValueError("n must be positive.")
    target = real_state_parameter_dimension(n)
    depth = 0
    while lightcone_parameter_slots(n, depth) < target:
        depth += 1
    return depth


def generic_all_column_cqsp_size_proxy(n: int) -> int:
    """Return ``2**(n+n)=4**n`` from generic CQSP with n index qubits."""

    if n < 1:
        raise ValueError("n must be positive.")
    return 1 << (2 * n)
