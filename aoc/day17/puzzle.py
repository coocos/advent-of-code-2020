from pathlib import Path


def parse_input() -> str:
    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    cubes = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            cubes[(x, y, 0)] = lines[y][x]
    return cubes


def bounds(cubes):

    x = (min(cube[0] for cube in cubes.keys()), max(cube[0] for cube in cubes.keys()))
    y = (min(cube[1] for cube in cubes.keys()), max(cube[1] for cube in cubes.keys()))
    z = (min(cube[2] for cube in cubes.keys()), max(cube[2] for cube in cubes.keys()))
    return (x, y, z)


def neighbours(cube):

    x, y, z = cube
    for dx in (-1, 1, 0):
        for dy in (-1, 1, 0):
            for dz in (-1, 1, 0):
                neighbour = (x + dx, y + dy, z + dz)
                if neighbour != cube:
                    yield neighbour


def draw(cubes):

    x_range, y_range, z_range = bounds(cubes)
    for z in range(z_range[0], z_range[1] + 1):
        print(f"z={z}")
        for y in range(y_range[0], y_range[1] + 1):
            row = []
            for x in range(x_range[0], x_range[1] + 1):
                if (x, y, z) in cubes:
                    row.append(cubes[(x, y, z)])
                else:
                    row.append(".")
            print("".join(row))
    print("")


def step(cubes):

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
                # print(f"Keeping {cube} as active")
                expanded_copy[cube] = "#"
            else:
                # print(f"Deactivating {cube}")
                expanded_copy[cube] = "."
        else:
            if active_neighbours == 3:
                # print(f"Activating {cube}")
                expanded_copy[cube] = "#"

    return expanded_copy


def active_cubes(cubes):

    return len([cube for cube in cubes.values() if cube == "#"])


if __name__ == "__main__":

    first_gen = parse_input()

    # First part
    cycle = 1
    next_gen = first_gen
    while cycle <= 6:
        next_gen = step(next_gen)
        cycle += 1

    assert active_cubes(next_gen) == 237
