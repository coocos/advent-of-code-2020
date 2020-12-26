import re
import collections
from pprint import pprint
from typing import Tuple, Dict, List
from pathlib import Path


def parse_input() -> Tuple[Dict, List]:
    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    rules = {}
    messages = []

    rule_pattern = r"^(\d+): (.*)$"
    for line in lines:
        if match := re.match(rule_pattern, line):
            name = match.group(1)
            rules[name] = match.group(2).replace('"', "").split(" ")
        else:
            messages.append(line)
    return rules, messages


def rule_to_regex(rule, rules):

    parts = []
    for token in rule:
        if token == "a" or token == "b":
            return token
        elif token == "|":
            parts.append(token)
            continue
        parts.append(rule_to_regex(rules[token], rules))
    return f"(?:{''.join(parts)})"


def matches_zero_rule(rules, messages):

    regexes = {}
    for name, rule in rules.items():
        regexes[name] = re.compile(f"^{rule_to_regex(rule, rules)}$")

    matches = 0
    for message in messages:
        if regexes["0"].match(message):
            matches += 1
    return matches


if __name__ == "__main__":

    rules, messages = parse_input()

    assert matches_zero_rule(rules, messages) == 198
