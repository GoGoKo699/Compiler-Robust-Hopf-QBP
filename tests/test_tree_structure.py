from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.frames import direct_real_frame
from compiler_robust_hopf.tree_structure import (
    prefix_angle_count,
    prefix_bridge_residual,
    reconstructed_frame,
    subtree_angle_indices,
    tail_direct_sum_residual,
)


class TreeStructureTests(unittest.TestCase):
    def test_prefix_and_tail_identities_for_every_cut(self) -> None:
        rng = np.random.default_rng(260914)
        for n in range(1, 9):
            theta = rng.uniform(-1.1, 1.1, size=(1 << n) - 1)
            reference = direct_real_frame(n, theta)
            for t in range(n + 1):
                self.assertLessEqual(
                    prefix_bridge_residual(n, t, theta), 1e-12
                )
                self.assertLessEqual(
                    tail_direct_sum_residual(n, t, theta), 1e-12
                )
                np.testing.assert_allclose(
                    reconstructed_frame(n, t, theta),
                    reference,
                    atol=1e-12,
                    rtol=0.0,
                )

    def test_subtree_angles_partition_every_angle_below_the_cut(self) -> None:
        for n in range(1, 15):
            total_angles = (1 << n) - 1
            for t in range(n + 1):
                suffix = n - t
                expected_per_subtree = (1 << suffix) - 1
                collected: list[int] = []
                for prefix in range(1 << t):
                    indices = subtree_angle_indices(n, t, prefix)
                    self.assertEqual(len(indices), expected_per_subtree)
                    collected.extend(indices)
                self.assertEqual(len(collected), len(set(collected)))
                self.assertEqual(
                    sorted(collected),
                    list(range(prefix_angle_count(t), total_angles)),
                )

    def test_invalid_subtree_prefix_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            subtree_angle_indices(3, 1, -1)
        with self.assertRaises(ValueError):
            subtree_angle_indices(3, 1, 2)


if __name__ == "__main__":
    unittest.main()
