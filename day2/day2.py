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
    fix_batches = seq.window(3).batch_by(is_correct_seq).collect()
    # if all windows are correct then the whole sequence is correct
    if fix_batches.len() == 1 and is_correct_seq(fix_batches[0][0]):
        return True

    # if there are 2 groups the error was at the beginning or at the end
    if fix_batches.len() == 2:
        # left = beginning, right = end
        left, right = fix_batches
        if not is_correct_seq(left[0]):
            if left.len() > 2:
                return False
            if left.len() == 1:
                return True
            l, r = left
            return is_correct_seq(r) or is_correct_seq(QList([l[0], r[1], r[2]])) or is_correct_seq(QList([l[0], l[1], r[2]]))
        else:
            if right.len() > 2:
                return False
            if right.len() == 1:
                return True
            l, r = right
            return is_correct_seq(l) or is_correct_seq(QList([l[0], r[1], r[2]])) or is_correct_seq(QList([l[0], l[1], r[2]]))

    # if there are 3 groups, only the middle one can contain errors.
    # Otherwise, we have 2 separate errors which cannot be corrected.
    if fix_batches.len() == 3:
        _, mid, _ = fix_batches
        if not is_correct_seq(mid[0]) and mid.len() < 3:
            # if the group is of length 1 it means we found a switch point of sequence monotonic (7 6 5 4 5 6 cannot be fixed)
            if mid.len() == 1:
                return False
            l, r = mid
            return is_correct_seq(QList([l[0], r[1], r[2]])) or is_correct_seq(QList([l[0], l[1], r[2]]))

    # if there is more groups than 3 we have at least 2 separate errors
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
