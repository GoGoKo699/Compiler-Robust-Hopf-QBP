from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

REPO = Path.cwd()
BASE_SHA = os.environ.get("BASE_SHA", "0e505324b5e5c2a3b6d41d3fe84abb27fcde0e91")
FINAL_BRANCH = os.environ.get("FINAL_BRANCH", "hyphen-inline-math-polish-20260906")
WORK = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "hopf-hyphen-inline-math"

FENCE = re.compile(r"^(?:\s*>\s*)*\s*(`{3,}|~{3,})")
# GitHub may leave a plain $...$ delimiter literal when it starts immediately
# after a word-forming hyphen.  Keep the visible compound unchanged but use the
# documented protected inline-math form: total-width-$`n`$.
PLAIN_HYPHEN_MATH = re.compile(
    r"(?P<hyphen>(?<=[A-Za-z0-9])[-‐‑‒–—])\$(?![`$])(?P<body>[^$\n]+?)(?<!\\)\$(?!\$)"
)


def run(*args: str, cwd: Path | None = None) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd or REPO,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(completed.stdout, end="")
    return completed.stdout


def rewrite_markdown(path: Path) -> list[dict[str, object]]:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    fence: str | None = None
    occurrences: list[dict[str, object]] = []
    rewritten: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            rewritten.append(line)
            continue

        if fence is not None:
            rewritten.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            body = match.group("body")
            occurrences.append(
                {
                    "line": line_number,
                    "source": match.group(0),
                    "body": body,
                }
            )
            return f'{match.group("hyphen")}$`{body}`$'

        rewritten.append(PLAIN_HYPHEN_MATH.sub(replace, line))

    updated = "".join(rewritten)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return occurrences


def write_regression_test(root: Path) -> None:
    test = r'''"""Regression test for word-hyphen-adjacent GitHub inline mathematics."""
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
'''
    (root / "tests" / "test_hyphen_inline_math.py").write_text(test, encoding="utf-8")


def main() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    run("git", "worktree", "add", "--detach", str(WORK), BASE_SHA)

    report: dict[str, list[dict[str, object]]] = {}
    for path in sorted(WORK.rglob("*.md")):
        if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
            continue
        occurrences = rewrite_markdown(path)
        if occurrences:
            report[str(path.relative_to(WORK))] = occurrences

    if not report:
        raise SystemExit("No word-hyphen-adjacent plain inline mathematics found.")

    write_regression_test(WORK)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"Rewrote {sum(len(items) for items in report.values())} occurrences in {len(report)} files.")

    run("python", "-m", "compileall", "-q", "compiler_robust_hopf", "scripts", "tests", "validate.py", cwd=WORK)
    run("python", "scripts/reviewer_walkthrough.py", cwd=WORK)
    run("python", "validate.py", cwd=WORK)
    run("python", "scripts/unified_resource_ledger.py", "--n", "12", cwd=WORK)
    run("python", "scripts/strict_zero_echo_ledger.py", "--n", "12", cwd=WORK)
    run("python", "scripts/check_upstream_sync.py", "--offline", cwd=WORK)

    mathjax = Path(os.environ["MATHJAX_ENTRY"])
    presentation_out = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "hopf-hyphen-presentation"
    run(
        "python",
        "scripts/check_presentation.py",
        "--mathjax",
        str(mathjax),
        "--output",
        str(presentation_out),
        cwd=WORK,
    )

    # Verify the final diff is intentionally narrow.
    changed = run("git", "status", "--short", cwd=WORK)
    allowed = {"tests/test_hyphen_inline_math.py", *report.keys()}
    observed = {
        line[3:]
        for line in changed.splitlines()
        if len(line) >= 4
    }
    if observed != allowed:
        raise SystemExit(
            f"Unexpected changed paths. observed={sorted(observed)} allowed={sorted(allowed)}"
        )

    run("git", "config", "user.name", "github-actions[bot]", cwd=WORK)
    run(
        "git",
        "config",
        "user.email",
        "41898282+github-actions[bot]@users.noreply.github.com",
        cwd=WORK,
    )
    run("git", "add", "--", *sorted(allowed), cwd=WORK)
    run("git", "diff", "--cached", "--check", cwd=WORK)
    run(
        "git",
        "commit",
        "-m",
        "Protect inline mathematics after word-forming hyphens",
        "-m",
        "Use GitHub's protected inline-math delimiters wherever a mathematical expression begins immediately after a word-forming hyphen. Preserve the visible compound, underlying TeX, scientific content, tables, diagrams, and display equations. Add a repository-wide regression test.",
        cwd=WORK,
    )
    head = run("git", "rev-parse", "HEAD", cwd=WORK).strip()
    run("git", "push", "--force", "origin", f"{head}:refs/heads/{FINAL_BRANCH}", cwd=WORK)
    print(f"FINAL_BRANCH={FINAL_BRANCH}")
    print(f"FINAL_COMMIT={head}")


if __name__ == "__main__":
    main()
