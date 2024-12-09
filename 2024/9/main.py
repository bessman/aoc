"""Advent of Code - Day 9

Author: Alexander Bessman
"""

from dataclasses import dataclass


def fragment(filesystem: list[int]):
    """Generate a fragmented filesystem representation.

    This function does not actually move any files around; it only calculates the
    representation that would result if the files were fragmented and moved.
    """
    frag = filesystem[:]
    tail_id = 0
    tail_size = 0

    for i, b in enumerate(frag):
        if i % 2:  # Empty memory block.
            while b:
                if not tail_size:
                    tail_size = frag.pop()
                    frag.pop()
                    tail_id = len(frag) // 2 + 1

                yield tail_id
                b -= 1
                tail_size -= 1
        else:  # File block.
            while b:
                yield i // 2
                b -= 1

    while tail_size:
        yield tail_id
        tail_size -= 1


@dataclass
class File:
    id: int
    address: int
    size: int


class Filesystem:
    def __init__(self, filesystem: list[int]) -> None:
        self.files = []
        self.empty = []
        address = 0

        for i, (f, e) in enumerate(zip(filesystem[::2], filesystem[1::2])):
            self.files.append(File(i, address, f))
            address += f
            self.empty.append(File(-1, address, e))
            address += e

        self.files.append(File(i + 1, address, filesystem[-1]))

    def compact(self):
        """Free up space by moving files to lower addresses when possible."""
        previous_id = self.files[-1].id + 1

        for f in self.files[::-1]:
            if f.id > previous_id:
                # Don't move a file which has already been moved.
                continue

            for e in self.empty:
                if e.address > f.address:
                    # Don't move file to the right.
                    break

                if f.size <= e.size:
                    f.address = e.address
                    e.size -= f.size
                    e.address += f.size
                    break

            previous_id = f.id


# %% Load input
with open("input.txt") as f:
    fs = [int(i) for i in f.read().strip()]


# %% Part 1
_1 = sum(i * b for i, b in enumerate(fragment(fs)))
# %%
print("1:", _1)

# %% Part 2
filesys = Filesystem(fs)
filesys.compact()
_2 = sum(f.id * (f.address + i) for f in filesys.files for i in range(f.size))
# %%
print("2:", _2)
