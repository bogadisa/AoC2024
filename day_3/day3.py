import re


def read_input(filename: str) -> list[str]:
    with open(filename) as infile:
        return infile.readlines()


def interpret_line(line: str, do: bool) -> tuple[str, bool]:
    split_sep = "do()" if not do else "don't()"
    split_line = line.split(split_sep, 1)

    if len(split_line) > 1:
        output, new_do = interpret_line(split_line[1], not do)
    else:
        output = ""
        new_do = do

    if do:
        output += split_line[0]

    return output, new_do


def filter_memory(memory: list[str]) -> list[str]:
    filtered_memory = []

    do = True
    for line in memory:
        output, do = interpret_line(line, do)
        filtered_memory.append(output)

    return filtered_memory


def exec_memory(memory: list[str], pattern: str):
    result = []
    for line in memory:
        matches = re.findall(pattern, line)
        for match in matches:
            x, y = int(match[0]), int(match[1])
            z = x * y
            result.append(z)

    return result


def main() -> int:
    memory = read_input("input_day3.txt")

    pattern = r"mul\(([0-9]*),([0-9]*)\)"

    result = exec_memory(memory, pattern)
    sum_results = sum(result)
    print("Answer to part 1: ", sum_results)

    filtered_memory = filter_memory(memory)
    filtered_result = exec_memory(filtered_memory, pattern)
    sum_filtered_results = sum(filtered_result)
    print("Answer to part 2: ", sum_filtered_results)

    return 0


if __name__ == "__main__":
    main()
