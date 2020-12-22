from collections import deque
from typing import List, Deque, Tuple
from pathlib import Path


def parse_input() -> List[Deque[int]]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    return [
        deque(map(int, lines[1 : lines.index("Player 2:")])),
        deque(map(int, lines[lines.index("Player 2:") + 1 :])),
    ]


def combat(deck_1: Deque[int], deck_2: Deque[int]) -> int:

    while deck_1 and deck_2:

        first = deck_1.popleft()
        second = deck_2.popleft()

        if first > second:
            deck_1.extend([first, second])
        else:
            deck_2.extend([second, first])

    return deck_score(deck_1 or deck_2)


def deck_score(deck: Deque[int]) -> int:

    return sum(n * card for n, card in enumerate(reversed(deck), start=1))


def recursive_combat(deck_1: Deque[int], deck_2: Deque[int]) -> Tuple[int, int]:

    seen_decks = set()

    while deck_1 and deck_2:

        state = f"{deck_1}-{deck_2}"
        if state in seen_decks:
            return deck_score(deck_1), 0
        seen_decks.add(state)

        first = deck_1.popleft()
        second = deck_2.popleft()

        if len(deck_1) >= first and len(deck_2) >= second:
            deck_scores = recursive_combat(
                deque(list(deck_1)[:first]), deque(list(deck_2)[:second])
            )
            player_wins = deck_scores[0] > deck_scores[1]
        else:
            player_wins = first > second

        if player_wins:
            deck_1.extend([first, second])
        else:
            deck_2.extend([second, first])

    return deck_score(deck_1), deck_score(deck_2)


if __name__ == "__main__":

    deck_1, deck_2 = parse_input()

    # First part
    assert combat(deck_1.copy(), deck_2.copy()) == 30138

    # Second part
    assert max(recursive_combat(deck_1.copy(), deck_2.copy())) == 31587
