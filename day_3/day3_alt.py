import re


def read_input(filename: str) -> list[str]:
    with open(filename) as infile:
        return infile.readlines()


def exec_memory(memory: list[str], pattern: str):
    result = []
    do = True
    for line in memory:
        matches = re.findall(pattern, line)
        for match in matches:
            if match[0] == "do()":
                do = True
            elif match[0] == "don't()":
                do = False
            else:
                if do:
                    x, y = int(match[-2]), int(match[-1])
                    z = x * y
                    result.append(z)

    return result


def main() -> int:
    memory = read_input("input_day3.txt")

    pattern = r"mul\(([0-9]*),([0-9]*)\)"

    result = exec_memory(memory, pattern)
    sum_results = sum(result)
    print("Answer to part 1: ", sum_results)

    new_pattern = r"(do\(\)|don't\(\)|mul\(([0-9]*),([0-9]*)\))"

    new_result = exec_memory(memory, new_pattern)
    sum_new_results = sum(new_result)
    print("Answer to part 2: ", sum_new_results)

    return 0


if __name__ == "__main__":
    main()
