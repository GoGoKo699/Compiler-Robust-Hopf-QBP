from __future__ import annotations

import random
import unittest

import numpy as np

from compiler_robust_hopf.frames import direct_real_frame
from compiler_robust_hopf.tree_decoder import (
    apply_reversible_operations,
    binary_to_unary_layers,
    binary_to_unary_operations,
    clean_binary_input,
    conditioned_prefix_resource_row,
    expected_clean_unary_output,
    reversible_layer_is_disjoint,
    tree_decoder_layout,
    tree_decoder_resource_row,
    unary_hopf_code_action,
    unary_layer_pairs,
)


class TreeDecoderTests(unittest.TestCase):
    def test_clean_binary_basis_maps_to_one_hot_and_back(self) -> None:
        for t in range(1, 10):
            operations = binary_to_unary_operations(t)
            if t <= 6:
                labels = range(1 << t)
            else:
                labels = sorted(
                    {
                        0,
                        1,
                        (1 << t) - 1,
                        *[(17 * index) % (1 << t) for index in range(32)],
                    }
                )
            for label in labels:
                clean_input = clean_binary_input(t, label)
                one_hot = apply_reversible_operations(clean_input, operations)
                self.assertEqual(one_hot, expected_clean_unary_output(t, label))
                recovered = apply_reversible_operations(
                    one_hot, operations, inverse=True
                )
                self.assertEqual(recovered, clean_input)

    def test_gate_list_is_reversible_on_arbitrary_basis_states(self) -> None:
        rng = random.Random(260908)
        for t in range(1, 7):
            layout = tree_decoder_layout(t)
            operations = binary_to_unary_operations(t)
            for _ in range(16):
                bits = tuple(
                    rng.randrange(2) for _ in range(layout.total_qubits)
                )
                output = apply_reversible_operations(bits, operations)
                recovered = apply_reversible_operations(
                    output, operations, inverse=True
                )
                self.assertEqual(recovered, bits)

    def test_explicit_layers_are_disjoint_and_match_depth_formula(self) -> None:
        for t in range(1, 11):
            layers = binary_to_unary_layers(t)
            row = tree_decoder_resource_row(t)
            self.assertEqual(len(layers), row.forward_depth_proxy)
            self.assertTrue(
                all(reversible_layer_is_disjoint(layer) for layer in layers)
            )
            self.assertEqual(
                sum(len(layer) for layer in layers),
                row.forward_gate_proxy,
            )

    def test_exact_workspace_and_closed_form_counts(self) -> None:
        for t in range(1, 25):
            branches = 1 << t
            row = tree_decoder_resource_row(t)
            self.assertEqual(row.branches, branches)
            self.assertEqual(
                row.clean_workspace_qubits,
                3 * branches - 2 - t,
            )
            self.assertEqual(row.toffoli_gates_forward, branches - 1)
            self.assertEqual(
                row.forward_gate_proxy,
                11 * branches - 10 - 5 * t,
            )
            self.assertEqual(
                row.round_trip_gate_proxy,
                2 * row.forward_gate_proxy,
            )
            self.assertEqual(row.forward_depth_proxy, 11 * t - 4)

    def test_conditioned_prefix_reuses_decoder_workspace(self) -> None:
        # The routed envelope applies only to a nontrivial cut, so n-t >= 1.
        for t in range(1, 25):
            decoder = tree_decoder_resource_row(t)
            for n in (t + 1, t + 2, t + 5):
                prefix = conditioned_prefix_resource_row(n, t)
                self.assertEqual(
                    prefix.clean_workspace_qubits,
                    decoder.clean_workspace_qubits,
                )
                self.assertLessEqual(
                    prefix.clean_workspace_qubits,
                    2 * (1 << t) * (n - t + 1),
                )

    def test_one_hot_givens_network_equals_complete_hopf_frame(self) -> None:
        rng = np.random.default_rng(260909)
        for t in range(1, 8):
            theta = rng.uniform(-1.1, 1.1, size=(1 << t) - 1)
            np.testing.assert_allclose(
                unary_hopf_code_action(t, theta),
                direct_real_frame(t, theta),
                atol=1e-12,
                rtol=0.0,
            )

    def test_each_givens_depth_uses_disjoint_mode_pairs(self) -> None:
        for t in range(1, 14):
            for depth in range(t):
                pairs = unary_layer_pairs(t, depth)
                flattened = [mode for pair in pairs for mode in pair]
                self.assertEqual(len(pairs), 1 << depth)
                self.assertEqual(len(flattened), len(set(flattened)))
                self.assertTrue(
                    all(0 <= mode < (1 << t) for mode in flattened)
                )


if __name__ == "__main__":
    unittest.main()
