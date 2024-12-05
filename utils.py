from typing import Generator
from pathlib import Path
import os

def read_lines(path: str | Path) -> Generator[str, None, None]:
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            yield line.strip()


if __name__ == '__main__':
    DAY = 3
    os.mkdir(f'./day{DAY}')
    with open(f'./day{DAY}/day{DAY}.py', 'w+', encoding='utf-8') as file:
        pass
    with open(f'./day{DAY}/input.txt', 'w+', encoding='utf-8') as file:
        pass
    with open(f'./day{DAY}/test.txt', 'w+', encoding='utf-8') as file:
        pass

