from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^\s*(```|~~~)")

SKIP_DIRS = {".git", ".venv", "__pycache__"}
SKIP_FILES = {
    "provenance/inline_math_candidates.txt",
}

PATH_SUFFIXES = (
    ".py",
    ".md",
    ".json",
    ".toml",
    ".yml",
    ".yaml",
    ".svg",
    ".txt",
    ".cff",
)

CODE_LITERALS = {
    "main",
    "Hopf-QBP",
    "Hopf-ansatz",
    "frame-safe",
    "state-column",
    "one-hot",
    "copy–uncopy",
    "route–operate–unroute",
    "X/CNOT/Toffoli",
    "CNOT/Fredkin",
    "Clifford+T",
    "FWHT",
    "UCG",
    "MCT",
    "QSP",
    "MIT",
    "PASS",
}

GREEK = {
    "theta": r"\theta",
    "phi": r"\phi",
    "psi": r"\psi",
    "varphi": r"\varphi",
    "lambda": r"\lambda",
    "alpha": r"\alpha",
    "beta": r"\beta",
    "chi": r"\chi",
    "xi": r"\xi",
    "epsilon": r"\varepsilon",
    "delta": r"\delta",
    "ell": r"\ell",
    "nabla": r"\nabla",
    "pi": r"\pi",
}

TEXT_SUBSCRIPTS = {
    "ph",
    "mag",
    "prep",
    "frame",
    "scalar",
    "grad",
    "direct",
    "routed",
    "UCG",
    "QSP",
    "bad",
    "safe",
    "matched",
    "ancilla",
    "suffix",
    "root",
    "target",
    "system",
    "work",
    "in",
    "out",
}

KNOWN_MATH_WORDS = {
    "Theta",
    "Omega",
    "sqrt",
    "partial",
    "lambda",
    "theta",
    "phi",
    "psi",
    "varphi",
    "alpha",
    "beta",
    "chi",
    "xi",
    "epsilon",
    "delta",
    "ell",
    "nabla",
    "pi",
    "diag",
    "exp",
    "log",
    "min",
    "max",
    "tensor",
    "xor",
}

SPECIAL = {
    "W_tilde": r"\widetilde W",
    "B_tilde_d": r"\widetilde B_d",
    "U_tilde": r"\widetilde U",
    "V_tilde": r"\widetilde V",
    "W_R": r"W_{\mathbb R}",
    "W_C": r"W_{\mathbb C}",
    "D_ph": r"D_{\mathrm{ph}}",
    "W_(C,mag)": r"W_{\mathbb C,\mathrm{mag}}",
    "W_C,mag": r"W_{\mathbb C,\mathrm{mag}}",
    "C_bad": r"C_{\mathrm{bad}}",
    "C_safe": r"C_{\mathrm{safe}}",
    "Q_bad": r"Q_{\mathrm{bad}}",
    "Q_perp": r"Q_{\perp}",
    "D_prep": r"D_{\mathrm{prep}}",
    "D_frame": r"D_{\mathrm{frame}}",
    "D_O": r"D_O",
    "S_grad": r"S_{\nabla}",
    "S_nabla": r"S_{\nabla}",
    "T_scalar": r"T_{\mathrm{scalar}}",
    "T_grad": r"T_{\mathrm{grad}}",
    "l_infinity": r"\ell_\infty",
    "l_2": r"\ell_2",
    "epsilon_infinity": r"\varepsilon_\infty",
    "sqrt(2)": r"\sqrt{2}",
}


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT).as_posix()
        if relative in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def looks_like_software(span: str) -> bool:
    stripped = span.strip()
    if stripped in CODE_LITERALS:
        return True
    if stripped.startswith(("http://", "https://", "arXiv:", "doi:")):
        return True
    if stripped.endswith(PATH_SUFFIXES) or "/" in stripped:
        return True
    if re.fullmatch(r"[0-9a-f]{7,40}", stripped):
        return True
    if re.fullmatch(r"v?\d+(?:\.\d+){1,3}(?:-[A-Za-z0-9.]+)?", stripped):
        return True
    if stripped.startswith(("python ", "pip ", "git ", "source ", "pytest ")):
        return True
    if "::" in stripped or stripped.startswith("--"):
        return True
    if "." in stripped and not re.search(r"\d\.\d", stripped):
        return True
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*(?:\([^)]*\))?", stripped):
        name = stripped.split("(", 1)[0]
        if "_" in name and name not in SPECIAL and name not in {
            "a_j",
            "e_j",
            "g_jj",
            "D_t",
            "F_t",
            "R_t",
            "L_d",
            "C_p",
            "T_h",
            "J_m",
            "P_d",
            "K_d",
            "S_E",
        }:
            return True
        if len(name) > 3 and name not in KNOWN_MATH_WORDS:
            return True
    return False


def looks_mathematical(span: str) -> bool:
    stripped = span.strip()
    if not stripped or looks_like_software(stripped):
        return False
    if re.search(r"\|[^`]*>|<[^`]*\|", stripped):
        return True
    if any(token in stripped for token in (">=", "<=", "=", "^", "**", "->", "=>")):
        return True
    if any(re.search(rf"\b{re.escape(word)}\b", stripped) for word in KNOWN_MATH_WORDS):
        return True
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9]+)?", stripped):
        return True
    if re.fullmatch(r"[A-Z]{1,3}\(\d+\)", stripped):
        return True
    if re.fullmatch(r"\([^)]*,[^)]*\)", stripped):
        return True
    if re.fullmatch(r"\[[^]]+\]", stripped) and any(ch.isdigit() for ch in stripped):
        return True
    if re.search(r"\d(?:[A-Za-z]|\*)|[A-Za-z]\d", stripped):
        return True
    if any(op in stripped for op in ("+", "-", "/", "*")):
        words = re.findall(r"[A-Za-z]+", stripped)
        if words and all(len(word) <= 8 or word in KNOWN_MATH_WORDS for word in words):
            return True
    if stripped in SPECIAL:
        return True
    return False


def convert_subscript_groups(text: str) -> str:
    # Convert the repository's ASCII convention x_(a,b) to x_{a,b}.
    pattern = re.compile(r"([A-Za-z\\]+)_\(([^()]*)\)")
    previous = None
    while previous != text:
        previous = text
        text = pattern.sub(lambda m: f"{m.group(1)}_{{{m.group(2)}}}", text)
    return text


def convert_kets_and_bras(text: str) -> str:
    text = re.sub(
        r"\|([^>|]+)>",
        lambda m: rf"\lvert {convert_inner(m.group(1))}\rangle",
        text,
    )
    text = re.sub(
        r"<([^<|]+)\|",
        lambda m: rf"\langle {convert_inner(m.group(1))}\rvert",
        text,
    )
    text = re.sub(
        r"\|([^|]+)\|",
        lambda m: rf"\lvert {convert_inner(m.group(1))}\rvert",
        text,
    )
    return text


def convert_functions(text: str) -> str:
    # Repeatedly convert innermost calls used by the repository's pseudo-math.
    function_map = {
        "sqrt": r"\sqrt",
        "Theta": r"\Theta",
        "Omega": r"\Omega",
        "O": "O",
        "log": r"\log",
        "min": r"\min",
        "max": r"\max",
        "diag": r"\mathrm{diag}",
        "exp": r"\exp",
    }
    call = re.compile(r"\b(Theta|Omega|sqrt|O|log|min|max|diag|exp)\(([^()]*)\)")
    previous = None
    while previous != text:
        previous = text

        def repl(match: re.Match[str]) -> str:
            name, arg = match.groups()
            converted = convert_inner(arg)
            command = function_map[name]
            if name == "sqrt":
                return rf"{command}{{{converted}}}"
            if name in {"Theta", "Omega", "O"}:
                return rf"{command}\!\left({converted}\right)"
            return rf"{command}\!\left({converted}\right)"

        text = call.sub(repl, text)
    return text


def convert_named_subscripts(text: str) -> str:
    text = text.replace("W_(C,mag)", r"W_{\mathbb C,\mathrm{mag}}")
    for original, replacement in sorted(SPECIAL.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"(?<![A-Za-z0-9]){re.escape(original)}(?![A-Za-z0-9])", replacement, text)
    text = re.sub(r"\b([A-Za-z])_R\b", lambda m: rf"{m.group(1)}_{{\mathbb R}}", text)
    text = re.sub(r"\b([A-Za-z])_C\b", lambda m: rf"{m.group(1)}_{{\mathbb C}}", text)
    text = re.sub(r"\b([A-Za-z])_perp\b", lambda m: rf"{m.group(1)}_{{\perp}}", text)
    for subscript in sorted(TEXT_SUBSCRIPTS, key=len, reverse=True):
        text = re.sub(
            rf"\b([A-Za-z])_{subscript}\b",
            lambda m, s=subscript: rf"{m.group(1)}_{{\mathrm{{{s}}}}}",
            text,
        )
    text = re.sub(r"\b([A-Za-z])_infinity\b", lambda m: rf"{m.group(1)}_\infty", text)
    return text


def convert_greek(text: str) -> str:
    for word, command in GREEK.items():
        text = re.sub(rf"(?<![A-Za-z\\]){word}(?![A-Za-z])", lambda _m, c=command: c, text)
    return text


def convert_common_fractions(text: str) -> str:
    replacements = (
        (r"2^n/(n+m)", r"\frac{2^n}{n+m}"),
        (r"N/(n+m)", r"\frac{N}{n+m}"),
        (r"2^n/n", r"\frac{2^n}{n}"),
        (r"N/n", r"\frac{N}{n}"),
        (r"2^s/s", r"\frac{2^s}{s}"),
        (r"2^d/(d+2)", r"\frac{2^d}{d+2}"),
        (r"n/\delta", r"\frac{n}{\delta}"),
    )
    for source, target in replacements:
        text = text.replace(source, target)
    return text


def convert_inner(text: str) -> str:
    text = text.strip()
    text = text.replace("**", "^")
    text = convert_named_subscripts(text)
    text = convert_subscript_groups(text)
    text = text.replace("^dagger", r"^{\dagger}")
    text = re.sub(r"\^\((-?[A-Za-z0-9+\-]+)\)", r"^{\1}", text)
    text = text.replace(">=", r"\geq ")
    text = text.replace("<=", r"\leq ")
    text = text.replace("!=", r"\neq ")
    text = text.replace("==", "=")
    text = text.replace("=>", r"\Longrightarrow ")
    text = text.replace("->", r"\mapsto ")
    text = re.sub(r"\btensor\b", r"\\otimes", text)
    text = re.sub(r"\bxor\b", r"\\oplus", text)
    text = text.replace("...", r"\ldots")
    text = convert_functions(text)
    text = convert_greek(text)
    text = convert_common_fractions(text)
    text = re.sub(r"(?<!\*)\*(?!\*)", r"\\cdot ", text)
    text = convert_kets_and_bras(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def convert_span(span: str) -> str:
    return f"${convert_inner(span)}$"


def transform_text(text: str) -> tuple[str, int]:
    output: list[str] = []
    changed = 0
    in_fence = False
    fence = ""

    for line in text.splitlines(keepends=True):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
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
            if not looks_mathematical(span):
                return match.group(0)
            changed += 1
            return convert_span(span)

        output.append(INLINE_CODE.sub(repl, line))

    return "".join(output), changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    changed_files: list[tuple[str, int]] = []
    for path in markdown_files():
        original = path.read_text(encoding="utf-8")
        transformed, count = transform_text(original)
        if not count:
            continue
        relative = path.relative_to(ROOT).as_posix()
        changed_files.append((relative, count))
        if not args.check:
            path.write_text(transformed, encoding="utf-8")

    for relative, count in changed_files:
        print(f"{relative}: {count} inline expression(s)")

    if args.check and changed_files:
        raise SystemExit(
            "inline mathematical code spans remain in "
            f"{len(changed_files)} Markdown file(s)"
        )

    print(
        f"{'would update' if args.check else 'updated'} "
        f"{len(changed_files)} Markdown file(s)"
    )


if __name__ == "__main__":
    main()
