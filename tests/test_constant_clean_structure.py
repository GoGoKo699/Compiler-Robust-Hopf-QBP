"""Finite matrix audits of constant-clean architecture restrictions.

These checks exercise complete program/work spaces, not just successful
normalized columns. They test signs, multiplication order, rank and premises;
they do not prove the corresponding asymptotic theorems. All calculations use
complex128 with absolute tolerance 2e-11 and rank threshold 2e-10.
"""
from __future__ import annotations

import itertools
import unittest

import numpy as np


ATOL = 2e-11
RANK_TOL = 2e-10
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)


def _block_diagonal(blocks: list[np.ndarray]) -> np.ndarray:
    rows = sum(block.shape[0] for block in blocks)
    columns = sum(block.shape[1] for block in blocks)
    result = np.zeros((rows, columns), dtype=complex)
    row = column = 0
    for block in blocks:
        r, c = block.shape
        result[row:row + r, column:column + c] = block
        row += r
        column += c
    return result


def _permutation(images: list[int]) -> np.ndarray:
    result = np.zeros((len(images), len(images)), dtype=complex)
    result[images, np.arange(len(images))] = 1
    return result


def _unitary(dimension: int, rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(dimension, dimension))
    matrix = matrix + 1j * rng.normal(size=(dimension, dimension))
    q, _ = np.linalg.qr(matrix)
    return q


def _ry(theta: float) -> np.ndarray:
    # The project convention is exp(-i theta Y), with no factor of one half.
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]], dtype=complex)


def _echo(interpreters: list[np.ndarray], mask: int) -> np.ndarray:
    """Complete XOR program echo: block z is D[z xor mask] D[z]^dagger."""
    dimension = interpreters[0].shape[0]
    loader = np.kron(_permutation([z ^ mask for z in range(len(interpreters))]),
                     np.eye(dimension))
    interpreter = _block_diagonal(interpreters)
    # Operators multiply right to left; both XOR queries restore the program.
    return loader @ interpreter @ loader @ interpreter.conj().T


def _norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, ord=2))


def _signed_subset_echo(address, bank, target, flag, table, width, correct_sign=True):
    """Integer actions in chronological gate order; no arithmetic-cost claim."""
    mask = (1 << width) - 1
    original_bit = (bank >> address) & 1
    flag ^= original_bit  # READ
    if correct_sign and flag:
        target ^= mask  # Controlled bitwise complement, not arithmetic negation.
    bank ^= 1 << address  # Q
    target = (target + sum(value for j, value in enumerate(table)
                           if (bank >> j) & 1)) & mask  # D
    bank ^= 1 << address  # Q
    target = (target - sum(value for j, value in enumerate(table)
                           if (bank >> j) & 1)) & mask  # Actual D inverse.
    if correct_sign and flag:
        target ^= mask
    flag ^= (bank >> address) & 1  # READ, using the returned bank.
    return bank, target, flag


def _tensor_phase_fixture():
    # Order: suffix-active bit, address, rotation target, two bank bits, clean flag.
    shape = (2, 2, 2, 4, 2)
    basis = list(np.ndindex(shape))

    def permutation(action):
        return _permutation([int(np.ravel_multi_index(action(*state), shape))
                             for state in basis])

    read = permutation(lambda p, x, t, z, q: (p, x, t, z, q ^ ((z >> x) & 1)))
    conditional_x = permutation(lambda p, x, t, z, q: (p, x, t ^ q, z, q))
    flip_target = permutation(lambda p, x, t, z, q: (p, x, t ^ 1, z, q))
    query = permutation(lambda p, x, t, z, q: (p, x, t, z ^ ((1 << x) if p and t else 0), q))
    query_complement = flip_target @ query @ flip_target
    embedding = np.eye(64, dtype=complex)[:, ::2]
    angles = (0.31, -0.47)
    bank_phase = np.diag([np.exp(1j * sum(angles[j] for j in range(2) if (z >> j) & 1))
                          for z in range(4)])
    ideal = np.diag([np.exp(1j * (2 * t - 1) * angles[x]) if p else 1.0
                     for p, x, t, z in np.ndindex(2, 2, 2, 4)])

    def compile_word(bank_unitary, wrong_inverse=False):
        operation = np.kron(np.eye(8), np.kron(bank_unitary, I2))
        forward = operation.conj().T @ query @ operation @ query
        complement = operation.conj().T @ query_complement @ operation @ query_complement
        middle = forward @ (complement if wrong_inverse else complement.conj().T)
        return read @ conditional_x @ middle @ conditional_x @ read

    return embedding, bank_phase, ideal, compile_word


def _weak_commutator_fixture():
    # Order: two bank bits, one arbitrary dirty helper, one private clean bit.
    # Desired P(theta_j) phases require weak commutator angles alpha_j=theta_j/2.
    theta = np.array([0.74, -0.46])
    alpha = theta / 2
    bank_flips = [_permutation([z ^ (1 << j) for z in range(4)]) for j in range(2)]
    flips = [np.kron(flip, np.eye(4)) for flip in bank_flips]
    bank_phase = np.diag([np.exp(1j * sum(alpha[j] for j in range(2)
                                        if (z >> j) & 1)) for z in range(4)])
    generator = np.kron(bank_flips[0], np.kron(X, X))
    gauge = np.cos(0.83) * np.eye(16) + 1j * np.sin(0.83) * generator
    operation = gauge @ np.kron(bank_phase, np.eye(4))
    embedding = np.eye(16, dtype=complex)[:, ::2]
    tensor_target = np.diag([np.exp(1j * sum(theta[j] for j in range(2)
                                           if (z >> j) & 1)) for z in range(4)])
    target = np.exp(-1j * sum(alpha)) * np.kron(tensor_target, I2)
    return embedding, operation, gauge, flips, alpha, target


def _swap_selected_commutator_fixture():
    # Order: suffix-active bit, address, target, two dirty bank bits, A's clean bit.
    shape = (2, 2, 2, 4, 2)
    basis = list(np.ndindex(shape))

    def permutation(action):
        return _permutation([int(np.ravel_multi_index(action(*state), shape))
                             for state in basis])

    swap = permutation(lambda p, x, t, z, c:
                       (p, x, (z >> x) & 1,
                        z ^ ((((z >> x) & 1) ^ t) << x), c))
    query = permutation(lambda p, x, t, z, c:
                        (p, x, t, z ^ ((1 << x) if p else 0), c))
    angles = np.array([0.31, -0.47])
    bank_phase = np.diag([np.exp(1j * sum(angles[j] for j in range(2)
                                        if (z >> j) & 1)) for z in range(4)])
    flip_zero = _permutation([z ^ 1 for z in range(4)])
    generator = np.kron(flip_zero, X)
    gauge = np.cos(0.79) * np.eye(8) + 1j * np.sin(0.79) * generator
    exact = gauge @ np.kron(bank_phase, I2)
    embedding = np.eye(64, dtype=complex)[:, ::2]
    ideal = np.diag([np.exp(1j * (2 * t - 1) * angles[x]) if p else 1.0
                     for p, x, t, z in np.ndindex(2, 2, 2, 4)])

    def compile_word(bank_and_private_work):
        operation = np.kron(np.eye(8), bank_and_private_work)
        return swap @ query @ operation.conj().T @ query @ operation @ swap

    return embedding, exact, angles, ideal, compile_word


class ConstantCleanStructureTests(unittest.TestCase):
    def test_exhaustive_hermitian_pauli_gap_on_one_clean_zero_code(self):
        # Two arbitrary input qubits followed by one initialized zero qubit.
        embedding = np.zeros((8, 4), dtype=complex)
        embedding[2 * np.arange(4), np.arange(4)] = 1
        paulis = []
        for factors in itertools.product((I2, X, Y, Z), repeat=3):
            matrix = np.kron(np.kron(factors[0], factors[1]), factors[2])
            paulis.extend((matrix, -matrix))
        self.assertEqual(len(paulis), 128)
        seen = set()
        for p in paulis:
            for q in paulis:
                restricted = (p - q) @ embedding
                squared = float(np.linalg.eigvalsh(
                    restricted.conj().T @ restricted)[-1])
                nearest = min((0.0, 2.0, 4.0), key=lambda x: abs(x - squared))
                self.assertLessEqual(abs(squared - nearest), ATOL)
                seen.add(nearest)
        self.assertEqual(seen, {0.0, 2.0, 4.0})
        # Distinct Paulis can agree on the code; clean X instead yields sqrt(2).
        self.assertLess(_norm((np.eye(8) - np.kron(np.eye(4), Z)) @ embedding), ATOL)
        self.assertAlmostEqual(_norm((np.eye(8) - np.kron(np.eye(4), X)) @ embedding),
                               np.sqrt(2), places=12)

    def test_same_embedding_adjoint_pairing_on_entire_program_space(self):
        rng = np.random.default_rng(918)
        interpreters = [_unitary(4, rng) for _ in range(4)]
        embedding = _unitary(4, rng)[:, :2]
        full_embedding = np.kron(np.eye(4), embedding)
        for mask in (1, 2, 3):
            actual = _echo(interpreters, mask)
            np.testing.assert_allclose(actual.conj().T @ actual, np.eye(16), atol=ATOL, rtol=0)
            accepted = full_embedding.conj().T @ actual @ full_embedding
            blocks = [embedding.conj().T @ interpreters[z ^ mask]
                      @ interpreters[z].conj().T @ embedding for z in range(4)]
            np.testing.assert_allclose(accepted, _block_diagonal(blocks), atol=ATOL, rtol=0)
            for z in range(4):
                np.testing.assert_allclose(blocks[z ^ mask], blocks[z].conj().T,
                                           atol=ATOL, rtol=0)

    def test_one_program_value_can_hide_the_same_embedding_failure(self):
        theta = 0.37
        target = _ry(theta)
        embedding = np.eye(4, dtype=complex)[:, :2]
        actual = _echo([np.eye(4), np.kron(I2, target)], 1)
        full_embedding = np.kron(I2, embedding)
        accepted = full_embedding.conj().T @ actual @ full_embedding
        np.testing.assert_allclose(accepted[:2, :2], target, atol=ATOL, rtol=0)
        np.testing.assert_allclose(accepted[2:, 2:], target.conj().T, atol=ATOL, rtol=0)
        error = _norm(accepted - np.kron(I2, target))
        self.assertAlmostEqual(error, 2 * np.sin(theta), places=12)
        self.assertGreater(error, 0.7)

    def test_different_flags_escape_same_embedding_pairing(self):
        target = _ry(0.37)
        zero = np.zeros((2, 2), dtype=complex)
        lifted = np.block([[zero, target.conj().T], [target, zero]])
        np.testing.assert_allclose(lifted, lifted.conj().T, atol=ATOL, rtol=0)
        np.testing.assert_allclose(lifted @ lifted, np.eye(4), atol=ATOL, rtol=0)
        actual = _echo([np.eye(4), lifted], 1)
        incoming = np.kron(I2, np.eye(4, dtype=complex)[:, :2])
        outgoing = np.kron(I2, np.eye(4, dtype=complex)[:, 2:])
        np.testing.assert_allclose(outgoing.conj().T @ actual @ incoming,
                                   np.kron(I2, target), atol=ATOL, rtol=0)
        np.testing.assert_allclose(incoming.conj().T @ actual @ outgoing,
                                   np.kron(I2, target.conj().T), atol=ATOL, rtol=0)
        np.testing.assert_allclose(incoming.conj().T @ actual @ incoming,
                                   np.zeros((4, 4)), atol=ATOL, rtol=0)
        # The claimed successful output is also correct before projection.
        np.testing.assert_allclose(actual @ incoming,
                                   outgoing @ np.kron(I2, target), atol=ATOL, rtol=0)
        self.assertGreater(_norm(target - target.conj().T), 0.7)

    def test_common_interpreter_cross_blocks_have_one_factorization(self):
        rng = np.random.default_rng(719)
        count, physical = 8, 4
        first = [_unitary(physical, rng) for _ in range(count)]
        second = [_unitary(physical, rng) for _ in range(count)]
        incoming = np.eye(physical, dtype=complex)[:, :2]
        outgoing = np.eye(physical, dtype=complex)[:, 2:]
        kernel = np.block([[outgoing.conj().T @ second[u]
                            @ first[v].conj().T @ incoming
                            for v in range(count)] for u in range(count)])
        left = np.vstack([outgoing.conj().T @ unitary for unitary in second])
        right = np.hstack([unitary.conj().T @ incoming for unitary in first])
        np.testing.assert_allclose(kernel, left @ right, atol=ATOL, rtol=0)
        self.assertEqual(np.linalg.matrix_rank(kernel, tol=RANK_TOL), physical)
        # Check the assembled blocks against actual program-space echo matrices.
        interpreters = first + second
        for mask in (0, 3, 7):
            actual = _echo(interpreters, count | mask)
            for v in range(count):
                u = v ^ mask
                physical_block = actual[v * physical:(v + 1) * physical,
                                        v * physical:(v + 1) * physical]
                np.testing.assert_allclose(
                    kernel[2 * u:2 * u + 2, 2 * v:2 * v + 2],
                    outgoing.conj().T @ physical_block @ incoming, atol=ATOL, rtol=0)

    def test_binary_angle_fourier_target_exceeds_the_rank_capacity(self):
        bits, alpha, physical = 3, 0.5, 4
        count = 1 << bits
        angles = [2.0 ** (-j - 1) for j in range(bits)]
        targets = [_ry(sum(angles[j] for j in range(bits) if (f >> j) & 1))
                   for f in range(count)]
        target_kernel = np.block([[alpha * targets[u ^ v]
                                   for v in range(count)] for u in range(count)])
        walsh = np.array([[(-1) ** ((u & v).bit_count())
                           for v in range(count)] for u in range(count)]) / np.sqrt(count)
        fourier = [sum(((-1) ** ((chi & f).bit_count())) * targets[f]
                       for f in range(count)) / count for chi in range(count)]
        change = np.kron(walsh, I2)
        np.testing.assert_allclose(change @ target_kernel @ change.conj().T,
                                   _block_diagonal([count * alpha * block
                                                    for block in fourier]), atol=ATOL, rtol=0)
        products = []
        for chi, block in enumerate(fourier):
            value = np.prod([np.sin(angle / 2) if (chi >> j) & 1
                             else np.cos(angle / 2) for j, angle in enumerate(angles)])
            products.extend((value, value))
            np.testing.assert_allclose(np.linalg.svd(block, compute_uv=False),
                                       [value, value], atol=ATOL, rtol=0)
        self.assertEqual(np.linalg.matrix_rank(target_kernel, tol=RANK_TOL), 2 * count)
        coarse_lower = 2.0 ** (-bits * (bits + 5) / 2)
        self.assertGreater(min(products), coarse_lower)
        delta = alpha * coarse_lower / 2
        self.assertEqual(sum(value > delta / alpha for value in products), 2 * count)
        self.assertGreater(2 * count, physical)

        # Even the best unrestricted rank-four approximation misses this target.
        left, singular, right = np.linalg.svd(target_kernel)
        truncated = (left[:, :physical] * singular[:physical]) @ right[:physical]
        spectral_error = _norm(target_kernel - truncated)
        self.assertAlmostEqual(spectral_error, singular[physical], places=12)
        block_error = max(_norm((target_kernel - truncated)[2 * u:2 * u + 2,
                                                              2 * v:2 * v + 2])
                          for u in range(count) for v in range(count))
        self.assertLessEqual(spectral_error, count * block_error + ATOL)
        self.assertGreater(block_error, delta)

    def test_cyclic_character_projector_rank_and_eigenvalue_sign(self):
        for bits in range(1, 5):
            count = 1 << bits
            root = np.exp(2j * np.pi / count)
            shift = _permutation([(j + 1) % count for j in range(count)])
            projector = sum(root ** (-y) * np.linalg.matrix_power(shift, y)
                            for y in range(count)) / count
            direct = np.array([[root ** (b - a) / count for b in range(count)]
                               for a in range(count)])
            np.testing.assert_allclose(projector, direct, atol=ATOL, rtol=0)
            np.testing.assert_allclose(projector @ projector, projector, atol=ATOL, rtol=0)
            np.testing.assert_allclose(projector.conj().T, projector, atol=ATOL, rtol=0)
            np.testing.assert_allclose(shift @ projector, root * projector, atol=ATOL, rtol=0)
            for spectators in (1, 2):
                extended = np.kron(projector, np.eye(spectators))
                self.assertEqual(np.linalg.matrix_rank(extended, tol=RANK_TOL), spectators)
            if bits >= 2:
                self.assertGreater(_norm(shift @ projector - root.conjugate() * projector),
                                   0.7)

    def test_single_addition_deficient_work_has_a_full_input_rank_witness(self):
        count = 4
        root = 1j
        shift = _permutation([1, 2, 3, 0])
        encoder = shift
        decoder = _permutation([0, 2, 1, 3])  # Bit reversal, not encoder inverse.
        incoming = np.eye(4, dtype=complex)[:, :2]  # s=1 clean, b=1 dirty.
        outgoing = np.eye(4, dtype=complex)[:, 2:]
        phase = np.exp(0.23j)
        addition = _block_diagonal([np.linalg.matrix_power(shift, y)
                                    for y in range(count)])
        actual = np.kron(np.eye(count), decoder) @ addition @ np.kron(np.eye(count), encoder)
        target = phase * np.kron(np.diag([root ** y for y in range(count)]), outgoing)
        full_error = _norm(actual @ np.kron(np.eye(count), incoming) - target)
        branches = [decoder @ np.linalg.matrix_power(shift, y) @ encoder @ incoming
                    for y in range(count)]
        branch_error = max(_norm(branches[y] - phase * root ** y * outgoing)
                           for y in range(count))
        self.assertAlmostEqual(full_error, branch_error, places=12)
        average = sum(root ** (-y) * branches[y] for y in range(count)) / count
        self.assertEqual(np.linalg.matrix_rank(average, tol=RANK_TOL), 1)
        witness = np.array([-root, 1], dtype=complex) / np.sqrt(2)
        np.testing.assert_allclose(average @ witness, np.zeros(4), atol=ATOL, rtol=0)
        self.assertAlmostEqual(np.linalg.norm((average - phase * outgoing) @ witness),
                               1.0, places=12)
        self.assertGreaterEqual(full_error, 1.0 - ATOL)

    def test_single_addition_succeeds_at_the_initialized_width_boundary(self):
        count, dirty_dimension = 4, 2  # s=m=2, with one arbitrary dirty wire.
        root = 1j
        shift = _permutation([1, 2, 3, 0])
        fourier = np.array([[root ** (-a * b) for b in range(count)]
                            for a in range(count)], dtype=complex) / np.sqrt(count)
        encoder = np.kron(fourier @ shift, np.eye(dirty_dimension))
        decoder = encoder.conj().T
        incoming = np.eye(count * dirty_dimension, dtype=complex)[:, :dirty_dimension]
        increment = np.kron(shift, np.eye(dirty_dimension))
        branches = [decoder @ np.linalg.matrix_power(increment, y) @ encoder @ incoming
                    for y in range(count)]
        for y, branch in enumerate(branches):
            np.testing.assert_allclose(branch, root ** y * incoming, atol=ATOL, rtol=0)
        full = _block_diagonal(branches)
        target = np.kron(np.diag([root ** y for y in range(count)]), incoming)
        np.testing.assert_allclose(full, target, atol=ATOL, rtol=0)

    def test_signed_subset_echo_exhaustive_dirty_inputs_and_flag_return(self):
        cases = 0
        for count, width in ((2, 3), (4, 2)):
            modulus = 1 << width
            for table in itertools.product(range(modulus), repeat=count):
                for address, bank, target in itertools.product(
                        range(count), range(1 << count), range(modulus)):
                    actual = _signed_subset_echo(address, bank, target, 0, table, width)
                    self.assertEqual(actual, (bank, (target + table[address]) % modulus, 0))
                    cases += 1
        self.assertEqual(cases, 69632)
        self.assertEqual(_signed_subset_echo(0, 1, 0, 0, (1, 0), 2, correct_sign=False),
                         (1, 3, 0))
        self.assertEqual(_signed_subset_echo(0, 1, 0, 0, (1, 0), 2), (1, 1, 0))

    def test_tensor_phase_bank_exact_full_isometry_and_inverse_order(self):
        embedding, bank_phase, ideal, compile_word = _tensor_phase_fixture()
        actual = compile_word(bank_phase)
        np.testing.assert_allclose(actual.conj().T @ actual, np.eye(64), atol=ATOL, rtol=0)
        np.testing.assert_allclose(actual @ embedding, embedding @ ideal, atol=ATOL, rtol=0)
        # On the inactive suffix, the entire operator is identity, even for flag=1.
        np.testing.assert_allclose(actual[:, :32], np.eye(64)[:, :32], atol=ATOL, rtol=0)
        self.assertLess(_norm((actual @ embedding)[1::2]), ATOL)
        wrong = compile_word(bank_phase, wrong_inverse=True)
        self.assertGreater(_norm(wrong @ embedding - embedding @ ideal), 0.5)

    def test_tensor_phase_bank_dense_approximation_charges_all_work_error(self):
        embedding, bank_phase, ideal, compile_word = _tensor_phase_fixture()
        rng = np.random.default_rng(614)
        raw = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
        generator = (raw + raw.conj().T) / 2
        generator /= _norm(generator)
        eigenvalues, eigenvectors = np.linalg.eigh(generator)
        perturbation = (eigenvectors * np.exp(0.043j * eigenvalues)) @ eigenvectors.conj().T
        scalar = np.exp(0.29j)
        approximate = scalar * perturbation @ bank_phase
        delta = _norm(approximate / scalar - bank_phase)
        actual = compile_word(approximate)
        np.testing.assert_allclose(actual, compile_word(approximate / scalar),
                                   atol=ATOL, rtol=0)
        full_defect = actual @ embedding - embedding @ ideal
        error = _norm(full_defect)
        self.assertLessEqual(error, 4 * delta + ATOL)
        commutator_error = max(
            _norm(approximate.conj().T @ flip @ approximate @ flip
                  - bank_phase.conj().T @ flip @ bank_phase @ flip)
            for flip in (np.kron(X, I2), np.kron(I2, X))
        )
        self.assertLessEqual(error, commutator_error + ATOL)
        self.assertGreater(error, 1e-3)
        # Actual inverses cancel arbitrary dense bank mixing on the inactive suffix.
        np.testing.assert_allclose(actual[:, :32], np.eye(64)[:, :32], atol=ATOL, rtol=0)
        # Approximate work return is not falsely replaced by exact flag return.
        self.assertGreater(_norm((actual @ embedding)[1::2]), 1e-3)

        # Explicit dirty/reference Bell pair, target |+>, active suffix, address zero.
        initial = np.zeros(64 * 2, dtype=complex)
        expected = np.zeros_like(initial)
        for target_bit in (0, 1):
            for bank, reference in ((0, 0), (3, 1)):
                index = int(np.ravel_multi_index((1, 0, target_bit, bank, 0),
                                                (2, 2, 2, 4, 2)))
                initial[2 * index + reference] = 0.5
                expected[2 * index + reference] = 0.5 * np.exp(1j * (2 * target_bit - 1) * 0.31)
        np.testing.assert_allclose(np.vdot(initial, initial), 1.0, atol=ATOL, rtol=0)
        reference_error = np.linalg.norm(np.kron(actual, I2) @ initial - expected)
        self.assertLessEqual(reference_error, error + ATOL)
        self.assertGreater(reference_error, 1e-3)

    def test_phase_bank_entangling_x_basis_factor_cancels_exactly(self):
        embedding, bank_phase, ideal, compile_word = _tensor_phase_fixture()
        angle = 0.63
        gauge = np.cos(angle) * np.eye(4) + 1j * np.sin(angle) * np.kron(X, X)
        batch = gauge @ bank_phase
        # The off-diagonal mixing cannot be removed by any scalar phase.
        self.assertGreater(abs(gauge[3, 0]), 0.5)
        for flip in (np.kron(X, I2), np.kron(I2, X)):
            np.testing.assert_allclose(batch.conj().T @ flip @ batch,
                                       bank_phase.conj().T @ flip @ bank_phase,
                                       atol=ATOL, rtol=0)
        np.testing.assert_allclose(compile_word(batch) @ embedding,
                                   embedding @ ideal, atol=ATOL, rtol=0)

    def test_swap_selected_commutator_needs_no_clean_readout(self):
        embedding, exact, angles, ideal, compile_word = _swap_selected_commutator_fixture()
        self.assertGreater(_norm(exact[1::2, ::2]), 0.7)
        actual = compile_word(exact)
        np.testing.assert_allclose(actual @ embedding, embedding @ ideal,
                                   atol=ATOL, rtol=0)
        self.assertLess(_norm((actual @ embedding)[1::2]), ATOL)
        # Inactivity is exact on all private-work inputs, not only initialized ones.
        np.testing.assert_allclose(actual[:, :32], np.eye(64)[:, :32], atol=ATOL, rtol=0)
        # Explicitly check the project's R_y(theta)=exp(-i theta Y) convention.
        hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        change = np.diag([1, 1j]) @ hadamard
        physical_change = np.kron(np.eye(4), np.kron(change, np.eye(8)))
        y_word = physical_change @ actual @ physical_change.conj().T
        y_target = _block_diagonal([
            np.kron(_ry(angles[x]), np.eye(4)) if p else np.eye(8)
            for p, x in np.ndindex(2, 2)])
        np.testing.assert_allclose(y_word @ embedding, embedding @ y_target,
                                   atol=ATOL, rtol=0)

    def test_swap_selected_commutator_dense_error_and_inactive_cancellation(self):
        embedding, exact, angles, ideal, compile_word = _swap_selected_commutator_fixture()
        rng = np.random.default_rng(3811)
        raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
        generator = (raw + raw.conj().T) / 2
        generator /= _norm(generator)
        values, vectors = np.linalg.eigh(generator)
        perturbation = (vectors * np.exp(0.037j * values)) @ vectors.conj().T
        operation = np.exp(0.29j) * perturbation @ exact
        bank_embedding = np.eye(8, dtype=complex)[:, ::2]
        errors = []
        for j in range(2):
            flip = np.kron(_permutation([z ^ (1 << j) for z in range(4)]), I2)
            weak_target = np.diag([
                np.exp(1j * angles[j] * (1 - 2 * ((z >> j) & 1))) for z in range(4)])
            commutator = operation.conj().T @ flip @ operation @ flip
            errors.append(_norm(commutator @ bank_embedding - bank_embedding @ weak_target))
        actual = compile_word(operation)
        error = _norm(actual @ embedding - embedding @ ideal)
        self.assertLessEqual(error, max(errors) + ATOL)
        self.assertGreater(error, 1e-3)
        self.assertGreater(_norm((actual @ embedding)[1::2]), 1e-3)
        np.testing.assert_allclose(actual[:, :32], np.eye(64)[:, :32], atol=ATOL, rtol=0)
        np.testing.assert_allclose(actual, compile_word(operation / np.exp(0.29j)),
                                   atol=ATOL, rtol=0)
        # A full phase-bank approximation has the sharper direct 2*delta bound.
        # Omit the gauge here: the preceding A is deliberately far from D itself.
        phase_bank = np.diag([
            np.exp(1j * sum(angles[j] for j in range(2) if (z >> j) & 1))
            for z, clean in np.ndindex(4, 2)])
        approximate_bank = np.exp(0.29j) * perturbation @ phase_bank
        delta = _norm(approximate_bank / np.exp(0.29j) - phase_bank)
        from_full_batch = compile_word(approximate_bank)
        full_batch_error = _norm(from_full_batch @ embedding - embedding @ ideal)
        self.assertLessEqual(full_batch_error, 2 * delta + ATOL)
        self.assertGreater(full_batch_error, 1e-3)
        np.testing.assert_allclose(from_full_batch[:, :32], np.eye(64)[:, :32],
                                   atol=ATOL, rtol=0)

    def test_weak_commutators_extract_batch_despite_private_work_leakage(self):
        embedding, operation, gauge, flips, alpha, target = _weak_commutator_fixture()
        # A itself strongly leaks its clean bit and entangles the dirty helper.
        self.assertGreater(_norm((operation @ embedding)[1::2]), 0.7)
        first_column = (operation @ embedding)[:, 0].reshape(4, 2, 2)
        helper_density = np.einsum('bdc,bec->de', first_column, first_column.conj())
        self.assertLess(float(np.trace(helper_density @ helper_density).real), 0.6)
        for j, flip in enumerate(flips):
            np.testing.assert_allclose(gauge @ flip, flip @ gauge, atol=ATOL, rtol=0)
            weak_target = np.kron(np.diag([
                np.exp(1j * alpha[j] * (1 - 2 * ((z >> j) & 1)))
                for z in range(4)]), I2)
            commutator = operation.conj().T @ flip @ operation @ flip
            np.testing.assert_allclose(commutator @ embedding, embedding @ weak_target,
                                       atol=ATOL, rtol=0)

        all_flip = flips[0] @ flips[1]
        # Exactly two calls to the common A/A^dagger, with rightmost acting first.
        extracted = all_flip @ operation.conj().T @ all_flip @ operation
        np.testing.assert_allclose(extracted @ embedding, embedding @ target,
                                   atol=ATOL, rtol=0)
        self.assertLess(_norm((extracted @ embedding)[1::2]), ATOL)
        # Purify the complete bank-plus-dirty-helper input, including its coherence.
        reference_dimension = embedding.shape[1]
        initial = embedding.ravel() / np.sqrt(reference_dimension)
        expected = (embedding @ target).ravel() / np.sqrt(reference_dimension)
        np.testing.assert_allclose(np.kron(extracted, np.eye(reference_dimension)) @ initial,
                                   expected, atol=ATOL, rtol=0)

    def test_weak_commutator_errors_charge_full_output_and_wrong_word(self):
        embedding, exact, _, flips, alpha, target = _weak_commutator_fixture()
        rng = np.random.default_rng(28719)
        raw = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16))
        generator = (raw + raw.conj().T) / 2
        generator /= _norm(generator)
        values, vectors = np.linalg.eigh(generator)
        perturbation = (vectors * np.exp(0.031j * values)) @ vectors.conj().T
        operation = perturbation @ exact
        errors = []
        for j, flip in enumerate(flips):
            weak_target = np.kron(np.diag([
                np.exp(1j * alpha[j] * (1 - 2 * ((z >> j) & 1)))
                for z in range(4)]), I2)
            commutator = operation.conj().T @ flip @ operation @ flip
            errors.append(_norm(commutator @ embedding - embedding @ weak_target))
        all_flip = flips[0] @ flips[1]
        extracted = all_flip @ operation.conj().T @ all_flip @ operation
        error = _norm(extracted @ embedding - embedding @ target)
        self.assertLessEqual(error, sum(errors) + ATOL)
        self.assertGreater(error, 1e-3)
        self.assertGreater(_norm((extracted @ embedding)[1::2]), 1e-3)
        # Swapping the forward and inverse calls does not preserve the contract.
        wrong = all_flip @ operation @ all_flip @ operation.conj().T
        self.assertGreater(_norm(wrong @ embedding - embedding @ target), 0.5)

    def test_weak_to_batch_linear_error_accumulation_is_sharp(self):
        beta = 0.021
        local_error = 2 * np.sin(beta / 2)
        for count in range(1, 7):
            alpha = np.array([(-1) ** j * (0.13 + 0.017 * j) for j in range(count)])
            signs = np.array([[1 - 2 * ((z >> j) & 1) for j in range(count)]
                              for z in range(1 << count)])
            for angle in alpha:
                local_actual = np.exp(1j * (angle + beta) * np.array([1, -1]))
                local_target = np.exp(1j * angle * np.array([1, -1]))
                self.assertAlmostEqual(float(np.max(abs(local_actual - local_target))),
                                       local_error, places=12)
            # A=product P(alpha_j+beta) extracts exp(-i sum_j(alpha_j+beta) Z_j).
            actual = np.exp(-1j * (signs @ (alpha + beta)))
            target = np.exp(-1j * (signs @ alpha))
            error = float(np.max(abs(actual - target)))
            expected = 2 * np.sin(count * beta / 2)
            self.assertLess(count * beta, np.pi / 2)
            self.assertAlmostEqual(error, expected, places=12)
            self.assertLessEqual(error, count * local_error + ATOL)
            self.assertGreaterEqual(error / local_error, 0.99 * count)
            # For count*beta<pi/2 the endpoint phases +/-count*beta have
            # optimal common-scalar center 1, so allowing a scalar cannot help.
            endpoints = actual[[0, -1]] / target[[0, -1]]
            np.testing.assert_allclose(endpoints,
                                       np.exp(1j * np.array([-count * beta, count * beta])),
                                       atol=ATOL, rtol=0)


if __name__ == "__main__":
    unittest.main()
