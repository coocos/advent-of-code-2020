from typing import Tuple, List, Literal
from pathlib import Path


def parse_input() -> List[Tuple[str, int]]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [(line[0], int(line[1:])) for line in f]


def navigate(
    instructions: List[Tuple[str, int]], mode: Literal["normal", "waypoint"]
) -> int:

    ship = [0, 0]
    velocity = [1, 0] if mode == "normal" else [10, -1]
    movement_target = ship if mode == "normal" else velocity

    for action, value in instructions:
        if action == "N":
            movement_target[1] -= value
        elif action == "S":
            movement_target[1] += value
        elif action == "E":
            movement_target[0] += value
        elif action == "W":
            movement_target[0] -= value
        elif action == "F":
            ship[0] += velocity[0] * value
            ship[1] += velocity[1] * value
        elif action == "L":
            for _ in range(value // 90):
                velocity[0], velocity[1] = velocity[1], -velocity[0]
        elif action == "R":
            for _ in range(value // 90):
                velocity[0], velocity[1] = -velocity[1], velocity[0]
        else:
            raise RuntimeError(f"Unknown action {action}")

    return abs(ship[0]) + abs(ship[1])


if __name__ == "__main__":

    instructions = parse_input()

    # First part
    assert navigate(instructions, "normal") == 1603

    # Second part
    assert navigate(instructions, "waypoint") == 52866
