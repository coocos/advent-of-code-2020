import re
from typing import List
from pathlib import Path


def parse_input() -> List[str]:
    with open(Path(__file__).parent / "input.txt") as f:
        return [line.strip() for line in f.readlines()]


def execute_v1(instructions: List[str]):

    memory = {}

    for instruction in instructions:
        operation, value = instruction.split(" = ")
        if operation == "mask":
            ones = int(value.replace("X", "0"), base=2)
            zeroes = int(value.replace("X", "1"), base=2)
        else:
            address = int(re.match(r"mem\[(\d+)\]", operation).group(1))
            memory[address] = (int(value) | ones) & zeroes

    return sum(memory.values())


def generate_masks(pre, post=""):

    if not pre:
        yield post
        return

    if pre[0] == "X":
        yield from generate_masks(pre[1:], post + "1")
        yield from generate_masks(pre[1:], post + "0")
    else:
        yield from generate_masks(pre[1:], post + pre[0])


def execute_v2(instructions: List[str]):

    memory = {}

    for instruction in instructions:
        operation, value = instruction.split(" = ")
        if operation == "mask":
            mask = value
        else:
            original_address = int(re.match(r"mem\[(\d+)\]", operation).group(1))
            base_mask = []
            for m, a in zip(mask, "{:036b}".format(original_address)):
                if m == "1":
                    base_mask.append("1")
                elif m == "0":
                    base_mask.append(a)
                else:
                    base_mask.append("X")
            base_mask = "".join(base_mask)
            for address in generate_masks(base_mask):
                memory[int(address, base=2)] = int(value)

    return sum(memory.values())


if __name__ == "__main__":

    instructions = parse_input()

    # First part
    assert execute_v1(instructions) == 16003257187056

    # Second part
    assert execute_v2(instructions) == 3219837697833
