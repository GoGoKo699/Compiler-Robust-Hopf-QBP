"""Exact finite audits of the dirty modular-lookup query construction.

Q is a whole-word XOR-query interface; INC is an exact controlled-increment
interface. The architecture tests below do not synthesize either interface or
infer its cost from a truth-table permutation. Native carry and small complete
adder tests separately expand literal Clifford+T gates, including all dirty
work and a purifying reference. Their deliberately simple increment emitter
is quadratic, and is not evidence for the cited linear increment cost.
"""
from __future__ import annotations

from itertools import product
from random import Random
import unittest

from tests.test_identical_phase_batching import (
    _exact_apply, _increment, _native, _permutation_word,
)
from verification.fault_tolerant.exact_arithmetic import CQ2, Q2


def _levels(width):
    blocks = [(0, width)]
    result = []
    while any(stop - start > 1 for start, stop in blocks):
        nodes = [(start, (start + stop) // 2, stop)
                 for start, stop in blocks if stop - start > 1]
        result.append(nodes)
        blocks = [child for start, stop in blocks for child in
                  (((start, (start + stop) // 2), ((start + stop) // 2, stop))
                   if stop - start > 1 else ((start, stop),))]
    return result


def _registers(width, address_width=0):
    y = tuple(range(address_width, address_width + width))
    g = tuple(range(address_width + width, address_width + 2 * width))
    a = tuple(range(address_width + 2 * width, address_width + 3 * width))
    return y, g, a


def _carry_query(y, g, a, segments):
    """Toggle all carries in disjoint segments, restoring y and a.

    The four Q calls use the SAME complete table word, even when only a subset
    of its bits participates in the carry calculation.
    """
    active = [i for start, stop in segments for i in range(start, stop)]
    ladder = [('CCX', y[i], g[i - 1], g[i])
              for start, stop in segments for i in range(start + 1, stop)]
    generation = ([('X', y[i]) for i in active]
                  + [('CCX', a[i], y[i], g[i]) for i in active]
                  + [('X', y[i]) for i in active])
    return ([('Q', y)] + ladder[::-1] + [('Q', a)] + generation
            + [('Q', a)] + generation + ladder + [('Q', y)])


def _level_word(y, g, a, nodes, omit_complements=False):
    carry = _carry_query(y, g, a, [(lo, mid) for lo, mid, hi in nodes])
    complement = ([] if omit_complements else
                  [('CX', g[mid - 1], y[i])
                   for lo, mid, hi in nodes for i in range(mid, hi)])
    increment = [('INC', g[mid - 1], y[mid:hi], 1)
                 for lo, mid, hi in nodes]
    decrement = [('INC', g[mid - 1], y[mid:hi], -1)
                 for lo, mid, hi in reversed(nodes)]
    return complement + carry + increment + carry + decrement + complement


def _lookup_word(width, address_width=0, omit_complements=False):
    y, g, a = _registers(width, address_width)
    return [gate for nodes in _levels(width)
            for gate in _level_word(y, g, a, nodes, omit_complements)] + [('Q', y)]


def _field(basis, wires):
    return sum(((basis >> wire) & 1) << j for j, wire in enumerate(wires))


def _replace(basis, wires, value):
    for j, wire in enumerate(wires):
        basis = (basis & ~(1 << wire)) | (((value >> j) & 1) << wire)
    return basis


def _apply_interfaces(basis, word, table, address_width=0):
    for gate in word:
        if gate[0] == 'Q':
            value = table[basis & ((1 << address_width) - 1)]
            for j, wire in enumerate(gate[1]):
                if (value >> j) & 1:
                    basis ^= 1 << wire
        elif gate[0] == 'INC':
            _, control, wires, direction = gate
            if (basis >> control) & 1:
                value = (_field(basis, wires) + direction) % (1 << len(wires))
                basis = _replace(basis, wires, value)
        else:
            basis = _permutation_word(basis, [gate])
    return basis


def _carry_mask(y, f, segments):
    result = 0
    for start, stop in segments:
        for i in range(start, stop):
            mask = (1 << (i - start + 1)) - 1
            carry = (((y >> start) & mask) + ((f >> start) & mask)) > mask
            result |= int(carry) << i
    return result


def _small_native(word, table, address_width, borrowed):
    """Native fixture only: one-bit address and a quadratic INC emitter."""
    assert address_width == 1 and len(table) == 2
    expanded = []
    for gate in word:
        if gate[0] == 'Q':
            for j, wire in enumerate(gate[1]):
                if (table[0] >> j) & 1:
                    expanded.append(('X', wire))
                if ((table[0] ^ table[1]) >> j) & 1:
                    expanded.append(('CX', 0, wire))
        elif gate[0] == 'INC':
            _, control, wires, direction = gate
            increment = _increment(control, wires, borrowed)
            expanded.extend(increment if direction == 1 else increment[::-1])
        else:
            expanded.append(gate)
    return _native(expanded)


class ModularLookupQueryTests(unittest.TestCase):
    def test_carry_query_all_dirty_basis_inputs(self):
        for width in range(1, 5):
            y, g, a = _registers(width)
            segments = [(0, width)]
            word = _carry_query(y, g, a, segments)
            self.assertEqual(sum(gate[0] == 'Q' for gate in word), 4)
            self.assertEqual(sum(gate[0] == 'CCX' for gate in word), 4 * width - 2)
            for f, value, carry_work, query_work in product(range(1 << width), repeat=4):
                basis = value | (carry_work << width) | (query_work << (2 * width))
                expected = basis ^ (_carry_mask(value, f, segments) << width)
                self.assertEqual(_apply_interfaces(basis, word, [f]), expected)

    def test_disjoint_carry_segments_leave_other_bits_untouched(self):
        width = 5
        y, g, a = _registers(width)
        segments = [(0, 2), (3, 5)]
        word = _carry_query(y, g, a, segments)
        rng = Random(82947)
        for _ in range(1000):
            f, value, carry_work, query_work = [rng.getrandbits(width) for _ in range(4)]
            basis = value | (carry_work << width) | (query_work << (2 * width))
            expected = basis ^ (_carry_mask(value, f, segments) << width)
            self.assertEqual(_apply_interfaces(basis, word, [f]), expected)

    def test_complete_lookup_all_dirty_basis_inputs(self):
        for width in range(1, 4):
            word = _lookup_word(width)
            y, _, _ = _registers(width)
            for f, value, carry_work, query_work in product(range(1 << width), repeat=4):
                basis = value | (carry_work << width) | (query_work << (2 * width))
                expected = _replace(basis, y, (value + f) % (1 << width))
                self.assertEqual(_apply_interfaces(basis, word, [f]), expected)

    def test_query_count_width_and_large_non_power_of_two_cases(self):
        rng = Random(73405)
        for width in list(range(1, 18)) + [24, 31, 32, 47, 64, 127, 128]:
            address_width = 2
            word = _lookup_word(width, address_width)
            y, _, _ = _registers(width, address_width)
            depth = (width - 1).bit_length()
            self.assertEqual(len(_levels(width)), depth)
            self.assertEqual(sum(gate[0] == 'Q' for gate in word), 8 * depth + 1)
            # All data and work are arbitrary; no initialized carry appears.
            for _ in range(25):
                table = [rng.getrandbits(width) for _ in range(4)]
                basis = rng.getrandbits(address_width + 3 * width)
                expected = _replace(basis, y, (_field(basis, y) + table[basis & 3])
                                    % (1 << width))
                self.assertEqual(_apply_interfaces(basis, word, table, address_width), expected)

    def test_native_complete_lookup_preserves_reference_coherence(self):
        width, address_width, table = 2, 1, [1, 2]
        y, _, a = _registers(width, address_width)
        word = _small_native(_lookup_word(width, address_width), table, address_width, a)
        physical_width = address_width + 3 * width
        initial, expected = {}, {}
        # Every arbitrary physical input has its own orthogonal reference label.
        for label in range(1 << physical_width):
            basis = label | (label << physical_width)
            coefficient = CQ2(Q2(label + 1), Q2(1 - label))
            output = _replace(basis, y, (_field(basis, y) + table[basis & 1])
                              % (1 << width))
            initial[basis] = coefficient
            expected[output] = coefficient
        self.assertEqual(_exact_apply(initial, word), expected)

    def test_missing_sign_correction_fails(self):
        width = 3
        value, f, carry_work, query_work = 1, 1, 1, 0
        basis = value | (carry_work << width) | (query_work << (2 * width))
        correct = _apply_interfaces(basis, _lookup_word(width), [f])
        broken = _apply_interfaces(basis, _lookup_word(width, omit_complements=True), [f])
        self.assertEqual(correct & 7, 2)
        self.assertEqual(broken & 7, 6)
        self.assertNotEqual(broken, correct)

    def test_wrong_ladder_order_and_unreturned_carries_fail(self):
        width = 3
        y, g, a = _registers(width)
        word = _carry_query(y, g, a, [(0, width)])
        ladder = [('CCX', y[i], g[i - 1], g[i]) for i in range(1, width)]
        broken = word[:-len(ladder) - 1] + ladder[::-1] + [word[-1]]
        basis, f = 7, 1
        self.assertEqual(_apply_interfaces(basis, word, [f]), basis ^ (7 << width))
        self.assertNotEqual(_apply_interfaces(basis, broken, [f]), basis ^ (7 << width))
        # One carry call alone changes a borrowed word, even if its boundary
        # output could be read correctly. The second call is essential.
        self.assertNotEqual(_apply_interfaces(basis, word, [f]) >> width, basis >> width)


if __name__ == '__main__':
    unittest.main()
