from qwlist import Lazy, QList
from utils import read_lines
from typing import List, Tuple, Literal

def find_starting_position(board: List[List[str]]) -> Tuple[int, int] | None:
    for i, row in enumerate(board):
        for j, c in enumerate(row):
            if c == '^':
                return i, j
    return None

def rotate(direction: str) -> str:
    return {'^': '>', '>': 'V', 'V': '<', '<': '^'}.get(direction, direction)

def print_board(board: QList[QList[str]]):
    print('\n'.join(board.map(lambda l: ''.join(l))))
    print()

def move(board: QList[QList[str]], x: int, y: int, direction: Literal['^', '<', 'V', '>']) -> Tuple[int, int, str] | None:
    deltas = {'^': (-1, 0), 'V': (1, 0), '<': (0, -1), '>': (0, 1)}
    dx, dy = deltas[direction]
    new_x = x + dx
    new_y = y + dy
    row = board.get(new_x)
    board[x][y] = 'X'
    if row is None:
        return None
    c = row.get(new_y)
    if c is None:
        return None
    if c == '#':
        return x, y, rotate(direction)
    return new_x, new_y, direction

def move_b(board: QList[QList[str]], x: int, y: int, direction: Literal['U', 'L', 'D', 'R'], acc: int, prev_x, prev_y) -> Tuple[int, int, str, int]:
    deltas = {'^': (-1, 0), 'V': (1, 0), '<': (0, -1), '>': (0, 1)}
    dx, dy = deltas[direction]
    if rotate(direction) == board[x][y] and board.get(x + dx, QList()).get(y + dy, '') != '':
        # found cycle
        print('\033[91mCycle', x, y, '\033[0m')
        acc += 1
    if prev_x == x and prev_y == y:
        print(direction)
        if rotate(rotate(direction)) == board[x][y]:
            # found cycle
            print('\033[91mCycle', x, y, '\033[0m')
            acc += 1
    board[x][y] = direction
    new_x = x + dx
    new_y = y + dy
    row = board.get(new_x)
    if row is None:
        return -1, -1, '', acc
    c = row.get(new_y)
    if c is None:
        return -1, -1, '', acc
    if c == '#':
        new_x = x - dx
        new_y = y - dy
        while board.get(new_x, QList()).get(new_y) is not None:
            c = board[new_x][new_y]
            if c == '#':
                break
            board[new_x][new_y] = direction
            new_x -= dx
            new_y -= dy
        return x, y, rotate(direction), acc
    return new_x, new_y, direction, acc


def sol_a() -> int:
    board = Lazy(read_lines('./input.txt')).map(QList).collect()
    pos = find_starting_position(board)
    assert pos is not None, 'no data in input file'
    x, y = pos
    res = (x, y, '^')
    while res:
        x, y, direction = res
        res = move(board, x, y, direction)
    return board.flatten().filter(lambda s: s == 'X').collect().len()


def sol_b() -> int:
    board = Lazy(read_lines('./test.txt')).map(QList).collect()
    pos = find_starting_position(board)
    assert pos is not None, 'no data in input file'
    x, y = pos
    prev = 0
    res = (x, y, '^', 0)
    while res[0] != -1:
        x, y, direction, acc = res
        if acc != prev:
            prev = acc
            print_board(board)
            input()
        res = move_b(board, x, y, direction, acc, -1, -1)
    return acc


def main():
    print(f'Solution a: {sol_a()}')
    # too low: 503
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()