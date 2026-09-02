"""Exact-distribution and output-sensitive decoders for global Hopf records."""
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
