from __future__ import annotations

import unittest

import numpy as np

from compiler_robust_hopf.frames import (
    complex_frame_matrix,
    direct_addressed_depth_layer,
    direct_real_frame,
    hopf_ry,
    real_frame_matrix,
)
from compiler_robust_hopf.strict_zero_echo import (
    borrowed_half_angle_ucg,
    borrowed_suffix_echo_layer,
    borrowed_suffix_echo_layer_resource_row,
    borrowed_suffix_positions,
    borrowed_suffix_toggle_permutation,
    borrowed_target_echo_permutation,
    echo_algebra_residual,
    echo_complex_frame_residual,
    echo_frame_residual,
    echo_layer_residual,
    echo_sector_action,
    strict_zero_echo_complex_frame,
    strict_zero_echo_complex_resource_row,
    strict_zero_echo_frame_resource_row,
    strict_zero_echo_real_frame,
)


class StrictZeroBorrowedSuffixEchoTests(unittest.TestCase):
    def test_four_sector_echo_table(self) -> None:
        rng = np.random.default_rng(260903)
        for theta in rng.uniform(-3.0, 3.0, size=32):
            for predicate in (0, 1):
                for borrowed in (0, 1):
                    action, final_bit = echo_sector_action(
                        float(theta),
                        predicate=predicate,
                        borrowed_bit=borrowed,
                    )
                    expected = (
                        hopf_ry(float(theta))
                        if predicate == 1 and borrowed == 0
                        else np.eye(2)
                    )
                    np.testing.assert_allclose(
                        action, expected, atol=1e-12, rtol=0.0
                    )
                    self.assertEqual(final_bit, borrowed)

    def test_echo_algebra_identities(self) -> None:
        rng = np.random.default_rng(260904)
        for theta in rng.uniform(-5.0, 5.0, size=64):
            residuals = echo_algebra_residual(float(theta))
            for residual in residuals.values():
                self.assertLessEqual(residual, 1e-12)

    def test_toggle_and_echo_permutations_are_self_inverse(self) -> None:
        for n in range(2, 9):
            for depth in range(n - 1):
                target, borrowed, remaining = borrowed_suffix_positions(n, depth)
                self.assertEqual(target, n - depth - 1)
                self.assertEqual(borrowed, n - depth - 2)
                self.assertEqual(remaining, tuple(range(borrowed)))
                for permutation in (
                    borrowed_suffix_toggle_permutation(n, depth),
                    borrowed_target_echo_permutation(n, depth),
                ):
                    np.testing.assert_allclose(
                        permutation.conj().T @ permutation,
                        np.eye(1 << n),
                        atol=1e-12,
                        rtol=0.0,
                    )
                    np.testing.assert_allclose(
                        permutation @ permutation,
                        np.eye(1 << n),
                        atol=1e-12,
                        rtol=0.0,
                    )

    def test_each_nonfinal_echo_layer_equals_addressed_layer(self) -> None:
        rng = np.random.default_rng(260905)
        for n in range(2, 9):
            for _ in range(2):
                for depth in range(n - 1):
                    angles = rng.uniform(-1.7, 1.7, size=1 << depth)
                    echo = borrowed_suffix_echo_layer(n, depth, angles)
                    direct = direct_addressed_depth_layer(n, depth, angles)
                    np.testing.assert_allclose(
                        echo, direct, atol=1e-12, rtol=0.0
                    )
                    self.assertLessEqual(
                        echo_layer_residual(n, depth, angles), 1e-12
                    )

                    half = borrowed_half_angle_ucg(n, depth, angles)
                    np.testing.assert_allclose(
                        half.conj().T @ half,
                        np.eye(1 << n),
                        atol=1e-12,
                        rtol=0.0,
                    )

    def test_complete_echo_frame_equals_both_frame_constructions(self) -> None:
        rng = np.random.default_rng(260906)
        for n in range(1, 9):
            theta = rng.uniform(-1.2, 1.2, size=(1 << n) - 1)
            echo = strict_zero_echo_real_frame(n, theta)
            np.testing.assert_allclose(
                echo, direct_real_frame(n, theta), atol=1e-12, rtol=0.0
            )
            np.testing.assert_allclose(
                echo, real_frame_matrix(theta), atol=1e-12, rtol=0.0
            )
            self.assertLessEqual(echo_frame_residual(n, theta), 1e-12)
            np.testing.assert_allclose(
                echo.conj().T @ echo,
                np.eye(1 << n),
                atol=1e-12,
                rtol=0.0,
            )

    def test_inverse_and_complex_frame_corollary(self) -> None:
        rng = np.random.default_rng(260907)
        for n in range(1, 8):
            theta = rng.uniform(-1.0, 1.0, size=(1 << n) - 1)
            phase = rng.uniform(-2.0, 2.0, size=1 << n)
            real = strict_zero_echo_real_frame(n, theta)
            np.testing.assert_allclose(
                real.conj().T,
                direct_real_frame(n, theta).conj().T,
                atol=1e-12,
                rtol=0.0,
            )
            complex_echo = strict_zero_echo_complex_frame(theta, phase)
            np.testing.assert_allclose(
                complex_echo,
                complex_frame_matrix(theta, phase),
                atol=1e-12,
                rtol=0.0,
            )
            self.assertLessEqual(
                echo_complex_frame_residual(theta, phase), 1e-12
            )

    def test_resource_ledger_has_zero_workspace_and_optimal_order(self) -> None:
        worst_real_depth_ratio = (0.0, None)
        worst_complex_depth_ratio = (0.0, None)
        worst_real_size_ratio = (0.0, None)
        worst_complex_size_ratio = (0.0, None)

        for n in range(1, 257):
            N = 1 << n
            real = strict_zero_echo_frame_resource_row(n)
            complex_row = strict_zero_echo_complex_resource_row(n)
            self.assertEqual(real.clean_ancillas, 0)
            self.assertEqual(complex_row.clean_ancillas, 0)
            self.assertEqual(real.nonfinal_layers, n - 1)
            self.assertEqual(real.half_angle_ucgs, 2 * (n - 1))
            self.assertEqual(real.predicate_toggles, 4 * (n - 1))
            self.assertEqual(real.target_echo_cnots, 2 * (n - 1))
            self.assertEqual(
                real.total_depth_proxy,
                real.nonfinal_depth_proxy + real.final_ucg_depth_proxy,
            )
            self.assertEqual(
                real.total_size_proxy,
                real.nonfinal_size_proxy + real.final_ucg_size_proxy,
            )
            self.assertEqual(
                complex_row.total_depth_proxy,
                complex_row.real_depth_proxy + complex_row.diagonal_depth_proxy,
            )
            self.assertEqual(
                complex_row.total_size_proxy,
                complex_row.real_size_proxy + complex_row.diagonal_size_proxy,
            )

            real_depth_ratio = (
                real.total_depth_proxy / real.optimal_qsp_depth_proxy
            )
            complex_depth_ratio = (
                complex_row.total_depth_proxy
                / complex_row.optimal_qsp_depth_proxy
            )
            real_size_ratio = real.total_size_proxy / N
            complex_size_ratio = complex_row.total_size_proxy / N
            if real_depth_ratio > worst_real_depth_ratio[0]:
                worst_real_depth_ratio = (real_depth_ratio, n)
            if complex_depth_ratio > worst_complex_depth_ratio[0]:
                worst_complex_depth_ratio = (complex_depth_ratio, n)
            if real_size_ratio > worst_real_size_ratio[0]:
                worst_real_size_ratio = (real_size_ratio, n)
            if complex_size_ratio > worst_complex_size_ratio[0]:
                worst_complex_size_ratio = (complex_size_ratio, n)

        self.assertLess(
            worst_real_depth_ratio[0],
            12.0,
            msg=f"worst real depth ratio: {worst_real_depth_ratio}",
        )
        self.assertLess(
            worst_complex_depth_ratio[0],
            13.0,
            msg=f"worst complex depth ratio: {worst_complex_depth_ratio}",
        )
        self.assertLess(
            worst_real_size_ratio[0],
            8.0,
            msg=f"worst real size ratio: {worst_real_size_ratio}",
        )
        self.assertLess(
            worst_complex_size_ratio[0],
            9.0,
            msg=f"worst complex size ratio: {worst_complex_size_ratio}",
        )

    def test_layer_resource_widths_and_zero_control_endpoint(self) -> None:
        for n in range(2, 65):
            for depth in range(n - 1):
                row = borrowed_suffix_echo_layer_resource_row(n, depth)
                self.assertEqual(row.clean_ancillas, 0)
                self.assertEqual(row.half_angle_ucg_width, depth + 2)
                self.assertEqual(
                    row.remaining_suffix_controls, n - depth - 2
                )
                self.assertEqual(
                    row.logical_nonidentity_blocks, 1 << depth
                )
                self.assertEqual(
                    row.full_width_logical_blocks, 1 << (n - 1)
                )
                if depth == n - 2:
                    self.assertEqual(row.remaining_suffix_controls, 0)
                    self.assertEqual(row.predicate_depth_proxy, 4)
                    self.assertEqual(row.predicate_size_proxy, 4)


if __name__ == "__main__":
    unittest.main()
