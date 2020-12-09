from itertools import combinations
from typing import List
from pathlib import Path


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [int(line.strip()) for line in f.readlines()]


def first_invalid_number(numbers: List[int]) -> int:

    previous_numbers = numbers[:25]
    for number in numbers[25:]:
        if not any(sum(c) == number for c in combinations(previous_numbers, 2)):
            return number
        previous_numbers = previous_numbers[1:] + [number]

    raise RuntimeError("No invalid number found")


def encryption_weakness(numbers: List[int], invalid_number: int) -> int:

    for head in range(len(numbers)):
        for tail in range(head + 2, len(numbers)):
            number_range = numbers[head:tail]
            if sum(number_range) == invalid_number:
                return min(number_range) + max(number_range)

    raise RuntimeError("No encryption weakness found")


if __name__ == "__main__":

    numbers = parse_input()

    # First part
    invalid_number = first_invalid_number(numbers)
    assert invalid_number == 15690279

    # Second part
    assert encryption_weakness(numbers, invalid_number) == 2174232
