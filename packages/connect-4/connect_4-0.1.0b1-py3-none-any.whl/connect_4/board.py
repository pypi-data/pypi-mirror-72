from connect_4.clear_screen import clear


class Board:
    def __init__(self, size=7):
        self.size = size
        self.blank = '-'
        self.board = [
            [self.blank for _ in range(self.size)] for _ in range(self.size)
        ]
        self.filled_columns = set()
        self.border = '_' * (self.size * 8 - 7)

    def __str__(self):
        clear()
        board = '\n\n'.join(
            '\t'.join(row) for row in self.board
        )
        row_numbers = '\t'.join([str(i + 1) for i in range(self.size)])
        return f"{board}\n{self.border}\n{row_numbers}\n"

    def is_filled(self):
        return len(self.filled_columns) == self.size

    def has_won(self, row, column):
        win_pattern = self.board[row][column] * 4
        valid_pos = lambda cell, offset: \
            cell + offset >= 0 and cell + offset < self.size

        # This variable will represent vertical direction
        vertical = ''

        # This variable will represent horizontal direction
        horizontal = ''

        # These variables will represent diagonal directions
        diagonal_left = ''
        diagonal_right = ''

        for offset in range(-3, 4):
            if valid_pos(row, offset):
                vertical += self.board[row + offset][column]
            if valid_pos(column, offset):
                horizontal += self.board[row][column + offset]
            if valid_pos(row, offset) and valid_pos(column, offset):
                diagonal_left += self.board[row + offset][column + offset]
            if valid_pos(row, -offset) and valid_pos(column, offset):
                diagonal_right += self.board[row - offset][column + offset]
        print(vertical, horizontal, diagonal_left, diagonal_right, sep="\n")
        for patterns in (vertical, horizontal, diagonal_left, diagonal_right):
            if win_pattern in patterns:
                return True
        return False

    def insert_coin(self, column, coin, engine):
        column -= 1
        for row in range(self.size - 1, -1, -1):
            if row == 0:
                self.filled_columns.add(column)
            if self.board[row][column] == self.blank:
                engine.display.animate(row, column, coin)
                return self.has_won(row, column)

        raise BoardFullError("Can't insert any more coins in this row")


class BoardFullError(Exception):
    def __init__(self, message):
        super().__init__(message)
