class Cell:
    def __init__(self, value=None):
        self._value = value
        self._possible = set(range(1,10))
        if value:
            self._possible.remove(value)

    def possibilities(self):
        return self._possible

    def add_possibility(self, value):
        self._possible.add(value)

    def set_value(self, value):
        if self._value:
            self._possible.add(self._value)
            self._possible.remove(value)
        self._possible.remove(value)
        self._value = value

    def value(self):
        return self._value

    def __repr__(self):
        return f"{{value: {self._value}, possibilities: {self._possible}}}"


class Board:
    def __init__(self, board = None):
        self._board = board if board is not None else [Cell() for c in range(0,81)]
        self._row_board = [self._board[Board._calculate_row_index(i)] for i in range(0, 81)]
        self._field_board = [self._board[Board._calculate_field_index(i)] for i in range(0,81)]

    @staticmethod
    def _calculate_row_index(i):
        return (i // 9)+ 9 * (i % 9)

    @staticmethod
    def _calculate_field_index(i):
        block_nr = i // 9
        col = block_nr % 3
        row = block_nr // 3
        block_idx = i % 9
        return (block_idx % 3) + 3 * col + block_idx // 3 * 9 + 27 * row

    def board(self):
        return self._board

    def row_board(self):
        return self._row_board

    def field_board(self):
        return self._field_board

    def find_square(self):
        f = list(filter(lambda c: c.value() is None, self._board))
        if len(f) == 0:
            return None
        return min(f, key=lambda c: len(c.possibilities()))

    @staticmethod
    def _check_number(l):
        for i in range(1,10):
            if i not in l:
                return False
        return True

    def is_solved(self):
        for i in range(0,9):
            board_slice = self._board[i*9:(i+1)*9]
            print(board_slice)


class Backtracking(Board):
    def solve(self):
        cell = self.find_square()
        if cell:
            idx = self.board().index(cell)
            for possibility in cell.possibilities():
                tmp = Backtracking(list(self.board()))
                tmp.board()[idx].set_value(possibility)
                tmp.solve()
                if tmp.is_solved():
                    return tmp.board()
        return None


sudoku_list = list("634200000002300007000900005000000736000023000048000000590000000000005410000031000")
sudoku = list(map(lambda c: Cell(c), map(lambda c: None if c == 0 else c, map(lambda c: int(c), sudoku_list))))
b = Backtracking(sudoku)
b.solve()