from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INLINE_CODE = re.compile(r"`([^`\n]+)`")


def markdown_files() -> list[Path]:
    ignored = {".git", ".venv", "__pycache__"}
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in ignored for part in path.parts)
    )


def outside_fences(lines: list[str]):
    in_fence = False
    fence = ""
    for line_number, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue
        if not in_fence:
            yield line_number, line


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="provenance/inline_math_candidates.txt")
    args = parser.parse_args()

    occurrences: dict[str, list[str]] = collections.defaultdict(list)
    for path in markdown_files():
        relative = path.relative_to(ROOT).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_number, line in outside_fences(lines):
            for span in INLINE_CODE.findall(line):
                occurrences[span].append(f"{relative}:{line_number}")

    output = [
        "Inline code-span inventory outside fenced blocks",
        "================================================",
        "",
    ]
    for span in sorted(occurrences, key=lambda value: (value.lower(), value)):
        locations = occurrences[span]
        output.append(f"[{len(locations):03d}] `{span}`")
        output.extend(f"      {location}" for location in locations)

    report = ROOT / args.report
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"wrote {report.relative_to(ROOT)} with {len(occurrences)} unique spans")


if __name__ == "__main__":
    main()
