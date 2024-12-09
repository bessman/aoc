"""Advent of Code 2024 - Day 7

Author: Alexander Bessman
"""

from itertools import product
from math import log10
from operator import add, mul


def cat(x: int, y: int) -> int:
    return x * 10 ** (int(log10(y)) + 1) + y


ops1 = (add, mul)
ops2 = (add, mul, cat)


with open("input.txt") as f:
    calibrations = []

    for line in f:
        tv, eq = line.strip().split(":")
        calibrations.append((int(tv), tuple(map(int, eq.strip().split()))))


valid = []

for test_value, equation in calibrations:
    for combination in product(*(len(equation) - 1) * [ops2]):
        out = equation[0]

        for i, op in zip(equation[1:], combination):
            out = op(out, i)

        if out == test_value:
            valid.append(out)
            break

print("2:", sum(valid))
