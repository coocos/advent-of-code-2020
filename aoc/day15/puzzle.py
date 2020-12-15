import collections
from time import time
from typing import List
from pathlib import Path


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [int(value) for value in f.read().strip().split(",")]


def play_until(values: List[int], n: int) -> int:

    spoken = collections.defaultdict(list)

    for i, value in enumerate(values):
        turn = i + 1
        spoken[value].append(turn)
    turn = len(values) + 1
    prev = value

    while turn <= n:
        value = 0 if len(spoken[prev]) == 1 else spoken[prev][-1] - spoken[prev][-2]
        spoken[value].append(turn)
        prev = value
        turn += 1

    return prev


if __name__ == "__main__":

    values = parse_input()

    # First part
    assert play_until(values, 2020) == 758

    # Second part
    assert play_until(values, 30_000_000) == 814
