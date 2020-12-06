from itertools import chain
from functools import reduce
from typing import List
from pathlib import Path


def parse_input() -> List[List[str]]:
    with open(Path(__file__).parent / "input.txt") as f:
        groups = f.read().split("\n\n")
    return [group.split("\n") for group in groups]


if __name__ == "__main__":

    groups = parse_input()

    # First part
    yes_answers = sum(len(set(chain(*g))) for g in groups)
    assert yes_answers == 6504

    # Second part
    yes_answers = sum(len(reduce(lambda x, y: set(x) & set(y), g)) for g in groups)
    assert yes_answers == 3351
