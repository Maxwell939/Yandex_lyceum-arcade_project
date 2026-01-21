import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from jump_game import JumpGame


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    jump_game = JumpGame()
    jump_game.setup()
    window.show_view(jump_game)
    arcade.run()

if __name__ == "__main__":
    main()