"""Strict-zero-workspace exploration from the Möttönen completion.

The positive-workspace theorem uses one clean predicate bit in its direct base
case.  This module asks what can be recovered when no additional qubit is
available.  It contains two exact operator factorizations and transparent
asymptotic term ledgers; it does not emit a low-level hardware circuit.

The first factorization views one addressed Hopf layer as a smaller Möttönen
uniformly controlled ``R_y`` circuit conditioned on a zero lower suffix.  If
that smaller circuit is controlled gate by gate, exact no-workspace
multi-controlled-gate decompositions give total ``O(2**n)`` size but only the
currently proved ``O(2**n)`` depth.

The second factorization compares the full Hopf frame ``W_n`` with the ordinary
Möttönen state-preparation completion ``U_n``.  Their correction is a direct
sum of inverse prefix completions indexed by the position of the rightmost one
in the computational-basis label.

All qubits in this file are ordered from most significant to least significant.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable

import numpy as np

from .frames import direct_addressed_depth_layer, direct_real_frame, hopf_ry


@dataclass(frozen=True)
class StrictZeroMottonenRow:
    """One transparent strict-zero-workspace resource row.

    The ``*_proxy`` fields expose asymptotic weighted sums with unit
    coefficients.  They are not exact elementary-gate counts.  The linear
    proxy corresponds to exact linear-size no-workspace decompositions of
    multi-controlled ``SU(2)`` and ``X`` gates; the quadratic proxy is a more
    conservative Barenco-style fallback.  Either proxy is ``O(2**n)``.
    """

    n: int
    dimension: int
    clean_ancillas: int
    hopf_angles: int
    mottonen_completion_primitive_upper_bound: int
    direct_conditioned_linear_size_proxy: int
    direct_conditioned_quadratic_size_proxy: int
    direct_sequential_depth_proxy: int
    rightmost_one_correction_blocks: int
    completion_correction_quadratic_size_proxy: int
    completion_plus_correction_size_proxy: int
    optimal_size_scale: int
    current_depth_upper_scale: int
    optimal_depth_target_proxy: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _validate_depth(n: int, depth: int) -> None:
    _validate_n(n)
    if not 0 <= depth < n:
        raise ValueError("depth must lie in 0, ..., n-1.")


def _angles_for_depth(angles: object, depth: int) -> np.ndarray:
    values = np.asarray(angles, dtype=float).reshape(-1)
    if values.size != 1 << depth:
        raise ValueError("angles must contain exactly 2**depth entries.")
    return values


def _theta_for_n(theta_mag: object, n: int) -> np.ndarray:
    _validate_n(n)
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    return values


def full_preparation_depth_layer(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Return the ordinary Möttönen preparation layer at one tree depth.

    Prefix ``p`` selects ``angles[p]`` on the depth target, independently of
    all lower suffix bits.  This is the full-unitary completion used for the
    standard breadth-first state-preparation cascade.
    """

    _validate_depth(n, depth)
    values = _angles_for_depth(angles, depth)
    suffix_width = n - depth - 1
    unitary = np.eye(1 << n, dtype=complex)
    for prefix, theta in enumerate(values):
        block = hopf_ry(float(theta))
        for suffix in range(1 << suffix_width):
            zero = (prefix << (n - depth)) | suffix
            one = zero | (1 << suffix_width)
            unitary[np.ix_([zero, one], [zero, one])] = block
    return unitary


def mottonen_completion(n: int, theta_mag: object) -> np.ndarray:
    """Return the full Möttönen-style state-preparation completion ``U_n``."""

    values = _theta_for_n(theta_mag, n)
    unitary = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(n):
        width = 1 << depth
        unitary = full_preparation_depth_layer(
            n, depth, values[offset : offset + width]
        ) @ unitary
        offset += width
    return unitary


def conditioned_small_completion_layer(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Condition a ``depth+1``-qubit UCR on the external suffix being zero.

    This is an independent construction of the addressed layer:

    ``V_d kron |0^s><0^s| + I kron (I-|0^s><0^s|)``,

    where ``V_d`` is the final Möttönen layer on ``depth+1`` qubits and
    ``s=n-depth-1``.
    """

    _validate_depth(n, depth)
    values = _angles_for_depth(angles, depth)
    active = full_preparation_depth_layer(depth + 1, depth, values)
    suffix_width = n - depth - 1
    suffix_dimension = 1 << suffix_width
    zero_projector = np.zeros(
        (suffix_dimension, suffix_dimension), dtype=complex
    )
    zero_projector[0, 0] = 1.0
    active_dimension = 1 << (depth + 1)
    return np.kron(active, zero_projector) + np.kron(
        np.eye(active_dimension, dtype=complex),
        np.eye(suffix_dimension, dtype=complex) - zero_projector,
    )


def conditioned_layer_residual(
    n: int,
    depth: int,
    angles: object,
) -> float:
    """Return the max-norm residual in the conditioned-UCR identity."""

    direct = direct_addressed_depth_layer(n, depth, angles)
    conditioned = conditioned_small_completion_layer(n, depth, angles)
    return float(np.max(np.abs(direct - conditioned)))


def rightmost_one_stratum_labels(n: int, position: int) -> tuple[int, ...]:
    """Return labels whose rightmost one is at ``position`` from the left.

    The first ``position`` bits are arbitrary, bit ``position`` is one, and all
    following bits are zero.  The stratum has dimension ``2**position``.
    """

    _validate_n(n)
    if not 0 <= position < n:
        raise ValueError("position must lie in 0, ..., n-1.")
    suffix_width = n - position - 1
    return tuple(
        (prefix << (n - position)) | (1 << suffix_width)
        for prefix in range(1 << position)
    )


def rightmost_one_partition(n: int) -> tuple[tuple[int, ...], ...]:
    """Return ``{|0^n>}`` followed by all rightmost-one strata."""

    _validate_n(n)
    return ((0,),) + tuple(
        rightmost_one_stratum_labels(n, position)
        for position in range(n)
    )


def prefix_completion(position: int, theta_mag: object) -> np.ndarray:
    """Return ``U_position`` from the first ``2**position-1`` angles."""

    if position < 0:
        raise ValueError("position must be nonnegative.")
    if position == 0:
        return np.eye(1, dtype=complex)
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    required = (1 << position) - 1
    if values.size < required:
        raise ValueError("theta_mag does not contain the required prefix angles.")
    return mottonen_completion(position, values[:required])


def completion_correction_matrix(n: int, theta_mag: object) -> np.ndarray:
    """Return the rightmost-one correction ``C_n`` in ``W_n = U_n C_n``.

    The all-zero line and the position-zero stratum are fixed.  On the stratum
    whose rightmost one occurs at position ``k>=1``, the correction is the
    inverse prefix completion ``U_k^dagger``.
    """

    values = _theta_for_n(theta_mag, n)
    correction = np.eye(1 << n, dtype=complex)
    for position in range(1, n):
        labels = rightmost_one_stratum_labels(n, position)
        inverse_prefix = prefix_completion(position, values).conj().T
        correction[np.ix_(labels, labels)] = inverse_prefix
    return correction


def completion_correction_factorized_frame(
    n: int, theta_mag: object
) -> np.ndarray:
    """Return ``U_n C_n`` from the Möttönen completion and correction."""

    values = _theta_for_n(theta_mag, n)
    return mottonen_completion(n, values) @ completion_correction_matrix(
        n, values
    )


def completion_correction_residual(n: int, theta_mag: object) -> float:
    """Return ``max|W_n-U_n C_n|``."""

    values = _theta_for_n(theta_mag, n)
    residual = direct_real_frame(n, values) - completion_correction_factorized_frame(
        n, values
    )
    return float(np.max(np.abs(residual)))


def layer_correction_matrix(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Return ``B_d=P_d^dagger A_d``.

    ``B_d`` is the identity on a zero lower suffix and applies the inverse full
    preparation layer on every nonzero lower suffix.
    """

    preparation = full_preparation_depth_layer(n, depth, angles)
    addressed = direct_addressed_depth_layer(n, depth, angles)
    return preparation.conj().T @ addressed


def layer_correction_product(n: int, theta_mag: object) -> np.ndarray:
    """Return ``B_0 B_1 ... B_(n-1)``, equal to ``C_n``."""

    values = _theta_for_n(theta_mag, n)
    correction = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(n):
        width = 1 << depth
        correction = correction @ layer_correction_matrix(
            n, depth, values[offset : offset + width]
        )
        offset += width
    return correction


def mottonen_ucr_primitive_upper_bound(depth: int) -> int:
    """Return a standard rotations-plus-CNOT primitive upper bound.

    The uncontrolled case is one rotation.  For ``depth>=1`` the standard
    Gray-code UCR uses at most ``2**depth`` rotations and ``2**depth`` CNOTs.
    """

    if depth < 0:
        raise ValueError("depth must be nonnegative.")
    return 1 if depth == 0 else 1 << (depth + 1)


def mottonen_completion_primitive_upper_bound(n: int) -> int:
    """Return ``2**(n+1)-3`` for the complete preparation cascade."""

    _validate_n(n)
    return sum(mottonen_ucr_primitive_upper_bound(depth) for depth in range(n))


def suffix_weighted_sum(n: int, *, power: int) -> int:
    """Return ``sum_d 2**d * (n-d)**power`` for ``power`` one or two."""

    _validate_n(n)
    if power not in (1, 2):
        raise ValueError("power must be one or two.")
    return sum((1 << depth) * (n - depth) ** power for depth in range(n))


def direct_conditioned_size_proxy(n: int, *, quadratic: bool) -> int:
    """Return a gate-control weighted strict-zero size proxy.

    The external suffix has ``n-depth-1`` open controls.  Adding those controls
    to every primitive of the smaller UCR costs polynomially in the number of
    controls and requires no clean workspace.  ``quadratic=True`` records the
    conservative square overhead; ``False`` records the available linear
    ``SU(2)``/multi-controlled-X scaling.  The ``X`` conjugations which turn
    open controls into positive controls are included once per layer.
    """

    _validate_n(n)
    total = 0
    for depth in range(n):
        active_control_width = n - depth
        overhead = active_control_width ** (2 if quadratic else 1)
        suffix_width = active_control_width - 1
        total += mottonen_ucr_primitive_upper_bound(depth) * overhead
        total += 2 * suffix_width
    return total


def completion_correction_size_proxy(n: int) -> int:
    """Return a conservative no-workspace proxy for the correction direct sum."""

    _validate_n(n)
    total = 0
    for position in range(1, n):
        external_controls = n - position
        prefix_primitives = mottonen_completion_primitive_upper_bound(position)
        total += prefix_primitives * (external_controls + 1) ** 2
        total += 2 * max(0, external_controls - 1)
    return total


def strict_zero_mottonen_row(n: int) -> StrictZeroMottonenRow:
    """Return one machine-readable strict-zero exploration row."""

    _validate_n(n)
    dimension = 1 << n
    completion = mottonen_completion_primitive_upper_bound(n)
    direct_linear = direct_conditioned_size_proxy(n, quadratic=False)
    direct_quadratic = direct_conditioned_size_proxy(n, quadratic=True)
    correction = completion_correction_size_proxy(n)
    return StrictZeroMottonenRow(
        n=n,
        dimension=dimension,
        clean_ancillas=0,
        hopf_angles=dimension - 1,
        mottonen_completion_primitive_upper_bound=completion,
        direct_conditioned_linear_size_proxy=direct_linear,
        direct_conditioned_quadratic_size_proxy=direct_quadratic,
        direct_sequential_depth_proxy=direct_quadratic,
        rightmost_one_correction_blocks=max(0, n - 1),
        completion_correction_quadratic_size_proxy=correction,
        completion_plus_correction_size_proxy=completion + correction,
        optimal_size_scale=dimension,
        current_depth_upper_scale=dimension,
        optimal_depth_target_proxy=n + math.ceil(dimension / n),
    )


def strict_zero_mottonen_rows(
    ns: Iterable[int],
) -> tuple[StrictZeroMottonenRow, ...]:
    """Return validated resource rows for an iterable of qubit counts."""

    return tuple(strict_zero_mottonen_row(int(n)) for n in ns)
