from qwlist import Lazy, QList
from utils import read_lines, fst, snd


def sol_a() -> int:
    numbers = Lazy(next(read_lines('./input.txt')))
    data, free_space = (
        numbers
        .enumerate()
        .group_by(lambda pair: pair[0] % 2)
        .map(lambda group: group.map(snd).map(int).collect())
    )
    return -1


def sol_b() -> int:
    return -1


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()