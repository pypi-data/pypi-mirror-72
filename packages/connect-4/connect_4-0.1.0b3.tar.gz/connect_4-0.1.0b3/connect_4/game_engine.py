from connect_4.player import Player
from connect_4.connect_four_interface import ConnectFourInterface
from connect_4.board import Board
from connect_4.random_bot import RandomBot
from random import shuffle
from connect_4.board import BoardFullError


class GameEngine:
    def __init__(self):
        self.player_1 = self.choose_player(1)
        self.player_2 = self.choose_player(2)
        self.board = Board()
        self.display = ConnectFourInterface(
            self.player_1,
            self.player_2,
            self.board
        )

    def choose_player(self, no):
        player_name = input(
            f"Enter player {no}'s name or leave blank to use a bot: "
        )
        if player_name:
            return Player(player_name)
        else:
            return RandomBot(f"Bot {no}")

    def play(self, current_player, next_player, retry=False):
        if self.board.is_filled():
            return False
        if not retry:
            print(self.display)
        column = current_player.get_input(self, retry)
        try:
            won = self.board.insert_coin(column, current_player.coin, self)
            if won:
                return current_player
        except BoardFullError as error:
            print(error)
            return self.play(current_player, next_player, True)
        return self.play(next_player, current_player)

    def start_game(self):
        print("Starting game....")
        players = [self.player_1, self.player_2]
        shuffle(players)
        first_player = players.pop()
        second_player = players.pop()

        winner = self.play(first_player, second_player)
        if winner:
            self.display.win(winner)
        else:
            self.display.draw()


def main():
    engine = GameEngine()
    engine.start_game()


if __name__ == "__main__":
    main()
