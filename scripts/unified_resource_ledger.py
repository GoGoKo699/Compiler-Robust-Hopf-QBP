#!/usr/bin/env python3
"""Print the unified all-workspace Hopf-frame resource ledger."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from compiler_robust_hopf.unified_compiler import (
    unified_complex_frame_resource_row,
    unified_real_frame_resource_rows,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument(
        "--ancillas",
        type=str,
        default=None,
        help="Comma-separated clean ancillary budgets.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "csv", "json"),
        default="text",
    )
    return parser.parse_args()


def default_budgets(n: int) -> list[int]:
    N = 1 << n
    return sorted(
        {
            0,
            1,
            n,
            4 * n - 1,
            4 * n,
            max(1, N // max(1, n * n)),
            max(1, N // n),
            N,
            2 * N,
            8 * N,
            *[1 << power for power in range(0, n + 3)],
        }
    )


def parse_budgets(raw: str | None, n: int) -> list[int]:
    if raw is None:
        return default_budgets(n)
    pieces = [piece.strip() for piece in raw.split(",")]
    if not pieces or any(not piece for piece in pieces):
        raise ValueError("--ancillas must be a comma-separated list of integers.")
    try:
        values = [int(piece) for piece in pieces]
    except ValueError as exc:
        raise ValueError("--ancillas must contain integers.") from exc
    if any(value < 0 for value in values):
        raise ValueError("Ancillary budgets must be nonnegative.")
    return values


def print_text(rows: list[dict[str, int | str]]) -> None:
    print("Unified all-workspace Hopf-frame ledger")
    print("External compiler framework: Yuan--Zhang, Quantum 7, 956 (2023).")
    print("Depth and size columns are transparent term proxies, not exact gates.")
    print(
        f"{'n':>3} {'N':>11} {'m':>11} {'used':>11} {'mode':>37} "
        f"{'t':>4} {'s':>4} {'B':>9} {'depth':>10} {'QSP':>10} {'size/N':>9}"
    )
    for row in rows:
        ratio = float(row["total_size_proxy"]) / float(row["dimension"])
        print(
            f"{int(row['n']):>3} {int(row['dimension']):>11} "
            f"{int(row['ancillas']):>11} "
            f"{int(row['workspace_used_upper_bound']):>11} "
            f"{str(row['mode']):>37} "
            f"{int(row['prefix_qubits']):>4} "
            f"{int(row['suffix_qubits']):>4} "
            f"{int(row['branches']):>9} "
            f"{int(row['total_depth_proxy']):>10} "
            f"{int(row['optimal_qsp_depth_proxy']):>10} "
            f"{ratio:>9.3f}"
        )
    print("\nInternally audited all-workspace theorem candidate:")
    print("  real and separated-complex size  = Theta(2**n)")
    print("  real and separated-complex depth = Theta(n + 2**n/(n+m))")
    print("  requested clean workspace is respected for every integer m>=0")
    print("  m=0 uses the borrowed-suffix echo; m>0 uses direct/routed schedules")


def main() -> int:
    args = parse_args()
    if args.n < 1:
        print("error: n must be positive.", file=sys.stderr)
        return 2
    try:
        budgets = parse_budgets(args.ancillas, args.n)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    real_rows = [
        asdict(row)
        for row in unified_real_frame_resource_rows(args.n, budgets)
    ]
    complex_rows = [
        asdict(unified_complex_frame_resource_row(args.n, budget))
        for budget in budgets
    ]
    if args.format == "text":
        print_text(real_rows)
    elif args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=list(real_rows[0]))
        writer.writeheader()
        writer.writerows(real_rows)
    else:
        print(
            json.dumps(
                {
                    "status": "internally audited theorem candidate; external review pending",
                    "active_framework": (
                        "Yuan and Zhang, Quantum 7, 956 (2023)"
                    ),
                    "historical_predecessor": (
                        "Sun et al., IEEE TCAD 42, 3301--3314 (2023)"
                    ),
                    "all_workspace_theorem": {
                        "size": "Theta(2**n)",
                        "depth": "Theta(n + 2**n/(n+m))",
                        "range": "every integer m>=0",
                    },
                    "strict_zero_schedule": (
                        "borrowed-suffix echo with two width-(d+2) half-angle UCGs per nonfinal depth"
                    ),
                    "real_rows": real_rows,
                    "complex_rows": complex_rows,
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
