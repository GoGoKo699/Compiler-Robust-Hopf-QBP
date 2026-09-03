from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.router import (
    apply_parallel_controlled_subframes,
    apply_router_forward,
    apply_router_inverse,
    branch_flags_are_clean,
    copies_are_clean,
    decode_clean_system_state,
    encode_clean_system_state,
    routed_basis_snapshot,
    routed_cut_residual,
    routed_tail_residual,
    router_fanout_layers,
    router_layer_is_disjoint,
    router_layout,
    router_schedule_row,
    router_swap_layers,
)
from compiler_robust_hopf.unified_compiler import (
    route_workspace_row,
    routing_depth_proxy,
    routing_size_proxy,
)


class CoherentRouterTests(unittest.TestCase):
    def test_explicit_layout_and_schedule_match_resource_ledger(self) -> None:
        for n in range(2, 13):
            for t in range(1, n):
                layout = router_layout(n, t)
                schedule = router_schedule_row(n, t)
                ledger = route_workspace_row(n, t)

                self.assertEqual(
                    layout.workspace_qubits,
                    ledger.tail_peak_ancillas,
                )
                self.assertEqual(
                    schedule.branch_data_ancillas,
                    ledger.branch_data_ancillas,
                )
                self.assertEqual(
                    schedule.token_ancillas,
                    ledger.token_ancillas,
                )
                self.assertEqual(
                    schedule.control_copy_ancillas,
                    ledger.control_copy_ancillas,
                )
                self.assertEqual(
                    schedule.reusable_branch_flags,
                    ledger.branch_flag_ancillas,
                )
                self.assertEqual(
                    schedule.forward_fredkin_gates,
                    ledger.forward_fredkin_gates,
                )
                self.assertEqual(
                    schedule.round_trip_depth,
                    routing_depth_proxy(n, t),
                )
                self.assertEqual(
                    schedule.round_trip_size,
                    routing_size_proxy(n, t),
                )

                expected_fanout_depth = (
                    t - 1 + (layout.suffix_qubits).bit_length()
                )
                self.assertEqual(schedule.fanout_depth, expected_fanout_depth)

    def test_every_declared_router_layer_is_disjoint(self) -> None:
        for n in range(2, 13):
            for t in range(1, n):
                layout = router_layout(n, t)
                for layer in (
                    *router_fanout_layers(layout),
                    *router_swap_layers(layout),
                ):
                    self.assertTrue(router_layer_is_disjoint(layer))

    def test_clean_basis_inputs_route_to_the_selected_branch_and_back(self) -> None:
        for n in range(2, 8):
            for t in range(1, n):
                layout = router_layout(n, t)
                suffix_mask = (1 << layout.suffix_qubits) - 1
                for label in range(1 << n):
                    snapshot = routed_basis_snapshot(layout, label)
                    self.assertEqual(
                        snapshot.prefix,
                        label >> layout.suffix_qubits,
                    )
                    self.assertEqual(snapshot.suffix, label & suffix_mask)
                    self.assertEqual(snapshot.active_branch, snapshot.prefix)
                    self.assertEqual(snapshot.active_token_count, 1)
                    self.assertFalse(snapshot.inactive_data_nonzero)
                    self.assertTrue(snapshot.copies_clean)

                    routed = apply_router_forward({label: 1.0 + 0.0j}, layout)
                    restored = apply_router_inverse(routed, layout)
                    self.assertEqual(restored, {label: 1.0 + 0.0j})

    def test_route_inverse_is_identity_on_arbitrary_entangled_inputs(self) -> None:
        rng = np.random.default_rng(260920)
        for n in range(2, 7):
            for t in range(1, n):
                layout = router_layout(n, t)
                state = rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)
                state /= np.linalg.norm(state)
                encoded = encode_clean_system_state(state, layout)
                routed = apply_router_forward(encoded, layout)
                self.assertTrue(copies_are_clean(routed, layout))
                restored = apply_router_inverse(routed, layout)
                decoded, leakage = decode_clean_system_state(restored, layout)
                np.testing.assert_allclose(decoded, state, atol=2e-12, rtol=0.0)
                self.assertLessEqual(leakage, 2e-12)

    def test_parallel_subframes_clear_flags_before_inverse_routing(self) -> None:
        rng = np.random.default_rng(260921)
        for n in range(3, 7):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            for t in range(1, n):
                layout = router_layout(n, t)
                state = rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)
                state /= np.linalg.norm(state)
                routed = apply_router_forward(
                    encode_clean_system_state(state, layout), layout
                )
                operated = apply_parallel_controlled_subframes(
                    routed, layout, theta
                )
                self.assertTrue(branch_flags_are_clean(operated, layout))
                self.assertTrue(copies_are_clean(operated, layout))
                restored = apply_router_inverse(operated, layout)
                _decoded, leakage = decode_clean_system_state(restored, layout)
                self.assertLessEqual(leakage, 2e-12)

    def test_routed_tail_matches_direct_sum_on_arbitrary_complex_inputs(self) -> None:
        rng = np.random.default_rng(260922)
        for n in range(2, 7):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            for t in range(1, n):
                state = rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)
                state /= np.linalg.norm(state)
                residual, leakage = routed_tail_residual(state, n, t, theta)
                self.assertLessEqual(residual, 3e-12)
                self.assertLessEqual(leakage, 3e-12)

    def test_complete_routed_cut_matches_the_hopf_frame(self) -> None:
        rng = np.random.default_rng(260923)
        for n in range(2, 6):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            for t in range(1, n):
                self.assertLessEqual(
                    routed_cut_residual(n, t, theta),
                    4e-12,
                )


if __name__ == "__main__":
    unittest.main()
