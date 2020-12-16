import re
import collections
from typing import Tuple, Dict, List
from pathlib import Path


def parse_input() -> Tuple[List, Dict]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    rules = {}
    tickets = []

    rule_pattern = r"(.+): (\d+)-(\d+) or (\d+)-(\d+)"
    ticket_pattern = r"\d,?"

    for line in lines:
        if match := re.match(rule_pattern, line):
            name = match.group(1)
            first = (int(match.group(2)), int(match.group(3)))
            second = (int(match.group(4)), int(match.group(5)))
            rules[name] = set(range(first[0], first[1] + 1)) | set(range(second[0], second[1] + 1))
        elif re.match(ticket_pattern, line):
            tickets.append([int(value) for value in line.split(",")])

    return tickets, rules


def ticket_scanning_error_rate(tickets, rules) -> int:

    valid_values = set()
    for rule_values in rules.values():
        valid_values.update(rule_values)

    error_rate = 0
    for ticket in tickets:
        for value in ticket:
            if value not in valid_values:
                error_rate += value
    return error_rate


def valid_tickets_only(tickets, rules) -> List:

    valid_values = set()
    for rule_values in rules.values():
        valid_values.update(rule_values)

    valid_tickets = []
    for ticket in tickets:
        if all(value in valid_values for value in ticket):
            valid_tickets.append(ticket)
    return valid_tickets


def possible_rules(tickets, rules):

    possible = collections.defaultdict(set)
    for position in range(len(tickets[0])):
        for rule in rules:
            possible[position].add(rule)

    for ticket in tickets:
        for position, value in enumerate(ticket):
            for rule, allowed_values in rules.items():
                if value not in allowed_values:
                    if rule in possible[position]:
                        possible[position].remove(rule)

    return possible


def find_rule_order(possible) -> List[str]:

    order = ["" for _ in possible]
    while possible:
        for position, rules in possible.items():
            if len(rules) == 1:
                order[position] = rules.pop()
                break
        del possible[position]
        for rules in possible.values():
            if order[position] in rules:
                rules.remove(order[position])
    return order

if __name__ == "__main__":

    # First part
    tickets, rules = parse_input()
    my_ticket, *other_tickets = tickets

    assert ticket_scanning_error_rate(tickets, rules) == 28884

    # Second part
    valid_tickets = valid_tickets_only(other_tickets, rules)
    possible = possible_rules(valid_tickets, rules)
    rule_order = find_rule_order(possible)
    product = 1
    for position, rule in enumerate(rule_order):
        if rule.startswith("departure"):
            product *= my_ticket[position]
    assert product == 1001849322119
