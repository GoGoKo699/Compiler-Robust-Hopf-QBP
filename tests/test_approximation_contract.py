"""Full-output approximation checks with adversarial completion and leakage.

Finite floating-point checks support the analytic QBP approximation proof.
They do not estimate circuit complexity or differentiate synthesized words.
"""
from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.compiler_boundaries import (
    normalized_hadamard,
    two_qubit_global_state_column_counterexample,
)
from compiler_robust_hopf.decoders import decode_balanced_magnitude_gradient
from compiler_robust_hopf.frames import real_frame_matrix, real_tree_data


ATOL = 2e-12


def _clean_embedding(dimension: int) -> np.ndarray:
    """One appended clean work bit; source index is the more significant one."""
    embedding = np.zeros((2 * dimension, dimension), dtype=complex)
    embedding[2 * np.arange(dimension), np.arange(dimension)] = 1.0
    return embedding


def _leaky_compiler(frame: np.ndarray, angle: float) -> np.ndarray:
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    generator = np.kron(np.kron(x, np.eye(2)), x)
    unitary_error = np.cos(angle) * np.eye(8) - 1j * np.sin(angle) * generator
    return unitary_error @ np.kron(frame, np.eye(2))


def _observable() -> np.ndarray:
    axis = np.array([1.0, 0.4 + 0.7j, -0.3j, 0.6], dtype=complex)
    axis /= np.linalg.norm(axis)
    return np.eye(4) - 2.0 * np.outer(axis, axis.conj())


def _dirty_reference() -> np.ndarray:
    # A dirty bit entangled with an external reference, not a supplied zero.
    return np.array([np.sqrt(0.3), 0.0, 0.0, np.exp(0.4j) * np.sqrt(0.7)])


def _protocol_state(
    frame_circuit: np.ndarray,
    observable: np.ndarray,
    *,
    controlled_phase_error: float = 0.0,
) -> np.ndarray:
    # Order: branch, system (dimension 4), clean work, dirty bit, reference.
    extension = np.kron(frame_circuit, np.eye(4))
    system_work_zero = np.zeros(8, dtype=complex)
    system_work_zero[0] = 1.0
    initial = np.kron(system_work_zero, _dirty_reference())
    prepared = extension @ initial
    response = np.kron(observable, np.eye(8)) @ prepared
    response *= np.exp(1j * controlled_phase_error)
    return np.concatenate((extension.conj().T @ prepared,
                           extension.conj().T @ response)) / np.sqrt(2.0)


def _measurement_distribution(state: np.ndarray) -> np.ndarray:
    basis_change = np.kron(normalized_hadamard(3), np.eye(8))
    amplitudes = (basis_change @ state).reshape(2, 4, 2, 2, 2)
    return (np.abs(amplitudes) ** 2).sum(axis=(2, 3, 4)).reshape(-1)


def _reference_density(state: np.ndarray) -> np.ndarray:
    # Trace branch, source and frame work; retain the dirty/reference pair.
    amplitudes = state.reshape(16, 4)
    return np.einsum("ai,aj->ij", amplitudes, amplitudes.conj())


class ApproximationContractTests(unittest.TestCase):
    def setUp(self):
        self.theta = np.array([-0.37, -0.61, 0.83])
        self.data = real_tree_data(self.theta)
        self.frame = real_frame_matrix(self.theta).astype(complex)
        self.embedding = _clean_embedding(4)
        self.observable = _observable()

    def test_actual_adjoint_and_reference_entangled_full_output(self):
        angle, oracle_phase = 0.071, 0.043
        actual = _leaky_compiler(self.frame, angle)
        ideal = np.kron(self.frame, np.eye(2))
        np.testing.assert_allclose(actual.conj().T @ actual, np.eye(8), atol=ATOL)
        forward_defect = actual @ self.embedding - self.embedding @ self.frame
        eta = np.linalg.norm(forward_defect, ord=2)
        inverse_defect = actual.conj().T @ self.embedding - self.embedding @ self.frame.conj().T
        identity_rhs = actual.conj().T @ (-forward_defect) @ self.frame.conj().T
        np.testing.assert_allclose(inverse_defect, identity_rhs, atol=ATOL)
        self.assertAlmostEqual(np.linalg.norm(inverse_defect, ord=2), eta, places=12)
        self.assertAlmostEqual(eta, 2.0 * np.sin(angle / 2), places=12)

        ideal_state = _protocol_state(ideal, self.observable)
        frame_only_state = _protocol_state(actual, self.observable)
        actual_state = _protocol_state(actual, self.observable,
                                       controlled_phase_error=oracle_phase)
        eta_o = abs(np.exp(1j * oracle_phase) - 1)
        self.assertLessEqual(np.linalg.norm(frame_only_state - ideal_state), np.sqrt(2) * eta + ATOL)
        self.assertLessEqual(np.linalg.norm(actual_state - ideal_state), np.sqrt(2) * eta + eta_o + ATOL)
        # The cancellation uses the actual adjoint: the entire reference branch agrees.
        np.testing.assert_allclose(frame_only_state[:32], ideal_state[:32], atol=ATOL)
        self.assertGreater(np.linalg.norm(actual_state.reshape(2, 4, 2, 2, 2)[:, :, 1]), 1e-3)
        dirty = _dirty_reference()
        np.testing.assert_allclose(_reference_density(actual_state),
                                   np.outer(dirty, dirty.conj()), atol=ATOL)

        probabilities = _measurement_distribution(actual_state)
        ideal_probabilities = _measurement_distribution(ideal_state)
        self.assertAlmostEqual(float(probabilities.sum()), 1.0, places=12)
        tv = 0.5 * np.abs(probabilities - ideal_probabilities).sum()
        self.assertGreater(tv, 1e-4)
        self.assertLessEqual(tv, np.linalg.norm(actual_state - ideal_state) + ATOL)
        actual_gradient = decode_balanced_magnitude_gradient(
            probabilities, self.data.incoming_amplitude, 2)
        expected_gradient = np.array([
            2 * np.vdot(derivative, self.observable @ self.data.state).real
            for derivative in self.data.derivatives
        ])
        ideal_gradient = decode_balanced_magnitude_gradient(
            ideal_probabilities, self.data.incoming_amplitude, 2)
        np.testing.assert_allclose(ideal_gradient, expected_gradient, atol=ATOL)
        bias = np.abs(actual_gradient - expected_gradient)
        self.assertGreater(float(bias.max()), 1e-4)
        self.assertTrue(np.all(bias <= 4 * np.abs(self.data.incoming_amplitude) * (eta + eta_o) + ATOL))

    def test_projected_block_error_misses_coherent_leakage(self):
        angle = 0.12
        actual = _leaky_compiler(self.frame, angle)
        eta = np.linalg.norm(actual @ self.embedding - self.embedding @ self.frame, ord=2)
        projected_error = np.linalg.norm(
            self.embedding.conj().T @ actual @ self.embedding - self.frame, ord=2)
        self.assertAlmostEqual(projected_error, 1 - np.cos(angle), places=12)
        self.assertGreater(eta, 10 * projected_error)
        ideal = np.kron(self.frame, np.eye(2))
        z_first = np.diag([1.0, 1.0, -1.0, -1.0])
        state_error = np.linalg.norm(_protocol_state(actual, z_first)
                                     - _protocol_state(ideal, z_first))
        # Replacing eta by projected_error would make the advertised full-output bound false.
        self.assertGreater(state_error, np.sqrt(2) * projected_error + 0.05)
        self.assertLessEqual(state_error, np.sqrt(2) * eta + ATOL)

    def test_state_column_agreement_is_not_zero_frame_error(self):
        fixture = two_qubit_global_state_column_counterexample()
        np.testing.assert_allclose(fixture.compiled_frame[:, 0], fixture.frame[:, 0], atol=ATOL)
        self.assertGreater(np.linalg.norm(fixture.compiled_frame - fixture.frame, ord=2), 0.5)
        self.assertGreater(np.linalg.norm(fixture.compiled_decoded_gradient
                                         - fixture.correct_decoded_gradient, ord=np.inf), 0.5)
        # A falsely zero error inferred from the prepared column predicts zero bias.
        column_only_eta = np.linalg.norm(fixture.compiled_frame[:, 0] - fixture.frame[:, 0])
        self.assertGreater(np.linalg.norm(fixture.compiled_decoded_gradient
                                         - fixture.analytic_gradient, ord=np.inf),
                           4 * column_only_eta + 0.5)

    def test_depth_record_bound_survives_an_arbitrary_output_distribution(self):
        # No physical-distribution hypothesis is needed for this deterministic norm.
        for branch in (0, 1):
            for outcome in range(4):
                distribution = np.zeros(8)
                distribution[4 * branch + outcome] = 1.0
                record = decode_balanced_magnitude_gradient(
                    distribution, self.data.incoming_amplitude, 2)
                self.assertAlmostEqual(abs(record[0]), 2.0, places=12)
                self.assertAlmostEqual(np.linalg.norm(record[1:]), 2.0, places=12)
                self.assertLessEqual(float(np.max(np.abs(record))), 2.0 + ATOL)


if __name__ == "__main__":
    unittest.main()
