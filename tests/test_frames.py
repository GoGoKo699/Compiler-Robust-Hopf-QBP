from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.conventions import marker_label
from compiler_robust_hopf.frames import (
    canonical_magnitude_angle_mask,
    complex_frame_matrix,
    complex_magnitude_frame_matrix,
    direct_real_frame,
    in_canonical_magnitude_domain,
    real_frame_matrix,
    real_tree_data,
)


class FrameTests(unittest.TestCase):
    def test_direct_addressed_frame_matches_recursive_frame(self) -> None:
        rng = np.random.default_rng(260906)
        for n in range(1, 8):
            theta = rng.uniform(-1.1, 1.1, size=(1 << n) - 1)
            np.testing.assert_allclose(
                direct_real_frame(n, theta),
                real_frame_matrix(theta),
                atol=1e-12,
                rtol=0.0,
            )

    def test_real_frame_is_orthogonal(self) -> None:
        rng = np.random.default_rng(260907)
        for n in range(1, 8):
            theta = rng.uniform(-1.2, 1.2, size=(1 << n) - 1)
            frame = real_frame_matrix(theta)
            np.testing.assert_allclose(
                frame.T @ frame,
                np.eye(1 << n),
                atol=1e-12,
                rtol=0.0,
            )
            data = real_tree_data(theta)
            np.testing.assert_allclose(frame[:, 0], data.state, atol=1e-12)
            np.testing.assert_allclose(
                data.metric,
                data.incoming_amplitude**2,
                atol=1e-12,
                rtol=0.0,
            )

    def test_canonical_real_domain_makes_incoming_amplitudes_nonnegative(self) -> None:
        rng = np.random.default_rng(260908)
        for n in range(1, 8):
            count = (1 << n) - 1
            split = (1 << (n - 1)) - 1 if n > 1 else 0
            theta = np.empty(count, dtype=float)
            theta[:split] = rng.uniform(0.0, 0.5 * np.pi, size=split)
            theta[split:] = rng.uniform(0.0, 2.0 * np.pi, size=count - split)
            self.assertTrue(in_canonical_magnitude_domain(theta))
            self.assertTrue(np.all(canonical_magnitude_angle_mask(theta)))
            data = real_tree_data(theta)
            self.assertTrue(np.all(data.incoming_amplitude >= -1e-14))
            np.testing.assert_allclose(
                data.incoming_amplitude,
                data.sqrt_metric,
                atol=1e-12,
                rtol=0.0,
            )

    def test_canonical_complex_magnitude_domain_uses_half_pi_everywhere(self) -> None:
        rng = np.random.default_rng(260909)
        for n in range(1, 8):
            theta = rng.uniform(0.0, 0.5 * np.pi, size=(1 << n) - 1)
            self.assertTrue(
                in_canonical_magnitude_domain(theta, complex_chart=True)
            )
            invalid = theta.copy()
            invalid[-1] = np.pi
            self.assertFalse(
                in_canonical_magnitude_domain(invalid, complex_chart=True)
            )

    def test_singular_coordinate_has_zero_derivative_but_unit_frame_continuation(self) -> None:
        theta = np.asarray([0.0, 0.43, 0.71])
        data = real_tree_data(theta)
        # Node 3 lies in the root's right subtree, which has zero incoming mass.
        self.assertEqual(float(data.incoming_amplitude[2]), 0.0)
        self.assertEqual(float(data.metric[2]), 0.0)
        self.assertFalse(bool(data.regular_mask[2]))
        np.testing.assert_allclose(
            data.derivatives[2],
            np.zeros(4),
            atol=1e-12,
            rtol=0.0,
        )
        continuation = real_frame_matrix(theta)[:, marker_label(3, 2)]
        self.assertAlmostEqual(float(np.linalg.norm(continuation)), 1.0)

    def test_separated_complex_magnitude_frame_is_unitary(self) -> None:
        rng = np.random.default_rng(260910)
        for n in range(1, 7):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            phase = rng.uniform(-2.0, 2.0, size=1 << n)
            frame = complex_magnitude_frame_matrix(theta, phase)
            np.testing.assert_allclose(
                frame.conj().T @ frame,
                np.eye(1 << n),
                atol=1e-12,
                rtol=0.0,
            )
            np.testing.assert_allclose(
                complex_frame_matrix(theta, phase),
                frame,
                atol=1e-12,
                rtol=0.0,
            )


if __name__ == "__main__":
    unittest.main()
