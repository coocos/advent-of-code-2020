from typing import Dict, Tuple, Iterable
from pathlib import Path


def parse_input() -> Dict[Tuple, str]:
    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    hypergrid: Dict[Tuple, str] = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            hypergrid[(x, y, 0, 0)] = lines[y][x]
    return hypergrid


def neighbours(cube: Tuple) -> Iterable[Tuple]:

    dimensions = len(cube)
    for dx in (-1, 1, 0):
        for dy in (-1, 1, 0):
            for dz in (-1, 1, 0):
                if dimensions == 3:
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

    grid = cubes.copy()
    for cube in cubes:
        for neighbour in neighbours(cube):
            if neighbour not in grid:
                grid[neighbour] = "."

    next_grid = grid.copy()
    for cube, state in grid.items():
        active_neighbours = 0
        for neighbour in neighbours(cube):
            if neighbour in grid and grid[neighbour] == "#":
                active_neighbours += 1
            if active_neighbours > 3:
                break
        if state == "#":
            next_grid[cube] = "#" if active_neighbours in (2, 3) else "."
        elif active_neighbours == 3:
            next_grid[cube] = "#"

    return next_grid


def active_cubes(grid: Dict[Tuple, str]) -> int:

    return len([cube for cube in grid.values() if cube == "#"])


def run_cycles(grid: Dict[Tuple, str], cycles: int) -> Dict[Tuple, str]:

    for _ in range(cycles):
        grid = step(grid)
    return grid


if __name__ == "__main__":

    hypergrid = parse_input()
    grid = {cube[:3]: value for cube, value in hypergrid.items()}

    # First part
    assert active_cubes(run_cycles(grid, cycles=6)) == 237

    # Second part
    assert active_cubes(run_cycles(hypergrid, cycles=6)) == 2448
