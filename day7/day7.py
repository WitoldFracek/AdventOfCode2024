from qwlist import Lazy, QList
from utils import read_lines
from typing import Callable, Tuple, Iterable


def concat(a: int, b: int) -> int:
    return int(f'{a}{b}')


def is_solvable(target: int, args: QList[int], operations: Iterable[Callable[[int, int], int]]) -> bool:
    return args.skip(1).flat_fold(lambda acc, x: [op(acc, x) for op in operations], args[0]).any(lambda x: x == target)


def parse_line(line: str) -> Tuple[int, QList[int]]:
    target, numbers = line.split(':')
    numbers = QList(numbers.split(' ')).filter(lambda x: x != '').map(int).collect()
    return int(target), numbers


def sol_a() -> int:
    operators = [int.__add__, int.__mul__]
    return (
        Lazy(read_lines('./input.txt'))
        .map(parse_line)
        .filter(lambda pair: is_solvable(pair[0], pair[1], operators))
        .map(lambda pair: pair[0])
        .collect()
        .sum()
    )


def sol_b() -> int:
    operators = [int.__add__, int.__mul__, concat]
    return (
        Lazy(read_lines('./input.txt'))
        .map(parse_line)
        .filter(lambda pair: is_solvable(pair[0], pair[1], operators))
        .map(lambda pair: pair[0])
        .collect()
        .sum()
    )


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()