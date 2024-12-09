from qwlist import Lazy, QList
from utils import read_lines
import re
from typing import Tuple


def parse_tuple(instruction: str) -> Tuple[int, int]:
    s = instruction[4:]
    s = s[:-1]
    l, r = s.split(',')
    return int(l), int(r)

def sol_a() -> int:
    data = ''.join(read_lines('./input.txt'))
    return (
        Lazy(re.findall(r'mul\([1-9]\d{0,2},[1-9]\d{0,2}\)', data))
        .map(parse_tuple)
        .map(lambda pair: pair[0] * pair[1])
        .sum()
    )


def append_command(acc: Tuple[bool, QList[str]], command) -> Tuple[bool, QList[str]]:
    do, xs = acc
    if command == 'do()':
        return True, xs
    if command == 'don\'t()':
        return False, xs
    if do:
        xs.append(command)
    return do, xs


def sol_b() -> int:
    data = ''.join(read_lines('./input.txt'))
    return (
        Lazy(re.findall(r'mul\([1-9]\d{0,2},[1-9]\d{0,2}\)|do\(\)|don\'t\(\)', data))
        .fold(append_command, (True, QList()))[1]
        .map(parse_tuple)
        .map(lambda pair: pair[0] * pair[1])
        .sum()
    )


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()
