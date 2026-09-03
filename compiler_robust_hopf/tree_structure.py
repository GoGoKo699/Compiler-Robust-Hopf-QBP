"""Exact tree identities used by the unified Hopf-frame compiler."""
from __future__ import annotations

import numpy as np

from .frames import direct_addressed_depth_layer, direct_real_frame


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _validate_cut(n: int, t: int) -> None:
    _validate_n(n)
    if not 0 <= t <= n:
        raise ValueError("t must lie in 0, ..., n.")


def _theta(theta_mag: object, n: int) -> np.ndarray:
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    return values


def prefix_angle_count(t: int) -> int:
    if t < 0:
        raise ValueError("t must be nonnegative.")
    return (1 << t) - 1


def direct_prefix_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return the product of addressed depths ``0, ..., t-1``."""

    _validate_cut(n, t)
    values = _theta(theta_mag, n)
    unitary = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(t):
        width = 1 << depth
        unitary = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        ) @ unitary
        offset += width
    return unitary


def conditioned_prefix_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return ``W_t`` conditioned on a zero external suffix."""

    _validate_cut(n, t)
    values = _theta(theta_mag, n)
    if t == 0:
        return np.eye(1 << n, dtype=complex)
    prefix = direct_real_frame(t, values[: prefix_angle_count(t)])
    suffix_dimension = 1 << (n - t)
    suffix_zero = np.zeros((suffix_dimension, suffix_dimension), dtype=complex)
    suffix_zero[0, 0] = 1.0
    return np.kron(prefix, suffix_zero) + np.kron(
        np.eye(1 << t, dtype=complex),
        np.eye(suffix_dimension, dtype=complex) - suffix_zero,
    )


def tail_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return the product of addressed depths ``t, ..., n-1``."""

    _validate_cut(n, t)
    values = _theta(theta_mag, n)
    unitary = np.eye(1 << n, dtype=complex)
    offset = prefix_angle_count(t)
    for depth in range(t, n):
        width = 1 << depth
        unitary = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        ) @ unitary
        offset += width
    return unitary


def subtree_angle_indices(n: int, t: int, prefix: int) -> tuple[int, ...]:
    """Return one depth-``t`` subtree's global angles in local BFS order."""

    _validate_cut(n, t)
    branches = 1 << t
    if not 0 <= prefix < branches:
        raise ValueError("prefix is outside the selected cut.")
    suffix_qubits = n - t
    indices: list[int] = []
    for local_depth in range(suffix_qubits):
        for local_position in range(1 << local_depth):
            global_node = (
                (1 << (t + local_depth))
                + (prefix << local_depth)
                + local_position
            )
            indices.append(global_node - 1)
    return tuple(indices)


def subtree_angles(theta_mag: object, n: int, t: int, prefix: int) -> np.ndarray:
    values = _theta(theta_mag, n)
    return values[list(subtree_angle_indices(n, t, prefix))].copy()


def tail_block_diagonal_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return ``direct_sum_r W_(n-t)^(r)`` for the addressed tail."""

    _validate_cut(n, t)
    values = _theta(theta_mag, n)
    suffix_qubits = n - t
    if suffix_qubits == 0:
        return np.eye(1 << n, dtype=complex)
    block_dimension = 1 << suffix_qubits
    unitary = np.zeros((1 << n, 1 << n), dtype=complex)
    for prefix in range(1 << t):
        block = direct_real_frame(
            suffix_qubits, subtree_angles(values, n, t, prefix)
        )
        start = prefix * block_dimension
        unitary[start : start + block_dimension, start : start + block_dimension] = block
    return unitary


def reconstructed_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return the exact cut factorization ``R_t F_t``."""

    return tail_block_diagonal_frame(n, t, theta_mag) @ conditioned_prefix_frame(
        n, t, theta_mag
    )


def prefix_bridge_residual(n: int, t: int, theta_mag: object) -> float:
    return float(
        np.max(
            np.abs(
                direct_prefix_frame(n, t, theta_mag)
                - conditioned_prefix_frame(n, t, theta_mag)
            )
        )
    )


def tail_direct_sum_residual(n: int, t: int, theta_mag: object) -> float:
    return float(
        np.max(
            np.abs(
                tail_frame(n, t, theta_mag)
                - tail_block_diagonal_frame(n, t, theta_mag)
            )
        )
    )
