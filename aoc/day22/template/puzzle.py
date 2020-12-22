from pathlib import Path

def parse_input() -> str:
    with open(Path(__file__).parent / "input.txt") as f:
        return f.read()


if __name__ == "__main__":
    print(parse_input())
