import re
import collections
from typing import List, Dict, TypedDict, Set
from pathlib import Path


class Food(TypedDict):

    ingredients: List[str]
    allergens: List[str]


def parse_input() -> List[Food]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f]

    foods: List[Food] = []
    for line in lines:
        if match := re.match(r"(.*) \(contains (.*)\)", line):
            ingredients = match.group(1).strip()
            allergens = match.group(2).strip()
            foods.append(
                {"ingredients": ingredients.split(), "allergens": allergens.split(", ")}
            )
    return foods


def solve_allergens(foods: List[Food]) -> Dict[str, str]:

    candidates: Dict[str, Set[str]] = {}
    for food in foods:
        for allergen in food["allergens"]:
            if allergen in candidates:
                candidates[allergen] = candidates[allergen] & set(food["ingredients"])
            else:
                candidates[allergen] = set(food["ingredients"])

    confirmed_allergens = collections.deque(
        [
            (allergen, candidate.pop())
            for allergen, candidate in candidates.items()
            if len(candidate) == 1
        ]
    )

    allergens = {}
    while confirmed_allergens:
        allergen, ingredient = confirmed_allergens.popleft()
        allergens[allergen] = ingredient
        for other_allergen, allergen_candidates in candidates.items():
            if ingredient in allergen_candidates:
                allergen_candidates.remove(ingredient)
                if len(allergen_candidates) == 1:
                    confirmed_allergens.append(
                        (other_allergen, allergen_candidates.pop())
                    )
    return allergens


def safe_ingredient_count(foods: List[Food], allergens: Dict[str, str]) -> int:

    safe_count = 0
    for food in foods:
        for ingredient in food["ingredients"]:
            if ingredient not in allergens.values():
                safe_count += 1

    return safe_count


def dangerous_ingredients(allergens: Dict[str, str]) -> str:

    return ",".join(allergens[allergen] for allergen in sorted(allergens.keys()))


if __name__ == "__main__":

    foods = parse_input()
    allergens = solve_allergens(foods)

    # First part
    assert safe_ingredient_count(foods, allergens) == 2072

    # Second part
    assert (
        dangerous_ingredients(allergens)
        == "fdsfpg,jmvxx,lkv,cbzcgvc,kfgln,pqqks,pqrvc,lclnj"
    )
