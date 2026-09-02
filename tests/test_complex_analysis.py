from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.complex_analysis import (
    common_phase_frame_residual,
    complex_magnitude_derivatives,
    complex_magnitude_gradient,
    complex_phase_derivatives,
    complex_phase_gradient,
    complex_state,
    diagonal_parameter_residual,
    diagonal_parity_angles,
    expectation,
    phase_gauge_residual,
    reconstruct_relative_phases,
    split_common_phase,
)
from compiler_robust_hopf.conventions import marker_label, parity
from compiler_robust_hopf.frames import (
    complex_frame_matrix,
    phase_layer_matrix,
    real_tree_data,
)


class ComplexAnalysisTests(unittest.TestCase):
    def test_frame_contains_state_and_weighted_magnitude_tangents(self) -> None:
        rng = np.random.default_rng(260906)
        for n in range(1, 6):
            N = 1 << n
            theta = rng.uniform(-1.1, 1.1, size=N - 1)
            phase = rng.uniform(-2.0, 2.0, size=N)
            data = real_tree_data(theta)
            state = complex_state(theta, phase)
            frame = complex_frame_matrix(theta, phase)
            derivatives = complex_magnitude_derivatives(theta, phase)
            np.testing.assert_allclose(frame[:, 0], state, atol=1e-12, rtol=0.0)
            for node, derivative in enumerate(derivatives, start=1):
                marker = marker_label(node, n)
                np.testing.assert_allclose(
                    derivative,
                    data.sqrt_metric[node - 1] * frame[:, marker],
                    atol=1e-12,
                    rtol=0.0,
                )

    def test_common_phase_is_a_projective_gauge(self) -> None:
        rng = np.random.default_rng(260907)
        for n in range(1, 6):
            N = 1 << n
            theta = rng.uniform(-0.8, 0.8, size=N - 1)
            phase = rng.uniform(-2.0, 2.0, size=N)
            shift = float(rng.uniform(-1.7, 1.7))
            self.assertLessEqual(
                common_phase_frame_residual(theta, phase, shift), 1e-12
            )
            np.testing.assert_allclose(
                complex_state(theta, phase + shift),
                np.exp(1j * shift) * complex_state(theta, phase),
                atol=1e-12,
                rtol=0.0,
            )

            raw = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
            observable = raw + raw.conj().T
            self.assertAlmostEqual(
                expectation(
                    complex_state(theta, phase + shift), observable
                ),
                expectation(complex_state(theta, phase), observable),
                places=10,
            )
            np.testing.assert_allclose(
                complex_magnitude_gradient(theta, phase + shift, observable),
                complex_magnitude_gradient(theta, phase, observable),
                atol=1e-10,
                rtol=0.0,
            )
            np.testing.assert_allclose(
                complex_phase_gradient(theta, phase + shift, observable),
                complex_phase_gradient(theta, phase, observable),
                atol=1e-10,
                rtol=0.0,
            )
            self.assertLessEqual(
                phase_gauge_residual(theta, phase, observable), 1e-10
            )

    def test_common_phase_factorization_is_exact(self) -> None:
        rng = np.random.default_rng(260908)
        for n in range(1, 7):
            phase = rng.uniform(-3.0, 3.0, size=1 << n)
            common, relative = split_common_phase(phase)
            self.assertAlmostEqual(relative[0], 0.0)
            np.testing.assert_allclose(
                phase_layer_matrix(phase),
                np.exp(1j * common) * phase_layer_matrix(relative),
                atol=1e-12,
                rtol=0.0,
            )

    def test_parity_phase_parameter_transform(self) -> None:
        rng = np.random.default_rng(260912)
        for n in range(1, 9):
            N = 1 << n
            phase = rng.uniform(-4.0, 4.0, size=N)
            common, alpha = diagonal_parity_angles(phase)
            self.assertEqual(alpha[0], 0.0)
            reconstructed = common + reconstruct_relative_phases(alpha)
            np.testing.assert_allclose(
                reconstructed, phase, atol=2e-12, rtol=0.0
            )
            self.assertLessEqual(diagonal_parameter_residual(phase), 2e-12)
            for leaf in range(N):
                direct = common + sum(
                    alpha[label] * parity(label, leaf)
                    for label in range(1, N)
                )
                self.assertAlmostEqual(direct, phase[leaf], places=10)

    def test_zero_amplitude_leaves_have_zero_phase_differential(self) -> None:
        rng = np.random.default_rng(260909)
        n = 3
        N = 1 << n
        theta = rng.uniform(-0.9, 0.9, size=N - 1)
        theta[0] = 0.0
        phase = rng.uniform(-2.0, 2.0, size=N)
        state = complex_state(theta, phase)
        derivatives = complex_phase_derivatives(theta, phase)
        raw = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
        observable = raw + raw.conj().T
        gradient = complex_phase_gradient(theta, phase, observable)
        for leaf in range(N // 2, N):
            self.assertEqual(state[leaf], 0.0)
            np.testing.assert_array_equal(derivatives[leaf], 0.0)
            self.assertEqual(gradient[leaf], 0.0)
        frame = complex_frame_matrix(theta, phase)
        np.testing.assert_allclose(
            frame.conj().T @ frame,
            np.eye(N),
            atol=1e-12,
            rtol=0.0,
        )


if __name__ == "__main__":
    unittest.main()
