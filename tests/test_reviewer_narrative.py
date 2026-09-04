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
    "docs/READING_GUIDE.md",
    "docs/HOPF_INTERFACE.md",
    "docs/COMPILER_THEOREM.md",
    "docs/QBP_CONSEQUENCE.md",
    "docs/VERIFICATION.md",
    "docs/SOURCE_MAP.md",
    "docs/RELATED_WORK.md",
)

COMPATIBILITY_PAGES = (
    "docs/INDEPENDENT_REVIEW_GUIDE.md",
)

DIAGRAMS = (
    "assets/problem-hierarchy.svg",
    "assets/frontier-match.svg",
    "assets/proof-map.svg",
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
    "compiler-specialist-reader-route-2026-09",
)

PERSONALIZATION_PHRASES = (
    "for yuan",
    "tailored for",
    "intended reviewer",
    "single reviewer",
)

MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_IMAGE = re.compile(r"<img\s+[^>]*src=\"([^\"]+)\"", re.IGNORECASE)


def local_target(page: Path, raw_target: str) -> Path | None:
    target = unquote(raw_target.strip())
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    return (page.parent / target).resolve()


class ReaderNarrativeTests(unittest.TestCase):
    def test_primary_pages_are_process_free_and_impersonal(self) -> None:
        for relative in PRIMARY_PAGES + COMPATIBILITY_PAGES:
            path = ROOT / relative
            self.assertTrue(path.is_file(), msg=relative)
            text = path.read_text(encoding="utf-8")
            lower = text.lower()
            for phrase in PROCESS_PHRASES:
                self.assertNotIn(phrase, text, msg=f"{phrase!r} in {relative}")
            for phrase in PERSONALIZATION_PHRASES:
                self.assertNotIn(phrase, lower, msg=f"{phrase!r} in {relative}")

    def test_primary_pages_use_the_selected_writing_conventions(self) -> None:
        for relative in PRIMARY_PAGES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn(
                "\\operatorname",
                text,
                msg=f"unsupported GitHub math command in {relative}",
            )
            self.assertNotIn("—", text, msg=f"em dash in {relative}")
            self.assertNotRegex(
                text,
                re.compile(r"\b[Yy]ou\b"),
                msg=f"direct second-person address in {relative}",
            )

    def test_landing_page_starts_from_the_synthesis_hierarchy(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertLess(len(readme), 16_000)
        self.assertIn("# Optimal Compilation of Hopf Differential Frames", readme)
        self.assertIn("## Main theorem", readme)
        self.assertIn("## Where this problem sits", readme)
        self.assertIn("Quantum state preparation", readme)
        self.assertIn("Controlled state preparation", readme)
        self.assertIn("General unitary synthesis", readme)
        self.assertIn("structured complete unitary", readme)
        self.assertIn("assets/problem-hierarchy.svg", readme)
        self.assertIn("assets/frontier-match.svg", readme)
        self.assertIn("assets/proof-map.svg", readme)

    def test_complete_note_has_the_intended_question_chain(self) -> None:
        review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
        self.assertGreater(len(review), 30_000)
        headings = (
            "## 1. A structured unitary-completion problem",
            "## 2. Minimal Hopf interface",
            "## 3. Why one correct state column is insufficient",
            "## 4. Exact circuit framework",
            "## 5. One compiler with three schedules",
            "## 6. Schedule Z: strict zero workspace",
            "## 7. Schedule P1: small positive workspace",
            "## 8. Schedule P2: larger workspace",
            "## 9. Matching lower bounds",
            "## 10. Phase-dressed complex magnitude frame",
            "## 11. Consequence for Hopf quantum backpropagation",
            "## 12. Verification and evidence levels",
        )
        positions = [review.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("### What has been established", review)
        self.assertIn("### Executable counterpart", review)
        self.assertIn("Technical checkpoint", review)

    def test_state_preparation_line_is_presented_generously_and_precisely(self) -> None:
        related = (ROOT / "docs" / "RELATED_WORK.md").read_text(encoding="utf-8")
        source = (ROOT / "docs" / "SOURCE_MAP.md").read_text(encoding="utf-8")
        combined = related + "\n" + source
        self.assertIn("one coherent compiler line", combined)
        self.assertIn("can be adapted", combined)
        self.assertIn("historical predecessor", combined)
        self.assertIn("P. Yuan and S. Zhang", combined)
        self.assertIn("X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang", combined)
        self.assertNotIn("fails to provide", combined.lower())
        self.assertNotIn("does not provide", combined.lower())

    def test_scientific_corrections_remain_visible(self) -> None:
        files = {
            relative: (ROOT / relative).read_text(encoding="utf-8")
            for relative in PRIMARY_PAGES
        }
        combined = " ".join(files.values())
        normalized = " ".join(combined.split()).lower()
        self.assertIn("oriented incoming amplitude", normalized)
        self.assertIn("chart-selected orthogonal continuation", normalized)
        self.assertIn("phase-dressed complex magnitude frame", normalized)
        self.assertIn("matched scalar and gradient programs", normalized)
        self.assertIn("raw hopf-coordinate gradient", normalized)
        self.assertIn("router.py", combined)
        self.assertIn("arxiv:2202.11302v2", normalized)
        self.assertIn("arxiv:2202.11302v3", normalized)

        theorem = files["docs/COMPILER_THEOREM.md"]
        self.assertIn("fixed-width controlled Givens", theorem)
        self.assertIn("C-B", theorem)
        self.assertIn("If `s=1`", theorem)
        self.assertIn("2^{n+1}=2N", theorem)

        qbp = files["docs/QBP_CONSEQUENCE.md"]
        self.assertIn("T_{\\mathrm{scalar}}^{\\mathrm{matched}}", qbp)
        self.assertIn("T_{\\mathrm{grad}}^{\\mathrm{matched}}", qbp)

    def test_technical_walkthrough_is_the_visible_entry_point(self) -> None:
        self.assertTrue((ROOT / "scripts" / "technical_walkthrough.py").is_file())
        for relative in PRIMARY_PAGES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("scripts/reviewer_walkthrough.py", text)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        verification = (ROOT / "docs" / "VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("scripts/technical_walkthrough.py", readme)
        self.assertIn("scripts/technical_walkthrough.py", verification)

    def test_primary_local_links_resolve(self) -> None:
        for relative in PRIMARY_PAGES + COMPATIBILITY_PAGES:
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

    def test_navigation_covers_the_reader_route(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for target in (
            "REVIEW.md",
            "docs/READING_GUIDE.md",
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
        self.assertIn("## Main route", documentation_index)
        self.assertIn("## Evidence and independent reconstructions", documentation_index)

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
            "faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582",
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
