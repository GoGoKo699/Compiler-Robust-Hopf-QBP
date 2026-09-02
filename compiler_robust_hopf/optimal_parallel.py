"""Tree-cut parallelization for the optimal all-ancilla Hopf-frame problem.

This module supports the first optimality checkpoint. It separates exact
operator identities and reversible-routing checks from asymptotic resource
bookkeeping.

The central exact identity is

    tail_t(W_n) = direct_sum_r W_{n-t}^{(r)},

where each block contains the Hopf angles in one depth-``t`` subtree.  A
coherent binary-tree router can move the suffix register into one of ``2**t``
disjoint branch registers, apply all controlled subtree frames in parallel, and
route the result back.

The resulting optimal-depth theorem is still labelled a proof candidate until a
second independent register and asymptotic audit is complete.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable

import numpy as np

from .ancilla_depth import (
    ancilla_depth_row,
    tail_frame,
    unary_prefix_depth_proxy,
    unary_prefix_size_proxy,
)
from .frames import direct_real_frame


@dataclass(frozen=True)
class RouteWorkspaceLedger:
    """Conservative clean-workspace ledger for one routed tree cut."""

    n: int
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    branch_data_ancillas: int
    token_ancillas: int
    control_copy_ancillas: int
    branch_flag_ancillas: int
    tail_peak_ancillas: int
    prefix_compiler_ancillas: int
    exact_peak_upper_bound: int
    simple_envelope: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


@dataclass(frozen=True)
class OptimalityPlanRow:
    """One transparent planner row for the candidate optimal construction."""

    n: int
    dimension: int
    requested_ancillas: int
    used_ancillas_upper_bound: int
    mode: str
    prefix_qubits: int
    suffix_qubits: int
    branches: int
    prefix_depth_proxy: int
    routing_depth_proxy: int
    controlled_branch_depth_proxy: int
    total_depth_proxy: int
    prefix_size_proxy: int
    routing_size_proxy: int
    controlled_branches_size_proxy: int
    total_size_proxy: int
    optimal_qsp_depth_proxy: int

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _validate_cut(n: int, t: int, *, allow_endpoints: bool = True) -> None:
    _validate_n(n)
    lower = 0 if allow_endpoints else 1
    upper = n if allow_endpoints else n - 1
    if not lower <= t <= upper:
        if allow_endpoints:
            raise ValueError("t must lie in 0, ..., n.")
        raise ValueError("A routed cut requires 1 <= t < n.")


def subtree_angle_indices(n: int, t: int, prefix: int) -> tuple[int, ...]:
    """Return zero-based angle indices for one depth-``t`` subtree.

    The returned order is the local breadth-first order of an ``n-t``-qubit
    Hopf frame.
    """

    _validate_cut(n, t)
    branches = 1 << t
    if not 0 <= prefix < branches:
        raise ValueError("prefix is outside the selected tree cut.")
    suffix_qubits = n - t
    indices: list[int] = []
    for local_depth in range(suffix_qubits):
        for local_position in range(1 << local_depth):
            global_node = (
                (1 << (t + local_depth))
                + (prefix << local_depth)
                + local_position
            )
            indices.append(global_node - 1)
    return tuple(indices)


def subtree_angles(
    theta_mag: object, n: int, t: int, prefix: int
) -> np.ndarray:
    """Extract one local subtree's angles in local breadth-first order."""

    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    return values[list(subtree_angle_indices(n, t, prefix))].copy()


def tail_block_diagonal_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Build the exact direct-sum form of the addressed tail ``R_t``."""

    _validate_cut(n, t)
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    suffix_qubits = n - t
    block_dimension = 1 << suffix_qubits
    dimension = 1 << n
    out = np.zeros((dimension, dimension), dtype=complex)
    if suffix_qubits == 0:
        return np.eye(dimension, dtype=complex)
    for prefix in range(1 << t):
        block = direct_real_frame(
            suffix_qubits, subtree_angles(values, n, t, prefix)
        )
        start = prefix * block_dimension
        stop = start + block_dimension
        out[start:stop, start:stop] = block
    return out


def tail_block_residual(n: int, t: int, theta_mag: object) -> float:
    """Return the maximum residual in the tree-cut direct-sum identity."""

    residual = tail_frame(n, t, theta_mag) - tail_block_diagonal_frame(
        n, t, theta_mag
    )
    return float(np.max(np.abs(residual)))


def route_workspace_ledger(n: int, t: int) -> RouteWorkspaceLedger:
    """Return the clean register ledger for a routed nontrivial tree cut.

    Registers are scheduled as follows.

    * ``(B-1)s`` qubits complete ``B`` suffix-data registers, one of which is
      the original system suffix.
    * ``B`` token qubits carry a coherently routed one-hot activation token.
    * at most ``(B-1)(s+1)`` temporary copies parallelize all Fredkin controls;
      after routing they are uncomputed and reused as branch predicate flags.
    * the conditioned-prefix compiler is sequential and reuses the same pool.

    The exact peak below is bounded by the simple envelope ``2B(s+1)``.
    """

    _validate_cut(n, t, allow_endpoints=False)
    branches = 1 << t
    suffix_qubits = n - t
    data = (branches - 1) * suffix_qubits
    tokens = branches
    copies = (branches - 1) * (suffix_qubits + 1)
    flags = branches if suffix_qubits > 1 else 0
    tail_peak = data + tokens + max(copies, flags)
    prefix_workspace = 3 * branches - t
    exact_peak = max(tail_peak, prefix_workspace)
    envelope = 2 * branches * (suffix_qubits + 1)
    if exact_peak > envelope:  # defensive assertion for future edits
        raise AssertionError("The simple routing workspace envelope was violated.")
    return RouteWorkspaceLedger(
        n=n,
        prefix_qubits=t,
        suffix_qubits=suffix_qubits,
        branches=branches,
        branch_data_ancillas=data,
        token_ancillas=tokens,
        control_copy_ancillas=copies,
        branch_flag_ancillas=flags,
        tail_peak_ancillas=tail_peak,
        prefix_compiler_ancillas=prefix_workspace,
        exact_peak_upper_bound=exact_peak,
        simple_envelope=envelope,
    )


def choose_routed_cut(n: int, ancillas: int) -> int | None:
    """Choose the largest cut satisfying ``2*2**t*(n-t+1) <= ancillas``."""

    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    choices = [
        t
        for t in range(1, n)
        if route_workspace_ledger(n, t).simple_envelope <= ancillas
    ]
    return max(choices) if choices else None


def _ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive.")
    return (value - 1).bit_length()


def controlled_branch_depth_proxy(suffix_qubits: int) -> int:
    """Expose one-flag controlled-subframe depth terms.

    The branch activation token is an external control.  Every nonfinal local
    layer computes a zero-suffix flag, applies a no-workspace UCG of width
    ``d+3``, and uncomputes the flag.  The final UCG has width ``s+1``.
    Unit coefficients are used only to keep every asymptotic contribution
    visible.
    """

    if suffix_qubits < 1:
        raise ValueError("suffix_qubits must be positive.")
    s = suffix_qubits
    predicate = sum(2 * (s - depth - 1) for depth in range(s - 1))
    linear = sum(depth + 3 for depth in range(s - 1)) + (s + 1)
    exponential = sum(
        math.ceil((1 << (depth + 3)) / (depth + 3))
        for depth in range(s - 1)
    ) + math.ceil((1 << (s + 1)) / (s + 1))
    return predicate + linear + exponential


def controlled_branch_size_proxy(suffix_qubits: int) -> int:
    """Expose the ``O(2**s)`` size terms of one controlled subtree frame."""

    if suffix_qubits < 1:
        raise ValueError("suffix_qubits must be positive.")
    s = suffix_qubits
    predicate = sum(2 * (s - depth - 1) for depth in range(s - 1))
    ucg = sum(1 << (depth + 3) for depth in range(s - 1)) + (1 << (s + 1))
    return predicate + ucg


def routing_depth_proxy(n: int, t: int) -> int:
    """Return a transparent route/unroute depth proxy.

    Four fanout-tree traversals cover fanout and uncomputation before the
    forward and reverse routers.  The routers themselves contain ``t`` Fredkin
    stages in each direction.
    """

    ledger = route_workspace_ledger(n, t)
    fanout_depth = _ceil_log2(ledger.branches * (ledger.suffix_qubits + 1))
    return 4 * fanout_depth + 2 * t


def routing_size_proxy(n: int, t: int) -> int:
    """Return a linear route/fanout size proxy."""

    ledger = route_workspace_ledger(n, t)
    edge_lanes = (ledger.branches - 1) * (ledger.suffix_qubits + 1)
    return 6 * edge_lanes


def routed_frame_depth_proxy(n: int, t: int) -> int:
    """Combine conditioned prefix, routing, and parallel branch depth proxies."""

    ledger = route_workspace_ledger(n, t)
    return (
        unary_prefix_depth_proxy(n, t)
        + routing_depth_proxy(n, t)
        + controlled_branch_depth_proxy(ledger.suffix_qubits)
    )


def routed_frame_size_proxy(n: int, t: int) -> int:
    """Combine all size proxies for one routed cut."""

    ledger = route_workspace_ledger(n, t)
    return (
        unary_prefix_size_proxy(n, t)
        + routing_size_proxy(n, t)
        + ledger.branches
        * controlled_branch_size_proxy(ledger.suffix_qubits)
    )


def optimal_qsp_depth_proxy(n: int, ancillas: int) -> int:
    """Return ``n + ceil(2**n/(n+m))`` for comparison only."""

    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    return n + math.ceil((1 << n) / (n + ancillas))


def optimality_plan_row(n: int, ancillas: int) -> OptimalityPlanRow:
    """Choose the audited low-workspace or routed candidate schedule.

    For ``m=0`` the selected low-workspace schedule uses one additional clean
    flag; this row does not conceal that endpoint.  For every ``m>=1`` the
    selected schedule uses at most the requested ``m`` ancillas.
    """

    _validate_n(n)
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")
    N = 1 << n
    cut = choose_routed_cut(n, ancillas)
    if cut is None:
        low = ancilla_depth_row(n, ancillas)
        return OptimalityPlanRow(
            n=n,
            dimension=N,
            requested_ancillas=ancillas,
            used_ancillas_upper_bound=low.frame_ancillas_upper_bound,
            mode="audited-low-workspace",
            prefix_qubits=low.unary_prefix_qubits,
            suffix_qubits=n - low.unary_prefix_qubits,
            branches=1 << low.unary_prefix_qubits,
            prefix_depth_proxy=low.prefix_depth_proxy,
            routing_depth_proxy=0,
            controlled_branch_depth_proxy=0,
            total_depth_proxy=low.total_frame_depth_proxy,
            prefix_size_proxy=low.prefix_size_proxy,
            routing_size_proxy=0,
            controlled_branches_size_proxy=low.ucg_size_proxy,
            total_size_proxy=low.total_frame_size_proxy,
            optimal_qsp_depth_proxy=optimal_qsp_depth_proxy(n, ancillas),
        )

    ledger = route_workspace_ledger(n, cut)
    prefix_depth = unary_prefix_depth_proxy(n, cut)
    route_depth = routing_depth_proxy(n, cut)
    branch_depth = controlled_branch_depth_proxy(ledger.suffix_qubits)
    prefix_size = unary_prefix_size_proxy(n, cut)
    route_size = routing_size_proxy(n, cut)
    branches_size = ledger.branches * controlled_branch_size_proxy(
        ledger.suffix_qubits
    )
    return OptimalityPlanRow(
        n=n,
        dimension=N,
        requested_ancillas=ancillas,
        used_ancillas_upper_bound=ledger.exact_peak_upper_bound,
        mode="routed-parallel-subframes",
        prefix_qubits=cut,
        suffix_qubits=ledger.suffix_qubits,
        branches=ledger.branches,
        prefix_depth_proxy=prefix_depth,
        routing_depth_proxy=route_depth,
        controlled_branch_depth_proxy=branch_depth,
        total_depth_proxy=prefix_depth + route_depth + branch_depth,
        prefix_size_proxy=prefix_size,
        routing_size_proxy=route_size,
        controlled_branches_size_proxy=branches_size,
        total_size_proxy=prefix_size + route_size + branches_size,
        optimal_qsp_depth_proxy=optimal_qsp_depth_proxy(n, ancillas),
    )


def optimality_plan_rows(
    n: int, ancillas: Iterable[int]
) -> tuple[OptimalityPlanRow, ...]:
    return tuple(optimality_plan_row(n, int(value)) for value in ancillas)


# ---------------------------------------------------------------------------
# Small dense checks of the coherent branch router.
# ---------------------------------------------------------------------------


def _route_layout(t: int, s: int) -> tuple[list[list[int]], list[int], int]:
    if t < 1 or s < 1:
        raise ValueError("Dense routed checks require t>=1 and s>=1.")
    branches = 1 << t
    data = [
        [t + branch * s + lane for lane in range(s)]
        for branch in range(branches)
    ]
    tokens = [t + branches * s + branch for branch in range(branches)]
    total_qubits = t + branches * s + branches
    return data, tokens, total_qubits


def _basis_bits(label: int, total_qubits: int) -> list[int]:
    return [
        (label >> (total_qubits - qubit - 1)) & 1
        for qubit in range(total_qubits)
    ]


def _basis_label(bits: list[int]) -> int:
    label = 0
    for bit in bits:
        label = (label << 1) | int(bit)
    return label


def coherent_route_permutation(
    t: int,
    s: int,
    *,
    inverse: bool = False,
    maximum_hilbert_dimension: int = 4096,
) -> np.ndarray:
    """Return the small dense basis permutation of the logical router.

    Prefix bits are processed from least significant to most significant.  At
    level ``ell``, register ``u`` is conditionally swapped with
    ``u+2**ell``.  The same route is applied to every suffix lane and to the
    activation token.  Control-copy fanout is omitted because it changes only
    parallel depth, not the logical permutation.
    """

    data, tokens, total_qubits = _route_layout(t, s)
    dimension = 1 << total_qubits
    if dimension > maximum_hilbert_dimension:
        raise ValueError(
            "Dense router checks are limited by maximum_hilbert_dimension."
        )
    levels = range(t - 1, -1, -1) if inverse else range(t)
    permutation = np.empty(dimension, dtype=np.int64)
    for label in range(dimension):
        bits = _basis_bits(label, total_qubits)
        for level in levels:
            control = t - level - 1
            if bits[control] == 0:
                continue
            offset = 1 << level
            for node in range(offset):
                other = node + offset
                for lane in range(s):
                    first = data[node][lane]
                    second = data[other][lane]
                    bits[first], bits[second] = bits[second], bits[first]
                first = tokens[node]
                second = tokens[other]
                bits[first], bits[second] = bits[second], bits[first]
        permutation[label] = _basis_label(bits)
    return permutation


def _apply_permutation(state: np.ndarray, permutation: np.ndarray) -> np.ndarray:
    out = np.zeros_like(state)
    out[permutation] = state
    return out


def _apply_controlled_local_unitary(
    state: np.ndarray,
    unitary: np.ndarray,
    control: int,
    targets: list[int],
    total_qubits: int,
) -> np.ndarray:
    target_dimension = 1 << len(targets)
    if unitary.shape != (target_dimension, target_dimension):
        raise ValueError("unitary dimension does not match target register.")
    other_axes = [
        qubit
        for qubit in range(total_qubits)
        if qubit != control and qubit not in targets
    ]
    axes = [control, *targets, *other_axes]
    inverse_axes = np.argsort(axes)
    tensor = np.transpose(
        state.reshape([2] * total_qubits), axes
    ).reshape(2, target_dimension, -1)
    tensor[1] = unitary @ tensor[1]
    return np.transpose(
        tensor.reshape([2] * total_qubits), inverse_axes
    ).reshape(-1)


def _embed_routed_input(
    system_state: object, t: int, s: int
) -> tuple[np.ndarray, int]:
    data, tokens, total_qubits = _route_layout(t, s)
    values = np.asarray(system_state, dtype=complex).reshape(-1)
    if values.size != 1 << (t + s):
        raise ValueError("system_state dimension does not match t+s.")
    out = np.zeros(1 << total_qubits, dtype=complex)
    for system_label, amplitude in enumerate(values):
        prefix = system_label >> s
        suffix = system_label & ((1 << s) - 1)
        bits = [0] * total_qubits
        for qubit in range(t):
            bits[qubit] = (prefix >> (t - qubit - 1)) & 1
        for lane in range(s):
            bits[data[0][lane]] = (suffix >> (s - lane - 1)) & 1
        bits[tokens[0]] = 1  # prepared from a clean qubit by one X gate
        out[_basis_label(bits)] = amplitude
    return out, total_qubits


def _extract_routed_output(
    state: np.ndarray, t: int, s: int
) -> tuple[np.ndarray, float]:
    data, tokens, total_qubits = _route_layout(t, s)
    system = np.zeros(1 << (t + s), dtype=complex)
    valid = np.zeros(state.size, dtype=bool)
    for system_label in range(system.size):
        prefix = system_label >> s
        suffix = system_label & ((1 << s) - 1)
        bits = [0] * total_qubits
        for qubit in range(t):
            bits[qubit] = (prefix >> (t - qubit - 1)) & 1
        for lane in range(s):
            bits[data[0][lane]] = (suffix >> (s - lane - 1)) & 1
        bits[tokens[0]] = 1
        label = _basis_label(bits)
        system[system_label] = state[label]
        valid[label] = True
    leakage = float(np.linalg.norm(state[~valid]))
    return system, leakage


def routed_tail_action_small(
    n: int,
    t: int,
    theta_mag: object,
    system_state: object,
    *,
    maximum_hilbert_dimension: int = 4096,
) -> tuple[np.ndarray, float]:
    """Simulate route--parallel-subframes--unroute for a small exact check."""

    _validate_cut(n, t, allow_endpoints=False)
    s = n - t
    data, tokens, total_qubits = _route_layout(t, s)
    if (1 << total_qubits) > maximum_hilbert_dimension:
        raise ValueError(
            "Dense routed checks are limited by maximum_hilbert_dimension."
        )
    state, _ = _embed_routed_input(system_state, t, s)
    forward = coherent_route_permutation(
        t, s, maximum_hilbert_dimension=maximum_hilbert_dimension
    )
    state = _apply_permutation(state, forward)
    for prefix in range(1 << t):
        block = direct_real_frame(
            s, subtree_angles(theta_mag, n, t, prefix)
        )
        state = _apply_controlled_local_unitary(
            state, block, tokens[prefix], data[prefix], total_qubits
        )
    backward = coherent_route_permutation(
        t,
        s,
        inverse=True,
        maximum_hilbert_dimension=maximum_hilbert_dimension,
    )
    state = _apply_permutation(state, backward)
    return _extract_routed_output(state, t, s)
