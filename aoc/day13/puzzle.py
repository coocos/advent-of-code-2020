import sys
import math
from functools import reduce
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


def least_common_multiple(numbers: List[int]) -> int:

    return reduce(lambda a, b: a * b // math.gcd(a, b), numbers)


def synced_buses(buses: List[str]) -> int:

    bus_offsets = [(int(bus), i) for i, bus in enumerate(buses) if bus != "x"]

    time = 0
    step = bus_offsets[0][0]
    locked = 1

    while True:
        synced = 0
        for bus, offset in bus_offsets:
            if (time + offset) % bus != 0:
                break
            synced += 1
        if synced > locked:
            step = least_common_multiple([bus[0] for bus in bus_offsets][:synced])
            locked = synced
        if locked == len(bus_offsets):
            break
        time += step

    return time


if __name__ == "__main__":

    time, buses = parse_input()

    # First part
    assert earliest_bus(time, buses) == 222

    # Second part
    assert synced_buses(buses) == 408270049879073
