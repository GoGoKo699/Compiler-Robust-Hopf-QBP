"""Finite audits of the one-clean-bit identical-phase construction.

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


if __name__ == '__main__':
    unittest.main()
