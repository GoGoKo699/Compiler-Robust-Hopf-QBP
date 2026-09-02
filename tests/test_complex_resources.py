from __future__ import annotations

import math
import unittest

import numpy as np

from compiler_robust_hopf.complex_resources import (
    complex_workspace_row,
    diagonal_ancillas_used,
    diagonal_synthesis_row,
    strict_zero_real_frame_depth_proxy,
    strict_zero_real_frame_size_proxy,
)
from compiler_robust_hopf.frames import (
    direct_addressed_depth_layer,
    hopf_ry,
)


class ComplexResourceTests(unittest.TestCase):
    def test_all_budget_diagonal_regimes(self) -> None:
        for n in range(1, 41):
            N = 1 << n
            budgets = {
                0,
                1,
                max(0, 2 * n - 1),
                2 * n,
                max(0, N // n - 1),
                N // n,
                N // n + 1,
                N,
                3 * N,
            }
            for exponent in range(n + 2):
                budgets.add(1 << exponent)
            for ancillas in sorted(budgets):
                used = diagonal_ancillas_used(n, ancillas)
                row = diagonal_synthesis_row(n, ancillas)
                self.assertEqual(row.used_ancillas, used)
                self.assertLessEqual(used, ancillas)
                if used:
                    self.assertGreaterEqual(used, 2 * n)
                    self.assertLessEqual(used, N // n)
                    self.assertIn(
                        row.mode,
                        {"parallel-ancilla", "capped-parallel-ancilla"},
                    )
                else:
                    self.assertEqual(row.mode, "ancilla-free")
                self.assertLessEqual(
                    row.total_depth_proxy,
                    4 * row.theorem_depth_proxy,
                )
                self.assertLessEqual(row.size_proxy, 9 * N + 1)
                self.assertEqual(row.parameter_count, N)
                self.assertEqual(row.parameter_preprocess_proxy, n * N)

    def test_complex_composition_reuses_one_clean_pool(self) -> None:
        for n in range(1, 33):
            N = 1 << n
            budgets = {
                0,
                1,
                2,
                3,
                n,
                2 * n,
                max(0, N // max(1, n * n)),
                N // n,
                N,
                3 * N,
            }
            for ancillas in sorted(budgets):
                row = complex_workspace_row(n, ancillas)
                self.assertEqual(row.dimension, N)
                self.assertEqual(
                    row.common_workspace_upper_bound,
                    max(1, ancillas),
                )
                self.assertLessEqual(row.diagonal_ancillas_used, ancillas)
                self.assertEqual(
                    row.complex_frame_depth_proxy,
                    row.real_frame_depth_proxy + row.diagonal_depth_proxy,
                )
                self.assertEqual(
                    row.complex_frame_size_proxy,
                    row.real_frame_size_proxy + row.diagonal_size_proxy,
                )
                self.assertEqual(row.magnitude_reverse_frame_applications, 1)
                self.assertEqual(row.direct_phase_reverse_frame_applications, 0)
                self.assertEqual(row.magnitude_decode_operations_per_shot, N)
                self.assertEqual(row.phase_decode_operations_per_shot, 1)
                self.assertEqual(row.phase_parameter_preprocess_proxy, n * N)
                log_factor = max(1, math.ceil(math.log2(n + 1)))
                self.assertLessEqual(
                    row.candidate_depth_proxy,
                    3 * log_factor * row.optimal_qsp_depth_proxy,
                )

    def test_strict_zero_workspace_fallback(self) -> None:
        for n in range(1, 41):
            N = 1 << n
            self.assertEqual(
                strict_zero_real_frame_depth_proxy(n),
                n * (n + math.ceil(N / n)),
            )
            self.assertEqual(strict_zero_real_frame_size_proxy(n), n * N)
            row = complex_workspace_row(n, 0)
            self.assertLessEqual(row.strict_zero_frame_depth_proxy, 3 * N)
            self.assertEqual(
                row.strict_zero_frame_size_proxy,
                (n + 1) * N + 1,
            )

    def test_each_addressed_layer_is_a_full_width_ucg(self) -> None:
        rng = np.random.default_rng(260910)
        for n in range(1, 7):
            N = 1 << n
            for depth in range(n):
                angles = rng.uniform(-1.0, 1.0, size=1 << depth)
                expected = np.eye(N, dtype=complex)
                target_shift = n - depth - 1
                target_mask = 1 << target_shift
                suffix_mask = target_mask - 1
                for label in range(N):
                    if label & target_mask:
                        continue
                    partner = label | target_mask
                    prefix = label >> (n - depth) if depth else 0
                    theta = angles[prefix] if (label & suffix_mask) == 0 else 0.0
                    expected[np.ix_([label, partner], [label, partner])] = hopf_ry(
                        float(theta)
                    )
                np.testing.assert_allclose(
                    direct_addressed_depth_layer(n, depth, angles),
                    expected,
                    atol=1e-12,
                    rtol=0.0,
                )


if __name__ == "__main__":
    unittest.main()
