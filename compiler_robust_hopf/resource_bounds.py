"""Exact integer helpers for the unified Hopf-frame resource proof.

These routines expose the elementary inequalities used by the analytic proof.
They are transparent regression checks and ledgers, not substitutes for the
proof in ``docs/COMPILER_THEOREM.md``.
"""
from __future__ import annotations


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _validate_workspace(m: int) -> None:
    if m < 0:
        raise ValueError("m must be nonnegative.")


def _ceil_div(numerator: int, denominator: int) -> int:
    if numerator < 0 or denominator < 1:
        raise ValueError("Require numerator>=0 and denominator>=1.")
    return (numerator + denominator - 1) // denominator


def real_state_parameter_dimension(n: int) -> int:
    """Return the dimension of the real unit sphere used by the Hopf chart."""

    _validate_n(n)
    return (1 << n) - 1


def parameter_count_depth_lower_bound(n: int, m: int) -> int:
    """Return the integer parameter-count lower bound on circuit depth.

    At most ``n+m`` arbitrary one-qubit gates can appear in one depth layer,
    and four real parameters per gate is a deliberately generous upper bound.
    """

    _validate_n(n)
    _validate_workspace(m)
    return _ceil_div(real_state_parameter_dimension(n), 4 * (n + m))


def lightcone_parameter_slots(n: int, depth: int) -> int:
    """Return the upper bound ``4*n*2**depth`` for relevant parameters."""

    _validate_n(n)
    if depth < 0:
        raise ValueError("depth must be nonnegative.")
    return 4 * n * (1 << depth)


def lightcone_depth_lower_bound(n: int) -> int:
    """Return the first depth whose output light cones can carry all parameters."""

    _validate_n(n)
    dimension = real_state_parameter_dimension(n)
    depth = 0
    while lightcone_parameter_slots(n, depth) < dimension:
        depth += 1
    return depth


def generic_all_column_cqsp_size_proxy(n: int) -> int:
    """Return the generic CQSP size scale for all ``2**n`` frame columns."""

    _validate_n(n)
    return 1 << (2 * n)


def low_workspace_absorption_holds(n: int, m: int) -> bool:
    """Check the explicit low-workspace inequality used by the direct schedule.

    For ``1 <= m < 4n`` the universal integer inequality

    ``n**2 <= 20 * 2**n / (n+m)``

    absorbs the polynomial sequential term into the state-preparation scale.
    The constant 20 is not optimized.
    """

    _validate_n(n)
    if not 1 <= m < 4 * n:
        raise ValueError("Require 1 <= m < 4n.")
    return n * n * (n + m) <= 20 * (1 << n)


def ucg_geometric_tail(n: int, denominator_shift: int) -> float:
    """Return ``sum_{k=1}^n 2**k/(k+s)`` for diagnostics."""

    _validate_n(n)
    _validate_workspace(denominator_shift)
    return sum(
        (1 << k) / (k + denominator_shift) for k in range(1, n + 1)
    )


def ucg_geometric_tail_upper_bound(n: int, denominator_shift: int) -> float:
    """Return the uniform analytic upper bound ``6*2**n/(n+s)``."""

    _validate_n(n)
    _validate_workspace(denominator_shift)
    return 6.0 * (1 << n) / (n + denominator_shift)


def routed_geometric_inequality_holds(n: int, m: int) -> bool:
    """Check the maximal-cut inequality for the routed schedule.

    The largest feasible nontrivial cut satisfies
    ``2*2**t*(n-t+1) <= m``. If ``s=n-t>1``, failure of the next cut gives
    ``m < 4*2**t*s`` and therefore ``2**s/s < 4*2**n/m``.
    """

    _validate_n(n)
    if n < 2 or m < 4 * n:
        raise ValueError("Require n>=2 and m>=4n.")

    from .unified_compiler import choose_routed_cut

    t = choose_routed_cut(n, m)
    if t is None:
        return False
    s = n - t
    if s == 1:
        return True
    branches = 1 << t
    dimension = 1 << n
    return (
        m < 4 * branches * s
        and m * (1 << s) < 4 * dimension * s
    )
