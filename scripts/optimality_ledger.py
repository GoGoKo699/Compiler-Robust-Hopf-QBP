#!/usr/bin/env python3
"""Print routed-subframe planner rows for optimality checkpoint 1."""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from compiler_robust_hopf.optimal_parallel import optimality_plan_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument(
        "--ancillas",
        type=str,
        default=None,
        help="Comma-separated clean ancillary budgets.",
    )
    parser.add_argument("--format", choices=("text", "csv", "json"), default="text")
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
            max(1, N // (n * n)),
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
        raise ValueError(
            "--ancillas must be a comma-separated list of integers."
        ) from exc
    if any(value < 0 for value in values):
        raise ValueError("Ancillary budgets must be nonnegative.")
    return values


def print_text(rows: list[dict[str, int | str]]) -> None:
    print("Optimal all-ancilla checkpoint-1 planner")
    print("Numeric depth and size columns are transparent term proxies, not exact gates.")
    print("The positive-workspace theorem remains a proof candidate pending audit.")
    print(
        f"{'n':>3} {'N':>11} {'m':>11} {'used':>11} {'mode':>28} "
        f"{'t':>4} {'s':>4} {'B':>9} {'depth':>10} {'QSP':>10} {'size/N':>9}"
    )
    for row in rows:
        ratio = float(row["total_size_proxy"]) / float(row["dimension"])
        print(
            f"{int(row['n']):>3} {int(row['dimension']):>11} "
            f"{int(row['requested_ancillas']):>11} "
            f"{int(row['used_ancillas_upper_bound']):>11} "
            f"{str(row['mode']):>28} "
            f"{int(row['prefix_qubits']):>4} "
            f"{int(row['suffix_qubits']):>4} "
            f"{int(row['branches']):>9} "
            f"{int(row['total_depth_proxy']):>10} "
            f"{int(row['optimal_qsp_depth_proxy']):>10} "
            f"{ratio:>9.3f}"
        )
    print("\nCandidate for m>=1:")
    print("  size  = O(2**n)")
    print("  depth = O(n + 2**n/(n+m))")
    print("  clean workspace <= m")
    print("Strict m=0 with both sharp size and optimal depth remains open.")


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
    rows = [asdict(row) for row in optimality_plan_rows(args.n, budgets)]
    if args.format == "text":
        print_text(rows)
    elif args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    else:
        print(
            json.dumps(
                {
                    "status": "optimal positive-workspace proof candidate",
                    "candidate_depth": "O(n + 2**n/(n+m)) for m>=1",
                    "candidate_size": "O(2**n)",
                    "strict_zero_endpoint": "open at simultaneous sharp size and depth",
                    "rows": rows,
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
