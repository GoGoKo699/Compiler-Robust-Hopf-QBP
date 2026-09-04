from __future__ import annotations

import json
import re
from pathlib import Path

from normalize_inline_math_v3 import (
    ROOT,
    FENCE,
    INLINE_CODE,
    audit,
    markdown_files,
    normalize_math_body,
)


GROUP = re.compile(r"^(?:SU|SO|U|O|Sp)\(\d+\)$")
PURE_NUMBER = re.compile(r"^-?\d+(?:\.\d+)?$")
NUMBER_FRACTION = re.compile(r"^-?\d+/\d+$")
NUMBER_LIST = re.compile(r"^\d+(?:,\d+)+$")
BINARY_LABEL = re.compile(r"^[01]{2,}$")
INTERVAL = re.compile(r"^[\[(].+,.+[\])]$")


def additional_math_span(span: str) -> bool:
    value = span.strip()
    return any(
        pattern.fullmatch(value)
        for pattern in (
            GROUP,
            PURE_NUMBER,
            NUMBER_FRACTION,
            NUMBER_LIST,
            BINARY_LABEL,
            INTERVAL,
        )
    )


def transform_text(text: str) -> tuple[str, int]:
    output: list[str] = []
    changed = 0
    in_fence = False
    fence = ""

    for line in text.splitlines(keepends=True):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if not in_fence:
                in_fence = True
                fence = token
            elif token == fence:
                in_fence = False
                fence = ""
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue

        def repl(match: re.Match[str]) -> str:
            nonlocal changed
            span = match.group(1)
            if not additional_math_span(span):
                return match.group(0)
            changed += 1
            return f"${normalize_math_body(span)}$"

        output.append(INLINE_CODE.sub(repl, line))

    return "".join(output), changed


def main() -> None:
    files = markdown_files()
    changed_files: list[dict[str, object]] = []
    for path in files:
        original = path.read_text(encoding="utf-8")
        transformed, count = transform_text(original)
        if count:
            path.write_text(transformed, encoding="utf-8")
            changed_files.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "replacement_count": count,
                }
            )

    report = audit(files)
    report["additional_changed_files"] = changed_files
    output = ROOT / "provenance" / "inline_math_normalization.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

    if (
        report["remaining_math_like_code_spans"]
        or report["suspicious_inline_math"]
        or report["unbalanced_inline_math_delimiters"]
    ):
        raise SystemExit("inline-mathematics audit failed")


if __name__ == "__main__":
    main()
