import collections
from typing import Dict, Tuple, List
from pathlib import Path


BagGraph = Dict[str, List[Tuple[str, int]]]


def parse_input() -> BagGraph:

    with open(Path(__file__).parent / "input.txt") as f:
        raw_rules = [line.strip().replace(",", "") for line in f]

    graph: BagGraph = {}
    for raw_rule in raw_rules:
        tokens = raw_rule.split(" ")
        bag = " ".join(tokens[:2])
        graph[bag] = []
        if tokens[4] == "no":
            continue
        nested_bags = tokens[4:]
        while nested_bags:
            graph[bag].append(
                (f"{nested_bags[1]} {nested_bags[2]}", int(nested_bags[0]))
            )
            nested_bags = nested_bags[4:]
    return graph


def contains_gold_bag(graph: BagGraph, bag: str) -> bool:

    for inner_bag, _ in graph[bag]:
        if inner_bag == "shiny gold" or contains_gold_bag(graph, inner_bag):
            return True

    return False


def count_bags_inside_gold_bag(graph: BagGraph) -> int:

    total = 0
    queue = collections.deque([("shiny gold", 1)])

    while queue:
        bag, quantity = queue.popleft()
        total += quantity
        for inner_bag, inner_quantity in graph[bag]:
            queue.append((inner_bag, quantity * inner_quantity))

    # Minus one because we don't want to count the shiny gold bag itself
    return total - 1


if __name__ == "__main__":

    rules = parse_input()

    # First part
    assert sum(1 for bag in rules if contains_gold_bag(rules, bag)) == 265

    # Second part
    assert count_bags_inside_gold_bag(rules) == 14177
