from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class UnifiedProvenanceTests(unittest.TestCase):
    def test_unified_provenance_paths_exist(self) -> None:
        payload = json.loads(
            (ROOT / "provenance" / "upstream.json").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(int(payload["schema_version"]), 1)
        tracked = payload.get("tracked_upstreams", payload.get("upstreams", []))
        self.assertGreaterEqual(len(tracked), 2)
        for entry in tracked:
            commit = str(entry["commit"])
            self.assertEqual(len(commit), 40)
            int(commit, 16)

        lineage = payload.get("active_lineage", payload.get("lineage", []))
        for entry in lineage:
            self.assertTrue((ROOT / entry["local_path"]).is_file())
        for relative in payload.get("project_native_paths", []):
            self.assertTrue((ROOT / relative).is_file())

    def test_recorded_commits_appear_in_sync_document(self) -> None:
        payload = json.loads(
            (ROOT / "provenance" / "upstream.json").read_text(encoding="utf-8")
        )
        sync = (ROOT / "SYNC.md").read_text(encoding="utf-8")
        tracked = payload.get("tracked_upstreams", payload.get("upstreams", []))
        for entry in tracked:
            self.assertIn(entry["repository"], sync)
            self.assertIn(entry["commit"], sync)


if __name__ == "__main__":
    unittest.main()
