class Player:
    player_coins = {"X", "O"}

    def __init__(self, name):
        self.name = name
        self.coin = self.player_coins.pop()

    def __str__(self):
        return f"{self.name} : {self.coin}"

    def get_input(self, game_engine, retry):
        if retry:
            input_string = "Please retry with new column number: "
        else:
            input_string = f"{self.name}'s Turn. " +\
                           "Please enter a column number: "
        return int(input(input_string))
