from typing import Generator
from pathlib import Path

def read_lines(day: int) -> Generator[str, None, None]:
    with open(Path(__file__).parent / f'day{day}' / 'input.txt', 'r', encoding='utf8') as file:
        for line in file:
            yield line.strip()
