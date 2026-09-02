from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHA40 = re.compile(r"^[0-9a-f]{40}$")


class ProvenanceTests(unittest.TestCase):
    def test_provenance_schema_and_paths(self) -> None:
        payload = json.loads(
            (ROOT / "provenance" / "upstream.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(
            payload["project"],
            "GoGoKo699/Compiler-Robust-Hopf-QBP",
        )

        upstreams = payload["tracked_upstreams"]
        self.assertGreaterEqual(len(upstreams), 2)
        for record in upstreams:
            self.assertRegex(record["commit"], SHA40)
            self.assertIn("/", record["repository"])
            self.assertTrue(record["branch"])
            self.assertTrue(record["role"])

        for record in payload["active_lineage"]:
            self.assertTrue((ROOT / record["local_path"]).is_file())
            self.assertTrue(record["upstream_path"])
            self.assertTrue(record["status"])

        for relative in payload["project_native_paths"]:
            self.assertTrue((ROOT / relative).is_file(), relative)

        fallback = payload["frozen_fallback"]
        self.assertEqual(fallback["branch"], "near-optimal-audited-2026-09")
        self.assertRegex(fallback["manifest_commit"], SHA40)

    def test_sync_document_names_recorded_commits(self) -> None:
        payload = json.loads(
            (ROOT / "provenance" / "upstream.json").read_text(
                encoding="utf-8"
            )
        )
        sync_text = (ROOT / "SYNC.md").read_text(encoding="utf-8")
        for record in payload["tracked_upstreams"]:
            self.assertIn(record["repository"], sync_text)
            self.assertIn(record["commit"], sync_text)


if __name__ == "__main__":
    unittest.main()
