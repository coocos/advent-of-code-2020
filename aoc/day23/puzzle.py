from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from pathlib import Path
from typing import Deque, Dict, List, Optional


def parse_input() -> List[int]:
    with open(Path(__file__).parent / "input.txt") as f:
        return list(map(int, list(f.read().strip())))


class Cup:
    def __init__(self, label: int) -> None:
        self.label = label
        self.next: Optional[Cup] = None

    def pop(self) -> Cup:
        popped = self.next
        if not popped:
            raise RuntimeError("Linked list is not circular")
        self.next = popped.next
        popped.next = None
        return popped

    def insert(self, cup: Cup) -> None:
        temp = self.next
        self.next = cup
        cup.next = temp

    def __repr__(self) -> str:
        return str(self.label) + " -> " + str(self.next.label)


def create_circular_list(labels: List[int]) -> Cup:
    head = Cup(labels[0])
    current = head
    for label in labels[1:]:
        current.next = Cup(label)
        current = current.next
    current.next = head
    return head


def create_label_map(cup: Cup) -> Dict[int, Cup]:
    labels = {}
    head = cup
    while head:
        if head.label in labels:
            break
        labels[head.label] = head
        head = head.next
    return labels


def debug(cup: Cup):
    labels = []
    seen = set()
    current = cup
    while current:
        if current.label in seen:
            break
        labels.append(current.label)
        seen.add(current.label)
        current = current.next
    print(" ".join(map(str, labels)))


def cups_as_str(cup: Cup, target: Cup) -> str:

    labels = []
    seen = set()
    current = cup
    while current:
        if current.label in seen:
            break
        labels.append(
            current.label if current.label != target.label else f"({current.label})"
        )
        seen.add(current.label)
        current = current.next
    return " ".join(map(str, labels))


def play(cup_list: List[int], moves: int = 0) -> str:

    cup = create_circular_list(cup_list)
    cups = create_label_map(cup)
    largest = max(cups)

    move = 1
    current = cup

    while move <= moves:

        pick_up = [current.pop(), current.pop(), current.pop()]

        destination = current.label - 1
        if destination == 0:
            destination = largest
        while destination in map(lambda cup: cup.label, pick_up):
            destination -= 1
            if destination <= 0:
                destination = largest

        while pick_up:
            cups[destination].insert(pick_up.pop())

        current = current.next
        move += 1

    labels_after_one = []
    current = cups[1].next
    for _ in range(8):
        labels_after_one.append(current.label)
        current = current.next
    return labels_after_one


if __name__ == "__main__":

    cups = parse_input()

    # First part
    assert "".join(map(str, play(cups, 100))) == "59374826"
