"""Explicit coherent routing for the large-workspace Hopf-frame compiler.

The router moves the logical suffix, together with a one-hot activation token,
into the branch selected by the logical prefix.  It is an exact reversible
permutation on the full register.  Prefix bits are copied by disjoint CNOT
fanout trees, each copied control drives one Fredkin gate, and every copy is
uncomputed before branch operations begin.

This module also supplies a sparse-state simulator for the complete
route--controlled-subframes--unroute construction.  The simulator includes the
per-branch suffix-predicate flags used by the direct controlled-subframe
schedule and verifies their exact cleanup.  It is intended for small exact
operator checks; the asymptotic UCG and multi-controlled-X decompositions remain
imported from Yuan--Zhang.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Literal, Mapping

import numpy as np

from .frames import hopf_ry
from .tree_structure import (
    conditioned_prefix_frame,
    subtree_angles,
    tail_block_diagonal_frame,
)


RouterGateKind = Literal["x", "cx", "cswap"]
SparseState = dict[int, complex]


@dataclass(frozen=True)
class RouterGate:
    """One reversible gate in the explicit router schedule."""

    kind: RouterGateKind
    qubits: tuple[int, ...]


RouterLayer = tuple[RouterGate, ...]


@dataclass(frozen=True)
class RouterLayout:
    """Physical-wire layout for one coherent tree router.

    System bit positions follow the ordinary integer convention: bit zero is
    the least-significant suffix bit.  Prefix bits are therefore listed from
    least to most significant so routing level ``j`` adds branch-index bit
    ``2**j``.

    The branch-flag wires alias the beginning of ``copy_pool``.  Prefix copies
    are uncomputed before the controlled subtree frames, so the same clean wires
    may be reused as one flag per branch and then cleared before inverse routing.
    """

    n: int
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    system: tuple[int, ...]
    prefix_lsb_to_msb: tuple[int, ...]
    branch_data: tuple[tuple[int, ...], ...]
    tokens: tuple[int, ...]
    copy_groups: tuple[tuple[int, ...], ...]
    copy_pool: tuple[int, ...]
    branch_flags: tuple[int, ...]
    total_qubits: int

    @property
    def block_width(self) -> int:
        return self.suffix_qubits + 1

    @property
    def workspace_qubits(self) -> int:
        return self.total_qubits - self.n

    @property
    def ancillas(self) -> tuple[int, ...]:
        return tuple(range(self.n, self.total_qubits))


@dataclass(frozen=True)
class RouterScheduleRow:
    """Counts read directly from the explicit router schedule."""

    n: int
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    block_width: int
    branch_data_ancillas: int
    token_ancillas: int
    control_copy_ancillas: int
    reusable_branch_flags: int
    workspace_qubits: int
    fanout_depth: int
    routing_levels: int
    forward_fredkin_gates: int
    round_trip_copy_cnots: int
    round_trip_fredkin_gates: int
    token_x_gates: int
    round_trip_depth: int
    round_trip_size: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


@dataclass(frozen=True)
class RoutedBasisSnapshot:
    """Decoded logical content after forward routing of one clean basis input."""

    prefix: int
    suffix: int
    active_branch: int
    active_token_count: int
    inactive_data_nonzero: bool
    copies_clean: bool


def _validate_cut(n: int, t: int) -> None:
    if n < 2 or not 1 <= t < n:
        raise ValueError("A routed cut requires n>=2 and 1<=t<n.")


def _ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive.")
    return (value - 1).bit_length()


def router_layout(n: int, t: int) -> RouterLayout:
    """Allocate the exact live registers used by the routed tail."""

    _validate_cut(n, t)
    suffix = n - t
    branches = 1 << t
    cursor = n

    branch_data: list[tuple[int, ...]] = [tuple(range(suffix))]
    for _branch in range(1, branches):
        branch_data.append(tuple(range(cursor, cursor + suffix)))
        cursor += suffix

    tokens = tuple(range(cursor, cursor + branches))
    cursor += branches

    copy_groups: list[tuple[int, ...]] = []
    for level in range(t):
        # One original prefix wire is available, so only k-1 copies are clean
        # workspace when k=2**level*(suffix+1) Fredkins run in parallel.
        copies = (1 << level) * (suffix + 1) - 1
        copy_groups.append(tuple(range(cursor, cursor + copies)))
        cursor += copies

    copy_pool = tuple(qubit for group in copy_groups for qubit in group)
    branch_flags = copy_pool[:branches] if suffix > 1 else ()
    if len(branch_flags) < (branches if suffix > 1 else 0):
        raise AssertionError("The cleared copy pool cannot hold branch flags.")

    return RouterLayout(
        n=n,
        prefix_qubits=t,
        suffix_qubits=suffix,
        branches=branches,
        system=tuple(range(n)),
        prefix_lsb_to_msb=tuple(suffix + level for level in range(t)),
        branch_data=tuple(branch_data),
        tokens=tokens,
        copy_groups=tuple(copy_groups),
        copy_pool=copy_pool,
        branch_flags=branch_flags,
        total_qubits=cursor,
    )


def _fanout_layers(
    source: int, targets: tuple[int, ...]
) -> tuple[tuple[RouterLayer, ...], tuple[int, ...]]:
    """Copy one coherent bit with a balanced disjoint CNOT tree."""

    active = [source]
    remaining = list(targets)
    layers: list[RouterLayer] = []
    while remaining:
        gates: list[RouterGate] = []
        new_controls: list[int] = []
        for control in tuple(active):
            if not remaining:
                break
            target = remaining.pop(0)
            gates.append(RouterGate("cx", (control, target)))
            new_controls.append(target)
        layers.append(tuple(gates))
        active.extend(new_controls)
    return tuple(layers), tuple(active)


def _merge_parallel_schedules(
    schedules: tuple[tuple[RouterLayer, ...], ...]
) -> tuple[RouterLayer, ...]:
    depth = max((len(schedule) for schedule in schedules), default=0)
    merged: list[RouterLayer] = []
    for layer_index in range(depth):
        gates: list[RouterGate] = []
        for schedule in schedules:
            if layer_index < len(schedule):
                gates.extend(schedule[layer_index])
        merged.append(tuple(gates))
    return tuple(merged)


def router_layer_is_disjoint(layer: RouterLayer) -> bool:
    """Return whether no two gates in one declared layer share a wire."""

    used: set[int] = set()
    for gate in layer:
        for qubit in gate.qubits:
            if qubit in used:
                return False
            used.add(qubit)
    return True


def router_fanout_layers(layout: RouterLayout) -> tuple[RouterLayer, ...]:
    """Return all prefix-copy trees merged at equal logical times."""

    schedules: list[tuple[RouterLayer, ...]] = []
    for level, targets in enumerate(layout.copy_groups):
        fanout, controls = _fanout_layers(
            layout.prefix_lsb_to_msb[level], targets
        )
        expected = (1 << level) * layout.block_width
        if len(controls) != expected:
            raise AssertionError("Prefix fanout produced the wrong control count.")
        schedules.append(fanout)
    merged = _merge_parallel_schedules(tuple(schedules))
    if not all(router_layer_is_disjoint(layer) for layer in merged):
        raise AssertionError("A prefix-fanout layer is not disjoint.")
    return merged


def router_swap_layers(layout: RouterLayout) -> tuple[RouterLayer, ...]:
    """Return the least-significant-prefix-bit-first Fredkin tree."""

    layers: list[RouterLayer] = []
    for level in range(layout.prefix_qubits):
        controls = (
            layout.prefix_lsb_to_msb[level],
            *layout.copy_groups[level],
        )
        offset = 1 << level
        gates: list[RouterGate] = []
        control_index = 0
        for lower_branch in range(offset):
            upper_branch = lower_branch + offset
            lower_block = (
                *layout.branch_data[lower_branch],
                layout.tokens[lower_branch],
            )
            upper_block = (
                *layout.branch_data[upper_branch],
                layout.tokens[upper_branch],
            )
            for first, second in zip(lower_block, upper_block, strict=True):
                gates.append(
                    RouterGate(
                        "cswap",
                        (controls[control_index], first, second),
                    )
                )
                control_index += 1
        if control_index != len(controls):
            raise AssertionError("A routing level did not consume every copy.")
        layer = tuple(gates)
        if not router_layer_is_disjoint(layer):
            raise AssertionError("A Fredkin routing layer is not disjoint.")
        layers.append(layer)
    return tuple(layers)


def router_schedule_row(n: int, t: int) -> RouterScheduleRow:
    """Derive router counts from the explicit allocated layout and layers."""

    layout = router_layout(n, t)
    fanout = router_fanout_layers(layout)
    swaps = router_swap_layers(layout)
    copy_count = sum(len(layer) for layer in fanout)
    fredkin_count = sum(len(layer) for layer in swaps)
    if copy_count != len(layout.copy_pool):
        raise AssertionError("Fanout gate count and allocated copies disagree.")

    forward_depth = 1 + 2 * len(fanout) + len(swaps)
    return RouterScheduleRow(
        n=n,
        prefix_qubits=t,
        suffix_qubits=layout.suffix_qubits,
        branches=layout.branches,
        block_width=layout.block_width,
        branch_data_ancillas=(layout.branches - 1) * layout.suffix_qubits,
        token_ancillas=layout.branches,
        control_copy_ancillas=len(layout.copy_pool),
        reusable_branch_flags=len(layout.branch_flags),
        workspace_qubits=layout.workspace_qubits,
        fanout_depth=len(fanout),
        routing_levels=len(swaps),
        forward_fredkin_gates=fredkin_count,
        round_trip_copy_cnots=4 * copy_count,
        round_trip_fredkin_gates=2 * fredkin_count,
        token_x_gates=2,
        round_trip_depth=2 * forward_depth,
        round_trip_size=4 * copy_count + 2 * fredkin_count + 2,
    )


def _clean_sparse(
    state: Mapping[int, complex], *, atol: float = 1e-14
) -> SparseState:
    return {
        int(label): complex(amplitude)
        for label, amplitude in state.items()
        if abs(amplitude) > atol
    }


def _apply_gate_to_label(label: int, gate: RouterGate) -> int:
    if gate.kind == "x":
        (target,) = gate.qubits
        return label ^ (1 << target)
    if gate.kind == "cx":
        control, target = gate.qubits
        return label ^ (((label >> control) & 1) << target)
    if gate.kind == "cswap":
        control, first, second = gate.qubits
        if (
            ((label >> control) & 1)
            and ((label >> first) & 1) != ((label >> second) & 1)
        ):
            return label ^ (1 << first) ^ (1 << second)
        return label
    raise ValueError(f"Unsupported router gate kind: {gate.kind}")


def apply_router_layer(
    state: Mapping[int, complex], layer: RouterLayer
) -> SparseState:
    """Apply one reversible layer to a sparse statevector."""

    if not router_layer_is_disjoint(layer):
        raise ValueError("Router layers must have disjoint support.")
    output: SparseState = {}
    for label, amplitude in state.items():
        routed = int(label)
        for gate in layer:
            routed = _apply_gate_to_label(routed, gate)
        output[routed] = output.get(routed, 0.0j) + complex(amplitude)
    return _clean_sparse(output)


def apply_router_layers(
    state: Mapping[int, complex],
    layers: tuple[RouterLayer, ...],
    *,
    inverse: bool = False,
) -> SparseState:
    output = _clean_sparse(state)
    sequence = reversed(layers) if inverse else layers
    for layer in sequence:
        # Every gate is self-inverse and gates in a layer are disjoint.
        output = apply_router_layer(output, layer)
    return output


def _apply_x(state: Mapping[int, complex], target: int) -> SparseState:
    return apply_router_layer(state, (RouterGate("x", (target,)),))


def workspace_leakage(
    state: Mapping[int, complex], layout: RouterLayout
) -> float:
    """Return probability mass outside the all-zero ancillary subspace."""

    leakage = 0.0
    for label, amplitude in state.items():
        if int(label) >> layout.n:
            leakage += abs(amplitude) ** 2
    return float(leakage)


def copies_are_clean(
    state: Mapping[int, complex], layout: RouterLayout
) -> bool:
    return all(
        all(((int(label) >> qubit) & 1) == 0 for qubit in layout.copy_pool)
        for label in state
    )


def branch_flags_are_clean(
    state: Mapping[int, complex], layout: RouterLayout
) -> bool:
    return all(
        all(((int(label) >> qubit) & 1) == 0 for qubit in layout.branch_flags)
        for label in state
    )


def encode_clean_system_state(
    system_state: object, layout: RouterLayout
) -> SparseState:
    """Embed an ``n``-qubit state with every router workspace wire zero."""

    values = np.asarray(system_state, dtype=complex).reshape(-1)
    if values.size != 1 << layout.n:
        raise ValueError("system_state has the wrong dimension.")
    return _clean_sparse(
        {label: amplitude for label, amplitude in enumerate(values)}
    )


def decode_clean_system_state(
    state: Mapping[int, complex], layout: RouterLayout
) -> tuple[np.ndarray, float]:
    """Return the clean-workspace system component and leakage probability."""

    system = np.zeros(1 << layout.n, dtype=complex)
    leakage = 0.0
    mask = (1 << layout.n) - 1
    for label, amplitude in state.items():
        value = int(label)
        if value >> layout.n:
            leakage += abs(amplitude) ** 2
        else:
            system[value & mask] += complex(amplitude)
    return system, float(leakage)


def apply_router_forward(
    state: Mapping[int, complex], layout: RouterLayout
) -> SparseState:
    """Initialize the root token, route, and clear all prefix copies."""

    if workspace_leakage(state, layout) > 1e-14:
        raise ValueError("Forward routing requires clean workspace input.")
    output = _apply_x(state, layout.tokens[0])
    fanout = router_fanout_layers(layout)
    output = apply_router_layers(output, fanout)
    output = apply_router_layers(output, router_swap_layers(layout))
    output = apply_router_layers(output, fanout, inverse=True)
    if not copies_are_clean(output, layout):
        raise AssertionError("Forward routing did not clear prefix copies.")
    return output


def apply_router_inverse(
    state: Mapping[int, complex], layout: RouterLayout
) -> SparseState:
    """Recompute prefix copies, unroute, clear them, and reset the root token."""

    if not copies_are_clean(state, layout):
        raise ValueError("Inverse routing requires the shared copy/flag pool clean.")
    output = _clean_sparse(state)
    fanout = router_fanout_layers(layout)
    output = apply_router_layers(output, fanout)
    output = apply_router_layers(output, router_swap_layers(layout), inverse=True)
    output = apply_router_layers(output, fanout, inverse=True)
    output = _apply_x(output, layout.tokens[0])
    return output


def _wire_value(label: int, wires_lsb_to_msb: tuple[int, ...]) -> int:
    return sum(
        ((label >> qubit) & 1) << position
        for position, qubit in enumerate(wires_lsb_to_msb)
    )


def routed_basis_snapshot(
    layout: RouterLayout, system_label: int
) -> RoutedBasisSnapshot:
    """Route one clean basis label and decode the branch/token content."""

    if not 0 <= system_label < 1 << layout.n:
        raise ValueError("system_label is outside the logical register.")
    routed = apply_router_forward({int(system_label): 1.0 + 0.0j}, layout)
    if len(routed) != 1:
        raise AssertionError("A basis input did not remain a basis state.")
    label = next(iter(routed))
    prefix = system_label >> layout.suffix_qubits
    suffix = system_label & ((1 << layout.suffix_qubits) - 1)
    active_tokens = [
        branch
        for branch, qubit in enumerate(layout.tokens)
        if (label >> qubit) & 1
    ]
    inactive_nonzero = any(
        _wire_value(label, wires) != 0
        for branch, wires in enumerate(layout.branch_data)
        if branch != prefix
    )
    return RoutedBasisSnapshot(
        prefix=prefix,
        suffix=suffix,
        active_branch=active_tokens[0] if len(active_tokens) == 1 else -1,
        active_token_count=len(active_tokens),
        inactive_data_nonzero=inactive_nonzero,
        copies_clean=copies_are_clean(routed, layout),
    )


def _toggle_zero_predicate(
    state: Mapping[int, complex],
    controls: tuple[int, ...],
    target: int,
) -> SparseState:
    """Apply an exact negative-control multi-controlled X basis action."""

    output: SparseState = {}
    for label, amplitude in state.items():
        value = int(label)
        predicate = all(((value >> qubit) & 1) == 0 for qubit in controls)
        if predicate:
            value ^= 1 << target
        output[value] = output.get(value, 0.0j) + complex(amplitude)
    return _clean_sparse(output)


def _apply_selected_ry(
    state: Mapping[int, complex],
    target: int,
    active: Callable[[int], bool],
    angle: Callable[[int], float],
) -> SparseState:
    """Apply one exact logical UCG block action to a sparse statevector."""

    values = _clean_sparse(state)
    target_mask = 1 << target
    bases = {label & ~target_mask for label in values}
    output: SparseState = {}
    for base in bases:
        zero_amplitude = values.get(base, 0.0j)
        one_label = base | target_mask
        one_amplitude = values.get(one_label, 0.0j)
        if active(base):
            rotation = hopf_ry(angle(base))
            transformed = rotation @ np.asarray(
                [zero_amplitude, one_amplitude], dtype=complex
            )
            zero_out, one_out = complex(transformed[0]), complex(transformed[1])
        else:
            zero_out, one_out = zero_amplitude, one_amplitude
        if abs(zero_out) > 1e-14:
            output[base] = output.get(base, 0.0j) + zero_out
        if abs(one_out) > 1e-14:
            output[one_label] = output.get(one_label, 0.0j) + one_out
    return _clean_sparse(output)


def apply_parallel_controlled_subframes(
    state: Mapping[int, complex],
    layout: RouterLayout,
    theta_mag: object,
) -> SparseState:
    """Apply all token-controlled subtree frames and clear branch flags.

    The branches are disjoint and may be scheduled in parallel.  The simulator
    loops over them only for convenience.  At a nonfinal local depth, one clean
    flag per branch stores the local zero-suffix predicate; those flags reuse the
    cleared prefix-copy pool.  The logical rotation is controlled jointly by
    the branch token and flag.  Final local depths need no flag.
    """

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    if theta.size != (1 << layout.n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    if not copies_are_clean(state, layout):
        raise ValueError("Controlled subframes require the shared pool clean.")

    all_branch_angles = tuple(
        subtree_angles(
            theta,
            layout.n,
            layout.prefix_qubits,
            branch,
        )
        for branch in range(layout.branches)
    )
    output = _clean_sparse(state)
    suffix = layout.suffix_qubits

    for local_depth in range(suffix):
        lower_suffix_width = suffix - local_depth - 1
        angle_start = (1 << local_depth) - 1
        angle_stop = (1 << (local_depth + 1)) - 1
        for branch in range(layout.branches):
            wires = layout.branch_data[branch]
            token = layout.tokens[branch]
            target = wires[lower_suffix_width]
            angles = all_branch_angles[branch][angle_start:angle_stop]

            if lower_suffix_width > 0:
                flag = layout.branch_flags[branch]
                lower_suffix = wires[:lower_suffix_width]
                output = _toggle_zero_predicate(output, lower_suffix, flag)

                def active(
                    base: int,
                    *,
                    token_wire: int = token,
                    flag_wire: int = flag,
                ) -> bool:
                    return bool(
                        ((base >> token_wire) & 1)
                        and ((base >> flag_wire) & 1)
                    )

            else:

                def active(
                    base: int, *, token_wire: int = token
                ) -> bool:
                    return bool((base >> token_wire) & 1)

            def selected_angle(
                base: int,
                *,
                data_wires: tuple[int, ...] = wires,
                depth: int = local_depth,
                table: np.ndarray = angles,
            ) -> float:
                branch_value = _wire_value(base, data_wires)
                prefix = branch_value >> (suffix - depth)
                return float(table[prefix])

            output = _apply_selected_ry(
                output, target, active, selected_angle
            )

            if lower_suffix_width > 0:
                output = _toggle_zero_predicate(output, lower_suffix, flag)

    if not branch_flags_are_clean(output, layout):
        raise AssertionError("A controlled subtree left a branch flag dirty.")
    return output


def apply_routed_tail(
    system_state: object,
    n: int,
    t: int,
    theta_mag: object,
) -> tuple[np.ndarray, float]:
    """Apply the explicit routed tail to an arbitrary logical system state."""

    layout = router_layout(n, t)
    routed = apply_router_forward(encode_clean_system_state(system_state, layout), layout)
    operated = apply_parallel_controlled_subframes(routed, layout, theta_mag)
    restored = apply_router_inverse(operated, layout)
    return decode_clean_system_state(restored, layout)


def routed_tail_residual(
    system_state: object,
    n: int,
    t: int,
    theta_mag: object,
) -> tuple[float, float]:
    """Compare the explicit routed tail with the ideal direct-sum tail."""

    state = np.asarray(system_state, dtype=complex).reshape(-1)
    if state.size != 1 << n:
        raise ValueError("system_state has the wrong dimension.")
    actual, leakage = apply_routed_tail(state, n, t, theta_mag)
    expected = tail_block_diagonal_frame(n, t, theta_mag) @ state
    residual = float(np.max(np.abs(actual - expected)))
    return residual, leakage


def routed_cut_frame_matrix(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Construct the complete routed cut operator for small exact tests."""

    _validate_cut(n, t)
    prefix = conditioned_prefix_frame(n, t, theta_mag)
    columns: list[np.ndarray] = []
    for label in range(1 << n):
        column, leakage = apply_routed_tail(prefix[:, label], n, t, theta_mag)
        if leakage > 1e-12:
            raise AssertionError("The routed cut leaked out of clean workspace.")
        columns.append(column)
    return np.column_stack(columns)


def routed_cut_residual(n: int, t: int, theta_mag: object) -> float:
    """Compare the explicit routed construction with the direct Hopf frame."""

    from .frames import direct_real_frame

    return float(
        np.max(
            np.abs(
                routed_cut_frame_matrix(n, t, theta_mag)
                - direct_real_frame(n, theta_mag)
            )
        )
    )
