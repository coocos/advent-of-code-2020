import collections
from typing import List, Dict
from pathlib import Path


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        adapters = sorted(int(line) for line in f.readlines())
    return adapters + [adapters[-1] + 3]


def ones_and_threes(adapters: List[int]) -> int:

    differences: Dict[int, int] = collections.defaultdict(int)
    previous = 0
    for adapter in adapters:
        differences[adapter - previous] += 1
        previous = adapter
    return differences[1] * differences[3]


def count_arrangements(adapters: List[int]) -> int:

    paths_to_adapter = {adapter: 0 for adapter in adapters}
    paths_to_adapter[0] = 1

    for adapter in paths_to_adapter:
        for jolt in [1, 2, 3]:
            if adapter - jolt in paths_to_adapter:
                paths_to_adapter[adapter] += paths_to_adapter[adapter - jolt]

    return paths_to_adapter[adapters[-1]]


if __name__ == "__main__":

    adapters = parse_input()

    # First part
    assert ones_and_threes(adapters) == 2592

    # Second part
    assert count_arrangements(adapters) == 198428693313536
