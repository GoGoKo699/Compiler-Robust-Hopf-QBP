"""Independent analytic constructions of balanced Hopf states and frames.

The recursive formulas are valid for unrestricted real angles.  In that form a
coordinate derivative carries an *oriented incoming amplitude* ``a_j``, which
may be negative, and the metric entry is ``g_jj=a_j**2``.  On the canonical
Hopf coordinate domains the incoming amplitudes are nonnegative, so
``a_j=sqrt(g_jj)`` with the principal square root.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .conventions import infer_n_from_theta_mag, marker_label


@dataclass(frozen=True)
class RealTreeData:
    """Recursive data for the balanced real Hopf tree.

    ``incoming_amplitude[j-1]`` is the signed ancestor-product multiplying the
    normalized complement at internal node ``j``.  ``sqrt_metric`` is retained
    as a read-only principal-square-root property for geometric notation; it is
    generally ``abs(incoming_amplitude)`` outside the canonical chart.
    """

    n: int
    state: np.ndarray
    subtree: tuple[np.ndarray | None, ...]
    complements: tuple[np.ndarray | None, ...]
    incoming_amplitude: np.ndarray
    metric: np.ndarray
    regular_mask: np.ndarray
    derivatives: tuple[np.ndarray, ...]

    @property
    def sqrt_metric(self) -> np.ndarray:
        """Return the principal nonnegative square roots of the metric entries."""

        return np.sqrt(self.metric)


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


def canonical_magnitude_angle_mask(
    theta_mag: object,
    *,
    complex_chart: bool = False,
    atol: float = 1e-12,
) -> np.ndarray:
    """Return which magnitude angles lie in the canonical Hopf domains.

    For the complex chart, every magnitude angle lies in ``[0, pi/2]``.  For
    the real chart, depths ``0,...,n-2`` lie in ``[0, pi/2]`` and the final
    depth lies in ``[0, 2*pi)`` so that leaf signs are represented without
    phases.  Endpoints are accepted up to ``atol``; the upper ``2*pi`` endpoint
    is identified with zero and is therefore excluded except for tolerance.
    """

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    mask = np.ones(theta.size, dtype=bool)
    split = (1 << (n - 1)) - 1 if n > 1 else 0
    half_pi = 0.5 * np.pi

    if split:
        mask[:split] = (
            (theta[:split] >= -atol)
            & (theta[:split] <= half_pi + atol)
        )

    final = theta[split:]
    if complex_chart:
        mask[split:] = (final >= -atol) & (final <= half_pi + atol)
    else:
        mask[split:] = (final >= -atol) & (final < 2.0 * np.pi + atol)
    return mask


def in_canonical_magnitude_domain(
    theta_mag: object,
    *,
    complex_chart: bool = False,
    atol: float = 1e-12,
) -> bool:
    """Return whether all magnitude angles satisfy the canonical domains."""

    return bool(
        np.all(
            canonical_magnitude_angle_mask(
                theta_mag,
                complex_chart=complex_chart,
                atol=atol,
            )
        )
    )


def real_tree_data(theta_mag: object) -> RealTreeData:
    """Return the recursive state, complements, metric, and derivatives.

    The calculation does not restrict angles to a canonical chart.  For each
    internal node ``j`` it constructs a unit complement ``e_j`` and the exact
    differential

    ``partial_(theta_j)|psi> = a_j |e_j>``,

    where ``a_j`` is the oriented incoming amplitude.  At ``a_j=0`` the raw
    derivative vanishes.  The marker column remains a canonical orthogonal
    continuation of the frame, but it is not a derivative-normalized tangent at
    that singular coordinate.
    """

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    dimension = 1 << n

    subtree: list[np.ndarray | None] = [None] * (2 * dimension)
    complements: list[np.ndarray | None] = [None] * dimension
    for leaf in range(dimension):
        subtree[dimension + leaf] = basis_vector(
            dimension, leaf, dtype=float
        )

    for node in range(dimension - 1, 0, -1):
        left = subtree[2 * node]
        right = subtree[2 * node + 1]
        assert left is not None and right is not None
        cosine = float(np.cos(theta[node - 1]))
        sine = float(np.sin(theta[node - 1]))
        subtree[node] = cosine * left + sine * right
        complements[node] = -sine * left + cosine * right

    incoming = np.zeros(dimension, dtype=float)
    incoming[1] = 1.0
    for node in range(1, dimension):
        left = 2 * node
        right = left + 1
        if left < dimension:
            incoming[left] = incoming[node] * np.cos(theta[node - 1])
        if right < dimension:
            incoming[right] = incoming[node] * np.sin(theta[node - 1])

    incoming_amplitude = incoming[1:].copy()
    metric = incoming_amplitude**2
    derivatives: list[np.ndarray] = []
    for node in range(1, dimension):
        complement = complements[node]
        assert complement is not None
        derivatives.append(incoming_amplitude[node - 1] * complement)

    root = subtree[1]
    assert root is not None
    return RealTreeData(
        n=n,
        state=np.asarray(root, dtype=float),
        subtree=tuple(subtree),
        complements=tuple(complements),
        incoming_amplitude=incoming_amplitude,
        metric=metric,
        regular_mask=metric > 0.0,
        derivatives=tuple(derivatives),
    )


def real_state(theta_mag: object) -> np.ndarray:
    return real_tree_data(theta_mag).state


def real_frame_matrix(theta_mag: object) -> np.ndarray:
    """Return the canonical real Hopf differential-frame continuation."""

    data = real_tree_data(theta_mag)
    dimension = 1 << data.n
    frame = np.zeros((dimension, dimension), dtype=float)
    frame[:, 0] = data.state
    for node in range(1, dimension):
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


def complex_magnitude_frame_matrix(
    theta_mag: object, theta_ph: object
) -> np.ndarray:
    """Return the phase-dressed complex magnitude frame ``D_ph W_R``.

    The remaining leaf-phase derivatives form a separate direct measurement
    stream; they cannot all be columns of the same ``N``-dimensional unitary.
    """

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    if phase.size != 1 << n:
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return phase_layer_matrix(phase) @ real_frame_matrix(theta)


def complex_frame_matrix(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Backward-compatible alias for :func:`complex_magnitude_frame_matrix`."""

    return complex_magnitude_frame_matrix(theta_mag, theta_ph)


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
        unitary[np.ix_([anchor, marker], [anchor, marker])] = hopf_ry(
            float(theta)
        )
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
