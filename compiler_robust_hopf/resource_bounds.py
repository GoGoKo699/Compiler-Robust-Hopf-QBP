"""Exact integer checks supporting the unified compiler resource proof.

These helpers make the proof inequalities machine-checkable. They do not infer
asymptotic statements from numerical fitting and they do not replace the
analytic arguments in the documentation.
"""
from __future__ import annotations

from fractions import Fraction

from .unified_compiler import choose_routed_cut, route_workspace_row


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _ceil_div(numerator: int, denominator: int) -> int:
    if numerator < 0 or denominator < 1:
        raise ValueError("Require numerator>=0 and denominator>=1.")
    return (numerator + denominator - 1) // denominator


def _ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive.")
    return (value - 1).bit_length()


def geometric_tail_sum(n: int, denominator_shift: int) -> Fraction:
    """Return ``sum_{k=1}^n 2^k/(k+s)`` exactly."""

    _validate_n(n)
    if denominator_shift < 0:
        raise ValueError("denominator_shift must be nonnegative.")
    return sum(
        (Fraction(1 << k, k + denominator_shift) for k in range(1, n + 1)),
        start=Fraction(0, 1),
    )


def geometric_tail_upper_bound(n: int, denominator_shift: int) -> Fraction:
    """Return the uniform bound ``6*2^n/(n+s)`` exactly."""

    _validate_n(n)
    if denominator_shift < 0:
        raise ValueError("denominator_shift must be nonnegative.")
    return Fraction(6 * (1 << n), n + denominator_shift)


def geometric_tail_bound_holds(n: int, denominator_shift: int) -> bool:
    return geometric_tail_sum(n, denominator_shift) <= geometric_tail_upper_bound(
        n, denominator_shift
    )


def low_workspace_absorption_holds(n: int, ancillas: int) -> bool:
    """Check the explicit low-workspace absorption used for ``1<=m<4n``.

    The uniform integer inequality

    ``n^2 <= 20 * 2^n/(n+m)``

    is stronger than needed for the asymptotic proof and holds throughout the
    declared low-workspace range.
    """

    _validate_n(n)
    if not 1 <= ancillas < 4 * n:
        raise ValueError("Require 1<=ancillas<4*n.")
    return n * n * (n + ancillas) <= 20 * (1 << n)


def routed_geometric_inequality_holds(n: int, ancillas: int) -> bool:
    """Check the maximal-cut inequality for ``m>=4n``.

    For the largest feasible cut ``t``, write ``B=2^t`` and ``s=n-t``. If
    ``s>1``, infeasibility of the next cut gives ``m < 4 B s`` and hence
    ``2^s/s < 4*2^n/m``. The ``s=1`` endpoint is handled separately.
    """

    _validate_n(n)
    if ancillas < 4 * n:
        raise ValueError("Require ancillas>=4*n.")
    cut = choose_routed_cut(n, ancillas)
    if cut is None:
        return False
    suffix = n - cut
    if suffix <= 1:
        return True
    branches = 1 << cut
    next_cut_infeasible = ancillas < 4 * branches * suffix
    desired = ancillas * (1 << suffix) < 4 * (1 << n) * suffix
    return next_cut_infeasible and desired


def subtree_polynomial_absorption_holds(n: int, suffix_qubits: int) -> bool:
    """Check ``s^2=O(n+2^s/s)`` with an explicit constant three."""

    _validate_n(n)
    if not 1 <= suffix_qubits <= n:
        raise ValueError("suffix_qubits must lie in 1, ..., n.")
    exponential = _ceil_div(1 << suffix_qubits, suffix_qubits)
    return suffix_qubits * suffix_qubits <= 3 * (n + exponential)


def routing_level_fredkin_count(n: int, t: int, level: int) -> int:
    """Return the number of routed data/token lanes at one binary-tree level."""

    if n < 2 or not 1 <= t < n:
        raise ValueError("A routed cut requires n>=2 and 1<=t<n.")
    if not 0 <= level < t:
        raise ValueError("level must lie in 0, ..., t-1.")
    suffix = n - t
    return (1 << level) * (suffix + 1)


def maximum_routing_fanout_depth(n: int, t: int) -> int:
    """Return the largest coherent control-copy depth over routing levels."""

    return max(
        _ceil_log2(routing_level_fredkin_count(n, t, level))
        for level in range(t)
    )


def real_state_parameter_dimension(n: int) -> int:
    _validate_n(n)
    return (1 << n) - 1


def parameter_count_depth_lower_bound(n: int, ancillas: int) -> int:
    """Return the parameter-count depth lower-bound proxy.

    At most four continuous real parameters are assigned to each one-qubit gate
    location in one depth layer on ``n+m`` wires.
    """

    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    return _ceil_div(real_state_parameter_dimension(n), 4 * (n + ancillas))


def lightcone_parameter_slots(n: int, depth: int) -> int:
    """Return the audited upper bound ``4*n*2^D`` on relevant parameters."""

    _validate_n(n)
    if depth < 0:
        raise ValueError("depth must be nonnegative.")
    return 4 * n * (1 << depth)


def lightcone_depth_lower_bound(n: int) -> int:
    """Return the least depth whose light-cone parameter bound reaches ``2^n-1``."""

    _validate_n(n)
    target = real_state_parameter_dimension(n)
    depth = 0
    while lightcone_parameter_slots(n, depth) < target:
        depth += 1
    return depth


def generic_all_column_cqsp_size_proxy(n: int) -> int:
    """Return the generic all-column CQSP size ``2^(n+n)=4^n``."""

    _validate_n(n)
    return 1 << (2 * n)


def routed_workspace_audit_holds(n: int, t: int) -> bool:
    """Check every closed-form routed-workspace contribution."""

    row = route_workspace_row(n, t)
    branches = 1 << t
    suffix = n - t
    return all(
        (
            row.branch_data_ancillas == (branches - 1) * suffix,
            row.token_ancillas == branches,
            row.control_copy_ancillas
            == (branches - 1) * (suffix + 1) - t,
            row.branch_flag_ancillas == (branches if suffix > 1 else 0),
            row.forward_fredkin_gates == (branches - 1) * (suffix + 1),
            row.maximum_fanout_depth == maximum_routing_fanout_depth(n, t),
            row.exact_complete_peak_ancillas <= row.simple_workspace_envelope,
        )
    )
