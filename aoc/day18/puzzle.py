from typing import List, Union, Callable
from operator import add, mul
from pathlib import Path


def parse_input() -> List[List[Union[str, int]]]:
    with open(Path(__file__).parent / "input.txt") as f:
        lines = [list(line.strip().replace(" ", "")) for line in f.readlines()]
    expressions = []
    for line in lines:
        expressions.append([int(c) if c.isnumeric() else c for c in line])
    return expressions


def left_to_right(expression: List[Union[str, int]]) -> int:

    accumulator = expression[0]
    operator = add
    for token in expression[1:]:
        if type(token) is int:
            accumulator = operator(accumulator, token)
        else:
            operator = add if token == "+" else mul
    return accumulator


def add_before_multiply(expression: List[Union[str, int]]) -> int:

    for operator, operation in [("+", add), ("*", mul)]:
        while operator in expression:
            pos = expression.index(operator)
            token = operation(expression[pos - 1], expression[pos + 1])
            expression = expression[: pos - 1] + [token] + expression[pos + 2 :]
    return expression[0]


def calculate(expression: List[Union[str, int]], apply_rule: Callable) -> int:

    stack = []
    current_expression = []

    for token in expression:
        if token == "(":
            stack.append(current_expression)
            current_expression = []
        elif token == ")":
            result = apply_rule(current_expression)
            current_expression = stack.pop()
            current_expression.append(result)
        else:
            current_expression.append(token)

    return apply_rule(current_expression)


if __name__ == "__main__":

    expressions = parse_input()

    # First part
    assert sum(calculate(exp, left_to_right) for exp in expressions) == 510009915468

    # Second part
    assert (
        sum(calculate(exp, add_before_multiply) for exp in expressions)
        == 321176691637769
    )
