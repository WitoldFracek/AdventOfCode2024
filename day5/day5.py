from qwlist import Lazy, QList
from utils import read_lines
from typing import List, TypeVar, Set

T = TypeVar('T')


class Page:
    def __init__(self, value: str, rules: Set[str]):
        self.value = value
        self.rules = rules

    def __lt__(self, other) -> bool:
        if not isinstance(other, Page):
            return NotImplemented
        if f'{other.value}|{self.value}' in self.rules:
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Page):
            return NotImplemented
        return self.value == other.value


def is_sequence_correct(seq: List[str], rules: Set[str]) -> bool:
    for i in range(len(seq)):
        a = seq[i]
        for j in range(i, len(seq)):
            b = seq[j]
            if f'{b}|{a}' in rules:
                return False
    return True


def take_middle(seq: List[T]) -> T:
    return seq[len(seq) // 2]


def sol_a() -> int:
    split = Lazy(read_lines('./input.txt')).split_when(lambda s: s == '')
    assert split is not None, 'no data in input file'
    rules, sequences = split
    rules = set(rules)
    return (
        sequences
        .map(lambda s: s.split(','))
        .filter(lambda s: is_sequence_correct(s, rules))
        .map(take_middle)
        .map(int)
        .sum()
    )


def sol_b() -> int:
    split = Lazy(read_lines('./input.txt')).split_when(lambda s: s == '')
    assert split is not None, 'no data in input file'
    rules, sequences = split
    rules = set(rules)
    return (
        sequences
        .map(lambda s: QList(s.split(',')))
        .filter(lambda s: not is_sequence_correct(s, rules))
        .map(lambda l:
            l.map(lambda s: Page(s, rules))
             .collect()
             .sorted()
             .map(lambda p: p.value)
             .collect()
        )
        .map(take_middle)
        .map(int)
        .sum()
    )


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()