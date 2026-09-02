from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.frames import (
    direct_addressed_depth_layer,
    direct_real_frame,
)
from compiler_robust_hopf.strict_zero_mottonen import (
    completion_correction_factorized_frame,
    completion_correction_matrix,
    completion_correction_residual,
    conditioned_layer_residual,
    conditioned_small_completion_layer,
    direct_conditioned_size_proxy,
    full_preparation_depth_layer,
    layer_correction_matrix,
    layer_correction_product,
    mottonen_completion,
    mottonen_completion_primitive_upper_bound,
    prefix_completion,
    rightmost_one_partition,
    rightmost_one_stratum_labels,
    strict_zero_mottonen_row,
    suffix_weighted_sum,
)


class StrictZeroMottonenTests(unittest.TestCase):
    def test_rightmost_one_strata_partition_the_basis(self) -> None:
        for n in range(1, 20):
            partition = rightmost_one_partition(n)
            flattened = [label for stratum in partition for label in stratum]
            self.assertEqual(len(flattened), 1 << n)
            self.assertEqual(len(flattened), len(set(flattened)))
            self.assertEqual(set(flattened), set(range(1 << n)))
            self.assertEqual(partition[0], (0,))
            for position in range(n):
                labels = rightmost_one_stratum_labels(n, position)
                self.assertEqual(len(labels), 1 << position)
                suffix_mask = (1 << (n - position - 1)) - 1
                delimiter = 1 << (n - position - 1)
                for label in labels:
                    self.assertEqual(label & suffix_mask, 0)
                    self.assertNotEqual(label & delimiter, 0)

    def test_mottonen_completion_has_the_hopf_state_column(self) -> None:
        rng = np.random.default_rng(260914)
        for n in range(1, 9):
            theta = rng.uniform(-1.1, 1.1, size=(1 << n) - 1)
            completion = mottonen_completion(n, theta)
            frame = direct_real_frame(n, theta)
            np.testing.assert_allclose(
                completion[:, 0], frame[:, 0], atol=1e-12, rtol=0.0
            )
            np.testing.assert_allclose(
                completion.conj().T @ completion,
                np.eye(1 << n),
                atol=1e-12,
                rtol=0.0,
            )

    def test_addressed_layer_is_suffix_conditioned_smaller_ucr(self) -> None:
        rng = np.random.default_rng(260915)
        for n in range(1, 9):
            for depth in range(n):
                angles = rng.uniform(-1.0, 1.0, size=1 << depth)
                np.testing.assert_allclose(
                    conditioned_small_completion_layer(n, depth, angles),
                    direct_addressed_depth_layer(n, depth, angles),
                    atol=1e-12,
                    rtol=0.0,
                )
                self.assertLessEqual(
                    conditioned_layer_residual(n, depth, angles), 1e-12
                )

    def test_completion_correction_recovers_the_complete_frame(self) -> None:
        rng = np.random.default_rng(260916)
        for n in range(1, 9):
            theta = rng.uniform(-0.95, 0.95, size=(1 << n) - 1)
            reference = direct_real_frame(n, theta)
            np.testing.assert_allclose(
                completion_correction_factorized_frame(n, theta),
                reference,
                atol=1e-12,
                rtol=0.0,
            )
            self.assertLessEqual(
                completion_correction_residual(n, theta), 1e-12
            )

    def test_correction_has_the_claimed_stratum_blocks(self) -> None:
        rng = np.random.default_rng(260917)
        for n in range(2, 8):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            correction = completion_correction_matrix(n, theta)
            self.assertAlmostEqual(correction[0, 0], 1.0)
            position_zero = rightmost_one_stratum_labels(n, 0)
            np.testing.assert_allclose(
                correction[np.ix_(position_zero, position_zero)],
                np.eye(1),
                atol=1e-12,
                rtol=0.0,
            )
            for position in range(1, n):
                labels = rightmost_one_stratum_labels(n, position)
                expected = prefix_completion(position, theta).conj().T
                np.testing.assert_allclose(
                    correction[np.ix_(labels, labels)],
                    expected,
                    atol=1e-12,
                    rtol=0.0,
                )
            np.testing.assert_allclose(
                correction.conj().T @ correction,
                np.eye(1 << n),
                atol=1e-12,
                rtol=0.0,
            )

    def test_layer_corrections_equal_the_rightmost_one_correction(self) -> None:
        rng = np.random.default_rng(260918)
        for n in range(1, 8):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            np.testing.assert_allclose(
                layer_correction_product(n, theta),
                completion_correction_matrix(n, theta),
                atol=1e-12,
                rtol=0.0,
            )

            offset = 0
            for depth in range(n):
                width = 1 << depth
                angles = theta[offset : offset + width]
                correction = layer_correction_matrix(n, depth, angles)
                preparation = full_preparation_depth_layer(n, depth, angles)
                addressed = direct_addressed_depth_layer(n, depth, angles)
                np.testing.assert_allclose(
                    preparation @ correction,
                    addressed,
                    atol=1e-12,
                    rtol=0.0,
                )
                offset += width

    def test_weighted_sums_and_size_proxies_are_linear_in_dimension(self) -> None:
        for n in range(1, 257):
            N = 1 << n
            self.assertEqual(
                suffix_weighted_sum(n, power=1),
                2 * N - n - 2,
            )
            self.assertLess(suffix_weighted_sum(n, power=2), 6 * N)
            self.assertEqual(
                mottonen_completion_primitive_upper_bound(n), 2 * N - 3
            )
            linear = direct_conditioned_size_proxy(n, quadratic=False)
            quadratic = direct_conditioned_size_proxy(n, quadratic=True)
            self.assertLess(linear, 5 * N)
            self.assertLess(quadratic, 12 * N)

            row = strict_zero_mottonen_row(n)
            self.assertEqual(row.clean_ancillas, 0)
            self.assertEqual(row.dimension, N)
            self.assertEqual(row.hopf_angles, N - 1)
            self.assertEqual(row.direct_conditioned_linear_size_proxy, linear)
            self.assertEqual(
                row.direct_conditioned_quadratic_size_proxy, quadratic
            )
            self.assertLess(row.completion_plus_correction_size_proxy, 24 * N)
            self.assertEqual(row.optimal_size_scale, N)
            self.assertEqual(row.current_depth_upper_scale, N)
            self.assertLessEqual(row.optimal_depth_target_proxy, N + n)


if __name__ == "__main__":
    unittest.main()
