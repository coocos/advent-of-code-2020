from collections import deque
from pathlib import Path
from typing import Deque


def parse_input() -> Deque[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return deque(map(int, list(f.read().strip())))


def play(cups: Deque[int], moves: int = 0) -> str:

    move = 1
    current = cups[0]
    while move <= moves:

        cups.rotate(-1)
        pick_up = [cups.popleft(), cups.popleft(), cups.popleft()]
        destination = current - 1
        if destination == 0:
            destination = max(cups)
        while destination in pick_up:
            destination -= 1
            if destination <= 0:
                destination = max(cups)
                break

        # FIXME: Rotating to the destination node is way too slow for part 2
        while cups[0] != destination:
            cups.rotate(1)
        cups.rotate(-1)

        while pick_up:
            cups.appendleft(pick_up.pop())

        # FIXME: Rotating to the current node is way too slow for part 2
        while cups[0] != current:
            cups.rotate(1)

        cups.rotate(-1)
        current = cups[0]

        move += 1

    while cups[0] != 1:
        cups.rotate(1)

    return "".join(map(str, list(cups)[1:]))


if __name__ == "__main__":

    cups = parse_input()

    # First part
    assert play(cups.copy(), 100) == "59374826"
