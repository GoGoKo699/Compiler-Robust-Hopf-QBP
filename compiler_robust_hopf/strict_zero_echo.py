"""Strict-zero borrowed-suffix compiler for addressed Hopf-frame layers.

This module implements the active ``m=0`` schedule selected by
:mod:`compiler_robust_hopf.unified_compiler`.

For a nonfinal addressed depth, one original suffix data qubit is used in place
as a restored predicate carrier. Four predicate-controlled toggles and two
half-angle UCGs implement the desired suffix-zero-controlled Hopf rotation on
the complete Hilbert space. The borrowed logical qubit is returned exactly on
every input, and no clean or dirty ancillary wire is introduced.

Resource values are transparent integer proxies for the asymptotic terms
imported from Yuan--Zhang's exact zero-ancilla UCG and multi-controlled-X
synthesis results. They are not finite native-gate counts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np

from .frames import (
    complex_frame_matrix,
    direct_addressed_depth_layer,
    direct_real_frame,
    hopf_ry,
    phase_layer_matrix,
)
from .unified_compiler import (
    optimal_qsp_depth_proxy,
    ucg_depth_proxy,
    ucg_size_proxy,
)


@dataclass(frozen=True)
class BorrowedSuffixEchoLayerRow:
    """One nonfinal addressed layer under the borrowed-suffix echo."""

    n: int
    depth: int
    prefix_qubits: int
    suffix_qubits: int
    target_bit_position: int
    borrowed_bit_position: int
    remaining_suffix_controls: int
    half_angle_ucg_width: int
    half_angle_ucgs: int
    predicate_toggles: int
    target_echo_cnots: int
    clean_ancillas: int
    ucg_depth_proxy: int
    predicate_depth_proxy: int
    echo_depth_proxy: int
    total_depth_proxy: int
    ucg_size_proxy: int
    predicate_size_proxy: int
    echo_size_proxy: int
    total_size_proxy: int
    logical_nonidentity_blocks: int
    full_width_logical_blocks: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


@dataclass(frozen=True)
class StrictZeroEchoFrameRow:
    """Strict-zero real-frame resource ledger."""

    n: int
    dimension: int
    clean_ancillas: int
    mode: str
    nonfinal_layers: int
    half_angle_ucgs: int
    predicate_toggles: int
    target_echo_cnots: int
    nonfinal_depth_proxy: int
    final_ucg_depth_proxy: int
    total_depth_proxy: int
    nonfinal_size_proxy: int
    final_ucg_size_proxy: int
    total_size_proxy: int
    optimal_qsp_depth_proxy: int
    previous_full_width_depth_proxy: int
    previous_full_width_size_proxy: int

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


@dataclass(frozen=True)
class StrictZeroEchoComplexRow:
    """Strict-zero separated-complex resource ledger."""

    n: int
    dimension: int
    clean_ancillas: int
    real_depth_proxy: int
    diagonal_depth_proxy: int
    total_depth_proxy: int
    real_size_proxy: int
    diagonal_size_proxy: int
    total_size_proxy: int
    optimal_qsp_depth_proxy: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _validate_nonfinal_depth(n: int, depth: int) -> None:
    _validate_n(n)
    if not 0 <= depth < n - 1:
        raise ValueError("The borrowed-suffix echo requires 0 <= depth < n-1.")


def _angles_for_depth(angles: object, depth: int) -> np.ndarray:
    values = np.asarray(angles, dtype=float).reshape(-1)
    if values.size != 1 << depth:
        raise ValueError("angles must contain exactly 2**depth entries.")
    return values


def borrowed_suffix_positions(n: int, depth: int) -> tuple[int, int, tuple[int, ...]]:
    """Return target, borrowed, and remaining-suffix bit positions.

    Bit positions are counted from the least-significant computational-basis
    bit. The borrowed bit is the suffix bit immediately below the Hopf target.
    """

    _validate_nonfinal_depth(n, depth)
    suffix_qubits = n - depth - 1
    target = suffix_qubits
    borrowed = suffix_qubits - 1
    remaining = tuple(range(borrowed))
    return target, borrowed, remaining


def borrowed_suffix_toggle_permutation(n: int, depth: int) -> np.ndarray:
    """Toggle the borrowed bit iff all remaining suffix bits are zero."""

    target, borrowed, remaining = borrowed_suffix_positions(n, depth)
    del target
    dimension = 1 << n
    remaining_mask = (1 << len(remaining)) - 1
    permutation = np.zeros((dimension, dimension), dtype=complex)
    for label in range(dimension):
        predicate = int((label & remaining_mask) == 0)
        output = label ^ (predicate << borrowed)
        permutation[output, label] = 1.0
    return permutation


def borrowed_target_echo_permutation(n: int, depth: int) -> np.ndarray:
    """Return the CNOT from the borrowed suffix bit to the Hopf target."""

    target, borrowed, _remaining = borrowed_suffix_positions(n, depth)
    dimension = 1 << n
    permutation = np.zeros((dimension, dimension), dtype=complex)
    for label in range(dimension):
        output = label ^ (((label >> borrowed) & 1) << target)
        permutation[output, label] = 1.0
    return permutation


def borrowed_half_angle_ucg(
    n: int,
    depth: int,
    angles: object,
    *,
    inverse: bool = False,
) -> np.ndarray:
    """Apply prefix-selected half-angle rotations when the borrowed bit is one."""

    values = _angles_for_depth(angles, depth)
    target, borrowed, _remaining = borrowed_suffix_positions(n, depth)
    sign = -1.0 if inverse else 1.0
    dimension = 1 << n
    unitary = np.eye(dimension, dtype=complex)

    for label in range(dimension):
        if (label >> target) & 1:
            continue
        if not ((label >> borrowed) & 1):
            continue
        partner = label | (1 << target)
        prefix = label >> (n - depth) if depth else 0
        unitary[np.ix_([label, partner], [label, partner])] = hopf_ry(
            sign * float(values[prefix]) / 2.0
        )
    return unitary


def borrowed_suffix_echo_layer(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Return the exact ancilla-free echo for one nonfinal addressed layer.

    The chronological gate sequence is

    ``X_b->t, T_h, C, T_h, X_b->t, T_h, C, T_h``,

    where ``T_h`` toggles the borrowed suffix bit when every remaining suffix
    bit is zero, and ``C`` is the prefix-selected ``R_y(theta/2)`` controlled
    by the borrowed bit.
    """

    values = _angles_for_depth(angles, depth)
    toggle = borrowed_suffix_toggle_permutation(n, depth)
    target_echo = borrowed_target_echo_permutation(n, depth)
    half = borrowed_half_angle_ucg(n, depth, values)

    unitary = np.eye(1 << n, dtype=complex)
    for gate in (
        target_echo,
        toggle,
        half,
        toggle,
        target_echo,
        toggle,
        half,
        toggle,
    ):
        unitary = gate @ unitary
    return unitary


def echo_sector_action(
    theta: float,
    *,
    predicate: int,
    borrowed_bit: int,
) -> tuple[np.ndarray, int]:
    """Return the target action and final borrowed bit in one abstract sector."""

    if predicate not in (0, 1) or borrowed_bit not in (0, 1):
        raise ValueError("predicate and borrowed_bit must be 0 or 1.")

    half = hopf_ry(float(theta) / 2.0)
    echo = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    action = np.eye(2, dtype=complex)
    bit = int(borrowed_bit)

    if bit:
        action = echo @ action
    bit ^= predicate
    if bit:
        action = half @ action
    bit ^= predicate
    if bit:
        action = echo @ action
    bit ^= predicate
    if bit:
        action = half @ action
    bit ^= predicate
    return action, bit


def echo_algebra_residual(theta: float) -> dict[str, float]:
    """Return residuals in the one-qubit identities used by the echo."""

    half = hopf_ry(float(theta) / 2.0)
    echo = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    return {
        "square": float(np.max(np.abs(half @ half - hopf_ry(float(theta))))),
        "conjugation": float(
            np.max(np.abs(echo @ half @ echo - half.conj().T))
        ),
        "cancelling_word": float(
            np.max(np.abs(half @ echo @ half @ echo - np.eye(2)))
        ),
    }


def strict_zero_echo_real_frame(n: int, theta_mag: object) -> np.ndarray:
    """Compose the exact strict-zero echo frame."""

    _validate_n(n)
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")

    unitary = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(n):
        width = 1 << depth
        angles = values[offset : offset + width]
        if depth < n - 1:
            layer = borrowed_suffix_echo_layer(n, depth, angles)
        else:
            layer = direct_addressed_depth_layer(n, depth, angles)
        unitary = layer @ unitary
        offset += width
    return unitary


def strict_zero_echo_complex_frame(
    theta_mag: object,
    theta_ph: object,
) -> np.ndarray:
    """Return ``D_ph W_R`` with the strict-zero echo real frame."""

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = (theta.size + 1).bit_length() - 1
    if theta.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size != 1 << n:
        raise ValueError("theta_ph must have length 2**n.")
    return phase_layer_matrix(phase) @ strict_zero_echo_real_frame(n, theta)


def echo_layer_residual(n: int, depth: int, angles: object) -> float:
    """Return max-norm residual against the addressed layer."""

    return float(
        np.max(
            np.abs(
                borrowed_suffix_echo_layer(n, depth, angles)
                - direct_addressed_depth_layer(n, depth, angles)
            )
        )
    )


def echo_frame_residual(n: int, theta_mag: object) -> float:
    """Return max-norm residual against the addressed complete frame."""

    return float(
        np.max(
            np.abs(
                strict_zero_echo_real_frame(n, theta_mag)
                - direct_real_frame(n, theta_mag)
            )
        )
    )


def echo_complex_frame_residual(theta_mag: object, theta_ph: object) -> float:
    """Return max-norm residual against the separated complex frame."""

    return float(
        np.max(
            np.abs(
                strict_zero_echo_complex_frame(theta_mag, theta_ph)
                - complex_frame_matrix(theta_mag, theta_ph)
            )
        )
    )


def _negative_control_toggle_depth_proxy(controls: int) -> int:
    if controls < 0:
        raise ValueError("controls must be nonnegative.")
    return 1 if controls == 0 else controls + 2


def _negative_control_toggle_size_proxy(controls: int) -> int:
    if controls < 0:
        raise ValueError("controls must be nonnegative.")
    return 1 if controls == 0 else 3 * controls


def borrowed_suffix_echo_layer_resource_row(
    n: int,
    depth: int,
) -> BorrowedSuffixEchoLayerRow:
    """Return one strict-zero layer term ledger."""

    target, borrowed, remaining = borrowed_suffix_positions(n, depth)
    suffix = n - depth - 1
    controls = len(remaining)
    width = depth + 2

    ucg_depth = 2 * ucg_depth_proxy(width, 0)
    predicate_depth = 4 * _negative_control_toggle_depth_proxy(controls)
    echo_depth = 2
    ucg_size = 2 * ucg_size_proxy(width)
    predicate_size = 4 * _negative_control_toggle_size_proxy(controls)
    echo_size = 2

    return BorrowedSuffixEchoLayerRow(
        n=n,
        depth=depth,
        prefix_qubits=depth,
        suffix_qubits=suffix,
        target_bit_position=target,
        borrowed_bit_position=borrowed,
        remaining_suffix_controls=controls,
        half_angle_ucg_width=width,
        half_angle_ucgs=2,
        predicate_toggles=4,
        target_echo_cnots=2,
        clean_ancillas=0,
        ucg_depth_proxy=ucg_depth,
        predicate_depth_proxy=predicate_depth,
        echo_depth_proxy=echo_depth,
        total_depth_proxy=ucg_depth + predicate_depth + echo_depth,
        ucg_size_proxy=ucg_size,
        predicate_size_proxy=predicate_size,
        echo_size_proxy=echo_size,
        total_size_proxy=ucg_size + predicate_size + echo_size,
        logical_nonidentity_blocks=1 << depth,
        full_width_logical_blocks=1 << (n - 1),
    )


def strict_zero_echo_frame_resource_row(n: int) -> StrictZeroEchoFrameRow:
    """Return the complete strict-zero real-frame term ledger."""

    _validate_n(n)
    dimension = 1 << n
    layers = tuple(
        borrowed_suffix_echo_layer_resource_row(n, depth)
        for depth in range(n - 1)
    )
    nonfinal_depth = sum(row.total_depth_proxy for row in layers)
    nonfinal_size = sum(row.total_size_proxy for row in layers)
    final_depth = ucg_depth_proxy(n, 0)
    final_size = ucg_size_proxy(n)

    return StrictZeroEchoFrameRow(
        n=n,
        dimension=dimension,
        clean_ancillas=0,
        mode="strict-zero-borrowed-suffix-echo",
        nonfinal_layers=n - 1,
        half_angle_ucgs=2 * (n - 1),
        predicate_toggles=4 * (n - 1),
        target_echo_cnots=2 * (n - 1),
        nonfinal_depth_proxy=nonfinal_depth,
        final_ucg_depth_proxy=final_depth,
        total_depth_proxy=nonfinal_depth + final_depth,
        nonfinal_size_proxy=nonfinal_size,
        final_ucg_size_proxy=final_size,
        total_size_proxy=nonfinal_size + final_size,
        optimal_qsp_depth_proxy=optimal_qsp_depth_proxy(n, 0),
        previous_full_width_depth_proxy=n * ucg_depth_proxy(n, 0),
        previous_full_width_size_proxy=n * ucg_size_proxy(n),
    )


def strict_zero_echo_complex_resource_row(n: int) -> StrictZeroEchoComplexRow:
    """Return the strict-zero separated-complex term ledger."""

    real = strict_zero_echo_frame_resource_row(n)
    diagonal_depth = ucg_depth_proxy(n, 0)
    diagonal_size = ucg_size_proxy(n)
    return StrictZeroEchoComplexRow(
        n=n,
        dimension=1 << n,
        clean_ancillas=0,
        real_depth_proxy=real.total_depth_proxy,
        diagonal_depth_proxy=diagonal_depth,
        total_depth_proxy=real.total_depth_proxy + diagonal_depth,
        real_size_proxy=real.total_size_proxy,
        diagonal_size_proxy=diagonal_size,
        total_size_proxy=real.total_size_proxy + diagonal_size,
        optimal_qsp_depth_proxy=real.optimal_qsp_depth_proxy,
    )


def strict_zero_echo_frame_resource_rows(
    ns: Iterable[int],
) -> tuple[StrictZeroEchoFrameRow, ...]:
    return tuple(strict_zero_echo_frame_resource_row(int(n)) for n in ns)
