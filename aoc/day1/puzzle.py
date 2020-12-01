from functools import reduce
from typing import List, Set, Optional
from pathlib import Path


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [int(line.strip()) for line in f.readlines()]


def find_sum_components(
    entries: List[int], length: int, target: int, components: Optional[List[int]] = None
) -> List[int]:

    if components is None:
        components = []

    if sum(components) > target or len(components) > length:
        return []
    elif sum(components) == target and len(components) == length:
        return components

    for entry in entries:
        valid_path = find_sum_components(entries, length, target, components + [entry])
        if valid_path:
            return valid_path

    return []


if __name__ == "__main__":

    entries = parse_input()

    # First part
    assert reduce(lambda x, y: x * y, find_sum_components(entries, 2, 2020)) == 440979

    # Second part
    assert reduce(lambda x, y: x * y, find_sum_components(entries, 3, 2020)) == 82498112