"""Exact arithmetic checks used by the strict-zero echo proof audit.

The functions in this module do not prove the circuit identities; those are
proved algebraically and checked as complete operators in ``strict_zero_echo``.
They expose the elementary summations and lower-bound counts without floating
point arithmetic so that the asymptotic reductions can be regression tested.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction


@dataclass(frozen=True)
class StrictZeroAuditRow:
    """One exact-arithmetic audit row for the strict-zero theorem."""

    n: int
    dimension: int
    dyadic_harmonic_sum: Fraction
    dyadic_harmonic_bound: Fraction
    polynomial_depth_term: int
    polynomial_depth_bound: Fraction
    geometric_size_sum: int
    real_state_dimension: int
    parameter_count_size_lower_bound: int
    parameter_count_depth_lower_bound: int

    def as_dict(self) -> dict[str, int | str]:
        payload = asdict(self)
        for key in (
            "dyadic_harmonic_sum",
            "dyadic_harmonic_bound",
            "polynomial_depth_bound",
        ):
            payload[key] = str(payload[key])
        return payload


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def ceil_fraction(value: Fraction) -> int:
    """Return the exact ceiling of a rational number."""

    return -(-value.numerator // value.denominator)


def dyadic_harmonic_sum(n: int) -> Fraction:
    """Return ``sum_{q=2}^n 2**q/q`` exactly."""

    _validate_n(n)
    return sum((Fraction(1 << q, q) for q in range(2, n + 1)), Fraction())


def dyadic_harmonic_bound(n: int) -> Fraction:
    """Return the uniform proof bound ``6*2**n/n``."""

    _validate_n(n)
    return Fraction(6 * (1 << n), n)


def dyadic_harmonic_bound_holds(n: int) -> bool:
    """Check the exact inequality used in the depth summation."""

    return dyadic_harmonic_sum(n) <= dyadic_harmonic_bound(n)


def polynomial_depth_term(n: int) -> int:
    """Expose a conservative ``n**2`` sequential/predicate term."""

    _validate_n(n)
    return n * n


def polynomial_depth_bound(n: int) -> Fraction:
    """Return ``4*2**n/n``, which uniformly dominates ``n**2``."""

    _validate_n(n)
    return Fraction(4 * (1 << n), n)


def polynomial_absorption_holds(n: int) -> bool:
    """Check ``n**2 <= 4*2**n/n`` exactly."""

    return Fraction(polynomial_depth_term(n), 1) <= polynomial_depth_bound(n)


def geometric_size_sum(n: int) -> int:
    """Return ``sum_{q=2}^n 2**q`` exactly."""

    _validate_n(n)
    if n < 2:
        return 0
    return (1 << (n + 1)) - 4


def real_state_parameter_dimension(n: int) -> int:
    """Dimension of an open real-state chart on the unit sphere."""

    _validate_n(n)
    return (1 << n) - 1


def parameter_count_size_lower_bound(n: int) -> int:
    """One safe lower bound from at most four real parameters per 1-qubit gate."""

    return ceil_fraction(Fraction(real_state_parameter_dimension(n), 4))


def parameter_count_depth_lower_bound(n: int) -> int:
    """Depth lower bound from at most ``n`` parameterized gates per layer."""

    return ceil_fraction(Fraction(real_state_parameter_dimension(n), 4 * n))


def strict_zero_audit_row(n: int) -> StrictZeroAuditRow:
    """Return one exact-arithmetic audit row."""

    _validate_n(n)
    return StrictZeroAuditRow(
        n=n,
        dimension=1 << n,
        dyadic_harmonic_sum=dyadic_harmonic_sum(n),
        dyadic_harmonic_bound=dyadic_harmonic_bound(n),
        polynomial_depth_term=polynomial_depth_term(n),
        polynomial_depth_bound=polynomial_depth_bound(n),
        geometric_size_sum=geometric_size_sum(n),
        real_state_dimension=real_state_parameter_dimension(n),
        parameter_count_size_lower_bound=parameter_count_size_lower_bound(n),
        parameter_count_depth_lower_bound=parameter_count_depth_lower_bound(n),
    )
