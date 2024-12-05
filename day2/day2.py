from qwlist import Lazy, QList
from utils import read_lines


def count_diff(values: QList[int]) -> QList[int]:
    return values.window(2).map(lambda w: w[0] - w[1]).collect()


def is_correct_seq(seq: QList[int]) -> bool:
    diffs = count_diff(seq)
    if diffs.all(lambda x: 0 < x < 4):
        return True
    if diffs.all(lambda x: -4 < x < 0):
        return True
    return False


def is_correct_with_removal(seq: QList[int]) -> bool:
    fix_batches = (
        seq
        .window(3)
        .map(is_correct_seq)
        .batch_by(lambda x: x)
        .collect()
    )
    if fix_batches.len() == 1 and fix_batches[0][0]:
        return True
    if fix_batches.len() == 2:
        left, right = fix_batches
        if not left[0] and left.len() == 1:
            return True
        if not right[0] and right.len() == 1:
            return True
    if fix_batches.len() == 3:
        _, mid, _ = fix_batches
        if not mid[0] and mid.len() < 4:
            return True
    return False


def is_correct_with_removal_brute(seq: QList[int]) -> bool:
    if is_correct_seq(seq):
        return True
    for i in range(seq.len()):
        sub = QList(seq[:i] + seq[i+1:])
        if is_correct_seq(sub):
            return True
    return False


def sol_a() -> int:
    return (
        Lazy(read_lines('./input.txt'))
        .map(lambda x: QList(x.split(' ')).map(int).collect())
        .filter(is_correct_seq)
        .collect()
        .len()
    )


def sol_b() -> int:
    return (
        Lazy(read_lines('./input.txt'))
        .map(lambda x: QList(x.split(' ')).map(int).collect())
        .filter(is_correct_with_removal)
        .collect()
        .len()
    )


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()
