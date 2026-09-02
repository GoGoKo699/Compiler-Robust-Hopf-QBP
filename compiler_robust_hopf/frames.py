"""Independent analytic constructions of balanced Hopf states and frames."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .conventions import infer_n_from_theta_mag, marker_label


@dataclass(frozen=True)
class RealTreeData:
    """Recursive data for the balanced real Hopf tree."""

    n: int
    state: np.ndarray
    subtree: tuple[np.ndarray | None, ...]
    complements: tuple[np.ndarray | None, ...]
    sqrt_metric: np.ndarray
    metric: np.ndarray
    derivatives: tuple[np.ndarray, ...]


def basis_vector(dimension: int, label: int, *, dtype: type = complex) -> np.ndarray:
    if dimension < 1 or not 0 <= label < dimension:
        raise ValueError("Invalid basis-vector dimension or label.")
    vector = np.zeros(dimension, dtype=dtype)
    vector[label] = 1
    return vector


def hopf_ry(theta: float) -> np.ndarray:
    """Return ``R_y(theta) = exp(-i theta Y)`` in the Hopf convention."""

    c = float(np.cos(theta))
    s = float(np.sin(theta))
    return np.asarray([[c, -s], [s, c]], dtype=complex)


def real_tree_data(theta_mag: object) -> RealTreeData:
    """Return the recursive state, complements, metric, and derivatives."""

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    N = 1 << n

    subtree: list[np.ndarray | None] = [None] * (2 * N)
    complements: list[np.ndarray | None] = [None] * N
    for leaf in range(N):
        subtree[N + leaf] = basis_vector(N, leaf, dtype=float)

    for node in range(N - 1, 0, -1):
        left = subtree[2 * node]
        right = subtree[2 * node + 1]
        assert left is not None and right is not None
        c = float(np.cos(theta[node - 1]))
        s = float(np.sin(theta[node - 1]))
        subtree[node] = c * left + s * right
        complements[node] = -s * left + c * right

    incoming = np.zeros(N, dtype=float)
    incoming[1] = 1.0
    for node in range(1, N):
        left = 2 * node
        right = left + 1
        if left < N:
            incoming[left] = incoming[node] * np.cos(theta[node - 1])
        if right < N:
            incoming[right] = incoming[node] * np.sin(theta[node - 1])

    sqrt_metric = incoming[1:].copy()
    derivatives: list[np.ndarray] = []
    for node in range(1, N):
        complement = complements[node]
        assert complement is not None
        derivatives.append(sqrt_metric[node - 1] * complement)

    root = subtree[1]
    assert root is not None
    return RealTreeData(
        n=n,
        state=np.asarray(root, dtype=float),
        subtree=tuple(subtree),
        complements=tuple(complements),
        sqrt_metric=sqrt_metric,
        metric=sqrt_metric**2,
        derivatives=tuple(derivatives),
    )


def real_state(theta_mag: object) -> np.ndarray:
    return real_tree_data(theta_mag).state


def real_frame_matrix(theta_mag: object) -> np.ndarray:
    """Return the canonical real Hopf differential frame."""

    data = real_tree_data(theta_mag)
    N = 1 << data.n
    frame = np.zeros((N, N), dtype=float)
    frame[:, 0] = data.state
    for node in range(1, N):
        complement = data.complements[node]
        assert complement is not None
        frame[:, marker_label(node, data.n)] = complement
    return frame


def phase_layer_matrix(theta_ph: object, *, inverse: bool = False) -> np.ndarray:
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size == 0 or phase.size & (phase.size - 1):
        raise ValueError("theta_ph length must be a positive power of two.")
    sign = -1.0 if inverse else 1.0
    return np.diag(np.exp(1j * sign * phase))


def complex_frame_matrix(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Return the separated complex frame ``D_ph W_R``."""

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    if phase.size != 1 << n:
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return phase_layer_matrix(phase) @ real_frame_matrix(theta)


def _validate_n_depth(n: int, depth: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")
    if not 0 <= depth < n:
        raise ValueError("depth must lie in 0, ..., n-1.")


def direct_addressed_depth_layer(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Return one addressed real-frame layer on the full system register."""

    _validate_n_depth(n, depth)
    values = np.asarray(angles, dtype=float).reshape(-1)
    if values.size != 1 << depth:
        raise ValueError("angles must contain exactly 2**depth entries.")

    dimension = 1 << n
    suffix_width = n - depth - 1
    unitary = np.eye(dimension, dtype=complex)
    for prefix, theta in enumerate(values):
        anchor = prefix << (n - depth)
        marker = anchor | (1 << suffix_width)
        unitary[np.ix_([anchor, marker], [anchor, marker])] = hopf_ry(float(theta))
    return unitary


def direct_real_frame(n: int, theta_mag: object) -> np.ndarray:
    """Compose every addressed frame layer in increasing tree-depth order."""

    if n < 1:
        raise ValueError("n must be positive.")
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")

    unitary = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(n):
        width = 1 << depth
        layer = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        )
        unitary = layer @ unitary
        offset += width
    return unitary
