"""Common-workspace resource ledgers for the separated complex Hopf frame.

The diagonal resource rows expose the exact piecewise use of the synthesis
results of Sun--Tian--Yang--Yuan--Zhang. The complete rows combine those terms
with the audited real-frame ledger. Numeric columns are transparent term
proxies, not exact elementary-gate counts or depths.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable

from .ancilla_depth import AncillaDepthRow, ancilla_depth_row


@dataclass(frozen=True)
class DiagonalSynthesisRow:
    """One exact-synthesis regime for an arbitrary ``n``-qubit diagonal."""

    n: int
    dimension: int
    requested_ancillas: int
    used_ancillas: int
    mode: str
    log_depth_proxy: int
    phase_round_depth_proxy: int
    global_phase_depth_proxy: int
    total_depth_proxy: int
    theorem_depth_proxy: int
    size_proxy: int
    parameter_count: int
    parameter_preprocess_proxy: int

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


@dataclass(frozen=True)
class ComplexWorkspaceRow:
    """Common-workspace ledger for ``W_C = D_ph W_R``."""

    n: int
    dimension: int
    state_ancillas: int
    common_workspace_upper_bound: int
    real_frame_workspace_upper_bound: int
    diagonal_ancillas_used: int
    diagonal_mode: str
    unary_prefix_qubits: int
    real_frame_depth_proxy: int
    diagonal_depth_proxy: int
    complex_frame_depth_proxy: int
    candidate_depth_proxy: int
    optimal_qsp_depth_proxy: int
    real_frame_size_proxy: int
    diagonal_size_proxy: int
    complex_frame_size_proxy: int
    strict_zero_frame_depth_proxy: int
    strict_zero_frame_size_proxy: int
    magnitude_reverse_frame_applications: int
    direct_phase_reverse_frame_applications: int
    magnitude_decode_operations_per_shot: int
    phase_decode_operations_per_shot: int
    phase_parameter_preprocess_proxy: int

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


def _validate_n_m(n: int, ancillas: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")
    if ancillas < 0:
        raise ValueError("ancillas must be nonnegative.")


def _ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive.")
    return (value - 1).bit_length()


def diagonal_ancillas_used(n: int, ancillas: int) -> int:
    """Choose a valid ancillary count for Sun et al. Lemma 10.

    Lemma 10 applies when ``2*n <= w <= 2**n/n``. Below that interval the
    ancilla-free Lemma 11 is used. Above it, the construction ignores surplus
    workspace and caps ``w`` at ``floor(2**n/n)``. For the finitely many small
    ``n`` where the interval is empty, the ancilla-free construction is used.
    """

    _validate_n_m(n, ancillas)
    N = 1 << n
    lower = 2 * n
    upper = N // n
    if upper < lower or ancillas < lower:
        return 0
    return min(ancillas, upper)


def diagonal_synthesis_mode(n: int, ancillas: int) -> str:
    used = diagonal_ancillas_used(n, ancillas)
    if used == 0:
        return "ancilla-free"
    if used == ancillas:
        return "parallel-ancilla"
    return "capped-parallel-ancilla"


def diagonal_synthesis_row(n: int, ancillas: int) -> DiagonalSynthesisRow:
    """Return an all-budget exact diagonal-synthesis ledger.

    The common phase is separated from a diagonal whose ``|0...0>`` entry is
    one. In the arbitrary-one-qubit gate model it is restored by one local
    scalar-phase gate. The cited ancillary construction explicitly uncomputes
    its copy and phase registers.
    """

    _validate_n_m(n, ancillas)
    N = 1 << n
    used = diagonal_ancillas_used(n, ancillas)
    if used == 0:
        log_term = 0
        phase_rounds = math.ceil(N / n)
        size = N + 1
    else:
        log_term = _ceil_log2(used)
        phase_rounds = math.ceil(N / used)
        size = 3 * N + n * used + math.ceil(7 * used / 2) + 1
    common_phase = 1
    total_depth = log_term + phase_rounds + common_phase
    theorem_depth = n + math.ceil(N / (n + ancillas))
    return DiagonalSynthesisRow(
        n=n,
        dimension=N,
        requested_ancillas=ancillas,
        used_ancillas=used,
        mode=diagonal_synthesis_mode(n, ancillas),
        log_depth_proxy=log_term,
        phase_round_depth_proxy=phase_rounds,
        global_phase_depth_proxy=common_phase,
        total_depth_proxy=total_depth,
        theorem_depth_proxy=theorem_depth,
        size_proxy=size,
        parameter_count=N,
        parameter_preprocess_proxy=n * N,
    )


def strict_zero_real_frame_depth_proxy(n: int) -> int:
    """Return the strict-zero-ancilla full-width-UCG fallback depth proxy."""

    _validate_n_m(n, 0)
    N = 1 << n
    return n * (n + math.ceil(N / n))


def strict_zero_real_frame_size_proxy(n: int) -> int:
    """Return the ``O(n*2**n)`` strict-zero-ancilla size proxy."""

    _validate_n_m(n, 0)
    return n * (1 << n)


def complex_workspace_row(n: int, state_ancillas: int) -> ComplexWorkspaceRow:
    """Compose the clean real frame and clean diagonal using one workspace pool."""

    _validate_n_m(n, state_ancillas)
    N = 1 << n
    real: AncillaDepthRow = ancilla_depth_row(n, state_ancillas)
    diagonal = diagonal_synthesis_row(n, state_ancillas)
    common_workspace = max(
        real.frame_ancillas_upper_bound,
        diagonal.used_ancillas,
    )
    complex_depth = real.total_frame_depth_proxy + diagonal.total_depth_proxy
    complex_size = real.total_frame_size_proxy + diagonal.size_proxy
    candidate_depth = (
        real.candidate_sequential_term
        + real.candidate_geometric_term
        + diagonal.theorem_depth_proxy
    )
    optimal_qsp_depth = (
        real.optimal_qsp_linear_term + real.optimal_qsp_geometric_term
    )
    strict_zero_depth = (
        strict_zero_real_frame_depth_proxy(n)
        + diagonal_synthesis_row(n, 0).total_depth_proxy
    )
    strict_zero_size = (
        strict_zero_real_frame_size_proxy(n)
        + diagonal_synthesis_row(n, 0).size_proxy
    )
    return ComplexWorkspaceRow(
        n=n,
        dimension=N,
        state_ancillas=state_ancillas,
        common_workspace_upper_bound=common_workspace,
        real_frame_workspace_upper_bound=real.frame_ancillas_upper_bound,
        diagonal_ancillas_used=diagonal.used_ancillas,
        diagonal_mode=diagonal.mode,
        unary_prefix_qubits=real.unary_prefix_qubits,
        real_frame_depth_proxy=real.total_frame_depth_proxy,
        diagonal_depth_proxy=diagonal.total_depth_proxy,
        complex_frame_depth_proxy=complex_depth,
        candidate_depth_proxy=candidate_depth,
        optimal_qsp_depth_proxy=optimal_qsp_depth,
        real_frame_size_proxy=real.total_frame_size_proxy,
        diagonal_size_proxy=diagonal.size_proxy,
        complex_frame_size_proxy=complex_size,
        strict_zero_frame_depth_proxy=strict_zero_depth,
        strict_zero_frame_size_proxy=strict_zero_size,
        magnitude_reverse_frame_applications=1,
        direct_phase_reverse_frame_applications=0,
        magnitude_decode_operations_per_shot=N,
        phase_decode_operations_per_shot=1,
        phase_parameter_preprocess_proxy=n * N,
    )


def complex_workspace_rows(
    n: int, state_ancillas: Iterable[int]
) -> tuple[ComplexWorkspaceRow, ...]:
    return tuple(complex_workspace_row(n, int(value)) for value in state_ancillas)
