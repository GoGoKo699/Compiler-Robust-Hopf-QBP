from __future__ import annotations

import unittest
from fractions import Fraction

from compiler_robust_hopf.strict_zero_audit import (
    dyadic_harmonic_bound,
    dyadic_harmonic_bound_holds,
    dyadic_harmonic_sum,
    geometric_size_sum,
    parameter_count_depth_lower_bound,
    parameter_count_size_lower_bound,
    polynomial_absorption_holds,
    polynomial_depth_bound,
    polynomial_depth_term,
    real_state_parameter_dimension,
    strict_zero_audit_row,
)


class StrictZeroEchoAuditTests(unittest.TestCase):
    def test_uniform_dyadic_harmonic_bound_exactly(self) -> None:
        for n in range(1, 1025):
            self.assertTrue(dyadic_harmonic_bound_holds(n), msg=f"n={n}")
            self.assertLessEqual(
                dyadic_harmonic_sum(n), dyadic_harmonic_bound(n)
            )

    def test_polynomial_depth_is_absorbed_exactly(self) -> None:
        for n in range(1, 1025):
            self.assertTrue(polynomial_absorption_holds(n), msg=f"n={n}")
            self.assertLessEqual(
                Fraction(polynomial_depth_term(n), 1),
                polynomial_depth_bound(n),
            )

    def test_geometric_size_sum_closed_form(self) -> None:
        self.assertEqual(geometric_size_sum(1), 0)
        for n in range(2, 256):
            self.assertEqual(
                geometric_size_sum(n),
                sum(1 << q for q in range(2, n + 1)),
            )
            self.assertLess(geometric_size_sum(n), 2 * (1 << n))

    def test_parameter_count_lower_bounds_are_safe(self) -> None:
        for n in range(1, 1025):
            dimension = real_state_parameter_dimension(n)
            size_lower = parameter_count_size_lower_bound(n)
            depth_lower = parameter_count_depth_lower_bound(n)
            self.assertGreaterEqual(4 * size_lower, dimension)
            if size_lower:
                self.assertLess(4 * (size_lower - 1), dimension)
            self.assertGreaterEqual(4 * n * depth_lower, dimension)
            if depth_lower:
                self.assertLess(4 * n * (depth_lower - 1), dimension)

    def test_audit_row_is_self_consistent(self) -> None:
        for n in range(1, 257):
            row = strict_zero_audit_row(n)
            self.assertEqual(row.dimension, 1 << n)
            self.assertEqual(row.real_state_dimension, (1 << n) - 1)
            self.assertLessEqual(
                row.dyadic_harmonic_sum, row.dyadic_harmonic_bound
            )
            self.assertLessEqual(
                Fraction(row.polynomial_depth_term, 1),
                row.polynomial_depth_bound,
            )
            payload = row.as_dict()
            self.assertEqual(payload["n"], n)
            self.assertIsInstance(payload["dyadic_harmonic_sum"], str)


if __name__ == "__main__":
    unittest.main()
