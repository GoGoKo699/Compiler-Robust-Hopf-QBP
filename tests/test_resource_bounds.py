from __future__ import annotations

import unittest

from compiler_robust_hopf.resource_bounds import (
    generic_all_column_cqsp_size_proxy,
    geometric_tail_bound_holds,
    lightcone_depth_lower_bound,
    lightcone_parameter_slots,
    low_workspace_absorption_holds,
    parameter_count_depth_lower_bound,
    real_state_parameter_dimension,
    routed_geometric_inequality_holds,
    routed_workspace_audit_holds,
    subtree_polynomial_absorption_holds,
)
from compiler_robust_hopf.unified_compiler import choose_routed_cut


class ResourceBoundTests(unittest.TestCase):
    def test_uniform_geometric_tail_bound(self) -> None:
        for n in range(1, 81):
            N = 1 << n
            shifts = {
                0,
                1,
                n,
                n * n,
                max(0, N // max(1, n * n)),
                max(0, N // n),
                N,
                10 * N,
            }
            for shift in shifts:
                self.assertTrue(geometric_tail_bound_holds(n, shift))

    def test_low_workspace_absorption(self) -> None:
        for n in range(1, 257):
            for ancillas in {1, max(1, n), max(1, 2 * n), 4 * n - 1}:
                if ancillas < 4 * n:
                    self.assertTrue(
                        low_workspace_absorption_holds(n, ancillas)
                    )

    def test_routed_cut_workspace_and_geometric_inequality(self) -> None:
        for n in range(2, 97):
            N = 1 << n
            budgets = {
                4 * n,
                4 * n + 1,
                max(4 * n, N // max(1, n * n)),
                max(4 * n, N // n),
                max(4 * n, N),
                max(4 * n, 2 * N),
                max(4 * n, 8 * N),
            }
            for ancillas in budgets:
                cut = choose_routed_cut(n, ancillas)
                self.assertIsNotNone(cut)
                assert cut is not None
                self.assertTrue(routed_workspace_audit_holds(n, cut))
                self.assertTrue(
                    routed_geometric_inequality_holds(n, ancillas)
                )

    def test_subtree_polynomial_term_is_absorbed(self) -> None:
        for n in range(1, 97):
            for suffix in range(1, n + 1):
                self.assertTrue(
                    subtree_polynomial_absorption_holds(n, suffix)
                )

    def test_real_state_parameter_and_lightcone_bounds(self) -> None:
        for n in range(1, 129):
            dimension = real_state_parameter_dimension(n)
            self.assertEqual(dimension, (1 << n) - 1)
            for ancillas in (0, 1, n, 1 << n, 1 << (n + 2)):
                lower = parameter_count_depth_lower_bound(n, ancillas)
                self.assertGreaterEqual(
                    4 * lower * (n + ancillas), dimension
                )
                if lower > 0:
                    self.assertLess(
                        4 * (lower - 1) * (n + ancillas), dimension
                    )

            lightcone = lightcone_depth_lower_bound(n)
            self.assertGreaterEqual(
                lightcone_parameter_slots(n, lightcone), dimension
            )
            if lightcone > 0:
                self.assertLess(
                    lightcone_parameter_slots(n, lightcone - 1), dimension
                )
            if n >= 16:
                self.assertGreaterEqual(lightcone, n // 2)

    def test_generic_all_column_cqsp_is_quadratic_in_dimension(self) -> None:
        for n in range(1, 33):
            dimension = 1 << n
            self.assertEqual(
                generic_all_column_cqsp_size_proxy(n),
                dimension * dimension,
            )


if __name__ == "__main__":
    unittest.main()
