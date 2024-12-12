from itertools import permutations


class Grid(complex):
    def __contains__(self, other: complex) -> bool:
        return (0 <= other.real < self.real) and (0 <= other.imag < self.imag)


def get_antinodes(
    antenna_pair: tuple[complex, complex],
    grid: Grid,
    harmonics: bool = True,
) -> set[complex]:
    diff = antenna_pair[0] - antenna_pair[1]
    antinode = antenna_pair[0] + diff
    antinodes: set[complex] = set()

    while antinode in grid:
        antinodes.add(antinode)
        antinode += diff

        if not harmonics:
            break

    return antinodes | set(antenna_pair * harmonics)


with open("input.txt") as f:
    antennas: dict[str, list[complex]] = {}

    for row, line in enumerate(f.read().split("\n")):
        for col, char in enumerate(line):
            if char == ".":
                continue
            antennas[char] = antennas.get(char, []) + [col + row * 1j]

grid = Grid(col + 1 + row * 1j)
antinodes_1: set[complex] = set()
antinodes_2: set[complex] = set()

for antenna_type in antennas.values():
    for antenna_pair in permutations(antenna_type, 2):
        antinodes_1 |= get_antinodes(antenna_pair, grid, harmonics=False)
        antinodes_2 |= get_antinodes(antenna_pair, grid, harmonics=True)

print("1:", len(antinodes_1))
print("2:", len(antinodes_2))
