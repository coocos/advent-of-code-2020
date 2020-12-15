from collections import defaultdict
from typing import List
from pathlib import Path


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [int(value) for value in f.read().strip().split(",")]


def play_until(values: List[int], n: int) -> int:

    turns = {}
    spoken = defaultdict(list)

    # Initialize with starting numbers
    for i, value in enumerate(values):
        turn = i + 1
        turns[turn] = value
        spoken[value].append(turn)
    turn = len(values) + 1

    # Brute force it
    while turn <= n:
        if turn % 100000 == 0:
            print(f"{n - turn} turns left")
        previous = turns[turn - 1]
        if len(spoken[previous]) == 1:
            turns[turn] = 0
            spoken[0].append(turn)
        else:
            new_value = spoken[previous][-1] - spoken[previous][-2]
            turns[turn] = new_value
            spoken[new_value].append(turn)
        turn += 1

    return turns[turn - 1]


if __name__ == "__main__":

    values = parse_input()

    # First part
    assert play_until(values, 2020) == 758

    # Second part
    assert play_until(values, 30000000) == 814
