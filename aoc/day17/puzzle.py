from typing import Dict, Tuple, Iterable
from pathlib import Path


def parse_input() -> Dict[Tuple, str]:
    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    hypercubes: Dict[Tuple, str] = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            hypercubes[(x, y, 0, 0)] = lines[y][x]
    return hypercubes


def neighbours(cube: Tuple) -> Iterable[Tuple]:

    for dx in (-1, 1, 0):
        for dy in (-1, 1, 0):
            for dz in (-1, 1, 0):
                if len(cube) == 3:
                    x, y, z = cube
                    neighbour = (x + dx, y + dy, z + dz)
                    if neighbour != cube:
                        yield neighbour
                else:
                    x, y, z, w = cube
                    for dw in (-1, 1, 0):
                        neighbour = (x + dx, y + dy, z + dz, w + dw)
                        if neighbour != cube:
                            yield neighbour


def step(cubes: Dict[Tuple, str]) -> Dict[Tuple, str]:

    expanded = cubes.copy()

    for cube in cubes:
        for neighbour in neighbours(cube):
            if neighbour not in expanded:
                expanded[neighbour] = "."

    expanded_copy = expanded.copy()
    for cube, state in expanded.items():
        active_neighbours = 0
        for neighbour in neighbours(cube):
            if neighbour in expanded and expanded[neighbour] == "#":
                active_neighbours += 1
        if state == "#":
            if active_neighbours in (2, 3):
                expanded_copy[cube] = "#"
            else:
                expanded_copy[cube] = "."
        else:
            if active_neighbours == 3:
                expanded_copy[cube] = "#"

    return expanded_copy


def active_cubes(cubes: Dict[Tuple, str]) -> int:

    return len([cube for cube in cubes.values() if cube == "#"])


if __name__ == "__main__":

    first_gen = parse_input()

    simpler_first_gen = {cube[:3]: value for cube, value in first_gen.items()}
    # First part
    cycle = 1
    next_gen = simpler_first_gen
    while cycle <= 6:
        next_gen = step(next_gen)
        cycle += 1
    assert active_cubes(next_gen) == 237


    # Second part
    cycle = 1
    next_gen = first_gen
    while cycle <= 6:
        next_gen = step(next_gen)
        cycle += 1
    assert active_cubes(next_gen) == 2448
