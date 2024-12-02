def read_input(filename: str) -> tuple[list[int], list[int]]:
    with open(filename) as infile:
        col1 = []
        col2 = []
        for line in infile.readlines():
            entry1, entry2 = line.strip().split("   ")
            col1.append(int(entry1))
            col2.append(int(entry2))

    return col1, col2


def sort_column(col: list[int]) -> list[int]:

    greatest_entry = col[0]
    output = [greatest_entry]
    for i, entry in enumerate(col[1:]):
        if entry < greatest_entry:
            for j in range(i + 1):
                if output[j] > entry:
                    output.insert(j, entry)
                    break
        else:
            output.append(entry)
            greatest_entry = entry

    return output


def calc_pair_distance(col1: list[int], col2: list[int]) -> list[int]:
    output = []
    for entry1, entry2 in zip(col1, col2):
        output.append(abs(entry1 - entry2))

    return output


def calc_overlap(col1: list[int], col2: list[int]) -> list[int]:
    output = []
    for entry in col1:
        if entry not in col2:
            output.append(0)
            continue
        ovelap_count = col2.count(entry)
        output.append(entry * ovelap_count)

    return output


def main() -> int:
    col1, col2 = read_input("input_day1.txt")
    col1_sorted = sort_column(col1)
    col2_sorted = sort_column(col2)

    pair_distance = calc_pair_distance(col1_sorted, col2_sorted)
    total_distance = sum(pair_distance)
    print("Answer to part 1: ", total_distance)
    overlap = calc_overlap(col1_sorted, col2_sorted)
    similarity_score = sum(overlap)
    print("Answer to part 2: ", similarity_score)

    return 0


if __name__ == "__main__":
    main()
