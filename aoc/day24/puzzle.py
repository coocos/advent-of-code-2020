from typing import List, Iterable
from pathlib import Path


def parse_input() -> List[str]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [line.strip() for line in f]


def next_step(instruction: str) -> Iterable[str]:

    direction = ""
    for char in instruction:
        if direction in ["e", "se", "sw", "w", "nw", "ne"]:
            yield direction
            direction = ""
        direction += char
    yield direction


def flip(instructions: List[str]):

    directions = {
        "e": (1, 0),
        "se": (0, 1),
        "sw": (-1, 1),
        "w": (-1, 0),
        "nw": (0, -1),
        "ne": (1, -1),
    }
    tiles = {}

    for instruction in instructions:

        position = (0, 0)
        for step in next_step(instruction):
            x, y = directions[step]
            position = (position[0] + x, position[1] + y)
        tiles[position] = "black" if position not in tiles else "white"

    return tiles


if __name__ == "__main__":

    instructions = parse_input()

    # First part
    tiles = flip(instructions)
    assert len([color for color in tiles.values() if color == "black"]) == 293
