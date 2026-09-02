from __future__ import annotations

import math
import unittest

import numpy as np

from compiler_robust_hopf.compiler_boundaries import (
    active_interface_residual,
    is_hermitian_unitary,
    is_unitary,
    two_qubit_checkpoint_interface_safe_example,
    two_qubit_checkpoint_state_column_counterexample,
    two_qubit_global_state_column_counterexample,
)


class CompilerBoundaryTests(unittest.TestCase):
    def test_global_state_column_equality_does_not_preserve_gradient(self) -> None:
        example = two_qubit_global_state_column_counterexample()
        zero = np.asarray([1.0, 0.0, 0.0, 0.0], dtype=complex)

        self.assertTrue(is_unitary(example.frame))
        self.assertTrue(is_unitary(example.mixer))
        self.assertTrue(is_unitary(example.compiled_frame))
        self.assertTrue(is_hermitian_unitary(example.observable))
        np.testing.assert_allclose(example.mixer @ zero, zero, atol=1e-12, rtol=0.0)
        np.testing.assert_allclose(
            example.frame @ zero,
            example.compiled_frame @ zero,
            atol=1e-12,
            rtol=0.0,
        )
        self.assertGreater(
            float(np.max(np.abs(example.frame - example.compiled_frame))), 0.5
        )

        response = example.observable @ example.state
        np.testing.assert_allclose(
            example.frame.conj().T @ response,
            np.asarray([0.0, 0.0, 1.0, 0.0], dtype=complex),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.compiled_frame.conj().T @ response,
            np.asarray([0.0, 1.0, 0.0, 0.0], dtype=complex),
            atol=1e-12,
            rtol=0.0,
        )

        np.testing.assert_allclose(
            example.correct_distribution,
            np.asarray([0.25, 0.25, 0.0, 0.0, 0.0, 0.0, 0.25, 0.25]),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.compiled_distribution,
            np.asarray([0.25, 0.0, 0.25, 0.0, 0.0, 0.25, 0.0, 0.25]),
            atol=1e-12,
            rtol=0.0,
        )
        self.assertAlmostEqual(
            0.5
            * float(
                np.sum(
                    np.abs(
                        example.correct_distribution
                        - example.compiled_distribution
                    )
                )
            ),
            0.5,
        )
        np.testing.assert_allclose(
            example.analytic_gradient,
            np.asarray([2.0, 0.0, 0.0]),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.correct_decoded_gradient,
            example.analytic_gradient,
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.compiled_decoded_gradient,
            np.asarray([0.0, math.sqrt(2.0), 0.0]),
            atol=1e-12,
            rtol=0.0,
        )

    def test_checkpoint_state_column_equality_can_flip_gradient_sign(self) -> None:
        example = two_qubit_checkpoint_state_column_counterexample()

        self.assertTrue(is_unitary(example.prefix))
        self.assertTrue(is_unitary(example.reference_suffix))
        self.assertTrue(is_unitary(example.interface_mixer))
        self.assertTrue(is_unitary(example.compiled_suffix))
        self.assertTrue(is_hermitian_unitary(example.observable))
        np.testing.assert_allclose(
            example.reference_suffix @ example.prefix_state,
            example.compiled_suffix @ example.prefix_state,
            atol=1e-12,
            rtol=0.0,
        )
        self.assertGreater(
            active_interface_residual(
                example.reference_suffix,
                example.compiled_suffix,
                example.interface_projector,
            ),
            0.5,
        )

        np.testing.assert_allclose(
            example.correct_distribution,
            np.asarray([0.0, 0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0]),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.compiled_distribution,
            np.asarray([0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0]),
            atol=1e-12,
            rtol=0.0,
        )
        self.assertAlmostEqual(example.analytic_depth_gradient, 2.0)
        np.testing.assert_allclose(
            example.correct_decoded_gradient,
            np.asarray([2.0]),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.compiled_decoded_gradient,
            np.asarray([-2.0]),
            atol=1e-12,
            rtol=0.0,
        )

    def test_active_interface_equality_preserves_mean_not_distribution(self) -> None:
        example = two_qubit_checkpoint_interface_safe_example()

        self.assertTrue(is_unitary(example.reference_suffix))
        self.assertTrue(is_unitary(example.off_interface_mixer))
        self.assertTrue(is_unitary(example.compiled_suffix))
        self.assertTrue(is_hermitian_unitary(example.observable))
        self.assertLessEqual(
            active_interface_residual(
                example.reference_suffix,
                example.compiled_suffix,
                example.interface_projector,
            ),
            1e-12,
        )
        np.testing.assert_allclose(
            example.reference_suffix @ example.prefix_state,
            example.compiled_suffix @ example.prefix_state,
            atol=1e-12,
            rtol=0.0,
        )
        self.assertGreater(
            float(
                np.max(
                    np.abs(example.reference_suffix - example.compiled_suffix)
                )
            ),
            0.5,
        )
        self.assertAlmostEqual(example.total_variation_distance, 0.25)
        np.testing.assert_allclose(
            example.correct_distribution,
            np.full(8, 0.125),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.compiled_distribution,
            np.asarray([0.125, 0.0, 0.125, 0.25, 0.125, 0.0, 0.125, 0.25]),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.correct_decoded_gradient,
            np.asarray([0.0]),
            atol=1e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            example.compiled_decoded_gradient,
            example.correct_decoded_gradient,
            atol=1e-12,
            rtol=0.0,
        )


if __name__ == "__main__":
    unittest.main()
