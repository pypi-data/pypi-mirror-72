from copy import copy
from decimal import Decimal


def digits2str(digits):
    return "".join(str(i) for i in digits)


def tuple2decimal(sign, digits, exponent):
    return Decimal(f"{'-' * sign}{digits2str(digits)}e{exponent}")


def change_digits(digits, num):
    n = len(digits) - 1
    digits[n] += num
    while digits[n] < 0:
        while digits[n] < 0:
            digits[n] += 10
            digits[n - 1] -= 1
        n -= 1
    return digits


class RangeDigit:
    def __init__(self, value, exact=False):
        sign, digits, exponent = Decimal(value).as_tuple()
        if exact or digits == (0,):
            sup = low = digits
        else:
            sup = list(digits) + [5]
            low = change_digits(sup.copy(), -10)
            if sign:
                low, sup = sup, low
            exponent -= 1
        self.low = tuple2decimal(sign, low, exponent)
        self.sup = tuple2decimal(sign, sup, exponent)

    def correct(self):
        if self.low > self.sup:
            self.low, self.sup = self.sup, self.low

    def __neg__(self):
        sd = copy(self)
        sd.low, sd.sup = -sd.sup, -sd.low
        return sd

    def __abs__(self):
        sd = copy(self)
        sd.low = abs(sd.low)
        sd.sup = abs(sd.sup)
        sd.correct()
        return sd

    def __iadd__(self, other):
        if isinstance(other, RangeDigit):
            self.low += other.low
            self.sup += other.sup
        else:
            self.low += other
            self.sup += other
        return self

    def __isub__(self, other):
        if isinstance(other, RangeDigit):
            self.low -= other.sup
            self.sup -= other.low
        else:
            self.low -= other
            self.sup -= other
        return self

    def __imul__(self, other):
        if isinstance(other, RangeDigit):
            if self.low.is_signed() == other.low.is_signed():
                self.low *= other.low
                self.sup *= other.sup
            else:
                self.low *= other.sup
                self.sup *= other.low
        else:
            self.low *= other
            self.sup *= other
        self.correct()
        return self

    def __itruediv__(self, other):
        if isinstance(other, RangeDigit):
            if self.low.is_signed() == other.low.is_signed():
                self.low /= other.sup
                self.sup /= other.low
            else:
                self.low /= other.low
                self.sup /= other.sup
        else:
            self.low /= other
            self.sup /= other
        self.correct()
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, RangeDigit):
            if self.low.is_signed() == other.low.is_signed():
                self.low //= other.sup
                self.sup //= other.low
            else:
                self.low //= other.low
                self.sup //= other.sup
        else:
            self.low //= other
            self.sup //= other
        self.correct()
        return self

    def __add__(self, other):
        sd = copy(self)
        sd += other
        return sd

    def __sub__(self, other):
        sd = copy(self)
        sd -= other
        return sd

    def __mul__(self, other):
        sd = copy(self)
        sd *= other
        return sd

    def __truediv__(self, other):
        sd = copy(self)
        sd /= other
        return sd

    def __floordiv__(self, other):
        sd = copy(self)
        sd //= other
        return sd

    def tostr(self):
        return f"<RangeDigit [{self.low} - {self.sup})>"

    def __repr__(self):
        if self.low.is_signed() != self.sup.is_signed():
            return self.tostr()
        if self.low < 0:
            return "-" + repr(abs(self))
        s0 = str(self.low)
        s1 = str(self.sup)
        s2 = str((self.low + self.sup) / 2)
        lst = []
        for c1, c2 in zip(s1, s2):
            if c1 != c2:
                break
            lst.append(c1)
        n = len(lst)
        if len(s0) > n and lst[n - 1] == s0[n - 1] and s0[n] >= "5":
            lst[n - 1] = chr(ord(lst[n - 1]) + 1)
        return "".join(lst)
