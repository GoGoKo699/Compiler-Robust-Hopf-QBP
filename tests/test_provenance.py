from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHA40 = re.compile(r"^[0-9a-f]{40}$")
PREVIOUS_HOPF_QBP_MAIN = "faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582"
CURRENT_HOPF_QBP_MAIN = "a9885317cf998a7df87ca07ba86e3bd4f0f419ef"


class ProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(
            (ROOT / "provenance" / "upstream.json").read_text(
                encoding="utf-8"
            )
        )

    def test_provenance_schema_and_upstreams(self) -> None:
        self.assertEqual(self.payload["schema_version"], 1)
        self.assertEqual(
            self.payload["current_repository"],
            "GoGoKo699/Compiler-Robust-Hopf-QBP",
        )
        upstreams = self.payload["upstreams"]
        self.assertGreaterEqual(len(upstreams), 2)
        for record in upstreams:
            self.assertRegex(record["tracked_commit"], SHA40)
            self.assertIn("/", record["repository"])
            self.assertTrue(record["tracked_branch"])
            self.assertTrue(record["role"])

        main = next(
            record
            for record in upstreams
            if record["repository"] == "GoGoKo699/Hopf-QBP"
            and record["tracked_branch"] == "main"
        )
        self.assertEqual(main["tracked_commit"], CURRENT_HOPF_QBP_MAIN)

    def test_active_lineage_and_native_paths_exist(self) -> None:
        for local_path, sources in self.payload["file_lineage"].items():
            self.assertTrue((ROOT / local_path).is_file(), local_path)
            self.assertTrue(sources)
        for local_path in self.payload["project_native_paths"]:
            self.assertTrue((ROOT / local_path).is_file(), local_path)
        self.assertIn(
            "compiler_robust_hopf/router.py",
            self.payload["project_native_paths"],
        )

    def test_upstream_reconciliation_records_scientific_boundaries(self) -> None:
        reconciliation = self.payload["upstream_reconciliation"]
        self.assertEqual(
            reconciliation["reviewed_main_commit"],
            CURRENT_HOPF_QBP_MAIN,
        )
        self.assertEqual(reconciliation["previous_main_commit"], PREVIOUS_HOPF_QBP_MAIN)
        self.assertEqual(reconciliation["commits_reviewed"], 5)
        joined = " ".join(reconciliation["relevant_changes"]).lower()
        self.assertIn("raw coordinatewise", joined)
        self.assertIn("natural-gradient", joined)
        self.assertIn("metric", joined)
        self.assertIn("controlled-observable", joined)

    def test_previous_reconciliation_and_file_lineage_are_retained(self) -> None:
        history = self.payload["upstream_reconciliation_history"]
        self.assertTrue(history)
        previous = history[-1]
        self.assertEqual(previous["reviewed_main_commit"], PREVIOUS_HOPF_QBP_MAIN)
        self.assertEqual(previous["commits_reviewed"], 10)
        self.assertEqual(
            previous["previous_main_commit"],
            "9957815767ef3649275960fd5e860fb91725ff26",
        )
        self.assertEqual(
            previous["reviewed_main_commit"],
            self.payload["upstream_reconciliation"]["previous_main_commit"],
        )
        for sources in self.payload["file_lineage"].values():
            self.assertTrue(all(CURRENT_HOPF_QBP_MAIN not in source for source in sources))
        seed = next(
            record for record in self.payload["upstreams"]
            if record["tracked_branch"] == "ancilla-depth-robustness-2026"
        )
        self.assertEqual(seed["tracked_commit"], "9cc564f493caff62b847fc362df522a68c6e83bf")

    def test_current_baseline_references_match_the_provenance(self) -> None:
        source_map = (ROOT / "docs/SOURCE_MAP.md").read_text(encoding="utf-8")
        sync = (ROOT / "SYNC.md").read_text(encoding="utf-8")
        current_upstreams = sync.split("## Current tracked upstreams", 1)[1].split("\n## ", 1)[0]
        # Historical reconciliation sections deliberately preserve earlier SHAs.
        for label, text in (("SOURCE_MAP", source_map), ("current upstreams", current_upstreams)):
            self.assertIn(CURRENT_HOPF_QBP_MAIN, text, label)
            self.assertNotIn(PREVIOUS_HOPF_QBP_MAIN, text, label)

    def test_zero_record_clarification_is_magnitude_specific(self) -> None:
        qbp = " ".join((ROOT / "docs/QBP_CONSEQUENCE.md").read_text(encoding="utf-8").split())
        sync = " ".join((ROOT / "SYNC.md").read_text(encoding="utf-8").split())
        self.assertIn(
            "At a singular magnitude coordinate, the raw coordinate record is exactly zero.",
            qbp,
        )
        self.assertNotIn("At a singular coordinate, the raw coordinate record is exactly zero.", qbp)
        self.assertIn("a zero magnitude metric weight", sync)
        self.assertIn("need not have zero individual signed one-hot records", sync)
        joined = " ".join(self.payload["upstream_reconciliation"]["relevant_changes"])
        self.assertIn("individual phase records need not vanish", joined)

    def test_sync_document_names_recorded_commits(self) -> None:
        sync_text = (ROOT / "SYNC.md").read_text(encoding="utf-8")
        for record in self.payload["upstreams"]:
            self.assertIn(record["repository"], sync_text)
            self.assertIn(record["tracked_commit"], sync_text)
        self.assertIn("Reconciliation completed", sync_text)
        self.assertIn(CURRENT_HOPF_QBP_MAIN, sync_text)

    def test_frozen_fallback_is_explicit(self) -> None:
        fallback = self.payload["frozen_fallback"]
        self.assertEqual(fallback["branch"], "near-optimal-audited-2026-09")
        self.assertRegex(fallback["manifest_commit"], SHA40)
        self.assertIn("not an active compiler path", fallback["policy"])


if __name__ == "__main__":
    unittest.main()
