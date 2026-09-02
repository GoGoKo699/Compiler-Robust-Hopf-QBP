from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.complex_analysis import (
    centered_leaf_phases,
    common_phase_factorization_residual,
    complex_chart_data,
    complex_magnitude_gradient,
    complex_phase_gradient,
    phase_gauge_residual,
    zero_amplitude_phase_residual,
)
from compiler_robust_hopf.conventions import marker_label
from compiler_robust_hopf.frames import complex_frame_matrix, real_tree_data


def random_hermitian(rng: np.random.Generator, dimension: int) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    return 0.5 * (raw + raw.conj().T)


class ComplexAnalysisTests(unittest.TestCase):
    def test_frame_contains_state_and_weighted_magnitude_tangents(self) -> None:
        rng = np.random.default_rng(260910)
        for n in range(1, 6):
            dimension = 1 << n
            magnitude = rng.uniform(-1.1, 1.1, size=dimension - 1)
            phase = rng.uniform(-1.5, 1.5, size=dimension)
            real = real_tree_data(magnitude)
            data = complex_chart_data(magnitude, phase)
            frame = complex_frame_matrix(magnitude, phase)
            np.testing.assert_allclose(
                frame[:, 0], data.state, atol=1e-12, rtol=0.0
            )
            for node, derivative in enumerate(
                data.magnitude_derivatives, start=1
            ):
                np.testing.assert_allclose(
                    derivative,
                    real.sqrt_metric[node - 1]
                    * frame[:, marker_label(node, n)],
                    atol=1e-12,
                    rtol=0.0,
                )

    def test_common_phase_is_a_projective_gauge(self) -> None:
        rng = np.random.default_rng(260911)
        for n in range(1, 6):
            dimension = 1 << n
            magnitude = rng.uniform(-1.0, 1.0, size=dimension - 1)
            phase = rng.uniform(-2.0, 2.0, size=dimension)
            observable = random_hermitian(rng, dimension)
            residuals = phase_gauge_residual(
                magnitude, phase, observable, shift=0.731
            )
            for residual in residuals.values():
                self.assertLessEqual(residual, 3e-11)

    def test_common_phase_factorization_is_exact(self) -> None:
        rng = np.random.default_rng(260912)
        for n in range(1, 8):
            phase = rng.uniform(-3.0, 3.0, size=1 << n)
            self.assertLessEqual(
                common_phase_factorization_residual(phase), 1e-12
            )
            common, relative = centered_leaf_phases(phase)
            self.assertAlmostEqual(common, float(phase[0]))
            self.assertAlmostEqual(float(relative[0]), 0.0)
            np.testing.assert_allclose(
                relative + common, phase, atol=1e-12, rtol=0.0
            )

    def test_zero_amplitude_leaves_have_zero_phase_differential(self) -> None:
        magnitude = np.asarray([0.0, 0.43, 0.71])
        phase = np.asarray([0.2, -0.3, 0.7, -1.1])
        observable = np.asarray(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, -1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, 1.0, 0.0],
            ],
            dtype=complex,
        )
        zero_leaves, derivative_residual, gradient_residual = (
            zero_amplitude_phase_residual(
                magnitude, phase, observable
            )
        )
        self.assertEqual(zero_leaves, (2, 3))
        self.assertLessEqual(derivative_residual, 1e-12)
        self.assertLessEqual(gradient_residual, 1e-12)
        self.assertAlmostEqual(
            float(
                np.sum(
                    complex_phase_gradient(
                        magnitude, phase, observable
                    )
                )
            ),
            0.0,
            places=12,
        )
        self.assertEqual(
            complex_magnitude_gradient(
                magnitude, phase, observable
            ).shape,
            (3,),
        )


if __name__ == "__main__":
    unittest.main()
