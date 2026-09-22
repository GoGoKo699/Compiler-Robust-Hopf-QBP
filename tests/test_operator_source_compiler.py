"""Small complete-space audits of the dirty operator-source compiler.

The source plane rotations are explicit Clifford+T words. The miniature
two-address-bit lookup uses phase-free X/CX/CCX dirty-selector echoes; its
general asymptotic implementation is proved separately. A two-layer fixture
expands every Toffoli and propagates all columns with just two clean flags.
Matrix checks use complex128, including all dirty input columns, with
tolerance 3e-11.
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


def _optimized_source_word(width):
    """Use the Clifford M_2 before the remaining source-plane conjugations."""
    assert width >= 2
    clifford_base = [('H', 1), ('CX', 1, 0), ('H', 0), ('CX', 1, 0), ('H', 1)]
    tail = _source_word(width)[len(_source_word(2)):]
    return _adjoint(tail) + clifford_base + tail


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


def _two_flag_diagonal(bits, theta):
    """Actual two-flag scalar phase block: replace target SELECT by S_b."""
    source = _operator_source(bits + 1)[0]
    scale = 1 << bits
    ks = [int(np.clip(np.rint((1 - value) * scale / 2), 0, scale))
          for value in (np.cos(theta), np.sin(theta))]
    scalar_circuits = [_scalar_block(source, _sign_word(k, bits))[0] for k in ks]
    zero = np.zeros_like(scalar_circuits[0])
    selected = np.block([[scalar_circuits[0], zero], [zero, scalar_circuits[1]]])
    identity = np.eye(scalar_circuits[0].shape[0], dtype=complex)
    hb = np.kron(H, identity)
    phase_b = np.kron(np.diag([1, 1j]), identity)
    unitary = hb @ phase_b @ selected @ hb
    core_size = source.shape[0]
    embedding = np.eye(4 * core_size, dtype=complex)[:, :core_size]
    coefficient = (1 - 2 * ks[0] / scale) + 1j * (1 - 2 * ks[1] / scale)
    return unitary, embedding, coefficient


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


def _basis_action(basis, word):
    for gate in word:
        if all((basis >> control) & 1 for control in gate[1:-1]):
            basis ^= 1 << gate[-1]
    return basis


def _controlled_swap(control, left, right):
    # Literal Fredkin, as phase-free X/CX/CCX gates.
    return [('CX', left, right), ('CCX', control, right, left), ('CX', left, right)]


def _selectswap_fixture(rows, word_bits, banks):
    """Small complete dirty SelectSwap words, including the actual inverse."""
    address_bits = rows.bit_length() - 1
    low_bits = banks.bit_length() - 1
    address = list(range(address_bits))
    output = list(range(address_bits, address_bits + word_bits))
    bank_start = address_bits + word_bits
    bank_words = [list(range(bank_start + j * word_bits, bank_start + (j + 1) * word_bits))
                  for j in range(banks)]
    bank_targets = [qubit for word in bank_words for qubit in word]
    high = address[low_bits:]
    selector = bank_start + banks * word_bits
    width = selector + (1 if len(high) == 2 else 0)
    mask = (1 << word_bits) - 1
    table = [((3 * row) ^ (row >> 1) ^ 1) & mask for row in range(rows)]
    chunks = [sum(table[chunk * banks + j] << (j * word_bits) for j in range(banks))
              for chunk in range(rows // banks)]
    if len(high) == 2:
        loader = _dirty_mask_lookup(high, bank_targets, selector, chunks)
    elif len(high) == 1:
        loader = []
        for chunk, data in enumerate(chunks):
            if chunk == 0:
                loader.append(('X', high[0]))
            loader += [('CX', high[0], target) for j, target in enumerate(bank_targets) if (data >> j) & 1]
            if chunk == 0:
                loader.append(('X', high[0]))
    else:
        loader = [('X', target) for j, target in enumerate(bank_targets) if (chunks[0] >> j) & 1]
    router = []
    for level in range(low_bits):
        stride = 1 << level
        for bank in range(0, banks, 2 * stride):
            for left, right in zip(bank_words[bank], bank_words[bank + stride]):
                router += _controlled_swap(address[level], left, right)
    copy = [('CX', bank_words[0][j], output[j]) for j in range(word_bits)]
    before_second_copy = loader + router + copy + _adjoint(router) + _adjoint(loader) + router
    query = before_second_copy + copy + _adjoint(router)
    missing_copy = before_second_copy + _adjoint(router)
    return width, address_bits, table, query, missing_copy, bank_start


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


def _two_layer_frame_fixture():
    """Full 256-dimensional actual frame; source precision is deliberately tiny."""
    core = [0, 1, 2]
    system0, system1, a, b, h = 3, 4, 5, 6, 7
    width = 8
    actual_blocks = {}
    for theta in (0, 0.37, 0.11, 0.89):
        unitary, local_embedding, _, _ = _two_flag_block(2, theta)
        actual_blocks[theta] = _amplify(unitary, local_embedding)[0]
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
    logical0 = np.eye(4, dtype=complex)
    logical0[np.ix_([0, 1], [0, 1])] = _rotation(0.37)
    logical1 = np.zeros((4, 4), dtype=complex)
    logical1[np.ix_([0, 2], [0, 2])] = _rotation(0.11)
    logical1[np.ix_([1, 3], [1, 3])] = _rotation(0.89)
    embedding = np.eye(1 << width, dtype=complex)[:, :32]
    return layer0, layer1, logical0, logical1, embedding


def _expand_toffolis(word):
    """Literal seven-T Toffoli decomposition, including its global phase."""
    expanded = []
    for gate in word:
        if gate[0] != 'CCX':
            expanded.append(gate)
            continue
        _, left, right, target = gate
        expanded += [('H', target), ('CX', right, target), ('TDG', target),
                     ('CX', left, target), ('T', target), ('CX', right, target),
                     ('TDG', target), ('CX', left, target), ('T', right),
                     ('T', target), ('H', target), ('CX', left, right),
                     ('T', left), ('TDG', right), ('CX', left, right)]
    return expanded


def _apply_native_word(width, word, columns):
    """Propagate complete initialized columns without a square circuit matrix."""
    result = columns.copy()
    indices = np.arange(1 << width)
    low = {q: indices[(indices & (1 << q)) == 0] for q in range(width)}
    high = {q: low[q] | (1 << q) for q in range(width)}
    phases = {'S': 1j, 'SDG': -1j, 'T': np.exp(1j * np.pi / 4),
              'TDG': np.exp(-1j * np.pi / 4)}
    for name, *qubits in word:
        if name == 'X':
            result = result[indices ^ (1 << qubits[0])]
        elif name == 'CX':
            control, target = qubits
            result = result[indices ^ (((indices >> control) & 1) << target)]
        elif name == 'H':
            q = qubits[0]
            row0, row1 = result[low[q]].copy(), result[high[q]].copy()
            result[low[q]] = (row0 + row1) / np.sqrt(2)
            result[high[q]] = (row0 - row1) / np.sqrt(2)
        else:
            result[high[qubits[0]]] *= phases[name]
    return result


def _native_two_layer_frame_fixture():
    """Tiny native two-clean frame; this is not the asymptotic compiler emitter.

    Three source bits encode two fractional bits. A single dirty selector
    suffices for these miniature tables by an explicit row-by-row echo.
    The precision is intentionally below the theorem's prescribed schedule.
    """
    core = [0, 1, 2]
    selector, z, system0, system1, a, b = 3, 4, 5, 6, 7, 8
    width = 9
    source = _source_word(len(core))
    inverse_source = _adjoint(source)
    mword = _optimized_source_word(len(core))
    control1 = inverse_source + [('CX', a, core[0])] + source
    control0 = inverse_source + [('X', a), ('CX', a, core[0]), ('X', a)] + source
    # R = I - 2 |00><00| tests exactly the two initialized flags.
    reflection = [('X', a), ('X', b), ('H', b), ('CX', a, b),
                  ('H', b), ('X', b), ('X', a)]
    minus_identity = [('X', a), ('S', a), ('S', a),
                      ('X', a), ('S', a), ('S', a)]

    def layer(target, prefix, suffix, angles):
        assert len(prefix) <= 1 and len(suffix) <= 1
        address = [b, *prefix]
        query = []
        for x, theta in enumerate(angles):
            for beta, value in enumerate((np.cos(theta), np.sin(theta))):
                k = int(np.clip(np.rint((1 - value) * 2), 0, 4))
                active_mask = sum(bit << j for j, bit in enumerate(_sign_word(k, 2)))
                delta = active_mask ^ beta  # Inactive encoding f0(b) = b e0.
                row = beta + 2 * x
                negate = [('X', q) for j, q in enumerate(address) if not (row >> j) & 1]
                mark = [('CX', address[0], selector)] if not prefix else [('CCX', *address, selector)]
                insert = [('CCX', selector, z, q) for j, q in enumerate(core) if (delta >> j) & 1]
                query += negate + mark + insert + mark + insert + _adjoint(negate)
        # h = [suffix=0] for layer zero and h = 1 for the empty suffix.
        predicate = [('X', z)] + [('CX', q, z) for q in suffix]
        echo = predicate + query + predicate + query
        hadamards = [('H', q) for q in core]
        baseline = [('H', core[0]), ('CX', b, core[0]), ('H', core[0])]
        phase = hadamards + echo + hadamards + baseline
        scalar = ([('H', a)] + control1 + _adjoint(phase) + mword
                  + phase + control0 + [('H', a)])
        select = [('SDG', target), ('CX', b, target), ('S', target), ('SDG', b)]
        block = _expand_toffolis([('H', b)] + scalar + select + [('H', b)])
        amplified = block + reflection + _adjoint(block) + reflection + block + minus_identity
        return amplified

    angles = (0.37, 0.21, 0.91)
    words = (layer(system0, [], [system1], angles[:1]),
             layer(system1, [system0], [], angles[1:]))
    logical0 = np.eye(4, dtype=complex)
    logical0[np.ix_([0, 1], [0, 1])] = _rotation(angles[0])
    logical1 = np.zeros((4, 4), dtype=complex)
    logical1[np.ix_([0, 2], [0, 2])] = _rotation(angles[1])
    logical1[np.ix_([1, 3], [1, 3])] = _rotation(angles[2])
    # Only a and b are initialized; every logical and dirty basis column occurs.
    embedding = np.eye(1 << width, dtype=complex)[:, :1 << a]
    return width, words, (logical0, logical1), angles, embedding


class OperatorSourceCompilerTests(unittest.TestCase):
    def test_optimized_native_source_counts_and_transfer_witnesses(self):
        for width in range(2, 6):
            word = _optimized_source_word(width)
            source = _word_matrix(width, word)
            _, gammas, amplitudes = _operator_source(width)
            expected = sum(amplitude * gamma for amplitude, gamma in zip(amplitudes, gammas))
            np.testing.assert_allclose(source, expected, atol=ATOL, rtol=0)
            self.assertEqual(sum(gate[0] in ('T', 'TDG') for gate in word), 2 * width - 4)
            witness = _pauli(width, {width - 1: Z})
            transfer = np.trace(witness @ source @ witness @ source.conj().T) / (1 << width)
            self.assertAlmostEqual(transfer.real, 1 - 2 ** (2 - width), delta=ATOL)
            self.assertAlmostEqual(transfer.imag, 0, delta=ATOL)

            forward = _source_word(width)
            controlled_word = _adjoint(forward) + [('CX', width, 0)] + forward
            controlled = _word_matrix(width + 1, controlled_word)
            zero = np.zeros_like(source)
            np.testing.assert_allclose(controlled, np.block([[np.eye(1 << width), zero],
                                                             [zero, expected]]), atol=ATOL, rtol=0)
            self.assertEqual(sum(gate[0] in ('T', 'TDG') for gate in controlled_word), 2 * width - 2)
            controlled_witness = np.kron(I2, witness)
            transfer = np.trace(controlled_witness @ controlled @ controlled_witness
                                @ controlled.conj().T) / (1 << (width + 1))
            self.assertAlmostEqual(transfer.real, 1 - 2 ** (1 - width), delta=ATOL)
            self.assertAlmostEqual(transfer.imag, 0, delta=ATOL)

    def test_exact_native_toffoli_phase_and_inverse(self):
        native = _expand_toffolis([('CCX', 0, 1, 2)])
        expected = _word_matrix(3, [('CCX', 0, 1, 2)])
        np.testing.assert_allclose(_word_matrix(3, native), expected, atol=ATOL, rtol=0)
        np.testing.assert_allclose(_word_matrix(3, native + _adjoint(native)),
                                   np.eye(8), atol=ATOL, rtol=0)
        self.assertEqual(sum(gate[0] in ('T', 'TDG') for gate in native), 7)

    def test_native_two_clean_full_frame_composition_without_reset(self):
        width, words, logical, angles, embedding = _native_two_layer_frame_fixture()
        self.assertEqual(embedding.shape, (512, 128))  # Exactly two clean flags.
        self.assertTrue(all(gate[0] in ('X', 'H', 'S', 'SDG', 'T', 'TDG', 'CX')
                            for word in words for gate in word))
        identity_dirty = np.eye(32)
        ideal = [np.kron(layer, identity_dirty) for layer in logical]
        outputs = [_apply_native_word(width, word, embedding) for word in words]
        errors = [np.linalg.norm(output - embedding @ target, ord=2)
                  for output, target in zip(outputs, ideal)]
        # Check each full output against the independent rotation and the
        # normalization-two OAA bound, including all rejected flag amplitudes.
        for error, layer_angles in zip(errors, (angles[:1], angles[1:])):
            zeta = max(np.linalg.norm(np.round(2 * np.array([np.cos(theta), np.sin(theta)])) / 2
                                      - np.array([np.cos(theta), np.sin(theta)]))
                       for theta in layer_angles)
            self.assertLess(zeta, 0.25)
            self.assertLessEqual(error, 4 * zeta + ATOL)
        output = _apply_native_word(width, words[1], outputs[0])
        expected = embedding @ np.kron(logical[1] @ logical[0], identity_dirty)
        full_error = np.linalg.norm(output - expected, ord=2)
        self.assertGreater(full_error, 1e-3)
        self.assertLessEqual(full_error, sum(errors) + ATOL)
        np.testing.assert_allclose(output.conj().T @ output, np.eye(128), atol=ATOL, rtol=0)

        # The next actual unitary consumes the entire previous output, including
        # nonzero leakage; replacing that output by a clean projection changes it.
        projected = outputs[0].copy()
        projected[128:] = 0
        self.assertGreater(np.linalg.norm(outputs[0] - projected, ord=2), 1e-3)
        reset_output = _apply_native_word(width, words[1], projected)
        self.assertGreater(np.linalg.norm(output - reset_output, ord=2), 1e-3)
        inactive = [column for column in range(128) if (column >> 6) & 1]
        np.testing.assert_allclose(outputs[0][:, inactive], embedding[:, inactive], atol=ATOL, rtol=0)

        # The selector and suffix control return exactly for all their arbitrary
        # input columns. Approximate return of the dirty source core is included
        # in full_error. The full-column norm also covers an arbitrary reference.
        rows, columns = np.indices(output.shape)
        changed_helpers = ((rows ^ columns) & ((1 << 3) | (1 << 4))) != 0
        np.testing.assert_allclose(output[changed_helpers], 0, atol=ATOL, rtol=0)

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
        layer0, layer1, logical0, logical1, embedding = _two_layer_frame_fixture()
        identity_core = np.eye(8)
        ideal0 = np.kron(logical0, identity_core)
        ideal1 = np.kron(logical1, identity_core)
        ideal_frame = np.kron(logical1 @ logical0, identity_core)
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
        inactive = [column for column in range(32) if (column >> 4) & 1]
        np.testing.assert_allclose(first_output[:, inactive], embedding[:, inactive], atol=ATOL, rtol=0)

    def test_full_word_selectswap_every_dirty_basis_input_and_inverse(self):
        for rows in (4, 8):
            for word_bits in (1, 2):
                for banks in (2, 4):
                    width, address_bits, table, query, _, _ = _selectswap_fixture(rows, word_bits, banks)
                    inverse = _adjoint(query)
                    with self.subTest(rows=rows, word_bits=word_bits, banks=banks):
                        for basis in range(1 << width):
                            address = basis & (rows - 1)
                            expected = basis ^ (table[address] << address_bits)
                            actual = _basis_action(basis, query)
                            self.assertEqual(actual, expected)
                            self.assertEqual(_basis_action(actual, inverse), basis)
        _, address_bits, table, _, missing_copy, bank_start = _selectswap_fixture(4, 1, 2)
        basis = 1 << bank_start  # Nonzero arbitrary initial selected bank.
        self.assertNotEqual(_basis_action(basis, missing_copy), basis ^ (table[0] << address_bits))

    def test_dirty_suffix_echo_native_all_inputs_and_missing_query(self):
        # All nine bits are arbitrary: core0,1; z2; b3; x4; suffix5,6,7;
        # borrowed t8. Only a basis permutation is materialized at this width.
        core, z, b, x, suffix, helper = [0, 1], 2, 3, 4, [5, 6, 7], 8
        masks = [3, 1, 0, 2]  # Nontrivial g(b,x), row b+2*x.
        negatives = [('X', qubit) for qubit in suffix]
        # Exact C3X using four Toffolis and arbitrary, restored helper t.
        toggle = [('CCX', suffix[0], suffix[1], helper),
                  ('CCX', helper, suffix[2], z)] * 2
        predicate = negatives + toggle + _adjoint(negatives)
        query = []
        for row, mask in enumerate(masks):
            negate_row = [('X', qubit) for j, qubit in enumerate((b, x)) if not ((row >> j) & 1)]
            mark = [('CCX', b, x, helper)]
            insert = [('CCX', helper, z, qubit) for j, qubit in enumerate(core) if (mask >> j) & 1]
            query += negate_row + mark + insert + mark + insert + _adjoint(negate_row)
        echo = predicate + query + predicate + query
        inverse = _adjoint(echo)
        for basis in range(512):
            active = all(not ((basis >> qubit) & 1) for qubit in suffix)
            row = ((basis >> b) & 1) + 2 * ((basis >> x) & 1)
            expected = basis ^ (masks[row] if active else 0)
            actual = _basis_action(basis, echo)
            self.assertEqual(actual, expected)
            self.assertEqual(_basis_action(actual, inverse), basis)
        # A complete phase-free basis equality proves the same operation on
        # superpositions and reference-entangled inputs, including dirty t,z.
        basis = (1 << z) | (1 << suffix[0]) | (1 << helper)
        self.assertNotEqual(_basis_action(basis, predicate + query + predicate), basis)

    def test_two_flag_dirty_suffix_source_matches_initialized_branch(self):
        # A 256-dimensional complete source/OAA fixture. The three-address-bit
        # query is a permutation macro; the preceding test audits its native echo.
        # core0,1 and z2 are dirty; target3, suffix4, x5 are logical; a6,b7 clean.
        width, z, target, suffix, x, a, b = 8, 2, 3, 4, 5, 6, 7
        angles = (np.pi, np.pi / 2)
        # Full active mask f(b,x), with row b+2*x.
        active_masks = [3, 1, 1, 0]
        images = []
        for basis in range(256):
            beta = (basis >> b) & 1
            row = beta + 2 * ((basis >> x) & 1)
            delta = active_masks[row] ^ beta  # Inactive f0 = b*e0.
            images.append(basis ^ (delta if (basis >> z) & 1 else 0))
        query = np.eye(256, dtype=complex)[np.argsort(images)]
        predicate = _word_matrix(width, [('X', z), ('CX', suffix, z)])
        echo = query @ predicate @ query @ predicate
        hadamards = _word_matrix(width, [('H', 0), ('H', 1)])
        baseline = _word_matrix(width, [('H', 0), ('CX', b, 0), ('H', 0)])
        phase = baseline @ hadamards @ echo @ hadamards
        expected_phase = []
        for basis in range(256):
            beta = (basis >> b) & 1
            row = beta + 2 * ((basis >> x) & 1)
            mask = beta if (basis >> suffix) & 1 else active_masks[row]
            expected_phase.append((-1) ** ((basis & 3) & mask).bit_count())
        np.testing.assert_allclose(phase, np.diag(expected_phase), atol=ATOL, rtol=0)

        source = _source_word(2)
        inverse_source = _adjoint(source)
        m = _word_matrix(width, inverse_source + [('X', 0)] + source)
        control1 = _word_matrix(width, inverse_source + [('CX', a, 0)] + source)
        control0 = _word_matrix(width, inverse_source + [('X', a), ('CX', a, 0), ('X', a)] + source)
        ha = _word_matrix(width, [('H', a)])
        scalar = ha @ control0 @ phase @ m @ phase.conj().T @ control1 @ ha
        select = _word_matrix(width, [('SDG', target), ('CX', b, target), ('S', target), ('SDG', b)])
        hb = _word_matrix(width, [('H', b)])
        actual = hb @ select @ scalar @ hb
        blocks = {theta: _two_flag_block(1, theta)[0] for theta in (0, *angles)}
        independent = _embed_addressed_blocks(
            width, [0, 1, target, a, b],
            lambda values: blocks[0 if values[suffix] else angles[values[x]]])
        np.testing.assert_allclose(actual, independent, atol=ATOL, rtol=0)

        embedding = np.eye(256, dtype=complex)[:, :64]
        amplified = _amplify(actual, embedding)[0]
        logical_target = _embed_addressed_blocks(
            6, [target], lambda values: _rotation(0 if values[suffix] else angles[values[x]]))
        output = amplified @ embedding
        np.testing.assert_allclose(output, embedding @ logical_target, atol=ATOL, rtol=0)
        coefficients = np.arange(1, 65) + 1j * np.arange(64, 0, -1)
        coefficients /= np.linalg.norm(coefficients)
        # Literal phase, coherent z=0/1, and full Schmidt reference support on
        # every dirty/logical input, without projecting the accepted output.
        np.testing.assert_allclose(output * coefficients, (embedding @ logical_target) * coefficients,
                                   atol=ATOL, rtol=0)

    def test_addressed_literal_diagonal_two_flags_and_reference(self):
        # Direct two-flag block; no initialized Y eigenwire is used.
        # Addressed matrices use the separately audited exact lookup interface.
        core = [0, 1, 2]
        a, b, address = 3, 4, 5
        columns = [dirty | (x << address) for x in range(2) for dirty in range(8)]
        embedding = np.eye(64, dtype=complex)[:, columns]
        for angles in ((np.pi / 2, np.pi / 2), (np.pi, -np.pi / 2), (0.37, 0.89)):
            blocks = {}
            for theta in angles:
                unitary, local_embedding, coefficient = _two_flag_diagonal(2, theta)
                accepted = local_embedding.conj().T @ unitary @ local_embedding
                np.testing.assert_allclose(accepted, coefficient * np.eye(8) / 2, atol=ATOL, rtol=0)
                blocks[theta] = _amplify(unitary, local_embedding)[0]
            actual = _embed_addressed_blocks(6, [*core, a, b],
                                            lambda values: blocks[angles[values[address]]])
            target = np.kron(np.diag(np.exp(1j * np.array(angles))), np.eye(8))
            output = actual @ embedding
            full_error = np.linalg.norm(output - embedding @ target, ord=2)
            if angles[0] != 0.37:
                np.testing.assert_allclose(output, embedding @ target, atol=ATOL, rtol=0)
            else:
                self.assertGreater(full_error, 1e-3)
                self.assertGreater(np.linalg.norm(output - embedding @ (embedding.conj().T @ output), ord=2), 1e-3)
            coefficients = np.arange(1, 17) + 1j * np.arange(16, 0, -1)
            coefficients = coefficients / np.linalg.norm(coefficients)
            # Full Schmidt support across address/core and an untouched reference.
            actual_reference = actual @ (embedding * coefficients)
            ideal_reference = (embedding @ target) * coefficients
            self.assertLessEqual(np.linalg.norm(actual_reference - ideal_reference), full_error + ATOL)
            if angles[0] == angles[1] == np.pi / 2:
                np.testing.assert_allclose(output, 1j * embedding, atol=ATOL, rtol=0)
                self.assertGreater(np.linalg.norm(output - embedding, ord=2), 1.4)

    def test_phase_dressed_frame_reuses_actual_flags_and_core(self):
        layer0, layer1, logical0, logical1, embedding = _two_layer_frame_fixture()
        angles = (0.17, -0.29, 0.43, 0.71)
        blocks = {}
        for theta in angles:
            unitary, local_embedding, _ = _two_flag_diagonal(2, theta)
            blocks[theta] = _amplify(unitary, local_embedding)[0]
        # Same core0..2 and flags a=5,b=6; suffix h=7 is untouched.
        diagonal = _embed_addressed_blocks(
            8, [0, 1, 2, 5, 6],
            lambda values: blocks[angles[values[3] + 2 * values[4]]])
        logical_diagonal = np.diag(np.exp(1j * np.array(angles)))
        ideal_diagonal = np.kron(logical_diagonal, np.eye(8))
        ideal_frame = np.kron(logical1 @ logical0, np.eye(8))
        frame_output = layer1 @ layer0 @ embedding
        actual = diagonal @ frame_output
        expected = embedding @ np.kron(logical_diagonal @ logical1 @ logical0, np.eye(8))
        frame_error = np.linalg.norm(frame_output - embedding @ ideal_frame, ord=2)
        diagonal_error = np.linalg.norm(diagonal @ embedding - embedding @ ideal_diagonal, ord=2)
        full_error = np.linalg.norm(actual - expected, ord=2)
        self.assertLessEqual(full_error, frame_error + diagonal_error + ATOL)
        retained_clean_column = embedding @ embedding.conj().T @ frame_output
        self.assertGreater(np.linalg.norm(frame_output - retained_clean_column, ord=2), 1e-3)
        self.assertGreater(np.linalg.norm(actual - diagonal @ retained_clean_column, ord=2), 1e-3)
        np.testing.assert_allclose(actual[128:], 0, atol=ATOL, rtol=0)

    def test_general_u2_multiplexor_euler_phase_and_four_stage_composition(self):
        # Matrix-block fixture, not a native scalable multiplexor emitter.
        # Core0..2 is dirty; target3 and address4 are arbitrary; only a5,b6
        # are initialized. Every stage reuses the same flags and source core.
        core, target, address, a, b = [0, 1, 2], 3, 4, 5, 6
        embedding = np.eye(128, dtype=complex)[:, :32]
        k = H @ np.diag([1, -1j])  # K=HS†, so K Y K†=Z.
        np.testing.assert_allclose(k @ Y @ k.conj().T, Z, atol=ATOL, rtol=0)
        local_k = np.kron(np.eye(4), np.kron(k, np.eye(8)))

        def rz(theta):
            return np.diag([np.exp(-1j * theta), np.exp(1j * theta)])

        def addressed(blocks):
            zero = np.zeros((2, 2), dtype=complex)
            return np.kron(np.block([[blocks[0], zero], [zero, blocks[1]]]), np.eye(8))

        cases = (
            ((np.pi / 2, np.pi), (np.pi / 2, -np.pi / 2),
             (0, np.pi / 2), (np.pi, np.pi / 2)),
            ((0.37, -1.03), (0.29, -0.53), (0.41, 1.07), (-0.23, 0.61)),
        )
        for case_index, (alpha, beta, gamma, delta) in enumerate(cases):
            with self.subTest(exact=case_index == 0):
                stages, ideals = [], []
                # Chronological order is delta, gamma, beta, alpha.
                for kind, angles in (('z', delta), ('y', gamma), ('z', beta), ('phase', alpha)):
                    blocks = []
                    for theta in angles:
                        if kind == 'phase':
                            unitary, initialized, _ = _two_flag_diagonal(2, theta)
                        else:
                            unitary, initialized, _, _ = _two_flag_block(2, theta)
                        actual = _amplify(unitary, initialized)[0]
                        if kind == 'z':
                            actual = local_k @ actual @ local_k.conj().T
                        blocks.append(actual)
                    active = [*core, a, b] if kind == 'phase' else [*core, target, a, b]
                    stages.append(_embed_addressed_blocks(7, active,
                                                           lambda values: blocks[values[address]]))
                    factor = ((lambda theta: np.exp(1j * theta) * I2) if kind == 'phase'
                              else rz if kind == 'z' else _rotation)
                    ideals.append(addressed([factor(theta) for theta in angles]))

                # Construct the independent literal U(2) blocks directly from
                # their Euler expression, including relative address phases.
                ideal = addressed([np.exp(1j * alpha[x]) * rz(beta[x])
                                   @ _rotation(gamma[x]) @ rz(delta[x]) for x in range(2)])
                expected = embedding @ ideal
                errors = [np.linalg.norm(stage @ embedding - embedding @ factor, ord=2)
                          for stage, factor in zip(stages, ideals)]
                first_output = stages[0] @ embedding
                output = first_output
                for stage in stages[1:]:
                    output = stage @ output
                full_error = np.linalg.norm(output - expected, ord=2)
                self.assertLessEqual(full_error, sum(errors) + ATOL)
                np.testing.assert_allclose(output.conj().T @ output, np.eye(32), atol=ATOL, rtol=0)
                if case_index == 0:
                    np.testing.assert_allclose(output, expected, atol=ATOL, rtol=0)
                    discarded_phases = addressed([rz(beta[x]) @ _rotation(gamma[x])
                                                  @ rz(delta[x]) for x in range(2)])
                    self.assertGreater(np.linalg.norm(output - embedding @ discarded_phases, ord=2), 1.9)
                else:
                    self.assertGreater(full_error, 1e-3)
                    projected = first_output.copy()
                    projected[32:] = 0
                    self.assertGreater(np.linalg.norm(first_output - projected, ord=2), 1e-3)
                    for stage in stages[1:]:
                        projected = stage @ projected
                    self.assertGreater(np.linalg.norm(output - projected, ord=2), 1e-3)

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
