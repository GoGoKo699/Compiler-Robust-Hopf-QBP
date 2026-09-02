"""Stable indexing conventions shared with the Hopf-QBP implementation."""
from __future__ import annotations

import math


def infer_n_from_theta_mag(theta_mag: object) -> int:
    """Infer ``n`` from a magnitude block of length ``2**n - 1``."""

    length = len(theta_mag)  # type: ignore[arg-type]
    n_float = math.log2(length + 1)
    n = int(round(n_float))
    if n < 1 or (1 << n) - 1 != length:
        raise ValueError("theta_mag must have length 2**n - 1 with n >= 1.")
    return n


def node_depth_position(node: int) -> tuple[int, int]:
    """Return ``(depth, position)`` for breadth-first node ``node``."""

    if node < 1:
        raise ValueError("Internal-node indices start at 1.")
    depth = node.bit_length() - 1
    return depth, node - (1 << depth)


def anchor_label(node: int, n: int) -> int:
    """Return the leftmost basis label in the subtree rooted at ``node``."""

    depth, position = node_depth_position(node)
    if depth >= n:
        raise ValueError("Node is not internal for the requested qubit count.")
    return position << (n - depth)


def marker_label(node: int, n: int) -> int:
    """Return the nonzero computational-basis marker for one Hopf node."""

    depth, position = node_depth_position(node)
    if depth >= n:
        raise ValueError("Node is not internal for the requested qubit count.")
    return (2 * position + 1) << (n - depth - 1)


def parity(first: int, second: int) -> int:
    """Return the mod-two inner product of two nonnegative integer labels."""

    if first < 0 or second < 0:
        raise ValueError("Parity labels must be nonnegative.")
    return (first & second).bit_count() & 1
