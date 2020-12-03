from functools import reduce
from operator import mul
from collections import namedtuple
from typing import List, Tuple
from pathlib import Path

Grid = List[List[str]]
Point = namedtuple("Point", ["x", "y"])


def parse_input() -> Grid:
    with open(Path(__file__).parent / "input.txt") as f:
        return [list(line.strip()) for line in f]


def trees_hit(grid: Grid, slope: Point) -> int:
    trees = 0
    width = len(grid[0])
    height = len(grid)
    position = Point(0, 0)
    while position.y < height:
        if grid[position.y][position.x] == "#":
            trees += 1
        position = Point((position.x + slope.x) % width, position.y + slope.y)
    return trees


if __name__ == "__main__":

    grid = parse_input()

    # First part
    assert trees_hit(grid, Point(3, 1)) == 268

    # Second part
    slopes = [Point(1, 1), Point(3, 1), Point(5, 1), Point(7, 1), Point(1, 2)]
    assert reduce(mul, [trees_hit(grid, slope) for slope in slopes]) == 3093068400
