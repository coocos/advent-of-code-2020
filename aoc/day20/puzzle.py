import re
import math
from operator import mul
from functools import reduce
from typing import Dict, List, Iterable, Set, Optional
from pathlib import Path

Tile = List[List[str]]


def parse_input() -> Dict[int, Tile]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f]

    tiles = {}
    tile: Tile = []

    for line in lines:
        if not line:
            continue
        elif match := re.match(r"Tile (\d+):", line):
            tile = []
            tiles[int(match.group(1))] = tile
        else:
            tile.append(list(line))
    return tiles


def draw(tile: List[List[str]]) -> None:

    for row in tile:
        print("".join(row))
    print("")


def generate_rotations(tile: Tile) -> Iterable[Tile]:

    size = len(tile)
    rotations = [tile]
    yield tile
    for _ in range(3):
        rotation: Tile = []
        for x in range(size):
            rotation.append([])
            for y in range(size):
                rotation[-1].append(rotations[-1][size - 1 - y][x])
        rotations.append(rotation)
        yield rotation


def generate_variations(tile: Tile) -> List[Tile]:

    original = tile
    horizontal = [list(reversed(row)) for row in tile]
    vertical = [row for row in reversed(tile)]
    size = len(tile)

    variations = []
    for variant in [original, horizontal, vertical]:
        for rotation in generate_rotations(variant):
            # FIXME: You shouldn't generate the same rotation to start with
            if rotation not in variations:
                variations.append(rotation)
    return variations


def find_arrangement(
    tiles: Dict[int, List[Tile]],
    unused_tiles: Optional[Set[int]] = None,
    arrangement: Optional[List[Tile]] = None,
) -> List[Tile]:

    if unused_tiles is None:
        unused_tiles = set(tiles.keys())
    if arrangement is None:
        arrangement = []

    if arrangement:
        position = len(arrangement) - 1
        size = int(math.sqrt(len(tiles)))
        if position >= size:
            top = position - size
            top_valid = arrangement[-1][0] == arrangement[top][-1]
        else:
            # Top row is always valid for tiles above it
            top_valid = True
        if arrangement and position % size != 0:
            last_column = [row[-1] for row in arrangement[-2]]
            first_column = [row[0] for row in arrangement[-1]]
            left_valid = last_column == first_column
        else:
            # First column is always valid for tiles to its left
            left_valid = True

        if not left_valid or not top_valid:
            return []

    if len(arrangement) == len(tiles):
        return arrangement

    for tile in unused_tiles:
        for variation in tiles[tile]:
            valid_arrangement = find_arrangement(
                tiles, unused_tiles - {tile}, arrangement + [variation]
            )
            if valid_arrangement:
                return valid_arrangement

    return []


def corners_from_arrangement(
    tile_variations: Dict[int, List[Tile]], arrangement: List[Tile]
) -> List[int]:

    names = []
    for tile in arrangement:
        for name, variations in tile_variations.items():
            if tile in variations:
                names.append(name)
    size = int(math.sqrt(len(tiles)))
    corner_tiles = [names[0], names[size - 1], names[-size], names[-1]]
    return corner_tiles


if __name__ == "__main__":

    tiles = parse_input()

    # First part
    tile_variations = {}
    for identifier, tile in tiles.items():
        tile_variations[identifier] = generate_variations(tile)

    arrangement = find_arrangement(tile_variations)
    corners = corners_from_arrangement(tile_variations, arrangement)
    assert reduce(mul, corners) == 66020135789767
