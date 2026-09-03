"""Exact-distribution and output-sensitive decoders for Hopf records."""
from __future__ import annotations

import numpy as np

from .conventions import marker_label, parity


def fwht(values: object) -> np.ndarray:
    """Return the unnormalized Walsh--Hadamard transform of a copy."""

    out = np.asarray(values, dtype=float).reshape(-1).copy()
    length = out.size
    if length == 0 or length & (length - 1):
        raise ValueError("FWHT input length must be a positive power of two.")
    width = 1
    while width < length:
        for start in range(0, length, 2 * width):
            first = out[start : start + width].copy()
            second = out[start + width : start + 2 * width].copy()
            out[start : start + width] = first + second
            out[start + width : start + 2 * width] = first - second
        width *= 2
    return out


def reshape_ancilla_system(probabilities: object) -> np.ndarray:
    probs = np.asarray(probabilities, dtype=float).reshape(-1)
    if probs.size < 4 or probs.size & (probs.size - 1):
        raise ValueError(
            "Probability vector must describe one ancilla and at least one system qubit."
        )
    return probs.reshape(2, probs.size // 2)


def signed_system_histogram(probabilities: object) -> np.ndarray:
    probs = reshape_ancilla_system(probabilities)
    return probs[0] - probs[1]


def global_moments_direct(probabilities: object) -> np.ndarray:
    signed = signed_system_histogram(probabilities)
    N = signed.size
    moments = np.zeros(N, dtype=float)
    for label in range(N):
        moments[label] = sum(
            value * (-1.0 if parity(label, outcome) else 1.0)
            for outcome, value in enumerate(signed)
        )
    return moments


def global_moments_fwht(probabilities: object) -> np.ndarray:
    return fwht(signed_system_histogram(probabilities))


def walsh_character_from_outcome(system_label: int, n: int) -> np.ndarray:
    """Generate all ``(-1)**parity(k, y)`` entries in ``O(2**n)`` work."""

    if n < 1:
        raise ValueError("n must be positive.")
    N = 1 << n
    try:
        label = int(system_label)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            "system_label must be an integer in 0, ..., 2**n - 1."
        ) from exc
    if label != system_label or not 0 <= label < N:
        raise ValueError(
            "system_label must be an integer in 0, ..., 2**n - 1."
        )

    character = np.empty(N, dtype=float)
    character[0] = 1.0
    width = 1
    for bit in range(n):
        sign = -1.0 if (label >> bit) & 1 else 1.0
        character[width : 2 * width] = sign * character[:width]
        width *= 2
    return character


def _integer_outcomes(values: object, *, name: str) -> np.ndarray:
    try:
        flat = np.asarray(values).reshape(-1)
        valid = np.all(np.isfinite(flat)) and np.all(flat == np.floor(flat))
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite integers.") from exc
    if not valid:
        raise ValueError(f"{name} must contain finite integers.")
    return flat.astype(np.int64)


def global_moments_recordwise(
    ancilla_bits: object,
    system_labels: object,
    n: int,
) -> np.ndarray:
    """Average all Walsh moments directly from measured outcomes.

    The arithmetic cost is ``O(S * 2**n)`` for ``S`` outcomes, and the storage
    cost is ``O(2**n)``.
    """

    if n < 1:
        raise ValueError("n must be positive.")
    ancilla = _integer_outcomes(ancilla_bits, name="ancilla_bits")
    labels = _integer_outcomes(system_labels, name="system_labels")
    if ancilla.size != labels.size:
        raise ValueError("ancilla_bits and system_labels must have the same length.")
    if ancilla.size == 0:
        raise ValueError("At least one measured outcome is required.")
    if np.any((ancilla < 0) | (ancilla > 1)):
        raise ValueError("ancilla_bits must contain only 0 and 1.")
    N = 1 << n
    if np.any((labels < 0) | (labels >= N)):
        raise ValueError("system_labels must lie in 0, ..., 2**n - 1.")

    moments = np.zeros(N, dtype=float)
    for ancilla_bit, system_label in zip(ancilla, labels, strict=True):
        branch_sign = -1.0 if ancilla_bit else 1.0
        moments += branch_sign * walsh_character_from_outcome(
            int(system_label), n
        )
    return moments / ancilla.size


def decode_balanced_magnitude_gradient(
    probabilities: object,
    sqrt_metric: object,
    n: int,
    *,
    use_fwht: bool = True,
) -> np.ndarray:
    """Decode all magnitude derivatives from an exact output distribution."""

    metric = np.asarray(sqrt_metric, dtype=float).reshape(-1)
    if metric.size != (1 << n) - 1:
        raise ValueError("sqrt_metric length does not match n.")
    moments = (
        global_moments_fwht(probabilities)
        if use_fwht
        else global_moments_direct(probabilities)
    )
    return np.asarray(
        [
            2.0 * metric[node - 1] * moments[marker_label(node, n)]
            for node in range(1, 1 << n)
        ],
        dtype=float,
    )


def decode_balanced_magnitude_samples_recordwise(
    ancilla_bits: object,
    system_labels: object,
    sqrt_metric: object,
    n: int,
) -> np.ndarray:
    """Decode the complete magnitude gradient directly from measured outcomes."""

    metric = np.asarray(sqrt_metric, dtype=float).reshape(-1)
    if metric.size != (1 << n) - 1:
        raise ValueError("sqrt_metric length does not match n.")
    moments = global_moments_recordwise(ancilla_bits, system_labels, n)
    return np.asarray(
        [
            2.0 * metric[node - 1] * moments[marker_label(node, n)]
            for node in range(1, 1 << n)
        ],
        dtype=float,
    )


def phase_record(ancilla_bit: int, leaf: int, dimension: int) -> np.ndarray:
    """Return the norm-two signed one-hot complex phase-gradient record."""

    if ancilla_bit not in (0, 1):
        raise ValueError("ancilla_bit must be 0 or 1.")
    if dimension < 1 or dimension & (dimension - 1):
        raise ValueError("dimension must be a positive power of two.")
    if not 0 <= leaf < dimension:
        raise ValueError("leaf is outside the phase-gradient vector.")
    record = np.zeros(dimension, dtype=float)
    record[leaf] = 2.0 * (-1.0 if ancilla_bit else 1.0)
    return record


def decode_phase_gradient(probabilities: object) -> np.ndarray:
    """Decode the complete phase gradient from an exact joint distribution."""

    probs = reshape_ancilla_system(probabilities)
    return 2.0 * (probs[0] - probs[1])


def decode_phase_samples(
    ancilla_bits: object,
    leaf_labels: object,
    dimension: int,
) -> np.ndarray:
    """Decode phase-gradient samples in ``O(S + dimension)`` work."""

    if dimension < 1 or dimension & (dimension - 1):
        raise ValueError("dimension must be a positive power of two.")
    ancilla = _integer_outcomes(ancilla_bits, name="ancilla_bits")
    leaves = _integer_outcomes(leaf_labels, name="leaf_labels")
    if ancilla.size != leaves.size:
        raise ValueError("ancilla_bits and leaf_labels must have the same length.")
    if ancilla.size == 0:
        raise ValueError("At least one measured outcome is required.")
    if np.any((ancilla < 0) | (ancilla > 1)):
        raise ValueError("ancilla_bits must contain only 0 and 1.")
    if np.any((leaves < 0) | (leaves >= dimension)):
        raise ValueError("leaf_labels lie outside the phase-gradient vector.")
    weights = np.where(ancilla == 0, 2.0, -2.0)
    return np.bincount(leaves, weights=weights, minlength=dimension) / ancilla.size


def decode_checkpoint_gradient(
    probabilities: object,
    n: int,
    depth: int,
) -> np.ndarray:
    """Decode one complete checkpoint depth block from exact probabilities.

    The flattened distribution is ancilla-major. System labels are big-endian;
    the checkpoint target is system index ``depth``. Lower-suffix outcomes are
    summed out exactly.
    """

    if n < 1:
        raise ValueError("n must be positive.")
    if not 0 <= depth < n:
        raise ValueError("depth must lie in 0, ..., n-1.")
    probs = reshape_ancilla_system(probabilities)
    if probs.shape[1] != 1 << n:
        raise ValueError("Probability vector does not match n.")
    width = 1 << depth
    result = np.zeros(width, dtype=float)
    target_shift = n - depth - 1
    for ancilla in (0, 1):
        for system_label in range(1 << n):
            prefix = system_label >> (n - depth) if depth else 0
            target = (system_label >> target_shift) & 1
            sign = -2.0 * (-1.0 if (ancilla + target) & 1 else 1.0)
            result[prefix] += sign * probs[ancilla, system_label]
    return result


def checkpoint_record(
    ancilla_bit: int,
    target_bit: int,
    prefix: int,
    width: int,
) -> np.ndarray:
    """Return the norm-two one-hot checkpoint score record."""

    if ancilla_bit not in (0, 1) or target_bit not in (0, 1):
        raise ValueError("ancilla_bit and target_bit must be 0 or 1.")
    if width < 1 or width & (width - 1):
        raise ValueError("width must be a positive power of two.")
    if not 0 <= prefix < width:
        raise ValueError("prefix lies outside the checkpoint block.")
    record = np.zeros(width, dtype=float)
    record[prefix] = -2.0 * (
        -1.0 if (ancilla_bit + target_bit) & 1 else 1.0
    )
    return record
