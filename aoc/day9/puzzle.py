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


def encryption_weakness(numbers: List[int], target_sum: int) -> int:

    for window_size in range(2, len(numbers)):
        window = sum(numbers[:window_size])
        for head in range(window_size, len(numbers)):
            if window == target_sum:
                numbers_in_window = numbers[head - window_size : head]
                return min(numbers_in_window) + max(numbers_in_window)
            entering = numbers[head]
            leaving = numbers[head - window_size]
            window += entering - leaving

    raise RuntimeError("No encryption weakness found")


if __name__ == "__main__":

    numbers = parse_input()

    # First part
    invalid_number = first_invalid_number(numbers)
    assert invalid_number == 15690279

    # Second part
    assert encryption_weakness(numbers, invalid_number) == 2174232
