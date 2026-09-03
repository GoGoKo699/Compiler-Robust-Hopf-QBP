#!/usr/bin/env python3
"""Readable eight-step walkthrough of the repository's central identities.

This script is an orientation tool. It checks representative exact finite
identities and integer resource conditions, but it does not replace the
analytic proofs in REVIEW.md and docs/COMPILER_THEOREM.md.
"""
from __future__ import annotations

import math
import sys
from collections.abc import Callable

import numpy as np

from compiler_robust_hopf.compiler_boundaries import (
    two_qubit_global_state_column_counterexample,
)
from compiler_robust_hopf.frames import (
    direct_real_frame,
    hopf_ry,
    real_frame_matrix,
)
from compiler_robust_hopf.resource_bounds import (
    low_workspace_absorption_holds,
    routed_geometric_inequality_holds,
)
from compiler_robust_hopf.strict_zero_echo import (
    echo_layer_residual,
    echo_sector_action,
)
from compiler_robust_hopf.unified_compiler import (
    diagonal_ucg_matrix,
    unified_real_frame_resource_row,
)


TOL = 2e-12


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def max_residual(first: object, second: object) -> float:
    return float(
        np.max(
            np.abs(
                np.asarray(first, dtype=complex)
                - np.asarray(second, dtype=complex)
            )
        )
    )


def step_frame_identity() -> str:
    theta = np.asarray([0.37, -0.61, 0.82], dtype=float)
    recursive = real_frame_matrix(theta)
    addressed = direct_real_frame(2, theta)
    residual = max_residual(recursive, addressed)
    orthogonality = max_residual(
        recursive.conj().T @ recursive, np.eye(4, dtype=complex)
    )
    require(residual <= TOL, f"frame residual {residual:.3e}")
    require(orthogonality <= TOL, f"orthogonality residual {orthogonality:.3e}")
    return f"addressed/recursive residual={residual:.1e}; orthogonality={orthogonality:.1e}"


def step_state_column_obstruction() -> str:
    example = two_qubit_global_state_column_counterexample()
    zero = np.asarray([1.0, 0.0, 0.0, 0.0], dtype=complex)
    state_residual = max_residual(
        example.frame @ zero, example.compiled_frame @ zero
    )
    require(state_residual <= TOL, f"state-column residual {state_residual:.3e}")
    require(
        max_residual(
            example.correct_decoded_gradient,
            np.asarray([2.0, 0.0, 0.0]),
        )
        <= TOL,
        "canonical decoded gradient is incorrect",
    )
    require(
        max_residual(
            example.compiled_decoded_gradient,
            np.asarray([0.0, math.sqrt(2.0), 0.0]),
        )
        <= TOL,
        "state-equivalent completion did not produce the expected obstruction",
    )
    return "same state column; decoded gradient (2,0,0) -> (0,sqrt(2),0)"


def step_four_sector_echo() -> str:
    theta = 0.731
    identity = np.eye(2, dtype=complex)
    expected = {
        (0, 0): (identity, 0),
        (0, 1): (identity, 1),
        (1, 0): (hopf_ry(theta), 0),
        (1, 1): (identity, 1),
    }
    worst = 0.0
    for sector, (target_expected, bit_expected) in expected.items():
        action, final_bit = echo_sector_action(
            theta, predicate=sector[0], borrowed_bit=sector[1]
        )
        worst = max(worst, max_residual(action, target_expected))
        require(final_bit == bit_expected, f"borrowed bit not restored in {sector}")
    require(worst <= TOL, f"sector residual {worst:.3e}")
    return f"all four (predicate, borrowed-bit) sectors exact; residual={worst:.1e}"


def step_borrowed_layer() -> str:
    angles = np.asarray([0.29, -0.77], dtype=float)
    residual = echo_layer_residual(4, 1, angles)
    require(residual <= TOL, f"echo/addressed layer residual {residual:.3e}")
    return f"n=4, depth=1 complete-layer residual={residual:.1e}; no work wire"


def step_phase_ucg() -> str:
    phases = np.asarray([0.1, -0.3, 0.7, 1.1, -0.8, 0.2, 1.4, -1.0])
    compiled = diagonal_ucg_matrix(phases)
    expected = np.diag(np.exp(1j * phases))
    residual = max_residual(compiled, expected)
    require(residual <= TOL, f"phase UCG residual {residual:.3e}")
    return f"arbitrary eight-leaf diagonal equals one UCG; residual={residual:.1e}"


def step_schedule_selection() -> str:
    n = 8
    zero = unified_real_frame_resource_row(n, 0)
    small = unified_real_frame_resource_row(n, 1)
    routed = unified_real_frame_resource_row(n, 4 * n)
    require(zero.mode == "strict-zero-borrowed-suffix-echo", zero.mode)
    require(small.mode == "direct-flagged-ucg", small.mode)
    require(routed.mode == "tree-decoder-routed-subframes", routed.mode)
    return f"m=0: echo; m=1: direct flag; m={4*n}: routed cut t={routed.prefix_qubits}"


def step_workspace_peak() -> str:
    n = 10
    budgets = (1, 4 * n, 8 * n, 1 << n, 4 * (1 << n))
    details: list[str] = []
    for m in budgets:
        row = unified_real_frame_resource_row(n, m)
        require(
            row.workspace_used_upper_bound <= m,
            f"mode {row.mode} uses {row.workspace_used_upper_bound}>{m}",
        )
        details.append(f"m={m}:{row.workspace_used_upper_bound}")
    return "peak workspace used/budget = " + ", ".join(details)


def step_resource_inequalities() -> str:
    require(low_workspace_absorption_holds(12, 1), "low-workspace bound failed")
    require(
        low_workspace_absorption_holds(12, 4 * 12 - 1),
        "low-workspace endpoint failed",
    )
    require(
        routed_geometric_inequality_holds(12, 4 * 12),
        "routed-cut bound failed",
    )
    require(
        routed_geometric_inequality_holds(12, 1 << 12),
        "large-workspace routed bound failed",
    )
    return "low-workspace absorption and maximal-cut bounds hold at both endpoints"


def main() -> int:
    checks: tuple[tuple[str, Callable[[], str]], ...] = (
        ("canonical two-qubit frame", step_frame_identity),
        ("state-column equality is insufficient", step_state_column_obstruction),
        ("strict-zero four-sector identity", step_four_sector_echo),
        ("borrowed suffix bit is restored", step_borrowed_layer),
        ("complex phase layer is one UCG", step_phase_ucg),
        ("workspace schedule selection", step_schedule_selection),
        ("peak workspace respects m", step_workspace_peak),
        ("resource inequalities", step_resource_inequalities),
    )

    print("Optimal Hopf-frame compiler: reviewer walkthrough")
    print("=" * 54)
    failures = 0
    for index, (name, check) in enumerate(checks, start=1):
        try:
            detail = check()
        except Exception as exc:  # noqa: BLE001 - readable validation report
            failures += 1
            print(f"[{index}] {name:<43} FAIL")
            print(f"    {type(exc).__name__}: {exc}")
        else:
            print(f"[{index}] {name:<43} PASS")
            print(f"    {detail}")

    print("-" * 54)
    if failures:
        print(f"Result: FAIL ({failures} check(s) failed)")
        return 1
    print("Result: PASS")
    print("These finite checks support, but do not replace, the analytic proof.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
