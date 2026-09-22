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
from compiler_robust_hopf.decoders import (
    decode_balanced_magnitude_samples_recordwise,
    decode_phase_gradient,
)
from compiler_robust_hopf.complex_analysis import (
    complex_magnitude_gradient,
    complex_phase_gradient,
)
from compiler_robust_hopf.frames import (
    complex_magnitude_frame_matrix,
    real_frame_matrix,
    real_tree_data,
)


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


def _phase_protocol_state(
    frame_circuit: np.ndarray,
    observable: np.ndarray,
    *,
    controlled_phase_error: float = 0.0,
) -> np.ndarray:
    # Direct phase stream: no inverse frame. Retain clean work and reference.
    initial = np.zeros(8, dtype=complex)
    initial[0] = 1.0
    prepared = np.kron(frame_circuit @ initial, _dirty_reference())
    response = np.kron(observable, np.eye(8)) @ prepared
    response *= np.exp(1j * controlled_phase_error)
    return np.concatenate((prepared, response)) / np.sqrt(2.0)


def _phase_measurement_distribution(state: np.ndarray) -> np.ndarray:
    # H S-dagger measures Y; the system is measured in its original basis.
    y_readout = np.array([[1.0, -1j], [1.0, 1j]]) / np.sqrt(2.0)
    amplitudes = (np.kron(y_readout, np.eye(32)) @ state).reshape(
        2, 4, 2, 2, 2
    )
    return (np.abs(amplitudes) ** 2).sum(axis=(2, 3, 4)).reshape(-1)


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

    def test_complex_phase_stream_full_output_and_vector_bias(self):
        phases = np.array([0.2, -0.8, 0.5, 1.1])
        frame = complex_magnitude_frame_matrix(self.theta, phases)
        ideal = np.kron(frame, np.eye(2))
        actual = _leaky_compiler(frame, 0.081)
        eta = np.linalg.norm(
            actual @ self.embedding - self.embedding @ frame, ord=2
        )
        phase_error = -0.067
        eta_o = abs(np.exp(1j * phase_error) - 1)
        ideal_state = _phase_protocol_state(ideal, self.observable)
        actual_state = _phase_protocol_state(
            actual, self.observable, controlled_phase_error=phase_error
        )
        self.assertLessEqual(
            np.linalg.norm(actual_state - ideal_state), eta + eta_o + ATOL
        )
        # Work leakage remains coherent through the measurement.
        self.assertGreater(
            np.linalg.norm(actual_state.reshape(2, 4, 2, 2, 2)[:, :, 1]), 0.01
        )
        exact = complex_phase_gradient(self.theta, phases, self.observable)
        decoded = decode_phase_gradient(
            _phase_measurement_distribution(ideal_state)
        )
        np.testing.assert_allclose(decoded, exact, atol=ATOL)
        approximate = decode_phase_gradient(
            _phase_measurement_distribution(actual_state)
        )
        bias = np.linalg.norm(approximate - exact)
        self.assertGreater(bias, 1e-4)
        self.assertLessEqual(bias, 4 * (eta + eta_o) + ATOL)
        # The sign is independently checked against the analytic phase derivative.
        self.assertGreater(np.linalg.norm(decoded + exact), 0.1)
        dirty = _dirty_reference()
        np.testing.assert_allclose(
            _reference_density(actual_state), np.outer(dirty, dirty.conj()),
            atol=ATOL,
        )

    def test_term_sampled_complex_gradient_means(self):
        phases = np.array([0.2, -0.8, 0.5, 1.1])
        frame = complex_magnitude_frame_matrix(self.theta, phases)
        circuit = np.kron(frame, np.eye(2))
        terms = [self.observable, np.diag([1.0, -1.0, 1.0, -1.0])]
        coefficients = np.array([1.25, -0.75])
        scale = np.sum(np.abs(coefficients))
        probabilities = np.abs(coefficients) / scale
        magnitude_mean, phase_mean = np.zeros(3), np.zeros(4)
        for probability, coefficient, term in zip(
            probabilities, coefficients, terms, strict=True
        ):
            factor = probability * scale * np.sign(coefficient)
            magnitude_mean += factor * decode_balanced_magnitude_gradient(
                _measurement_distribution(_protocol_state(circuit, term)),
                self.data.incoming_amplitude, 2,
            )
            phase_mean += factor * decode_phase_gradient(
                _phase_measurement_distribution(_phase_protocol_state(circuit, term))
            )
        hamiltonian = sum(c * term for c, term in zip(coefficients, terms))
        np.testing.assert_allclose(
            magnitude_mean,
            complex_magnitude_gradient(self.theta, phases, hamiltonian),
            atol=ATOL,
        )
        np.testing.assert_allclose(
            phase_mean, complex_phase_gradient(self.theta, phases, hamiltonian),
            atol=ATOL,
        )

    def test_rounded_weights_change_every_empirical_mean_by_at_most_budget(self):
        scale, tau = 2.0, 0.003
        exact_weights = self.data.incoming_amplitude
        rounded_weights = exact_weights + tau * np.array([1.0, -1.0, 0.4])
        # Incorporate negative term signs into the decoded branch sign.
        branch = np.array([0, 1, 1, 0, 1])
        negative_term = np.array([1, 0, 1, 0, 0])
        signed_branch = branch ^ negative_term
        outcomes = np.array([0, 1, 3, 2, 1])
        exact = scale * decode_balanced_magnitude_samples_recordwise(
            signed_branch, outcomes, exact_weights, 2
        )
        rounded = scale * decode_balanced_magnitude_samples_recordwise(
            signed_branch, outcomes, rounded_weights, 2
        )
        self.assertGreater(np.max(np.abs(rounded - exact)), 1e-4)
        self.assertLessEqual(np.max(np.abs(rounded - exact)), 2 * scale * tau + ATOL)
        # A deterministic record saturates the bound for a maximal weight error.
        exact_single = scale * decode_balanced_magnitude_samples_recordwise(
            [0], [0], exact_weights, 2
        )
        rounded_single = scale * decode_balanced_magnitude_samples_recordwise(
            [0], [0], rounded_weights, 2
        )
        self.assertAlmostEqual(
            np.max(np.abs(rounded_single - exact_single)), 2 * scale * tau,
            places=12,
        )

    def test_reused_dirty_bank_changes_shot_law_but_preserves_conditional_bias(self):
        # One system and one dirty bit. Idle initialized flags can be tensored
        # onto this complete-isometry fixture. The system is initialized anew
        # for each execution, while the dirty bit is actually retained.
        theta, phases = [0.43], [0.2, -0.6]
        frame = complex_magnitude_frame_matrix(theta, phases)
        x = np.array([[0, 1], [1, 0]], dtype=complex)
        y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        z = np.diag([1.0, -1.0])
        observable = (0.31 * x + 0.47 * y + 0.8 * z) / np.linalg.norm(
            [0.31, 0.47, 0.8]
        )
        angle = 0.16
        actual = (
            np.cos(angle) * np.eye(4) - 1j * np.sin(angle) * np.kron(x, z)
        ) @ np.kron(frame, np.eye(2))
        eta = np.linalg.norm(actual - np.kron(frame, np.eye(2)), ord=2)
        system_zero = np.vstack([np.eye(2), np.zeros((2, 2))])
        prepared = actual @ system_zero
        response = np.kron(observable, np.eye(2)) @ prepared
        # Exact measurement instrument on the retained dirty bit, Y then Z.
        instruments = [
            (prepared[2 * leaf:2 * leaf + 2]
             - 1j * sign * response[2 * leaf:2 * leaf + 2]) / 2
            for sign in (1, -1) for leaf in range(2)
        ]
        np.testing.assert_allclose(
            sum(k.conj().T @ k for k in instruments), np.eye(2), atol=ATOL
        )
        dirty = np.array([np.sqrt(0.3), np.exp(0.27j) * np.sqrt(0.7)])
        density = np.outer(dirty, dirty.conj())

        def probabilities(rho):
            return np.array([
                np.trace(k @ rho @ k.conj().T).real for k in instruments
            ])

        first = probabilities(density)
        exact_gradient = complex_phase_gradient(theta, phases, observable)
        conditional_law_changes = []
        for instrument, probability in zip(instruments, first, strict=True):
            self.assertGreater(probability, 1e-3)
            updated_dirty = instrument @ density @ instrument.conj().T / probability
            second = probabilities(updated_dirty)
            conditional_law_changes.append(np.max(np.abs(second - first)))
            conditional_mean = decode_phase_gradient(second)
            self.assertLessEqual(
                np.linalg.norm(conditional_mean - exact_gradient),
                4 * eta + ATOL,
            )
            # Conditional centering, the premise of the martingale argument.
            records = np.array([[2, 0], [0, 2], [-2, 0], [0, -2]])
            np.testing.assert_allclose(
                second @ (records - conditional_mean), np.zeros(2), atol=ATOL
            )
            self.assertLessEqual(
                np.max(np.linalg.norm(records - conditional_mean, axis=1)),
                4 + ATOL,
            )
        self.assertGreater(max(conditional_law_changes), 0.02)


if __name__ == "__main__":
    unittest.main()
