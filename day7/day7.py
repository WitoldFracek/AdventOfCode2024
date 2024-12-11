from qwlist import Lazy, QList
from utils import read_lines
from typing import List, Callable, Dict


def to_base_n(number: int, base: int, digits: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    if base < 2 or base > 36:
        raise ValueError(f'base must be between 2 and 37')
    if number == 0:
        return "0"
    is_negative = number < 0
    number = abs(number)
    result = []
    while number:
        result.append(digits[number % base])
        number //= base
    if is_negative:
        result.append('-')
    return ''.join(reversed(result))


def concat(a: int, b: int) -> int:
    return int(f'{a}{b}')


def is_solvable(
        target: int,
        args: List[int],
        operators: List[Callable[[int, int], int]],
        digits: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
) -> bool:
    base = len(operators)
    ops: Dict[str, Callable[[int, int], int]] = {c: op for c, op in zip(digits, operators)}
    args = QList(args)
    operators = 0
    ops_str = f"{to_base_n(operators, base, digits=digits):0>{args.len()}}"
    while ops_str.startswith('0'):
        score = args[0]
        for (x, op) in args.zip(ops_str).skip(1):
            score = ops[op](score, x)
            if score > target:
                break
        if score == target:
            return True
        operators += 1
        ops_str = f"{to_base_n(operators, base, digits=digits):0>{args.len()}}"
    return False


def sol_a() -> int:
    operators = [int.__add__, int.__mul__]
    return (
        Lazy(read_lines('./input.txt'))
        .map(lambda x: x.split(':'))
        .map(lambda pair: (
            pair[0],
            Lazy(pair[1].split(' '))
                .filter(lambda x: x != '')
                .map(int)
                .collect()
            )
        )
        .map(lambda pair: (int(pair[0]), pair[1]))
        .filter(lambda pair: is_solvable(pair[0], pair[1], operators))
        .map(lambda pair: pair[0])
        .collect()
        .sum()
    )


def sol_b() -> int:
    operators = [int.__add__, int.__mul__, concat]
    return (
        Lazy(read_lines('./input.txt'))
        .map(lambda x: x.split(':'))
        .map(lambda pair: (
                pair[0],
                Lazy(pair[1].split(' '))
                .filter(lambda x: x != '')
                .map(int)
                .collect()
            )
        )
        .map(lambda pair: (int(pair[0]), pair[1]))
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