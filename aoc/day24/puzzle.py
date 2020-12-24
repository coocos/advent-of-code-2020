from collections import defaultdict
from typing import List, Iterable, Dict, Tuple
from pathlib import Path


Coord = Tuple[int, int]
Grid = Dict[Coord, str]


def parse_input() -> List[str]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [line.strip() for line in f]


def next_step(instruction: str) -> Iterable[Coord]:

    directions = {
        "e": (1, 0),
        "se": (0, 1),
        "sw": (-1, 1),
        "w": (-1, 0),
        "nw": (0, -1),
        "ne": (1, -1),
    }
    direction = ""
    for char in instruction:
        if direction in directions:
            yield directions[direction]
            direction = ""
        direction += char
    yield directions[direction]


def flip(instructions: List[str]) -> Grid:

    tiles: Grid = {}

    for instruction in instructions:
        position = (0, 0)
        for x, y in next_step(instruction):
            position = (position[0] + x, position[1] + y)
        tiles[position] = "black" if position not in tiles else "white"

    return tiles


def neighbours(x: int, y: int) -> Iterable[Coord]:

    for dx, dy in [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]:
        yield x + dx, y + dy


def automata(tiles: Grid) -> Grid:

    expanded = tiles.copy()
    for position in tiles:
        for neighbour in neighbours(*position):
            if neighbour not in tiles:
                expanded[neighbour] = "white"

    next_gen = tiles.copy()

    for position, tile in expanded.items():

        black_tiles = 0
        for neighbour in neighbours(*position):
            if expanded.get(neighbour, "white") == "black":
                black_tiles += 1

        if tile == "white" and black_tiles == 2:
            next_gen[position] = "black"
        elif tile == "black" and (black_tiles == 0 or black_tiles > 2):
            next_gen[position] = "white"

    return next_gen


def simulate(tiles: Grid, days: int = 100) -> Grid:

    current_gen = tiles
    while days > 0:
        current_gen = automata(current_gen)
        black_tiles = len([color for color in current_gen.values() if color == "black"])
        days -= 1
    return current_gen


if __name__ == "__main__":

    instructions = parse_input()

    # First part
    tiles = flip(instructions)
    assert len([color for color in tiles.values() if color == "black"]) == 293

    # Second part
    tiles = simulate(tiles)
    assert len([color for color in tiles.values() if color == "black"]) == 3967
