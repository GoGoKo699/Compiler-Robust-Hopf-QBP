"""Tiny exact fixtures for the returned graph-source attenuation proof.

All matrix entries and comparisons are in Q(sqrt(2), i). These fixtures
exercise the proof's interfaces; finite examples do not establish its
general support-rank or algebraic-number lower bounds.
"""
from __future__ import annotations

from fractions import Fraction
import unittest

import numpy as np

from tests.test_identical_phase_batching import _exact_apply
from tests.test_operator_source_compiler import _source_word
from verification.fault_tolerant.exact_arithmetic import CQ2, Q2, CO, CZ, CI


ROOT_HALF = CQ2(Q2(0, Fraction(1, 2)))


def _identity(size):
    return np.array([[CO if row == col else CZ for col in range(size)]
                     for row in range(size)], dtype=object)


def _dagger(matrix):
    return np.array([[entry.conj() for entry in row] for row in matrix.T], dtype=object)


def _scale(matrix, scalar):
    return np.array([[entry * scalar for entry in row] for row in matrix], dtype=object)


def _trace(matrix):
    return sum((matrix[j, j] for j in range(len(matrix))), CZ)


def _native_matrix(width, word):
    # S, S-dagger and Z are expanded only for exact simulation. Their T-word
    # lengths here are not used for the proof's non-Clifford gate accounting.
    expanded = []
    for gate in word:
        if gate[0] in ('S', 'SDG', 'Z'):
            name, count = {'S': ('T', 2), 'SDG': ('TDG', 2), 'Z': ('T', 4)}[gate[0]]
            expanded.extend([(name, gate[1])] * count)
        else:
            expanded.append(gate)
    size = 1 << width
    result = np.array([[CZ for _ in range(size)] for _ in range(size)], dtype=object)
    for col in range(size):
        for row, amplitude in _exact_apply({col: CO}, expanded).items():
            result[row, col] = amplitude
    return result


def _pauli(width, xmask=0, zmask=0):
    size = 1 << width
    result = np.array([[CZ for _ in range(size)] for _ in range(size)], dtype=object)
    phase = [CO, CI, -CO, -CI][(xmask & zmask).bit_count() % 4]
    for col in range(size):
        result[col ^ xmask, col] = phase * (-1 if (col & zmask).bit_count() % 2 else 1)
    return result


def _binary_rank(labels):
    pivots = {}
    for label in labels:
        while label:
            pivot = label.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = label
                break
            label ^= pivots[pivot]
    return len(pivots)


def _graph_fixture():
    width, size = 3, 8
    native_source = _native_matrix(width, _source_word(width))
    gammas = [_pauli(width, 1 << j, (1 << j) - 1) for j in range(width)]
    source = native_source @ gammas[0] @ _dagger(native_source)
    identity = _identity(size)
    coefficients = [ROOT_HALF, CQ2(Fraction(1, 2)), CQ2(Fraction(1, 2))]
    expected_source = sum((_scale(gamma, coefficient)
                           for gamma, coefficient in zip(gammas, coefficients)),
                          np.array([[CZ] * size for _ in range(size)], dtype=object))
    np.testing.assert_array_equal(source, expected_source)
    np.testing.assert_array_equal(source @ source, identity)
    encoding = _scale(np.vstack([identity, source]), ROOT_HALF)
    complement = _scale(np.vstack([identity, -source]), ROOT_HALF)
    zero = np.array([[CZ] * size for _ in range(size)], dtype=object)
    selected = np.block([[zero, gammas[1]], [gammas[1], zero]])
    return source, encoding, complement, selected


class OperatorSourceReuseTests(unittest.TestCase):
    def test_native_t_expands_accepted_positive_operator_support(self):
        # One retained data qubit (bit 0), one private flag (bit 1).
        # Chronological T,H,CX measures a rotated X Pauli on the data.
        word = [('T', 0), ('H', 0), ('CX', 0, 1)]
        unitary = _native_matrix(2, word)
        accepted = unitary[:2, :2]
        positive = _dagger(accepted) @ accepted
        expected = _scale(_identity(2), CQ2(Fraction(1, 2)))
        expected += _scale(_pauli(1, 1, 0) - _pauli(1, 1, 1), ROOT_HALF / 2)
        np.testing.assert_array_equal(positive, expected)
        support = []
        for xmask in range(2):
            for zmask in range(2):
                coefficient = _trace(_pauli(1, xmask, zmask) @ positive) / 2
                if coefficient != CZ:
                    support.append(xmask | (zmask << 1))
        self.assertEqual(set(support), {0, 1, 3})  # I, X, Y.
        private_flags = 1
        t_count = sum(gate[0] in ('T', 'TDG') for gate in word)
        self.assertEqual(_binary_rank(support), private_flags + t_count)
        # Without T the same accepted operator has only one nonidentity label.
        clifford = _native_matrix(2, word[1:])[:2, :2]
        clifford_positive = _dagger(clifford) @ clifford
        np.testing.assert_array_equal(clifford_positive,
                                      _scale(_identity(2) + _pauli(1, 1), CQ2(Fraction(1, 2))))

    def test_mixed_acceptance_lattice_and_physical_field_conjugation(self):
        for phase in ('T', 'TDG'):
            # A spectator retained qubit is maximally mixed; the private flag
            # alone receives H, phase, H. Its acceptance is genuinely irrational.
            word = [('H', 1), (phase, 1), ('H', 1)]
            accepted = _native_matrix(2, word)[:2, :2]
            q = _trace(_dagger(accepted) @ accepted) / 2
            self.assertEqual(q, CQ2(Q2(Fraction(1, 2), Fraction(1, 4))))
            conjugate_word = [('H', 1), (phase, 1), ('Z', 1), ('H', 1)]
            conjugate_accepted = _native_matrix(2, conjugate_word)[:2, :2]
            physical_conjugate = _trace(_dagger(conjugate_accepted) @ conjugate_accepted) / 2
            field_conjugate = CQ2(Q2(q.real.a, -q.real.b))
            self.assertEqual(physical_conjugate, field_conjugate)
            self.assertEqual(q * physical_conjugate, CQ2(Fraction(1, 8)))
            self.assertGreater(q.real, Q2(0))
            self.assertLessEqual(q.real, Q2(1))
            self.assertGreater(physical_conjugate.real, Q2(0))
            self.assertLessEqual(physical_conjugate.real, Q2(1))
            # r=tau=1: 2^r sqrt(2)^tau q is 1+sqrt(2), with integral norm -1.
            numerator = q * CQ2(Q2(0, 2))
            self.assertEqual(numerator, CQ2(Q2(1, 1)))
            self.assertEqual(numerator.real.a ** 2 - 2 * numerator.real.b ** 2, -1)

    def test_scalar_graph_compression_has_exact_large_leakage(self):
        source, encoding, complement, selected = _graph_fixture()
        identity = _identity(8)
        coefficient = CQ2(Fraction(1, 2))  # j=2k-1=1 with k=1.
        np.testing.assert_array_equal(_dagger(encoding) @ encoding, identity)
        np.testing.assert_array_equal(_dagger(encoding) @ selected @ encoding,
                                      _scale(identity, coefficient))
        leakage = _dagger(complement) @ selected @ encoding
        np.testing.assert_array_equal(_dagger(leakage) @ leakage,
                                      _scale(identity, CQ2(Fraction(3, 4))))
        full_error = selected @ encoding - _scale(encoding, coefficient)
        np.testing.assert_array_equal(_dagger(full_error) @ full_error,
                                      _scale(identity, CQ2(Fraction(3, 4))))
        projector = encoding @ _dagger(encoding)
        np.testing.assert_array_equal(projector @ selected @ encoding,
                                      _scale(encoding, coefficient))
        zero = np.array([[CZ] * 8 for _ in range(8)], dtype=object)
        np.testing.assert_array_equal(_scale(projector, 2) - _identity(16),
                                      np.block([[zero, source], [source, zero]]))

    def test_fresh_hadamard_flags_realize_attenuation_with_r_equals_two_k(self):
        _, encoding, _, _ = _graph_fixture()
        for k in (1, 2):
            private_flags = 2 * k
            word = [('H', flag) for flag in range(private_flags)]
            accepted_scalar = _native_matrix(private_flags, word)[0, 0]
            coefficient = CQ2(Fraction(1, 1 << k))
            self.assertEqual(accepted_scalar, coefficient)
            self.assertEqual(sum(gate[0] in ('T', 'TDG') for gate in word), 0)
            accepted = _scale(_identity(16), accepted_scalar)
            np.testing.assert_array_equal(accepted @ encoding, _scale(encoding, coefficient))
            # Zero acceptance has exactly lambda error, not strict relative error.
            zero_error = _scale(encoding, -coefficient)
            np.testing.assert_array_equal(_dagger(zero_error) @ zero_error,
                                          _scale(_identity(8), coefficient * coefficient))
        # Two coherent H calls on one flag give identity, not two fresh
        # projection events. No measurement/reset is hidden in this block.
        reused_flag = _native_matrix(1, [('H', 0), ('H', 0)])[0, 0]
        self.assertEqual(reused_flag, CO)
        self.assertNotEqual(reused_flag, CQ2(Fraction(1, 2)))


if __name__ == '__main__':
    unittest.main()
