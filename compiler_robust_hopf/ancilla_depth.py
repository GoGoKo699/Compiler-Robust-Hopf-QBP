"""Exact Hopf identities and audited term ledgers for ancilla--depth compilation.

The matrix routines establish Hopf-specific operator identities. The resource
rows expose the contributions used in the asymptotic proof; they are not exact
elementary-gate counts or depths.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable

import numpy as np

from .frames import direct_addressed_depth_layer, direct_real_frame, hopf_ry


@dataclass(frozen=True)
class AncillaDepthRow:
    """One machine-readable audited resource ledger."""

    n: int
    dimension: int
    state_ancillas: int
    frame_ancillas_upper_bound: int
    unary_prefix_qubits: int
    unary_prefix_ancilla_upper_bound: int
    maximum_unary_control_copies: int
    tail_layers: int
    nonfinal_ucg_work_ancillas: int
    final_ucg_work_ancillas: int
    prefix_depth_proxy: int
    tail_predicate_depth_proxy: int
    ucg_linear_depth_proxy: int
    ucg_exponential_depth_proxy: int
    total_frame_depth_proxy: int
    prefix_size_proxy: int
    tail_predicate_size_proxy: int
    ucg_size_proxy: int
    total_frame_size_proxy: int
    candidate_geometric_term: int
    candidate_sequential_term: int
    optimal_qsp_linear_term: int
    optimal_qsp_geometric_term: int
    logical_hopf_rotations: int
    recordwise_decode_operations_per_shot: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _validate_n_t(n: int, t: int) -> None:
    _validate_n(n)
    if not 0 <= t <= n:
        raise ValueError("t must lie in 0, ..., n.")


def _theta_for_n(theta_mag: object, n: int) -> np.ndarray:
    _validate_n(n)
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    return values


def prefix_angle_count(t: int) -> int:
    if t < 0:
        raise ValueError("t must be nonnegative.")
    return (1 << t) - 1


def direct_prefix_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return addressed depths ``0, ..., t-1`` on the full register."""

    _validate_n_t(n, t)
    values = _theta_for_n(theta_mag, n)
    unitary = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(t):
        width = 1 << depth
        layer = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        )
        unitary = layer @ unitary
        offset += width
    return unitary


def conditioned_prefix_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return ``W_t`` conditioned on the external lower suffix being zero."""

    _validate_n_t(n, t)
    values = _theta_for_n(theta_mag, n)
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
    """Return addressed depths ``t, ..., n-1``."""

    _validate_n_t(n, t)
    values = _theta_for_n(theta_mag, n)
    unitary = np.eye(1 << n, dtype=complex)
    offset = prefix_angle_count(t)
    for depth in range(t, n):
        width = 1 << depth
        layer = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        )
        unitary = layer @ unitary
        offset += width
    return unitary


def hybrid_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    return tail_frame(n, t, theta_mag) @ conditioned_prefix_frame(
        n, t, theta_mag
    )


def prefix_bridge_residual(n: int, t: int, theta_mag: object) -> float:
    residual = direct_prefix_frame(n, t, theta_mag) - conditioned_prefix_frame(
        n, t, theta_mag
    )
    return float(np.max(np.abs(residual)))


def hybrid_frame_residual(n: int, t: int, theta_mag: object) -> float:
    residual = hybrid_frame(n, t, theta_mag) - direct_real_frame(n, theta_mag)
    return float(np.max(np.abs(residual)))


def unary_layer_pairs(t: int, depth: int) -> tuple[tuple[int, int], ...]:
    """Return disjoint unary-mode pairs for one Hopf tree depth."""

    if t < 1:
        raise ValueError("t must be positive for a unary Hopf layer.")
    if not 0 <= depth < t:
        raise ValueError("depth must lie in 0, ..., t-1.")
    suffix_width = t - depth - 1
    return tuple(
        (
            position << (t - depth),
            (position << (t - depth)) | (1 << suffix_width),
        )
        for position in range(1 << depth)
    )


def unary_code_isometry(
    t: int, *, maximum_hilbert_dimension: int = 4096
) -> np.ndarray:
    """Embed ``t`` binary qubits in the one-excitation code of ``2**t`` modes."""

    if t < 1:
        raise ValueError("t must be positive for the unary-code matrix check.")
    modes = 1 << t
    hilbert_dimension = 1 << modes
    if hilbert_dimension > maximum_hilbert_dimension:
        raise ValueError(
            "Dense unary-code checks are limited by maximum_hilbert_dimension."
        )
    isometry = np.zeros((hilbert_dimension, modes), dtype=complex)
    for label in range(modes):
        isometry[1 << label, label] = 1.0
    return isometry


def unary_two_mode_givens(
    modes: int,
    first: int,
    second: int,
    theta: float,
    *,
    maximum_hilbert_dimension: int = 4096,
) -> np.ndarray:
    """Return a number-preserving two-mode Givens gate for small exact tests."""

    if modes < 2:
        raise ValueError("modes must be at least two.")
    if not 0 <= first < modes or not 0 <= second < modes or first == second:
        raise ValueError("first and second must be distinct valid mode indices.")
    hilbert_dimension = 1 << modes
    if hilbert_dimension > maximum_hilbert_dimension:
        raise ValueError(
            "Dense unary-code checks are limited by maximum_hilbert_dimension."
        )

    gate = np.eye(hilbert_dimension, dtype=complex)
    pair_mask = (1 << first) | (1 << second)
    block = hopf_ry(float(theta))
    for label in range(hilbert_dimension):
        if ((label >> first) & 1) and not ((label >> second) & 1):
            partner = label ^ pair_mask
            gate[np.ix_([label, partner], [label, partner])] = block
    return gate


def unary_hopf_network(
    t: int,
    theta_prefix: object,
    *,
    maximum_hilbert_dimension: int = 4096,
) -> np.ndarray:
    """Return the dense unary Givens network for a small Hopf frame."""

    if t < 1:
        raise ValueError("t must be positive for the unary-code matrix check.")
    values = np.asarray(theta_prefix, dtype=float).reshape(-1)
    if values.size != prefix_angle_count(t):
        raise ValueError("theta_prefix must have length 2**t - 1.")
    modes = 1 << t
    hilbert_dimension = 1 << modes
    if hilbert_dimension > maximum_hilbert_dimension:
        raise ValueError(
            "Dense unary-code checks are limited by maximum_hilbert_dimension."
        )

    unitary = np.eye(hilbert_dimension, dtype=complex)
    for depth in range(t):
        for first, second in unary_layer_pairs(t, depth):
            position = first >> (t - depth)
            node = (1 << depth) + position
            gate = unary_two_mode_givens(
                modes,
                first,
                second,
                values[node - 1],
                maximum_hilbert_dimension=maximum_hilbert_dimension,
            )
            unitary = gate @ unitary
    return unitary


def unary_code_action(t: int, theta_prefix: object) -> np.ndarray:
    isometry = unary_code_isometry(t)
    network = unary_hopf_network(t, theta_prefix)
    return isometry.conj().T @ network @ isometry


def unary_code_leakage(t: int, theta_prefix: object) -> float:
    isometry = unary_code_isometry(t)
    network = unary_hopf_network(t, theta_prefix)
    projector = isometry @ isometry.conj().T
    leakage = (
        np.eye(network.shape[0], dtype=complex) - projector
    ) @ network @ isometry
    return float(np.max(np.abs(leakage)))


def maximum_unary_control_copies(t: int) -> int:
    if t < 0:
        raise ValueError("t must be nonnegative.")
    return 0 if t == 0 else 1 << (t - 1)


def unary_prefix_ancilla_upper_bound(t: int) -> int:
    """Return the conservative clean-workspace bound ``3*2**t - t``."""

    if t < 0:
        raise ValueError("t must be nonnegative.")
    return 0 if t == 0 else 3 * (1 << t) - t


def hybrid_prefix_qubits(n: int, state_ancillas: int) -> int:
    """Return ``min(n, max(0, floor(log2(m/3))))`` conservatively."""

    _validate_n(n)
    if state_ancillas < 0:
        raise ValueError("state_ancillas must be nonnegative.")
    if state_ancillas < 3:
        return 0
    quotient = state_ancillas // 3
    return min(n, quotient.bit_length() - 1)


def frame_ancilla_upper_bound(state_ancillas: int) -> int:
    """Return the audited total frame workspace bound.

    The construction uses the same ``m`` ancillary qubits as the matched state
    compiler whenever ``m >= 1``. Only the strict ``m = 0`` endpoint needs one
    additional reusable suffix flag.
    """

    if state_ancillas < 0:
        raise ValueError("state_ancillas must be nonnegative.")
    return max(1, state_ancillas)


def tail_ucg_work_ancillas(state_ancillas: int, *, final: bool) -> int:
    """Return clean work qubits available to one tail UCG.

    A nonfinal addressed layer reserves one of the ``m`` qubits as the
    suffix-zero flag. The final layer has no suffix predicate and can use all
    ``m`` work qubits. At ``m=0`` the frame's one extra flag is not counted as
    UCG workspace.
    """

    if state_ancillas < 0:
        raise ValueError("state_ancillas must be nonnegative.")
    if final:
        return state_ancillas
    return max(0, state_ancillas - 1)


def frame_layer_ucg_qubits(n: int, depth: int) -> int:
    """Return the UCG width, including its target, for one frame layer."""

    _validate_n(n)
    if not 0 <= depth < n:
        raise ValueError("depth must lie in 0, ..., n-1.")
    return depth + 2 if depth < n - 1 else n


def ucg_depth_proxy(total_qubits: int, work_ancillas: int) -> tuple[int, int]:
    """Expose the terms in ``O(k + 2**k/(k+m))`` with unit coefficients."""

    if total_qubits < 1:
        raise ValueError("total_qubits must be positive.")
    if work_ancillas < 0:
        raise ValueError("work_ancillas must be nonnegative.")
    linear = total_qubits
    exponential = math.ceil(
        (1 << total_qubits) / (total_qubits + work_ancillas)
    )
    return linear, exponential


def geometric_tail_sum(n: int, denominator_shift: int) -> float:
    """Return ``sum(2**k/(k+s), k=1..n)`` for audit checks."""

    _validate_n(n)
    if denominator_shift < 0:
        raise ValueError("denominator_shift must be nonnegative.")
    return sum(
        (1 << k) / (k + denominator_shift) for k in range(1, n + 1)
    )


def geometric_tail_upper_bound(n: int, denominator_shift: int) -> float:
    """Return the proved uniform upper bound ``6*2**n/(n+s)``."""

    _validate_n(n)
    if denominator_shift < 0:
        raise ValueError("denominator_shift must be nonnegative.")
    return 6.0 * (1 << n) / (n + denominator_shift)


def unary_prefix_depth_proxy(n: int, t: int) -> int:
    """Expose clean unary-prefix contributions with unit coefficients."""

    _validate_n_t(n, t)
    if t == 0:
        return 0
    if t == n:
        return 3 * t  # encode, t Givens layers, decode
    return 2 * t + t + 2 * (n - t) + 2 * t


def unary_prefix_size_proxy(n: int, t: int) -> int:
    """Expose the corrected prefix-size form ``O(2**t + n - t)``."""

    _validate_n_t(n, t)
    if t == 0:
        return 0
    return (1 << t) + (n - t)


def ancilla_depth_row(n: int, state_ancillas: int) -> AncillaDepthRow:
    """Return one audited resource term ledger."""

    _validate_n(n)
    if state_ancillas < 0:
        raise ValueError("state_ancillas must be nonnegative.")

    N = 1 << n
    t = hybrid_prefix_qubits(n, state_ancillas)
    prefix_depth = unary_prefix_depth_proxy(n, t)
    prefix_size = unary_prefix_size_proxy(n, t)
    tail_predicate_depth = 0
    ucg_linear = 0
    ucg_exponential = 0
    ucg_size = 0
    for depth in range(t, n):
        final = depth == n - 1
        suffix_width = n - depth - 1
        tail_predicate_depth += 2 * suffix_width
        width = frame_layer_ucg_qubits(n, depth)
        work = tail_ucg_work_ancillas(state_ancillas, final=final)
        linear, exponential = ucg_depth_proxy(width, work)
        ucg_linear += linear
        ucg_exponential += exponential
        ucg_size += 1 << width

    total_depth = (
        prefix_depth
        + tail_predicate_depth
        + ucg_linear
        + ucg_exponential
    )
    total_size = prefix_size + tail_predicate_depth + ucg_size
    return AncillaDepthRow(
        n=n,
        dimension=N,
        state_ancillas=state_ancillas,
        frame_ancillas_upper_bound=frame_ancilla_upper_bound(state_ancillas),
        unary_prefix_qubits=t,
        unary_prefix_ancilla_upper_bound=unary_prefix_ancilla_upper_bound(t),
        maximum_unary_control_copies=maximum_unary_control_copies(t),
        tail_layers=n - t,
        nonfinal_ucg_work_ancillas=(
            tail_ucg_work_ancillas(state_ancillas, final=False)
            if t < n - 1
            else 0
        ),
        final_ucg_work_ancillas=(
            tail_ucg_work_ancillas(state_ancillas, final=True)
            if t < n
            else 0
        ),
        prefix_depth_proxy=prefix_depth,
        tail_predicate_depth_proxy=tail_predicate_depth,
        ucg_linear_depth_proxy=ucg_linear,
        ucg_exponential_depth_proxy=ucg_exponential,
        total_frame_depth_proxy=total_depth,
        prefix_size_proxy=prefix_size,
        tail_predicate_size_proxy=tail_predicate_depth,
        ucg_size_proxy=ucg_size,
        total_frame_size_proxy=total_size,
        candidate_geometric_term=math.ceil(N / (n + state_ancillas)),
        candidate_sequential_term=n * (n - t + 1),
        optimal_qsp_linear_term=n,
        optimal_qsp_geometric_term=math.ceil(N / (n + state_ancillas)),
        logical_hopf_rotations=N - 1,
        recordwise_decode_operations_per_shot=N,
    )


def ancilla_depth_rows(
    n: int, state_ancillas: Iterable[int]
) -> tuple[AncillaDepthRow, ...]:
    return tuple(ancilla_depth_row(n, int(value)) for value in state_ancillas)
