from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.optimal_parallel import (
    choose_routed_cut,
    coherent_route_permutation,
    optimal_qsp_depth_proxy,
    optimality_plan_row,
    route_workspace_ledger,
    routed_frame_size_proxy,
    routed_tail_action_small,
    subtree_angle_indices,
    tail_block_diagonal_frame,
    tail_block_residual,
)
from compiler_robust_hopf.ancilla_depth import tail_frame


class OptimalParallelTests(unittest.TestCase):
    def test_tail_is_direct_sum_of_subtree_frames(self) -> None:
        rng = np.random.default_rng(260906)
        for n in range(1, 9):
            theta = rng.uniform(-1.1, 1.1, size=(1 << n) - 1)
            for t in range(n + 1):
                np.testing.assert_allclose(
                    tail_block_diagonal_frame(n, t, theta),
                    tail_frame(n, t, theta),
                    atol=1e-12,
                    rtol=0.0,
                )
                self.assertLessEqual(tail_block_residual(n, t, theta), 1e-12)

    def test_subtree_angle_partition_is_exact(self) -> None:
        for n in range(1, 13):
            for t in range(n + 1):
                observed: list[int] = []
                for prefix in range(1 << t):
                    observed.extend(subtree_angle_indices(n, t, prefix))
                expected = list(range((1 << t) - 1, (1 << n) - 1))
                self.assertEqual(sorted(observed), expected)
                self.assertEqual(len(observed), len(set(observed)))

    def test_router_is_a_reversible_basis_permutation(self) -> None:
        for t, s in ((1, 1), (1, 2), (2, 1)):
            forward = coherent_route_permutation(t, s)
            backward = coherent_route_permutation(t, s, inverse=True)
            identity = np.arange(forward.size, dtype=np.int64)
            np.testing.assert_array_equal(forward[backward], identity)
            np.testing.assert_array_equal(backward[forward], identity)
            self.assertEqual(len(np.unique(forward)), forward.size)

    def test_routed_parallel_subframes_equal_tail_operator(self) -> None:
        rng = np.random.default_rng(260907)
        for n, t in ((2, 1), (3, 1), (3, 2)):
            theta = rng.uniform(-0.9, 0.9, size=(1 << n) - 1)
            state = rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)
            state /= np.linalg.norm(state)
            routed, leakage = routed_tail_action_small(n, t, theta, state)
            expected = tail_frame(n, t, theta) @ state
            np.testing.assert_allclose(routed, expected, atol=1e-12, rtol=0.0)
            self.assertLessEqual(leakage, 1e-12)

    def test_workspace_ledger_fits_simple_envelope(self) -> None:
        for n in range(2, 41):
            for t in range(1, n):
                row = route_workspace_ledger(n, t)
                self.assertLessEqual(
                    row.exact_peak_upper_bound, row.simple_envelope
                )
                self.assertEqual(row.branches, 1 << t)
                self.assertEqual(row.suffix_qubits, n - t)
                self.assertLessEqual(row.prefix_compiler_ancillas, row.simple_envelope)
                self.assertLessEqual(row.tail_peak_ancillas, row.simple_envelope)

    def test_cut_is_maximal_and_uses_no_more_than_budget(self) -> None:
        for n in range(2, 65):
            N = 1 << n
            budgets = sorted(
                {
                    0,
                    1,
                    n,
                    4 * n - 1,
                    4 * n,
                    max(1, N // (n * n)),
                    max(1, N // n),
                    N,
                    2 * N,
                    8 * N,
                    *[1 << power for power in range(0, n + 3)],
                }
            )
            for budget in budgets:
                cut = choose_routed_cut(n, budget)
                if cut is None:
                    self.assertLess(budget, 4 * n)
                    continue
                row = route_workspace_ledger(n, cut)
                self.assertLessEqual(row.exact_peak_upper_bound, budget)
                self.assertLessEqual(row.simple_envelope, budget)
                if cut < n - 1:
                    self.assertGreater(
                        route_workspace_ledger(n, cut + 1).simple_envelope,
                        budget,
                    )

    def test_routed_proxy_remains_constant_factor_on_broad_grid(self) -> None:
        # This is a diagnostic of the term ledger, not a numerical proof of an
        # asymptotic theorem. The proof is recorded separately.
        for n in range(2, 81):
            N = 1 << n
            budgets = sorted(
                {
                    4 * n,
                    max(4 * n, N // (n * n)),
                    max(4 * n, N // n),
                    N,
                    2 * N,
                    8 * N,
                    *[1 << power for power in range(0, n + 4)],
                }
            )
            for budget in budgets:
                cut = choose_routed_cut(n, budget)
                if cut is None:
                    continue
                plan = optimality_plan_row(n, budget)
                self.assertEqual(plan.mode, "routed-parallel-subframes")
                self.assertLessEqual(plan.used_ancillas_upper_bound, budget)
                self.assertLessEqual(
                    plan.total_depth_proxy,
                    64 * optimal_qsp_depth_proxy(n, budget),
                )
                self.assertLessEqual(routed_frame_size_proxy(n, cut), 16 * N)

    def test_zero_and_positive_workspace_are_not_conflated(self) -> None:
        for n in range(2, 16):
            zero = optimality_plan_row(n, 0)
            self.assertEqual(zero.mode, "audited-low-workspace")
            self.assertEqual(zero.requested_ancillas, 0)
            self.assertEqual(zero.used_ancillas_upper_bound, 1)
            for budget in (1, 2, 3, 4 * n - 1, 4 * n, 1 << n):
                positive = optimality_plan_row(n, budget)
                self.assertLessEqual(positive.used_ancillas_upper_bound, budget)


if __name__ == "__main__":
    unittest.main()
