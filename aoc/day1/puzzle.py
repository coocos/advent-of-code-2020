from functools import reduce
from operator import mul
from typing import List, Set, Optional
from pathlib import Path


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [int(line.strip()) for line in f.readlines()]


def find_sum_components(
    values: List[int], count: int, target: int, components: Optional[List[int]] = None
) -> List[int]:
    """Returns N values which sum to the given target value"""

    if components is None:
        components = []

    if sum(components) > target or len(components) > count:
        return []
    elif sum(components) == target and len(components) == count:
        return components

    for value in values:
        sum_components = find_sum_components(
            values, count, target, components + [value]
        )
        if sum_components:
            return sum_components

    return []


if __name__ == "__main__":

    values = parse_input()

    # First part
    assert reduce(mul, find_sum_components(values, 2, 2020)) == 440979

    # Second part
    assert reduce(mul, find_sum_components(values, 3, 2020)) == 82498112
