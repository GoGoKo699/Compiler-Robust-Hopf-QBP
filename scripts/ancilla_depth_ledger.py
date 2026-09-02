#!/usr/bin/env python3
"""Print the candidate Hopf-frame ancilla--depth term ledger."""
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
        help="Comma-separated state-compiler ancillary budgets.",
    )
    parser.add_argument("--format", choices=("text", "csv", "json"), default="text")
    return parser.parse_args()


def default_budgets(n: int) -> list[int]:
    N = 1 << n
    log_n = max(1, math.ceil(math.log2(max(2, n))))
    return sorted(
        {
            0,
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
    print("Compiler-robust Hopf-frame research ledger")
    print("Depth columns are unit-coefficient term proxies, not exact gate depths.")
    print("The frame workspace bound is the matched state budget plus one clean flag.")
    print(
        f"{'n':>3} {'N':>9} {'m':>9} {'frame':>9} {'t':>4} {'tail':>5} "
        f"{'prefix':>8} {'pred':>8} {'UCG-lin':>8} {'UCG-exp':>8} "
        f"{'total':>8} {'candidate':>10} {'QSP opt.':>9}"
    )
    for row in rows:
        candidate = row["candidate_sequential_term"] + row["candidate_geometric_term"]
        qsp = row["optimal_qsp_linear_term"] + row["optimal_qsp_geometric_term"]
        print(
            f"{row['n']:>3} {row['dimension']:>9} {row['state_ancillas']:>9} "
            f"{row['frame_ancillas_upper_bound']:>9} "
            f"{row['unary_prefix_qubits']:>4} {row['tail_layers']:>5} "
            f"{row['prefix_depth_proxy']:>8} "
            f"{row['tail_predicate_depth_proxy']:>8} "
            f"{row['ucg_linear_depth_proxy']:>8} "
            f"{row['ucg_exponential_depth_proxy']:>8} "
            f"{row['total_frame_depth_proxy']:>8} {candidate:>10} {qsp:>9}"
        )
    print("\nCandidate: O(n (n - t + 1) + 2**n/(n + m)).")
    print("QSP optimum: Theta(n + 2**n/(n + m)).")
    print("The exact bridge and unary-code identities are validated separately.")


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
                    "status": "research theorem candidate",
                    "rows": rows,
                    "candidate_depth": "O(n*(n-t+1) + 2**n/(n+m))",
                    "optimal_qsp_depth": "Theta(n + 2**n/(n+m))",
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
