from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.frames import (
    complex_frame_matrix,
    direct_real_frame,
)
from compiler_robust_hopf.tree_structure import reconstructed_frame
from compiler_robust_hopf.unified_compiler import (
    choose_routed_cut,
    controlled_unitary,
    diagonal_ucg_blocks,
    diagonal_ucg_matrix,
    diagonal_ucg_resource_row,
    direct_frame_resource_row,
    route_workspace_row,
    unified_complex_frame_resource_row,
    unified_cut_frame_matrix,
    unified_real_frame_resource_row,
)


class UnifiedCompilerTests(unittest.TestCase):
    def test_every_tree_cut_recovers_the_complete_frame(self) -> None:
        rng = np.random.default_rng(260910)
        for n in range(1, 9):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            reference = direct_real_frame(n, theta)
            for t in range(n + 1):
                np.testing.assert_allclose(
                    reconstructed_frame(n, t, theta),
                    reference,
                    atol=1e-12,
                    rtol=0.0,
                )
                np.testing.assert_allclose(
                    unified_cut_frame_matrix(n, t, theta),
                    reference,
                    atol=1e-12,
                    rtol=0.0,
                )

    def test_arbitrary_phase_diagonal_is_exactly_one_ucg(self) -> None:
        rng = np.random.default_rng(260911)
        for n in range(1, 10):
            phases = rng.uniform(-2.0, 2.0, size=1 << n)
            expected = np.diag(np.exp(1j * phases))
            blocks = diagonal_ucg_blocks(phases)
            self.assertEqual(len(blocks), 1 << (n - 1))
            np.testing.assert_allclose(
                diagonal_ucg_matrix(phases),
                expected,
                atol=1e-12,
                rtol=0.0,
            )
            np.testing.assert_allclose(
                diagonal_ucg_matrix(phases, inverse=True),
                expected.conj().T,
                atol=1e-12,
                rtol=0.0,
            )

    def test_one_ucg_diagonal_composes_to_the_complex_frame(self) -> None:
        rng = np.random.default_rng(260912)
        for n in range(1, 8):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            phases = rng.uniform(-1.5, 1.5, size=1 << n)
            np.testing.assert_allclose(
                diagonal_ucg_matrix(phases) @ direct_real_frame(n, theta),
                complex_frame_matrix(theta, phases),
                atol=1e-12,
                rtol=0.0,
            )

    def test_controlled_operator_helper_is_exact(self) -> None:
        rng = np.random.default_rng(260913)
        for n in range(1, 6):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            frame = direct_real_frame(n, theta)
            controlled = controlled_unitary(frame)
            dimension = 1 << n
            np.testing.assert_allclose(
                controlled[:dimension, :dimension],
                np.eye(dimension),
                atol=1e-12,
                rtol=0.0,
            )
            np.testing.assert_allclose(
                controlled[dimension:, dimension:],
                frame,
                atol=1e-12,
                rtol=0.0,
            )
            np.testing.assert_allclose(
                controlled.conj().T @ controlled,
                np.eye(2 * dimension),
                atol=1e-12,
                rtol=0.0,
            )

    def test_direct_compiler_respects_workspace_endpoints(self) -> None:
        for n in range(1, 30):
            zero = direct_frame_resource_row(n, 0)
            self.assertEqual(zero.workspace_used_upper_bound, 0)
            self.assertEqual(zero.mode, "strict-zero-full-width-ucg")
            for ancillas in (1, 2, n, 4 * n):
                row = direct_frame_resource_row(n, ancillas)
                self.assertEqual(row.workspace_used_upper_bound, ancillas)
                self.assertEqual(row.mode, "direct-flagged-ucg")
                controlled = direct_frame_resource_row(
                    n, ancillas, controlled=True
                )
                self.assertEqual(controlled.workspace_used_upper_bound, ancillas)
                self.assertGreaterEqual(
                    controlled.total_depth_proxy,
                    row.total_depth_proxy,
                )

    def test_unified_workspace_ledger_on_broad_grid(self) -> None:
        for n in range(1, 65):
            N = 1 << n
            budgets = sorted(
                {
                    0,
                    1,
                    n,
                    4 * n - 1,
                    4 * n,
                    max(1, N // max(1, n * n)),
                    max(1, N // n),
                    N,
                    2 * N,
                    8 * N,
                    *[1 << power for power in range(0, n + 3)],
                }
            )
            for ancillas in budgets:
                real = unified_real_frame_resource_row(n, ancillas)
                self.assertLessEqual(
                    real.workspace_used_upper_bound,
                    ancillas,
                )
                cut = choose_routed_cut(n, ancillas)
                if real.mode == "tree-decoder-routed-subframes":
                    self.assertIsNotNone(cut)
                    assert cut is not None
                    route = route_workspace_row(n, cut)
                    self.assertLessEqual(
                        route.exact_complete_peak_ancillas,
                        ancillas,
                    )
                    self.assertGreaterEqual(ancillas, 4 * n)
                else:
                    self.assertIsNone(cut)

                complex_row = unified_complex_frame_resource_row(n, ancillas)
                self.assertLessEqual(
                    complex_row.workspace_used_upper_bound,
                    ancillas,
                )
                diagonal = diagonal_ucg_resource_row(n, ancillas)
                self.assertEqual(
                    diagonal.workspace_used_upper_bound,
                    ancillas,
                )

    def test_resource_proxies_remain_uniformly_bounded(self) -> None:
        # This is a regression diagnostic for the transparent term ledger. The
        # asymptotic theorem is proved in the documentation, not by fitting.
        worst_depth = (0.0, None)
        worst_size = (0.0, None)
        for n in range(2, 81):
            N = 1 << n
            budgets = sorted(
                {
                    1,
                    n,
                    4 * n - 1,
                    4 * n,
                    max(1, N // (n * n)),
                    max(1, N // n),
                    N,
                    2 * N,
                    8 * N,
                    *[1 << power for power in range(0, n + 4)],
                }
            )
            for ancillas in budgets:
                row = unified_real_frame_resource_row(n, ancillas)
                depth_ratio = (
                    row.total_depth_proxy / row.optimal_qsp_depth_proxy
                )
                size_ratio = row.total_size_proxy / N
                if depth_ratio > worst_depth[0]:
                    worst_depth = (
                        depth_ratio,
                        (n, ancillas, row.mode),
                    )
                if size_ratio > worst_size[0]:
                    worst_size = (
                        size_ratio,
                        (n, ancillas, row.mode),
                    )
        self.assertLess(
            worst_depth[0],
            64.0,
            msg=f"worst depth proxy: {worst_depth}",
        )
        self.assertLess(
            worst_size[0],
            32.0,
            msg=f"worst size proxy: {worst_size}",
        )


if __name__ == "__main__":
    unittest.main()
