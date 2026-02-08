# game_state.py
from config import *

class GameState:
    def __init__(self):
        self.state = "MENU"
        self.timer = GAME_LENGTH

    def update(self):
        if self.state == "PLAYING":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "CUTSCENE"
                return "CUTSCENE"

        return None

    def reset(self):
        self.state = "PLAYING"
        self.timer = GAME_LENGTH
