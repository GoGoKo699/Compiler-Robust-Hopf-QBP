#!/usr/bin/env python3
"""Print the strict-zero borrowed-suffix echo research ledger."""
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

from compiler_robust_hopf.strict_zero_echo import (
    borrowed_suffix_echo_layer_resource_row,
    strict_zero_echo_complex_resource_row,
    strict_zero_echo_frame_resource_row,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument(
        "--format",
        choices=("text", "csv", "json"),
        default="text",
    )
    parser.add_argument(
        "--layers",
        action="store_true",
        help="Include the nonfinal per-depth ledger.",
    )
    return parser.parse_args()


def print_text(
    real: dict[str, int | str],
    complex_row: dict[str, int],
    layers: list[dict[str, int]],
) -> None:
    print("Strict-zero borrowed-suffix echo research ledger")
    print("Status: theorem candidate pending independent audit")
    print("No clean or dirty ancillary qubit is introduced.")
    print()
    print(
        f"n={real['n']}  N={real['dimension']}  "
        f"mode={real['mode']}  clean ancillas={real['clean_ancillas']}"
    )
    print(
        "real frame:    "
        f"depth proxy={real['total_depth_proxy']}  "
        f"size proxy={real['total_size_proxy']}"
    )
    print(
        "complex frame: "
        f"depth proxy={complex_row['total_depth_proxy']}  "
        f"size proxy={complex_row['total_size_proxy']}"
    )
    print(
        "optimal QSP depth proxy: "
        f"{real['optimal_qsp_depth_proxy']}"
    )
    print(
        "previous strict-zero full-width-UCG fallback: "
        f"depth proxy={real['previous_full_width_depth_proxy']}  "
        f"size proxy={real['previous_full_width_size_proxy']}"
    )
    print()
    print("Candidate theorem:")
    print("  size  = Theta(2**n)")
    print("  depth = Theta(n + 2**n/n)")
    print("  clean ancillary qubits = 0")
    if layers:
        print()
        print(
            f"{'d':>4} {'suffix':>7} {'borrowed':>8} {'rem':>5} "
            f"{'UCG q':>6} {'depth':>9} {'size':>9} "
            f"{'active':>9} {'full':>9}"
        )
        for row in layers:
            print(
                f"{row['depth']:>4} {row['suffix_qubits']:>7} "
                f"{row['borrowed_bit_position']:>8} "
                f"{row['remaining_suffix_controls']:>5} "
                f"{row['half_angle_ucg_width']:>6} "
                f"{row['total_depth_proxy']:>9} "
                f"{row['total_size_proxy']:>9} "
                f"{row['logical_nonidentity_blocks']:>9} "
                f"{row['full_width_logical_blocks']:>9}"
            )


def main() -> int:
    args = parse_args()
    if args.n < 1:
        print("error: n must be positive.", file=sys.stderr)
        return 2

    real_obj = strict_zero_echo_frame_resource_row(args.n)
    complex_obj = strict_zero_echo_complex_resource_row(args.n)
    layer_objs = [
        borrowed_suffix_echo_layer_resource_row(args.n, depth)
        for depth in range(args.n - 1)
    ]
    real = asdict(real_obj)
    complex_row = asdict(complex_obj)
    layers = [asdict(row) for row in layer_objs]

    if args.format == "text":
        print_text(real, complex_row, layers if args.layers else [])
    elif args.format == "csv":
        rows = layers if args.layers else [real]
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    else:
        print(
            json.dumps(
                {
                    "status": "theorem candidate pending independent audit",
                    "construction": "borrowed-suffix four-toggle echo",
                    "external_framework": (
                        "Yuan and Zhang, Quantum 7, 956 (2023)"
                    ),
                    "claimed_range": "strict m=0",
                    "candidate_theorem": {
                        "real_size": "Theta(2**n)",
                        "real_depth": "Theta(n + 2**n/n)",
                        "complex_size": "Theta(2**n)",
                        "complex_depth": "Theta(n + 2**n/n)",
                        "clean_ancillas": 0,
                    },
                    "real": real,
                    "complex": complex_row,
                    "layers": layers if args.layers else [],
                    "evidence_boundary": (
                        "integer term ledger; analytic proof and independent "
                        "audit remain load-bearing"
                    ),
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
