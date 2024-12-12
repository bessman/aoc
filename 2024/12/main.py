"""Advend of Code 2024 - Day 12

Author: Alexander Bessman

Solved by walking around each distinct area and counting steps (perimeter) and
turns (sides).
"""

from dataclasses import dataclass
from typing import Iterator

import numpy as np
import numpy.typing as npt
from scipy import ndimage


UP = -1j
RIGHT = 1
DOWN = 1j
LEFT = -1


@dataclass
class Walker:
    """Previously employed as guard in prototype suit manufacturing lab."""

    pos: complex
    dir: complex

    @property
    def row(self) -> int:
        return int(self.pos.imag)

    @property
    def col(self) -> int:
        return int(self.pos.real)

    def step(self) -> None:
        self.pos += self.dir

    def lookahead(self) -> tuple[int, int]:
        pos = self.pos + self.dir
        return int(pos.imag), int(pos.real)

    def lookright(self) -> tuple[int, int]:
        pos = self.pos + self.dir * 1j
        return int(pos.imag), int(pos.real)

    def __repr__(self) -> str:
        arrow = {RIGHT: ">", DOWN: "v", LEFT: "<", UP: "^"}[self.dir]
        return f"{self.row, self.col} {arrow}"


def bw_perim_vertic(bw: npt.NDArray) -> tuple[int, int]:
    """Count perimeter and vertices of area of 1's in a 2D binary matrix.

    This is a recursive function, but recursion depth should not exceed 1 in normal
    circumstances.

    Parameters
    ----------
    bw : NDArray

    Returns
    -------
    perimeter, num_vertices : tuple[int, int]
    """
    # Vertices are found by walking one lap around the shape and counting turns.
    origin = complex(*min(zip(*bw.nonzero()))[::-1]) + 1  # One above topleftmost 1.
    walker = Walker(origin, RIGHT)
    walker.step()
    frame = np.pad(bw, 1)
    steps = 1
    turns = 0

    while not walker.pos == origin:
        if not frame[*walker.lookright()]:
            # Nothing on walker's righthand side, turn right.
            walker.dir *= 1j
            turns += 1
            steps -= 1  # Walker overstepped area, discard last stepcount.

        elif frame[*walker.lookahead()]:
            # Something ahead, turn left.
            walker.dir *= -1j
            turns += 1
            steps += 1  # Walker is adjacent to two (or three) walls.

            if frame[*walker.lookahead()]:
                # Something ahead again, we're in a dead end. Turn left again.
                walker.dir *= -1j
                turns += 1
                steps += 1

        walker.step()
        steps += 1

    # Matrix may have holes, need to find perimeter/vertices of each hole.
    regions, n = ndimage.label(1 - frame)

    # 0 is current area of interest, 1 is background/padding, 2+ are holes.
    for hole in range(2, n + 1):
        st = bw_perim_vertic(regions == hole)  # Recurse.
        steps += st[0]
        turns += st[1]

    return steps, turns


def garden_properties(garden: npt.NDArray) -> Iterator[tuple[int, int, int]]:
    for k, plant in plants.items():
        regions, n = ndimage.label(garden == plant)

        for region in range(1, n + 1):
            bw = region == regions
            area = bw.sum()
            perimeter, sides = bw_perim_vertic(bw)
            yield area, perimeter, sides


def main(garden: npt.NDArray) -> tuple[int, int]:
    cost1 = 0
    cost2 = 0

    for area, perimeter, sides in garden_properties(garden):
        cost1 += area * perimeter
        cost2 += area * sides

    return cost1, cost2


with open("input.txt") as f:
    plants = {}
    garden = []

    for line in f:
        for plant in list(line.strip()):
            if plant not in plants:
                plants[plant] = max(plants.values(), default=0) + 1
        garden.append([plants[c] for c in line.strip()])

garden = np.array(garden)
cost1, cost2 = main(garden)

print("1:", cost1)
print("2:", cost2)
