from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return list(map(int, list(f.read().strip())))


class Ring:
    def __init__(self, cups: List[int]) -> None:

        self.cups = {}
        for i in range(len(cups) - 1):
            self.cups[cups[i]] = cups[i + 1]
        self.cups[cups[i + 1]] = cups[0]

    def pop(self, cup: int) -> int:

        next_cup = self.cups[cup]
        self.cups[cup] = self.cups[next_cup]
        del self.cups[next_cup]
        return next_cup

    def insert(self, cup: int, new_cup: int) -> None:

        old_next = self.cups[cup]
        self.cups[cup] = new_cup
        self.cups[new_cup] = old_next

    def __getitem__(self, cup: int) -> int:
        return self.cups[cup]


def play(cup_list: List[int], moves: int = 100) -> List[int]:

    largest = max(cup_list)
    ring = Ring(cup_list)

    move = 1
    current = cup_list[0]

    while move <= moves:

        pick_up = [ring.pop(current) for _ in range(3)]

        destination = current - 1
        if destination == 0:
            destination = largest
        while destination in pick_up:
            destination -= 1
            if destination <= 0:
                destination = largest

        while pick_up:
            ring.insert(destination, pick_up.pop())

        current = ring[current]
        move += 1

    clockwise_cups: List[int] = []
    current = ring[1]
    while len(clockwise_cups) < 8:
        clockwise_cups.append(current)
        current = ring[current]
    return clockwise_cups


if __name__ == "__main__":

    cups = parse_input()

    # First part
    assert "".join(map(str, play(cups, 100))) == "59374826"

    # Second part
    clockwise_cups = play(cups + list(range(10, 1_000_000 + 1)), 10_000_000)
    assert clockwise_cups[0] * clockwise_cups[1] == 66878091588
