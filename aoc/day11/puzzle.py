from itertools import chain
from copy import deepcopy
from typing import List, Tuple, Iterable, Dict, Literal
from pathlib import Path


def parse_input() -> List[List[str]]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [list(line.strip()) for line in f]


directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


def adjacent_seats(x: int, y: int, grid: List[List[str]]) -> List[Tuple[int, int]]:

    seats = []
    for dx, dy in directions:
        pos_x = x + dx
        pos_y = y + dy
        if (
            0 <= pos_x < len(grid[0])
            and 0 <= pos_y < len(grid)
            and grid[pos_y][pos_x] == "L"
        ):
            seats.append((pos_x, pos_y))
    return seats


def visible_seats(x: int, y: int, grid: List[List[str]]) -> List[Tuple[int, int]]:

    seats = []
    for dx, dy in directions:
        pos_x = x
        pos_y = y
        while True:
            pos_x += dx
            pos_y += dy
            if pos_x < 0 or pos_x >= len(grid[0]) or pos_y < 0 or pos_y >= len(grid):
                break
            if grid[pos_y][pos_x] == "L":
                seats.append((pos_x, pos_y))
                break
    return seats


def seat_graph(grid: List[List[str]]) -> Dict:

    graph = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "L":
                graph[(x, y)] = {
                    "adjacent": adjacent_seats(x, y, grid),
                    "visible": visible_seats(x, y, grid),
                }
    return graph


def step(
    graph: Dict, generation: Dict, preference: Literal["visible", "adjacent"]
) -> Dict:

    next_generation = generation.copy()
    for seat in generation:
        if generation[seat] == "L":
            occupied = 0
            for neighbour in graph[seat][preference]:
                if generation[neighbour] == "#":
                    occupied += 1
                    break
            if not occupied:
                next_generation[seat] = "#"
        else:
            occupied = 0
            for neighbour in graph[seat][preference]:
                if generation[neighbour] == "#":
                    occupied += 1
                    if occupied >= (4 if preference == "adjacent" else 5):
                        next_generation[seat] = "L"
                        break
    return next_generation


def simulate(
    graph: Dict, generation: Dict, preference: Literal["adjacent", "visible"]
) -> int:

    generation = generation.copy()
    while (next_generation := step(graph, generation, preference)) != generation:
        generation = next_generation
    return len([seat for seat in generation.values() if seat == "#"])


if __name__ == "__main__":

    graph = seat_graph(parse_input())
    first_generation = {position: "L" for position in graph}

    # First part
    assert simulate(graph, first_generation, "adjacent") == 2483

    # Second part
    assert simulate(graph, first_generation, "visible") == 2285
