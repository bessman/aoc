"""Advent of Code 2024 - Day 1

Author: Alexander Bessman
"""

with open("input.txt") as f:
    locations = [int(x) for xx in f for x in xx.split()]

left = sorted(locations[::2])
right = sorted(locations[1::2])

print("1:", sum(abs(a - b) for a, b in zip(left, right)))
print("2:", sum(a * right.count(a) for a in left))
