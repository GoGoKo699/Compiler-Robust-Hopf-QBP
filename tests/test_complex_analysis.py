from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.complex_analysis import (
    centered_leaf_phases,
    common_phase_factorization_residual,
    complex_chart_data,
    complex_full_gradient,
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
        rng = np.random.default_rng(260915)
        for n in range(1, 6):
            dimension = 1 << n
            theta = rng.uniform(-1.1, 1.1, size=dimension - 1)
            phases = rng.uniform(-1.5, 1.5, size=dimension)
            real = real_tree_data(theta)
            data = complex_chart_data(theta, phases)
            frame = complex_frame_matrix(theta, phases)
            np.testing.assert_allclose(
                frame[:, 0], data.state, atol=1e-12, rtol=0.0
            )
            for node, derivative in enumerate(
                data.magnitude_derivatives, start=1
            ):
                marker = marker_label(node, n)
                np.testing.assert_allclose(
                    derivative,
                    real.sqrt_metric[node - 1] * frame[:, marker],
                    atol=1e-12,
                    rtol=0.0,
                )

    def test_common_phase_is_a_projective_gauge(self) -> None:
        rng = np.random.default_rng(260916)
        for n in range(1, 6):
            dimension = 1 << n
            theta = rng.uniform(-1.0, 1.0, size=dimension - 1)
            phases = rng.uniform(-2.0, 2.0, size=dimension)
            observable = random_hermitian(rng, dimension)
            residuals = phase_gauge_residual(
                theta, phases, observable, shift=0.731
            )
            for residual in residuals.values():
                self.assertLessEqual(residual, 3e-11)

    def test_common_phase_factorization_is_exact(self) -> None:
        rng = np.random.default_rng(260917)
        for n in range(1, 9):
            phases = rng.uniform(-3.0, 3.0, size=1 << n)
            self.assertLessEqual(
                common_phase_factorization_residual(phases), 1e-12
            )
            common, relative = centered_leaf_phases(phases)
            self.assertAlmostEqual(common, float(phases[0]))
            self.assertAlmostEqual(float(relative[0]), 0.0)
            np.testing.assert_allclose(
                relative + common, phases, atol=1e-12, rtol=0.0
            )

    def test_zero_amplitude_leaves_have_zero_phase_differential(self) -> None:
        theta = np.asarray([0.0, 0.43, 0.71])
        phases = np.asarray([0.2, -0.3, 0.7, -1.1])
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
            zero_amplitude_phase_residual(theta, phases, observable)
        )
        self.assertEqual(zero_leaves, (2, 3))
        self.assertLessEqual(derivative_residual, 1e-12)
        self.assertLessEqual(gradient_residual, 1e-12)
        phase_gradient = complex_phase_gradient(theta, phases, observable)
        self.assertAlmostEqual(float(np.sum(phase_gradient)), 0.0, places=12)
        magnitude_gradient = complex_magnitude_gradient(
            theta, phases, observable
        )
        self.assertEqual(magnitude_gradient.shape, (3,))
        self.assertEqual(
            complex_full_gradient(theta, phases, observable).shape,
            (7,),
        )


if __name__ == "__main__":
    unittest.main()
