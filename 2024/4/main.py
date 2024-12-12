"""Advent of Code 2024 - Day 4

Author: Alexander Bessman

This solution uses template matching via OpenCV. Essentially, the input is treated as a
bitmap image with four colors, and the target words as smaller images to be found within
that image.
"""

import cv2
import numpy as np
import numpy.typing as npt

X, M, A, S = 1, 2, 3, 4


def count_word(puzzle: npt.NDArray[np.uint8], word: npt.NDArray[np.uint8]) -> int:
    mask = (word != 0).astype(np.uint8)
    result = cv2.matchTemplate(puzzle, word, cv2.TM_SQDIFF, mask=mask)
    return np.count_nonzero(result == 0)


# %% Load input
with open("input.txt") as f:
    puzzle = np.vstack(
        [
            np.array(
                [{"X": X, "M": M, "A": A, "S": S}[c] for c in line], dtype=np.uint8
            )
            for line in f.read().splitlines()
        ]
    )

# %% Part 1
xmas = np.array([[X, M, A, S]], dtype=np.uint8)
xmas_diag = np.diag(xmas[0])
words = (np.rot90(w, i) for w in (xmas, xmas_diag) for i in range(4))
solution = sum(count_word(puzzle, w) for w in words)
# %%
print("1:", solution)

# %% Part 2
x_mas = np.array(
    [
        [M, 0, M],
        [0, A, 0],
        [S, 0, S],
    ],
    dtype=np.uint8,
)
words = (np.rot90(x_mas, i) for i in range(4))
solution = sum(count_word(puzzle, w) for w in words)
# %%
print("2:", solution)
