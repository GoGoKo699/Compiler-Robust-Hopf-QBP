"""Exact scalar arithmetic retained for the bounded Gray-source checks.

Q2 and CQ2 are verbatim class extractions from the research modules listed in
PROVENANCE.json. No frame certificate, optimizer, or residual compiler is imported.
Floating display methods are retained for source fidelity; no check uses them.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from functools import total_ordering
import math


@total_ordering
@dataclass(frozen=True)
class Q2:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def parse(x):
        if isinstance(x, Q2):
            return x
        if isinstance(x, (list, tuple)) and len(x) == 2:
            return Q2(F(x[0]), F(x[1]))
        return Q2(F(x))

    def __add__(self, other):
        z = self.parse(other)
        return Q2(self.a + z.a, self.b + z.b)

    __radd__ = __add__

    def __neg__(self):
        return Q2(-self.a, -self.b)

    def __sub__(self, other):
        return self + -self.parse(other)

    def __rsub__(self, other):
        return self.parse(other) + -self

    def __mul__(self, other):
        z = self.parse(other)
        return Q2(self.a*z.a + 2*self.b*z.b, self.a*z.b + self.b*z.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        z = self.parse(other)
        denominator = z.a*z.a - 2*z.b*z.b
        if not denominator:
            raise ZeroDivisionError
        return self*Q2(z.a/denominator, -z.b/denominator)

    def sign(self):
        if not self.b:
            return (self.a > 0) - (self.a < 0)
        if not self.a:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        difference = self.a*self.a - 2*self.b*self.b
        return ((difference > 0) - (difference < 0))*(1 if self.a > 0 else -1)

    def __eq__(self, other):
        try:
            z = self.parse(other)
            return self.a == z.a and self.b == z.b
        except (TypeError, ValueError):
            return False

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __abs__(self):
        return -self if self.sign() < 0 else self

    def record(self):
        return [str(self.a), str(self.b)]

    def display(self):
        return float(self.a) + math.sqrt(2)*float(self.b)


ZERO, ONE = Q2(), Q2(1)


@dataclass(frozen=True)
class CQ2:
    real: Q2 = ZERO
    imag: Q2 = ZERO

    def __post_init__(self):
        object.__setattr__(self, "real", Q2.parse(self.real))
        object.__setattr__(self, "imag", Q2.parse(self.imag))

    @staticmethod
    def parse(x):
        return x if isinstance(x, CQ2) else CQ2(Q2.parse(x))

    def __add__(self, other):
        z = self.parse(other)
        return CQ2(self.real + z.real, self.imag + z.imag)

    __radd__ = __add__

    def __neg__(self):
        return CQ2(-self.real, -self.imag)

    def __sub__(self, other):
        return self + -self.parse(other)

    def __rsub__(self, other):
        return self.parse(other) + -self

    def __mul__(self, other):
        z = self.parse(other)
        return CQ2(self.real*z.real - self.imag*z.imag,
                   self.real*z.imag + self.imag*z.real)

    __rmul__ = __mul__

    def __truediv__(self, other):
        z = self.parse(other)
        return self*z.conj() / z.abs2() if z.imag != ZERO else CQ2(self.real/z.real, self.imag/z.real)

    def conj(self):
        return CQ2(self.real, -self.imag)

    def abs2(self):
        return self.real*self.real + self.imag*self.imag

    def record(self):
        return {"real_qsqrt2": self.real.record(), "imag_qsqrt2": self.imag.record()}

    def display(self):
        return complex(self.real.display(), self.imag.display())


CZ, CO, CI = CQ2(), CQ2(1), CQ2(0, 1)
