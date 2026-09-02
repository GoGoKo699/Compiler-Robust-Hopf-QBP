from __future__ import annotations

import unittest

from compiler_robust_hopf.optimal_audit import (
    exact_control_copy_count,
    generic_all_column_cqsp_size_proxy,
    lightcone_depth_lower_bound,
    lightcone_parameter_slots,
    low_workspace_absorption_holds,
    maximum_routing_fanout_depth,
    parameter_count_depth_lower_bound,
    real_state_parameter_dimension,
    routed_geometric_inequality_holds,
    router_audit_row,
    routing_level_fredkin_count,
)
from compiler_robust_hopf.optimal_parallel import choose_routed_cut


class OptimalAuditTests(unittest.TestCase):
    def test_exact_control_copy_formula_and_fanout_depth(self) -> None:
        for n in range(2, 41):
            for t in range(1, n):
                s = n - t
                B = 1 << t
                expected_copies = (B - 1) * (s + 1) - t
                self.assertEqual(exact_control_copy_count(n, t), expected_copies)
                expected_depth = max(
                    (routing_level_fredkin_count(n, t, level) - 1).bit_length()
                    for level in range(t)
                )
                self.assertEqual(
                    maximum_routing_fanout_depth(n, t), expected_depth
                )

    def test_exact_workspace_is_inside_candidate_envelope(self) -> None:
        for n in range(2, 65):
            for t in range(1, n):
                row = router_audit_row(n, t)
                B = 1 << t
                s = n - t
                self.assertEqual(
                    row.forward_fredkin_gates, (B - 1) * (s + 1)
                )
                self.assertEqual(
                    row.round_trip_fredkin_gates,
                    2 * (B - 1) * (s + 1),
                )
                self.assertTrue(row.copy_pool_covers_flags)
                self.assertLess(
                    row.exact_tail_peak_ancillas,
                    row.simple_workspace_envelope,
                )
                self.assertLessEqual(
                    row.prefix_compiler_ancillas,
                    row.simple_workspace_envelope,
                )
                self.assertLessEqual(
                    row.exact_complete_peak_ancillas,
                    row.simple_workspace_envelope,
                )

    def test_low_workspace_absorption_with_explicit_constant(self) -> None:
        for n in range(1, 257):
            for m in {1, max(1, n), max(1, 2 * n), 4 * n - 1}:
                if m < 4 * n:
                    self.assertTrue(low_workspace_absorption_holds(n, m))

    def test_maximal_cut_geometric_inequality(self) -> None:
        for n in range(2, 129):
            N = 1 << n
            budgets = {
                4 * n,
                4 * n + 1,
                max(4 * n, N // (n * n)),
                max(4 * n, N // n),
                N,
                2 * N,
                8 * N,
                *[1 << power for power in range(0, n + 4)],
            }
            for m in budgets:
                if m < 4 * n:
                    continue
                self.assertIsNotNone(choose_routed_cut(n, m))
                self.assertTrue(routed_geometric_inequality_holds(n, m))

    def test_real_state_parameter_and_lightcone_bounds(self) -> None:
        for n in range(1, 129):
            dimension = real_state_parameter_dimension(n)
            self.assertEqual(dimension, (1 << n) - 1)
            for m in (0, 1, n, 1 << n, 1 << (n + 2)):
                lower = parameter_count_depth_lower_bound(n, m)
                self.assertGreaterEqual(4 * lower * (n + m), dimension)
                if lower > 0:
                    self.assertLess(4 * (lower - 1) * (n + m), dimension)

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
            N = 1 << n
            self.assertEqual(generic_all_column_cqsp_size_proxy(n), N * N)


if __name__ == "__main__":
    unittest.main()
