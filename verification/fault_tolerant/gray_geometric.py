"""Exact bounded gate-word model for the CP22 Gray geometric primitive.

The raw chain is controlled by an unchanged enable bit.  Its scratch is
zero on entry and returned to zero for every data/enable input.  A separate
outer decoder uses unconditional CNOTs and is intended for enable-one state
preparation.  These are logical gates, not emitted QASM or a frame compiler.
"""

from dataclasses import dataclass
from fractions import Fraction as F

from exact_arithmetic import Q2, CQ2, CZ, CO, CI


HALF_ROOT = CQ2(Q2(0, F(1, 2)))


@dataclass(frozen=True)
class Gate:
    op: str
    qubits: tuple
    stage: str = ""


def layout(t):
    if not isinstance(t, int) or isinstance(t, bool) or t < 1:
        raise ValueError("positive integer data width required")
    return {"data": tuple(range(t)), "enable": t,
            "scratch": tuple(range(t + 1, 2 * t)), "qubits": 2 * t}


def inverse_word(word):
    inverse_phase = {"S": "SDG", "SDG": "S", "T": "TDG", "TDG": "T"}
    return [Gate(inverse_phase.get(g.op, g.op), g.qubits, g.stage)
            for g in reversed(word)]


def emit_chain(t):
    """Emit a controlled reflected-Gray ordered-H chain with t-1 scratch."""
    registers = layout(t)

    def emit(data, enable, scratch, path):
        if len(data) == 1:
            return [Gate("CH", (enable, data[0]), path + "/base")]
        high, lower = data[0], data[1:]
        flag = scratch[0]
        first_compute = [Gate("X", (high,), path + "/first_flag_compute"),
                         Gate("CCX", (enable, high, flag), path + "/first_flag_compute"),
                         Gate("X", (high,), path + "/first_flag_compute")]
        first_uncompute = [Gate(g.op, g.qubits, path + "/first_flag_uncompute")
                           for g in inverse_word(first_compute)]
        word = first_compute + emit(lower, flag, scratch[1:], path + "/first") + first_uncompute

        # The child flag has already been erased.  Reuse this entire scratch
        # pool for the bridge predicate; none of its controls is the target.
        predicate = [enable] + list(lower)
        bridge_compute = [Gate("X", (bit,), path + "/bridge_compute") for bit in lower[1:]]
        bridge_compute.append(Gate("CCX", (predicate[0], predicate[1], scratch[0]), path + "/bridge_compute"))
        for index in range(2, len(predicate)):
            bridge_compute.append(Gate("CCX", (scratch[index - 2], predicate[index], scratch[index - 1]), path + "/bridge_compute"))
        bridge_uncompute = [Gate(g.op, g.qubits, path + "/bridge_uncompute")
                            for g in inverse_word(bridge_compute)]
        word += bridge_compute + [Gate("CH", (scratch[len(predicate) - 2], high), path + "/bridge")] + bridge_uncompute

        second_compute = Gate("CCX", (enable, high, flag), path + "/second_flag_compute")
        second_uncompute = Gate("CCX", (enable, high, flag), path + "/second_flag_uncompute")
        reverse_x = Gate("X", (lower[0],), path + "/reverse_orientation")
        word += [second_compute, reverse_x] + emit(lower, flag, scratch[1:], path + "/second") + [reverse_x, second_uncompute]
        return word

    return emit(registers["data"], registers["enable"], registers["scratch"], "root")


def emit_decoder(t):
    """Unconditional Gray-to-binary decoder, only for the outer wrapper."""
    data = layout(t)["data"]
    return [Gate("CX", (data[index - 1], data[index]), "outer_decoder")
            for index in range(1, t)]


def controlled_h_decomposition(control, target):
    """Chronological A†, CZ, A, where A=S H T H S†; literal phases cancel."""
    before = [Gate("SDG", (target,)), Gate("H", (target,)), Gate("TDG", (target,)),
              Gate("H", (target,)), Gate("S", (target,))]
    after = [Gate("SDG", (target,)), Gate("H", (target,)), Gate("T", (target,)),
             Gate("H", (target,)), Gate("S", (target,))]
    return before + [Gate("CZ", (control, target))] + after


def _accumulate(state, index, value):
    value = state.get(index, CZ) + value
    if value == CZ:
        state.pop(index, None)
    else:
        state[index] = value


def apply_word(word, state):
    """Apply exact logical gates to a sparse state, retaining every work bit."""
    state = dict(state)
    for gate in word:
        op, q = gate.op, gate.qubits
        if op in ("X", "CX", "CCX"):
            controls, target = q[:-1], q[-1]
            state = {index ^ (1 << target) if all((index >> c) & 1 for c in controls) else index: amplitude
                     for index, amplitude in state.items()}
        elif op in ("H", "CH"):
            target = q[-1]
            controls = q[:-1]
            result = {}
            for index, amplitude in state.items():
                if not all((index >> c) & 1 for c in controls):
                    _accumulate(result, index, amplitude)
                    continue
                bit = (index >> target) & 1
                base = index & ~(1 << target)
                _accumulate(result, base, amplitude * HALF_ROOT)
                _accumulate(result, base | (1 << target), amplitude * HALF_ROOT * (-1 if bit else 1))
            state = result
        elif op == "CZ":
            state = {index: -amplitude if all((index >> c) & 1 for c in q) else amplitude
                     for index, amplitude in state.items()}
        elif op in ("S", "SDG", "T", "TDG"):
            phase = {"S": CI, "SDG": -CI, "T": (CO + CI) * HALF_ROOT,
                     "TDG": (CO - CI) * HALF_ROOT}[op]
            state = {index: amplitude * phase if (index >> q[0]) & 1 else amplitude
                     for index, amplitude in state.items()}
        else:
            raise ValueError("unsupported exact logical gate")
    return state


def logical_basis(t, data_value, enable):
    registers = layout(t)
    if not 0 <= data_value < (1 << t) or enable not in (0, 1):
        raise ValueError("invalid logical basis value")
    return (enable << registers["enable"]) | sum(
        ((data_value >> (t - 1 - index)) & 1) << bit
        for index, bit in enumerate(registers["data"]))


def read_data(t, basis):
    return sum(((basis >> bit) & 1) << (t - 1 - index)
               for index, bit in enumerate(layout(t)["data"]))


def expected_amplitude(exponent):
    """Positive 2**(-exponent/2), exactly in Q(sqrt(2))."""
    if exponent % 2:
        return CQ2(Q2(0, F(1, 1 << ((exponent + 1) // 2))))
    return CQ2(F(1, 1 << (exponent // 2)))
