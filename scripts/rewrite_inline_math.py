#!/usr/bin/env python3
"""Replace ASCII pseudo-mathematics in prose code spans by inline LaTeX.

The rewrite is deliberately limited to the scientific Markdown pages listed
below. Fenced code blocks, Markdown tables, filenames, repository names,
software identifiers, and public API identifiers remain in code font.
"""

from __future__ import annotations

import re
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
SYMBOL_TUPLE = re.compile(
    r"^\([A-Za-z](?:_[A-Za-z0-9]+)?(?:,[A-Za-z](?:_[A-Za-z0-9]+)?)+\)$"
)
MATH_WORD = re.compile(
    r"(?:Theta|Omega|sqrt|partial|lambda|theta|phi|psi|alpha|beta|chi|xi|"
    r"epsilon|delta|nabla|mathrm|mathbb|lvert|rangle|varphi)"
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
    "Hopf-QBP",
    "Hopf-QBP/main",
}

SNAKE_CASE_IDENTIFIER = re.compile(
    r"^[a-z][a-z0-9]+(?:_[a-z0-9]+)+(?:\([^`]*\))?$"
)
SNAKE_CASE_EXPRESSION = re.compile(
    r"^[a-z][a-z0-9]+(?:_[a-z0-9]+)+(?:\*\*\d+|\[[^`]*\])$"
)
CAMEL_CASE_IDENTIFIER = re.compile(r"^[A-Z][A-Za-z0-9]+(?:\([^`]*\))?$")
HEX_SHA = re.compile(r"^[0-9a-f]{7,40}$")
VERSION = re.compile(r"^\d+(?:\.\d+){1,3}(?:-[A-Za-z0-9.]+)?$")
HYPHENATED_IDENTIFIER = re.compile(
    r"^[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+(?:/main)?$"
)

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
    "varphi",
)

GREEK = {
    "alpha": r"\alpha",
    "beta": r"\beta",
    "chi": r"\chi",
    "delta": r"\delta",
    "epsilon": r"\varepsilon",
    "lambda": r"\lambda",
    "phi": r"\phi",
    "pi": r"\pi",
    "psi": r"\psi",
    "theta": r"\theta",
    "varphi": r"\varphi",
    "xi": r"\xi",
}

SPECIAL_SYMBOLS = {
    "W_(C,mag)": r"W_{\mathbb C,\mathrm{mag}}",
    "W_R": r"W_{\mathbb R}",
    "D_ph": r"D_{\mathrm{ph}}",
    "W_tilde": r"\widetilde W",
    "U_tilde": r"\widetilde U",
    "V_tilde": r"\widetilde V",
    "B_tilde_d": r"\widetilde B_d",
    "D_prep": r"D_{\mathrm{prep}}",
    "D_frame": r"D_{\mathrm{frame}}",
    "S_grad": r"S_{\mathrm{grad}}",
    "C_bad": r"C_{\mathrm{bad}}",
    "C_safe": r"C_{\mathrm{safe}}",
    "Q_bad": r"Q_{\mathrm{bad}}",
    "Q_perp": r"Q_{\perp}",
    "epsilon_infinity": r"\varepsilon_{\infty}",
    "l_infinity": r"\ell_{\infty}",
    "l_2": r"\ell_2",
}


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
    if HYPHENATED_IDENTIFIER.fullmatch(span):
        return True
    if SNAKE_CASE_EXPRESSION.fullmatch(span):
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
    if SINGLE_MATH_SYMBOL.fullmatch(span) or SYMBOL_TUPLE.fullmatch(span):
        return True
    if MATH_WORD.search(span) or MATH_EXPRESSION.search(span):
        return True
    if span.startswith(("[0,", "(", "{")) and any(
        token in span for token in ("pi", "theta", "phi", "n", "m", "N")
    ):
        return True
    return False


def regex_literal_sub(pattern: str, replacement: str, text: str) -> str:
    """Use a callable so LaTeX backslashes are never parsed as re templates."""
    return re.sub(pattern, lambda _match: replacement, text)


def replace_kets(text: str) -> str:
    def ket(match: re.Match[str]) -> str:
        label = convert_atoms(match.group(1))
        return rf"\lvert {label}\rangle"

    return re.sub(r"\|([^|>]+)>", ket, text)


def convert_atoms(text: str) -> str:
    for source, target in sorted(SPECIAL_SYMBOLS.items(), key=lambda item: -len(item[0])):
        text = text.replace(source, target)

    text = text.replace("**", "^")
    text = re.sub(r"\^\(([^()]*)\)", r"^{\1}", text)
    text = re.sub(r"_\(([^()]*)\)", r"_{\1}", text)
    text = text.replace("^dagger", r"^{\dagger}")

    for source, target in GREEK.items():
        pattern = rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])"
        text = regex_literal_sub(pattern, target, text)

    text = regex_literal_sub(r"(?<![A-Za-z])partial(?=_)", r"\partial", text)
    text = regex_literal_sub(r"(?<![A-Za-z])nabla(?![A-Za-z])", r"\nabla", text)

    text = text.replace("_infinity", r"_{\infty}")
    text = text.replace("_matched", r"_{\mathrm{matched}}")
    text = text.replace("_scalar", r"_{\mathrm{scalar}}")
    text = text.replace("_grad", r"_{\mathrm{grad}}")
    text = text.replace("_prep", r"_{\mathrm{prep}}")
    text = text.replace("_frame", r"_{\mathrm{frame}}")
    text = text.replace("_ph", r"_{\mathrm{ph}}")
    text = text.replace("_mag", r"_{\mathrm{mag}}")

    text = re.sub(
        r"sqrt\(([^()]*)\)",
        lambda match: rf"\sqrt{{{match.group(1)}}}",
        text,
    )
    text = regex_literal_sub(r"(?<![A-Za-z])Theta\(", r"\Theta(", text)
    text = regex_literal_sub(r"(?<![A-Za-z])Omega\(", r"\Omega(", text)
    text = regex_literal_sub(r"(?<![A-Za-z])log(?=[ (])", r"\log", text)
    text = regex_literal_sub(r"(?<![A-Za-z])min(?=[{(])", r"\min", text)
    text = regex_literal_sub(r"(?<![A-Za-z])max(?=[{(])", r"\max", text)
    text = regex_literal_sub(r"(?<![A-Za-z])diag(?=[{(])", r"\mathrm{diag}", text)

    text = text.replace(">=", r"\geq")
    text = text.replace("<=", r"\leq")
    text = text.replace("...", r"\ldots")
    text = text.replace(" tensor ", r"\otimes ")

    text = re.sub(
        r"(?<![A-Za-z])([A-Za-z0-9{}^]+)/(\([^()]+\))",
        lambda match: rf"\frac{{{match.group(1)}}}{{{match.group(2)[1:-1]}}}",
        text,
    )
    text = re.sub(
        r"(?<![A-Za-z])([A-Za-z0-9{}^]+)/([A-Za-z0-9{}^]+)",
        lambda match: rf"\frac{{{match.group(1)}}}{{{match.group(2)}}}",
        text,
    )

    text = re.sub(
        r"(?<![A-Za-z])1/2(?![0-9])",
        lambda _match: r"\tfrac12",
        text,
    )
    text = re.sub(
        r"(?<![A-Za-z])1/4(?![0-9])",
        lambda _match: r"\tfrac14",
        text,
    )

    text = re.sub(
        r"([A-Za-z}])2\^",
        lambda match: f"{match.group(1)}\\,2^",
        text,
    )
    text = re.sub(
        r"2\^([A-Za-z])([A-Za-z])\b",
        lambda match: f"2^{match.group(1)}\\,{match.group(2)}",
        text,
    )

    return text


def to_latex(span: str) -> str:
    text = replace_kets(span)
    text = convert_atoms(text)

    # A vertical-bar pair without a ket delimiter denotes an absolute value or
    # bit-string length in the source notation.
    text = re.sub(
        r"\|([^|]+)\|",
        lambda match: rf"\lvert {match.group(1)}\rvert",
        text,
    )

    text = text.replace(" xor ", r"\oplus ")
    text = re.sub(r"\s+", " ", text).strip()
    return f"${text}$"


def rewrite_page(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines: list[str] = []
    in_fence = False

    for line in original.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            lines.append(line)
            continue
        if in_fence or is_table_line(line):
            lines.append(line)
            continue

        def replacement(match: re.Match[str]) -> str:
            span = match.group(1)
            if not looks_mathematical(span):
                return match.group(0)
            return to_latex(span)

        lines.append(INLINE_CODE.sub(replacement, line))

    updated = "".join(lines)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed: list[str] = []
    for relative in SCIENTIFIC_MARKDOWN:
        path = ROOT / relative
        if rewrite_page(path):
            changed.append(relative)

    print(f"Rewrote {len(changed)} Markdown files.")
    for relative in changed:
        print(relative)


if __name__ == "__main__":
    main()
