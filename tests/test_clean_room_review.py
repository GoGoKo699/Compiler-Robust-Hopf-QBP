from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CleanRoomReviewTests(unittest.TestCase):
    def test_review_records_all_workspace_verdict_and_evidence_boundary(self) -> None:
        text = (ROOT / "docs" / "CLEAN_ROOM_ALL_WORKSPACE_REVIEW.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("third internal proof review", text)
        self.assertIn("not external peer review", text.lower())
        self.assertIn("not a legal novelty opinion", text.lower())
        self.assertIn("for every integer `m>=0`", text)
        self.assertIn("q=d+2", text)
        self.assertIn("2B(s+1)", text)
        self.assertIn("independent specialist review", text)

    def test_prior_art_search_is_machine_readable_and_conservative(self) -> None:
        payload = json.loads(
            (ROOT / "provenance" / "prior_art_search.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(payload["schema_version"], 1)
        self.assertIn("not external peer review", payload["status"])
        self.assertIn("not a legal novelty opinion", payload["status"])
        self.assertFalse(
            payload["negative_search_result"]["exact_match_found"]
        )
        self.assertIn(
            "not proof of novelty",
            payload["negative_search_result"]["interpretation"].lower(),
        )

        keys = {entry["key"] for entry in payload["sources"]}
        required = {
            "barenco_1995",
            "mottonen_2005",
            "bergholm_2005",
            "yuan_zhang_2023",
            "low_kliuchnikov_schaeffer_2024",
            "claudon_2024",
            "khattar_gidney_2025",
            "zindorf_bose_2025",
            "xu_et_al_2025",
            "su_et_al_2026",
            "bona_2026",
            "liu_zhou_meng_2026",
        }
        self.assertTrue(required.issubset(keys))

        prohibited = payload["claim_policy"]["do_not_claim"]
        self.assertIn("first square-root controlled-unitary echo", prohibited)
        self.assertIn("legal novelty determination", prohibited)

    def test_human_readable_prior_art_record_matches_policy(self) -> None:
        text = (ROOT / "docs" / "PRIOR_ART_SEARCH_2026_09.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Search date: **2026-09-03**", text)
        self.assertIn("not a legal novelty opinion", text.lower())
        self.assertIn("negative result of a bounded search", text.lower())
        self.assertIn("Zindorf and Bose", text)
        self.assertIn("Borrowing Dirty Qubits in Quantum Programs", text)
        self.assertIn("Bona", text)
        self.assertIn("Quantum Uncomputation of Clean and Dirty Ancilla Qubits", text)
        self.assertIn("independent circuit-synthesis specialist", text)


if __name__ == "__main__":
    unittest.main()
