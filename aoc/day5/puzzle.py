import collections
from typing import List
from pathlib import Path


def parse_input() -> List[str]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [line.strip() for line in f.readlines()]


def partition(boarding_pass: str, low: int, high: int) -> int:
    for char in boarding_pass:
        middle = (low + high) // 2
        if char in "LF":
            high = middle
        else:
            low = middle + 1
    return low


def seat_id(boarding_pass: str) -> int:
    row = boarding_pass[:7]
    column = boarding_pass[7:]
    return partition(row, 0, 127) * 8 + partition(column, 0, 7)


if __name__ == "__main__":

    boarding_passes = parse_input()

    # First part
    seats = list(map(seat_id, boarding_passes))
    assert max(seats) == 955

    # Second part
    missing_seat = -1
    known_seats = set(seats)
    for seat in range(min(seats), max(seats)):
        if seat not in known_seats:
            missing_seat = seat
            break
    assert missing_seat == 569