from qwlist import Lazy, QList
from utils import read_lines
from typing import Tuple


def collect_numbers(acc: Tuple[QList[int], QList[int]], pair: Tuple[int, int]) -> Tuple[QList[int], QList[int]]:
    left, right = acc
    left.append(pair[0])
    right.append(pair[1])
    return left, right


def sol_a() -> int:
    left, right = (
        Lazy(read_lines(1))
        .map(lambda line: line.split(' '))
        .map(lambda x: (int(x[0]), int(x[-1])))
        .fold(collect_numbers, (QList(), QList()))
    )
    return (
        left
        .sorted()
        .zip(right.sorted())
        .map(lambda pair: abs(pair[0] - pair[1]))
        .sum()
    )

def sol_b() -> int:
    return -1

def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()
