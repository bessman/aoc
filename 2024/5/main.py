"""Advent of Code 2024 - Day 5

Author: Alexander Bessman

This solution treats the input as (several) systems of inequalities, which can be solved
with linear programming.
"""

from scipy.optimize import linprog


def sort_update(update: list[int], rules: list[tuple[int, int]]) -> list[int]:
    A = []

    for small, big in rules:
        ub = [0] * len(update)
        ub[update.index(small)] = 1
        ub[update.index(big)] = -1
        A.append(ub)

    b = [-1] * len(A)
    c = [1] * len(update)
    bounds = [(0, None)] * len(update)
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
    key = {k: int(v) for k, v in zip(update, res.x)}
    return sorted(update, key=lambda k: key[k])


with open("input.txt") as f:
    k = 0
    rules = []

    while "|" in (line := next(f)):
        rules.append([int(i) for i in line.strip().split("|")])

    updates = [[int(i) for i in line.strip().split(",")] for line in f]

middle_correct = []
middle_wrong = []

# The problem as a whole cannot be viewed as a linear programming problem because the
# page relationships contain loops. But the pages involved in a single update never
# contain loops, and thus CAN be viewed as a LP problem.
for update in updates:
    active_rules = [(a, b) for a, b in rules if a in update and b in update]
    sorted_update = sort_update(update, active_rules)
    middle = sorted_update[(len(sorted_update) - 1) // 2]

    if sorted_update == update:
        middle_correct.append(middle)
    else:
        middle_wrong.append(middle)

print("1:", sum(middle_correct))
print("2:", sum(middle_wrong))
