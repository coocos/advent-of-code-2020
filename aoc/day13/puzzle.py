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

if __name__ == "__main__":

    time, buses = parse_input()

    # First part
    assert earliest_bus(time, buses) == 222
