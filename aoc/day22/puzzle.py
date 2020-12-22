from collections import deque
from typing import List, Deque
from pathlib import Path


def parse_input() -> List[List[int]]:

    with open(Path(__file__).parent / "input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    return [
        list(map(int, lines[1 : lines.index("Player 2:")])),
        list(map(int, lines[lines.index("Player 2:") + 1 :])),
    ]


def combat(decks: List[List[int]]) -> int:

    deck_1, deck_2 = (deque(deck) for deck in decks)

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


def recursive_combat(deck_1: Deque[int], deck_2: Deque[int], game: int = 1):

    seen_decks = set()

    while deck_1 and deck_2:

        state = f"{deck_1}-{deck_2}"
        if state in seen_decks:
            if game == 1:
                return deck_1
            else:
                return True
        seen_decks.add(state)

        first = deck_1.popleft()
        second = deck_2.popleft()

        player_won = False
        if len(deck_1) >= first and len(deck_2) >= second:
            player_won = recursive_combat(
                deque(list(deck_1)[:first]), deque(list(deck_2)[:second]), game + 1
            )
            if player_won:
                deck_1.extend([first, second])
            else:
                deck_2.extend([second, first])
        elif first > second:
            deck_1.extend([first, second])
        else:
            deck_2.extend([second, first])

    if game == 1:
        return deck_1 or deck_2

    if deck_1:
        return True
    else:
        return False


if __name__ == "__main__":

    decks = parse_input()

    # First part
    assert combat(decks) == 30138

    # Second part
    winning_deck = recursive_combat(deque(decks[0]), deque(decks[1]))
    assert (
        sum(n * card for n, card in enumerate(reversed(winning_deck), start=1)) == 31587
    )
