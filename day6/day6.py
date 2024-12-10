from qwlist import Lazy, QList
from utils import read_lines, Option
from typing import List, Tuple, Literal, TypeAlias, Iterable, Set, Optional

Board: TypeAlias = QList[QList["Cell"]]
DataA: TypeAlias = Tuple[int, int, str]
DataB: TypeAlias = Tuple[int, int, str, Set[Tuple[int, int]]]

class Cell:
    def __init__(self, *chars):
        self.chars = list(chars)

    def __contains__(self, item: str):
        return item in self.chars

    def set(self, value: str):
        if len(self.chars) == 1 and '' in self.chars:
            self.chars = [value]
        elif value not in self.chars:
            self.chars.append(value)

    def __repr__(self) -> str:
        if len(self.chars) == 1 and '' in self.chars:
            return '.   |'
        return f'{"".join(sorted(self.chars)):<4}|'

    def is_obstacle(self) -> bool:
        return '#' in self.chars

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

def neighbours(board: Board, x: int, y: int) -> Tuple[Option[Cell], Option[Cell], Option[Cell], Option[Cell]]:
    return (
        Option.wrap(board.get(x - 1, QList()).get(y)),
        Option.wrap(board.get(x, QList()).get(y + 1)),
        Option.wrap(board.get(x + 1, QList()).get(y)),
        Option.wrap(board.get(x, QList()).get(y - 1))
    )

def print_board(board: Board):
    print('\n'.join(board.map(lambda l: ''.join(l.map(repr)))))
    print()

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
    board[x][y].set(direction)
    dx, dy = deltas(direction)
    new_x = x + dx
    new_y = y + dy
    next_cell: Cell = board.get(new_x, QList()).get(new_y)

    # out of the maze
    if next_cell is None:
        return Option.none()

    # obstacle up front
    if '#' in next_cell:
        # __fill_between_obstacles(board, x, y, dx, dy, direction)
        return Option.some((x, y, rotate(direction), obstacles))

    # path that allows for rectangular loops
    # if rotate(direction) in next_cell and board.get(new_x + dx, QList()).get(new_y + dy, '##') != '##':
    #     obstacles.add((new_x + dx, new_y + dy))

    # path that allows for line loops
    # if rotate(rotate(direction)) in next_cell:
    #     new_dx, new_dy = deltas(rotate(direction))
    #     if '#' in board.get(new_x + dx, QList()).get(new_y + dy, ''):
    #         if '#' not in board.get(new_x + new_dx, QList()).get(new_y + new_dy, '#'):
    #             obstacles.add((new_x + new_dx, new_y + new_dy))
    return Option.some((new_x, new_y, direction, obstacles))



def __fill_between_obstacles(board: QList[QList[str]], x: int, y: int, dx: int, dy: int, direction: str):
    new_x = x - dx
    new_y = y - dy
    # go backward until an obstacle or the end of the maze is found
    while board.get(new_x, QList()).get(new_y) is not None:
        c = board[new_x][new_y]
        if '#' in c:
            break
        if direction in c:
            pass
        elif c.startswith('.'):
            board[new_x][new_y] = f'{direction}. '
        else:
            board[new_x][new_y] = f'{c[0]}{direction} '
        new_x -= dx
        new_y -= dy

def __can_line_loop_be_created(board: QList[QList[str]], x: int, y: int, direction: str, obstacles: Set[Tuple[int, int]]) -> bool:
    #....
    #...V  (x, y)
    #...^  (x + dx, y + dy)
    #...#  (x + 2 * dx, y + 2 * dy) next_char
    dx, dy = deltas(direction)
    new_x = x + 2 * dx
    new_y = y + 2 * dy
    next_char = board.get(new_x, QList()).get(new_y, '')
    if next_char == '':
        return False
    if next_char == '#':
        new_direction = rotate(direction)
        new_dx, new_dy = deltas(new_direction)
        if board.get(x + dx + new_dx, QList()).get(y + dy + new_dy, '#') != '#':
            obstacles.add((x + dx + new_dx, y + dy + new_dy))
            return True
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
    board = Lazy(read_lines('./test.txt')).map(QList).collect()
    pos = find_starting_position(board)
    board: Board = board.map(lambda row:
        row.map(lambda c:
            Cell('') if c == '.' else Cell(c)
        ).collect()
    ).collect()
    assert pos is not None, 'no data in input file'
    x, y = pos
    res = Option.some((x, y, '^', set()))
    print_board(board)
    while res.is_some():
        x, y, direction, obs = res.unwrap()
        print(obs)
        res = move_b(board, x, y, direction, obs)
        print_board(board)
        input()

    # prev = 0
    # res = (x, y, '^', set())
    # while res[0] != -1:
    #     x, y, direction, obs = res
    #     if prev != len(obs):
    #         # print_board(board)
    #         # input()
    #         prev = len(obs)
    #     res = move_b(board, x, y, direction, obs)
    # print(obs)
    return -1

def main():
    print(f'Solution a: {sol_a()}')
    # too low: 503
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()