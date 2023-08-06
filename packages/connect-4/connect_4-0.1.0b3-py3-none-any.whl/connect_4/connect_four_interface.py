from connect_4.interface import DisplayInterface
from time import sleep


class ConnectFourInterface(DisplayInterface):
    def __init__(self, player_1, player_2, board):
        self.board = board
        self.border = self.board.border
        self.player_1 = player_1
        self.player_2 = player_2

    def animate(self, row, column, coin):
        for r in range(row + 1):
            if r > 0:
                self.board.board[r - 1][column] = self.board.blank
            self.board.board[r][column] = coin
            print(self)
            sleep(.2)

    def win(self, winner):
        border = f"{self.border.replace('_', '*')}\n" * 2
        print_text = f"{winner.name}({winner.coin}) has won the game"
        remaining_space = len(self.border) - len(print_text)
        print_text = f"{' ' * round(remaining_space / 2)}{print_text}"
        print(f"{border}{self.board}{border}{print_text}\n{border}")

    def draw(self):
        border = f"{self.border.replace('_', '*')}\n" * 2
        print(f"{border}{self.board}{border}This game is a draw\n{border}")

