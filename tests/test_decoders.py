from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.conventions import parity
from compiler_robust_hopf.decoders import (
    decode_balanced_magnitude_gradient,
    decode_balanced_magnitude_samples_recordwise,
    decode_phase_gradient,
    decode_phase_samples,
    fwht,
    global_moments_direct,
    global_moments_fwht,
    global_moments_recordwise,
    phase_record,
    walsh_character_from_outcome,
)


class DecoderTests(unittest.TestCase):
    def test_fwht_matches_dense_hadamard(self) -> None:
        rng = np.random.default_rng(123)
        for n in range(1, 7):
            values = rng.normal(size=1 << n)
            dense = np.asarray([[1.0]])
            h = np.asarray([[1.0, 1.0], [1.0, -1.0]])
            for _ in range(n):
                dense = np.kron(dense, h)
            np.testing.assert_allclose(
                fwht(values), dense @ values, atol=1e-12, rtol=0.0
            )

    def test_direct_and_fwht_global_moments(self) -> None:
        rng = np.random.default_rng(456)
        probabilities = rng.uniform(size=32)
        probabilities /= probabilities.sum()
        np.testing.assert_allclose(
            global_moments_direct(probabilities),
            global_moments_fwht(probabilities),
            atol=1e-12,
            rtol=0.0,
        )

    def test_walsh_character_matches_direct_parity(self) -> None:
        for n in range(1, 7):
            N = 1 << n
            for outcome in range(N):
                expected = np.asarray(
                    [
                        -1.0 if parity(label, outcome) else 1.0
                        for label in range(N)
                    ]
                )
                np.testing.assert_array_equal(
                    walsh_character_from_outcome(outcome, n), expected
                )

    def test_recordwise_decoder_matches_empirical_fwht(self) -> None:
        rng = np.random.default_rng(260905)
        for n in range(1, 7):
            N = 1 << n
            shots = 3 * n + 1
            ancilla = rng.integers(0, 2, size=shots)
            labels = rng.integers(0, N, size=shots)
            probabilities = np.zeros(2 * N, dtype=float)
            for bit, label in zip(ancilla, labels, strict=True):
                probabilities[int(bit) * N + int(label)] += 1.0 / shots
            np.testing.assert_allclose(
                global_moments_recordwise(ancilla, labels, n),
                global_moments_fwht(probabilities),
                atol=1e-12,
                rtol=0.0,
            )
            sqrt_metric = rng.uniform(0.0, 1.0, size=N - 1)
            np.testing.assert_allclose(
                decode_balanced_magnitude_samples_recordwise(
                    ancilla, labels, sqrt_metric, n
                ),
                decode_balanced_magnitude_gradient(
                    probabilities, sqrt_metric, n
                ),
                atol=1e-12,
                rtol=0.0,
            )

    def test_phase_sample_decoder_matches_empirical_distribution(self) -> None:
        rng = np.random.default_rng(260911)
        for n in range(1, 8):
            N = 1 << n
            shots = 5 * n + 3
            ancilla = rng.integers(0, 2, size=shots)
            leaves = rng.integers(0, N, size=shots)
            probabilities = np.zeros(2 * N, dtype=float)
            for bit, leaf in zip(ancilla, leaves, strict=True):
                probabilities[int(bit) * N + int(leaf)] += 1.0 / shots
            np.testing.assert_allclose(
                decode_phase_samples(ancilla, leaves, N),
                decode_phase_gradient(probabilities),
                atol=1e-12,
                rtol=0.0,
            )

    def test_phase_records_have_fixed_norm_two(self) -> None:
        for N in (2, 4, 8, 16, 32):
            for bit in (0, 1):
                for leaf in range(N):
                    self.assertEqual(
                        np.linalg.norm(phase_record(bit, leaf, N)),
                        2.0,
                    )

    def test_recordwise_decoder_rejects_invalid_outcomes(self) -> None:
        with self.assertRaises(ValueError):
            global_moments_recordwise([], [], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 1], [0], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 2], [0, 1], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 1], [0, 4], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0.0, 0.5], [0, 1], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 1], [0, np.nan], 2)
        with self.assertRaises(ValueError):
            walsh_character_from_outcome(np.nan, 2)
        with self.assertRaises(ValueError):
            decode_phase_samples([], [], 4)
        with self.assertRaises(ValueError):
            decode_phase_samples([0, 1], [0], 4)
        with self.assertRaises(ValueError):
            decode_phase_samples([0, 2], [0, 1], 4)
        with self.assertRaises(ValueError):
            decode_phase_samples([0, 1], [0, 4], 4)
        with self.assertRaises(ValueError):
            phase_record(0, 0, 3)


if __name__ == "__main__":
    unittest.main()
