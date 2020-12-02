import re
from typing import List, Tuple, Counter
from collections import namedtuple, Counter
from pathlib import Path


Policy = namedtuple("NamedTuple", ["low", "high", "letter"])


def parse_input() -> List[Tuple[Policy, str]]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    passwords = []
    pattern = r"(?P<low>\d+)-(?P<high>\d+) (?P<letter>\w): (?P<password>\w+)"
    for line in lines:
        match = re.match(pattern, line)
        if not match:
            raise RuntimeError(f"Failed to parse {line}")
        policy = Policy(
            int(match.group("low")), int(match.group("high")), match.group("letter")
        )
        passwords.append((policy, match.group("password")))
    return passwords


def first_policy(policy: Policy, password: str) -> int:
    letters = Counter(password)
    return (
        policy.letter in letters and policy.low <= letters[policy.letter] <= policy.high
    )


def second_policy(policy: Policy, password: str) -> bool:
    first = password[policy.low - 1] == policy.letter
    second = password[policy.high - 1] == policy.letter
    return first != second


if __name__ == "__main__":

    passwords = parse_input()

    # First part
    assert (
        sum(1 for policy, password in passwords if first_policy(policy, password))
        == 378
    )

    # Second part
    assert (
        sum(1 for policy, password in passwords if second_policy(policy, password))
        == 280
    )
