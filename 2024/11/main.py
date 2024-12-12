"""Advent of Code 2024 - Day 11

Author: Alexander Bessman
"""

from collections import Counter
from functools import cache
from math import log10


@cache
def blink(stone) -> tuple[int]:
    if stone == 0:
        return (1,)

    size = int(log10(stone))

    if size % 2:
        return divmod(stone, 10 ** (size // 2 + 1))

    return (stone * 2024,)


def main(stones: Counter[int, int], blinks: int) -> int:
    for i in range(blinks):
        new = Counter()

        for s, n in stones.items():
            for stone in blink(s):
                new[stone] += n

        stones = new
    return stones


with open("input.txt") as f:
    stones = Counter(map(int, f.read().strip().split()))

print("1:", main(stones, 25).total())
print("2:", main(stones, 75).total())
