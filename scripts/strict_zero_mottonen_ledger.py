#!/usr/bin/env python3
"""Print the strict-zero Möttönen exploration ledger."""
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

from compiler_robust_hopf.strict_zero_mottonen import (
    strict_zero_mottonen_rows,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nmin", type=int, default=1)
    parser.add_argument("--nmax", type=int, default=16)
    parser.add_argument(
        "--format", choices=("text", "csv", "json"), default="text"
    )
    return parser.parse_args()


def print_text(rows: list[dict[str, int]]) -> None:
    print("Strict-zero Möttönen completion exploration")
    print("All size columns are transparent asymptotic proxies, not exact gate counts.")
    print(
        f"{'n':>3} {'N':>11} {'direct-linear':>15} {'direct-quad':>13} "
        f"{'U+C quad':>12} {'depth upper':>12} {'depth target':>13}"
    )
    for row in rows:
        print(
            f"{row['n']:>3} {row['dimension']:>11} "
            f"{row['direct_conditioned_linear_size_proxy']:>15} "
            f"{row['direct_conditioned_quadratic_size_proxy']:>13} "
            f"{row['completion_plus_correction_size_proxy']:>12} "
            f"{row['current_depth_upper_scale']:>12} "
            f"{row['optimal_depth_target_proxy']:>13}"
        )
    print("\nEstablished on this branch, relative to exact no-workspace controls:")
    print("  strict-zero real-frame size  = Theta(2**n)")
    print("  strict-zero real-frame depth = O(2**n)")
    print("Remaining target:")
    print("  depth = O(n + 2**n/n) with the same zero workspace and linear size")


def main() -> int:
    args = parse_args()
    if args.nmin < 1 or args.nmax < args.nmin:
        print("error: require 1 <= nmin <= nmax", file=sys.stderr)
        return 2
    rows = [
        asdict(row)
        for row in strict_zero_mottonen_rows(
            range(args.nmin, args.nmax + 1)
        )
    ]
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
                    "status": "strict-zero size theorem; optimal depth open",
                    "clean_ancillas": 0,
                    "size": "Theta(2**n)",
                    "depth_upper": "O(2**n)",
                    "depth_target": "O(n + 2**n/n)",
                    "rows": rows,
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
