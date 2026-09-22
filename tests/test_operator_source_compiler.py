"""Small complete-space audits of the dirty operator-source compiler.

The source plane rotations are explicit Clifford+T words. The miniature
two-address-bit lookup uses phase-free X/CX/CCX dirty-selector echoes; its
general asymptotic implementation is proved separately. Matrix checks use
complex128, including all dirty input columns, with tolerance 3e-11.
"""
from __future__ import annotations

import unittest

import numpy as np


ATOL = 3e-11
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


def _pauli(width, factors):
    result = np.ones((1, 1), dtype=complex)
    for qubit in reversed(range(width)):
        result = np.kron(result, factors.get(qubit, I2))
    return result


def _adjoint(word):
    inverse = {'T': 'TDG', 'TDG': 'T', 'S': 'SDG', 'SDG': 'S'}
    return [(inverse.get(gate[0], gate[0]), *gate[1:]) for gate in reversed(word)]


def _word_matrix(width, word):
    """Chronological gate words; qubit zero is the low integer bit."""
    size = 1 << width
    result = np.eye(size, dtype=complex)
    for gate in word:
        name = gate[0]
        if name in ('X', 'CX', 'CCX'):
            images = [basis ^ (1 << gate[-1])
                      if all((basis >> control) & 1 for control in gate[1:-1]) else basis
                      for basis in range(size)]
            result = result[np.argsort(images)]
        elif name == 'H':
            bit = 1 << gate[1]
            for low in range(size):
                if low & bit:
                    continue
                high = low | bit
                row0, row1 = result[low].copy(), result[high].copy()
                result[low] = (row0 + row1) / np.sqrt(2)
                result[high] = (row0 - row1) / np.sqrt(2)
        else:
            phase = {'Z': -1, 'S': 1j, 'SDG': -1j,
                     'T': np.exp(1j * np.pi / 4),
                     'TDG': np.exp(-1j * np.pi / 4)}[name]
            result[[basis for basis in range(size) if (basis >> gate[1]) & 1]] *= phase
    return result


def _source_word(width):
    # R_j = exp(+i pi Y_j X_(j+1)/8), up to an irrelevant scalar.
    # K=(SH)_j H_(j+1) maps Z_j Z_(j+1) to Y_j X_(j+1).
    return [gate for j in range(width - 1) for gate in
            [('SDG', j), ('H', j), ('H', j + 1), ('CX', j, j + 1),
             ('TDG', j + 1), ('CX', j, j + 1),
             ('H', j), ('S', j), ('H', j + 1)]]


def _operator_source(width):
    gammas = [_pauli(width, {**{k: Z for k in range(j)}, j: X}) for j in range(width)]
    amplitudes = [2 ** (-(j + 1) / 2) for j in range(width - 1)]
    amplitudes.append(2 ** (-(width - 1) / 2))
    unitary = _word_matrix(width, _source_word(width))
    source = unitary @ gammas[0] @ unitary.conj().T
    return source, gammas, np.array(amplitudes)


def _sign_word(k, bits):
    """Dyadic c=1-2k/2**bits, including both literal endpoints."""
    if k == 1 << bits:
        return [1] * (bits + 1)
    return [(k >> (bits - 1 - j)) & 1 for j in range(bits)] + [0]


def _scalar_block(source, signs):
    width = len(signs)
    size = 1 << width
    mask = _pauli(width, {j: Z for j, bit in enumerate(signs) if bit})
    masked_source = mask @ source @ mask.conj().T
    identity = np.eye(size, dtype=complex)
    zero = np.zeros_like(identity)
    control0 = np.block([[source, zero], [zero, identity]])
    control1 = np.block([[identity, zero], [zero, source]])
    hadamard = np.kron(H, identity)
    circuit = hadamard @ control0 @ np.kron(I2, masked_source) @ control1 @ hadamard
    return circuit, masked_source


def _rotation(theta):
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]], dtype=complex)


def _two_flag_block(bits, theta):
    """Full two-flag block, with flags b,a above target and dirty core."""
    width = bits + 1
    source = _operator_source(width)[0]
    scale = 1 << bits
    ks = [int(np.clip(np.rint((1 - value) * scale / 2), 0, scale))
          for value in (np.cos(theta), np.sin(theta))]
    coefficients = [1 - 2 * k / scale for k in ks]
    scalar_circuits = [_scalar_block(source, _sign_word(k, bits))[0] for k in ks]
    core_size = 1 << width
    # Insert target below flag a, above core, preserving the source's a blocks.
    lifted = [np.block([[np.kron(I2, circuit[row * core_size:(row + 1) * core_size,
                                          col * core_size:(col + 1) * core_size])
                         for col in range(2)] for row in range(2)])
              for circuit in scalar_circuits]
    zero = np.zeros_like(lifted[0])
    coefficient_select = np.block([[lifted[0], zero], [zero, lifted[1]]])
    identity = np.eye(4 * core_size, dtype=complex)
    phase_y = np.kron(I2, np.kron(-1j * Y, np.eye(core_size)))
    select = np.block([[identity, zero], [zero, phase_y]])
    hb = np.kron(H, identity)
    unitary = hb @ select @ coefficient_select @ hb
    input_size = 2 * core_size
    embedding = np.eye(4 * input_size, dtype=complex)[:, :input_size]
    target = np.kron(_rotation(theta), np.eye(core_size))
    return unitary, embedding, target, coefficients


def _amplify(unitary, embedding):
    reflection = np.eye(unitary.shape[0], dtype=complex) - 2 * embedding @ embedding.conj().T
    return -unitary @ reflection @ unitary.conj().T @ reflection @ unitary, reflection


def _dirty_mask_lookup(address, core, selector, masks):
    """Exact two-address-bit selector echo on every selector input."""
    assert len(address) == 2
    word = []
    for row, mask in enumerate(masks):
        if not mask:
            continue
        negations = [('X', address[j]) for j in range(2) if not ((row >> j) & 1)]
        predicate = [('CCX', *address, selector)]
        insert = [('CX', selector, qubit) for j, qubit in enumerate(core) if (mask >> j) & 1]
        word += negations + predicate + insert + predicate + insert + negations[::-1]
    return word


def _native_endpoint_fixture():
    # Low to high: 2 dirty core bits, dirty selector, target, address, a, b.
    core = [0, 1]
    selector, target, address, a, b = 2, 3, 4, 5, 6
    width = 7
    # theta(address=0)=pi; theta(address=1)=pi/2. Row index is address+2*b.
    ks = [2, 1, 1, 0]
    masks = [sum(bit << j for j, bit in enumerate(_sign_word(k, 1))) for k in ks]
    lookup = _dirty_mask_lookup([address, b], core, selector, masks)
    hadamards = [('H', qubit) for qubit in core]
    phase_word = hadamards + lookup + hadamards
    source = _source_word(len(core))
    source_inverse = _adjoint(source)
    mword = source_inverse + [('X', 0)] + source
    control1 = source_inverse + [('CX', a, 0)] + source
    control0 = source_inverse + [('X', a), ('CX', a, 0), ('X', a)] + source
    scalar = ([('H', a)] + control1 + _adjoint(phase_word) + mword
              + phase_word + control0 + [('H', a)])
    minus_i_y = [('SDG', target), ('CX', b, target), ('S', target), ('SDG', b)]
    word = [('H', b)] + scalar + minus_i_y + [('H', b)]
    unitary = _word_matrix(width, word)
    input_size = 1 << 5
    embedding = np.eye(1 << width, dtype=complex)[:, :input_size]
    target_matrix = np.block([
        [np.kron(_rotation(np.pi), np.eye(8)), np.zeros((16, 16))],
        [np.zeros((16, 16)), np.kron(_rotation(np.pi / 2), np.eye(8))]])
    return unitary, embedding, target_matrix, phase_word, masks


def _embed_addressed_blocks(width, active, choose_block):
    """Embed local actual unitaries; all other bits are preserved controls."""
    spectators = [qubit for qubit in range(width) if qubit not in active]
    result = np.zeros((1 << width, 1 << width), dtype=complex)
    for assignment in range(1 << len(spectators)):
        values = {qubit: (assignment >> j) & 1 for j, qubit in enumerate(spectators)}
        fixed = sum(value << qubit for qubit, value in values.items())
        indices = [fixed | sum(((local >> j) & 1) << qubit for j, qubit in enumerate(active))
                   for local in range(1 << len(active))]
        result[np.ix_(indices, indices)] = choose_block(values)
    return result


class OperatorSourceCompilerTests(unittest.TestCase):
    def test_native_geometric_operator_source(self):
        for width in range(2, 6):
            source, gammas, amplitudes = _operator_source(width)
            identity = np.eye(1 << width)
            expected = sum(amplitude * gamma for amplitude, gamma in zip(amplitudes, gammas))
            np.testing.assert_allclose(source, expected, atol=ATOL, rtol=0)
            np.testing.assert_allclose(source @ source, identity, atol=ATOL, rtol=0)
            for j, gamma in enumerate(gammas):
                for k, other in enumerate(gammas):
                    np.testing.assert_allclose(gamma @ other + other @ gamma,
                                               2 * identity if j == k else 0, atol=ATOL, rtol=0)
            self.assertEqual(sum(gate[0] in ('T', 'TDG') for gate in _source_word(width)), width - 1)

    def test_every_small_sign_mask_and_dyadic_endpoint(self):
        for bits in range(1, 4):
            width = bits + 1
            source, _, amplitudes = _operator_source(width)
            identity = np.eye(1 << width)
            for mask in range(1 << width):
                signs = [(mask >> j) & 1 for j in range(width)]
                circuit, masked = _scalar_block(source, signs)
                coefficient = sum(amplitude ** 2 * (-1) ** bit
                                  for amplitude, bit in zip(amplitudes, signs))
                np.testing.assert_allclose((source @ masked + masked @ source) / 2,
                                           coefficient * identity, atol=ATOL, rtol=0)
                np.testing.assert_allclose(circuit[:len(identity), :len(identity)],
                                           coefficient * identity, atol=ATOL, rtol=0)
            for k in range((1 << bits) + 1):
                circuit = _scalar_block(source, _sign_word(k, bits))[0]
                coefficient = 1 - 2 * k / (1 << bits)
                np.testing.assert_allclose(circuit[:len(identity), :len(identity)],
                                           coefficient * identity, atol=ATOL, rtol=0)

    def test_cosine_sine_block_and_full_oaa_error(self):
        for bits in range(1, 4):
            for theta in (0, np.pi / 2, np.pi, -np.pi / 2, 0.37):
                unitary, embedding, target, (cosine, sine) = _two_flag_block(bits, theta)
                accepted = embedding.conj().T @ unitary @ embedding
                core_size = accepted.shape[0] // 2
                expected_block = np.kron((cosine * I2 - 1j * sine * Y) / 2, np.eye(core_size))
                np.testing.assert_allclose(accepted, expected_block, atol=ATOL, rtol=0)
                amplified, _ = _amplify(unitary, embedding)
                actual_column = amplified @ embedding
                error = np.linalg.norm(actual_column - embedding @ target, ord=2)
                zeta = np.linalg.norm(2 * accepted - target, ord=2)
                if zeta <= 0.25:
                    self.assertLessEqual(error, 4 * zeta + ATOL)
                # Exact formula includes the rejected output, without postselection.
                rho2 = cosine ** 2 + sine ** 2
                error2 = 2 - (3 - rho2) * (cosine * np.cos(theta) + sine * np.sin(theta))
                self.assertAlmostEqual(error ** 2, max(0, error2), delta=ATOL)
                if theta != 0.37:
                    np.testing.assert_allclose(actual_column, embedding @ target, atol=ATOL, rtol=0)

    def test_composed_dirty_selector_and_literal_addressed_rotation(self):
        unitary, embedding, target, phase_word, masks = _native_endpoint_fixture()
        phase = _word_matrix(7, phase_word)
        diagonal = [(-1) ** ((basis & 3) & masks[((basis >> 4) & 1) + 2 * ((basis >> 6) & 1)]).bit_count()
                    for basis in range(128)]
        np.testing.assert_allclose(phase, np.diag(diagonal), atol=ATOL, rtol=0)
        np.testing.assert_allclose(embedding.conj().T @ unitary @ embedding, target / 2, atol=ATOL, rtol=0)
        amplified, _ = _amplify(unitary, embedding)
        np.testing.assert_allclose(amplified @ embedding, embedding @ target, atol=ATOL, rtol=0)

    def test_arbitrary_dirty_reference_return(self):
        unitary, embedding, target, _, _ = _native_endpoint_fixture()
        amplified, _ = _amplify(unitary, embedding)
        dimension = embedding.shape[1]
        # A full-Schmidt-rank reference purifies logical input, core and helper.
        coefficients = np.arange(1, dimension + 1, dtype=float)
        coefficients /= np.linalg.norm(coefficients)
        initial = (embedding * coefficients).reshape(-1)
        expected = ((embedding @ target) * coefficients).reshape(-1)
        actual = (amplified @ initial.reshape(amplified.shape[0], dimension)).reshape(-1)
        np.testing.assert_allclose(actual, expected, atol=ATOL, rtol=0)

    def test_two_layer_frame_reuses_leaked_work_and_erases_suffix_flag(self):
        # Three dirty source bits, two logical bits, flags a,b, suffix flag h.
        # This composition audit embeds actual local blocks, not a native QROM
        # implementation; the preceding endpoint fixture audits that query.
        core = [0, 1, 2]
        system0, system1, a, b, h = 3, 4, 5, 6, 7
        width = 8
        actual_blocks = {}
        for theta in (0, 0.37, 0.11, 0.89):
            unitary, local_embedding, _, _ = _two_flag_block(2, theta)
            actual_blocks[theta] = _amplify(unitary, local_embedding)[0]

        # First suffix is system1=0. The final layer's empty suffix is true.
        compute_suffix = _word_matrix(width, [('X', h), ('CX', system1, h)])
        compute_empty_suffix = _word_matrix(width, [('X', h)])
        selected0 = _embed_addressed_blocks(
            width, [*core, system0, a, b],
            lambda values: actual_blocks[0.37 if values[h] else 0])
        selected1 = _embed_addressed_blocks(
            width, [*core, system1, a, b],
            lambda values: actual_blocks[(0.89 if values[system0] else 0.11) if values[h] else 0])
        layer0 = compute_suffix.conj().T @ selected0 @ compute_suffix
        layer1 = compute_empty_suffix.conj().T @ selected1 @ compute_empty_suffix

        # Independently form the two logical Hopf layers in basis x0+2*x1.
        logical0 = np.eye(4, dtype=complex)
        logical0[np.ix_([0, 1], [0, 1])] = _rotation(0.37)
        logical1 = np.zeros((4, 4), dtype=complex)
        logical1[np.ix_([0, 2], [0, 2])] = _rotation(0.11)
        logical1[np.ix_([1, 3], [1, 3])] = _rotation(0.89)
        identity_core = np.eye(8)
        ideal0 = np.kron(logical0, identity_core)
        ideal1 = np.kron(logical1, identity_core)
        ideal_frame = np.kron(logical1 @ logical0, identity_core)
        embedding = np.eye(1 << width, dtype=complex)[:, :32]
        error0 = np.linalg.norm(layer0 @ embedding - embedding @ ideal0, ord=2)
        error1 = np.linalg.norm(layer1 @ embedding - embedding @ ideal1, ord=2)
        actual_frame = layer1 @ layer0 @ embedding
        frame_error = np.linalg.norm(actual_frame - embedding @ ideal_frame, ord=2)
        self.assertLessEqual(frame_error, error0 + error1 + ATOL)
        self.assertGreater(frame_error, 1e-3)

        # No zero-work projection/reset may be inserted before the second layer.
        first_output = layer0 @ embedding
        retained_clean_column = embedding @ embedding.conj().T @ first_output
        self.assertGreater(np.linalg.norm(first_output - retained_clean_column, ord=2), 1e-3)
        self.assertGreater(np.linalg.norm(actual_frame - layer1 @ retained_clean_column, ord=2), 1e-3)

        # h is erased even for arbitrary a,b and core inputs, a stronger invariant
        # than return only on the completely initialized input columns.
        np.testing.assert_allclose(layer0[128:, :128], 0, atol=ATOL, rtol=0)
        np.testing.assert_allclose(layer1[128:, :128], 0, atol=ATOL, rtol=0)
        np.testing.assert_allclose(actual_frame[128:], 0, atol=ATOL, rtol=0)
        # The first layer is exactly inactive when its suffix is one.
        inactive = [column for column in range(32) if (column >> system1) & 1]
        np.testing.assert_allclose(first_output[:, inactive], embedding[:, inactive], atol=ATOL, rtol=0)

    def test_missing_mask_and_wrong_oaa_inverse_are_detected(self):
        source = _operator_source(3)[0]
        desired = _scalar_block(source, _sign_word(2, 2))[0][:8, :8]
        missing_mask = _scalar_block(source, [0, 0, 0])[0][:8, :8]
        np.testing.assert_allclose(desired, 0, atol=ATOL, rtol=0)
        np.testing.assert_allclose(missing_mask, np.eye(8), atol=ATOL, rtol=0)
        unitary, embedding, target, _, _ = _native_endpoint_fixture()
        amplified, reflection = _amplify(unitary, embedding)
        wrong_inverse = -unitary @ reflection @ unitary @ reflection @ unitary
        self.assertGreater(np.linalg.norm(wrong_inverse @ embedding - embedding @ target, ord=2), 0.1)
        self.assertGreater(np.linalg.norm(-amplified @ embedding - embedding @ target, ord=2), 1.9)
        approximate, initialized, _, _ = _two_flag_block(3, 0.37)
        correct, r = _amplify(approximate, initialized)
        wrong_order = -approximate.conj().T @ r @ approximate @ r @ approximate
        self.assertGreater(np.linalg.norm((wrong_order - correct) @ initialized, ord=2), 0.2)
        np.testing.assert_allclose(_word_matrix(1, [('X', 0), ('Z', 0), ('X', 0), ('Z', 0)]),
                                   -I2, atol=ATOL, rtol=0)


if __name__ == '__main__':
    unittest.main()
