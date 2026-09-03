from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.frames import direct_addressed_depth_layer, hopf_ry
from compiler_robust_hopf.resource_bounds import (
    generic_all_column_cqsp_size_proxy,
    lightcone_depth_lower_bound,
    lightcone_parameter_slots,
    low_workspace_absorption_holds,
    parameter_count_depth_lower_bound,
    real_state_parameter_dimension,
    routed_geometric_inequality_holds,
    ucg_geometric_tail,
    ucg_geometric_tail_upper_bound,
)
from compiler_robust_hopf.unified_compiler import (
    choose_routed_cut,
    route_workspace_row,
)


class ResourceBoundTests(unittest.TestCase):
    def test_router_counts_and_workspace_envelope(self) -> None:
        for n in range(2, 65):
            for t in range(1, n):
                row = route_workspace_row(n, t)
                branches = 1 << t
                suffix = n - t
                self.assertEqual(
                    row.control_copy_ancillas,
                    (branches - 1) * (suffix + 1) - t,
                )
                self.assertEqual(
                    row.forward_fredkin_gates,
                    (branches - 1) * (suffix + 1),
                )
                self.assertLessEqual(
                    row.exact_complete_peak_ancillas,
                    row.simple_workspace_envelope,
                )
                self.assertEqual(
                    row.simple_workspace_envelope,
                    2 * branches * (suffix + 1),
                )

    def test_low_workspace_polynomial_term_is_absorbed(self) -> None:
        for n in range(1, 257):
            for m in {1, max(1, n), max(1, 2 * n), 4 * n - 1}:
                if m < 4 * n:
                    self.assertTrue(low_workspace_absorption_holds(n, m))

    def test_maximal_routed_cut_geometric_inequality(self) -> None:
        for n in range(2, 129):
            dimension = 1 << n
            budgets = {
                4 * n,
                4 * n + 1,
                max(4 * n, dimension // max(1, n * n)),
                max(4 * n, dimension // n),
                dimension,
                2 * dimension,
                8 * dimension,
                *[1 << power for power in range(0, n + 4)],
            }
            for m in budgets:
                if m < 4 * n:
                    continue
                self.assertIsNotNone(choose_routed_cut(n, m))
                self.assertTrue(routed_geometric_inequality_holds(n, m))

    def test_real_state_parameter_and_lightcone_lower_bounds(self) -> None:
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

    def test_uniform_ucg_geometric_tail_bound(self) -> None:
        for n in range(1, 81):
            dimension = 1 << n
            for shift in {
                0,
                1,
                n,
                n * n,
                max(0, dimension // max(1, n * n)),
                max(0, dimension // n),
                dimension,
                10 * dimension,
            }:
                self.assertLessEqual(
                    ucg_geometric_tail(n, shift),
                    ucg_geometric_tail_upper_bound(n, shift)
                    * (1.0 + 1e-12),
                )

    def test_generic_all_column_cqsp_scale_is_quadratic(self) -> None:
        for n in range(1, 33):
            dimension = 1 << n
            self.assertEqual(
                generic_all_column_cqsp_size_proxy(n),
                dimension * dimension,
            )

    def test_each_addressed_layer_is_a_full_width_ucg(self) -> None:
        rng = np.random.default_rng(260914)
        for n in range(1, 7):
            dimension = 1 << n
            for depth in range(n):
                angles = rng.uniform(-1.0, 1.0, size=1 << depth)
                expected = np.eye(dimension, dtype=complex)
                target_shift = n - depth - 1
                target_mask = 1 << target_shift
                suffix_mask = target_mask - 1
                for label in range(dimension):
                    if label & target_mask:
                        continue
                    partner = label | target_mask
                    prefix = label >> (n - depth) if depth else 0
                    theta = (
                        angles[prefix]
                        if (label & suffix_mask) == 0
                        else 0.0
                    )
                    expected[
                        np.ix_([label, partner], [label, partner])
                    ] = hopf_ry(float(theta))
                np.testing.assert_allclose(
                    direct_addressed_depth_layer(n, depth, angles),
                    expected,
                    atol=1e-12,
                    rtol=0.0,
                )


if __name__ == "__main__":
    unittest.main()
