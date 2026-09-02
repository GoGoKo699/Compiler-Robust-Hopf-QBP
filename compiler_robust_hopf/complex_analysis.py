"""Complex Hopf-chart geometry independent of any elementary compiler.

The active compiler represents the leaf-phase diagonal as one uniformly
controlled gate. This module therefore contains only chart identities,
derivatives, gauge checks, and objective gradients; compiler-parameter
transforms live in :mod:`compiler_robust_hopf.unified_compiler`.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .frames import complex_frame_matrix, phase_layer_matrix, real_tree_data


@dataclass(frozen=True)
class ComplexChartData:
    """State and coordinate derivatives of the separated complex Hopf chart."""

    state: np.ndarray
    magnitude_derivatives: tuple[np.ndarray, ...]
    phase_derivatives: tuple[np.ndarray, ...]
    phase_gradient_null_direction: np.ndarray


def _phase_vector(theta_ph: object, dimension: int) -> np.ndarray:
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size != dimension:
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return phase


def complex_state(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Return the complex Hopf state ``D_ph |psi_R>``."""

    real = real_tree_data(theta_mag)
    phase = _phase_vector(theta_ph, real.state.size)
    return np.exp(1j * phase) * real.state


def complex_chart_data(theta_mag: object, theta_ph: object) -> ComplexChartData:
    """Return complex magnitude and phase derivatives without finite differences."""

    real = real_tree_data(theta_mag)
    phase = _phase_vector(theta_ph, real.state.size)
    phase_factors = np.exp(1j * phase)
    state = phase_factors * real.state
    magnitude = tuple(
        phase_factors * derivative for derivative in real.derivatives
    )

    phase_derivatives: list[np.ndarray] = []
    for leaf in range(state.size):
        derivative = np.zeros(state.size, dtype=complex)
        derivative[leaf] = 1j * state[leaf]
        phase_derivatives.append(derivative)

    return ComplexChartData(
        state=state,
        magnitude_derivatives=magnitude,
        phase_derivatives=tuple(phase_derivatives),
        phase_gradient_null_direction=np.ones(state.size, dtype=float),
    )


def expectation(state: object, observable: object) -> float:
    """Return the real expectation of a Hermitian observable."""

    psi = np.asarray(state, dtype=complex).reshape(-1)
    operator = np.asarray(observable, dtype=complex)
    if operator.shape != (psi.size, psi.size):
        raise ValueError("observable dimension does not match the state.")
    return float(np.real(np.vdot(psi, operator @ psi)))


def _coordinate_gradient(
    state: np.ndarray,
    derivatives: tuple[np.ndarray, ...],
    observable: object,
) -> np.ndarray:
    operator = np.asarray(observable, dtype=complex)
    if operator.shape != (state.size, state.size):
        raise ValueError("observable dimension does not match the state.")
    response = operator @ state
    return np.asarray(
        [2.0 * np.real(np.vdot(derivative, response)) for derivative in derivatives],
        dtype=float,
    )


def complex_magnitude_gradient(
    theta_mag: object,
    theta_ph: object,
    observable: object,
) -> np.ndarray:
    """Return all magnitude-coordinate derivatives."""

    data = complex_chart_data(theta_mag, theta_ph)
    return _coordinate_gradient(
        data.state, data.magnitude_derivatives, observable
    )


def complex_phase_gradient(
    theta_mag: object,
    theta_ph: object,
    observable: object,
) -> np.ndarray:
    """Return all leaf-phase derivatives."""

    data = complex_chart_data(theta_mag, theta_ph)
    return _coordinate_gradient(data.state, data.phase_derivatives, observable)


def complex_full_gradient(
    theta_mag: object,
    theta_ph: object,
    observable: object,
) -> np.ndarray:
    """Return magnitude derivatives followed by leaf-phase derivatives."""

    return np.concatenate(
        (
            complex_magnitude_gradient(theta_mag, theta_ph, observable),
            complex_phase_gradient(theta_mag, theta_ph, observable),
        )
    )


def centered_leaf_phases(theta_ph: object) -> tuple[float, np.ndarray]:
    """Separate one common phase from the relative leaf phases.

    This is a geometric gauge decomposition, not the active diagonal-compiler
    parameterization. The active compiler stores the original phase pairs
    directly as one uniformly controlled gate.
    """

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size == 0 or phase.size & (phase.size - 1):
        raise ValueError("theta_ph length must be a positive power of two.")
    common = float(phase[0])
    return common, phase - common


def common_phase_shifted(theta_ph: object, shift: float) -> np.ndarray:
    """Return the leaf phases after one common projective shift."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    return phase + float(shift)


def phase_gauge_residual(
    theta_mag: object,
    theta_ph: object,
    observable: object,
    *,
    shift: float,
) -> dict[str, float]:
    """Return state/frame/objective/gradient residuals under a common phase."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    shifted = common_phase_shifted(phase, shift)
    state = complex_state(theta_mag, phase)
    shifted_state = complex_state(theta_mag, shifted)
    frame = complex_frame_matrix(theta_mag, phase)
    shifted_frame = complex_frame_matrix(theta_mag, shifted)
    magnitude = complex_magnitude_gradient(theta_mag, phase, observable)
    shifted_magnitude = complex_magnitude_gradient(theta_mag, shifted, observable)
    phase_gradient = complex_phase_gradient(theta_mag, phase, observable)
    shifted_phase_gradient = complex_phase_gradient(
        theta_mag, shifted, observable
    )
    return {
        "state": float(
            np.max(np.abs(shifted_state - np.exp(1j * shift) * state))
        ),
        "frame": float(
            np.max(np.abs(shifted_frame - np.exp(1j * shift) * frame))
        ),
        "expectation": abs(
            expectation(state, observable)
            - expectation(shifted_state, observable)
        ),
        "magnitude_gradient": float(
            np.max(np.abs(magnitude - shifted_magnitude))
        ),
        "phase_gradient": float(
            np.max(np.abs(phase_gradient - shifted_phase_gradient))
        ),
        "phase_gradient_sum": abs(float(np.sum(phase_gradient))),
    }


def common_phase_factorization_residual(theta_ph: object) -> float:
    """Check ``D_ph = exp(i phi_0) D_(phi-phi_0)`` exactly."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    common, relative = centered_leaf_phases(phase)
    direct = phase_layer_matrix(phase)
    factored = np.exp(1j * common) * phase_layer_matrix(relative)
    return float(np.max(np.abs(direct - factored)))


def zero_amplitude_phase_residual(
    theta_mag: object,
    theta_ph: object,
    observable: object,
    *,
    atol: float = 1e-12,
) -> tuple[tuple[int, ...], float, float]:
    """Check phase differentials and gradients at exactly zero-amplitude leaves."""

    data = complex_chart_data(theta_mag, theta_ph)
    gradient = complex_phase_gradient(theta_mag, theta_ph, observable)
    zero_leaves = tuple(
        int(index)
        for index in np.flatnonzero(np.abs(data.state) <= float(atol))
    )
    derivative_residual = max(
        (
            float(np.linalg.norm(data.phase_derivatives[index]))
            for index in zero_leaves
        ),
        default=0.0,
    )
    gradient_residual = max(
        (abs(float(gradient[index])) for index in zero_leaves),
        default=0.0,
    )
    return zero_leaves, derivative_residual, gradient_residual
