from typing import Tuple, List, Literal
from pathlib import Path


def parse_input() -> List[Tuple[str, int]]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [(line[0], int(line[1:])) for line in f]


def navigate(
    instructions: List[Tuple[str, int]], mode: Literal["normal", "waypoint"]
) -> int:

    position = [0, 0]
    direction = [1, 0] if mode == "normal" else [10, -1]

    for action, value in instructions:

        if action == "N":
            if mode == "normal":
                position[1] -= value
            else:
                direction[1] -= value
        elif action == "S":
            if mode == "normal":
                position[1] += value
            else:
                direction[1] += value
        elif action == "E":
            if mode == "normal":
                position[0] += value
            else:
                direction[0] += value
        elif action == "W":
            if mode == "normal":
                position[0] -= value
            else:
                direction[0] -= value
        elif action == "F":
            position[0] += direction[0] * value
            position[1] += direction[1] * value
        elif action == "L":
            for _ in range(value // 90):
                direction[0], direction[1] = direction[1], -direction[0]
        elif action == "R":
            for _ in range(value // 90):
                direction[0], direction[1] = -direction[1], direction[0]
        else:
            raise RuntimeError(f"Unknown action {action}")

    return abs(0 + position[0]) + abs(0 + position[1])


if __name__ == "__main__":

    instructions = parse_input()

    # First part
    assert navigate(instructions, "normal") == 1603

    # Second part
    assert navigate(instructions, "waypoint") == 52866
