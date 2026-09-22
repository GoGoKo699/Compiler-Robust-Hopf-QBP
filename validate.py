#!/usr/bin/env python3
"""Run the repository unittest collection; exact receipt suites run separately."""
from __future__ import annotations

import argparse
import platform
import sys
import unittest
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent
    print(f"Python: {platform.python_version()}")
    print(f"NumPy: {np.__version__}")
    suite = unittest.defaultTestLoader.discover(
        str(root / "tests"), pattern="test_*.py", top_level_dir=str(root)
    )
    result = unittest.TextTestRunner(
        stream=sys.stdout, verbosity=1 if args.quiet else 2
    ).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
