"""CP28 exact finite checks for a shared capped-geometric lowering source.

Uses Q(sqrt(2), i) arithmetic. These are finite circuit/block-identity fixtures,
not a synthesizer, an asymptotic resource proof, or a universal theorem test.
The M=4, Q=J=2, p=1/2 fixtures and freely chosen digit tables test the general
local algebra, not production M=4J or the tightened-coarse normalization budget.
In particular, f_0 may be one here; production residuals make f_0 zero.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROJECT = HERE
sys.path.insert(0, str(PROJECT))
from geometric_reflection_checks import C, ZERO, ONE, IMAG, geometric_column, identity, multiply, dagger, matrix_digest

INV_SQRT2 = C(0, F(1, 2))
# (source index, data, mode, entry, digit, underflow, matrix-unit failure,
#  zero-digit failure, history counter). Source is deliberately absent from F.
SRC, DATA, MODE, ENTRY, DIGIT, UNDER, MATRIX_FAIL, ZERO_FAIL, COUNTER = range(9)
LOCAL = (MODE, ENTRY, DIGIT, UNDER, MATRIX_FAIL, ZERO_FAIL)
M = 4
Q = J = 2
P = F(1, 2)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def replace(basis, field, value):
    out = list(basis)
    out[field] = value
    return tuple(out)


def tidy(state):
    return {key: value for key, value in state.items() if value != ZERO}


def accum(state, key, value):
    state[key] = state.get(key, ZERO) + value


def hadamard(state, field):
    out = {}
    for basis, value in state.items():
        old = basis[field]
        accum(out, replace(basis, field, 0), INV_SQRT2 * value)
        accum(out, replace(basis, field, 1), (-1 if old else 1) * INV_SQRT2 * value)
    return tidy(out)


def source_pair_h(state, left, right):
    out = {}
    for basis, value in state.items():
        old = basis[SRC]
        if old not in (left, right):
            accum(out, basis, value)
        else:
            accum(out, replace(basis, SRC, left), INV_SQRT2 * value)
            accum(out, replace(basis, SRC, right), (-1 if old == right else 1) * INV_SQRT2 * value)
    return tidy(out)


def prepare_source(state, inverse=False):
    pairs = [(0, 1), (1, 2), (2, 3)]
    for left, right in (reversed(pairs) if inverse else pairs):
        state = source_pair_h(state, left, right)
    return state


def shift_basis(j, flag, d, size, inverse=False, omit_underflow=False):
    # Every representable invalid offset has a fixed zero-contraction extension.
    if d >= size:
        return j, flag ^ 1
    if inverse:
        j = (j + d) % size
        return j, flag ^ (int(j < d) if not omit_underflow else 0)
    flag ^= int(j < d) if not omit_underflow else 0
    return (j - d) % size, flag


# entry gives (x,y,phase); tables indexed [entry][digit].
FIXTURES = (
    {"entries": ((1, 0, IMAG), (0, 1, -ONE)), "bits": ((1, 1), (0, 1))},
    {"entries": ((0, 1, -IMAG), (1, 0, ONE)), "bits": ((1, 0), (1, 1))},
    {"entries": ((0, 0, IMAG), (1, 1, -IMAG)), "bits": ((0, 1), (1, 1))},
)


def select(state, stage, inverse=False, omit_zero=False, omit_underflow=False):
    out = {}
    fixture = FIXTURES[stage]
    for basis, value in state.items():
        if basis[MODE] != 0:
            accum(out, basis, value)
            continue
        ell, k = basis[ENTRY], basis[DIGIT]
        if not fixture["bits"][ell][k]:
            target = basis if omit_zero else replace(basis, ZERO_FAIL, basis[ZERO_FAIL] ^ 1)
            accum(out, target, value)
            continue
        x, y, phase = fixture["entries"][ell]
        target = list(basis)
        if inverse:
            target[SRC], target[UNDER] = shift_basis(target[SRC], target[UNDER], 2*k, M, True, omit_underflow)
            target[DATA] ^= x ^ y
            target[MATRIX_FAIL] ^= int(target[DATA] != y)
            value *= phase.conj()
        else:
            target[MATRIX_FAIL] ^= int(target[DATA] != y)
            target[DATA] ^= x ^ y
            target[SRC], target[UNDER] = shift_basis(target[SRC], target[UNDER], 2*k, M, False, omit_underflow)
            value *= phase
        accum(out, tuple(target), value)
    return tidy(out)


def kernel(state, stage, inverse=False, omit_zero=False, omit_underflow=False):
    for field in (MODE, ENTRY, DIGIT):
        state = hadamard(state, field)
    state = select(state, stage, inverse, omit_zero, omit_underflow)
    for field in (DIGIT, ENTRY, MODE):
        state = hadamard(state, field)
    return state


def history(state, modulus, inverse=False, tested=LOCAL):
    out = {}
    for basis, value in state.items():
        failed = any(basis[field] for field in tested)
        count = (basis[COUNTER] + (-1 if inverse else 1) * int(failed)) % modulus
        accum(out, replace(basis, COUNTER, count), value)
    return tidy(out)


def stream(state, stages, modulus, inverse=False, tested=LOCAL):
    if inverse:
        for offset in reversed(range(len(stages))):
            stage = stages[offset]
            state = kernel(state, stage, True)
            if offset != 0:
                state = history(state, modulus, True, tested)
    else:
        for offset, stage in enumerate(stages):
            state = kernel(state, stage)
            if offset + 1 < len(stages):
                state = history(state, modulus, tested=tested)
    return state


def basis0(source, data):
    return (source, data, 0, 0, 0, 0, 0, 0, 0)


def project(state, clean_counter=True):
    return {basis: value for basis, value in state.items()
            if all(basis[field] == 0 for field in LOCAL) and (not clean_counter or basis[COUNTER] == 0)}


def block_from_apply(apply, dimension=2*M):
    columns = []
    for col in range(dimension):
        actual = project(apply({basis0(col//2, col%2): ONE}))
        columns.append([actual.get(basis0(row//2, row%2), ZERO) for row in range(dimension)])
    return [list(row) for row in zip(*columns)]


def expected_block(stage, source_factored=False):
    dim = 2 if source_factored else 2*M
    result = [[(1-P) * value for value in row] for row in identity(dim)]
    fixture = FIXTURES[stage]
    for ell, (x, y, phase) in enumerate(fixture["entries"]):
        for k in range(J):
            if not fixture["bits"][ell][k]:
                continue
            coeff = P / (Q*J) * phase
            if source_factored:
                result[x][y] += F(1, 1 << k) * coeff
            else:
                for j in range(2*k, M):
                    result[2*(j-2*k)+x][2*j+y] += coeff
    return result


def state_norm2(state):
    return sum((value.conj()*value for value in state.values()), ZERO)


def check_shifts():
    records = []
    permutation_cases = defect_cases = invalid_cases = 0
    for size in (2, 4, 8, 16):
        g = geometric_column(size)
        require(sum((a*a.conj() for a in g), ZERO) == ONE, "source normalized")
        offset_limit = 2*size
        for d in range(offset_limit):
            mapped = set()
            for j, flag in product(range(size), (0, 1)):
                out = shift_basis(j, flag, d, size)
                require(shift_basis(*out, d, size, inverse=True) == (j, flag), "actual inverse on arbitrary incoming shift flags")
                mapped.add(out)
                permutation_cases += 1
            require(len(mapped) == 2*size, "shift extension is a full permutation")
            # Projection of flag zero agrees with truncated lowering, including invalid offsets.
            actual = [ZERO] * size
            for j, value in enumerate(g):
                out, flag = shift_basis(j, 0, d, size)
                if flag == 0:
                    actual[out] += value
            expected = [g[j+d] if j+d < size else ZERO for j in range(size)]
            require(actual == expected, "accepted shift agrees with S^d")
            exponent = d
            eigenvalue = C(F(1, 1 << (exponent//2))) if exponent % 2 == 0 else C(0, F(1, 1 << ((exponent+1)//2)))
            defect = sum(((a-eigenvalue*b).conj()*(a-eigenvalue*b) for a, b in zip(actual, g)), ZERO)
            if d == 0:
                require(defect == ZERO, "zero shift has no defect")
            elif d < size:
                require(defect == C(F(4, 1 << size), F(-2, 1 << size)), "uniform capped-source shift defect")
                defect_cases += 1
            else:
                require(defect == C(F(1, 1 << d)), "invalid shift is zero with eigenvector comparison norm 2^-d")
                invalid_cases += 1
        records.append({"M": size, "valid_nonzero_offsets": size-1, "offset_codes_checked": offset_limit})
    # Omitting overflow probability changes the advertised uniform defect.
    uncapped = geometric_column(4, capped=False)
    bad = sum(((uncapped[j+1] if j+1 < 4 else ZERO)-INV_SQRT2*uncapped[j]).conj()*
              ((uncapped[j+1] if j+1 < 4 else ZERO)-INV_SQRT2*uncapped[j]) for j in range(4))
    require(bad != C(F(4, 16), F(-2, 16)), "incorrect overflow convention detected")
    return {"fixtures": records, "permutation_input_cases": permutation_cases,
            "valid_nonzero_defects": defect_cases, "invalid_offset_defects": invalid_cases}


def check_kernels():
    records = []
    inverse_columns = 0
    for stage in range(3):
        actual = block_from_apply(lambda state: kernel(state, stage))
        expected = expected_block(stage)
        require(actual == expected, "actual Bdag SELECT B accepted block equals shifted matrix-unit sum")
        # All computational inputs, including arbitrary failure flags; counter is a spectator.
        for source, data, mode, entry, digit, uf, mf, zf in product(range(M), *((0, 1),)*7):
            basis = (source, data, mode, entry, digit, uf, mf, zf, 0)
            state = kernel({basis: ONE}, stage)
            require(kernel(state, stage, inverse=True) == {basis: ONE}, "full local-kernel actual inverse")
            inverse_columns += 1
        g = geometric_column(M)
        A = expected_block(stage, True)
        errors = []
        for data in (0, 1):
            initial = {basis0(source, data): value for source, value in enumerate(g)}
            actual_state = project(kernel(initial, stage))
            target = {basis0(source, row): value*A[row][data] for source, value in enumerate(g) for row in (0, 1)}
            errors.append(tidy({key: actual_state.get(key, ZERO)-target.get(key, ZERO) for key in set(actual_state)|set(target)}))
        gram = [[sum((errors[a].get(key, ZERO).conj()*errors[b].get(key, ZERO) for key in set(errors[a])|set(errors[b])), ZERO)
                 for b in (0, 1)] for a in (0, 1)]
        # J=2 makes every nonzero shift the same d=2, so the error factors exactly.
        R = [[ZERO for _ in range(2)] for _ in range(2)]
        for ell, (x, y, phase) in enumerate(FIXTURES[stage]["entries"]):
            if FIXTURES[stage]["bits"][ell][1]:
                R[x][y] += P/(Q*J)*phase
        delta2 = C(F(4, 16), F(-2, 16))
        expected_gram = [[delta2*value for value in row] for row in multiply(dagger(R), R)]
        require(gram == expected_gram, "initialized-source factorization error Gram matrix")
        records.append({"stage": stage, "accepted_block_sha256": matrix_digest(actual),
                        "factor_target_sha256": matrix_digest(A), "error_gram": [[x.serialize() for x in row] for row in gram]})
    bad_zero = block_from_apply(lambda state: kernel(state, 0, omit_zero=True))
    bad_under = block_from_apply(lambda state: kernel(state, 0, omit_underflow=True))
    require(bad_zero != expected_block(0), "omitting active zero-digit failure flag changes accepted block")
    require(bad_under != expected_block(0), "omitting underflow flag changes lowering into a cyclic shift")
    return {"fixtures": records, "full_inverse_columns": inverse_columns,
            "initialized_accepted_block_columns": 3*2*M,
            "negative_controls": ["omitted_zero_digit_flag", "omitted_underflow_flag", "wrong_overflow_probability"]}


def check_streams():
    records = []
    for stages, modulus in (((0, 1), 2), ((0, 1, 2), 4)):
        expected = identity(2*M)
        for stage in stages:
            expected = multiply(expected_block(stage), expected)
        actual = block_from_apply(lambda state: stream(state, stages, modulus))
        require(actual == expected, "nonwrapping history gives product of source-system accepted blocks")
        initialized_columns = []
        for data in (0, 1):
            initial = {basis0(0, data): ONE}
            prepared = prepare_source(initial)
            require(prepared == {basis0(source, data): value for source, value in enumerate(geometric_column(M))}, "one actual preparation produces capped source")
            require(prepare_source(prepared, inverse=True) == initial, "source preparation actual inverse")
            evolved = stream(prepared, stages, modulus)
            require(stream(evolved, stages, modulus, inverse=True) == prepared, "actual streamed inverse on prepared source")
            # Gdag is applied only after all kernels. The final source projection
            # is the contraction <g| product(K_j) |g>, not a per-stage reset.
            final = project(prepare_source(evolved, inverse=True))
            final_values = [final.get(basis0(0, row), ZERO) for row in (0, 1)]
            g = geometric_column(M)
            expected_values = [sum((g[sr].conj()*expected[2*sr+row][2*sc+data]*g[sc]
                                   for sr in range(M) for sc in range(M)), ZERO) for row in (0, 1)]
            require(final_values == expected_values, "single preparation and final inverse contract the full shifted block product")
            initialized_columns.append([x.serialize() for x in final_values])
        records.append({"stages": list(stages), "counter_modulus": modulus,
                        "accepted_product_sha256": matrix_digest(actual),
                        "one_preparation_final_clean_columns": initialized_columns})
    # A final workspace test alone permits amplitude to leave and reenter the
    # shared clean workspace. It must not be mistaken for a block product.
    no_history = block_from_apply(lambda state: stream(state, (0, 1), 1))
    true_product = multiply(expected_block(1), expected_block(0))
    require(no_history != true_product, "omitting history admits returned failures")
    flags_only = (UNDER, MATRIX_FAIL, ZERO_FAIL)
    missing_labels = block_from_apply(lambda state: stream(state, (0, 1), 2, tested=flags_only))
    require(missing_labels != true_product, "omitting unprepared mode/entry/digit labels from F admits returned failures")
    wrapped = block_from_apply(lambda state: stream(state, (0, 1, 2), 2))
    true_three = multiply(expected_block(2), true_product)
    require(wrapped != true_three, "counter wraparound admits histories with two prior failures")
    return {"fixtures": records, "accepted_product_columns": 2*2*M,
            "actual_inverse_prepared_columns": 4,
            "negative_controls": ["no_failure_history", "missing_unprepared_labels_from_F", "counter_wraparound"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "results" / "shift_kernel_checks.json")
    args = parser.parse_args()
    receipt = {"checkpoint": 28, "status": "passed", "arithmetic": "exact Q(sqrt(2),i), stdlib fractions",
               "scope": "Finite explicit unitary fixtures and exact identities; no compiled gate counts or universal proof inferred.",
               "fixture_limit": "M=4,Q=J=2,p=1/2 and arbitrary digits (including f_0=1) test the general local identity, not production M=4J, tightened-coarse residuals, bounded normalization, or an emitted outer OAA.",
               "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "helper_sha256": sha256((PROJECT / "geometric_reflection_checks.py").read_bytes()).hexdigest(),
               "shifts": check_shifts(), "kernels": check_kernels(), "streaming": check_streams()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(args.output),
                      "shift_permutation_inputs": receipt["shifts"]["permutation_input_cases"],
                      "local_inverse_columns": receipt["kernels"]["full_inverse_columns"],
                      "streamed_block_columns": receipt["streaming"]["accepted_product_columns"]}))


if __name__ == "__main__":
    main()
