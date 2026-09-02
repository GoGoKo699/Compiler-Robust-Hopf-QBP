"""Self-contained binary--one-hot tree decoder for Hopf prefix frames.

The construction uses only fixed-width reversible gates and coherent CNOT-tree
copying. It replaces the previously imported unary-to-binary subroutine.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np

from .frames import hopf_ry


GateKind = Literal["x", "cx", "ccx"]


@dataclass(frozen=True)
class ReversibleGate:
    kind: GateKind
    qubits: tuple[int, ...]


@dataclass(frozen=True)
class TreeDecoderLayout:
    t: int
    branches: int
    binary: tuple[int, ...]
    unary: tuple[int, ...]
    internal_by_depth: tuple[tuple[int, ...], ...]
    shared_pool: tuple[int, ...]
    total_qubits: int

    @property
    def workspace_qubits(self) -> int:
        return self.total_qubits - self.t


@dataclass(frozen=True)
class TreeDecoderResourceRow:
    t: int
    branches: int
    unary_register_qubits: int
    internal_indicator_qubits: int
    shared_copy_reduction_qubits: int
    clean_workspace_qubits: int
    forward_depth_proxy: int
    round_trip_depth_proxy: int
    forward_gate_proxy: int
    round_trip_gate_proxy: int
    toffoli_gates_forward: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


@dataclass(frozen=True)
class ConditionedPrefixResourceRow:
    n: int
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    clean_workspace_qubits: int
    decoder_round_trip_depth_proxy: int
    suffix_predicate_depth_proxy: int
    control_fanout_depth_proxy: int
    givens_layer_depth_proxy: int
    total_depth_proxy: int
    decoder_round_trip_gate_proxy: int
    suffix_predicate_gate_proxy: int
    control_fanout_gate_proxy: int
    givens_gate_proxy: int
    total_gate_proxy: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


def _validate_t(t: int) -> None:
    if t < 1:
        raise ValueError("t must be positive.")


def _ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive.")
    return (value - 1).bit_length()


def tree_decoder_layout(t: int) -> TreeDecoderLayout:
    _validate_t(t)
    branches = 1 << t
    cursor = 0
    binary = tuple(range(cursor, cursor + t))
    cursor += t
    unary = tuple(range(cursor, cursor + branches))
    cursor += branches
    internal: list[tuple[int, ...]] = []
    for depth in range(t):
        width = 1 << depth
        internal.append(tuple(range(cursor, cursor + width)))
        cursor += width
    pool_width = branches - 1 - t
    shared_pool = tuple(range(cursor, cursor + pool_width))
    cursor += pool_width
    return TreeDecoderLayout(
        t=t,
        branches=branches,
        binary=binary,
        unary=unary,
        internal_by_depth=tuple(internal),
        shared_pool=shared_pool,
        total_qubits=cursor,
    )


def _fanout_operations(
    source: int, targets: tuple[int, ...]
) -> tuple[tuple[ReversibleGate, ...], tuple[int, ...]]:
    active = [source]
    remaining = list(targets)
    operations: list[ReversibleGate] = []
    while remaining:
        new_controls: list[int] = []
        for control in tuple(active):
            if not remaining:
                break
            target = remaining.pop(0)
            operations.append(ReversibleGate("cx", (control, target)))
            new_controls.append(target)
        active.extend(new_controls)
    return tuple(operations), tuple(active)


def _parity_tree_operations(
    inputs: tuple[int, ...], ancillas: tuple[int, ...]
) -> tuple[tuple[ReversibleGate, ...], int]:
    if not inputs:
        raise ValueError("A parity tree needs at least one input.")
    if len(inputs) == 1:
        if ancillas:
            raise ValueError("A one-input parity tree needs no ancillas.")
        return (), inputs[0]
    if len(ancillas) != len(inputs) - 1:
        raise ValueError("A binary parity tree needs len(inputs)-1 ancillas.")
    current = list(inputs)
    pool = iter(ancillas)
    operations: list[ReversibleGate] = []
    while len(current) > 1:
        next_level: list[int] = []
        for first, second in zip(current[0::2], current[1::2], strict=True):
            target = next(pool)
            operations.append(ReversibleGate("cx", (first, target)))
            operations.append(ReversibleGate("cx", (second, target)))
            next_level.append(target)
        current = next_level
    return tuple(operations), current[0]


def binary_to_unary_operations(t: int) -> tuple[ReversibleGate, ...]:
    """Return a clean reversible tree decoder.

    On the clean subspace it maps ``|x>|0...0>`` to
    ``|0...0>|e_x>|0...0>``. Reversing the operation list implements the
    inverse map.
    """

    layout = tree_decoder_layout(t)
    operations: list[ReversibleGate] = []

    fanouts: list[tuple[ReversibleGate, ...]] = []
    controls_by_depth: list[tuple[int, ...]] = []
    offset = 0
    for depth in range(t):
        copies = (1 << depth) - 1
        targets = layout.shared_pool[offset : offset + copies]
        offset += copies
        fanout, controls = _fanout_operations(layout.binary[depth], targets)
        fanouts.append(fanout)
        controls_by_depth.append(controls)
    for fanout in fanouts:
        operations.extend(fanout)

    operations.append(ReversibleGate("x", (layout.internal_by_depth[0][0],)))
    for depth in range(t):
        parents = layout.internal_by_depth[depth]
        children = (
            layout.internal_by_depth[depth + 1]
            if depth < t - 1
            else layout.unary
        )
        for position, parent in enumerate(parents):
            left = children[2 * position]
            right = children[2 * position + 1]
            address_control = controls_by_depth[depth][position]
            operations.append(ReversibleGate("cx", (parent, left)))
            operations.append(
                ReversibleGate("ccx", (parent, address_control, right))
            )
            operations.append(ReversibleGate("cx", (right, left)))

    for fanout in reversed(fanouts):
        operations.extend(reversed(fanout))

    reductions: list[tuple[ReversibleGate, ...]] = []
    roots: list[int] = []
    offset = 0
    for depth in range(t):
        ancilla_count = (1 << depth) - 1
        ancillas = layout.shared_pool[offset : offset + ancilla_count]
        offset += ancilla_count
        children = (
            layout.internal_by_depth[depth + 1]
            if depth < t - 1
            else layout.unary
        )
        right_children = tuple(
            children[2 * position + 1] for position in range(1 << depth)
        )
        reduction, root = _parity_tree_operations(right_children, ancillas)
        reductions.append(reduction)
        roots.append(root)
    for reduction in reductions:
        operations.extend(reduction)
    for depth, root in enumerate(roots):
        operations.append(ReversibleGate("cx", (root, layout.binary[depth])))
    for reduction in reversed(reductions):
        operations.extend(reversed(reduction))

    for depth in range(t):
        parents = layout.internal_by_depth[depth]
        children = (
            layout.internal_by_depth[depth + 1]
            if depth < t - 1
            else layout.unary
        )
        for position, parent in enumerate(parents):
            operations.append(
                ReversibleGate("cx", (children[2 * position], parent))
            )
            operations.append(
                ReversibleGate("cx", (children[2 * position + 1], parent))
            )
    return tuple(operations)


def apply_reversible_operations(
    bits: object,
    operations: tuple[ReversibleGate, ...],
    *,
    inverse: bool = False,
) -> tuple[int, ...]:
    """Apply the classical action of the reversible gate list to one basis state."""

    values = [int(value) for value in bits]  # type: ignore[arg-type]
    if any(value not in (0, 1) for value in values):
        raise ValueError("bits must contain only 0 and 1.")
    sequence = reversed(operations) if inverse else operations
    for gate in sequence:
        if gate.kind == "x":
            (target,) = gate.qubits
            values[target] ^= 1
        elif gate.kind == "cx":
            control, target = gate.qubits
            values[target] ^= values[control]
        elif gate.kind == "ccx":
            first, second, target = gate.qubits
            values[target] ^= values[first] & values[second]
        else:  # pragma: no cover
            raise ValueError(f"Unsupported gate kind: {gate.kind}")
    return tuple(values)


def clean_binary_input(t: int, label: int) -> tuple[int, ...]:
    layout = tree_decoder_layout(t)
    if not 0 <= label < layout.branches:
        raise ValueError("label is outside the t-bit binary register.")
    bits = [0] * layout.total_qubits
    for position, qubit in enumerate(layout.binary):
        bits[qubit] = (label >> (t - position - 1)) & 1
    return tuple(bits)


def expected_clean_unary_output(t: int, label: int) -> tuple[int, ...]:
    layout = tree_decoder_layout(t)
    if not 0 <= label < layout.branches:
        raise ValueError("label is outside the unary register.")
    bits = [0] * layout.total_qubits
    bits[layout.unary[label]] = 1
    return tuple(bits)


def tree_decoder_resource_row(t: int) -> TreeDecoderResourceRow:
    _validate_t(t)
    branches = 1 << t
    shared = branches - 1 - t
    workspace = branches + (branches - 1) + shared
    forward_depth = 11 * t - 4
    forward_gates = 11 * branches - 10 - 5 * t
    return TreeDecoderResourceRow(
        t=t,
        branches=branches,
        unary_register_qubits=branches,
        internal_indicator_qubits=branches - 1,
        shared_copy_reduction_qubits=shared,
        clean_workspace_qubits=workspace,
        forward_depth_proxy=forward_depth,
        round_trip_depth_proxy=2 * forward_depth,
        forward_gate_proxy=forward_gates,
        round_trip_gate_proxy=2 * forward_gates,
        toffoli_gates_forward=branches - 1,
    )


def unary_layer_pairs(t: int, depth: int) -> tuple[tuple[int, int], ...]:
    """Return disjoint one-hot mode pairs for one Hopf tree depth."""

    _validate_t(t)
    if not 0 <= depth < t:
        raise ValueError("depth must lie in 0, ..., t-1.")
    suffix_width = t - depth - 1
    return tuple(
        (
            position << (t - depth),
            (position << (t - depth)) | (1 << suffix_width),
        )
        for position in range(1 << depth)
    )


def unary_hopf_code_action(t: int, theta_prefix: object) -> np.ndarray:
    """Return the Hopf Givens network on the one-hot code space."""

    _validate_t(t)
    values = np.asarray(theta_prefix, dtype=float).reshape(-1)
    branches = 1 << t
    if values.size != branches - 1:
        raise ValueError("theta_prefix must have length 2**t - 1.")
    unitary = np.eye(branches, dtype=complex)
    offset = 0
    for depth in range(t):
        layer = np.eye(branches, dtype=complex)
        pairs = unary_layer_pairs(t, depth)
        for position, (first, second) in enumerate(pairs):
            layer[np.ix_([first, second], [first, second])] = hopf_ry(
                float(values[offset + position])
            )
        unitary = layer @ unitary
        offset += 1 << depth
    return unitary


def conditioned_prefix_resource_row(n: int, t: int) -> ConditionedPrefixResourceRow:
    """Return the self-contained tree-decoder prefix ledger."""

    if n < 1 or not 1 <= t <= n:
        raise ValueError("Require n>=1 and 1<=t<=n.")
    decoder = tree_decoder_resource_row(t)
    suffix = n - t
    branches = 1 << t
    available_after_encoding = (branches - 1) + (branches - 1 - t)
    needed_live_controls = 0 if suffix == 0 else max(1, branches // 2)
    if needed_live_controls > available_after_encoding:
        raise AssertionError("Decoder workspace cannot hold the live prefix controls.")

    predicate_depth = 0 if suffix == 0 else 2 * suffix
    predicate_gates = 0 if suffix == 0 else 2 * suffix
    fanout_depth = 0 if suffix == 0 else 2 * max(0, t - 1)
    fanout_gates = 0 if suffix == 0 else 2 * max(0, branches // 2 - 1)
    givens_depth = t
    givens_gates = branches - 1
    total_depth = (
        decoder.round_trip_depth_proxy
        + predicate_depth
        + fanout_depth
        + givens_depth
    )
    total_gates = (
        decoder.round_trip_gate_proxy
        + predicate_gates
        + fanout_gates
        + givens_gates
    )
    return ConditionedPrefixResourceRow(
        n=n,
        prefix_qubits=t,
        suffix_qubits=suffix,
        branches=branches,
        clean_workspace_qubits=decoder.clean_workspace_qubits,
        decoder_round_trip_depth_proxy=decoder.round_trip_depth_proxy,
        suffix_predicate_depth_proxy=predicate_depth,
        control_fanout_depth_proxy=fanout_depth,
        givens_layer_depth_proxy=givens_depth,
        total_depth_proxy=total_depth,
        decoder_round_trip_gate_proxy=decoder.round_trip_gate_proxy,
        suffix_predicate_gate_proxy=predicate_gates,
        control_fanout_gate_proxy=fanout_gates,
        givens_gate_proxy=givens_gates,
        total_gate_proxy=total_gates,
    )
