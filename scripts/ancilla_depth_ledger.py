#!/usr/bin/env python3
"""Print the audited Hopf-frame ancilla--depth term ledger."""
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

from compiler_robust_hopf.ancilla_depth import ancilla_depth_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument(
        "--ancillas",
        type=str,
        default=None,
        help="Comma-separated matched state-compiler ancillary budgets.",
    )
    parser.add_argument(
        "--format", choices=("text", "csv", "json"), default="text"
    )
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
            max(1, N // max(1, n)),
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


def print_text(rows: list[dict[str, int]]) -> None:
    print("Compiler-robust Hopf-frame audited ledger")
    print("Depth and size columns are unit-coefficient proxies, not exact gate costs.")
    print("Frame workspace: same m for m>=1; one clean flag at m=0.")
    print(
        f"{'n':>3} {'N':>9} {'m':>8} {'frame':>7} {'t':>4} "
        f"{'UCG w':>6} {'prefix D':>8} {'pred D':>7} {'UCG D':>8} "
        f"{'total D':>8} {'prefix S':>8} {'UCG S':>9} {'total S':>9}"
    )
    for row in rows:
        ucg_depth = (
            row["ucg_linear_depth_proxy"]
            + row["ucg_exponential_depth_proxy"]
        )
        work = row["nonfinal_ucg_work_ancillas"]
        print(
            f"{row['n']:>3} {row['dimension']:>9} "
            f"{row['state_ancillas']:>8} "
            f"{row['frame_ancillas_upper_bound']:>7} "
            f"{row['unary_prefix_qubits']:>4} {work:>6} "
            f"{row['prefix_depth_proxy']:>8} "
            f"{row['tail_predicate_depth_proxy']:>7} "
            f"{ucg_depth:>8} {row['total_frame_depth_proxy']:>8} "
            f"{row['prefix_size_proxy']:>8} "
            f"{row['ucg_size_proxy']:>9} "
            f"{row['total_frame_size_proxy']:>9}"
        )
    print("\nAudited theorem:")
    print("  workspace <= max(1, m)")
    print("  size = O(2**n)")
    print("  depth = O(n (n - t + 1) + 2**n/(n + m))")
    print("  t = min(n, max(0, floor(log2(m/3))))")
    print("The prefix-size proxy exposes the corrected O(2**t + n - t) form.")


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

    rows = [asdict(row) for row in ancilla_depth_rows(args.n, budgets)]
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
                    "status": (
                        "real-frame theorem internally proof-audited relative "
                        "to imported exact synthesis lemmas"
                    ),
                    "rows": rows,
                    "workspace_bound": "max(1,m)",
                    "same_matched_workspace_for": "m>=1",
                    "candidate_depth": (
                        "O(n*(n-t+1) + 2**n/(n+m))"
                    ),
                    "complete_size": "O(2**n)",
                    "prefix_size": "O(2**t + n - t)",
                    "optimal_qsp_depth": (
                        "Theta(n + 2**n/(n+m))"
                    ),
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
