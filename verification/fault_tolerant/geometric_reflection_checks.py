"""CP25 finite exact matrix checks; stdlib only, no synthesis/lower-bound proof.

Matrices are over Q(sqrt(2),i). This checks the specific coefficients and small
physical Galois examples used in the accompanying analytic resource argument.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


@dataclass(frozen=True)
class C:
    a: F = F(0)
    b: F = F(0)
    c: F = F(0)
    d: F = F(0)

    def __post_init__(self):
        for name in ("a", "b", "c", "d"):
            object.__setattr__(self, name, F(getattr(self, name)))

    @staticmethod
    def coerce(value):
        return value if isinstance(value, C) else C(value)

    def __add__(self, other):
        other = self.coerce(other)
        return C(self.a+other.a, self.b+other.b, self.c+other.c, self.d+other.d)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        def pair(a, b, e, f):
            return a*e+2*b*f, a*f+b*e
        rr = pair(self.a, self.b, other.a, other.b)
        ii = pair(self.c, self.d, other.c, other.d)
        ri = pair(self.a, self.b, other.c, other.d)
        ir = pair(self.c, self.d, other.a, other.b)
        return C(rr[0]-ii[0], rr[1]-ii[1], ri[0]+ir[0], ri[1]+ir[1])

    __rmul__ = __mul__

    def conj(self):
        return C(self.a, self.b, -self.c, -self.d)

    def sigma(self):
        return C(self.a, -self.b, self.c, -self.d)

    def real_sign(self):
        require(self.c == self.d == 0, "real algebraic comparison")
        if self.b == 0:
            return (self.a > 0)-(self.a < 0)
        if self.a == 0 or self.a*self.b > 0:
            return (self.b > 0)-(self.b < 0)
        difference = self.a*self.a-2*self.b*self.b
        sign = (difference > 0)-(difference < 0)
        return sign if self.a > 0 else -sign

    def absolute(self):
        return -self if self.real_sign() < 0 else self

    def rational(self):
        require(self.b == self.c == self.d == 0, "coefficient is rational")
        return self.a

    def serialize(self):
        return [str(self.a), str(self.b), str(self.c), str(self.d)]


ZERO, ONE, IMAG = C(), C(1), C(0, 0, 1)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def identity(size):
    return [[ONE if i == j else ZERO for j in range(size)] for i in range(size)]


def multiply(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b)) if a[i][k] != ZERO and b[k][j] != ZERO), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]


def dagger(a):
    return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]


def trace_product(a, b):
    return sum((a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a))
                if a[i][j] != ZERO and b[j][i] != ZERO), ZERO)


def tensor(a, b):
    return [[a[i//len(b)][j//len(b[0])]*b[i % len(b)][j % len(b[0])]
             for j in range(len(a[0])*len(b[0]))] for i in range(len(a)*len(b))]


def scale(value, a):
    return [[value*x for x in row] for row in a]


def matrix_digest(matrix):
    return sha256(json.dumps([[x.serialize() for x in row] for row in matrix], separators=(",", ":")).encode()).hexdigest()


I = identity(2)
X = [[ZERO, ONE], [ONE, ZERO]]
Y = [[ZERO, -IMAG], [IMAG, ZERO]]
Z = [[ONE, ZERO], [ZERO, -ONE]]
H = [[C(0, F(1, 2)), C(0, F(1, 2))], [C(0, F(1, 2)), C(0, F(-1, 2))]]
T = [[ONE, ZERO], [ZERO, C(0, F(1, 2), 0, F(1, 2))]]
TDG = dagger(T)
S = [[ONE, ZERO], [ZERO, IMAG]]
PAULIS = {"I": I, "X": X, "Y": Y, "Z": Z}


def geometric_column(size, capped=True):
    column = []
    for j in range(size):
        exponent = size-1 if capped and j == size-1 else j+1
        column.append(C(F(1, 1 << (exponent//2))) if exponent % 2 == 0
                      else C(0, F(1, 1 << ((exponent+1)//2))))
    return column


def reflection(column):
    return [[(ONE if i == j else ZERO)-2*column[i]*column[j].conj()
             for j in range(len(column))] for i in range(len(column))]


def diagonal_z(size, bit=0):
    return [[C(-1 if ((i >> bit) & 1) else 1) if i == j else ZERO
             for j in range(size)] for i in range(size)]


def expectation(column, observable):
    output = multiply(observable, [[x] for x in column])
    return sum((column[i].conj()*output[i][0] for i in range(len(column))), ZERO)


def ptm_coefficient(unitary, p, q):
    evolved = multiply(multiply(unitary, q), dagger(unitary))
    return F(1, len(unitary))*trace_product(p, evolved)


def dyadic_denominator_exponent(value):
    denominator = value.denominator
    exponent = denominator.bit_length()-1
    require(denominator == 1 << exponent, "reduced rational denominator is dyadic")
    return exponent


def check_reflection_matrices():
    records = []
    for size in (4, 8, 16):
        t = size.bit_length()-1
        column, z = geometric_column(size), diagonal_z(size)
        require(sum((x*x.conj() for x in column), ZERO) == ONE, "capped geometric column is normalized")
        matrix = reflection(column)
        require(multiply(matrix, dagger(matrix)) == identity(size), "full reflected matrix is exactly unitary")
        expectation_z = expectation(column, z).rational()
        coefficient = ptm_coefficient(matrix, z, z).rational()
        odd_a = ((1 << (size-2))-1)//3
        require(3*odd_a == (1 << (size-2))-1 and odd_a % 2 == 1, "closed parity numerator is odd integer")
        require(expectation_z == F(odd_a, 1 << (size-2)), "independent full matrix parity expectation")
        require(coefficient == 1-F(4, size)*(1-expectation_z**2), "full matrix normalized PTM identity")
        expected_d = 2*size+t-6
        d = dyadic_denominator_exponent(coefficient)
        require(d == expected_d and coefficient.numerator % 2 == 1, "reduced reflection denominator and odd numerator")
        numerator = (1 << expected_d)-(1 << (2*size-4))+odd_a**2
        require(coefficient == F(numerator, 1 << expected_d) and numerator % 2 == 1, "expanded reflection numerator parity")
        prep_d = dyadic_denominator_exponent(expectation_z)
        require(prep_d == size-2, "preparation expectation reduced denominator")
        require(2*d == 4*size+2*t-12 and 2*prep_d == 2*size-4, "twice-denominator lower-bound expressions")
        records.append({"M": size, "t": t, "z": str(expectation_z), "u": str(coefficient),
                        "reflection_denominator_exponent": d, "reflection_2d_expression": 2*d,
                        "preparation_denominator_exponent": prep_d, "preparation_2d_expression": 2*prep_d,
                        "reflection_matrix_sha256": matrix_digest(matrix)})
    # Additional zero/history bits and an independent source change the full
    # reflection dimension, while preserving the chosen source expectation.
    extension_records = []
    base = geometric_column(4)
    for name, other in (("one_zero_bit", [ONE, ZERO]), ("second_independent_source", geometric_column(4))):
        column = [a*b for a in base for b in other]
        dimension = len(column)
        q = dimension.bit_length()-1
        observable = diagonal_z(dimension, len(other).bit_length()-1)
        matrix = reflection(column)
        parity = expectation(column, observable).rational()
        coefficient = ptm_coefficient(matrix, observable, observable).rational()
        require(parity == F(1, 4), "chosen source parity unaffected by additional source/history register")
        require(coefficient == 1-F(4, dimension)*(1-parity**2), "extended full reflection normalized PTM")
        exponent = dyadic_denominator_exponent(coefficient)
        require(2*exponent == 16+2*q-12, "extended reflection twice-denominator expression")
        extension_records.append({"fixture": name, "source_M": 4, "dimension": dimension,
                                  "q": q, "u": str(coefficient), "denominator_exponent": exponent})
    # Incorrectly omitting the overflow mass destroys normalization and the
    # reflection's involution. Omitting normalized trace changes its denominator.
    bad_column = geometric_column(4, capped=False)
    bad_reflection = reflection(bad_column)
    require(sum((x*x.conj() for x in bad_column), ZERO) != ONE, "ordinary last atom cannot replace overflow")
    require(multiply(bad_reflection, bad_reflection) != identity(4), "incorrect overflow is detected by full matrix involution")
    require(dyadic_denominator_exponent(F(1, 16)*4) != 4, "omitting 1/M PTM normalization changes reduced denominator")
    require((F(1, 16)*(1 << 5)).numerator % 2 == 0, "off-by-one denominator exponent is not least/odd")
    return {"full_matrix_cases": records, "extended_column_cases": extension_records,
            "incorrect_overflow_detected": True, "unnormalized_trace_detected": True,
            "off_by_one_denominator_detected": True}


def gate_matrix(name, target, qubits):
    if name in ("CX", "CZ"):
        require(qubits == 2, "two-qubit fixture gate")
        if name == "CX":
            return [[ONE if i == (j ^ (1 if j & 2 else 0)) else ZERO for j in range(4)] for i in range(4)]
        return [[C(-1 if i == 3 else 1) if i == j else ZERO for j in range(4)] for i in range(4)]
    gate = {"H": H, "S": S, "T": T, "TDG": TDG, "Z": Z}[name]
    if qubits == 1:
        return gate
    return tensor(gate, I) if target == 0 else tensor(I, gate)


def word_matrix(word, qubits, physical_galois=False):
    matrix = identity(1 << qubits)
    for name, target in word:
        matrix = multiply(gate_matrix(name, target, qubits), matrix)
        if physical_galois and name in ("T", "TDG"):
            matrix = multiply(gate_matrix("Z", target, qubits), matrix)
    return matrix


def full_ptm(matrix, qubits):
    paulis = list(PAULIS.items()) if qubits == 1 else [(a+b, tensor(p, q)) for a, p in PAULIS.items() for b, q in PAULIS.items()]
    result = {}
    for q_name, q in paulis:
        evolved = multiply(multiply(matrix, q), dagger(matrix))
        for p_name, p in paulis:
            result[p_name, q_name] = F(1, len(matrix))*trace_product(p, evolved)
    return result


def logical_induced_coefficient(matrix, p, q, initialized):
    density = [[ONE, ZERO], [ZERO, ZERO]] if initialized else scale(F(1, 2), I)
    evolved = multiply(multiply(matrix, tensor(q, density)), dagger(matrix))
    return F(1, 2)*trace_product(tensor(p, I), evolved)


def finite_norm_bound(coefficient, tau, denominator, rational_target):
    require((coefficient-C(1)).real_sign() <= 0 and (coefficient+C(1)).real_sign() >= 0, "physical coefficient bounded by one")
    conjugate = coefficient.sigma()
    require((conjugate-C(1)).real_sign() <= 0 and (conjugate+C(1)).real_sign() >= 0, "physical conjugate coefficient bounded by one")
    difference = coefficient-C(rational_target)
    norm = (difference*difference.sigma()).rational()
    scaled_norm = norm*denominator**2*(1 << tau)
    require(scaled_norm.denominator == 1 and scaled_norm != 0, "finite algebraic norm has nonzero integral numerator at claimed scale")
    separation = F(1, 2*denominator**2*(1 << tau))
    require((difference.absolute()-C(separation)).real_sign() >= 0, "finite conjugate norm separation constant")


def check_physical_galois():
    fixtures = [("T", 1, [("T", 0)]), ("TDG", 1, [("TDG", 0)]),
                ("one_qubit_mixed", 1, [("H", 0), ("T", 0), ("S", 0), ("TDG", 0), ("H", 0)]),
                ("two_qubit_entangling", 2, [("H", 0), ("T", 0), ("CX", 0), ("TDG", 1), ("S", 0), ("CZ", 0), ("H", 1), ("T", 1)])]
    records, norm_checks, induced_checks = [], 0, 0
    nontrivial = False
    for name, qubits, word in fixtures:
        matrix = word_matrix(word, qubits)
        changed = word_matrix(word, qubits, physical_galois=True)
        require(multiply(matrix, dagger(matrix)) == identity(1 << qubits), "fixture matrix unitary")
        ordinary, physical = full_ptm(matrix, qubits), full_ptm(changed, qubits)
        tau = sum(gate in ("T", "TDG") for gate, _ in word)
        for label, coefficient in ordinary.items():
            require(coefficient.c == coefficient.d == 0, "PTM coefficients are real")
            require(coefficient.sigma() == physical[label], "field conjugation equals physical T->ZT and TDG->ZTDG channel")
            nontrivial |= coefficient != coefficient.sigma()
            for size in (4, 8, 16):
                finite_norm_bound(coefficient, tau, 9*size, 1-F(32, 9*size))
                norm_checks += 1
            finite_norm_bound(coefficient, tau, 3, F(1, 3))
            norm_checks += 1
        if qubits == 2:
            for initialized in (False, True):
                for p_name, p in PAULIS.items():
                    for q_name, q in PAULIS.items():
                        direct = logical_induced_coefficient(matrix, p, q, initialized)
                        expansion = ordinary[p_name+"I", q_name+"I"]
                        if initialized:
                            expansion += ordinary[p_name+"I", q_name+"Z"]
                        require(direct == expansion, "initialized/mixed-helper PTM expansion has no extra dyadic denominator")
                        galois_direct = logical_induced_coefficient(changed, p, q, initialized)
                        require(direct.sigma() == galois_direct, "induced coefficient conjugate is physically realized without helper return assumption")
                        for size in (4, 8, 16):
                            finite_norm_bound(direct, tau, 9*size, 1-F(32, 9*size))
                            norm_checks += 1
                        induced_checks += 1
        records.append({"fixture": name, "qubits": qubits, "word": word, "T_or_TDG_count": tau,
                        "full_PTM_entries": len(ordinary), "unitary_matrix_sha256": matrix_digest(matrix),
                        "physical_galois_matrix_sha256": matrix_digest(changed)})
    require(nontrivial, "fixtures exercise nonrational coefficients changed by field conjugation")
    return {"fixtures": records, "nontrivial_field_conjugation_exercised": True,
            "full_PTM_entries_checked": sum(record["full_PTM_entries"] for record in records),
            "initialized_and_mixed_helper_coefficients": induced_checks,
            "finite_algebraic_norm_separation_checks": norm_checks,
            "scope": "Finite physical examples of the identities; not a proof of the general channel lattice or ancillary lower bound."}


def check_exact_tails():
    records, reflection_budgets, preparation_budgets = [], 0, 0
    for size in (4, 8, 16, 32, 64, 128):
        probabilities = [F(1, 1 << (j+1)) for j in range(size-1)]+[F(1, 1 << (size-1))]
        require(sum(probabilities) == 1, "independent rational source normalization")
        parity = sum(((-1)**j*p for j, p in enumerate(probabilities)), F(0))
        coefficient = 1-F(4, size)*(1-parity**2)
        target = 1-F(32, 9*size)
        tail = abs(coefficient-target)
        bound = F(32, 9*size*(1 << size))
        require(tail == bound-F(64, 9*size*(1 << (2*size))), "exact reflection rational tail identity")
        require(tail <= bound, "reflection tail constant 32/(9M)")
        prep_tail = abs(parity-F(1, 3))
        require(prep_tail == F(4, 3*(1 << size)), "exact fresh-source parity tail")
        tested = []
        for precision in sorted({1, 2, size-2, size-1, size, size+1}):
            eta = F(1, 1 << precision)
            reflection_applicable = size >= max(4, precision)
            preparation_applicable = size >= precision+2
            if reflection_applicable:
                require(tail <= eta and 2*eta+tail <= 3*eta, "reflection approximation budget constant three")
                reflection_budgets += 1
            if preparation_applicable:
                require(prep_tail <= eta/3 and 2*eta+prep_tail <= 3*eta, "preparation approximation budget constant three")
                preparation_budgets += 1
            tested.append({"L": precision, "reflection_condition": reflection_applicable,
                           "preparation_condition": preparation_applicable})
        records.append({"M": size, "z": str(parity), "u": str(coefficient),
                        "reflection_tail": str(tail), "reflection_tail_bound": str(bound),
                        "preparation_tail": str(prep_tail), "precision_cases": tested})
    return {"cases": records, "reflection_budget_checks": reflection_budgets,
            "preparation_budget_checks": preparation_budgets,
            "scope": "Exact rational tails and stated numerical constants; no synthesized approximate reflection is supplied."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent/"results"/"geometric_reflection_checks.json")
    output = parser.parse_args().output.resolve()
    report = {"checkpoint": 25, "status": "passed", "arithmetic": "Exact Fraction arithmetic in Q(sqrt(2),i)",
              "scope": "Independent finite full-matrix coefficients, reduced denominators, physical Galois examples and rational tail constants. These tests do not prove the asymptotic lattice theorem, synthesize circuits, or certify an additive lower bound for whole sequences.",
              "reflection_matrices": check_reflection_matrices(), "physical_galois": check_physical_galois(),
              "exact_tails": check_exact_tails(),
              "source_sha256": {Path(__file__).name: sha256(Path(__file__).read_bytes()).hexdigest()}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": "passed", "reflection_matrix_cases": len(report["reflection_matrices"]["full_matrix_cases"]),
                      "PTM_entries": report["physical_galois"]["full_PTM_entries_checked"],
                      "norm_separation_checks": report["physical_galois"]["finite_algebraic_norm_separation_checks"],
                      "receipt": str(output), "receipt_sha256": sha256(output.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
