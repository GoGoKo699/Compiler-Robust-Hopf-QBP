from __future__ import annotations

import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

PRIMARY_PAGES = (
    "README.md",
    "REVIEW.md",
    "docs/README.md",
    "docs/HOPF_INTERFACE.md",
    "docs/COMPILER_THEOREM.md",
    "docs/FAULT_TOLERANT_COMPILER.md",
    "docs/QBP_APPROXIMATION.md",
    "docs/QBP_CONSEQUENCE.md",
    "docs/VERIFICATION.md",
    "docs/SOURCE_MAP.md",
    "docs/RELATED_WORK.md",
    "docs/INDEPENDENT_REVIEW_GUIDE.md",
    "docs/RESEARCH_STATUS.md",
    "docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md",
    "docs/STRICT_ZERO_ECHO_AUDIT.md",
    "docs/CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md",
    "compiler_robust_hopf/README.md",
    "tests/README.md",
    "scripts/README.md",
    "assets/README.md",
    "provenance/README.md",
    "manuscript/README.md",
    "research/README.md",
    "research/CONSTANT_CLEAN_ENDPOINT.md",
    "research/CONSTANT_CLEAN_PROGRESS.md",
    "research/constant_clean/README.md",
    "research/constant_clean/GLOBAL_BLOCK_FOLLOWUP.md",
    "research/constant_clean/JOINT_CLOCK_FOLLOWUP.md",
    "research/constant_clean/DIRTY_RETURN_LOWER_BOUND_FOLLOWUP.md",
    "research/constant_clean/MODULAR_LOOKUP_FOLLOWUP.md",
    "research/constant_clean/ENDPOINT_LITERATURE_FOLLOWUP.md",
    "research/constant_clean/IDENTICAL_PHASE_BATCHING.md",
    "research/constant_clean/OPERATOR_SOURCE_COMPILER.md",
)

TABLE_MATH_PAGES = (
    "README.md",
    "REVIEW.md",
    "docs/HOPF_INTERFACE.md",
    "docs/COMPILER_THEOREM.md",
    "docs/FAULT_TOLERANT_COMPILER.md",
    "docs/QBP_APPROXIMATION.md",
    "docs/QBP_CONSEQUENCE.md",
    "docs/END_TO_END_QBP.md",
    "docs/UNIFIED_YUAN_ZHANG_COMPILER.md",
    "docs/CLAIM_SUPPORT.md",
    "docs/SOURCE_MAP.md",
    "docs/RESEARCH_STATUS.md",
    "docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md",
    "docs/STRICT_ZERO_ECHO_AUDIT.md",
    "docs/CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md",
)

DIAGRAMS = (
    "assets/state-vs-frame.svg",
    "assets/two-qubit-obstruction.svg",
    "assets/strict-zero-echo.svg",
    "assets/tree-cut-routing.svg",
    "assets/literature-lineage.svg",
)

PROCESS_PHRASES = (
    "PR #",
    "Issue #",
    "pull request",
    "merge-ref",
    "all-workspace-unified-final",
    "reviewer-narrative-redesign",
    "peer-review-revision-2026-09",
    "compiler-reader-refurnishing-2026-09",
)

MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_IMAGE = re.compile(r"<img\s+[^>]*src=\"([^\"]+)\"", re.IGNORECASE)
INLINE_CODE = re.compile(r"`([^`\n]+)`")
PROTECTED_INLINE_MATH = re.compile(r"\$`[^`\n]+`\$")
MATH_FUNCTION_CODE = re.compile(
    r"(?<![A-Za-z])(?:Theta|Omega|sqrt|partial|lambda|min|max|diag|O)\s*[(_]"
)
KET_CODE = re.compile(r"\|[^`]*>")
SINGLE_SYMBOL_CODE = re.compile(r"^[A-Za-z](?:_[A-Za-z0-9]+)?$")
GROUP_SYMBOL_CODE = re.compile(r"^[A-Z]{1,3}\(\d+\)$")
ARITHMETIC_CODE = re.compile(r"^[0-9A-Za-z_{}(), ]*[+*/-][0-9A-Za-z_{}(), +*/-]*$")


def local_target(page: Path, raw_target: str) -> Path | None:
    target = unquote(raw_target.strip())
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    return (page.parent / target).resolve()


def compact(text: str) -> str:
    return " ".join(text.split())


def markdown_table_body_line(line: str) -> bool:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return False
    return bool(stripped.strip("|: -"))


def code_span_looks_mathematical(span: str) -> bool:
    if any(token in span for token in ("<=", ">=", "=", "^", "**")):
        return True
    if MATH_FUNCTION_CODE.search(span) or KET_CODE.search(span):
        return True
    if "pi/" in span or SINGLE_SYMBOL_CODE.fullmatch(span):
        return True
    if GROUP_SYMBOL_CODE.fullmatch(span):
        return True
    if ARITHMETIC_CODE.fullmatch(span):
        words = re.findall(r"[A-Za-z]+", span)
        return bool(words) and all(len(word) <= 3 for word in words)
    return False


class ReviewerNarrativeTests(unittest.TestCase):
    def test_primary_pages_exist_and_have_no_workflow_language(self) -> None:
        for relative in PRIMARY_PAGES:
            path = ROOT / relative
            self.assertTrue(path.is_file(), msg=relative)
            text = path.read_text(encoding="utf-8")
            for phrase in PROCESS_PHRASES:
                self.assertNotIn(phrase, text, msg=f"{phrase!r} in {relative}")

    def test_primary_pages_use_github_safe_math_commands(self) -> None:
        for relative in PRIMARY_PAGES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn(
                "\\operatorname",
                text,
                msg=f"unsupported GitHub math command in {relative}",
            )

    def test_markdown_tables_render_mathematics_instead_of_code(self) -> None:
        offenders: list[str] = []
        for relative in TABLE_MATH_PAGES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for line_number, line in enumerate(text.splitlines(), start=1):
                if not markdown_table_body_line(line):
                    continue
                line_without_protected_math = PROTECTED_INLINE_MATH.sub("", line)
                for span in INLINE_CODE.findall(line_without_protected_math):
                    if code_span_looks_mathematical(span):
                        offenders.append(f"{relative}:{line_number}: `{span}`")

        self.assertFalse(
            offenders,
            msg="Math-like code spans remain in Markdown tables:\n"
            + "\n".join(offenders),
        )

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(r"$U\lvert 0^n\rangle$", readme)
        hopf = (ROOT / "docs" / "HOPF_INTERFACE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            r"$W_{\mathbb C,\mathrm{mag}}=D_{\mathrm{ph}}W_{\mathbb R}$",
            hopf,
        )
        accounting = (ROOT / "docs" / "END_TO_END_QBP.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(r"$\ell_\infty$", accounting)

    def test_landing_page_starts_from_the_prescribed_completion(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        opening = compact(readme[:2500]).lower()
        self.assertLess(len(readme), 15_000)
        self.assertIn("# optimal compilation of hopf differential frames", opening)
        self.assertIn("prescribed unitary completion", opening)
        self.assertIn("exact state preparation normally specifies one initialized input", opening)
        self.assertIn("this repository asks whether the prescribed hopf completion", opening)
        self.assertNotIn("yuan and zhang determine", opening)

    def test_complete_narrative_follows_the_compiler_first_chain(self) -> None:
        review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
        self.assertGreater(len(review), 25_000)
        headings = (
            "## 0. Problem and results",
            "## 1. Why the prescribed completion matters",
            "## 2. The Hopf operator seen by a compiler",
            "## 3. Exact compiler toolkit",
            "## 4. Strict zero workspace",
            "## 5. Small positive workspace",
            "## 6. Larger workspace: cut, route, and parallelize",
            "## 7. Matching lower bounds",
            "## 8. Phase-dressed complex magnitude frame",
            "## 9. Finite precision and fault-tolerant compilation",
            "## 10. Consequence for quantum backpropagation",
        )
        positions = [review.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("### 1.2 A complete two-qubit obstruction", review)
        self.assertIn("> **Proof checkpoint.**", review)
        self.assertNotIn("What should be checked here?", review)

    def test_relation_to_prior_work_is_precise_and_generous(self) -> None:
        pages = {
            relative: (ROOT / relative).read_text(encoding="utf-8")
            for relative in (
                "README.md",
                "REVIEW.md",
                "docs/COMPILER_THEOREM.md",
                "docs/SOURCE_MAP.md",
                "docs/RELATED_WORK.md",
            )
        }
        combined = " ".join(pages.values())
        normalized = compact(combined).lower()
        self.assertIn("can be adapted", normalized)
        self.assertIn("prescribed", normalized)
        self.assertNotIn("does not provide", normalized)
        self.assertNotIn("failed to provide", normalized)
        self.assertIn("historical predecessor", normalized)
        self.assertIn("p. yuan and s. zhang", normalized)
        self.assertIn("x. sun", pages["docs/RELATED_WORK.md"].lower())

    def test_scientific_corrections_remain_visible(self) -> None:
        files = {
            relative: (ROOT / relative).read_text(encoding="utf-8")
            for relative in (
                "README.md",
                "REVIEW.md",
                "docs/HOPF_INTERFACE.md",
                "docs/COMPILER_THEOREM.md",
                "docs/QBP_CONSEQUENCE.md",
                "docs/VERIFICATION.md",
                "docs/SOURCE_MAP.md",
            )
        }
        combined = " ".join(files.values())
        normalized = compact(combined).lower()
        self.assertIn("oriented incoming amplitude", normalized)
        self.assertIn("chart-selected orthogonal continuation", normalized)
        self.assertIn("complex magnitude frame", normalized)
        self.assertIn("matched", normalized)
        self.assertIn("raw hopf-coordinate gradient", normalized)
        self.assertIn("router.py", combined)
        self.assertIn("arxiv:2202.11302v2", normalized)
        self.assertIn("arxiv:2202.11302v3", normalized)

        theorem = files["docs/COMPILER_THEOREM.md"]
        theorem_compact = compact(theorem)
        self.assertIn("fixed-width controlled Givens rotations", theorem_compact)
        self.assertIn("C-B", theorem)
        self.assertIn("If $s=1$", theorem)

        verification = files["docs/VERIFICATION.md"]
        self.assertIn("explicit CNOT-fanout and Fredkin layers", verification)
        self.assertIn("prefix–suffix-entangled inputs", verification)
        self.assertIn("Evidence levels", verification)

        qbp = files["docs/QBP_CONSEQUENCE.md"]
        self.assertIn("T_{\\mathrm{scalar}}^{\\mathrm{matched}}", qbp)
        self.assertIn("T_{\\mathrm{grad}}^{\\mathrm{matched}}", qbp)

    def test_clean_room_review_matches_the_active_theorem(self) -> None:
        clean_room = (
            ROOT / "docs" / "CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md"
        ).read_text(encoding="utf-8")
        self.assertIn("S_{\\mathbb C,\\mathrm{mag}}", clean_room)
        self.assertIn("D_{\\mathbb C,\\mathrm{mag}}", clean_room)
        self.assertIn("\\mathrm{diag}", clean_room)
        self.assertIn("router.py", clean_room)
        self.assertNotIn("S_{\\mathbb C}(n,m)", clean_room)
        self.assertNotIn("D_{\\mathbb C}(n,m)", clean_room)

    def test_primary_local_links_resolve(self) -> None:
        for relative in PRIMARY_PAGES:
            page = ROOT / relative
            text = page.read_text(encoding="utf-8")
            targets = MARKDOWN_LINK.findall(text) + HTML_IMAGE.findall(text)
            for raw_target in targets:
                target = local_target(page, raw_target)
                if target is None:
                    continue
                self.assertTrue(
                    target.exists(),
                    msg=f"broken link in {relative}: {raw_target}",
                )

    def test_svg_diagrams_are_well_formed_and_accessible(self) -> None:
        namespace = "{http://www.w3.org/2000/svg}"
        for relative in DIAGRAMS:
            path = ROOT / relative
            self.assertTrue(path.is_file(), msg=relative)
            root = ET.parse(path).getroot()
            self.assertTrue(root.tag.endswith("svg"), msg=relative)
            self.assertIsNotNone(root.find(f"{namespace}title"), msg=relative)
            self.assertIsNotNone(root.find(f"{namespace}desc"), msg=relative)
            self.assertIn("viewBox", root.attrib, msg=relative)

        state_figure = (ROOT / DIAGRAMS[0]).read_text(encoding="utf-8")
        self.assertIn("prescribed unitary completion", state_figure)
        lineage_figure = (ROOT / DIAGRAMS[-1]).read_text(encoding="utf-8")
        self.assertIn("All-workspace frontier", lineage_figure)
        self.assertNotIn("Sun et al.", lineage_figure)

    def test_navigation_covers_the_three_reading_passes(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for target in (
            "REVIEW.md",
            "docs/HOPF_INTERFACE.md",
            "docs/COMPILER_THEOREM.md",
            "docs/QBP_CONSEQUENCE.md",
            "docs/VERIFICATION.md",
            "docs/SOURCE_MAP.md",
            "docs/RELATED_WORK.md",
        ):
            self.assertIn(target, readme)

        documentation_index = (ROOT / "docs" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Pass I: orient the synthesis question", documentation_index)
        self.assertIn("Pass II: inspect the proof by component", documentation_index)
        self.assertIn("Pass III: inspect evidence and provenance", documentation_index)
        for target in (
            "../compiler_robust_hopf/README.md",
            "../tests/README.md",
            "../scripts/README.md",
            "../assets/README.md",
            "../provenance/README.md",
        ):
            self.assertIn(target, documentation_index)

        verification = (ROOT / "docs" / "VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("PROOF_AUDIT.md", verification)
        self.assertIn("STRICT_ZERO_ECHO_AUDIT.md", verification)
        self.assertIn("CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md", verification)

    def test_router_and_source_versions_are_machine_checkable(self) -> None:
        self.assertTrue((ROOT / "compiler_robust_hopf" / "router.py").is_file())
        self.assertTrue((ROOT / "tests" / "test_router.py").is_file())

        upstream = json.loads(
            (ROOT / "provenance" / "upstream.json").read_text(encoding="utf-8")
        )
        current = next(
            record
            for record in upstream["upstreams"]
            if record["repository"] == "GoGoKo699/Hopf-QBP"
            and record["tracked_branch"] == "main"
        )
        self.assertEqual(
            current["tracked_commit"],
            "a9885317cf998a7df87ca07ba86e3bd4f0f419ef",
        )

        literature = json.loads(
            (ROOT / "provenance" / "literature.json").read_text(
                encoding="utf-8"
            )
        )
        active = literature["active_compiler_framework"]
        self.assertEqual(active["published_eprint"], "arXiv:2202.11302v2")
        self.assertEqual(active["checked_arxiv_revision"], "arXiv:2202.11302v3")


if __name__ == "__main__":
    unittest.main()
