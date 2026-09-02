"""Complex Hopf states, derivatives, gradients, gauge, and phase synthesis.

These routines are independent NumPy references. They support the exact
logical and geometric checks needed by the common-workspace complex-frame
theorem; they do not implement a particular elementary gate compiler.
"""
from __future__ import annotations

import numpy as np

from .decoders import fwht
from .frames import RealTreeData, complex_frame_matrix, real_tree_data


def _phase_for_data(theta_ph: object, data: RealTreeData) -> np.ndarray:
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size != 1 << data.n:
        raise ValueError("theta_ph must contain one phase for every Hopf leaf.")
    return phase


def complex_state(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Return the separated complex Hopf state ``D_ph |psi_R>``."""

    data = real_tree_data(theta_mag)
    phase = _phase_for_data(theta_ph, data)
    return np.exp(1j * phase) * data.state


def complex_magnitude_derivatives(
    theta_mag: object, theta_ph: object
) -> tuple[np.ndarray, ...]:
    """Return derivatives with respect to all real-tree magnitude angles."""

    data = real_tree_data(theta_mag)
    phase = np.exp(1j * _phase_for_data(theta_ph, data))
    return tuple(phase * derivative for derivative in data.derivatives)


def complex_phase_derivatives(
    theta_mag: object, theta_ph: object
) -> tuple[np.ndarray, ...]:
    """Return ``partial_{phi_l}|psi> = i psi_l |l>`` for every leaf."""

    state = complex_state(theta_mag, theta_ph)
    derivatives: list[np.ndarray] = []
    for leaf, amplitude in enumerate(state):
        derivative = np.zeros(state.size, dtype=complex)
        derivative[leaf] = 1j * amplitude
        derivatives.append(derivative)
    return tuple(derivatives)


def expectation(state: object, observable: object) -> float:
    """Return the real expectation value of a Hermitian observable."""

    vector = np.asarray(state, dtype=complex).reshape(-1)
    matrix = np.asarray(observable, dtype=complex)
    if matrix.shape != (vector.size, vector.size):
        raise ValueError("observable shape does not match the state dimension.")
    return float(np.real(np.vdot(vector, matrix @ vector)))


def coordinate_gradient(
    state: object,
    derivatives: tuple[np.ndarray, ...],
    observable: object,
) -> np.ndarray:
    """Return ``2 Re <partial_j psi|O|psi>`` for supplied derivatives."""

    vector = np.asarray(state, dtype=complex).reshape(-1)
    matrix = np.asarray(observable, dtype=complex)
    if matrix.shape != (vector.size, vector.size):
        raise ValueError("observable shape does not match the state dimension.")
    response = matrix @ vector
    output: list[float] = []
    for derivative in derivatives:
        tangent = np.asarray(derivative, dtype=complex).reshape(-1)
        if tangent.size != vector.size:
            raise ValueError("derivative dimension does not match the state.")
        output.append(2.0 * float(np.real(np.vdot(tangent, response))))
    return np.asarray(output, dtype=float)


def complex_magnitude_gradient(
    theta_mag: object, theta_ph: object, observable: object
) -> np.ndarray:
    state = complex_state(theta_mag, theta_ph)
    return coordinate_gradient(
        state,
        complex_magnitude_derivatives(theta_mag, theta_ph),
        observable,
    )


def complex_phase_gradient(
    theta_mag: object, theta_ph: object, observable: object
) -> np.ndarray:
    state = complex_state(theta_mag, theta_ph)
    return coordinate_gradient(
        state,
        complex_phase_derivatives(theta_mag, theta_ph),
        observable,
    )


def split_common_phase(theta_ph: object) -> tuple[float, np.ndarray]:
    """Split leaf phases into one common phase and a zero-at-leaf-zero remainder."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size == 0 or phase.size & (phase.size - 1):
        raise ValueError("theta_ph length must be a positive power of two.")
    common = float(phase[0])
    return common, phase - common


def diagonal_parity_angles(theta_ph: object) -> tuple[float, np.ndarray]:
    """Return exact parity-phase synthesis parameters in ``O(N log N)`` work.

    With ``p_s(x) = <s,x> mod 2``, the returned vector has ``alpha[0] = 0`` and

    ``theta_ph[x] = common + sum_s alpha[s] * p_s(x)``.

    This is the parameter transform used by Walsh/Gray-code diagonal synthesis.
    """

    common, relative = split_common_phase(theta_ph)
    N = relative.size
    spectrum = fwht(relative)
    alpha = np.zeros(N, dtype=float)
    alpha[1:] = (-2.0 / N) * spectrum[1:]
    return common, alpha


def reconstruct_relative_phases(alpha: object) -> np.ndarray:
    """Reconstruct ``sum_s alpha_s p_s(x)`` by one Walsh transform."""

    values = np.asarray(alpha, dtype=float).reshape(-1)
    if values.size == 0 or values.size & (values.size - 1):
        raise ValueError("alpha length must be a positive power of two.")
    if abs(float(values[0])) > 1e-12:
        raise ValueError("alpha[0] must vanish for parity-phase synthesis.")
    return 0.5 * (float(np.sum(values)) - fwht(values))


def diagonal_parameter_residual(theta_ph: object) -> float:
    """Return the maximum reconstruction residual of the parity-angle transform."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    common, alpha = diagonal_parity_angles(phase)
    reconstructed = common + reconstruct_relative_phases(alpha)
    return float(np.max(np.abs(reconstructed - phase)))


def common_phase_frame_residual(
    theta_mag: object, theta_ph: object, shift: float
) -> float:
    """Check ``W_C(phi + shift*1) = exp(i*shift) W_C(phi)``."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    before = complex_frame_matrix(theta_mag, phase)
    after = complex_frame_matrix(theta_mag, phase + float(shift))
    return float(np.max(np.abs(after - np.exp(1j * float(shift)) * before)))


def phase_gauge_residual(
    theta_mag: object, theta_ph: object, observable: object
) -> float:
    """Return ``abs(sum_l partial E / partial phi_l)``."""

    return float(
        abs(np.sum(complex_phase_gradient(theta_mag, theta_ph, observable)))
    )
