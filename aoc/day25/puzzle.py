from typing import List
from pathlib import Path


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [int(line.strip()) for line in f]


def loop_size(key: int) -> int:

    value = 1
    subject_number = 7
    loop_size = 0
    while value != key:
        value *= subject_number
        value = value % 20201227
        loop_size += 1
    return loop_size


def encryption_key(key: int, loop_size: int) -> int:

    value = 1
    for _ in range(loop_size):
        value *= key
        value = value % 20201227
    return value


if __name__ == "__main__":

    card_key, door_key = parse_input()

    # First part
    card_secret = loop_size(card_key)
    door_secret = loop_size(door_key)
    assert encryption_key(card_key, door_secret) == 18293391
    assert encryption_key(door_key, card_secret) == 18293391
