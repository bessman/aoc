"""Advent of Code - Day 10

Author: Alexander Bessman
"""

from typing import Iterator


class Topology:
    def __init__(self, elevation: list[list[int]]) -> None:
        self.elevation = elevation

    @property
    def trailheads(self) -> Iterator[complex]:
        for i, line in enumerate(self.elevation):
            for j, location in enumerate(line):
                if self[i + j * 1j] == 0:
                    yield i + j * 1j

    def __getitem__(self, key: complex) -> int:
        x = int(key.real)
        y = int(key.imag)

        if any(i < 0 for i in (x, y)):
            return float("nan")

        try:
            return self.elevation[x][y]
        except IndexError:
            return float("nan")

    def __repr__(self) -> str:
        return "\n".join("".join(str(p) for p in line) for line in self.elevation)


def hike(location: complex, topology: Topology) -> list[list[complex]]:
    """Return all trails which start from 'location'.

    This is a recursive function.

    Parameters
    ----------
    location : complex
    topology : Topology

    Returns
    -------
    list[list[complex]]
    """
    up = -1
    right = 1j
    down = 1
    left = -1j
    trails = [[]]
    elev = topology[location]

    # Add all trails which continue from this position.
    for direction in (up, right, down, left):
        adjacent = topology[location + direction]
        if adjacent - elev == 1:
            trails.extend(hike(location + direction, topology))

    # Append the current position to all trails.
    for trail in trails:
        trail.append(location)

    return trails


def summit_climbs(topology: Topology) -> Iterator[list[complex]]:
    summit = 9
    for h in topology.trailheads:
        trails = hike(h, topology)
        yield from (t for t in trails if topology[t[0]] == summit)


def unique_summit_climbs(topology: Topology) -> Iterator[list[complex]]:
    climbs = set()

    for t in summit_climbs(topology):
        if (t[-1], t[0]) not in climbs:
            yield t
            climbs.add((t[-1], t[0]))


with open("input.txt") as f:
    topology = Topology([[int(p) for p in list(line.strip())] for line in f])

print("1:", len(list(unique_summit_climbs(topology))))
print("2:", len(list(summit_climbs(topology))))
