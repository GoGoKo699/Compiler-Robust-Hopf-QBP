from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHA40 = re.compile(r"^[0-9a-f]{40}$")


class ProvenanceTests(unittest.TestCase):
    def test_provenance_is_well_formed_and_paths_exist(self) -> None:
        path = ROOT / "provenance" / "upstream.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            payload["current_repository"],
            "GoGoKo699/Compiler-Robust-Hopf-QBP",
        )
        self.assertGreaterEqual(len(payload["upstreams"]), 2)
        for record in payload["upstreams"]:
            self.assertRegex(record["tracked_commit"], SHA40)
            self.assertIn("/", record["repository"])
            self.assertTrue(record["tracked_branch"])
        for local_path, sources in payload["file_lineage"].items():
            self.assertTrue((ROOT / local_path).is_file(), local_path)
            self.assertTrue(sources)

    def test_sync_document_names_recorded_commits(self) -> None:
        provenance = json.loads(
            (ROOT / "provenance" / "upstream.json").read_text(encoding="utf-8")
        )
        sync_text = (ROOT / "SYNC.md").read_text(encoding="utf-8")
        for record in provenance["upstreams"]:
            self.assertIn(record["tracked_commit"], sync_text)


if __name__ == "__main__":
    unittest.main()
