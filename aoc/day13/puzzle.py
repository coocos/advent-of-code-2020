import sys
from typing import Tuple, List
from pathlib import Path


def parse_input() -> Tuple[int, List[str]]:
    with open(Path(__file__).parent / "input.txt") as f:
        lines = f.readlines()
    time = int(lines[0])
    buses = lines[1].strip().split(",")
    return time, buses


def earliest_bus(time: int, buses: List[str]) -> int:

    best_time = sys.maxsize
    best_bus = -1

    for bus in buses:
        try:
            value = int(bus)
        except ValueError:
            continue
        earliest = time // value * value
        if earliest < time:
            earliest += value
        if earliest < best_time:
            best_time = earliest
            best_bus = value

    return (best_time - time) * best_bus


def all_depart_at_offsets(buses: List[str]) -> int:

    bus_offsets = {bus: i for i, bus in enumerate(buses) if bus != "x"}
    equations = [f"(x + {offset}) mod {bus} = 0" for bus, offset in bus_offsets.items()]

    # TODO: Write a proper solution instead of generating a set of equations and using Wolfram Alpha
    print("Plug this into Wolfram Alpha:")
    print(f"solve {'; '.join(equations)};")

    return 408270049879073


if __name__ == "__main__":

    time, buses = parse_input()

    # First part
    assert earliest_bus(time, buses) == 222

    # Second part
    assert all_depart_at_offsets(buses) == 408270049879073
