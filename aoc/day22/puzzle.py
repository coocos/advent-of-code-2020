import collections
from typing import List
from pathlib import Path


def parse_input() -> List[List[int]]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    return [
        list(map(int, lines[1 : lines.index("Player 2:")])),
        list(map(int, lines[lines.index("Player 2:") + 1 :])),
    ]


def winners_score(cards: List[List[int]]):

    deck_1, deck_2 = (collections.deque(deck) for deck in cards)

    while deck_1 and deck_2:

        first = deck_1.popleft()
        second = deck_2.popleft()

        if first > second:
            deck_1.append(first)
            deck_1.append(second)
        else:
            deck_2.append(second)
            deck_2.append(first)

    return sum(n * card for n, card in enumerate(reversed(deck_1 or deck_2), start=1))


if __name__ == "__main__":

    cards = parse_input()

    # First part
    assert winners_score(cards) == 30138
