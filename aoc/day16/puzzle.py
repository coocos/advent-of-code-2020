import re
import collections
from operator import mul
from functools import reduce
from itertools import chain
from typing import Tuple, Dict, List, Set
from pathlib import Path


def parse_input() -> Tuple[List[List[int]], Dict[str, Set[int]]]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    fields = {}
    tickets = []

    field_pattern = r"(.+): (\d+)-(\d+) or (\d+)-(\d+)"
    ticket_pattern = r"\d,?"

    for line in lines:
        if match := re.match(field_pattern, line):
            name = match.group(1)
            first = (int(match.group(2)), int(match.group(3)))
            second = (int(match.group(4)), int(match.group(5)))
            fields[name] = set(range(first[0], first[1] + 1)) | set(
                range(second[0], second[1] + 1)
            )
        elif re.match(ticket_pattern, line):
            tickets.append([int(value) for value in line.split(",")])

    return tickets, fields


def ticket_scanning_error_rate(
    tickets: List[List[int]], fields: Dict[str, Set[int]]
) -> int:

    valid_values = set(chain(*fields.values()))
    ticket_values = chain(*tickets)
    return sum(value for value in ticket_values if value not in valid_values)


def valid_tickets_only(
    tickets: List[List[int]], fields: Dict[str, Set[int]]
) -> List[List[int]]:

    valid_values = set(chain(*fields.values()))
    return [ticket for ticket in tickets if set(ticket) < valid_values]


def possible_field_positions(
    tickets: List[List[int]], fields: Dict[str, Set[int]]
) -> Dict[int, Set[str]]:

    possible_fields = {
        position: set(fields.keys()) for position in range(len(tickets[0]))
    }

    for ticket in tickets:
        for position, value in enumerate(ticket):
            for field, valid_values in fields.items():
                if value not in valid_values:
                    if field in possible_fields[position]:
                        possible_fields[position].remove(field)

    return possible_fields


def find_field_order(possible_fields: Dict[int, Set[str]]) -> List[str]:

    order = ["" for _ in possible_fields]
    while possible_fields:
        for position, fields in possible_fields.items():
            if len(fields) == 1:
                order[position] = fields.pop()
                del possible_fields[position]
                break
        for fields in possible_fields.values():
            if order[position] in fields:
                fields.remove(order[position])

    return order


if __name__ == "__main__":

    # First part
    tickets, fields = parse_input()
    my_ticket, *other_tickets = tickets
    assert ticket_scanning_error_rate(tickets, fields) == 28884

    # Second part
    valid_tickets = valid_tickets_only(other_tickets, fields)
    possible_fields = possible_field_positions(valid_tickets, fields)
    departure_fields = []
    for position, field in enumerate(find_field_order(possible_fields)):
        if field.startswith("departure"):
            departure_fields.append(my_ticket[position])
    assert reduce(mul, departure_fields) == 1001849322119
