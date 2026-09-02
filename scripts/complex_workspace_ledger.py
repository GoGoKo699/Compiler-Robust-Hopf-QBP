#!/usr/bin/env python3
"""Print the common-workspace ledger for the separated complex Hopf frame."""
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

from compiler_robust_hopf.complex_resources import complex_workspace_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument(
        "--ancillas",
        type=str,
        default=None,
        help="Comma-separated matched state-preparation ancillary budgets.",
    )
    parser.add_argument("--format", choices=("text", "csv", "json"), default="text")
    return parser.parse_args()


def default_budgets(n: int) -> list[int]:
    N = 1 << n
    log_n = max(1, math.ceil(math.log2(max(2, n))))
    return sorted(
        {
            0,
            1,
            n,
            2 * n,
            max(1, N // max(1, n * n)),
            max(1, N // max(1, n * log_n)),
            max(1, N // n),
            N,
            3 * N,
        }
    )


def parse_budgets(raw: str | None, n: int) -> list[int]:
    if raw is None:
        return default_budgets(n)
    pieces = [piece.strip() for piece in raw.split(",")]
    if not pieces or any(not piece for piece in pieces):
        raise ValueError("--ancillas must be a comma-separated list of integers.")
    try:
        budgets = [int(piece) for piece in pieces]
    except ValueError as exc:
        raise ValueError(
            "--ancillas must be a comma-separated list of integers."
        ) from exc
    if any(value < 0 for value in budgets):
        raise ValueError("Ancillary budgets must be nonnegative.")
    return budgets


def print_text(rows: list[dict[str, int | str]]) -> None:
    print("Separated complex Hopf-frame common-workspace ledger")
    print("Numeric depth and size columns are term proxies, not finite gate counts.")
    print(
        f"{'n':>3} {'N':>9} {'m':>9} {'common':>8} {'diag-used':>10} "
        f"{'diag mode':>24} {'real D':>9} {'diag D':>9} {'complex D':>10} "
        f"{'candidate':>10} {'QSP opt.':>9}"
    )
    for row in rows:
        print(
            f"{int(row['n']):>3} {int(row['dimension']):>9} "
            f"{int(row['state_ancillas']):>9} "
            f"{int(row['common_workspace_upper_bound']):>8} "
            f"{int(row['diagonal_ancillas_used']):>10} "
            f"{str(row['diagonal_mode']):>24} "
            f"{int(row['real_frame_depth_proxy']):>9} "
            f"{int(row['diagonal_depth_proxy']):>9} "
            f"{int(row['complex_frame_depth_proxy']):>10} "
            f"{int(row['candidate_depth_proxy']):>10} "
            f"{int(row['optimal_qsp_depth_proxy']):>9}"
        )
    print("\nFor m >= 1, W_R and D_ph reuse the same m clean ancillary qubits.")
    print("For m = 0, the O(N)-size construction uses one reusable real-frame flag.")
    print("A strict zero-ancilla fallback is also reported in JSON/CSV output.")


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

    rows = [asdict(row) for row in complex_workspace_rows(args.n, budgets)]
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
                    "status": "common-workspace complex-frame theorem",
                    "frame": "W_C = D_ph W_R",
                    "workspace": (
                        "same m for m>=1; one additive clean flag at nominal m=0"
                    ),
                    "diagonal_depth": "O(n + 2**n/(n+m))",
                    "complex_frame_depth": (
                        "O(n*(n-t+1) + 2**n/(n+m))"
                    ),
                    "strict_zero_fallback": (
                        "O(2**n) depth and O(n*2**n) size"
                    ),
                    "rows": rows,
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
