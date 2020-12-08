from typing import List, Tuple, Iterable
from pathlib import Path

Program = List[Tuple[str, int]]


def parse_input() -> Program:

    with open(Path(__file__).parent / "input.txt") as f:
        instructions = [line.strip().split() for line in f]
    return [(operation, int(argument)) for operation, argument in instructions]


def patched_programs(program: Program) -> Iterable[Program]:

    patched_operations = {"nop": "jmp", "jmp": "nop"}
    for address, instruction in enumerate(program):
        operation, argument = instruction
        if operation in patched_operations:
            patched_program = program[:]
            patched_program[address] = (patched_operations[operation], argument)
            yield patched_program


def execute(program: Program) -> Tuple[int, bool]:

    executed = set()
    accumulator = 0
    pointer = 0

    while pointer not in executed:
        executed.add(pointer)
        try:
            operation, argument = program[pointer]
        except IndexError:
            return accumulator, False
        if operation == "nop":
            pointer += 1
        elif operation == "acc":
            accumulator += argument
            pointer += 1
        elif operation == "jmp":
            pointer += argument
        else:
            raise RuntimeError(f"Unknown operation: {operation}")

    return accumulator, True


if __name__ == "__main__":

    program = parse_input()

    # First part
    accumulator, looped = execute(program)
    assert accumulator == 1867

    # Second part
    for patched_program in patched_programs(program):
        accumulator, looped = execute(patched_program)
        if not looped:
            break
    assert accumulator == 1303
