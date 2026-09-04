from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LiteraturePolicyTests(unittest.TestCase):
    def test_literature_roles_are_machine_readable_and_correct(self) -> None:
        payload = json.loads(
            (ROOT / "provenance" / "literature.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(int(payload["schema_version"]), 3)

        active = payload["active_compiler_framework"]
        self.assertEqual(active["authors"], ["Pei Yuan", "Shengyu Zhang"])
        self.assertEqual(active["journal"], "Quantum")
        self.assertEqual(active["article"], 956)
        self.assertEqual(active["published_eprint"], "arXiv:2202.11302v2")
        self.assertEqual(active["checked_arxiv_revision"], "arXiv:2202.11302v3")
        self.assertIn("normative", active["version_policy"])
        self.assertIn("retain", active["version_policy"])
        self.assertIn("sole active", active["policy"])
        self.assertEqual(
            set(active["roles"]),
            {"theorem_1", "theorem_2", "lemma_5", "lemma_6", "lemma_9"},
        )

        historical = payload["historical_predecessor"]
        self.assertEqual(
            historical["authors"],
            [
                "Xiaoming Sun",
                "Guojing Tian",
                "Shuai Yang",
                "Pei Yuan",
                "Shengyu Zhang",
            ],
        )
        self.assertIn("historical", historical["policy"])
        self.assertIn("not an active alternative", historical["policy"])

    def test_strict_zero_prior_art_and_claim_boundary_are_recorded(self) -> None:
        payload = json.loads(
            (ROOT / "provenance" / "literature.json").read_text(
                encoding="utf-8"
            )
        )
        titles = {entry["title"] for entry in payload["strict_zero_prior_art"]}
        self.assertIn("Elementary gates for quantum computation", titles)
        self.assertIn(
            "Polylogarithmic-depth controlled-NOT gates without ancilla qubits",
            titles,
        )
        self.assertIn(
            "Rise of conditionally clean ancillae for efficient quantum circuit constructions",
            titles,
        )
        self.assertIn(
            "A Unified Framework for Optimizing Uniformly Controlled Structures in Quantum Circuits",
            titles,
        )

        policy = payload["strict_zero_claim_policy"]
        self.assertIn("Hopf", policy["project_specific_claim"])
        self.assertIn("broader independent review", policy["review_status"])
        prohibited = " ".join(policy["do_not_claim"]).lower()
        self.assertIn("borrowed", prohibited)
        self.assertIn("toggle", prohibited)
        self.assertIn("square-root", prohibited)

    def test_active_compiler_sources_have_no_legacy_imports(self) -> None:
        active_paths = (
            "compiler_robust_hopf/tree_structure.py",
            "compiler_robust_hopf/tree_decoder.py",
            "compiler_robust_hopf/router.py",
            "compiler_robust_hopf/strict_zero_echo.py",
            "compiler_robust_hopf/unified_compiler.py",
        )
        forbidden = (
            "from .ancilla_depth",
            "from .complex_resources",
            "from .optimal_parallel",
            "from .optimal_audit",
            "Lemma 28",
            "Sun-style",
        )
        for relative in active_paths:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for phrase in forbidden:
                self.assertNotIn(phrase, text, msg=f"{phrase!r} in {relative}")

    def test_active_docs_use_one_framework_and_all_workspace_scope(self) -> None:
        active_docs = (
            "README.md",
            "REVIEW.md",
            "docs/HOPF_INTERFACE.md",
            "docs/COMPILER_THEOREM.md",
            "docs/QBP_CONSEQUENCE.md",
            "docs/VERIFICATION.md",
            "docs/SOURCE_MAP.md",
            "docs/THEOREM_OVERVIEW.md",
            "docs/UNIFIED_YUAN_ZHANG_COMPILER.md",
            "docs/END_TO_END_QBP.md",
            "docs/PROOF_AUDIT.md",
            "docs/RESEARCH_STATUS.md",
            "docs/CLAIM_SUPPORT.md",
            "manuscript/README.md",
        )
        source_bearing_docs = (
            "README.md",
            "docs/COMPILER_THEOREM.md",
            "docs/SOURCE_MAP.md",
            "docs/RELATED_WORK.md",
            "docs/RESEARCH_STATUS.md",
            "docs/CLAIM_SUPPORT.md",
            "docs/PROOF_AUDIT.md",
            "manuscript/README.md",
        )
        theorem_bearing_docs = (
            "README.md",
            "REVIEW.md",
            "docs/HOPF_INTERFACE.md",
            "docs/COMPILER_THEOREM.md",
            "docs/QBP_CONSEQUENCE.md",
            "docs/THEOREM_OVERVIEW.md",
            "docs/UNIFIED_YUAN_ZHANG_COMPILER.md",
            "docs/END_TO_END_QBP.md",
            "docs/PROOF_AUDIT.md",
            "docs/RESEARCH_STATUS.md",
            "docs/CLAIM_SUPPORT.md",
            "manuscript/README.md",
        )
        retired_names = (
            "ancilla_depth.py",
            "complex_resources.py",
            "optimal_parallel.py",
            "optimal_audit.py",
            "ancilla_depth_ledger.py",
            "complex_workspace_ledger.py",
            "optimality_ledger.py",
        )

        for relative in active_docs:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for retired in retired_names:
                self.assertNotIn(retired, text, msg=f"{retired} in {relative}")

        # The compiler source should be cited precisely in source-bearing pages,
        # but need not be repeated in every step of the linear narrative.
        for relative in source_bearing_docs:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("Yuan", text, msg=f"missing active source in {relative}")

        for relative in theorem_bearing_docs:
            text = (ROOT / relative).read_text(encoding="utf-8")
            compact = "".join(text.split())
            self.assertIn(
                "m>=0",
                compact,
                msg=f"missing all-workspace theorem scope in {relative}",
            )

        primary = " ".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in (
                "README.md",
                "REVIEW.md",
                "docs/HOPF_INTERFACE.md",
                "docs/COMPILER_THEOREM.md",
                "docs/QBP_CONSEQUENCE.md",
                "docs/VERIFICATION.md",
                "docs/SOURCE_MAP.md",
            )
        )
        normalized_primary = " ".join(primary.split()).lower()
        self.assertIn("incoming amplitude", normalized_primary)
        self.assertIn("complex magnitude frame", normalized_primary)
        self.assertIn("router.py", primary)
        self.assertIn("matched", normalized_primary)
        self.assertIn("raw coordinate", normalized_primary)
        self.assertIn("prescribed", normalized_primary)

        related = (ROOT / "docs" / "RELATED_WORK.md").read_text(
            encoding="utf-8"
        )
        normalized_related = " ".join(related.split())
        self.assertIn("historical predecessor", normalized_related.lower())
        self.assertIn("Sun", related)
        self.assertIn("Yuan", related)
        self.assertIn("Barenco", related)
        self.assertIn("Khattar", related)
        self.assertIn("can be adapted", normalized_related.lower())

        prior_art = (ROOT / "docs" / "STRICT_ZERO_PRIOR_ART.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(prior_art.split())
        self.assertIn("not a legal novelty opinion", normalized)
        self.assertIn("Hopf-specific", prior_art)
        self.assertIn("should not be used", prior_art)

    def test_active_unified_dispatch_uses_strict_zero_echo(self) -> None:
        text = (
            ROOT / "compiler_robust_hopf" / "unified_compiler.py"
        ).read_text(encoding="utf-8")
        self.assertIn("strict_zero_echo_frame_resource_row", text)
        self.assertIn("if ancillas == 0", text)
        self.assertIn("strict-zero-full-width-ucg-baseline", text)

    def test_router_is_explicit_and_operator_tested(self) -> None:
        router = (ROOT / "compiler_robust_hopf" / "router.py").read_text(
            encoding="utf-8"
        )
        tests = (ROOT / "tests" / "test_router.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("router_swap_layers", router)
        self.assertIn("apply_router_forward", router)
        self.assertIn("apply_parallel_controlled_subframes", router)
        self.assertIn("routed_tail_residual", router)
        self.assertIn(
            "test_route_inverse_is_identity_on_arbitrary_entangled_inputs",
            tests,
        )
        self.assertIn(
            "test_routed_tail_matches_direct_sum_on_arbitrary_complex_inputs",
            tests,
        )
        self.assertIn("branch_flags_are_clean", tests)

    def test_retired_paths_are_absent_from_active_tree(self) -> None:
        retired = (
            "compiler_robust_hopf/ancilla_depth.py",
            "compiler_robust_hopf/complex_resources.py",
            "compiler_robust_hopf/optimal_parallel.py",
            "compiler_robust_hopf/optimal_audit.py",
            "scripts/ancilla_depth_ledger.py",
            "scripts/complex_workspace_ledger.py",
            "scripts/optimality_ledger.py",
            "tests/test_ancilla_depth.py",
            "tests/test_complex_resources.py",
            "tests/test_optimal_parallel.py",
            "tests/test_optimal_audit.py",
        )
        for relative in retired:
            self.assertFalse((ROOT / relative).exists(), msg=relative)


if __name__ == "__main__":
    unittest.main()
