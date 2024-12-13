from qwlist import Lazy, QList
from utils import read_lines
from typing import TypeAlias, Tuple

Board: TypeAlias = QList[QList[str]]
Node: TypeAlias = Tuple[int, int]


def antinode_pair(n1: Node, n2: Node) -> Tuple[Node, Node]:
    x1, y1 = n1
    x2, y2 = n2
    return (2 * x2 - x1, 2 * y2 - y1), (2 * x1 - x2, 2 * y1 - y2)


def antinode_list(n1: Node, n2: Node, max_x: int, max_y: int) -> QList[Node]:
    x1, y1 = n1
    x2, y2 = n2
    ret = QList([n1, n2])
    ax, ay = 2 * x2 - x1, 2 * y2 - y1
    while 0 <= ax < max_x and 0 <= ay < max_y:
        ret.append((ax, ay))
        ax += x2 - x1
        ay += y2 - y1
    ax, ay = 2 * x1 - x2, 2 * y1 - y2
    while 0 <= ax < max_x and 0 <= ay < max_y:
        ret.append((ax, ay))
        ax += x1 - x2
        ay += y1 - y2
    return ret


def antinodes_a(nodes: QList[Node]) -> Lazy[Node]:
    return (
        nodes.enumerate(start=1).flatmap(lambda in1:
            nodes.skip(in1[0]).map(lambda n2:
                antinode_pair(in1[1], n2)
            )
        )
    ).flatmap(lambda pair: [pair[0], pair[1]])


def antinodes_b(nodes: QList[Node], max_x: int, max_y: int) -> Lazy[Node]:
    return (
        nodes.enumerate(start=1).flatmap(lambda in1:
            nodes.skip(in1[0]).flatmap(lambda n2:
                antinode_list(in1[1], n2, max_x, max_y)
            )
        )
    )

def sol_a() -> int:
    board: Board = QList(read_lines('./input.txt')).map(lambda x: QList(x)).collect()
    return len(set(
        board
        .enumerate()
        .flatmap(lambda irow:
            irow[1]
            .enumerate()
            .filter(lambda pair: pair[1] != '.')
            .map(lambda pair: (irow[0], pair[0]))
        )
        .group_by(lambda coords: board[coords[0]][coords[1]])
        .map(antinodes_a)
        .flatmap(lambda group:
            group.filter(lambda node:
                board.get(node[0], QList()).get(node[1]) is not None
            )
        )
    ))


def sol_b() -> int:
    board: Board = QList(read_lines('./input.txt')).map(lambda x: QList(x)).collect()
    max_x = board.len()
    max_y = board.get(0, QList()).len()
    return len(set(
        board
        .enumerate()
        .flatmap(lambda irow:
            irow[1]
            .enumerate()
            .filter(lambda pair: pair[1] != '.')
            .map(lambda pair: (irow[0], pair[0]))
        )
        .group_by(lambda coords: board[coords[0]][coords[1]])
        .map(lambda group: antinodes_b(group, max_x, max_y))
        .flatten()
    ))


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()
