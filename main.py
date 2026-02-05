import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from game_view import GameView
from start_view import StartView


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    setup_view = StartView(game_view=GameView())
    window.show_view(setup_view)
    arcade.run()

if __name__ == "__main__":
    main()