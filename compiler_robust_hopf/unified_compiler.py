"""Unified Hopf-frame compiler based on the Yuan--Zhang circuit framework.

The active construction uses a self-contained reversible tree decoder for the
conditioned prefix, the exact Hopf tail direct sum, coherent branch routing,
Yuan--Zhang UCG and multi-controlled-X primitives, and one UCG for the complex
phase diagonal.

Resource values below are transparent term proxies, not finite elementary-gate
counts. The asymptotic theorem is proved in the companion documentation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np

from .frames import direct_real_frame
from .tree_decoder import conditioned_prefix_resource_row
from .tree_structure import conditioned_prefix_frame, tail_block_diagonal_frame


@dataclass(frozen=True)
class DirectFrameResourceRow:
    n: int
    dimension: int
    ancillas: int
    controlled: bool
    mode: str
    workspace_used_upper_bound: int
    predicate_depth_proxy: int
    ucg_depth_proxy: int
    total_depth_proxy: int
    predicate_size_proxy: int
    ucg_size_proxy: int
    total_size_proxy: int

    def as_dict(self) -> dict[str, int | bool | str]:
        return asdict(self)


@dataclass(frozen=True)
class RouteWorkspaceRow:
    n: int
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    branch_data_ancillas: int
    token_ancillas: int
    control_copy_ancillas: int
    branch_flag_ancillas: int
    tail_peak_ancillas: int
    prefix_peak_ancillas: int
    exact_complete_peak_ancillas: int
    simple_workspace_envelope: int
    maximum_fanout_depth: int
    forward_fredkin_gates: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


@dataclass(frozen=True)
class UnifiedFrameResourceRow:
    n: int
    dimension: int
    ancillas: int
    mode: str
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    workspace_used_upper_bound: int
    prefix_depth_proxy: int
    routing_depth_proxy: int
    controlled_subframe_depth_proxy: int
    total_depth_proxy: int
    prefix_size_proxy: int
    routing_size_proxy: int
    controlled_subframes_size_proxy: int
    total_size_proxy: int
    optimal_qsp_depth_proxy: int

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


@dataclass(frozen=True)
class DiagonalUCGResourceRow:
    n: int
    dimension: int
    ancillas: int
    controls: int
    one_qubit_blocks: int
    workspace_used_upper_bound: int
    depth_proxy: int
    size_proxy: int
    block_table_generation_proxy: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


@dataclass(frozen=True)
class UnifiedComplexResourceRow:
    n: int
    dimension: int
    ancillas: int
    real_mode: str
    workspace_used_upper_bound: int
    real_depth_proxy: int
    diagonal_depth_proxy: int
    total_depth_proxy: int
    real_size_proxy: int
    diagonal_size_proxy: int
    total_size_proxy: int
    optimal_qsp_depth_proxy: int

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _ceil_div(numerator: int, denominator: int) -> int:
    if numerator < 0 or denominator < 1:
        raise ValueError("Require numerator>=0 and denominator>=1.")
    return (numerator + denominator - 1) // denominator


def _ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive.")
    return (value - 1).bit_length()


def ucg_depth_proxy(total_qubits: int, work_ancillas: int) -> int:
    """Return ``k + ceil(2**k/(k+m))`` from Yuan--Zhang Lemma 6."""

    if total_qubits < 1 or work_ancillas < 0:
        raise ValueError("Require total_qubits>=1 and work_ancillas>=0.")
    return total_qubits + _ceil_div(
        1 << total_qubits, total_qubits + work_ancillas
    )


def ucg_size_proxy(total_qubits: int) -> int:
    if total_qubits < 1:
        raise ValueError("total_qubits must be positive.")
    return 1 << total_qubits


def direct_frame_resource_row(
    n: int, ancillas: int, *, controlled: bool = False
) -> DirectFrameResourceRow:
    """Return the direct addressed compiler using only Yuan--Zhang primitives."""

    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    dimension = 1 << n
    external = 1 if controlled else 0
    predicate_depth = 0
    predicate_size = 0
    ucg_depth = 0
    ucg_size = 0

    if ancillas == 0:
        width = n + external
        for _depth in range(n):
            ucg_depth += ucg_depth_proxy(width, 0)
            ucg_size += ucg_size_proxy(width)
        return DirectFrameResourceRow(
            n=n,
            dimension=dimension,
            ancillas=0,
            controlled=controlled,
            mode="strict-zero-full-width-ucg",
            workspace_used_upper_bound=0,
            predicate_depth_proxy=0,
            ucg_depth_proxy=ucg_depth,
            total_depth_proxy=ucg_depth,
            predicate_size_proxy=0,
            ucg_size_proxy=ucg_size,
            total_size_proxy=ucg_size,
        )

    for depth in range(n):
        final = depth == n - 1
        if not final:
            suffix_width = n - depth - 1
            predicate_depth += 2 * suffix_width
            predicate_size += 2 * suffix_width
            width = depth + 2 + external
            work = ancillas - 1
        else:
            width = n + external
            work = ancillas
        ucg_depth += ucg_depth_proxy(width, work)
        ucg_size += ucg_size_proxy(width)

    return DirectFrameResourceRow(
        n=n,
        dimension=dimension,
        ancillas=ancillas,
        controlled=controlled,
        mode="direct-flagged-ucg",
        workspace_used_upper_bound=ancillas,
        predicate_depth_proxy=predicate_depth,
        ucg_depth_proxy=ucg_depth,
        total_depth_proxy=predicate_depth + ucg_depth,
        predicate_size_proxy=predicate_size,
        ucg_size_proxy=ucg_size,
        total_size_proxy=predicate_size + ucg_size,
    )


def exact_control_copy_count(n: int, t: int) -> int:
    if n < 2 or not 1 <= t < n:
        raise ValueError("A routed cut requires n>=2 and 1<=t<n.")
    branches = 1 << t
    suffix_qubits = n - t
    return (branches - 1) * (suffix_qubits + 1) - t


def route_workspace_row(n: int, t: int) -> RouteWorkspaceRow:
    if n < 2 or not 1 <= t < n:
        raise ValueError("A routed cut requires n>=2 and 1<=t<n.")
    branches = 1 << t
    suffix = n - t
    data = (branches - 1) * suffix
    tokens = branches
    copies = exact_control_copy_count(n, t)
    flags = branches if suffix > 1 else 0
    tail_peak = data + tokens + max(copies, flags)
    prefix_peak = conditioned_prefix_resource_row(n, t).clean_workspace_qubits
    exact_peak = max(tail_peak, prefix_peak)
    envelope = 2 * branches * (suffix + 1)
    if exact_peak > envelope:
        raise AssertionError("The routed construction exceeded its simple envelope.")
    max_fanout = (t - 1) + _ceil_log2(suffix + 1)
    fredkins = (branches - 1) * (suffix + 1)
    return RouteWorkspaceRow(
        n=n,
        prefix_qubits=t,
        suffix_qubits=suffix,
        branches=branches,
        branch_data_ancillas=data,
        token_ancillas=tokens,
        control_copy_ancillas=copies,
        branch_flag_ancillas=flags,
        tail_peak_ancillas=tail_peak,
        prefix_peak_ancillas=prefix_peak,
        exact_complete_peak_ancillas=exact_peak,
        simple_workspace_envelope=envelope,
        maximum_fanout_depth=max_fanout,
        forward_fredkin_gates=fredkins,
    )


def choose_routed_cut(n: int, ancillas: int) -> int | None:
    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    if n == 1:
        return None
    choices = [
        t
        for t in range(1, n)
        if route_workspace_row(n, t).simple_workspace_envelope <= ancillas
    ]
    return max(choices) if choices else None


def routing_depth_proxy(n: int, t: int) -> int:
    row = route_workspace_row(n, t)
    return 4 * row.maximum_fanout_depth + 2 * t + 2


def routing_size_proxy(n: int, t: int) -> int:
    row = route_workspace_row(n, t)
    return (
        4 * row.control_copy_ancillas
        + 2 * row.forward_fredkin_gates
        + 2
    )


def optimal_qsp_depth_proxy(n: int, ancillas: int) -> int:
    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    return n + _ceil_div(1 << n, n + ancillas)


def unified_real_frame_resource_row(
    n: int, ancillas: int
) -> UnifiedFrameResourceRow:
    """Select the sole active Hopf-frame compiler."""

    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    dimension = 1 << n
    cut = choose_routed_cut(n, ancillas)
    if cut is None:
        base = direct_frame_resource_row(n, ancillas)
        return UnifiedFrameResourceRow(
            n=n,
            dimension=dimension,
            ancillas=ancillas,
            mode=base.mode,
            prefix_qubits=0,
            suffix_qubits=n,
            branches=1,
            workspace_used_upper_bound=base.workspace_used_upper_bound,
            prefix_depth_proxy=0,
            routing_depth_proxy=0,
            controlled_subframe_depth_proxy=base.total_depth_proxy,
            total_depth_proxy=base.total_depth_proxy,
            prefix_size_proxy=0,
            routing_size_proxy=0,
            controlled_subframes_size_proxy=base.total_size_proxy,
            total_size_proxy=base.total_size_proxy,
            optimal_qsp_depth_proxy=optimal_qsp_depth_proxy(n, ancillas),
        )

    route = route_workspace_row(n, cut)
    prefix = conditioned_prefix_resource_row(n, cut)
    suffix = n - cut
    branch_workspace = 0 if suffix == 1 else 1
    branch = direct_frame_resource_row(
        suffix, branch_workspace, controlled=True
    )
    route_depth = routing_depth_proxy(n, cut)
    route_size = routing_size_proxy(n, cut)
    branches_size = route.branches * branch.total_size_proxy
    total_depth = prefix.total_depth_proxy + route_depth + branch.total_depth_proxy
    total_size = prefix.total_gate_proxy + route_size + branches_size
    return UnifiedFrameResourceRow(
        n=n,
        dimension=dimension,
        ancillas=ancillas,
        mode="tree-decoder-routed-subframes",
        prefix_qubits=cut,
        suffix_qubits=suffix,
        branches=route.branches,
        workspace_used_upper_bound=route.exact_complete_peak_ancillas,
        prefix_depth_proxy=prefix.total_depth_proxy,
        routing_depth_proxy=route_depth,
        controlled_subframe_depth_proxy=branch.total_depth_proxy,
        total_depth_proxy=total_depth,
        prefix_size_proxy=prefix.total_gate_proxy,
        routing_size_proxy=route_size,
        controlled_subframes_size_proxy=branches_size,
        total_size_proxy=total_size,
        optimal_qsp_depth_proxy=optimal_qsp_depth_proxy(n, ancillas),
    )


def unified_real_frame_resource_rows(
    n: int, ancillas: Iterable[int]
) -> tuple[UnifiedFrameResourceRow, ...]:
    return tuple(unified_real_frame_resource_row(n, int(m)) for m in ancillas)


def diagonal_ucg_blocks(
    theta_ph: object, *, inverse: bool = False
) -> tuple[np.ndarray, ...]:
    """Return the one-qubit blocks of the exact leaf-phase UCG."""

    phases = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phases.size < 2 or phases.size & (phases.size - 1):
        raise ValueError("theta_ph must have power-of-two length at least two.")
    sign = -1.0 if inverse else 1.0
    blocks: list[np.ndarray] = []
    for control_label in range(phases.size // 2):
        first = np.exp(1j * sign * phases[2 * control_label])
        second = np.exp(1j * sign * phases[2 * control_label + 1])
        blocks.append(np.diag([first, second]).astype(complex))
    return tuple(blocks)


def diagonal_from_ucg_blocks(blocks: object) -> np.ndarray:
    values = tuple(np.asarray(block, dtype=complex) for block in blocks)  # type: ignore[arg-type]
    if not values or any(block.shape != (2, 2) for block in values):
        raise ValueError("blocks must be a nonempty sequence of 2-by-2 matrices.")
    count = len(values)
    if count & (count - 1):
        raise ValueError("The number of UCG blocks must be a power of two.")
    unitary = np.zeros((2 * count, 2 * count), dtype=complex)
    for label, block in enumerate(values):
        start = 2 * label
        unitary[start : start + 2, start : start + 2] = block
    return unitary


def diagonal_ucg_matrix(theta_ph: object, *, inverse: bool = False) -> np.ndarray:
    return diagonal_from_ucg_blocks(diagonal_ucg_blocks(theta_ph, inverse=inverse))


def diagonal_ucg_resource_row(n: int, ancillas: int) -> DiagonalUCGResourceRow:
    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    dimension = 1 << n
    return DiagonalUCGResourceRow(
        n=n,
        dimension=dimension,
        ancillas=ancillas,
        controls=n - 1,
        one_qubit_blocks=dimension // 2,
        workspace_used_upper_bound=ancillas,
        depth_proxy=ucg_depth_proxy(n, ancillas),
        size_proxy=ucg_size_proxy(n),
        block_table_generation_proxy=dimension,
    )


def unified_complex_frame_resource_row(
    n: int, ancillas: int
) -> UnifiedComplexResourceRow:
    real = unified_real_frame_resource_row(n, ancillas)
    diagonal = diagonal_ucg_resource_row(n, ancillas)
    return UnifiedComplexResourceRow(
        n=n,
        dimension=1 << n,
        ancillas=ancillas,
        real_mode=real.mode,
        workspace_used_upper_bound=max(
            real.workspace_used_upper_bound,
            diagonal.workspace_used_upper_bound,
        ),
        real_depth_proxy=real.total_depth_proxy,
        diagonal_depth_proxy=diagonal.depth_proxy,
        total_depth_proxy=real.total_depth_proxy + diagonal.depth_proxy,
        real_size_proxy=real.total_size_proxy,
        diagonal_size_proxy=diagonal.size_proxy,
        total_size_proxy=real.total_size_proxy + diagonal.size_proxy,
        optimal_qsp_depth_proxy=real.optimal_qsp_depth_proxy,
    )


def controlled_unitary(unitary: object) -> np.ndarray:
    """Return ``|0><0| tensor I + |1><1| tensor U``."""

    value = np.asarray(unitary, dtype=complex)
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise ValueError("unitary must be square.")
    identity = np.eye(value.shape[0], dtype=complex)
    out = np.zeros((2 * value.shape[0], 2 * value.shape[0]), dtype=complex)
    out[: value.shape[0], : value.shape[0]] = identity
    out[value.shape[0] :, value.shape[0] :] = value
    return out


def unified_cut_frame_matrix(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return the exact logical operator of the routed cut construction."""

    return tail_block_diagonal_frame(n, t, theta_mag) @ conditioned_prefix_frame(
        n, t, theta_mag
    )


def unified_cut_residual(n: int, t: int, theta_mag: object) -> float:
    return float(
        np.max(
            np.abs(
                unified_cut_frame_matrix(n, t, theta_mag)
                - direct_real_frame(n, theta_mag)
            )
        )
    )
