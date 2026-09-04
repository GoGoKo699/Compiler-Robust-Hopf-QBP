from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCIENTIFIC_MARKDOWN = (
    "README.md",
    "REVIEW.md",
    "docs/CLAIM_SUPPORT.md",
    "docs/CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md",
    "docs/COMPILER_BOUNDARIES.md",
    "docs/COMPILER_THEOREM.md",
    "docs/END_TO_END_QBP.md",
    "docs/FRAME_SAFE_COMPILATION.md",
    "docs/HOPF_INTERFACE.md",
    "docs/INDEPENDENT_REVIEW_GUIDE.md",
    "docs/PRIOR_ART_SEARCH_2026_09.md",
    "docs/PROOF_AUDIT.md",
    "docs/QBP_CONSEQUENCE.md",
    "docs/RELATED_WORK.md",
    "docs/RESEARCH_STATUS.md",
    "docs/SOURCE_MAP.md",
    "docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md",
    "docs/STRICT_ZERO_ECHO_AUDIT.md",
    "docs/STRICT_ZERO_PRIOR_ART.md",
    "docs/THEOREM_OVERVIEW.md",
    "docs/UNIFIED_YUAN_ZHANG_COMPILER.md",
    "docs/VERIFICATION.md",
    "compiler_robust_hopf/README.md",
    "manuscript/README.md",
)

INLINE_CODE = re.compile(r"`([^`\n]+)`")
SINGLE_MATH_SYMBOL = re.compile(
    r"^(?:[A-Za-z]|[A-Za-z]_[A-Za-z0-9]+|[A-Z]_[A-Za-z0-9(),]+)$"
)
MATH_WORD = re.compile(
    r"(?:Theta|Omega|sqrt|partial|lambda|theta|phi|psi|alpha|beta|chi|xi|"
    r"epsilon|delta|nabla|mathrm|mathbb|lvert|rangle)"
)
MATH_EXPRESSION = re.compile(
    r"(?:<=|>=|\^|\*\*|(?<![A-Za-z])(?:O|S|D|T|W|C|F|L|R|J|Q|V|P|I)\s*[(_]|"
    r"[A-Za-z0-9_)][=+*/-][A-Za-z0-9_(]|\|[^`]*>)"
)

CODE_SUFFIXES = (
    ".py",
    ".md",
    ".json",
    ".toml",
    ".cff",
    ".yml",
    ".yaml",
)

CODE_LITERALS = {
    "main",
    "README.md",
    "Python 3.11",
    "Python 3.13",
    "NumPy",
    "UCG",
    "MCT",
    "QSP",
    "QBP",
    "FWHT",
    "CNOT",
    "X/CNOT/Toffoli",
    "CNOT/Fredkin",
    "U(2)",
}

SNAKE_CASE_IDENTIFIER = re.compile(
    r"^[a-z][a-z0-9]+(?:_[a-z0-9]+)+(?:\([^`]*\))?$"
)
CAMEL_CASE_IDENTIFIER = re.compile(r"^[A-Z][A-Za-z0-9]+(?:\([^`]*\))?$")
HEX_SHA = re.compile(r"^[0-9a-f]{7,40}$")
VERSION = re.compile(r"^\d+(?:\.\d+){1,3}(?:-[A-Za-z0-9.]+)?$")

MATH_NAME_PREFIXES = (
    "alpha",
    "beta",
    "theta",
    "phi",
    "psi",
    "lambda",
    "epsilon",
    "delta",
    "chi",
    "xi",
    "nabla",
)


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def is_code_identifier(span: str) -> bool:
    if span in CODE_LITERALS:
        return True
    if span.startswith(("arXiv:", "doi:", "http://", "https://", "--")):
        return True
    if span.endswith(CODE_SUFFIXES) or "/" in span and any(
        suffix in span for suffix in CODE_SUFFIXES
    ):
        return True
    if HEX_SHA.fullmatch(span) or VERSION.fullmatch(span):
        return True
    if span.startswith("atol="):
        return True
    if SNAKE_CASE_IDENTIFIER.fullmatch(span):
        root = span.split("_", 1)[0]
        return root not in MATH_NAME_PREFIXES
    if CAMEL_CASE_IDENTIFIER.fullmatch(span) and not SINGLE_MATH_SYMBOL.fullmatch(span):
        return True
    return False


def looks_mathematical(span: str) -> bool:
    if is_code_identifier(span):
        return False
    if SINGLE_MATH_SYMBOL.fullmatch(span):
        return True
    if MATH_WORD.search(span) or MATH_EXPRESSION.search(span):
        return True
    if span.startswith(("[0,", "(", "{")) and any(
        token in span for token in ("pi", "theta", "phi", "n", "m", "N")
    ):
        return True
    return False


def prose_code_spans(path: Path) -> list[tuple[int, str]]:
    offenders: list[tuple[int, str]] = []
    in_fence = False
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or is_table_line(line):
            continue
        for span in INLINE_CODE.findall(line):
            if looks_mathematical(span):
                offenders.append((line_number, span))
    return offenders


class InlineMathRenderingTests(unittest.TestCase):
    def test_scientific_prose_uses_inline_math_for_symbols(self) -> None:
        offenders: list[str] = []
        for relative in SCIENTIFIC_MARKDOWN:
            path = ROOT / relative
            self.assertTrue(path.is_file(), msg=relative)
            offenders.extend(
                f"{relative}:{line_number}: `{span}`"
                for line_number, span in prose_code_spans(path)
            )

        self.assertFalse(
            offenders,
            msg="Math-like code spans remain inside prose:\n" + "\n".join(offenders),
        )

    def test_representative_inline_formulas_are_rendered(self) -> None:
        qbp = (ROOT / "docs" / "QBP_CONSEQUENCE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(r"$a_j$ is the oriented incoming amplitude", qbp)
        self.assertIn(r"$g_{j,j}=a_j^2$", qbp)
        self.assertIn(r"$a_j\geq0$", qbp)
        self.assertIn(r"$a_j=\sqrt{g_{j,j}}$", qbp)
        self.assertIn(r"$g_{j,j}=0$", qbp)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(r"$m\geq0$", readme)
        self.assertIn(r"$N$-dimensional unitary", readme)


if __name__ == "__main__":
    unittest.main()
