from typing import Literal
import numpy as np


def read_input(filename: str) -> np.ndarray[np.ndarray[str]]:
    output = []
    with open(filename) as infile:
        for line in infile.readlines():
            output.append(np.array(list(line.strip())))

    return np.array(output)


def convert_to_matrix(
    crossword: np.ndarray[np.ndarray[str]], letters_in_crossword: str
) -> dict[str, np.ndarray[np.ndarray[int]]]:
    letter_matrices = {}
    for letter in letters_in_crossword:
        letter_array = np.where(crossword == letter, 1, 0)
        letter_matrices[letter] = letter_array

    return letter_matrices


def pad_matrices(
    matrices: dict[str, np.ndarray[np.ndarray[int]]],
    pad: int,
) -> tuple[dict[str, np.ndarray[np.ndarray[int]]], np.ndarray[int]]:
    keys = list(matrices.keys())
    matrix_shape = matrices[keys[0]].shape
    for key in matrices:
        matrices[key] = np.pad(
            matrices[key],
            ((pad - 1, pad), (pad - 1, pad)),
            "constant",
        )

    return matrices, np.array(matrix_shape)


def get_slice_from_offset(pad_size: int, offset: np.ndarray[int]) -> list[slice]:
    return [
        slice(pad_size - 1 + offset[0], -pad_size + offset[0]),
        slice(pad_size - 1 + offset[1], -pad_size + offset[1]),
    ]


def search_crossword(
    letter_matrices: dict[str, np.ndarray[np.ndarray[int]]],
    shape: np.ndarray[int],
    offsets: dict[str, np.ndarray[int]],
) -> tuple[int, dict[str, np.ndarray[int]]]:
    total_matches = 0
    n_letters = len(letter_matrices)
    crossword_match_map = {}
    for direction in [1, -1]:
        for offset_type in offsets:
            crossword_match = np.zeros(shape, dtype=int) + 1
            offset = np.zeros((2), dtype=int)
            for letter in letter_matrices:
                crossword_match *= letter_matrices[letter][
                    *get_slice_from_offset(n_letters, offset)
                ]
                offset += offsets[offset_type] * direction

            crossword_match_map[
                offset_type + "_reverse" if direction == -1 else offset_type
            ] = crossword_match
            total_matches += np.sum(crossword_match)

    return total_matches, crossword_match_map


def find_crosses(
    crossword_match_map: dict[str, np.ndarray[int]],
    letters: list[str],
    cross_combos: dict[str, dict[str, tuple[int, int]]],
) -> int:

    n_letters = len(letters)
    total_crosses = 0
    for combo in cross_combos:
        cross_matrix = crossword_match_map[combo][
            *get_slice_from_offset(n_letters, [0, 0])
        ].copy()

        for key, offset in cross_combos[combo].items():
            offset_match = crossword_match_map[key][
                *get_slice_from_offset(n_letters, offset)
            ].copy()

            cross_matrix += offset_match

        cross_matrix_matches = np.where(cross_matrix == 2, 1, 0)

        total_crosses += np.sum(cross_matrix_matches)

    return total_crosses


def main() -> int:
    crossword = read_input("input_day4.txt")
    letters = ["X", "M", "A", "S"]
    letter_matrices = convert_to_matrix(crossword, letters_in_crossword=letters)
    padded_letter_matrices, shape = pad_matrices(letter_matrices, pad=len(letters))
    offsets = {
        "diagonal": np.array([-1, 1]),
        "diagonal_flipped": np.array([-1, -1]),
        "horizontal": np.array([0, 1]),
        "vertical": np.array([1, 0]),
    }
    total_matches, _ = search_crossword(padded_letter_matrices, shape, offsets)
    print("Answer to part 1: ", total_matches)

    letters = ["M", "A", "S"]
    letter_matrices = convert_to_matrix(crossword, letters_in_crossword=letters)
    padded_letter_matrices, shape = pad_matrices(letter_matrices, pad=len(letters))
    offsets = {
        "diagonal": np.array([-1, 1]),
        "diagonal_flipped": np.array([-1, -1]),
    }
    total_matches, crossword_match_map = search_crossword(
        padded_letter_matrices, shape, offsets
    )
    cross_combos = {
        "diagonal": {"diagonal_flipped": (0, 2), "diagonal_flipped_reverse": (-2, 0)},
        "diagonal_reverse": {
            "diagonal_flipped": (2, 0),
            "diagonal_flipped_reverse": (0, -2),
        },
    }
    padded_crossword_match_map, _ = pad_matrices(crossword_match_map, pad=len(letters))
    total_crosses = find_crosses(padded_crossword_match_map, letters, cross_combos)
    print("Answer to part 2: ", total_crosses)
    return 0


if __name__ == "__main__":
    main()
