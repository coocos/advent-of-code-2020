from copy import deepcopy
from typing import List, Tuple, Iterable
from pathlib import Path

Grid = List[List[str]]


def parse_input() -> Grid:
    with open(Path(__file__).parent / "input.txt") as f:
        return [list(line.strip()) for line in f]


surrounding = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


def adjacent_neighbours(x: int, y: int, grid: Grid) -> int:

    occupied = 0
    height = len(grid)
    width = len(grid[0])
    for dx, dy in surrounding:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == "#":
            occupied += 1
    return occupied


def visible_neighbours(x: int, y: int, grid: Grid) -> int:

    occupied = 0
    height = len(grid)
    width = len(grid[0])
    for dx, dy in surrounding:
        pos_x = x
        pos_y = y
        while True:
            pos_x += dx
            pos_y += dy
            if 0 <= pos_x < width and 0 <= pos_y < height:
                if grid[pos_y][pos_x] == "#":
                    occupied += 1
                    break
                elif grid[pos_y][pos_x] == "L":
                    break
            else:
                break
    return occupied


def simulate_adjacent(original: Grid) -> Grid:

    grid = deepcopy(original)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            seat = original[y][x]
            if seat == "L" and adjacent_neighbours(x, y, original) == 0:
                grid[y][x] = "#"
            elif seat == "#" and adjacent_neighbours(x, y, original) >= 4:
                grid[y][x] = "L"
    return grid


def simulate_visible(original: Grid) -> Grid:

    grid = deepcopy(original)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            seat = original[y][x]
            if seat == "L" and visible_neighbours(x, y, original) == 0:
                grid[y][x] = "#"
            elif seat == "#" and visible_neighbours(x, y, original) >= 5:
                grid[y][x] = "L"
    return grid


def count_seats(grid: Grid) -> int:

    occupied = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "#":
                occupied += 1
    return occupied


if __name__ == "__main__":

    original = parse_input()

    # First part
    grid = deepcopy(original)
    while True:
        new_grid = simulate_adjacent(grid)
        if str(new_grid) == str(grid):
            break
        grid = new_grid

    assert count_seats(grid) == 2483

    # Second part
    grid = deepcopy(original)
    while True:
        new_grid = simulate_visible(grid)
        if str(new_grid) == str(grid):
            break
        grid = new_grid

    assert count_seats(grid) == 2285
