import os
import sys
import arcade
from pyglet.graphics import Batch
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

class StartView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.game_view = game_view
        self.start_text = None
        self.any_key_text1 = None
        self.any_key_text2 = None
        self.batch = None
        font_path = os.path.join(BASE_PATH, "fonts", "PressStart2P-Regular.ttf")
        arcade.load_font(font_path)

    def on_draw(self) -> None:
        self.clear()
        self.batch = Batch()
        self.start_text = arcade.Text(SCREEN_TITLE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE,
                                      font_size=30, font_name="Press Start 2P", anchor_x="center", batch=self.batch)
        self.any_key_text1 = arcade.Text("Нажмите любую", self.window.width / 2,
                                         self.window.height / 2 - 75, arcade.color.GRAY, font_size=15,
                                         font_name="Press Start 2P", anchor_x="center", batch=self.batch)
        self.any_key_text2 = arcade.Text("клавишу для запуска", self.window.width / 2, self.window.height / 2 - 75 - 30,
                                         arcade.color.GRAY, font_size=15, font_name="Press Start 2P",
                                         anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.game_view.setup()
        self.window.show_view(self.game_view)