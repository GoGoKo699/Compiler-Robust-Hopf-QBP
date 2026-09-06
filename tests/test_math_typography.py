"""Regression checks for mathematical meaning and code/prose typography."""
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$")
FENCE = re.compile(r"^(?:\s*>\s*)*\s*(`{3,}|~{3,})")
PROTECTED_MATH = re.compile(r"\$`([^`\n]+)`\$")
KNOWN_CODE = {
    "incoming_amplitude", "incoming_amplitude**2", "metric", "sqrt_metric",
    "regular_coordinate_mask(atol=...)", "in_canonical_magnitude_domain",
}


def prose_lines(text: str):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
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


def math_code(value: str) -> bool:
    """Flag mathematical code spans, without treating software as mathematics."""
    if value in KNOWN_CODE:
        return False
    if value.startswith(("http", "arXiv:", "doi:", "GoGoKo699/", "Hopf-",
                         "python ", "pip ", "git ", "--", "../", "./")):
        return False
    if re.search(r"\.(?:py|md|json|toml|ya?ml|svg|txt|cff)(?:$|[#/])", value):
        return False
    if re.fullmatch(r"[0-9a-f]{7,40}", value):
        return False
    if re.fullmatch(r"v?\d+(?:\.\d+)+(?:-[\w.]+)?", value):
        return False
    return bool(
        re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9]+)?", value)
        or re.search(r"\b(?:Theta|Omega|sqrt|partial|lambda|theta|varphi|phi|psi|pi|delta)\b", value)
        or re.search(r"(?:>=|<=|_\(|\|.*>|\^|\*\*)", value)
        or re.match(r"[A-Za-z](?:_[A-Za-z0-9]+)?[=<>]", value)
        or value in {"L_d^(n)", "F_t^(n)", "R_t^(n)", "W_tilde", "br", "XCX=C^(-1)"}
    )


class MathTypographyTests(unittest.TestCase):
    def test_qbp_metric_paragraph_preserves_meaning(self) -> None:
        text = " ".join((ROOT / "docs/QBP_CONSEQUENCE.md").read_text().split())
        self.assertIn(
            r"For unrestricted angles, $a_j$ is the oriented incoming amplitude and $g_{j,j}=a_j^2$.",
            text,
        )
        self.assertIn(r"On the canonical Hopf domains, $a_j\geq0$ and $a_j=\sqrt{g_{j,j}}$.", text)
        self.assertIn(r"If $g_{j,j}=0$, the raw coordinate derivative is zero", text)

    def test_dimension_labels_are_not_operator_powers(self) -> None:
        theorem = (ROOT / "docs/COMPILER_THEOREM.md").read_text()
        for symbol in ("L_d", "F_t", "R_t"):
            self.assertIn("$" + symbol + "^{(n)}$", theorem)
        for path in ROOT.rglob("*.md"):
            if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                continue
            for number, line in prose_lines(path.read_text()):
                for body in INLINE_MATH.findall(PROTECTED_MATH.sub(lambda m: "$" + m[1] + "$", line)):
                    self.assertIsNone(
                        re.search(r"\b(?:L_d|F_t|R_t)\^\{?n\}?(?![A-Za-z])", body),
                        msg=f"dimension label lost parentheses: {path}:{number}: {body}",
                    )

    def test_adjoints_indices_and_controls_keep_their_roles(self) -> None:
        frame = (ROOT / "docs/FRAME_SAFE_COMPILATION.md").read_text()
        self.assertIn(r"$\widetilde W^{\dagger}$", frame)
        self.assertIn(r"$\widetilde WJ_m=J_mW$", frame)
        bounds = (ROOT / "docs/COMPILER_BOUNDARIES.md").read_text()
        self.assertIn(r"$\widetilde B_d^{\dagger}$", bounds)
        self.assertIn(r"$-2Y_{\mathrm{ancilla}}\otimes K_{d,r}$", bounds)
        verification = (ROOT / "docs/VERIFICATION.md").read_text()
        self.assertIn(r"$XCX=C^{-1}$", verification)

    def test_echo_cleanup_sentence_does_not_undo_the_target(self) -> None:
        theorem = " ".join((ROOT / "docs/COMPILER_THEOREM.md").read_text().split())
        self.assertIn(
            r"implements $L_d^{(n)}$ exactly, with the borrowed suffix bit restored and no additional sector-dependent phase.",
            theorem,
        )
        self.assertNotIn("restores every system qubit", theorem)

    def test_family_quantifiers_are_visible_on_main_routes(self) -> None:
        for relative in ("README.md", "REVIEW.md", "docs/COMPILER_THEOREM.md"):
            text = " ".join((ROOT / relative).read_text().split())
            self.assertIn("upper bounds hold for every parameter tuple", text, relative)
            self.assertIn("lower bounds hold in the worst case over the Hopf-frame family", text, relative)
            self.assertIn("uniformly in the clean-workspace budget", text, relative)

    def test_actual_software_identifiers_and_links_are_preserved(self) -> None:
        hopf = (ROOT / "docs/HOPF_INTERFACE.md").read_text()
        for identifier in KNOWN_CODE:
            self.assertIn("`" + identifier + "`", hopf)
        # A descriptive file link is just as valid as a code-formatted label.
        verification = (ROOT / "docs/VERIFICATION.md").read_text()
        self.assertIn(
            "[router and sparse-state simulator](../compiler_robust_hopf/router.py)",
            verification,
        )
        index = (ROOT / "compiler_robust_hopf/README.md").read_text()
        self.assertIn("`direct_real_frame(n, theta)`", index)
        self.assertIn("`real_frame_matrix(theta)`", index)

    def test_prose_has_no_recognized_math_disguised_as_code(self) -> None:
        failures = []
        for path in ROOT.rglob("*.md"):
            if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                continue
            for number, line in prose_lines(path.read_text()):
                # Existing table typography has its own regression coverage.
                if line.lstrip().startswith("|"):
                    continue
                for match in INLINE_CODE.finditer(PROTECTED_MATH.sub("", line)):
                    value = match.group(2)
                    # Long function names and their literal arguments are code.
                    name = value.split("(", 1)[0]
                    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{3,}", name) and name not in {
                        "sqrt", "Theta", "Omega", "lambda", "W_tilde", "cos"
                    }:
                        continue
                    if math_code(value):
                        failures.append(f"{path.relative_to(ROOT)}:{number}: {value}")
        self.assertEqual(failures, [])

    def test_inline_math_syntax_has_no_conversion_artifacts(self) -> None:
        failures = []
        for path in ROOT.rglob("*.md"):
            if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                continue
            for number, line in prose_lines(path.read_text()):
                without_code = INLINE_CODE.sub("", PROTECTED_MATH.sub(lambda m: "$" + m[1] + "$", line))
                if len(re.findall(r"(?<!\\)\$", without_code)) % 2:
                    failures.append(f"{path}:{number}: unpaired dollar delimiter")
                for body in INLINE_MATH.findall(without_code):
                    if re.search(r"(?<!\\)\b(?:Theta|Omega|sqrt|partial|lambda|theta|phi|psi|varphi|delta|epsilon|log|cos|sin)\b", body):
                        failures.append(f"{path}:{number}: bare function or Greek name {body}")
                    if re.search(r">=|<=|\*\*|_\(|\\\\[A-Za-z]", body):
                        failures.append(f"{path}:{number}: malformed conversion {body}")
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
