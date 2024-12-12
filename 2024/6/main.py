"""Advent of Code 2024 - Day 6

Author: Alexander Bessman

This is a brute-force solution.
"""

from __future__ import annotations

from copy import copy
from dataclasses import astuple, dataclass
from typing import Literal, NamedTuple, Iterable


Direction = Literal[-1j, 1, 1j, -1]


class CRange:
    def __init__(
        self,
        start: complex | int,
        stop: complex | int,
        step: complex | int,
    ) -> None:
        self.start = start
        self.stop = stop
        self.step = step

        if ((self.stop - self.start) / self.step).imag:
            raise ValueError("'stop' not in range")

    def __contains__(self, value: complex) -> bool:
        inline = (value - self.start) / self.step

        if inline.imag:
            # value is on a different vector.
            return False

        if int(inline.real) != inline.real:
            # value is not on a step.
            return False

        ratio = (value - self.start) / (self.stop - self.start)
        assert ratio.imag == 0

        if 0 <= ratio.real < 1:
            return True

        # value is outside range.
        return False

    def __iter__(self) -> Iterable[complex | int]:
        # if self.step.real:
        #     rrange = range(*map(int, (self.start.real, self.stop.real, self.step.real)))
        # else:
        #     rrange = repeat(0)
        # if self.step.imag:
        #     irange = range(*map(int, (self.start.imag, self.stop.imag, self.step.imag)))
        # else:
        #     irange = repeat(0)
        # yield from (r + i * 1j for r, i in zip(rrange, irange))
        inline = (self.stop - self.start) / self.step

        if inline.imag or inline.real <= 0:
            return

        i = self.start

        while (
            i.real * self.step.real <= self.stop.real * self.step.real
            and i.imag * self.step.imag < self.stop.imag * self.step.imag
        ) or (
            i.real * self.step.real < self.stop.real * self.step.real
            and i.imag * self.step.imag <= self.stop.imag * self.step.imag
        ):
            yield i
            i += self.step

    def __repr__(self) -> str:
        return f"CRange({self.start}, {self.stop}, {self.step})"


class Grid(NamedTuple):
    size: complex
    obstacles: set[complex]

    def __contains__(self, value: complex) -> bool:
        return (0 <= value.real < self.size.real) and (0 <= value.imag < self.size.imag)


@dataclass
class Guard:
    pos: complex
    dir: Direction

    def __hash__(self) -> int:
        return hash(astuple(self))


def walk(guard: Guard, grid: Grid) -> tuple[Guard | None, set[complex]]:
    """Walk guard until next obstacle.

    Parameters
    ----------
    guard : Guard
        Current guard location and direction.
    grid : Grid
        Grid size and locations of obstacles.

    Return
    ------
    guard : Guard | None
        New location and direction of guard, or None if guard left the grid.
    traversed : set[complex]
        All locations traversed by guard, including starting and final location.
    """
    match guard.dir:
        case -1j:
            stop = guard.pos.real - 1j
        case 1:
            stop = grid.size.real + guard.pos.imag * 1j
        case 1j:
            stop = guard.pos.real + grid.size.imag * 1j
        case -1:
            stop = -1 + guard.pos.imag * 1j
        case _:
            raise RuntimeError

    path = CRange(
        start=guard.pos,
        stop=stop,
        step=guard.dir,
    )
    obs = min(
        [o for o in grid.obstacles if o in path],
        default=path.stop,
        key=lambda x: abs(x - guard.pos),
    )
    traversed = set(CRange(guard.pos, obs, guard.dir))
    guard.pos = obs - guard.dir
    guard.dir *= -1j  # Turn right.

    if obs in grid:
        return guard, traversed

    return None, traversed


def detect_loop(guard: Guard, grid: Grid) -> bool:
    """Detect if the guard enters a loop.

    Parameters
    ----------
    guard : Guard
    grid : Grid

    Returns
    -------
    bool
        True if guard never leaves grid.
    """
    previous_guard_states = set([guard])

    while guard:
        guard, _ = walk(guard, grid)

        if not guard:
            return False

        if guard in previous_guard_states:
            return True

        previous_guard_states.add(guard)

    assert False  # Never reached.


# %% Load input
with open("input.txt") as f:
    raw = f.read()

width = raw.index("\n")
height = len(raw.splitlines())
guard_origin = Guard(complex(*divmod(raw.index("^"), width + 1)), -1)
obstacles = set()
lraw = list(raw)

while "#" in lraw:
    obstacles.add(complex(*divmod(lraw.index("#"), width + 1)))
    lraw[lraw.index("#")] = "¤"

grid = Grid(complex(height, width), obstacles)

# %% Part 1
traversed = set()
guard = copy(guard_origin)

while guard:
    guard, walked = walk(guard, grid)
    traversed |= walked

print("1:", len(traversed))

# %% Part 2
# Sloooooooow
new_obstacles = traversed ^ set([guard_origin.pos])
new_grids = (Grid(grid.size, grid.obstacles | set([o])) for o in new_obstacles)
print("2:", sum(detect_loop(copy(guard_origin), g) for g in new_grids))
