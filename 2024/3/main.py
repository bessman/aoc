"""Advent of Code 2024 - Day 3

Author: Alexander Bessman
"""

import re
from operator import mul


mul_pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")

with open("input.txt") as f:
    mem = f.read()

muls = re.findall(mul_pattern, mem)
print("1:", sum(eval(m) for m in muls))

enabled_mem = mem.split("don't()")[0]

for section in mem.split("don't()")[1:]:
    segments = section.split("do()")
    enabled_mem += "".join(segments[1:])

enabled_muls = re.findall(mul_pattern, enabled_mem)
print("2:", sum(eval(m) for m in enabled_muls))
