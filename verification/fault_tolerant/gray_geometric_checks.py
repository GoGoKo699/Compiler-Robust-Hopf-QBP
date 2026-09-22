"""Focused exact CP22 Gray-chain verification; no generic compiler claims."""

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from exact_arithmetic import Q2, CZ, CO
from gray_geometric import (
    Gate, HALF_ROOT, apply_word, controlled_h_decomposition, emit_chain,
    emit_decoder, expected_amplitude, inverse_word, layout, logical_basis, read_data,
)


ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def direct_gray_chain(t, data_value, enable):
    """Independent product of ordered two-level H matrices in Gray order."""
    state = {logical_basis(t, data_value, enable): CO}
    if not enable:
        return state
    gray = [index ^ (index >> 1) for index in range(1 << t)]
    for first, second in zip(gray, gray[1:]):
        a, b = logical_basis(t, first, 1), logical_basis(t, second, 1)
        x, y = state.pop(a, CZ), state.pop(b, CZ)
        for index, value in ((a, (x + y) * HALF_ROOT), (b, (x - y) * HALF_ROOT)):
            if value != CZ:
                state[index] = value
    return state


def check_ch_decomposition():
    logical = [Gate("CH", (0, 1))]
    expanded = controlled_h_decomposition(0, 1)
    for index in range(4):
        initial = {index: CO}
        actual = apply_word(expanded, initial)
        require(actual == apply_word(logical, initial), "literal-phase controlled-H decomposition")
        require(apply_word(inverse_word(expanded), actual) == initial, "expanded CH actual adjoint")
    counts = Counter(g.op for g in expanded)
    require(counts["T"] == counts["TDG"] == 1, "two non-Clifford phase gates in CH decomposition")
    return {"all_basis_columns": 4, "literal_phase_equal": True,
            "chronological_word": [g.op for g in expanded],
            "counted_operations": dict(sorted(counts.items())), "T_and_Tdag_count": 2}


def check_width(t):
    registers = layout(t)
    word, decoder = emit_chain(t), emit_decoder(t)
    scratch_mask = sum(1 << bit for bit in registers["scratch"])
    full_columns = 0
    for enable in (0, 1):
        for data in range(1 << t):
            initial = {logical_basis(t, data, enable): CO}
            actual = apply_word(word, initial)
            require(all(index & scratch_mask == 0 for index in actual), "all scratch exactly returned on every logical column")
            require(all(((index >> registers["enable"]) & 1) == enable for index in actual), "enable unchanged")
            require(actual == direct_gray_chain(t, data, enable), "independent ordered Gray-chain matrix columns")
            require(apply_word(inverse_word(word), actual) == initial, "actual reversed chain word")
            if not enable:
                require(actual == initial, "disabled raw chain is exactly identity on arbitrary data")
            full_columns += 1

    initial = {logical_basis(t, 0, 1): CO}
    prepared = apply_word(word + decoder, initial)
    M = 1 << t
    expected = {logical_basis(t, j, 1): expected_amplitude(j + 1 if j < M - 1 else M - 1)
                for j in range(M)}
    require(prepared == expected, "positive exact geometric amplitudes after outer decoder")
    require(apply_word(inverse_word(word + decoder), prepared) == initial, "actual inverse of complete preparation wrapper")
    probabilities = [prepared[logical_basis(t, j, 1)].abs2() for j in range(M)]
    require(all(p.b == 0 for p in probabilities), "rational dyadic geometric probabilities")
    rational = [p.a for p in probabilities]
    require(rational[:-1] == [F(1, 1 << (j + 1)) for j in range(M - 1)], "all frozen probabilities")
    require(rational[-1] == F(1, 1 << (M - 1)), "one unresolved terminal tail")
    require(sum(rational) == 1, "exact probability normalization")

    # A coherent reference entangled with both a disabled nonzero data input
    # and an enabled nonzero data input tests linearity across these branches.
    reference = registers["qubits"]
    first_data, second_data = M - 1, M // 2
    witness = {logical_basis(t, first_data, 0): HALF_ROOT,
               logical_basis(t, second_data, 1) | (1 << reference): HALF_ROOT}
    witness_expected = {}
    for index, amplitude in direct_gray_chain(t, first_data, 0).items():
        witness_expected[index] = amplitude * HALF_ROOT
    for index, amplitude in direct_gray_chain(t, second_data, 1).items():
        witness_expected[index | (1 << reference)] = amplitude * HALF_ROOT
    witness_actual = apply_word(word, witness)
    require(witness_actual == witness_expected, "coherent enabled/disabled reference witness")
    require(all(index & scratch_mask == 0 for index in witness_actual), "reference witness scratch cleanup")
    require(apply_word(inverse_word(word), witness_actual) == witness, "reference witness actual reverse")
    counts = Counter(g.op for g in word)
    require(len(registers["scratch"]) == t - 1, "allocated shared scratch pool")
    return {"t": t, "M": M, "physical_qubits_without_reference": registers["qubits"],
            "scratch_bits": len(registers["scratch"]), "root_enable_bits": 1,
            "all_initialized_scratch_input_columns": full_columns,
            "counted_chain_operations": {op: counts[op] for op in ("X", "CCX", "CH")},
            "counted_chain_word_length": len(word), "outer_decoder_CX_count": len(decoder),
            "exact_probabilities": [str(p) for p in rational],
            "frozen_probability_mass": str(sum(rational[:-1])), "terminal_tail_probability": str(rational[-1]),
            "all_amplitudes_positive": True, "all_logical_columns_scratch_clean": True,
            "actual_reverse_passed": True, "nonzero_data_controlled_reference_witness": True}


def check_structural_regressions():
    t = 2
    word = emit_chain(t)
    initial = {logical_basis(t, 0, 1): CO}
    expected = apply_word(word, initial)
    without_orientation = [g for g in word if not g.stage.endswith("/reverse_orientation")]
    require(apply_word(without_orientation, initial) != expected, "omitted reverse-half X conjugations must be detected")

    # Deliberately defer erasing the first-child enable until after the bridge
    # has modified high.  This also violates the bridge's clean-scratch entry.
    deferred = [g for g in word if g.stage == "root/first_flag_uncompute"]
    wrong = [g for g in word if g.stage != "root/first_flag_uncompute"]
    insertion = max(index for index, g in enumerate(wrong) if g.stage == "root/bridge_uncompute") + 1
    wrong[insertion:insertion] = deferred
    wrong_state = apply_word(wrong, initial)
    mask = sum(1 << bit for bit in layout(t)["scratch"])
    require(wrong_state != expected, "uncompute-after-bridge error must be detected")
    require(any(index & mask for index in wrong_state), "deferred prefix cleanup leaks scratch")
    return {"t": t, "missing_reverse_half_X_detected": True,
            "prefix_uncompute_deferred_past_bridge_detected": True,
            "deferred_prefix_uncompute_leaks_scratch": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "gray_geometric_checks.json")
    args = parser.parse_args()
    ch = check_ch_decomposition()
    widths = [check_width(t) for t in range(1, 6)]
    for previous, row in zip(widths, widths[1:]):
        t = row["t"]
        a, b = previous["counted_chain_operations"], row["counted_chain_operations"]
        require(b["CH"] == 2 * a["CH"] + 1, "emitted CH recurrence")
        require(b["CCX"] == 2 * a["CCX"] + 2 * t + 2, "emitted Toffoli recurrence")
        require(b["X"] == 2 * a["X"] + 2 * t + 2, "emitted X recurrence")
    regressions = check_structural_regressions()
    receipt = {
        "checkpoint": 22, "status": "passed",
        "arithmetic": "Exact sparse states in Q(sqrt(2), i); every emitted logical gate is applied.",
        "controlled_H": ch, "width_cases": widths, "regressions": regressions,
        "total_initialized_scratch_columns": sum(row["all_initialized_scratch_input_columns"] for row in widths),
        "counting": {"source": "Counts are read from literal emitted gate words, then their finite recurrences are checked.",
                     "CH_recurrence": "H_t = 2 H_(t-1) + 1, H_1 = 1",
                     "CCX_recurrence": "C_t = 2 C_(t-1) + 2t + 2, C_1 = 0",
                     "qualification": "The asymptotic recurrence solution and seven-T Toffoli compilation are analytic. No compiled T count or generic frame resource bound is certified by these finite tests."},
        "scope": [
            "Widths t=1..5; all 124 data/enable basis columns with initialized scratch, exact positive geometric amplitudes, frozen probabilities, terminal tail, and actual reverse words.",
            "The raw chain is controlled and exactly disabled on every data input. The separate unconditional outer Gray decoder is tested only as an enable-one state-preparation wrapper.",
            "The child-enable scratch is erased before the bridge changes the high data bit and reuses that scratch pool. An explicit wrong-order regression leaks scratch.",
            "Each width includes a coherent untouched-reference witness with nonzero data and both enable values.",
            "Controlled-H has an independently checked literal-phase Clifford+T decomposition. Other logical Toffoli gates are evaluated as exact permutations.",
            "No old suite, generic frame compiler, coefficient sampler, digit lookup, QASM, or end-to-end resource theorem is claimed.",
        ],
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ("gray_geometric.py", "gray_geometric_checks.py",
                                       "exact_arithmetic.py")},
    }
    path = args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "width_cases": len(widths),
                      "initialized_scratch_columns": receipt["total_initialized_scratch_columns"],
                      "reference_witnesses": len(widths), "regressions": len(regressions) - 1,
                      "receipt": str(path)}, indent=2))


if __name__ == "__main__":
    main()
