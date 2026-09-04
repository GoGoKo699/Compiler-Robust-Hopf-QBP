from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$")

PATH_SUFFIXES = (
    ".py", ".md", ".json", ".toml", ".yml", ".yaml", ".svg", ".txt", ".cff"
)
CODE_LITERALS = {
    "main", "Hopf-QBP", "Hopf-ansatz", "frame-safe", "state-column",
    "one-hot", "copy–uncopy", "route–operate–unroute", "X/CNOT/Toffoli",
    "CNOT/Fredkin", "Clifford+T", "FWHT", "UCG", "MCT", "QSP", "MIT",
    "PASS", "README", "Markdown", "NumPy", "Python",
}
MATH_NAMES = {
    "Theta", "Omega", "sqrt", "partial", "lambda", "theta", "phi", "psi",
    "varphi", "alpha", "beta", "chi", "xi", "epsilon", "delta", "ell",
    "nabla", "pi", "diag", "exp", "log", "min", "max", "tensor", "xor",
}


def markdown_files() -> list[Path]:
    ignored = {".git", ".venv", "__pycache__"}
    return sorted(
        path for path in ROOT.rglob("*.md")
        if not any(part in ignored for part in path.parts)
    )


def prose_lines(path: Path):
    in_fence = False
    fence = ""
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if not in_fence:
                in_fence = True
                fence = token
            elif token == fence:
                in_fence = False
                fence = ""
            continue
        if not in_fence:
            yield line_number, line


def mathematical_identifier(name: str) -> bool:
    if name in MATH_NAMES:
        return True
    if re.fullmatch(r"[A-Za-z]", name):
        return True
    prefix = name.split("_", 1)[0]
    return len(prefix) == 1 or prefix in MATH_NAMES


def software_span(span: str) -> bool:
    value = span.strip()
    if value in CODE_LITERALS:
        return True
    if value.startswith(("http://", "https://", "arXiv:", "doi:")):
        return True
    if value.endswith(PATH_SUFFIXES) or value.startswith(("../", "./")):
        return True
    if re.fullmatch(r"[0-9a-f]{7,40}", value):
        return True
    if re.fullmatch(r"v?\d+(?:\.\d+){1,3}(?:-[A-Za-z0-9.]+)?", value):
        return True
    if value.startswith(("python ", "pip ", "git ", "source ", "pytest ")):
        return True
    if "::" in value or value.startswith("--"):
        return True
    if "." in value and not re.search(r"\d\.\d", value):
        return True
    assignment = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)=(.+)", value)
    if assignment and not mathematical_identifier(assignment.group(1)):
        return True
    call = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*)(?:\([^)]*\))?", value)
    if call and not mathematical_identifier(call.group(1)):
        return True
    return False


def math_like_code(span: str) -> bool:
    value = span.strip()
    if not value or software_span(value):
        return False
    if re.search(r"\|[^`]*>|<[^`]*\|", value):
        return True
    if any(token in value for token in (">=", "<=", "=", "^", "**", "->", "=>", "_(")):
        return True
    if re.search(r"[<>]", value):
        return True
    if any(re.search(rf"\b{re.escape(name)}\b", value) for name in MATH_NAMES):
        return True
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9]+)?", value):
        return True
    call = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*)\([^)]*\)", value)
    if call and mathematical_identifier(call.group(1)):
        return True
    if re.fullmatch(r"\([^)]*,[^)]*\)", value):
        return True
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9]+)?(?:,[A-Za-z](?:_[A-Za-z0-9]+)?)+", value):
        return True
    if re.fullmatch(r"\[[^]]+\]", value) and any(ch.isdigit() for ch in value):
        return True
    if re.search(r"\d(?:[A-Za-z]|\*)|[A-Za-z]\d", value):
        return True
    if any(operator in value for operator in ("+", "-", "/", "*")):
        words = re.findall(r"[A-Za-z]+", value)
        return bool(words) and all(len(word) <= 8 or word in MATH_NAMES for word in words)
    return False


class InlineMathProseTests(unittest.TestCase):
    def test_math_like_code_spans_are_absent_from_prose(self) -> None:
        offenders: list[str] = []
        for path in markdown_files():
            relative = path.relative_to(ROOT).as_posix()
            for line_number, line in prose_lines(path):
                for span in INLINE_CODE.findall(line):
                    if math_like_code(span):
                        offenders.append(f"{relative}:{line_number}: `{span}`")
        self.assertFalse(
            offenders,
            msg="Mathematical notation remains formatted as code:\n" + "\n".join(offenders),
        )

    def test_inline_math_has_no_ascii_pseudonotation(self) -> None:
        offenders: list[str] = []
        forbidden = (
            re.compile(r"(?<!\\)\b(?:Theta|Omega|sqrt|partial|lambda|theta|phi|psi|varphi|epsilon|delta|nabla|pi)\b"),
            re.compile(r">=|<=|\*\*|_\("),
            re.compile(r"\|[^$|]*>|<[^$|]*\|"),
        )
        for path in markdown_files():
            relative = path.relative_to(ROOT).as_posix()
            for line_number, line in prose_lines(path):
                for body in INLINE_MATH.findall(line):
                    if any(pattern.search(body) for pattern in forbidden):
                        offenders.append(f"{relative}:{line_number}: ${body}$")
        self.assertFalse(
            offenders,
            msg="ASCII pseudo-notation remains inside inline math:\n" + "\n".join(offenders),
        )

    def test_inline_math_delimiters_are_balanced_line_by_line(self) -> None:
        offenders: list[str] = []
        for path in markdown_files():
            relative = path.relative_to(ROOT).as_posix()
            for line_number, line in prose_lines(path):
                if len(re.findall(r"(?<!\\)\$", line)) % 2:
                    offenders.append(f"{relative}:{line_number}: {line.strip()}")
        self.assertFalse(
            offenders,
            msg="Unbalanced inline-math delimiters:\n" + "\n".join(offenders),
        )

    def test_qbp_metric_paragraph_is_rendered_as_mathematics(self) -> None:
        qbp = (ROOT / "docs" / "QBP_CONSEQUENCE.md").read_text(encoding="utf-8")
        compact = " ".join(qbp.split())
        self.assertIn(
            "For unrestricted angles, $a_j$ is the oriented incoming amplitude and "
            "$g_{j,j}=a_j^2$.",
            compact,
        )
        self.assertIn(
            "On the canonical Hopf domains, $a_j\\geq 0$ and "
            "$a_j=\\sqrt{g_{j,j}}$.",
            compact,
        )
        self.assertIn("If $g_{j,j}=0$, the raw coordinate derivative is zero", compact)

    def test_software_identifiers_remain_code(self) -> None:
        hopf = (ROOT / "docs" / "HOPF_INTERFACE.md").read_text(encoding="utf-8")
        for identifier in (
            "`incoming_amplitude`",
            "`sqrt_metric`",
            "`regular_coordinate_mask(atol=...)`",
            "`in_canonical_magnitude_domain`",
        ):
            self.assertIn(identifier, hopf)
        verification = (ROOT / "docs" / "VERIFICATION.md").read_text(encoding="utf-8")
        self.assertIn("`router.py`", verification)


if __name__ == "__main__":
    unittest.main()
