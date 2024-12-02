def read_input(filename: str) -> list[list[int]]:
    reports = []
    with open(filename) as infile:
        for line in infile.readlines():
            written_report = line.strip().split(" ")
            parsed_report = [int(level) for level in written_report]

            reports.append(parsed_report)

    return reports


def evaluate_report(report: list[int]) -> tuple[bool, int]:
    prev_level = report[0]
    is_increasing = None
    passed = True
    for i, level in enumerate(report[1:]):
        diff = level - prev_level
        if diff == 0 or abs(diff) > 3:
            passed = False

        if is_increasing is None:
            is_increasing = True if diff > 0 else False
        elif is_increasing:
            if diff < 0:
                passed = False
        else:
            if diff > 0:
                passed = False

        prev_level = level

        if not passed:
            break

    unsafe_level = i + 1

    return passed, unsafe_level


def process_reports(
    reports: list[list[int]], dampner_enabled: bool = False
) -> list[bool]:
    report_evaluations = []
    for report in reports:
        passed, unsafe_level = evaluate_report(report)
        if dampner_enabled:
            revised_report = report[:unsafe_level] + report[unsafe_level + 1 :]
            passed, _ = evaluate_report(revised_report)
            if not passed:
                # Somehow works
                reversed_report = report[::-1]
                passed, unsafe_level = evaluate_report(reversed_report)
                revised_report = (
                    reversed_report[:unsafe_level] + reversed_report[unsafe_level + 1 :]
                )
                passed, _ = evaluate_report(revised_report)

        report_evaluations.append(passed)

    return report_evaluations


def main() -> int:
    reports = read_input("input_day2.txt")
    report_evaluations = process_reports(reports)
    n_safe_reports = sum(report_evaluations)
    print("Answer to part 1: ", n_safe_reports)
    report_evaluations_w_dampener = process_reports(reports, dampner_enabled=True)
    n_safe_reports_w_dampener = sum(report_evaluations_w_dampener)
    print("Answer to part 2: ", n_safe_reports_w_dampener)

    return 0


if __name__ == "__main__":
    main()
