from connect_4.player import Player
from random import choice
from time import sleep


class RandomBot(Player):
    def __init__(self, name="Random Bot"):
        super().__init__(name)

    def get_input(self, game_engine, retry):
        column = choice(range(game_engine.board.size)) + 1
        if retry:
            input_string = "Please retry with new column number: "
        else:
            input_string = f"{self.name}'s Turn. " +\
                           "Please enter a column number: "
        print(input_string, end='', flush=True)
        sleep(1)
        print(column)
        sleep(2)
        return column
