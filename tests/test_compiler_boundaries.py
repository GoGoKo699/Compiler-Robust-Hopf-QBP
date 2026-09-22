from __future__ import annotations

import math
import unittest

import numpy as np

from compiler_robust_hopf.compiler_boundaries import (
    active_interface_residual,
    global_protocol_distribution,
    is_hermitian_unitary,
    is_unitary,
    normalized_hadamard,
    two_qubit_checkpoint_interface_safe_example,
    two_qubit_checkpoint_state_column_counterexample,
    two_qubit_global_state_column_counterexample,
)
from compiler_robust_hopf.conventions import marker_label
from compiler_robust_hopf.decoders import decode_balanced_magnitude_gradient
from compiler_robust_hopf.frames import real_frame_matrix, real_tree_data


class CompilerBoundaryTests(unittest.TestCase):
    def test_worst_observable_detects_complex_marker_error_up_to_common_phase(
        self,
    ) -> None:
        example = two_qubit_global_state_column_counterexample()
        frame = example.frame
        state = example.state
        common_phase = np.exp(0.37j)
        mixer = np.diag(np.exp(1.0j * np.asarray([0.0, 0.53, -0.27, 0.81])))
        compiled = common_phase * frame @ mixer
        np.testing.assert_allclose(compiled[:, 0], common_phase * state, atol=1e-12)

        for node in range(1, 4):
            label = marker_label(node, 2)
            difference = compiled[:, label] / common_phase - frame[:, label]
            error = float(np.linalg.norm(difference))
            witness_state = difference / error
            observable = (
                np.outer(witness_state, state.conj())
                + np.outer(state, witness_state.conj())
                + np.eye(4)
                - np.outer(state, state.conj())
                - np.outer(witness_state, witness_state.conj())
            )
            self.assertTrue(is_hermitian_unitary(observable))
            correct = decode_balanced_magnitude_gradient(
                global_protocol_distribution(frame, observable),
                example.sqrt_metric,
                2,
            )
            observed = decode_balanced_magnitude_gradient(
                global_protocol_distribution(compiled, observable),
                example.sqrt_metric,
                2,
            )
            self.assertAlmostEqual(
                abs(observed[node - 1] - correct[node - 1]),
                2 * example.sqrt_metric[node - 1] * error,
            )

    def test_worst_observable_detects_projected_marker_with_workspace_leakage(
        self,
    ) -> None:
        example = two_qubit_global_state_column_counterexample()
        frame, state = example.frame, example.state
        label = marker_label(1, 2)
        angle = 0.71
        mixer = np.eye(8, dtype=complex)
        positions = [2 * label, 2 * label + 1]
        mixer[np.ix_(positions, positions)] = np.asarray(
            [[math.cos(angle), -math.sin(angle)],
             [math.sin(angle), math.cos(angle)]]
        )
        compiled = np.kron(frame, np.eye(2)) @ mixer
        self.assertTrue(is_unitary(compiled))
        clean_state = np.kron(state, np.asarray([1.0, 0.0]))
        np.testing.assert_allclose(compiled[:, 0], clean_state, atol=1e-12)
        projected_marker = compiled[::2, 2 * label]
        difference = projected_marker - frame[:, label]
        projected_error = float(np.linalg.norm(difference))
        witness_state = difference / projected_error
        observable = (
            np.outer(witness_state, state.conj())
            + np.outer(state, witness_state.conj())
            + np.eye(4)
            - np.outer(state, state.conj())
            - np.outer(witness_state, witness_state.conj())
        )
        self.assertTrue(is_hermitian_unitary(observable))

        # Simulate the actual interference circuit, measuring the system and
        # branch flag in X while marginalizing the untouched work qubit.
        branch_zero = compiled.conj().T @ clean_state
        branch_one = compiled.conj().T @ np.kron(observable, np.eye(2)) @ clean_state
        joint = np.concatenate([branch_zero, branch_one]) / math.sqrt(2.0)
        basis_change = np.kron(normalized_hadamard(3), np.eye(2))
        probabilities = (np.abs(basis_change @ joint) ** 2).reshape(2, 4, 2)
        marginal = probabilities.sum(axis=2).reshape(-1)
        observed = decode_balanced_magnitude_gradient(marginal, example.sqrt_metric, 2)
        correct = decode_balanced_magnitude_gradient(
            global_protocol_distribution(frame, observable), example.sqrt_metric, 2
        )
        self.assertAlmostEqual(
            abs(observed[0] - correct[0]), 2 * projected_error
        )
        full_error = float(np.linalg.norm(
            compiled[:, 2 * label] - np.kron(frame[:, label], [1.0, 0.0])
        ))
        self.assertGreater(full_error, projected_error)
        self.assertAlmostEqual(full_error ** 2, 2 * projected_error)

    def test_singular_raw_gradient_does_not_identify_its_marker_column(self) -> None:
        theta = np.asarray([0.0, 0.4, 0.7])
        frame = real_frame_matrix(theta)
        incoming = real_tree_data(theta).incoming_amplitude
        self.assertEqual(incoming[2], 0.0)
        mixer = np.eye(4, dtype=complex)
        mixer[marker_label(3, 2), marker_label(3, 2)] = 1.0j
        compiled = frame @ mixer
        self.assertGreater(float(np.linalg.norm(compiled - frame)), 1.0)
        paulis = (
            np.eye(2),
            np.asarray([[0.0, 1.0], [1.0, 0.0]]),
            np.asarray([[0.0, -1.0j], [1.0j, 0.0]]),
            np.diag([1.0, -1.0]),
        )
        for first in paulis:
            for second in paulis:
                observable = np.kron(first, second)
                correct = decode_balanced_magnitude_gradient(
                    global_protocol_distribution(frame, observable), incoming, 2
                )
                observed = decode_balanced_magnitude_gradient(
                    global_protocol_distribution(compiled, observable), incoming, 2
                )
                np.testing.assert_allclose(observed, correct, atol=1e-12, rtol=0.0)

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
