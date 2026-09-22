"""CP28 finite exact checks of shift-kernel scales, budgets, and support.

Only integers and Fraction are used.  The square-root source-tail constant is
bounded above by two.  These checks do not synthesize gates, count actual gates,
prove asymptotic bounds by sampling, or test the full shift-kernel unitary.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceil_log2(value):
    require(isinstance(value, int) and value > 0, "positive integer logarithm input")
    return (value - 1).bit_length()


def pow2(exponent):
    return F(1 << exponent) if exponent >= 0 else F(1, 1 << -exponent)


def schedule(n):
    """Retained height-one greedy partition in reverse construction order."""
    blocks, covered = [(0, 1)], 1
    while covered < n:
        exponent, remaining = covered // 2, n - covered
        height = remaining if exponent >= ceil_log2(remaining) else 1 << exponent
        blocks.append((covered, height))
        covered += height
    return blocks


def padded_domains(n):
    return [32 * (1 << (n - depth)) * (1 << ceil_log2(height + 1))
            for depth, height in schedule(n)]


def parameters(L, R):
    J = 1 << ceil_log2(L + 8)
    M = 4 * J
    p = pow2(-ceil_log2(8 * R))
    return J, M, p


def check_scales_and_budgets():
    cases, stage_cases, rounding_cases, interval_cases = [], 0, 0, 0
    for n in (1, 2, 3, 4, 7, 8, 15, 16, 24, 32):
        blocks, Q = schedule(n), padded_domains(n)
        R, Qmax = len(blocks), max(Q)
        for L in sorted({6, 7, 8, 15, 16, 23, 24, 31, 32, 63, 64, 127, 128, 511,
                         min(n ** 3, 512), 1 << min(n, 12)}):
            if L < 6:
                continue
            J, M, p = parameters(L, R)
            eta, c = pow2(-L), (1 - p) ** R
            require(J.bit_count() == M.bit_count() == 1, "J and M are literal powers of two")
            require(L + 8 <= J < 2 * (L + 8), "J has the advertised padded cutoff")
            require(M == 4 * J and M // 2 == 2 * J, "source cutoff has exact integer half")
            require(F(1, 16 * R) < p <= F(1, 8 * R), "dyadic p brackets")
            require(R * p <= F(1, 8), "sum of correction probabilities")
            require(c >= 1 - R * p >= F(7, 8), "Bernoulli bound gives survival mass")
            alpha, mode = 1 / c, 1 / (2 * c)
            require(1 <= alpha <= F(8, 7) < 2, "normalization below two")
            require(F(1, 2) <= mode <= F(4, 7), "final normalizer is a valid probability")
            delta = p / (4 * n * Qmax * J)
            for (_, height), domain in zip(blocks, Q):
                stage_cases += 1
                epsilon = p / ((1 - p) * domain * J)
                require(domain.bit_count() == 1, "actual phase dictionary is padded")
                require(height * delta <= p / (4 * Qmax * J) <= epsilon / 4,
                        "group residual is at most a quarter coefficient scale")
                require((1 - p) * epsilon == p / (domain * J),
                        "binary coefficient multiplier equals the physical uniform probability")
                # All nonnegative phase coefficients fit [0, epsilon/4].
                # The coefficient 0 is preserved literally; omitted small terms
                # are covered by the same absolute error, with no division by them.
                unit = pow2(1 - J)
                ratios = [F(0), F(1, 4), F(1, 8), F(1, 7), F(1, 12), unit / 2,
                          min(F(1, 4), unit), F(1, 4) - unit / 3]
                for ratio in ratios:
                    require(0 <= ratio <= F(1, 4), "rounding fixture is admitted")
                    numerator = (ratio / unit).numerator // (ratio / unit).denominator
                    digits = [(numerator >> (J - 1 - k)) & 1 for k in range(J)]
                    rounded_ratio = sum((bit * pow2(-k) for k, bit in enumerate(digits)), F(0))
                    require(rounded_ratio == numerator * unit, "literal digit positions reconstruct truncation")
                    require(0 <= epsilon * (ratio - rounded_ratio) < epsilon * unit,
                            "one phase coefficient absolute tail bound")
                    require(ratio != 0 or all(bit == 0 for bit in digits), "structural zero is not rounded up")
                    rounding_cases += 1
                    # A certified enclosure can straddle an exact binary-grid
                    # boundary. Round its lower endpoint, without querying an
                    # exact real comparison oracle at that boundary.
                    lower, upper = max(F(0), ratio - unit / 2), min(F(1, 4), ratio + unit / 2)
                    require(lower <= ratio <= upper and upper - lower <= unit,
                            "certified enclosure contains the actual coefficient")
                    lower_units = lower / unit
                    rounded_lower = (lower_units.numerator // lower_units.denominator) * unit
                    require(0 <= rounded_lower <= ratio and ratio - rounded_lower < 2 * unit,
                            "certified lower-enclosure rounding has less than two grid units error")
                    require(ratio != F(1, 4) or rounded_lower < ratio,
                            "fixture crosses an exact binary boundary and still returns a certified lower digit value")
                    interval_cases += 1
            # sqrt(4-2sqrt(2)) < 2, so this rational majorant is conservative.
            source_error = 2 * R * p * pow2(-M // 2)
            digit_error = R * p * pow2(2 - J) / J
            kernel_error = source_error + digit_error
            require(kernel_error <= eta / 128, "summed source and digit errors fit the reserved budget")
            # The physical final mode uses a separate exactly prepared finite
            # dyadic source. A probability error beta changes a block by <=beta.
            beta = eta / 128
            require(mode * c == F(1, 2), "ideal final accepted block is W/2")
            block_error = kernel_error + beta
            require(8 * block_error < eta, "normalization-two complete-error allowance: zeta=2*block_error, complete error<4*zeta")
            cases.append({"n": n, "L": L, "R": R, "J": J, "M": M,
                          "p": str(p), "coarse_precision_bits": ceil_log2(delta.denominator),
                          "kernel_error_over_eta_upper": str(kernel_error / eta)})
    return {"parameter_cases": len(cases), "stage_scale_cases": stage_cases,
            "coefficient_rounding_cases": rounding_cases, "certified_interval_rounding_cases": interval_cases, "cases": cases,
            "source_constant": "sqrt(4-2sqrt(2)) < 2",
            "rounding": "J digits at positions k=0,...,J-1; lower-enclosure floor on mesh 2^(1-J); two-grid-unit conservative tail",
            "scope": "Exact finite scalar budgets. Complete-work propagation and amplification are analytic contracts audited separately."}


def check_domain_and_word_ledger():
    records = []
    for n in (1, 2, 3, 4, 7, 8, 15, 16, 24, 25, 32, 64, 128, 256):
        blocks, domains = schedule(n), padded_domains(n)
        N, R = 1 << n, len(blocks)
        require(sum(height for _, height in blocks) == n, "block heights partition all depths")
        require(sum(domains) <= 320 * N, "retained actual dictionary domains total at most 320N")
        sqrt_majorant = sum((pow2((5 + ceil_log2(height + 1) - depth + 1) // 2)
                              for depth, height in blocks), F(0))
        require(sqrt_majorant <= 64, "dyadic square-root domain majorants total at most 64sqrt(N)")
        # This checks precision bit lengths without allocating the exponentially
        # longer denominator 2^(-L) for the high-n endpoint.
        L = max(6, N)
        J, M, p = parameters(L, R)
        w_proxy = ceil_log2(4 * n * max(domains) * J) + ceil_log2(p.denominator)
        h = 1 + ceil_log2(L + n + 2)
        require(w_proxy <= 12 * (n + h), "coarse precision length fits a constant multiple of n+h")
        require(ceil_log2(M) <= h + 6, "one source address fits O(h)")
        table_domain = J * sum(domains)
        require(table_domain <= 640 * N * (L + 8), "all literal phase-digit lookup positions are O(NL)")
        records.append({"n": n, "R": R, "sum_Q_over_N": str(F(sum(domains), N)),
                        "coarse_precision_proxy_bits": w_proxy, "h": h,
                        "source_index_bits": ceil_log2(M), "digit_position_bits": ceil_log2(J)})
    # Finite instances only: the uniform absorption proof belongs in the note.
    direct_cases = 0
    for n in range(1, 65):
        N = 1 << n
        L = max(1, n ** 3 - 1)
        require(n * n * L <= 256 * N, "sampled direct-splice overhead nL<=16sqrt(NL)")
        direct_cases += 1
    return {"partition_cases": records, "direct_splice_finite_cases": direct_cases,
            "scope": "Analytic cost proxies and exact bit lengths, not emitted T/Clifford counts or new asymptotic proofs."}


def sparse_frame(n, t):
    N = 1 << n
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    rows = [{j: F(1)} for j in range(N)]
    for depth in range(n):
        stride, half = 1 << (n - depth), 1 << (n - depth - 1)
        for prefix in range(1 << depth):
            a, b = prefix * stride, prefix * stride + half
            old_a, old_b = rows[a], rows[b]
            columns = set(old_a) | set(old_b)
            rows[a] = {j: value for j in columns
                       if (value := c * old_a.get(j, 0) - s * old_b.get(j, 0))}
            rows[b] = {j: value for j in columns
                       if (value := s * old_a.get(j, 0) + c * old_b.get(j, 0))}
    return rows, c, s


def check_support_obstruction():
    records = []
    fixtures = [(n, F(1, 8), "algebraic support only") for n in range(1, 7)]
    n = 8
    q = n + 2 * ceil_log2(n) + 7
    fixtures.append((n, pow2(-q), "admissible near-identity endpoint"))
    for n, t, label in fixtures:
        N, (rows, c, s) = 1 << n, sparse_frame(n, t)
        total = sum(len(row) for row in rows)
        off_diagonal = sum(sum(j != i for j in row) for i, row in enumerate(rows))
        require(total == (n + 1) * N, "full frame has exactly (n+1)N supported entries")
        require(off_diagonal == n * N, "full frame has exactly nN off-diagonal entries")
        require(all(row.get(i, 0) for i, row in enumerate(rows)), "all diagonal entries nonzero")
        require(c >= s >= t > 0, "every tree-path factor is at least t")
        minimum = min(abs(value) for row in rows for value in row.values())
        require(minimum >= t ** n, "every nonzero exact frame entry exceeds the path lower bound")
        if label.startswith("admissible"):
            require(4 * t * t / (1 + t * t) <= F(1, 64 * N * n * n) ** 2,
                    "exact squared local operator error meets retained coarse tolerance")
            require(minimum / 2 > pow2(-N), "every normalized supported entry exceeds endpoint error")
        records.append({"n": n, "N": N, "t": str(t), "scope": label,
                        "total_nonzeros": total, "off_diagonal_nonzeros": off_diagonal})
    exponent_cases = []
    for n in range(8, 65):
        q = n + 2 * ceil_log2(n) + 7
        require(q * n + 1 < 1 << n, "retained entry-size exponent is below endpoint precision")
        require(2 * pow2(-q) <= F(1, 64 * (1 << n) * n * n), "local error upper bound is permitted")
        exponent_cases.append(n)
    return {"exact_frame_cases": records, "entry_exponent_cases": len(exponent_cases),
            "scope": "Finite sparse rational frames and exact scalar inequalities. The all-n support obstruction is proved analytically in positive_support.md; no general frame T lower bound is asserted."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results" / "shift_resource_checks.json")
    args = parser.parse_args()
    report = {"checkpoint": 28, "status": "passed", "arithmetic": "integer and Fraction only",
              "scales_and_budgets": check_scales_and_budgets(),
              "domain_and_word_ledger": check_domain_and_word_ledger(),
              "support_obstruction": check_support_obstruction(),
              "source_sha256": {Path(__file__).name: sha256(Path(__file__).read_bytes()).hexdigest()}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "passed", "parameter_cases": report["scales_and_budgets"]["parameter_cases"],
                      "rounding_cases": report["scales_and_budgets"]["coefficient_rounding_cases"],
                      "interval_cases": report["scales_and_budgets"]["certified_interval_rounding_cases"],
                      "sparse_frame_cases": len(report["support_obstruction"]["exact_frame_cases"]),
                      "receipt": str(args.output), "receipt_sha256": sha256(args.output.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
