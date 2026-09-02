from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHA40 = re.compile(r"^[0-9a-f]{40}$")


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

    def test_active_lineage_and_native_paths_exist(self) -> None:
        for local_path, sources in self.payload["file_lineage"].items():
            self.assertTrue((ROOT / local_path).is_file(), local_path)
            self.assertTrue(sources)
        for local_path in self.payload["project_native_paths"]:
            self.assertTrue((ROOT / local_path).is_file(), local_path)

    def test_sync_document_names_recorded_commits(self) -> None:
        sync_text = (ROOT / "SYNC.md").read_text(encoding="utf-8")
        for record in self.payload["upstreams"]:
            self.assertIn(record["repository"], sync_text)
            self.assertIn(record["tracked_commit"], sync_text)

    def test_frozen_fallback_is_explicit(self) -> None:
        fallback = self.payload["frozen_fallback"]
        self.assertEqual(fallback["branch"], "near-optimal-audited-2026-09")
        self.assertRegex(fallback["manifest_commit"], SHA40)
        self.assertIn("not an active compiler path", fallback["policy"])


if __name__ == "__main__":
    unittest.main()
