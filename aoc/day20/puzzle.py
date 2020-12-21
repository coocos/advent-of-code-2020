import re
import math
from itertools import chain
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
            # FIXME: You shouldn't generate a duplicate rotation to start with
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


def create_monster_map(tiles: List[Tile]) -> Tile:

    without_edges: List[Tile] = []
    for tile in tiles:
        without_edges.append([row[1:-1] for row in tile[1:-1]])

    size = int(math.sqrt(len(tiles)))

    monster_map = []
    while without_edges:
        row_of_tiles = without_edges[:size]
        for i in range(len(without_edges[0])):
            row = []
            for tile in row_of_tiles:
                row.extend(tile[i])
            monster_map.append(row)
        without_edges = without_edges[size:]

    return monster_map


def is_monster(x: int, y: int, tile: Tile) -> bool:

    coords = [
        (x, y + 1),
        (x + 1, y + 2),
        (x + 4, y + 2),
        (x + 5, y + 1),
        (x + 6, y + 1),
        (x + 7, y + 2),
        (x + 10, y + 2),
        (x + 11, y + 1),
        (x + 12, y + 1),
        (x + 13, y + 2),
        (x + 16, y + 2),
        (x + 17, y + 1),
        (x + 18, y + 1),
        (x + 18, y),
        (x + 19, y + 1),
    ]

    try:
        return all(tile[coord[1]][coord[0]] == "#" for coord in coords)
    except IndexError:
        return False


def water_roughness(tiles: List[Tile]) -> int:

    monsters = 0
    monster_map = create_monster_map(tiles)
    for variation in generate_variations(monster_map):
        for y in range(len(variation)):
            for x in range(len(variation)):
                if is_monster(x, y, variation):
                    monsters += 1

    cells = len([cell for cell in chain(*variation) if cell == "#"])

    # Monster take up 15 hash signs per monster
    return cells - monsters * 15


if __name__ == "__main__":

    tiles = parse_input()

    # First part
    tile_variations = {name: generate_variations(tile) for name, tile in tiles.items()}
    arrangement = find_arrangement(tile_variations)
    corners = corners_from_arrangement(tile_variations, arrangement)
    assert reduce(mul, corners) == 66020135789767

    # Second part
    assert water_roughness(arrangement) == 1537
