from qwlist import Lazy, QList
from utils import read_lines, Option
from typing import Tuple, TypeAlias, Iterable, Set

Board: TypeAlias = QList[QList["Cell"]]
DataA: TypeAlias = Tuple[int, int, str]
DataB: TypeAlias = Tuple[int, int, str, Set[Tuple[int, int]]]

class Cell:
    def __init__(self, *chars):
        self.chars = list(chars)
        self.is_marked = False

    def __contains__(self, item: str):
        return item in self.chars

    def add(self, value: str):
        if value not in self.chars:
            self.chars.append(value)

    def remove(self, value: str):
        if value in self.chars:
            self.chars.remove(value)

    def is_obstacle(self) -> bool:
        return '#' in self.chars

    def is_visited(self) -> bool:
        return len(self.chars) != 0


def find_starting_position(board: Iterable[Iterable[str]]) -> Tuple[int, int] | None:
    for i, row in enumerate(board):
        for j, c in enumerate(row):
            if c == '^':
                return i, j
    return None


def rotate(direction: str) -> str:
    return {'^': '>', '>': 'V', 'V': '<', '<': '^'}.get(direction, direction)


def deltas(direction: str) -> Tuple[int, int]:
    return {'^': (-1, 0), 'V': (1, 0), '<': (0, -1), '>': (0, 1)}[direction]


def neighbour(board: Board, x: int, y: int, direction: str) -> Option[Cell]:
    dx, dy = deltas(rotate(direction))
    return Option.wrap(board.get(x + dx, QList()).get(y + dy))


def move(board: Board, x: int, y: int, direction: str) -> Option[DataA]:
    dx, dy = deltas(direction)
    new_x = x + dx
    new_y = y + dy
    row = board.get(new_x)
    board[x][y] = 'X'
    if row is None:
        return Option.none()
    c = row.get(new_y)
    if c is None:
        return Option.none()
    if c == '#':
        return Option.some((x, y, rotate(direction)))
    return Option.some((new_x, new_y, direction))

def move_b(board: Board, x: int, y: int, direction: str, obstacles: Set[Tuple[int, int]]) -> Option[DataB]:
    board[x][y].add(direction)
    dx, dy = deltas(direction)
    new_x = x + dx
    new_y = y + dy
    next_cell: Cell = board.get(new_x, QList()).get(new_y)

    if next_cell is None:
        return Option.none()

    if next_cell.is_obstacle():
        return Option.some((x, y, rotate(direction), obstacles))

    if __can_loop(board, x, y, direction):
        obstacles.add((new_x, new_y))
    return Option.some((new_x, new_y, direction, obstacles))


def __can_loop(board: Board, x: int, y: int, direction: str) -> bool:
    tx, ty = deltas(direction)
    obs_x = x + tx
    obs_y = y + ty
    if board[obs_x][obs_y].is_visited():
        return False
    if rotate(direction) in board[x][y]:
        return True

    board[obs_x][obs_y].add('#')
    steps = set()

    direction = rotate(direction)
    dx, dy = deltas(direction)
    next_cell: Option[Cell] = Option.wrap(board.get(x + dx, QList()).get(y + dy))
    while next_cell.is_some():
        if next_cell.unwrap().is_obstacle():
            if (x, y, direction) in steps:
                board[obs_x][obs_y].remove('#')
                return True
            steps.add((x, y, direction))
            direction = rotate(direction)
            dx, dy = deltas(direction)
            next_cell = Option.wrap(board.get(x + dx, QList()).get(y + dy))
            continue
        x += dx
        y += dy
        next_cell = Option.wrap(board.get(x + dx, QList()).get(y + dy))
    board[obs_x][obs_y].remove('#')
    return False


def sol_a() -> int:
    board = Lazy(read_lines('./input.txt')).map(QList).collect()
    pos = find_starting_position(board)
    assert pos is not None, 'no data in input file'
    x, y = pos
    res = Option.some((x, y, '^'))
    while res.is_some():
        x, y, direction = res.unwrap()
        res = move(board, x, y, direction)
    return board.flatten().filter(lambda s: s == 'X').collect().len()


def sol_b() -> int:
    board = Lazy(read_lines('./input.txt')).map(lambda s: QList(s)).collect()
    pos = find_starting_position(board)
    board: Board = board.map(lambda row:
        row.map(lambda c:
            Cell() if c == '.' else Cell(c)
        ).collect()
    ).collect()
    assert pos is not None, 'no data in input file'
    x, y = pos
    obstacles = set()
    res = Option.some((x, y, '^', obstacles))
    while res.is_some():
        x, y, direction, obstacles = res.unwrap()
        res = move_b(board, x, y, direction, obstacles)
    return len(obstacles)

def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()