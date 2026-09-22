"""Finite audits of one-clean-bit masked phase batching.

Integer tests exhaust every dirty basis input in the stated small ranges.
Exact native checks use Q(sqrt(2), i); the small complex128 test separately
exercises full output error for a nondiagonal approximate phase bank. These
are circuit/contract checks, not a high-precision synthesis implementation.
"""
from __future__ import annotations

from fractions import Fraction
import unittest

import numpy as np

from verification.fault_tolerant.exact_arithmetic import CQ2, Q2, CO, CZ


def _mcx(controls, target, helpers):
    """Chronological X/CX/CCX word; every helper is arbitrary and restored."""
    controls = tuple(controls)
    k = len(controls)
    if k <= 2:
        return [(('X', 'CX', 'CCX')[k], *controls, target)]
    assert len(helpers) >= k - 2
    a = helpers[:k - 2]
    first = [('CCX', controls[0], controls[1], a[0])]
    chain = [('CCX', controls[j], a[j - 2], a[j - 1])
             for j in range(2, k - 1)]
    last = [('CCX', controls[-1], a[-1], target)]
    return (first + chain + last + chain[::-1] + first
            + chain + last + chain[::-1])


def _increment(control, accumulator, helpers):
    return [gate for j in reversed(range(len(accumulator)))
            for gate in _mcx([control, *accumulator[:j]], accumulator[j], helpers)]


def _population_add(m):
    t = m.bit_length()  # ceil(log2(m + 1)), including powers of two.
    r = t + 1
    accumulator = list(range(m, m + r))
    helpers = list(range(m + r, m + r + r - 2))
    word = [gate for control in range(m)
            for gate in _increment(control, accumulator, helpers)]
    return t, r, helpers, word


def _permutation_word(state, word):
    for gate in word:
        if all((state >> control) & 1 for control in gate[1:-1]):
            state ^= 1 << gate[-1]
    return state


def _native_ccx(a, b, c):
    # Literal seven-T Toffoli, with no relative or global phase.
    return [('H', c), ('CX', b, c), ('TDG', c), ('CX', a, c),
            ('T', c), ('CX', b, c), ('TDG', c), ('CX', a, c),
            ('T', b), ('T', c), ('H', c), ('CX', a, b),
            ('T', a), ('TDG', b), ('CX', a, b)]


def _native(word):
    return [native_gate for gate in word for native_gate in
            (_native_ccx(*gate[1:]) if gate[0] == 'CCX' else [gate])]


def _adjoint(word):
    inverse = {'T': 'TDG', 'TDG': 'T'}
    return [(inverse.get(gate[0], gate[0]), *gate[1:]) for gate in reversed(word)]


ROOT_HALF = CQ2(Q2(0, Fraction(1, 2)))
OMEGA = CQ2(Q2(0, Fraction(1, 2)), Q2(0, Fraction(1, 2)))


def _exact_apply(state, word):
    for gate in word:
        result = {}
        for basis, amplitude in state.items():
            if gate[0] == 'H':
                target = gate[1]
                low = basis & ~(1 << target)
                sign = -1 if (basis >> target) & 1 else 1
                for output, factor in ((low, ROOT_HALF),
                                       (low | (1 << target), sign * ROOT_HALF)):
                    result[output] = result.get(output, CZ) + factor * amplitude
            elif gate[0] in ('T', 'TDG'):
                phase = OMEGA if gate[0] == 'T' else OMEGA.conj()
                result[basis] = amplitude * (phase if (basis >> gate[1]) & 1 else CO)
            else:
                output = _permutation_word(basis, [gate])
                result[output] = result.get(output, CZ) + amplitude
        state = {key: value for key, value in result.items() if value != CZ}
    return state


def _signed_phase_fixture(weights, theta, perturbation, scalar, r=None):
    """Full permutation-matrix offset macros, not native offset emitters.

    A spectator bit models an arbitrary returned arithmetic helper. The
    separate literature bound pays for implementing these exact permutations.
    """
    m = len(weights)
    if r is None:
        r = sum(abs(weight) for weight in weights).bit_length() + 1
    q = 1 << (r - 1)
    assert q > sum(abs(weight) for weight in weights)
    mask = (1 << r) - 1
    size = 1 << (m + r + 1)
    center = sum(max(-weight, 0) for weight in weights)

    def h(basis):
        return sum(weight for j, weight in enumerate(weights) if (basis >> j) & 1)

    def add_to_accumulator(basis, offset):
        old = (basis >> m) & mask
        return (basis & ~(mask << m)) | (((old + offset) & mask) << m)

    arithmetic_images = [add_to_accumulator(basis, h(basis)) for basis in range(size)]
    center_images = [add_to_accumulator(basis, center) for basis in range(size)]
    arithmetic = np.eye(size, dtype=complex)[np.argsort(arithmetic_images)]
    centering = np.eye(size, dtype=complex)[np.argsort(center_images)]
    phase = np.diag([np.exp(1j * theta * ((basis >> m) & mask)) for basis in range(size)])
    top = m + r - 1
    flip = np.eye(size, dtype=complex)[[basis ^ (1 << top) for basis in range(size)]]
    error_unitary = np.cos(perturbation) * np.eye(size) + 1j * np.sin(perturbation) * flip
    compiled = np.exp(1j * scalar) * error_unitary @ phase
    actual = (centering.conj().T @ arithmetic.conj().T @ compiled @ arithmetic
              @ compiled.conj().T @ centering)
    ideal = (centering.conj().T @ arithmetic.conj().T @ phase @ arithmetic
             @ phase.conj().T @ centering)
    columns = [basis for basis in range(size) if not ((basis >> top) & 1)]
    embedding = np.eye(size, dtype=complex)[:, columns]
    target = np.diag([np.exp(1j * theta * h(basis)) for basis in columns])
    delta = np.linalg.norm(compiled - np.exp(1j * scalar) * phase, ord=2)
    leaked_rows = [basis for basis in range(size) if (basis >> top) & 1]
    return actual, ideal, embedding, target, delta, leaked_rows


class IdenticalPhaseBatchingTests(unittest.TestCase):
    def test_borrowed_mcx_every_dirty_basis_input(self):
        for k in range(1, 7):
            helpers = list(range(k + 1, k + 1 + max(0, k - 2)))
            word = _mcx(range(k), k, helpers)
            expected_count = 0 if k == 1 else 1 if k == 2 else 4 * k - 8
            self.assertEqual(sum(g[0] == 'CCX' for g in word), expected_count)
            for basis in range(1 << (k + 1 + len(helpers))):
                expected = basis ^ ((1 << k) if basis & ((1 << k) - 1)
                                    == (1 << k) - 1 else 0)
                self.assertEqual(_permutation_word(basis, word), expected)
                self.assertEqual(_permutation_word(expected, word[::-1]), basis)

    def test_increment_every_accumulator_and_helper_input(self):
        for r in range(2, 7):
            accumulator = list(range(1, r + 1))
            helpers = list(range(r + 1, 2 * r - 1))
            word = _increment(0, accumulator, helpers)
            self.assertEqual(sum(g[0] == 'CCX' for g in word),
                             2 * (r - 2) * (r - 1) + 1)
            mask = (1 << r) - 1
            for basis in range(1 << (2 * r - 1)):
                old = (basis >> 1) & mask
                new = (old + (basis & 1)) & mask
                expected = (basis & ~(mask << 1)) | (new << 1)
                self.assertEqual(_permutation_word(basis, word), expected)
                self.assertEqual(_permutation_word(expected, word[::-1]), basis)

    def test_batch_integer_phase_and_complete_return(self):
        for m in range(1, 7):
            t, r, helpers, word = _population_add(m)
            q = 1 << t
            self.assertEqual(len(helpers), t - 1)
            for x in range(1 << m):
                h = x.bit_count()
                for y in range(q):
                    for helper in range(1 << len(helpers)):
                        basis = x | (y << m) | (helper << (m + r))
                        after = _permutation_word(basis, word)
                        self.assertEqual(after, x | ((y + h) << m)
                                         | (helper << (m + r)))
                        # D after A minus D before A: identity for every real angle.
                        self.assertEqual(((after >> m) & (2 * q - 1)) - y, h)
                        self.assertEqual(_permutation_word(after, word[::-1]), basis)

    def test_without_clean_overflow_bit_wrap_changes_phase(self):
        m = 3
        q = 1 << m.bit_length()
        y = q - 1
        self.assertNotEqual((y + m) % q - y, m)
        self.assertEqual((y + m) % q - y, m - q)

    def test_literal_seven_t_toffoli(self):
        word = _native_ccx(0, 1, 2)
        self.assertEqual(sum(g[0] in ('T', 'TDG') for g in word), 7)
        for basis in range(8):
            expected = _permutation_word(basis, [('CCX', 0, 1, 2)])
            self.assertEqual(_exact_apply({basis: CO}, word), {expected: CO})

    def test_exact_native_batch_preserves_reference_coherence(self):
        m = 2
        t, r, helpers, word = _population_add(m)
        arithmetic = _native(word)
        phase = [('T', m + j) for j in range(r) for _ in range(1 << j)]
        compiled = _adjoint(phase) + arithmetic + phase + _adjoint(arithmetic)
        width = m + r + len(helpers)
        # Distinct reference labels purify the entire permitted input space.
        # Unnormalized coefficients suffice for an exact linear identity.
        initial, expected = {}, {}
        label = 0
        for x in range(1 << m):
            for y in range(1 << t):
                for helper in range(1 << len(helpers)):
                    basis = x | (y << m) | (helper << (m + r)) | (label << width)
                    coefficient = CQ2(Q2(label + 1), Q2(1 - label))
                    target_phase = CO
                    for _ in range(x.bit_count()):
                        target_phase *= OMEGA
                    initial[basis] = coefficient
                    expected[basis] = coefficient * target_phase
                    label += 1
        self.assertEqual(_exact_apply(initial, compiled), expected)

    def test_nondiagonal_approximation_full_output_error(self):
        m = 2
        t, r, helpers, word = _population_add(m)
        width = m + r + len(helpers)
        size = 1 << width
        images = [_permutation_word(basis, word) for basis in range(size)]
        arithmetic = np.eye(size, dtype=complex)[np.argsort(images)]
        theta, perturbation, scalar = 0.231, 0.017, 0.413
        phase = np.diag([np.exp(1j * theta * ((basis >> m) & ((1 << r) - 1)))
                         for basis in range(size)])
        top = m + t
        flip = np.eye(size, dtype=complex)[[basis ^ (1 << top) for basis in range(size)]]
        error_unitary = np.cos(perturbation) * np.eye(size) + 1j * np.sin(perturbation) * flip
        compiled = np.exp(1j * scalar) * error_unitary @ phase
        actual = arithmetic.conj().T @ compiled @ arithmetic @ compiled.conj().T
        columns = [basis for basis in range(size) if not ((basis >> top) & 1)]
        expected = np.eye(size, dtype=complex)[:, columns] @ np.diag([
            np.exp(1j * theta * (basis & ((1 << m) - 1)).bit_count()) for basis in columns])
        delta = np.linalg.norm(compiled - np.exp(1j * scalar) * phase, ord=2)
        full_error = np.linalg.norm(actual[:, columns] - expected, ord=2)
        self.assertLessEqual(full_error, 2 * delta + 2e-12)
        self.assertGreater(full_error, 1e-4)
        leaked_rows = [basis for basis in range(size) if (basis >> top) & 1]
        self.assertGreater(np.linalg.norm(actual[np.ix_(leaked_rows, columns)]), 1e-4)
        without_scalar = arithmetic.conj().T @ (error_unitary @ phase) @ arithmetic @ (error_unitary @ phase).conj().T
        np.testing.assert_allclose(actual, without_scalar, atol=2e-12, rtol=0)

    def test_signed_centering_integer_phase_and_all_dirty_return(self):
        # Exact macro identities for signed offsets. No native cost inferred.
        fixtures = [(-2, 1), (-1, 0, 3), (3, -4, 2), (-2, -1),
                    (0, 0), (4, -4), (1, 2, 3)]
        for weights in fixtures:
            m = len(weights)
            total = sum(abs(weight) for weight in weights)
            q = 1 << total.bit_length()
            modulus = 2 * q
            center = sum(max(-weight, 0) for weight in weights)
            for x in range(1 << m):
                h = sum(weight for j, weight in enumerate(weights) if (x >> j) & 1)
                for y in range(q):
                    for helper in range(4):
                        # Chronological R, D†, A, D, A†, R†.
                        centered = (y + center) % modulus
                        shifted = (centered + h) % modulus
                        self.assertEqual(centered, y + center)
                        self.assertEqual(shifted, y + center + h)
                        self.assertEqual(shifted - centered, h)
                        after_inverse = (shifted - h - center) % modulus
                        self.assertEqual((x, after_inverse, helper), (x, y, helper))

    def test_negative_weight_requires_centering_for_general_angle(self):
        weights = (-3, 2)
        q = 1 << sum(abs(weight) for weight in weights).bit_length()
        modulus = 2 * q
        y, h = 0, weights[0]
        self.assertEqual((y + h) % modulus - y, h + modulus)
        self.assertNotEqual((y + h) % modulus - y, h)
        center = sum(max(-weight, 0) for weight in weights)
        self.assertEqual((y + center + h) % modulus - (y + center), h)

    def test_signed_batch_nondiagonal_full_output_and_actual_inverse(self):
        actual, ideal, embedding, target, delta, leaked_rows = _signed_phase_fixture(
            (-1, 2), theta=0.317, perturbation=0.019, scalar=-0.231)
        np.testing.assert_allclose(ideal @ embedding, embedding @ target, atol=2e-12, rtol=0)
        full_error = np.linalg.norm(actual @ embedding - embedding @ target, ord=2)
        self.assertLessEqual(full_error, 2 * delta + 2e-12)
        self.assertGreater(full_error, 1e-4)
        self.assertGreater(np.linalg.norm((actual @ embedding)[leaked_rows]), 1e-4)
        # A common scalar is canceled by the actual adjoint of the same C.
        without_scalar = _signed_phase_fixture(
            (-1, 2), theta=0.317, perturbation=0.019, scalar=0)[0]
        np.testing.assert_allclose(actual, without_scalar, atol=2e-12, rtol=0)

    def test_two_signed_bases_reuse_clean_bit_with_leakage(self):
        first = _signed_phase_fixture((-1, 2), 0.317, 0.019, -0.231)
        second = _signed_phase_fixture((2, -1), -0.413, -0.013, 0.127)
        v1, _, embedding, target1, delta1, leaked_rows = first
        v2, _, embedding2, target2, delta2, _ = second
        np.testing.assert_array_equal(embedding, embedding2)
        self.assertGreater(np.linalg.norm((v1 @ embedding)[leaked_rows]), 1e-4)
        # No projection, initialization, or reset between the two actual words.
        actual = v2 @ v1 @ embedding
        expected = embedding @ target2 @ target1
        full_error = np.linalg.norm(actual - expected, ord=2)
        self.assertLessEqual(full_error, 2 * (delta1 + delta2) + 3e-12)
        self.assertGreater(full_error, 1e-4)


if __name__ == '__main__':
    unittest.main()
