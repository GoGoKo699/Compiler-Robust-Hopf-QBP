from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.frames import (
    complex_frame_matrix,
    direct_real_frame,
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

    def test_separated_complex_frame_is_unitary(self) -> None:
        rng = np.random.default_rng(260908)
        for n in range(1, 7):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            phase = rng.uniform(-2.0, 2.0, size=1 << n)
            frame = complex_frame_matrix(theta, phase)
            np.testing.assert_allclose(
                frame.conj().T @ frame,
                np.eye(1 << n),
                atol=1e-12,
                rtol=0.0,
            )


if __name__ == "__main__":
    unittest.main()
