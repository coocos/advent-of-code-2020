import re
from typing import List, Iterable
from pathlib import Path


def parse_input() -> List[List[str]]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [line.strip().split(" = ") for line in f.readlines()]


def execute_decoder_v1(instructions: List[List[str]]):

    memory = {}

    for operation, value in instructions:
        if operation == "mask":
            ones = int(value.replace("X", "0"), base=2)
            zeroes = int(value.replace("X", "1"), base=2)
        else:
            address = int(operation[4 : operation.index("]")])
            memory[address] = (int(value) | ones) & zeroes

    return sum(memory.values())


def addresses(unapplied: List[str], applied: List[str] = None) -> Iterable[int]:

    if not unapplied and applied:
        yield int("".join(applied), base=2)
        return

    if applied is None:
        applied = []

    bit, *rest = unapplied
    if bit == "X":
        yield from addresses(rest, applied + ["1"])
        yield from addresses(rest, applied + ["0"])
    else:
        yield from addresses(rest, applied + [bit])


def execute_decoder_v2(instructions: List[List[str]]):

    memory = {}

    for operation, value in instructions:
        if operation == "mask":
            bitmask = value
        else:
            address = "{:036b}".format(int(operation[4 : operation.index("]")]))
            mask = [a if m == "0" else m for m, a in zip(bitmask, address)]
            for floating_address in addresses(mask):
                memory[floating_address] = int(value)

    return sum(memory.values())


if __name__ == "__main__":

    instructions = parse_input()

    # First part
    assert execute_decoder_v1(instructions) == 16003257187056

    # Second part
    assert execute_decoder_v2(instructions) == 3219837697833
