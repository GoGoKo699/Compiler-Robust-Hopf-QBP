"""Regression test for word-hyphen-adjacent GitHub inline mathematics."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^(?:\s*>\s*)*\s*(`{3,}|~{3,})")
PLAIN_HYPHEN_MATH = re.compile(
    r"(?P<hyphen>(?<=[A-Za-z0-9])[-‐‑‒–—])\$(?![`$])(?P<body>[^$\n]+?)(?<!\\)\$(?!\$)"
)
PROTECTED_HYPHEN_MATH = re.compile(
    r"(?<=[A-Za-z0-9])[-‐‑‒–—]\$`[^`\n]+`\$"
)


def prose_lines(text: str):
    fence = None
    for number, line in enumerate(text.splitlines(), start=1):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, line


class HyphenInlineMathTests(unittest.TestCase):
    def test_word_hyphens_do_not_precede_plain_inline_math(self) -> None:
        failures: list[str] = []
        protected = 0
        for path in ROOT.rglob("*.md"):
            if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                continue
            for number, line in prose_lines(path.read_text(encoding="utf-8")):
                for match in PLAIN_HYPHEN_MATH.finditer(line):
                    failures.append(
                        f"{path.relative_to(ROOT)}:{number}: {match.group(0)}"
                    )
                protected += len(PROTECTED_HYPHEN_MATH.findall(line))
        self.assertEqual(failures, [])
        self.assertGreater(
            protected,
            0,
            msg="expected at least one protected word-hyphen inline expression",
        )

    def test_representative_compound_uses_protected_math(self) -> None:
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in ROOT.rglob("*.md")
            if not any(part in {".git", ".venv", "__pycache__"} for part in path.parts)
        )
        self.assertIn("total-width-$`n`$", corpus)


if __name__ == "__main__":
    unittest.main()
