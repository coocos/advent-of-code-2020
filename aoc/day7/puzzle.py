import re
import collections
from typing import Dict, Tuple, List
from pathlib import Path


BagGraph = Dict[str, List[Tuple[str, int]]]


def parse_input() -> BagGraph:

    with open(Path(__file__).parent / "input.txt") as f:
        rules = [line.strip().replace(",", "") for line in f]

    pattern = r"(\w+ \w+) bags contain (.+)\."
    inner_pattern = r"(\d+) (\w+ \w+) bags?"

    graph: BagGraph = {}
    for rule in rules:
        bag, inner_bags = re.match(pattern, rule).groups()
        graph[bag] = []
        for quantity, name in re.findall(inner_pattern, inner_bags):
            graph[bag].append((name, int(quantity)))

    return graph


def contains_bag(graph: BagGraph, bag: str, target: str) -> bool:

    for inner_bag, _ in graph[bag]:
        if inner_bag == target or contains_bag(graph, inner_bag, target):
            return True
    return False


def count_bags_within_bag(graph: BagGraph, bag: str) -> int:

    bags = 0
    queue = collections.deque([(bag, 1)])

    while queue:
        bag, quantity = queue.popleft()
        bags += quantity
        for inner_bag, inner_quantity in graph[bag]:
            queue.append((inner_bag, quantity * inner_quantity))

    # Minus one because we don't want to count the shiny gold bag itself
    return bags - 1


if __name__ == "__main__":

    graph = parse_input()

    # First part
    assert sum(1 for bag in graph if contains_bag(graph, bag, "shiny gold")) == 265

    # Second part
    assert count_bags_within_bag(graph, "shiny gold") == 14177
