import arcade
import sys
import os

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from game_view import GameView
from start_view import StartView

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    setup_view = StartView(game_view=GameView())
    window.show_view(setup_view)
    arcade.run()

if __name__ == "__main__":
    main()