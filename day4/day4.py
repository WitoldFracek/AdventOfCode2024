from qwlist import Lazy, QList
from utils import read_lines

def search_horizontal(data: QList[str]) -> int:
     return (
        data
        .flatmap(lambda l:
            Lazy(l)
            .window(4)
            .map(lambda b: b.sum())
            .filter(lambda s: s == 'XMAS' or s == 'SAMX')
        )
        .collect()
        .len()
    )

def search_vertical(data: QList[str]) -> int:
    return (
        Lazy(zip(*data))
        .map(Lazy)
        .flatmap(lambda l:
            l.window(4)
             .map(lambda b: b.sum())
             .filter(lambda s: s == 'XMAS' or s == 'SAMX')
        )
        .collect()
        .len()
    )

def search_diagonal(data: QList[str], diag_len: int, patterns: set[str], on_both_at_once: bool = False) -> int:
    len_ = len(data[0])
    count = 0
    for batch in data.window(diag_len).map(lambda b: b.map(QList).collect()):
        for i in range(len_ - diag_len + 1):
            d1 = ''.join(batch[j][i + j] for j in range(diag_len))
            d2 = ''.join(batch[diag_len - 1 - j][i + j] for j in range(diag_len))
            if on_both_at_once:
                if d1 in patterns and d2 in patterns:
                    count += 1
            else:
                if d1 in patterns:
                    count += 1
                if d2 in patterns:
                    count += 1
    return count

def sol_a() -> int:
    lines = QList(read_lines('./input.txt'))
    hor = search_horizontal(lines)
    ver = search_vertical(lines)
    dia = search_diagonal(lines, diag_len=4, patterns={'XMAS', 'SAMX'})
    return dia + hor + ver


def sol_b() -> int:
    lines = QList(read_lines('./input.txt'))
    count = search_diagonal(lines, diag_len=3, patterns={'SAM', 'MAS'}, on_both_at_once=True)
    return count


def main():
    # too low: 1439
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()