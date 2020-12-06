import re
from typing import List, Dict, Callable, Any
from pathlib import Path

Passport = Dict[str, str]


def parse_input() -> List[Passport]:
    with open(Path(__file__).parent / "input.txt") as f:
        raw_passports = [
            re.split(r" |\n", passport) for passport in f.read().split("\n\n")
        ]
    passports: List[Passport] = []
    for raw_passport in raw_passports:
        passports.append(dict(field.split(":") for field in raw_passport))
    return passports


def field_rules() -> Dict[str, Callable[[str], Any]]:
    def _hgt(height: str) -> bool:
        if not re.match(r"^\d+(cm|in)$", height):
            return False
        value, unit = int(height[:-2]), height[-2:]
        return 150 <= value <= 193 if unit == "cm" else 59 <= value <= 76

    return {
        "byr": lambda year: 1920 <= int(year) <= 2002,
        "iyr": lambda year: 2010 <= int(year) <= 2020,
        "eyr": lambda year: 2020 <= int(year) <= 2030,
        "hgt": _hgt,
        "hcl": lambda hair: re.match(r"^#[0-9a-f]{6}$", hair),
        "ecl": lambda eyes: re.match(r"^(?:amb|blu|brn|gry|grn|hzl|oth)$", eyes),
        "pid": lambda passport: re.match(r"^[0-9]{9}$", passport),
    }


if __name__ == "__main__":

    passports = parse_input()
    rules = field_rules()

    # First and second part combined
    passports_with_required_fields = 0
    passports_with_valid_fields = 0

    for passport in passports:

        required_fields = all(field in passport for field in rules)
        valid_fields = required_fields and all(
            rule(passport.get(field, "")) for field, rule in rules.items()
        )

        passports_with_required_fields += int(required_fields)
        passports_with_valid_fields += int(valid_fields)

    assert passports_with_required_fields == 260
    assert passports_with_valid_fields == 153
