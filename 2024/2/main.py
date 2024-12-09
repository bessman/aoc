"""Advent of Code 2024 - Day 2

Author: Alexander Bessman
"""

from typing import Literal, Optional


def is_monotonic(
    report: list[int],
    threshold: Optional[int] = None,
    almost: bool = False,
) -> bool:
    previous = report[0]
    direction = sign(report[1] - previous)

    for i, level in enumerate(report[1:]):
        if direction == 0:
            break
        if sign(level - previous) != direction:
            break
        if abs(level - previous) > threshold:
            break
        previous = level
    else:
        return True

    if almost:
        tmp = report[:]
        tmp.pop(i - 1)

        if is_monotonic(tmp, threshold=threshold):
            return True

        tmp = report[:]
        tmp.pop(i)

        if is_monotonic(tmp, threshold=threshold):
            return True

        tmp = report[:]
        tmp.pop(i + 1)
        return is_monotonic(tmp, threshold=threshold)

    return False


def sign(n: int) -> Literal[1, 0, -1]:
    if n > 0:
        return 1
    if n == 0:
        return 0
    return -1


safe = 0
safeish = 0

with open("input.txt") as f:
    for line in f:
        report = [int(level) for level in line.split()]
        safe += is_monotonic(report, threshold=3)
        safeish += is_monotonic(report, threshold=3, almost=True)

print("1:", safe)
print("2:", safeish)
