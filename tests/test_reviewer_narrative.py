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
    "peer-review-revision-2026-09",
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

    def test_primary_pages_use_github_safe_math_commands(self) -> None:
        for relative in PRIMARY_PAGES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn(
                "\\operatorname",
                text,
                msg=f"unsupported GitHub math command in {relative}",
            )

    def test_landing_page_is_short_and_review_is_substantial(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
        self.assertLess(len(readme), 15_000)
        self.assertGreater(len(review), 30_000)
        self.assertIn("# Optimal Compilation of Hopf Differential Frames", readme)
        self.assertIn("## Main result under technical review", readme)
        self.assertIn("## 3. Two qubits", review)
        self.assertIn("## 6. Strict zero workspace", review)
        self.assertIn("## 8. Larger workspace", review)
        self.assertIn("## 11. Quantum-backpropagation consequence", review)

    def test_peer_review_corrections_are_visible_in_primary_route(self) -> None:
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
        normalized = " ".join(combined.split()).lower()
        self.assertIn("oriented incoming amplitude", normalized)
        self.assertIn("singular", normalized)
        self.assertIn("complex magnitude frame", normalized)
        self.assertIn("matched", normalized)
        self.assertIn("raw hopf-coordinate gradient", normalized)
        self.assertIn("router.py", combined)
        self.assertIn("arxiv:2202.11302v2", normalized)
        self.assertIn("arxiv:2202.11302v3", normalized)

        verification = files["docs/VERIFICATION.md"]
        self.assertIn("explicit CNOT-fanout and Fredkin layers", verification)
        self.assertIn("arbitrary prefix–suffix-entangled inputs", verification)
        self.assertIn("implementation levels", verification.lower())

        qbp = files["docs/QBP_CONSEQUENCE.md"]
        self.assertIn("T_{\\mathrm{scalar}}^{\\mathrm{matched}}", qbp)
        self.assertIn("T_{\\mathrm{grad}}^{\\mathrm{matched}}", qbp)

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
