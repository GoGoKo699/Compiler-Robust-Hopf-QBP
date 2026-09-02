"""Exact counterexamples and interface checks for compiler robustness.

The examples in this module are intentionally two-qubit and Qibo-free. They
separate three logically different promises:

* equality of one prepared state column;
* equality of a checkpoint suffix on its complete active interface; and
* equality of a complete differential-frame unitary.

State-column equality is insufficient for both global-frame and checkpoint
reverse circuits. Checkpoint means require less than full-unitary equality, but
more than one state column: an objective-independent sufficient condition is
isometric equality on the active checkpoint interface.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .decoders import (
    decode_balanced_magnitude_gradient,
    decode_checkpoint_gradient,
)
from .frames import hopf_ry, real_frame_matrix, real_tree_data


@dataclass(frozen=True)
class GlobalStateColumnCounterexample:
    """Complete data for the minimal two-qubit global-frame obstruction."""

    theta: np.ndarray
    frame: np.ndarray
    mixer: np.ndarray
    compiled_frame: np.ndarray
    observable: np.ndarray
    state: np.ndarray
    sqrt_metric: np.ndarray
    analytic_gradient: np.ndarray
    correct_distribution: np.ndarray
    compiled_distribution: np.ndarray
    correct_decoded_gradient: np.ndarray
    compiled_decoded_gradient: np.ndarray


@dataclass(frozen=True)
class CheckpointStateColumnCounterexample:
    """Two-qubit depth-zero checkpoint failure under state-column equality."""

    theta: np.ndarray
    prefix: np.ndarray
    reference_suffix: np.ndarray
    interface_mixer: np.ndarray
    compiled_suffix: np.ndarray
    interface_projector: np.ndarray
    observable: np.ndarray
    prefix_state: np.ndarray
    prepared_state: np.ndarray
    analytic_depth_gradient: float
    correct_distribution: np.ndarray
    compiled_distribution: np.ndarray
    correct_decoded_gradient: np.ndarray
    compiled_decoded_gradient: np.ndarray


@dataclass(frozen=True)
class CheckpointInterfaceSafeExample:
    """A compiler preserving checkpoint means but not the full distribution."""

    theta: np.ndarray
    prefix: np.ndarray
    reference_suffix: np.ndarray
    off_interface_mixer: np.ndarray
    compiled_suffix: np.ndarray
    interface_projector: np.ndarray
    observable: np.ndarray
    prefix_state: np.ndarray
    prepared_state: np.ndarray
    correct_distribution: np.ndarray
    compiled_distribution: np.ndarray
    correct_decoded_gradient: np.ndarray
    compiled_decoded_gradient: np.ndarray
    total_variation_distance: float


def _validate_square_power_of_two(matrix: object, *, name: str) -> np.ndarray:
    values = np.asarray(matrix, dtype=complex)
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError(f"{name} must be square.")
    dimension = values.shape[0]
    if dimension < 2 or dimension & (dimension - 1):
        raise ValueError(f"{name} dimension must be a power of two.")
    return values


def _n_from_dimension(dimension: int) -> int:
    if dimension < 2 or dimension & (dimension - 1):
        raise ValueError("dimension must be a power of two of at least two.")
    return dimension.bit_length() - 1


def _kron_all(factors: list[np.ndarray]) -> np.ndarray:
    out = np.asarray([[1.0]], dtype=complex)
    for factor in factors:
        out = np.kron(out, factor)
    return out


def normalized_hadamard(qubits: int) -> np.ndarray:
    """Return the normalized Walsh--Hadamard matrix on ``qubits`` qubits."""

    if qubits < 1:
        raise ValueError("qubits must be positive.")
    one = np.asarray([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2.0)
    return _kron_all([one] * qubits)


def y_basis_change() -> np.ndarray:
    """Return the premeasurement basis change ``H S^dagger`` for Pauli Y."""

    hadamard = np.asarray(
        [[1.0, 1.0], [1.0, -1.0]], dtype=complex
    ) / math.sqrt(2.0)
    s_dagger = np.diag(np.asarray([1.0, -1.0j], dtype=complex))
    return hadamard @ s_dagger


def is_unitary(matrix: object, *, atol: float = 1e-12) -> bool:
    values = _validate_square_power_of_two(matrix, name="matrix")
    identity = np.eye(values.shape[0], dtype=complex)
    return bool(
        np.allclose(values.conj().T @ values, identity, atol=atol, rtol=0.0)
    )


def is_hermitian_unitary(matrix: object, *, atol: float = 1e-12) -> bool:
    values = _validate_square_power_of_two(matrix, name="matrix")
    identity = np.eye(values.shape[0], dtype=complex)
    return bool(
        np.allclose(values, values.conj().T, atol=atol, rtol=0.0)
        and np.allclose(values @ values, identity, atol=atol, rtol=0.0)
    )


def global_protocol_distribution(
    frame: object,
    observable: object,
) -> np.ndarray:
    """Return the exact global-protocol distribution for a consistent frame.

    The input unitary is used for forward preparation and its adjoint for the
    reverse block. The ancilla and all system qubits are measured in the X
    basis. The flattened order is ancilla-major, then big-endian system label.
    """

    unitary = _validate_square_power_of_two(frame, name="frame")
    operator = _validate_square_power_of_two(observable, name="observable")
    if unitary.shape != operator.shape:
        raise ValueError("frame and observable dimensions must agree.")
    dimension = unitary.shape[0]
    n = _n_from_dimension(dimension)
    zero = np.zeros(dimension, dtype=complex)
    zero[0] = 1.0
    state = unitary @ zero
    reverse = unitary.conj().T
    branch_zero = reverse @ state
    branch_one = reverse @ operator @ state
    joint = (
        np.kron(np.asarray([1.0, 0.0], dtype=complex), branch_zero)
        + np.kron(np.asarray([0.0, 1.0], dtype=complex), branch_one)
    ) / math.sqrt(2.0)
    basis_change = np.kron(normalized_hadamard(1), normalized_hadamard(n))
    probabilities = np.abs(basis_change @ joint) ** 2
    return probabilities / probabilities.sum()


def checkpoint_interface_projector(n: int, depth: int) -> np.ndarray:
    """Project onto a zero lower suffix at checkpoint depth ``depth``."""

    if n < 1:
        raise ValueError("n must be positive.")
    if not 0 <= depth < n:
        raise ValueError("depth must lie in 0, ..., n-1.")
    dimension = 1 << n
    suffix_width = n - depth - 1
    diagonal = np.zeros(dimension, dtype=complex)
    for label in range(dimension):
        if suffix_width == 0 or (label & ((1 << suffix_width) - 1)) == 0:
            diagonal[label] = 1.0
    return np.diag(diagonal)


def active_interface_residual(
    reference_suffix: object,
    compiled_suffix: object,
    projector: object,
    *,
    phase: float = 0.0,
) -> float:
    """Return ``||C P - exp(i phase) B P||_max`` for no-workspace checks."""

    reference = _validate_square_power_of_two(
        reference_suffix, name="reference_suffix"
    )
    compiled = _validate_square_power_of_two(
        compiled_suffix, name="compiled_suffix"
    )
    active = _validate_square_power_of_two(projector, name="projector")
    if reference.shape != compiled.shape or reference.shape != active.shape:
        raise ValueError("suffix and projector dimensions must agree.")
    residual = compiled @ active - np.exp(1.0j * phase) * reference @ active
    return float(np.max(np.abs(residual)))


def checkpoint_protocol_distribution(
    prefix: object,
    suffix: object,
    observable: object,
    *,
    target: int,
) -> np.ndarray:
    """Return one exact checkpoint distribution with consistent suffix use.

    The full state is prepared as ``suffix @ prefix @ |0>``. After the
    controlled observable, ``suffix^dagger`` is applied. The ancilla and the
    selected system target are measured in the Y basis; all other system qubits
    remain in the computational basis. Flattening is ancilla-major.
    """

    prefix_u = _validate_square_power_of_two(prefix, name="prefix")
    suffix_u = _validate_square_power_of_two(suffix, name="suffix")
    operator = _validate_square_power_of_two(observable, name="observable")
    if prefix_u.shape != suffix_u.shape or prefix_u.shape != operator.shape:
        raise ValueError("prefix, suffix, and observable dimensions must agree.")
    dimension = prefix_u.shape[0]
    n = _n_from_dimension(dimension)
    if not 0 <= target < n:
        raise ValueError("target must lie in 0, ..., n-1.")

    zero = np.zeros(dimension, dtype=complex)
    zero[0] = 1.0
    prepared = suffix_u @ prefix_u @ zero
    reverse = suffix_u.conj().T
    branch_zero = reverse @ prepared
    branch_one = reverse @ operator @ prepared
    joint = (
        np.kron(np.asarray([1.0, 0.0], dtype=complex), branch_zero)
        + np.kron(np.asarray([0.0, 1.0], dtype=complex), branch_one)
    ) / math.sqrt(2.0)

    identity = np.eye(2, dtype=complex)
    y_change = y_basis_change()
    factors = [y_change]
    factors.extend(y_change if qubit == target else identity for qubit in range(n))
    probabilities = np.abs(_kron_all(factors) @ joint) ** 2
    return probabilities / probabilities.sum()


def two_qubit_checkpoint_factors(
    theta: object,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the depth-zero prefix and depth-one suffix for two qubits."""

    values = np.asarray(theta, dtype=float).reshape(-1)
    if values.size != 3:
        raise ValueError("The two-qubit real Hopf chart has three angles.")
    identity = np.eye(2, dtype=complex)
    prefix = np.kron(hopf_ry(float(values[0])), identity)
    suffix = np.zeros((4, 4), dtype=complex)
    suffix[0:2, 0:2] = hopf_ry(float(values[1]))
    suffix[2:4, 2:4] = hopf_ry(float(values[2]))
    return prefix, suffix


def _analytic_real_gradient(theta: np.ndarray, observable: np.ndarray) -> np.ndarray:
    data = real_tree_data(theta)
    state = data.state.astype(complex)
    response = observable @ state
    return np.asarray(
        [
            2.0 * np.real(np.vdot(derivative, response))
            for derivative in data.derivatives
        ],
        dtype=float,
    )


def two_qubit_global_state_column_counterexample(
) -> GlobalStateColumnCounterexample:
    """Return a closed-form global counterexample at ``theta_j = pi/4``.

    ``Q`` is the two-qubit SWAP, which fixes ``|00>`` but exchanges the root
    and left-child marker labels. Consequently ``V = W Q`` prepares exactly the
    same state as ``W`` while its inverse sends the observable response to the
    wrong marker.
    """

    theta = np.full(3, math.pi / 4.0, dtype=float)
    frame = np.asarray(real_frame_matrix(theta), dtype=complex)
    mixer = np.asarray(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=complex,
    )
    compiled = frame @ mixer
    observable = -np.kron(
        np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=complex),
        np.eye(2, dtype=complex),
    )
    zero = np.asarray([1.0, 0.0, 0.0, 0.0], dtype=complex)
    state = frame @ zero
    data = real_tree_data(theta)
    analytic = _analytic_real_gradient(theta, observable)
    correct_distribution = global_protocol_distribution(frame, observable)
    compiled_distribution = global_protocol_distribution(compiled, observable)
    correct_decoded = decode_balanced_magnitude_gradient(
        correct_distribution, data.sqrt_metric, 2
    )
    compiled_decoded = decode_balanced_magnitude_gradient(
        compiled_distribution, data.sqrt_metric, 2
    )
    return GlobalStateColumnCounterexample(
        theta=theta,
        frame=frame,
        mixer=mixer,
        compiled_frame=compiled,
        observable=observable,
        state=state,
        sqrt_metric=data.sqrt_metric.copy(),
        analytic_gradient=analytic,
        correct_distribution=correct_distribution,
        compiled_distribution=compiled_distribution,
        correct_decoded_gradient=correct_decoded,
        compiled_decoded_gradient=compiled_decoded,
    )


def two_qubit_checkpoint_state_column_counterexample(
) -> CheckpointStateColumnCounterexample:
    """Return a depth-zero checkpoint whose gradient changes sign.

    At the equal-angle point, the prefix state is ``|+0>``. The mixer
    ``X tensor I`` fixes that one state but flips its root-tangent partner. The
    compiled suffix ``C = B Q`` therefore prepares the same final state while
    violating the complete active-interface contract.
    """

    theta = np.full(3, math.pi / 4.0, dtype=float)
    prefix, suffix = two_qubit_checkpoint_factors(theta)
    pauli_x = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    interface_mixer = np.kron(pauli_x, np.eye(2, dtype=complex))
    compiled = suffix @ interface_mixer
    projector = checkpoint_interface_projector(2, 0)
    pauli_z = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    observable = -np.kron(pauli_z, np.eye(2, dtype=complex))
    zero = np.asarray([1.0, 0.0, 0.0, 0.0], dtype=complex)
    prefix_state = prefix @ zero
    state = suffix @ prefix_state
    analytic = _analytic_real_gradient(theta, observable)
    correct_distribution = checkpoint_protocol_distribution(
        prefix, suffix, observable, target=0
    )
    compiled_distribution = checkpoint_protocol_distribution(
        prefix, compiled, observable, target=0
    )
    correct_decoded = decode_checkpoint_gradient(correct_distribution, 2, 0)
    compiled_decoded = decode_checkpoint_gradient(compiled_distribution, 2, 0)
    return CheckpointStateColumnCounterexample(
        theta=theta,
        prefix=prefix,
        reference_suffix=suffix,
        interface_mixer=interface_mixer,
        compiled_suffix=compiled,
        interface_projector=projector,
        observable=observable,
        prefix_state=prefix_state,
        prepared_state=state,
        analytic_depth_gradient=float(analytic[0]),
        correct_distribution=correct_distribution,
        compiled_distribution=compiled_distribution,
        correct_decoded_gradient=correct_decoded,
        compiled_decoded_gradient=compiled_decoded,
    )


def two_qubit_checkpoint_interface_safe_example(
) -> CheckpointInterfaceSafeExample:
    """Return an interface-safe compiler with a different full distribution.

    The diagonal mixer ``diag(1,1,1,i)`` is the identity on the depth-zero
    active interface (the lower suffix is zero) but changes the orthogonal
    suffix sector. It therefore preserves checkpoint estimator means while it
    may change unobserved-suffix-resolved probabilities.
    """

    theta = np.full(3, math.pi / 4.0, dtype=float)
    prefix, suffix = two_qubit_checkpoint_factors(theta)
    off_interface_mixer = np.diag(
        np.asarray([1.0, 1.0, 1.0, 1.0j], dtype=complex)
    )
    compiled = suffix @ off_interface_mixer
    projector = checkpoint_interface_projector(2, 0)
    pauli_z = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    observable = np.kron(np.eye(2, dtype=complex), pauli_z)
    zero = np.asarray([1.0, 0.0, 0.0, 0.0], dtype=complex)
    prefix_state = prefix @ zero
    state = suffix @ prefix_state
    correct_distribution = checkpoint_protocol_distribution(
        prefix, suffix, observable, target=0
    )
    compiled_distribution = checkpoint_protocol_distribution(
        prefix, compiled, observable, target=0
    )
    correct_decoded = decode_checkpoint_gradient(correct_distribution, 2, 0)
    compiled_decoded = decode_checkpoint_gradient(compiled_distribution, 2, 0)
    total_variation = 0.5 * float(
        np.sum(np.abs(correct_distribution - compiled_distribution))
    )
    return CheckpointInterfaceSafeExample(
        theta=theta,
        prefix=prefix,
        reference_suffix=suffix,
        off_interface_mixer=off_interface_mixer,
        compiled_suffix=compiled,
        interface_projector=projector,
        observable=observable,
        prefix_state=prefix_state,
        prepared_state=state,
        correct_distribution=correct_distribution,
        compiled_distribution=compiled_distribution,
        correct_decoded_gradient=correct_decoded,
        compiled_decoded_gradient=compiled_decoded,
        total_variation_distance=total_variation,
    )
