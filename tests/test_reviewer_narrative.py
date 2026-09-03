from __future__ import annotations

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
    "docs/QBP_CONSEQUENCE.md",
    "docs/VERIFICATION.md",
    "docs/SOURCE_MAP.md",
    "docs/RELATED_WORK.md",
    "docs/INDEPENDENT_REVIEW_GUIDE.md",
    "docs/RESEARCH_STATUS.md",
    "docs/STRICT_ZERO_BORROWED_SUFFIX_ECHO.md",
    "docs/STRICT_ZERO_ECHO_AUDIT.md",
    "manuscript/README.md",
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


class ReviewerNarrativeTests(unittest.TestCase):
    def test_primary_pages_exist_and_have_no_workflow_language(self) -> None:
        for relative in PRIMARY_PAGES:
            path = ROOT / relative
            self.assertTrue(path.is_file(), msg=relative)
            text = path.read_text(encoding="utf-8")
            for phrase in PROCESS_PHRASES:
                self.assertNotIn(phrase, text, msg=f"{phrase!r} in {relative}")

    def test_landing_page_is_short_and_review_is_substantial(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
        self.assertLess(len(readme), 12_000)
        self.assertGreater(len(review), 30_000)
        self.assertIn("# Optimal Compilation of Hopf Differential Frames", readme)
        self.assertIn("## Main result under technical review", readme)
        self.assertIn("## 3. Two qubits", review)
        self.assertIn("## 6. Strict zero workspace", review)
        self.assertIn("## 11. Quantum-backpropagation consequence", review)

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

    def test_navigation_covers_the_complete_reader_route(self) -> None:
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
        self.assertIn("Main reading route", documentation_index)
        self.assertIn("Evidence and internal review", documentation_index)

        verification = (ROOT / "docs" / "VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("PROOF_AUDIT.md", verification)
        self.assertIn("STRICT_ZERO_ECHO_AUDIT.md", verification)
        self.assertIn("CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md", verification)


if __name__ == "__main__":
    unittest.main()
