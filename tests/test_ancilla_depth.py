from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.ancilla_depth import (
    ancilla_depth_row,
    conditioned_prefix_frame,
    direct_prefix_frame,
    frame_ancilla_upper_bound,
    geometric_tail_sum,
    geometric_tail_upper_bound,
    hybrid_frame,
    hybrid_frame_residual,
    hybrid_prefix_qubits,
    maximum_unary_control_copies,
    prefix_angle_count,
    prefix_bridge_residual,
    tail_frame,
    tail_ucg_work_ancillas,
    unary_code_action,
    unary_code_leakage,
    unary_hopf_network,
    unary_layer_pairs,
    unary_prefix_ancilla_upper_bound,
    unary_prefix_size_proxy,
)
from compiler_robust_hopf.frames import real_frame_matrix


class AncillaDepthTests(unittest.TestCase):
    def test_conditioned_prefix_bridge_for_every_cut(self) -> None:
        rng = np.random.default_rng(260902)
        for n in range(1, 9):
            theta = rng.uniform(-1.2, 1.2, size=(1 << n) - 1)
            for t in range(n + 1):
                if t == 0:
                    expected = np.eye(1 << n, dtype=complex)
                else:
                    prefix = real_frame_matrix(theta[: prefix_angle_count(t)])
                    suffix_dimension = 1 << (n - t)
                    suffix_zero = np.zeros(
                        (suffix_dimension, suffix_dimension), dtype=complex
                    )
                    suffix_zero[0, 0] = 1.0
                    expected = np.kron(prefix, suffix_zero) + np.kron(
                        np.eye(1 << t, dtype=complex),
                        np.eye(suffix_dimension, dtype=complex) - suffix_zero,
                    )
                np.testing.assert_allclose(
                    direct_prefix_frame(n, t, theta),
                    expected,
                    atol=1e-12,
                    rtol=0.0,
                )
                np.testing.assert_allclose(
                    conditioned_prefix_frame(n, t, theta),
                    expected,
                    atol=1e-12,
                    rtol=0.0,
                )
                self.assertLessEqual(prefix_bridge_residual(n, t, theta), 1e-12)

    def test_hybrid_factorization_recovers_complete_frame(self) -> None:
        rng = np.random.default_rng(260903)
        for n in range(1, 8):
            theta = rng.uniform(-0.9, 0.9, size=(1 << n) - 1)
            reference = real_frame_matrix(theta)
            for t in range(n + 1):
                np.testing.assert_allclose(
                    hybrid_frame(n, t, theta),
                    reference,
                    atol=1e-12,
                    rtol=0.0,
                )
                np.testing.assert_allclose(
                    tail_frame(n, t, theta) @ direct_prefix_frame(n, t, theta),
                    reference,
                    atol=1e-12,
                    rtol=0.0,
                )
                self.assertLessEqual(hybrid_frame_residual(n, t, theta), 1e-12)

    def test_unary_layers_are_disjoint(self) -> None:
        for t in range(1, 9):
            for depth in range(t):
                pairs = unary_layer_pairs(t, depth)
                self.assertEqual(len(pairs), 1 << depth)
                flattened = [mode for pair in pairs for mode in pair]
                self.assertEqual(len(flattened), len(set(flattened)))
                self.assertTrue(all(0 <= mode < (1 << t) for mode in flattened))

    def test_unary_network_preserves_code_and_equals_frame(self) -> None:
        rng = np.random.default_rng(260904)
        for t in range(1, 4):
            theta = rng.uniform(-1.0, 1.0, size=prefix_angle_count(t))
            np.testing.assert_allclose(
                unary_code_action(t, theta),
                real_frame_matrix(theta),
                atol=1e-12,
                rtol=0.0,
            )
            self.assertLessEqual(unary_code_leakage(t, theta), 1e-12)
            network = unary_hopf_network(t, theta)
            np.testing.assert_allclose(
                network.conj().T @ network,
                np.eye(network.shape[0]),
                atol=1e-12,
                rtol=0.0,
            )

    def test_workspace_and_term_ledger(self) -> None:
        for n in range(1, 17):
            N = 1 << n
            budgets = sorted(
                {
                    0,
                    1,
                    2,
                    3,
                    n,
                    n * n,
                    max(0, N // max(1, n * n)),
                    N,
                    3 * N,
                }
            )
            for ancillas in budgets:
                t = hybrid_prefix_qubits(n, ancillas)
                self.assertLessEqual(unary_prefix_ancilla_upper_bound(t), ancillas)
                self.assertEqual(
                    frame_ancilla_upper_bound(ancillas), max(1, ancillas)
                )
                self.assertEqual(
                    tail_ucg_work_ancillas(ancillas, final=False),
                    max(0, ancillas - 1),
                )
                self.assertEqual(
                    tail_ucg_work_ancillas(ancillas, final=True), ancillas
                )

                row = ancilla_depth_row(n, ancillas)
                self.assertEqual(row.dimension, N)
                self.assertEqual(
                    row.frame_ancillas_upper_bound, max(1, ancillas)
                )
                self.assertEqual(row.unary_prefix_qubits, t)
                self.assertEqual(
                    row.maximum_unary_control_copies,
                    maximum_unary_control_copies(t),
                )
                self.assertEqual(row.tail_layers, n - t)
                self.assertEqual(row.logical_hopf_rotations, N - 1)
                self.assertEqual(row.recordwise_decode_operations_per_shot, N)
                self.assertEqual(
                    row.prefix_size_proxy, unary_prefix_size_proxy(n, t)
                )
                self.assertEqual(
                    row.total_frame_depth_proxy,
                    row.prefix_depth_proxy
                    + row.tail_predicate_depth_proxy
                    + row.ucg_linear_depth_proxy
                    + row.ucg_exponential_depth_proxy,
                )
                self.assertEqual(
                    row.total_frame_size_proxy,
                    row.prefix_size_proxy
                    + row.tail_predicate_size_proxy
                    + row.ucg_size_proxy,
                )
                self.assertEqual(
                    row.nonfinal_ucg_work_ancillas,
                    max(0, ancillas - 1) if t < n - 1 else 0,
                )
                self.assertEqual(
                    row.final_ucg_work_ancillas,
                    ancillas if t < n else 0,
                )

    def test_uniform_geometric_tail_bound(self) -> None:
        for n in range(1, 81):
            N = 1 << n
            budgets = {
                0,
                1,
                2,
                3,
                n,
                n * n,
                max(0, N // max(1, n * n)),
                max(0, N // max(1, n)),
                N,
                10 * N,
            }
            for shift in budgets:
                self.assertLessEqual(
                    geometric_tail_sum(n, shift),
                    geometric_tail_upper_bound(n, shift) * (1.0 + 1e-12),
                )

    def test_endpoint_rows(self) -> None:
        self.assertEqual(ancilla_depth_row(1, 0).frame_ancillas_upper_bound, 1)
        for n in range(1, 14):
            full = ancilla_depth_row(n, 3 * (1 << n))
            self.assertEqual(full.unary_prefix_qubits, n)
            self.assertEqual(full.tail_layers, 0)
            self.assertEqual(full.nonfinal_ucg_work_ancillas, 0)
            self.assertEqual(full.final_ucg_work_ancillas, 0)
            self.assertEqual(full.ucg_size_proxy, 0)
            self.assertEqual(full.tail_predicate_depth_proxy, 0)
            self.assertEqual(full.total_frame_depth_proxy, 3 * n)

    def test_dense_unary_guard(self) -> None:
        with self.assertRaises(ValueError):
            unary_hopf_network(4, np.zeros(prefix_angle_count(4)))


if __name__ == "__main__":
    unittest.main()
