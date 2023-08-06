class DisplayInterface:
    def __init__(self):
        self.player_1 = None
        self.player_2 = None
        self.board = None
        self.border = None

    def __str__(self):
        return f"\n\n{self.border}\n{self.player_1}\n{self.player_2}\n" +\
               f"{self.border}\n\n{self.board}"
