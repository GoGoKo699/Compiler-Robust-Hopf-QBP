from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^\s*(```|~~~)")

SKIP_DIRS = {".git", ".venv", "__pycache__"}
SKIP_FILES = {"provenance/inline_math_candidates.txt"}
PATH_SUFFIXES = (
    ".py", ".md", ".json", ".toml", ".yml", ".yaml", ".svg", ".txt", ".cff"
)
CODE_LITERALS = {
    "main", "Hopf-QBP", "Hopf-ansatz", "frame-safe", "state-column",
    "one-hot", "copy–uncopy", "route–operate–unroute", "X/CNOT/Toffoli",
    "CNOT/Fredkin", "Clifford+T", "FWHT", "UCG", "MCT", "QSP", "MIT",
    "PASS", "README", "Markdown", "NumPy", "Python",
}
GREEK = {
    "theta": r"\theta", "phi": r"\phi", "psi": r"\psi",
    "varphi": r"\varphi", "lambda": r"\lambda", "alpha": r"\alpha",
    "beta": r"\beta", "chi": r"\chi", "xi": r"\xi",
    "epsilon": r"\varepsilon", "delta": r"\delta", "ell": r"\ell",
    "nabla": r"\nabla", "pi": r"\pi",
}
KNOWN_MATH_WORDS = set(GREEK) | {
    "Theta", "Omega", "sqrt", "partial", "diag", "exp", "log", "min",
    "max", "tensor", "xor",
}
TEXT_SUBSCRIPTS = {
    "ph", "mag", "prep", "frame", "scalar", "grad", "direct", "routed",
    "UCG", "QSP", "bad", "safe", "matched", "ancilla", "suffix", "root",
    "target", "system", "work", "in", "out",
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
    "C_bad": r"C_{\mathrm{bad}}",
    "C_safe": r"C_{\mathrm{safe}}",
    "Q_bad": r"Q_{\mathrm{bad}}",
    "Q_perp": r"Q_{\perp}",
    "D_prep": r"D_{\mathrm{prep}}",
    "D_frame": r"D_{\mathrm{frame}}",
    "S_grad": r"S_{\nabla}",
    "S_nabla": r"S_{\nabla}",
    "T_scalar": r"T_{\mathrm{scalar}}",
    "T_grad": r"T_{\mathrm{grad}}",
    "l_infinity": r"\ell_\infty",
    "l_2": r"\ell_2",
    "epsilon_infinity": r"\varepsilon_\infty",
}


def markdown_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*.md")
        if path.relative_to(ROOT).as_posix() not in SKIP_FILES
        and not any(part in SKIP_DIRS for part in path.parts)
    )


def identifier_head(span: str) -> str:
    return span.split("(", 1)[0]


def mathematical_identifier(name: str) -> bool:
    if name in SPECIAL or name in KNOWN_MATH_WORDS:
        return True
    if re.fullmatch(r"[A-Za-z]", name):
        return True
    if re.fullmatch(r"[A-Za-z]_[A-Za-z0-9]+", name):
        return True
    prefix = name.split("_", 1)[0]
    return prefix in GREEK or len(prefix) == 1


def looks_like_software(span: str) -> bool:
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
    named_argument = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)=(.+)", value)
    if named_argument and not mathematical_identifier(named_argument.group(1)):
        return True
    call = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*)(?:\([^)]*\))?", value)
    if call and not mathematical_identifier(call.group(1)):
        return True
    return False


def looks_mathematical(span: str) -> bool:
    value = span.strip()
    if not value or looks_like_software(value):
        return False
    if re.search(r"\|[^`]*>|<[^`]*\|", value):
        return True
    if any(token in value for token in (">=", "<=", "=", "^", "**", "->", "=>", "_(")):
        return True
    if re.search(r"[<>]", value) and not re.search(r"https?://", value):
        return True
    if any(re.search(rf"\b{re.escape(word)}\b", value) for word in KNOWN_MATH_WORDS):
        return True
    if value in SPECIAL:
        return True
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9]+)?", value):
        return True
    if re.fullmatch(r"(?:[A-Za-z]+_)?[A-Za-z](?:_[A-Za-z0-9]+)?\([^)]*\)", value):
        return mathematical_identifier(identifier_head(value))
    if re.fullmatch(r"[A-Z]{1,3}\(\d+\)", value):
        return True
    if re.fullmatch(r"\([^)]*,[^)]*\)", value):
        return True
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9]+)?(?:,[A-Za-z](?:_[A-Za-z0-9]+)?)+", value):
        return True
    if re.fullmatch(r"\[[^]]+\]", value) and any(ch.isdigit() for ch in value):
        return True
    if re.search(r"\d(?:[A-Za-z]|\*)|[A-Za-z]\d", value):
        return True
    if any(op in value for op in ("+", "-", "/", "*")):
        words = re.findall(r"[A-Za-z]+", value)
        if words and all(len(word) <= 8 or word in KNOWN_MATH_WORDS for word in words):
            return True
    return False


def replace_literal(text: str, source: str, target: str) -> str:
    return re.sub(
        rf"(?<![A-Za-z0-9]){re.escape(source)}(?![A-Za-z0-9])",
        lambda _match, replacement=target: replacement,
        text,
    )


def convert_named_symbols(text: str) -> str:
    for source, target in sorted(SPECIAL.items(), key=lambda item: -len(item[0])):
        text = replace_literal(text, source, target)
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


def convert_grouped_subscripts(text: str) -> str:
    pattern = re.compile(r"([A-Za-z\\]+)_\(([^()]*)\)")
    previous = None
    while text != previous:
        previous = text
        text = pattern.sub(lambda m: f"{m.group(1)}_{{{m.group(2)}}}", text)
    return text


def convert_greek(text: str) -> str:
    for word, command in GREEK.items():
        text = re.sub(
            rf"(?<![A-Za-z\\]){word}(?![A-Za-z])",
            lambda _match, replacement=command: replacement,
            text,
        )
    text = re.sub(r"(?<![A-Za-z\\])partial(?![A-Za-z])", lambda _m: r"\partial", text)
    return text


def convert_functions(text: str) -> str:
    commands = {
        "sqrt": r"\sqrt", "Theta": r"\Theta", "Omega": r"\Omega",
        "O": "O", "log": r"\log", "min": r"\min", "max": r"\max",
        "diag": r"\mathrm{diag}", "exp": r"\exp",
    }
    call = re.compile(r"\b(Theta|Omega|sqrt|O|log|min|max|diag|exp)\(([^()]*)\)")
    previous = None
    while text != previous:
        previous = text

        def repl(match: re.Match[str]) -> str:
            name, argument = match.groups()
            converted = convert_inner(argument)
            command = commands[name]
            if name == "sqrt":
                return rf"{command}{{{converted}}}"
            return rf"{command}\!\left({converted}\right)"

        text = call.sub(repl, text)
    return text


def convert_kets_bras_norms(text: str) -> str:
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


def convert_common_fractions(text: str) -> str:
    for source, target in (
        (r"2^n/(n+m)", r"\frac{2^n}{n+m}"),
        (r"N/(n+m)", r"\frac{N}{n+m}"),
        (r"2^n/n", r"\frac{2^n}{n}"),
        (r"N/n", r"\frac{N}{n}"),
        (r"2^s/s", r"\frac{2^s}{s}"),
        (r"2^d/(d+2)", r"\frac{2^d}{d+2}"),
        (r"n/\delta", r"\frac{n}{\delta}"),
    ):
        text = text.replace(source, target)
    return text


def convert_inner(raw: str) -> str:
    text = raw.strip().replace("**", "^")
    text = convert_named_symbols(text)
    text = convert_grouped_subscripts(text)
    text = convert_kets_bras_norms(text)
    text = text.replace("^dagger", r"^{\dagger}")
    text = re.sub(r"\^\((-?[A-Za-z0-9+\-]+)\)", r"^{\1}", text)
    text = text.replace(">=", r"\geq ")
    text = text.replace("<=", r"\leq ")
    text = text.replace("!=", r"\neq ")
    text = text.replace("==", "=")
    text = text.replace("=>", r"\Longrightarrow ")
    text = text.replace("->", r"\mapsto ")
    text = re.sub(r"\btensor\b", lambda _m: r"\otimes", text)
    text = re.sub(r"\bxor\b", lambda _m: r"\oplus", text)
    text = text.replace("...", r"\ldots")
    text = convert_functions(text)
    text = convert_greek(text)
    text = convert_common_fractions(text)
    text = re.sub(r"(?<!\*)\*(?!\*)", lambda _m: r"\cdot ", text)
    text = text.replace("B2^s", r"B\,2^s")
    return re.sub(r"\s+", " ", text).strip()


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
            if not looks_mathematical(span):
                return match.group(0)
            changed += 1
            return f"${convert_inner(span)}$"

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
        if count == 0:
            continue
        relative = path.relative_to(ROOT).as_posix()
        changed_files.append((relative, count))
        if not args.check:
            path.write_text(transformed, encoding="utf-8")

    for relative, count in changed_files:
        print(f"{relative}: {count} inline expression(s)")
    if args.check and changed_files:
        raise SystemExit(
            f"inline mathematical code spans remain in {len(changed_files)} Markdown file(s)"
        )
    print(f"{'would update' if args.check else 'updated'} {len(changed_files)} Markdown file(s)")


if __name__ == "__main__":
    main()
